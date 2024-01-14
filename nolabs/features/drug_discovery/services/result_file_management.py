import json
import os.path
import shutil
from typing import List

import numpy as np

from nolabs.domain.experiment import ExperimentId
from nolabs.infrastructure.settings import Settings
from nolabs.utils.pdb import PDBWriter, PDBReader

from nolabs.utils.sdf import SDFReader, SDFWriter
from nolabs.utils.uuid_utils import generate_uuid
from nolabs.features.drug_discovery.data_models.target import TargetId
from nolabs.features.drug_discovery.data_models.ligand import LigandId
from nolabs.features.drug_discovery.data_models.result import ResultId, ResultMetaData, DockingResultData
from nolabs.features.drug_discovery.services.ligand_file_management import LigandsFileManagement


class ResultsFileManagement:
    def __init__(self, settings: Settings, ligand_file_management: LigandsFileManagement):
        self._settings = settings
        self.sdf_reader = SDFReader()
        self.sdf_writer = SDFWriter()
        self.pdb_writer = PDBWriter()
        self.pdb_reader = PDBReader()
        self._ligand_file_management = ligand_file_management

    def ensure_results_folder_exists(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId):
        if not os.path.isdir(self.results_folder(experiment_id, target_id, ligand_id)):
            os.mkdir(self.results_folder(experiment_id, target_id, ligand_id))

    def ensure_result_folder_exists(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                                    result_id: ResultId):
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, result_id)
        if not os.path.isdir(result_folder):
            os.mkdir(result_folder)

    def results_folder(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId) -> str:
        parent_ligand_folder = self._ligand_file_management.ligand_folder(experiment_id, target_id, ligand_id)
        return os.path.join(parent_ligand_folder, 'results')

    def result_folder(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                      result_id: ResultId) -> str:
        return os.path.join(self.results_folder(experiment_id, target_id, ligand_id), result_id.value)

    def create_result_folder(
            self, experiment_id: ExperimentId,
            target_id: TargetId,
            ligand_id: LigandId,
            result_id: ResultId
    ):
        self.ensure_results_folder_exists(experiment_id, target_id, ligand_id)
        results_dir = self.results_folder(experiment_id, target_id, ligand_id)
        os.mkdir(os.path.join(results_dir, result_id.value))
        self.update_result_metadata(experiment_id, target_id, ligand_id, result_id, "target_id", target_id.value)
        self.update_result_metadata(experiment_id, target_id, ligand_id, result_id, "ligand_id", ligand_id.value)
        self.update_result_metadata(experiment_id, target_id, ligand_id, result_id, "result_id", result_id.value
                                    )

    def store_result_data(self, experiment_id: ExperimentId,
                          target_id: TargetId,
                          ligand_id: LigandId,
                          result_data: DockingResultData) -> ResultMetaData:
        result_id = ResultId(generate_uuid())
        self.create_result_folder(experiment_id, target_id, ligand_id, result_id)
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, result_id)

        sdf_file_name = self._settings.drug_discovery_docking_result_sdf_file_name
        sdf_file_path = os.path.join(result_folder, sdf_file_name)
        sdf_contents = result_data.predicted_sdf
        self.sdf_writer.write_sdf(sdf_contents, sdf_file_path)

        pdb_file_name = self._settings.drug_discovery_docking_result_pdb_file_name
        pdb_file_path = os.path.join(result_folder, pdb_file_name)
        pdb_contents = result_data.predicted_pdb
        self.pdb_writer.write_pdb(pdb_contents, pdb_file_path)

        plddt_file_name = self._settings.drug_discovery_docking_result_plddt_file_name
        plddt_file_path = os.path.join(result_folder, plddt_file_name)
        plddt_list = result_data.plddt_array
        np.save(plddt_file_path, np.asarray(plddt_list))

        return ResultMetaData(result_id=result_id.value, target_id=target_id.value, ligand_id=ligand_id.value)

    def delete_result(self, experiment_id: ExperimentId,
                      target_id: TargetId,
                      ligand_id: LigandId,
                      result_id: ResultId) -> ResultId:
        self.results_folder(experiment_id, target_id, ligand_id)
        self.result_folder(experiment_id, target_id, ligand_id, result_id)
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, result_id)
        shutil.rmtree(result_folder)

        return result_id

    def update_result_metadata(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                               result_id: ResultId, key: str, value: str):
        metadata_file = os.path.join(self.result_folder(experiment_id, target_id, ligand_id, result_id),
                                     self._settings.drug_discovery_docking_result_metadata_filename_name)
        if os.path.exists(metadata_file):
            metadata = json.load(open(metadata_file))
            metadata[key] = value
            json.dump(metadata, open(metadata_file, 'w'))
        else:
            metadata = {key: value}
            json.dump(metadata, open(metadata_file, 'w'))

    def get_result_metadata(self, experiment_id: ExperimentId, target_id: TargetId, ligand_id: LigandId,
                            result_id: ResultId) -> ResultMetaData:
        metadata_file = os.path.join(self.result_folder(experiment_id, target_id, ligand_id, result_id),
                                     self._settings.drug_discovery_ligand_metadata_file_name)
        metadata = json.load(open(metadata_file))
        result_metadata = ResultMetaData(result_id=metadata["result_id"],
                                         target_id=metadata["target_id"],
                                         ligand_id=metadata["ligand_id"])
        return result_metadata

    def get_results_list(self, experiment_id: ExperimentId,
                         target_id: TargetId, ligand_id: LigandId) -> List[ResultMetaData]:
        results_folder = self.results_folder(experiment_id, target_id, ligand_id)
        result_list = []
        for t_id in os.listdir(results_folder):
            if os.path.isdir(os.path.join(results_folder, t_id)):
                result_id = ResultId(t_id)
                ligand_metadata = self.get_result_metadata(experiment_id, target_id, ligand_id, result_id)
                result_list.append(ligand_metadata)

        return result_list

    def get_docking_result_data(self,
                                experiment_id: ExperimentId,
                                target_id: TargetId, ligand_id: LigandId,
                                result_id: ResultId) -> DockingResultData:
        result_folder = self.result_folder(experiment_id, target_id, ligand_id, result_id)

        sdf_file_name = self._settings.drug_discovery_docking_result_sdf_file_name
        sdf_file_path = os.path.join(result_folder, sdf_file_name)
        sdf_contents = self.sdf_reader.read_sdf(sdf_file_path)

        pdb_file_name = self._settings.drug_discovery_docking_result_pdb_file_name
        pdb_file_path = os.path.join(result_folder, pdb_file_name)
        pdb_contents = self.pdb_reader.read_pdb(pdb_file_path)

        plddt_file_name = self._settings.drug_discovery_docking_result_plddt_file_name
        plddt_file_path = os.path.join(result_folder, plddt_file_name)
        plddt_list = np.load(plddt_file_path).tolist()

        return DockingResultData(predicted_pdb=pdb_contents, predicted_sdf=sdf_contents, plddt_array=plddt_list)

