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

from nolabs_microservice.models.send_message_response import SendMessageResponse

class TestSendMessageResponse(unittest.TestCase):
    """SendMessageResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SendMessageResponse:
        """Test SendMessageResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SendMessageResponse`
        """
        model = SendMessageResponse()
        if include_optional:
            return SendMessageResponse(
                biobuddy_response = nolabs_microservice.models.message.Message(
                    role = null, 
                    message = null, 
                    type = null, )
            )
        else:
            return SendMessageResponse(
                biobuddy_response = nolabs_microservice.models.message.Message(
                    role = null, 
                    message = null, 
                    type = null, ),
        )
        """

    def testSendMessageResponse(self):
        """Test SendMessageResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
