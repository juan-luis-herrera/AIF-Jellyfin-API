import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from media_server_api.models.conf_param import ConfParam  # noqa: E501
from media_server_api.models.conf_param_value import ConfParamValue  # noqa: E501
from media_server_api import util, api_bridge

def config_change(conf_param, body=None):  # noqa: E501
    """Change parameter.

    Changes the value of the requested parameter. # noqa: E501

    :param conf_param: Name of the parameter to describe
    :type conf_param: str
    :param conf_param_value: 
    :type conf_param_value: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    conf_param_value = body
    if conf_param in api_bridge.CONTROLLER.discover_configuration():
        if api_bridge.CONTROLLER.set_param_value(conf_param, conf_param_value):
            return "", 200
        else:
            return "Invalid value for the parameter", 400
    else:
        return "The requested parameter does not exist", 404


def config_describe(conf_param):  # noqa: E501
    """Describe configurable parameter.

    Returns the description of the requested parameter. # noqa: E501

    :param conf_param: Name of the parameter to describe
    :type conf_param: str

    :rtype: Union[ConfParam, Tuple[ConfParam, int], Tuple[ConfParam, int, Dict[str, str]]
    """
    description = api_bridge.CONTROLLER.describe_param(conf_param)
    if description is not None:
        return description, 200
    else:
        return "The requested parameter does not exist", 404


def config_discover():  # noqa: E501
    """Discover configuration.

    Returns the list of configurable service parameters. # noqa: E501


    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return api_bridge.CONTROLLER.discover_configuration(), 200


def config_value(conf_param):  # noqa: E501
    """Parameter value.

    Returns the current value of the requested parameter. # noqa: E501

    :param conf_param: Name of the parameter to describe
    :type conf_param: str

    :rtype: Union[ConfParamValue, Tuple[ConfParamValue, int], Tuple[ConfParamValue, int, Dict[str, str]]
    """
    value = api_bridge.CONTROLLER.get_param_value(conf_param)
    if value is not None:
        return value, 200
    else:
        return "The requested parameter does not exist", 404
