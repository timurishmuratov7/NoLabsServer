# coding: utf-8

"""
    NoLabs

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel
from nolabs_microservice.models.integrators_request import IntegratorsRequest
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class NolabsApiModelsConformationsExperimentPropertiesResponse(BaseModel):
    """
    NolabsApiModelsConformationsExperimentPropertiesResponse
    """ # noqa: E501
    pdb_file: Optional[Any]
    pdb_file_name: Optional[Any]
    total_frames: Optional[Any]
    temperature_k: Optional[Any]
    take_frame_every: Optional[Any]
    step_size: Optional[Any]
    replace_non_standard_residues: Optional[Any]
    add_missing_atoms: Optional[Any]
    add_missing_hydrogens: Optional[Any]
    friction_coeff: Optional[Any]
    ignore_missing_atoms: Optional[Any]
    integrator: Optional[IntegratorsRequest] = None
    __properties: ClassVar[List[str]] = ["pdb_file", "pdb_file_name", "total_frames", "temperature_k", "take_frame_every", "step_size", "replace_non_standard_residues", "add_missing_atoms", "add_missing_hydrogens", "friction_coeff", "ignore_missing_atoms", "integrator"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of NolabsApiModelsConformationsExperimentPropertiesResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # set to None if pdb_file (nullable) is None
        # and model_fields_set contains the field
        if self.pdb_file is None and "pdb_file" in self.model_fields_set:
            _dict['pdb_file'] = None

        # set to None if pdb_file_name (nullable) is None
        # and model_fields_set contains the field
        if self.pdb_file_name is None and "pdb_file_name" in self.model_fields_set:
            _dict['pdb_file_name'] = None

        # set to None if total_frames (nullable) is None
        # and model_fields_set contains the field
        if self.total_frames is None and "total_frames" in self.model_fields_set:
            _dict['total_frames'] = None

        # set to None if temperature_k (nullable) is None
        # and model_fields_set contains the field
        if self.temperature_k is None and "temperature_k" in self.model_fields_set:
            _dict['temperature_k'] = None

        # set to None if take_frame_every (nullable) is None
        # and model_fields_set contains the field
        if self.take_frame_every is None and "take_frame_every" in self.model_fields_set:
            _dict['take_frame_every'] = None

        # set to None if step_size (nullable) is None
        # and model_fields_set contains the field
        if self.step_size is None and "step_size" in self.model_fields_set:
            _dict['step_size'] = None

        # set to None if replace_non_standard_residues (nullable) is None
        # and model_fields_set contains the field
        if self.replace_non_standard_residues is None and "replace_non_standard_residues" in self.model_fields_set:
            _dict['replace_non_standard_residues'] = None

        # set to None if add_missing_atoms (nullable) is None
        # and model_fields_set contains the field
        if self.add_missing_atoms is None and "add_missing_atoms" in self.model_fields_set:
            _dict['add_missing_atoms'] = None

        # set to None if add_missing_hydrogens (nullable) is None
        # and model_fields_set contains the field
        if self.add_missing_hydrogens is None and "add_missing_hydrogens" in self.model_fields_set:
            _dict['add_missing_hydrogens'] = None

        # set to None if friction_coeff (nullable) is None
        # and model_fields_set contains the field
        if self.friction_coeff is None and "friction_coeff" in self.model_fields_set:
            _dict['friction_coeff'] = None

        # set to None if ignore_missing_atoms (nullable) is None
        # and model_fields_set contains the field
        if self.ignore_missing_atoms is None and "ignore_missing_atoms" in self.model_fields_set:
            _dict['ignore_missing_atoms'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of NolabsApiModelsConformationsExperimentPropertiesResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pdb_file": obj.get("pdb_file"),
            "pdb_file_name": obj.get("pdb_file_name"),
            "total_frames": obj.get("total_frames"),
            "temperature_k": obj.get("temperature_k"),
            "take_frame_every": obj.get("take_frame_every"),
            "step_size": obj.get("step_size"),
            "replace_non_standard_residues": obj.get("replace_non_standard_residues"),
            "add_missing_atoms": obj.get("add_missing_atoms"),
            "add_missing_hydrogens": obj.get("add_missing_hydrogens"),
            "friction_coeff": obj.get("friction_coeff"),
            "ignore_missing_atoms": obj.get("ignore_missing_atoms"),
            "integrator": obj.get("integrator")
        })
        return _obj


