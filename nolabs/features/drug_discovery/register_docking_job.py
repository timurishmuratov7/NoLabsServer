from nolabs.api_models.drug_discovery import RegisterDockingJobRequest, RegisterDockingJobResponse
from nolabs.domain.experiment import ExperimentId
from nolabs.features.drug_discovery.data_models.ligand import LigandId
from nolabs.features.drug_discovery.data_models.result import JobId
from nolabs.features.drug_discovery.data_models.target import TargetId
from nolabs.features.drug_discovery.services.result_file_management import ResultsFileManagement
from nolabs.utils import generate_uuid


class RegisterDockingJobFeature:
    # TODO: check for a job with absolutely similar inputs to remove unnecessary computations
    def __init__(self, file_management: ResultsFileManagement):
        self._file_management = file_management

    def handle(self, request: RegisterDockingJobRequest) -> RegisterDockingJobResponse:

        experiment_id = ExperimentId(request.experiment_id)
        target_id = TargetId(request.target_id)
        ligand_id = LigandId(request.ligand_id)

        job_id = JobId(generate_uuid())

        self._file_management.create_result_folder(experiment_id, target_id, ligand_id, job_id)

        return RegisterDockingJobResponse(job_id=job_id.value)