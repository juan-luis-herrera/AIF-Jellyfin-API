import unittest

from flask import json

from media_server_api.models.conf_param import ConfParam  # noqa: E501
from media_server_api.models.conf_param_value import ConfParamValue  # noqa: E501
from media_server_api.test import BaseTestCase


class TestConfigController(BaseTestCase):
    """ConfigController integration test stubs"""

    def test_config_change(self):
        """Test case for config_change

        Change parameter.
        """
        conf_param_value = {"value":True}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/v0/config/{conf_param}'.format(conf_param='nextBackup'),
            method='PUT',
            headers=headers,
            data=json.dumps(conf_param_value),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_config_discover(self):
        """Test case for config_discover

        Discover, describe, and gather configuration.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v0/config',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_config_value(self):
        """Test case for config_value

        Parameter value.
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v0/config/{conf_param}'.format(conf_param='nextBackup'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
