import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from media_server_api.models.conf_param import ConfParam  # noqa: E501
from media_server_api.models.conf_param_value import ConfParamValue  # noqa: E501
from media_server_api import util


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
    return 'do some magic!'


def config_describe(conf_param):  # noqa: E501
    """Describe configurable parameter.

    Returns the description of the requested parameter. # noqa: E501

    :param conf_param: Name of the parameter to describe
    :type conf_param: str

    :rtype: Union[ConfParam, Tuple[ConfParam, int], Tuple[ConfParam, int, Dict[str, str]]
    """
    return 'do some magic!'


def config_discover():  # noqa: E501
    """Discover configuration.

    Returns the list of configurable service parameters. # noqa: E501


    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return 'do some magic!'


def config_value(conf_param):  # noqa: E501
    """Parameter value.

    Returns the current value of the requested parameter. # noqa: E501

    :param conf_param: Name of the parameter to describe
    :type conf_param: str

    :rtype: Union[ConfParamValue, Tuple[ConfParamValue, int], Tuple[ConfParamValue, int, Dict[str, str]]
    """
    return 'do some magic!'
