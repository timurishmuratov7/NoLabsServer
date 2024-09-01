import asyncio
import datetime
import uuid
from collections import defaultdict, deque
from typing import List, Optional, Dict, Any, Set
from uuid import UUID

from prefect import flow
from prefect.context import get_run_context

from nolabs.application.workflow.data import WorkflowState, WorkflowRunModel
from nolabs.application.workflow.workflow import Component
from nolabs.infrastructure.environment import Environment
from nolabs.infrastructure.settings import Settings


class PrefectDagExecutor:
    _settings: Settings

    def __init__(self):
        self._settings = Settings.load()

    async def execute(self, workflow_id: UUID, components: List[Component], extra: Optional[Dict[str, Any]] = None):
        dag = generate_workflow_dag(workflow_id=workflow_id, components=components, extra=extra)

        if self._settings.get_environment() == Environment.LOCAL:
            await dag()


def generate_workflow_dag(workflow_id: uuid.UUID, components: List[Component], extra: Optional[Dict[str, Any]] = None):
    @flow(name=str(workflow_id), flow_run_name=f'workflow-{str(workflow_id)}')
    async def workflow():
        ctx = get_run_context()
        flow_run_id = ctx.flow_run.id

        state: WorkflowState = WorkflowState.objects.with_id(workflow_id)
        state.runs.append(WorkflowRunModel.create(flow_run_id=flow_run_id, created_at=datetime.datetime.utcnow()))
        state.save()

        component_map: Dict[uuid.UUID, Component] = {c.id: c for c in components}

        in_degree: Dict[uuid.UUID, int] = defaultdict(int)
        adj_list: Dict[uuid.UUID, Set[uuid.UUID]] = defaultdict(set)

        for component in components:
            for prev_id in component.previous_component_ids:
                adj_list[prev_id].add(component.id)
                in_degree[component.id] += 1

        queue = deque([c.id for c in components if in_degree[c.id] == 0])

        while queue:
            parallel_group = []

            for _ in range(len(queue)):
                current_id = queue.popleft()
                current_component = component_map[current_id]
                parallel_group.append(current_component)

            group = [
                c.component_flow_type(
                    component_id=c.id,
                    component_name=c.name,
                    workflow_id=workflow_id,
                    extra=extra
                ).execute()
                for c in parallel_group
            ]

            await asyncio.gather(*group)

            for component in parallel_group:
                for dependent_id in adj_list[component.id]:
                    in_degree[dependent_id] -= 1

                    if in_degree[dependent_id] == 0:
                        queue.append(dependent_id)

    return workflow
