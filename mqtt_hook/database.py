from abc import ABC, abstractmethod
from interpret import MessageInterpreter, MessageInterpreterInflux

from paho.mqtt.client import MQTTMessage

class DatabaseConnector(ABC):

    @abstractmethod
    def __init__(self, interpreter: MessageInterpreter):
        pass
    
    @abstractmethod
    def start(self) -> bool:
        pass

    @abstractmethod
    def stop (self) -> None:
        pass

    @abstractmethod
    def store(self, message: MQTTMessage) -> bool:
        pass

import config

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from zoneinfo import ZoneInfo

import logging

class InfluxDBConnector(DatabaseConnector):

    def __init__(self, interpreter: MessageInterpreterInflux):
        self._interpreter = interpreter
        self._token = config.INFLUX_TOKEN
        self._org = config.INFLUX_ORG
        self._url = config.INFLUX_URL
        self._bucket = config.INFLUX_BUCKET
        self._write_client = None
        self.LOGGER = logging.getLogger(__name__)
        self.LOGGER.debug("InfluxDB connector created")

    def start(self) -> bool:
        try:
            self._write_client = InfluxDBClient(url=self._url, token=self._token, org=self._org)
            self.LOGGER.info(f"Connected successfully to InfluxDB@{self._url}")
            return True
        except Exception as err:
            self.LOGGER.error(f"Error connecting to InfluxDB@{self._url}: {str(err)}")
            return False

    def stop(self) -> None:
        self._write_client.close()
        self.LOGGER.info("InfluxDB connection closed")

    def store(self, message: MQTTMessage) -> bool:
        try:
            with self._write_client.write_api(write_options=SYNCHRONOUS) as write_api:
                point = self._interpreter.interpret_message(message)
                write_api.write(bucket=self._bucket, org=self._org, record=point)
                self.LOGGER.debug("Successfully wrote point to InfluxDB")
                return True
            return False # In case an exception is raised during writing and the with block is exited before reaching the return statement
        except Exception as err:
            self.LOGGER.warn(f"Error writing point to InfluxDB: {str(err)}")
            return False