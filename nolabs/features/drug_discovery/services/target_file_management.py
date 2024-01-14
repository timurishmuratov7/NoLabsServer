import json
import os.path
import shutil
import numpy as np
from typing import List

from nolabs.domain.experiment import ExperimentId
from nolabs.infrastructure.settings import Settings

from nolabs.utils.fasta import FastaReader, FastaWriter
from nolabs.utils.pdb import PDBReader, PDBWriter
from nolabs.utils.uuid_utils import generate_uuid
from nolabs.features.drug_discovery.data_models.target import TargetId, TargetMetaData
from fastapi import UploadFile


class TargetsFileManagement:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.fasta_reader = FastaReader()
        self.fasta_writer = FastaWriter()
        self.pdb_reader = PDBReader()
        self.pdb_writer = PDBWriter()

    def ensure_targets_folder_exists(self, experiment_id: ExperimentId):
        if not os.path.isdir(self.targets_folder(experiment_id)):
            os.mkdir(self.targets_folder(experiment_id))

    def ensure_target_folder_exists(self, experiment_id: ExperimentId, target_id: TargetId):
        target_folder = self.target_folder(experiment_id, target_id)
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

    def targets_folder(self, experiment_id: ExperimentId) -> str:
        return os.path.join(self._settings.drug_discovery_experiments_folder, experiment_id.value, 'targets')

    def target_folder(self, experiment_id: ExperimentId, target_id: TargetId) -> str:
        return os.path.join(self.targets_folder(experiment_id), target_id.value)

    def create_target_folder(self, experiment_id: ExperimentId, target_id: TargetId):
        self.ensure_targets_folder_exists(experiment_id)
        targets_dir = self.targets_folder(experiment_id)
        os.mkdir(os.path.join(targets_dir, target_id.value))

    def store_target(self, experiment_id: ExperimentId, fasta_file: UploadFile) -> List[TargetMetaData]:
        self.ensure_targets_folder_exists(experiment_id)

        original_filename = fasta_file.filename
        contents = fasta_file.file.read().decode('utf-8')
        ids2sequences = self.fasta_reader.get_ids2seqs(fasta_contents=contents)

        result_list = []

        for amino_acid in ids2sequences:
            target_name, sequence = amino_acid.name, amino_acid.sequence
            target_id = TargetId(generate_uuid())
            self.ensure_target_folder_exists(experiment_id, target_id)
            target_folder = self.target_folder(experiment_id, target_id)

            self.fasta_writer.write_single_fasta(target_name, sequence,
                                                 os.path.join(target_folder, target_name + ".fasta"))

            self.update_target_metadata(experiment_id, target_id, "id", target_id.value)
            self.update_target_metadata(experiment_id, target_id, "name", target_name)
            self.update_target_metadata(experiment_id, target_id, "original_filename", original_filename)

            result_list.append(TargetMetaData(target_id=target_id.value,
                                              target_name=target_name))

        return result_list

    def delete_target(self, experiment_id: ExperimentId, target_id: TargetId):
        self.ensure_targets_folder_exists(experiment_id)
        self.ensure_target_folder_exists(experiment_id, target_id)
        target_folder = self.target_folder(experiment_id, target_id)
        shutil.rmtree(target_folder)

        return target_id

    def update_target_metadata(self, experiment_id: ExperimentId, target_id: TargetId, key: str, value: str):
        metadata_file = os.path.join(self.target_folder(experiment_id, target_id),
                                     self._settings.drug_discovery_target_metadata_file_name)
        if os.path.exists(metadata_file):
            metadata = json.load(open(metadata_file))
            metadata[key] = value
            json.dump(metadata, open(metadata_file, 'w'))
        else:
            metadata = {key: value}
            json.dump(metadata, open(metadata_file, 'w'))

    def get_target_metadata(self, experiment_id: ExperimentId, target_id: TargetId) -> TargetMetaData:
        metadata_file = os.path.join(self.target_folder(experiment_id, target_id),
                                     self._settings.drug_discovery_target_metadata_file_name)
        metadata = json.load(open(metadata_file))
        target_metadata = TargetMetaData(target_id=metadata["id"], target_name=metadata["name"])
        return target_metadata

    def get_targets_list(self, experiment_id: ExperimentId) -> List[TargetMetaData]:
        targets_folder = self.targets_folder(experiment_id)
        result_list = []
        for t_id in os.listdir(targets_folder):
            if os.path.isdir(os.path.join(targets_folder, t_id)):
                target_id = TargetId(t_id)
                target_metadata = self.get_target_metadata(experiment_id, target_id)
                result_list.append(target_metadata)

        return result_list

    def get_target_data(self, experiment_id: ExperimentId, target_id: TargetId) -> tuple[str, str, str | None]:
        target_folder = self.target_folder(experiment_id, target_id)
        target_metadata = self.get_target_metadata(experiment_id, target_id)
        target_name = target_metadata.target_name

        ids2sequences = self.fasta_reader.get_ids2seqs_from_path(os.path.join(target_folder, target_name + ".fasta"))
        sequence = [amino_acid.sequence for amino_acid in ids2sequences if amino_acid.name == target_name][0]
        pdb_content = self.get_pdb_contents(experiment_id, target_id)

        return target_name, sequence, pdb_content

    def get_pdb_contents(self, experiment_id: ExperimentId, target_id: TargetId) -> str | None:
        target_folder = self.target_folder(experiment_id, target_id)
        target_metadata = self.get_target_metadata(experiment_id, target_id)
        target_name = target_metadata.target_name
        if os.path.exists(os.path.join(target_folder, target_name + ".pdb")):
            return self.pdb_reader.read_pdb(os.path.join(target_folder, target_name + ".pdb"))

        return None

    def store_pdb_contents(self, experiment_id: ExperimentId, target_id: TargetId, pdb_content: str) -> None:
        target_folder = self.target_folder(experiment_id, target_id)
        target_metadata = self.get_target_metadata(experiment_id, target_id)
        target_name = target_metadata.target_name
        self.pdb_writer.write_pdb(os.path.join(target_folder, target_name + ".pdb"), pdb_content)

    def get_fasta_contents(self, experiment_id: ExperimentId, target_id: TargetId) -> str | None:
        target_folder = self.target_folder(experiment_id, target_id)
        target_metadata = self.get_target_metadata(experiment_id, target_id)
        target_name = target_metadata.target_name
        if os.path.exists(os.path.join(target_folder, target_name + ".fasta")):
            return self.fasta_reader.get_contents_from_path(os.path.join(target_folder, target_name + ".fasta"))

        return None

    def get_binding_pocket(self, experiment_id: ExperimentId, target_id: TargetId) -> List[int] | None:
        target_folder = self.target_folder(experiment_id, target_id)
        pocket_file = os.path.join(target_folder, self._settings.drug_discovery_pocket_directory_name,
                                   self._settings.drug_discovery_pocket_file_name)
        if os.path.exists(pocket_file):
            pocket_arr = np.load(file=pocket_file)
            return pocket_arr.tolist()

        return None

    def store_binding_pocket(self, experiment_id: ExperimentId, target_id: TargetId, pocket_ids: List[int]):
        target_folder = self.target_folder(experiment_id, target_id)
        pocket_file = os.path.join(target_folder, self._settings.drug_discovery_pocket_directory_name,
                                   self._settings.drug_discovery_pocket_file_name)
        if os.path.exists(pocket_file):
            pocket_arr = np.asarray(pocket_ids)
            np.save(pocket_file, pocket_arr)
        else:
            pocket_dir = os.path.join(target_folder, self._settings.drug_discovery_pocket_directory_name)
            if not os.path.exists(pocket_dir):
                os.mkdir(pocket_dir)
            pocket_arr = np.asarray(pocket_ids)
            np.save(pocket_file, pocket_arr)

    def get_msa_api_url(self) -> str:
        return self._settings.drug_discovery_msa_url

    def get_msa(self, experiment_id: ExperimentId, target_id: TargetId) -> str | None:
        target_folder = self.target_folder(experiment_id, target_id)
        msa_file_path = os.path.join(target_folder, self._settings.drug_discovery_pocket_directory_name,
                                     self._settings.drug_discovery_msa_file_name)
        if os.path.exists(msa_file_path):
            with open(msa_file_path, "r") as f:
                msa_contents = f.read()
                return msa_contents

        return None

    def store_msa(self, experiment_id: ExperimentId, target_id: TargetId, msa_contents: str):
        target_folder = self.target_folder(experiment_id, target_id)
        msa_file_path = os.path.join(target_folder, self._settings.drug_discovery_pocket_directory_name,
                                     self._settings.drug_discovery_msa_file_name)
        if os.path.exists(msa_file_path):
            with open(msa_file_path, "w") as f:
                f.write(msa_contents)
