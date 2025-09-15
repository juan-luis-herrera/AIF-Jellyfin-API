import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from media_server_api.models.slo import SLO  # noqa: E501
from media_server_api.models.slo_value import SLOValue  # noqa: E501
from media_server_api import util


def slo_describe(slo_id):  # noqa: E501
    """Describe SLO.

    Returns the description of the requested SLO. # noqa: E501

    :param slo_id: ID of SLO to describe
    :type slo_id: str

    :rtype: Union[SLO, Tuple[SLO, int], Tuple[SLO, int, Dict[str, str]]
    """
    return 'do some magic!'


def slo_discover():  # noqa: E501
    """Discover SLOs.

    Returns the list of declared SLOs of the service. # noqa: E501


    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return 'do some magic!'


def slo_value(slo_id):  # noqa: E501
    """SLO value.

    Returns the current value of the requested SLO. # noqa: E501

    :param slo_id: ID of SLO to describe
    :type slo_id: str

    :rtype: Union[SLOValue, Tuple[SLOValue, int], Tuple[SLOValue, int, Dict[str, str]]
    """
    return 'do some magic!'
