import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from media_server_api.models.slo import SLO  # noqa: E501
from media_server_api.models.slo_value import SLOValue  # noqa: E501
from media_server_api import util, api_bridge


def slo_describe(slo_id):  # noqa: E501
    """Describe SLO.

    Returns the description of the requested SLO. # noqa: E501

    :param slo_id: ID of SLO to describe
    :type slo_id: str

    :rtype: Union[SLO, Tuple[SLO, int], Tuple[SLO, int, Dict[str, str]]
    """
    slo = api_bridge.SLO_CONTROLLER.describe_slo(slo_id)
    if slo is not None:
        return slo, 200
    else:
        return "The requested SLO does not exist", 404


def slo_discover():  # noqa: E501
    """Discover SLOs.

    Returns the list of declared SLOs of the service. # noqa: E501


    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return api_bridge.SLO_CONTROLLER.discover_slos()


def slo_value(slo_id):  # noqa: E501
    """SLO value.

    Returns the current value of the requested SLO. # noqa: E501

    :param slo_id: ID of SLO to describe
    :type slo_id: str

    :rtype: Union[SLOValue, Tuple[SLOValue, int], Tuple[SLOValue, int, Dict[str, str]]
    """
    value = api_bridge.SLO_CONTROLLER.get_value_slo(slo_id)
    if value is not None:
        return value, 200
    else:
        return "The requested SLO does not exist", 404
