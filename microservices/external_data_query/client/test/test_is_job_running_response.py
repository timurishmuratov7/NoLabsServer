# coding: utf-8

"""
    RCSB PDB Query API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from external_data_query_microservice.models.is_job_running_response import (
    IsJobRunningResponse,
)


class TestIsJobRunningResponse(unittest.TestCase):
    """IsJobRunningResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> IsJobRunningResponse:
        """Test IsJobRunningResponse
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `IsJobRunningResponse`
        """
        model = IsJobRunningResponse()
        if include_optional:
            return IsJobRunningResponse(
                is_running = True
            )
        else:
            return IsJobRunningResponse(
                is_running = True,
        )
        """

    def testIsJobRunningResponse(self):
        """Test IsJobRunningResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
