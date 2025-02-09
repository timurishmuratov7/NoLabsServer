__all__ = [
    "FoldingBackendEnum",
    "JobResult",
    "JobResponse",
    "RunJobRequest",
    "GetJobStatusResponse",
]


from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic.dataclasses import dataclass


class FoldingBackendEnum(str, Enum):
    rosettafold = "rosettafold"
    esmfold = "esmfold"
    esmfold_light = "esmfold_light"


@dataclass
class JobResult:
    protein_id: UUID
    pdb: str


@dataclass
class JobResponse:
    job_id: UUID
    job_name: str
    backend: FoldingBackendEnum
    protein_id: UUID
    result: JobResult
    experiment_id: UUID


@dataclass
class SetupJobRequest:
    experiment_id: UUID
    backend: Optional[FoldingBackendEnum]
    protein_id: UUID
    job_id: Optional[UUID] = None
    job_name: Optional[str] = None


@dataclass
class RunJobRequest:
    job_id: UUID


@dataclass
class GetJobStatusResponse:
    running: bool
    result_valid: bool
