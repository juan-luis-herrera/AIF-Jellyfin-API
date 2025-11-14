from media_server_api.slo_controller import config
from media_server_api.slo_controller.parser import SLOParser
from media_server_api.models.slo import SLO
from abc import ABC, abstractmethod
import logging


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
    def get_slo(self, slo_id: str) -> SLO|None:
        pass

from influxdb_client import InfluxDBClient

class InfluxDBSLOController(SLOController):

    def __init__(self, parser: type[SLOParser]):
        self._slos, initial_queries = parser.parse_slo_file(config.SLO_FILE)
        self._queries = {k: f'from(bucket: "{config.INFLUX_BUCKET}")  ' +  initial_queries[k] for k in initial_queries}
        self._logger = logging.getLogger("gunicorn.error")
        self._logger.debug("Created InfluxDB SLO controller")

    def __enter__(self):
        self._influx_client = InfluxDBClient(url=config.INFLUX_URL, token=config.INFLUX_TOKEN, org=config.INFLUX_ORG)
        self._logger.info("InfluxDB SLO controller successfully started")
        return self

    def __exit__(self, *exc):
        self._influx_client.close()
        self._logger.info("InfluxDB SLO controller stopped")

    def discover_slos(self) -> list[str]:
        self._logger.debug("SLO discovery called")
        for slo in self._slos:
            self._update_value(slo)
        return self._slos.copy()
    
    def get_slo(self, slo_id: str):
        self._logger.debug(f"SLO {slo_id} described")
        if slo_id not in self._slos:
            self._logger.warning(f"SLO {slo_id} does not exist")
        else:
            self._update_value(slo_id)
        return self._slos.get(slo_id)

    def _update_value(self, slo_id: str):
        if slo_id in self._slos:
            query_api = self._influx_client.query_api()
            result = query_api.query(self._queries[slo_id])
            self._logger.debug("Successfully queried InfluxDB")
            if len(result) > 0 and len(result[0].records) > 0:
                if len(result) > 1 or len(result[0].records) > 1:
                    self._logger.warning("Multiple tables or records returned. Only the first one will be returned.")
                value = result[0].records[0].get_value()
            else:
                self._logger.warning(f"No records found for SLO {slo_id}")
                value = None 
            self._slos[slo_id].value = value
        