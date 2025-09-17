import os

MQTT_BROKER = os.getenv("MQTT_BROKER", default="localhost")
"""Host to connect to as a broker for MQTT telemetry"""

MQTT_PORT = int(os.getenv("MQTT_PORT", default=1883))
"""Port to connect to as a broker for MQTT telemetry"""

MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", default="media-server-api")
"""Formattable string used to genreate the MQTT client ID"""

MQTT_TOPIC = os.getenv("MQTT_TOPIC", default="autowatcher/reporting")
"""Topic to subscribe to for data gathering"""

INFLUX_URL = os.getenv("INFLUX_URL", default="http://localhost:8086")
"""URL to connect to InfluxDBv2 (as a telemetry database)"""

INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", default="december")
"""Token for authenticating with InfluxDB (as a telemetry database)"""

INFLUX_ORG = os.getenv("INFLUX_ORG", default="tuwien")
"""Token for authenticating with InfluxDB (as a telemetry database)"""

INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", default="telemetry")
"""Bucket to write data to in InfluxDB"""

CONFIG_FILE = os.getenv("CONFIG_FILE", default="mqtt_hook/confs/jellyfin-qos.json")
"""File to configure the MQTT hook"""