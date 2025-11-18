import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from media_server_api.models.slo import SLO  # noqa: E501
from media_server_api import util, api_bridge


def slo_discover():  # noqa: E501
    """Discover, describe, and gather values of SLOs.

    Returns the list of declared SLOs of the service with their definitions and current values # noqa: E501


    :rtype: Union[List[SLO], Tuple[List[SLO], int], Tuple[List[SLO], int, Dict[str, str]]
    """
    return api_bridge.SLO_CONTROLLER.discover_slos(), 200


def slo_get(slo_id):  # noqa: E501
    """Describe and gather value of an SLO.

    Returns the description and current value of the requested SLO. # noqa: E501

    :param slo_id: ID of SLO to describe
    :type slo_id: str

    :rtype: Union[SLO, Tuple[SLO, int], Tuple[SLO, int, Dict[str, str]]
    """
    slo = api_bridge.SLO_CONTROLLER.get_slo(slo_id)
    if slo is not None:
        return slo, 200
    else:
        return "The requested SLO does not exist", 404
