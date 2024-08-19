import uuid
from datetime import datetime
from typing import Any, Dict, List, TYPE_CHECKING

from mongoengine import ReferenceField, UUIDField, Document, DictField, CASCADE, ListField, DateTimeField, StringField, \
    EmbeddedDocumentListField, IntField, EmbeddedDocument

from nolabs.application.workflow.schema import WorkflowSchema
from nolabs.domain.models.common import Experiment

if TYPE_CHECKING:
    from nolabs.application.workflow.component import Component


class InputPropertyErrorDbModel(EmbeddedDocument):
    loc: List[str] = ListField(StringField())
    msg: str = StringField()

    @classmethod
    def create(cls, loc: List[str], msg: str) -> 'InputPropertyErrorDbModel':
        return InputPropertyErrorDbModel(
            loc=loc,
            msg=msg
        )


class WorkflowState(Document):
    id: uuid.UUID = UUIDField(primary_key=True)
    experiment: Experiment = ReferenceField(Experiment, required=True, reverse_delete_rule=CASCADE)
    schema: Dict[str, Any] = DictField()

    meta = {'collection': 'workflows'}

    @staticmethod
    def create(id: uuid.UUID,
               experiment: Experiment,
               schema: WorkflowSchema) -> 'WorkflowState':
        return WorkflowState(
            id=id,
            experiment=experiment,
            schema=schema.dict()
        )

    def set_schema(self, schema: WorkflowSchema):
        self.schema = schema.dict()

    def get_schema(self) -> WorkflowSchema:
        return WorkflowSchema(**self.schema)


class ComponentState(Document):
    id: uuid.UUID = UUIDField(primary_key=True)
    experiment_id: uuid.UUID = UUIDField(required=True)
    workflow: WorkflowState = ReferenceField(WorkflowState, reverse_delete_rule=CASCADE)

    input_property_errors: List[InputPropertyErrorDbModel] = EmbeddedDocumentListField(InputPropertyErrorDbModel)

    job_ids: List[uuid.UUID] = ListField(UUIDField())
    last_jobs_count: int = IntField()

    last_executed_at: datetime = DateTimeField()

    name: str = StringField()

    # region component fields

    input_schema: Dict[str, Any] = DictField()
    output_schema: Dict[str, Any] = DictField()
    input_value_dict: Dict[str, Any] = DictField()
    output_value_dict: Dict[str, Any] = DictField()
    previous_component_ids: List[uuid.UUID] = ListField(UUIDField())

    # endregion

    meta = {'collection': 'components'}

    @classmethod
    def create(cls,
               id: uuid.UUID,
               workflow: WorkflowState,
               component: 'Component'):
        return ComponentState(
            id=id,
            experiment_id=workflow.experiment.id,
            workflow=workflow,
            input_schema=component.input_schema.dict(),
            output_schema=component.output_schema.dict(),
            input_value_dict=component.input_value_dict,
            output_value_dict=component.output_value_dict,
            previous_component_ids=component.previous_component_ids,
            name=component.name,
            job_ids=component.job_ids
        )

    def set_component(self, component: 'Component'):
        self.input_schema = component.input_schema.dict()
        self.output_schema = component.output_schema.dict()
        self.input_value_dict = component.input_value_dict
        self.output_value_dict = component.output_value_dict
        self.previous_component_ids = component.previous_component_ids
