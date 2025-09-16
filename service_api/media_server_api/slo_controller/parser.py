from abc import ABC, abstractmethod
from datetime import datetime, date
from media_server_api.models.slo import SLO
from media_server_api.models.slo_type import SLOType
from media_server_api.models.range_slo import RangeSLO
from media_server_api.models.integer_range_slo import IntegerRangeSLO
from media_server_api.models.date_range_slo import DateRangeSLO
from media_server_api.models.date_time_range_slo import DateTimeRangeSLO
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

    @staticmethod
    def _build_description(slo_type: SLOType, description) -> bool|RangeSLO|IntegerRangeSLO|DateRangeSLO|DateTimeRangeSLO|float|int|str|date|datetime:
        if slo_type == SLOType.BOOLEAN:
            return True
        elif slo_type in [SLOType.TARGET_VALUE, SLOType.INTEGER_TARGET_VALUE, SLOType.STRING_TARGET_VALUE, SLOType.DATE_TARGET_VALUE, SLOType.DATETIME_TARGET_VALUE]:
            return description
        elif slo_type == SLOType.RANGE:
            return RangeSLO(min_value=description.get("min_value"), max_value=description.get("max_value"), min_range=description["min_range"], max_range=description["max_range"])
        elif slo_type == SLOType.INTEGER_RANGE:
            return IntegerRangeSLO(min_value=description.get("min_value"), max_value=description.get("max_value"), min_range=description["min_range"], max_range=description["max_range"])
        elif slo_type == SLOType.DATE_RANGE:
            return DateRangeSLO(min_value=description.get("min_value"), max_value=description.get("max_value"), min_range=description["min_range"], max_range=description["max_range"])
        elif slo_type == SLOType.DATETIME_RANGE:
            return DateTimeRangeSLO(min_value=description.get("min_value"), max_value=description.get("max_value"), min_range=description["min_range"], max_range=description["max_range"])

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
            slo = SLO(id=unparsed_slo["id"], name=unparsed_slo["name"], type=slo_type, description=cls._build_description(slo_type, unparsed_slo["description"]))
            slos[unparsed_slo[cls._ID_KEY]] = slo
            queries[unparsed_slo[cls._ID_KEY]] = query
            cls._LOGGER.debug("SLO parsed successfully")
        cls._LOGGER.info(f"SLO configuration parsed successfully. {len(slos)} SLOs parsed")
        return slos, queries