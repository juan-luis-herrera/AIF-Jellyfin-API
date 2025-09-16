from media_server_api.slo_controller import config
from media_server_api.slo_controller.parser import SLOParser
from media_server_api.models.slo import SLO
from abc import ABC, abstractmethod


class SLOController(ABC):

    @abstractmethod
    def __init__(self, parser: type[SLOParser]):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, *exc):
        pass

    @abstractmethod
    def discover_slos(self) -> list[str]:
        pass
    
    @abstractmethod
    def describe_slo(self, slo_id: str) -> SLO|None:
        pass
    
    @abstractmethod
    def get_value_slo(self, slo_id: str):
        pass 

from influxdb_client import InfluxDBClient

class InfluxDBSLOController(SLOController):

    def __init__(self, parser: type[SLOParser]):
        self._slos, initial_queries = parser.parse_slo_file(config.SLO_FILE)
        self._queries = {k: f'from(bucket: "{config.INFLUX_BUCKET}")  ' +  initial_queries[k] for k in initial_queries}

    def __enter__(self):
        self._influx_client = InfluxDBClient(url=config.INFLUX_URL, token=config.INFLUX_TOKEN, org=config.INFLUX_ORG)
        return self

    def __exit__(self, *exc):
        self._influx_client.close()

    def discover_slos(self) -> list[str]:
        return list(self._slos.keys())
    
    def describe_slo(self, slo_id: str) -> SLO|None:
        return self._slos.get(slo_id)
    
    def get_value_slo(self, slo_id: str):
        query_api = self._influx_client.query_api()
        result = query_api.query(self._queries[slo_id])
        if len(result) > 0 and len(result[0].records) > 0:
            return result[0].records[0].get_value()
        else:
            return None 