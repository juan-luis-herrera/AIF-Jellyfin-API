import json
from datetime import datetime
from zoneinfo import ZoneInfo
import config
from paho.mqtt import client as mqtt_client
from database import DatabaseConnector

import logging

LOG_FORMAT = "[%(levelname)s] [%(name)s] [%(asctime)s] - %(message)s"

class MQTTError(RuntimeError):
    pass


class MQTTHook:

    def __init__(self, db_connectors = list[DatabaseConnector]):
        self._mqtt_broker = config.MQTT_BROKER
        self._mqtt_port = config.MQTT_PORT
        self._client_id = config.MQTT_CLIENT_ID
        self._mqtt_client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, self._client_id)
        self._mqtt_client.on_connect = self._connect_handling
        self._mqtt_client.on_message = self._message_handling
        self._database_connectors = db_connectors
        self.LOGGER = logging.getLogger(__name__)
        self.LOGGER.debug("MQTT hook created")

    def _connect_handling(self, client, userdata, flags, rc, properties):
        if rc != 0:
            raise MQTTError(f"Error on MQTT connection, code {rc}")
        else:
            client.subscribe(config.MQTT_TOPIC)
            self.LOGGER.info("MQTT connection and subscription successful")
    
    def _message_handling(self, client, userdata, message):
        try:
            self.LOGGER.debug(f"Got message - Payload size {len(message.payload)}")
            res = True
            for conn in self._database_connectors:
                res = res and conn.store(message)
            if res:
                self.LOGGER.debug("Successfully stored in all connectors")
            else:
                self.LOGGER.warn("Some connector failed to store - Check logs")
        except Exception as err:
            self.LOGGER.error(f"Error in message handling: {str(err)}")
    
    def hook(self) -> None:
        self.LOGGER.info("Starting execution loop")
        self._mqtt_client.loop_forever()

    def __enter__(self):
        try:
            for idx, conn in enumerate(self._database_connectors):
                res = conn.start()
                if res:
                    self.LOGGER.info(f"Successfully started database connector {idx+1}")
                else:
                    self._database_connectors.remove(conn)
                    self.LOGGER.warn(f"Connector {str(res)} failed - removed from list")
            self.LOGGER.info("Connecting to MQTT...")
            self._mqtt_client.connect(self._mqtt_broker, self._mqtt_port)
        except ConnectionRefusedError:
            self.LOGGER.error("Error during MQTT connection: refused")
        except MQTTError as err:
            self.LOGGER.error(f"Error during MQTT connection: {str(err)}")
        return self

    def __exit__(self, *exc):
        self.LOGGER.debug("Stopping hook...")
        for conn in self._database_connectors:
            conn.stop()
        self._mqtt_client.loop_stop()
        self.LOGGER.info("MQTT hook stopped")

if __name__ == '__main__':
    from database import InfluxDBConnector
    from interpret import MessageInterpreterJSONInflux
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    connectors = [
        InfluxDBConnector(MessageInterpreterJSONInflux(config.CONFIG_FILE))
    ]
    with MQTTHook(connectors) as hook:
        hook.hook()