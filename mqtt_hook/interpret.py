import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from abc import ABC, abstractmethod

from paho.mqtt.client import MQTTMessage
from influxdb_client import Point

class MessageInterpreter(ABC):
    TOPIC_KEYWORD = "$TOPIC"
    MESSAGE_ID_KEYWORD = "$MID"
    MESSAGE_TIMESTAMP_KEYWORD ="$TS"
    KEYWORDS = [TOPIC_KEYWORD, MESSAGE_ID_KEYWORD, MESSAGE_TIMESTAMP_KEYWORD]

    @abstractmethod
    def __init__(self, config_file: str):
        pass

    @abstractmethod
    def interpret_message(self, msg: MQTTMessage):
        pass

    @classmethod
    def _process_keyword(cls, keyword: str, msg: MQTTMessage):
        if keyword == cls.TOPIC_KEYWORD:
            return msg.topic
        elif keyword == cls.MESSAGE_ID_KEYWORD:
            return msg.mid
        elif keyword == cls.MESSAGE_TIMESTAMP_KEYWORD:
            return msg.timestamp
        else:
            return None
        
class MessageInterpreterInflux(MessageInterpreter, ABC):

    @abstractmethod
    def interpret_message(self, msg: MQTTMessage) -> Point:
        pass

class MessageInterpreterJSONInflux(MessageInterpreterInflux):

    def __init__(self, config_file: str):
        with open(config_file, 'r') as in_json:
            self._config = json.load(in_json)
        self.LOGGER = logging.getLogger(__name__)
    
    def _process_key_value(self, element: dict, msg: MQTTMessage, message: dict) -> tuple[str, str]:
        name = element.get("label", element["name"])
        if element["name"] in self.KEYWORDS:
            return name, self._process_keyword(element["name"], msg)
        else:
            value = message.get(element["name"], element["default"])
            if "/" in element["name"]:
                for navigation in element["name"].split("/")[1:]:
                    if not isinstance(value, dict):
                        break
                    value = value.get(navigation, element["default"])
            return name, value
    
    def _process_time(self, time_conf: dict, msg: MQTTMessage, message: dict) -> datetime:
        if time_conf["name"] in self.KEYWORDS:
            time_str = self._process_keyword(time_conf["name"], msg)
        else:
            time_str = message.get(time_conf["name"], None)
        if time_str is not None:
            dt = datetime.strptime(time_str, time_conf["format"])
            if "timezone" in time_conf:
                dt.replace(tzinfo=ZoneInfo(time_conf["timezone"]))
        else:
            dt = datetime.now()
        utc_dt = dt.astimezone(ZoneInfo("Etc/UTC"))
        return utc_dt
    
    def interpret_message(self, msg: MQTTMessage) -> Point:
        str_message = msg.payload.decode()
        self.LOGGER.debug(f"UTF-8 message: {str_message}")
        message = json.loads(str_message)
        self.LOGGER.debug("Successfully unmarshalled message")
        point = Point(self._config["measurement"])
        for tag in self._config.get("tags", []):
            point.tag(*self._process_key_value(tag, msg, message))
        for field in self._config.get("fields", []):
            point.field(*self._process_key_value(field, msg, message))
        if "time" in self._config:
            point.time(self._process_time(self._config["time"], msg, message))
        self.LOGGER.debug(f"Interpreted InfluxDB Point: {str(point)}")
        return point

