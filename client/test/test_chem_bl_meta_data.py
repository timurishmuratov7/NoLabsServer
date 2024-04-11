# coding: utf-8

"""
    NoLabs

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from nolabs_microservice.models.chem_bl_meta_data import ChemBLMetaData

class TestChemBLMetaData(unittest.TestCase):
    """ChemBLMetaData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ChemBLMetaData:
        """Test ChemBLMetaData
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ChemBLMetaData`
        """
        model = ChemBLMetaData()
        if include_optional:
            return ChemBLMetaData(
                chembl_id = None,
                link = None,
                pref_name = None
            )
        else:
            return ChemBLMetaData(
                chembl_id = None,
                link = None,
                pref_name = None,
        )
        """

    def testChemBLMetaData(self):
        """Test ChemBLMetaData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
