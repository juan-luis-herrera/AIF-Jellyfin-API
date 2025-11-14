from abc import ABC, abstractmethod
from datetime import datetime, date
from media_server_api.models.slo import SLO
from media_server_api.models.slo_type import SLOType
import logging


class SLOParser(ABC):

    @classmethod
    @abstractmethod
    def parse_slo_file(cls, slo_file: str) -> tuple[dict[str, SLO], dict[str, str]]:
        pass

import json
class JSONSLOParser(SLOParser):
    _QUERY_KEY = "query"
    _ID_KEY = "id"
    _TYPE_PARSING = {
        "boolean": SLOType.BOOLEAN,
        "range": SLOType.RANGE,
        "integer_range": SLOType.INTEGER_RANGE,
        "date_range": SLOType.DATE_RANGE,
        "datetime_range": SLOType.DATETIME_RANGE,
        "target_value": SLOType.TARGET_VALUE,
        "integer_target_value": SLOType.INTEGER_TARGET_VALUE,
        "string_target_value": SLOType.STRING_TARGET_VALUE,
        "date_target_value": SLOType.DATE_TARGET_VALUE,
        "datetime_target_value": SLOType.DATETIME_TARGET_VALUE
    }
    _LOGGER = logging.getLogger("gunicorn.error")

    @classmethod
    def parse_slo_file(cls, slo_file: str) -> dict[str, (SLO, str)]:
        cls._LOGGER.debug("Parsing SLO configuration")
        with open(slo_file, 'r') as in_json:
            slo_list = json.load(in_json)
        slos = {}
        queries = {}
        for unparsed_slo in slo_list:
            cls._LOGGER.debug(f"Parsing SLO {unparsed_slo["id"]}")
            query = unparsed_slo.pop(cls._QUERY_KEY)
            slo_type = cls._TYPE_PARSING[unparsed_slo["type"]]
            slo = SLO(id=unparsed_slo["id"], name=unparsed_slo["name"], type=slo_type, description=unparsed_slo["description"], value=None)
            slos[unparsed_slo[cls._ID_KEY]] = slo
            queries[unparsed_slo[cls._ID_KEY]] = query
            cls._LOGGER.debug("SLO parsed successfully")
        cls._LOGGER.info(f"SLO configuration parsed successfully. {len(slos)} SLOs parsed")
        return slos, queries