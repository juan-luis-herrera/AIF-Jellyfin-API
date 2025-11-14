import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from media_server_api.models.conf_param import ConfParam  # noqa: E501
from media_server_api.models.conf_param_value import ConfParamValue  # noqa: E501
from media_server_api import util
from media_server_api import api_bridge


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
    if connexion.request.is_json:
        conf_param_value = ConfParamValue.from_dict(connexion.request.get_json())  # noqa: E501
        code = api_bridge.SERVICE_CONTROLLER.set_param_value(conf_param, conf_param_value["value"])
        return {200: "", 404: "The requested parameter does not exist", 400: "Invalid value for the parameter"}[code], code
    return "Invalid value for the parameter", 400


def config_discover():  # noqa: E501
    """Discover, describe, and gather configuration.

    Returns the list of configurable service parameters with their definitions and current values. # noqa: E501


    :rtype: Union[List[ConfParam], Tuple[List[ConfParam], int], Tuple[List[ConfParam], int, Dict[str, str]]
    """
    return api_bridge.SERVICE_CONTROLLER.discover_configuration(), 200


def config_value(conf_param):  # noqa: E501
    """Parameter value.

    Returns the description and current value of the requested parameter. # noqa: E501

    :param conf_param: Name of the parameter to describe
    :type conf_param: str

    :rtype: Union[ConfParam, Tuple[ConfParam, int], Tuple[ConfParam, int, Dict[str, str]]
    """
    value = api_bridge.SERVICE_CONTROLLER.get_param(conf_param)
    if value is not None:
        return value, 200
    else:
        return "The requested parameter does not exist", 404
