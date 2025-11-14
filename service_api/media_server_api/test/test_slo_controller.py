import unittest

from flask import json

from media_server_api.models.slo import SLO  # noqa: E501
from media_server_api.test import BaseTestCase


class TestSloController(BaseTestCase):
    """SloController integration test stubs"""

    def test_slo_discover(self):
        """Test case for slo_discover

        Discover, describe, and gather values of SLOs.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v0/slos',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_slo_value(self):
        """Test case for slo_value

        Describe and gather value of an SLO.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v0/slos/{slo_id}'.format(slo_id='rps'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
