from dataclasses import dataclass
from typing import List, Optional, Dict
from uuid import UUID

from nolabs.exceptions import NoLabsException, ErrorCodes
from nolabs.workflow.application.models import WorkflowSchemaDbModel
from nolabs.workflow.component_factory import PythonComponentFactory
from nolabs.workflow.component import PythonComponent
from nolabs.workflow.workflow_schema import WorkflowSchemaModel, WorkflowComponentModel, JobValidationError


@dataclass
class WorkflowValidationError:
    msg: str


class Workflow:
    running: bool
    executing_workflows: Dict[UUID, 'Workflow']
    workflow_schema: WorkflowSchemaModel
    factory: PythonComponentFactory

    def __init__(self, workflow_schema: WorkflowSchemaModel, factory: PythonComponentFactory):
        self.workflow_schema = workflow_schema
        self.factory = factory

    async def execute(self):
        try:
            db_model: WorkflowSchemaDbModel = WorkflowSchemaDbModel.objects.with_id(self.workflow_schema.workflow_id)

            self.running = True

            components = self.create_from_schema(workflow_schema=self.workflow_schema, component_factory=self.factory)

            async def execute(component: PythonComponent):
                for previous in component.previous:
                    await execute(previous)

                    validation_errors = previous.validate_output()

                    if validation_errors:
                        self.workflow_schema.get_wf_component(previous.id).error = ', '.join(
                            [ve.msg for ve in validation_errors])
                        self.workflow_schema.valid = False
                        db_model.set_workflow_value(self.workflow_schema)
                        db_model.save()

                    return

                input_changed = component.set_input_from_previous()

                if not input_changed:
                    return

                validation_errors = component.validate_input()

                if validation_errors:
                    self.workflow_schema.get_wf_component(component.id).error = ', '.join(
                        [ve.msg for ve in validation_errors])
                    db_model.set_workflow_value(self.workflow_schema)
                    db_model.save()
                    return

                await component.setup_jobs()

                jobs_validation_errors = await component.prevalidate_jobs()

                if jobs_validation_errors:
                    self.workflow_schema.get_wf_component(component.id).error = [JobValidationError(
                        job_id=ve.job_id,
                        msg=ve.msg
                    ) for ve in jobs_validation_errors]
                else:
                    self.workflow_schema.get_wf_component(component.id).jobs_errors = []
                    db_model.set_workflow_value(self.workflow_schema)
                    db_model.save()

                await component.execute()

            for component in components:
                await execute(component=component)

        finally:
            self.running = False

    @staticmethod
    def validate_graph(graph: List[PythonComponent]) -> Optional[WorkflowValidationError]:
        if not graph:
            return WorkflowValidationError(
                msg='Workflow graph is empty'
            )

        if Workflow.is_cyclic(graph):
            return WorkflowValidationError(
                msg='Workflow graph must be acyclic'
            )

        return None

    @classmethod
    def validate_schema(
            cls,
            workflow_schema: WorkflowSchemaModel,
            component_factory: PythonComponentFactory
    ) -> bool:
        components: List[PythonComponent] = [
            component_factory.create_component_instance(name=wf.name, id=wf.component_id) for wf in
            workflow_schema.workflow_components
        ]

        if Workflow.validate_graph(graph=components):
            return False

        for workflow_component in workflow_schema.workflow_components:
            # Check that component exists
            if not component_factory.component_exists(name=workflow_component.name):
                return False

            component = component_factory.create_component_instance(name=workflow_component.name,
                                                                    id=workflow_component.component_id)

            # Check that component mappings exist
            for mapping in workflow_component.mappings:
                source_components = [c for c in workflow_schema.workflow_components if
                                     c.component_id == mapping.source_component_id]
                if not source_components:
                    return False

                if not source_components:
                    return False

                source_component = component_factory.create_component_instance(name=source_components[0].name,
                                                                               id=source_components[0].component_id)

                component.add_previous(component=source_component)
                error = component.try_map_property(component=source_component,
                                                   path_from=mapping.source_path,
                                                   path_to=mapping.target_path)

                if error:
                    return False

            for default in workflow_component.defaults:
                error = component.try_set_default(default.path_to, value=default.value)

                if error:
                    return False

        return True

    @classmethod
    def create_from_schema(cls,
                           workflow_schema: WorkflowSchemaModel,
                           component_factory: PythonComponentFactory) -> List[PythonComponent]:
        valid = cls.validate_schema(
            workflow_schema=workflow_schema,
            component_factory=component_factory)

        if not valid:
            raise NoLabsException(ErrorCodes.invalid_workflow_schema,
                                  f'Run {cls.set_schema_errors} to get schema errors')

        components: List[PythonComponent] = []

        component: WorkflowComponentModel
        for component in workflow_schema.workflow_components:
            components.append(
                component_factory.create_component_instance(name=component.name, id=component.component_id)
            )

        for workflow_component in workflow_schema.workflow_components:
            component: PythonComponent = [c for c in components if c.id == workflow_component.component_id][0]

            if not component:
                raise NoLabsException(ErrorCodes.component_not_found)

            # Check that component mappings exist
            for mapping in workflow_component.mappings:
                source_component: PythonComponent = [c for c in components if c.id == mapping.source_component_id][0]

                component.add_previous(component=source_component)
                component.try_map_property(component=source_component,
                                           path_from=mapping.source_path,
                                           path_to=mapping.target_path)

            for default in workflow_component.defaults:
                component.try_set_default(default.path_to, value=default.value)

        return components

    @classmethod
    def set_schema_errors(
            cls,
            workflow_schema: WorkflowSchemaModel,
            component_factory: PythonComponentFactory):
        component_not_found_template = lambda c_id: f'Component with id {c_id} not found'

        schema_valid = True

        for component in workflow_schema.workflow_components:
            if component.name not in [c_name for c_name in component_factory.components.keys()]:
                component.error = f'Component with name {component.name} not found'
                workflow_schema.valid = False
                return

        components: List[PythonComponent] = [
            component_factory.create_component_instance(name=wf.name, id=wf.component_id) for wf in
            workflow_schema.workflow_components
        ]

        graph_validation_error = Workflow.validate_graph(graph=components)

        if graph_validation_error:
            workflow_schema.error = graph_validation_error.msg

        if Workflow.validate_graph(graph=components):
            workflow_schema.error = 'Workflow must be acyclic'
            schema_valid = False

        for workflow_component in workflow_schema.workflow_components:
            # Check that component exists
            if not component_factory.component_exists(name=workflow_component.name):
                workflow_component.error = component_not_found_template(workflow_component.component_id)
                schema_valid = False
                continue

            component: PythonComponent = component_factory.create_component_instance(name=workflow_component.name,
                                                                                     id=workflow_component.component_id)

            # Check that component mappings exist
            for mapping in workflow_component.mappings:
                source_components = [c for c in workflow_schema.workflow_components if
                                     c.component_id == mapping.source_component_id]
                if not source_components:
                    raise NoLabsException(ErrorCodes.component_not_found)

                source_component = component_factory.create_component_instance(name=source_components[0].name,
                                                                               id=source_components[0].component_id)

                component.add_previous(component=source_component)

                error = component.try_map_property(component=source_component,
                                                   path_from=mapping.source_path,
                                                   path_to=mapping.target_path)

                if error:
                    mapping.error = error.msg
                    schema_valid = False

            for default in workflow_component.defaults:
                error = component.try_set_default(path_to=default.path_to, value=default.value)
                if error:
                    default.error = error.msg
                    schema_valid = False

        workflow_schema.valid = schema_valid
        return schema_valid

    @staticmethod
    def is_cyclic(graph: List[PythonComponent]) -> bool:
        visited: Set[WorkflowGraphNode] = set()  # type: ignore
        recursion_stack = set()

        def dfs(vertex: PythonComponent):
            if vertex in recursion_stack:
                return True
            if vertex in visited:
                return False

            visited.add(vertex)
            recursion_stack.add(vertex)

            for neighbor in vertex.previous:
                if dfs(neighbor):  # type: ignore # TODO Change later
                    return True

            recursion_stack.remove(vertex)
            return False

        for vertex in graph:
            if vertex not in visited:
                if dfs(vertex):
                    return True

        return False
