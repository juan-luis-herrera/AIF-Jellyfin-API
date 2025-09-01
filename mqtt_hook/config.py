import os

MQTT_BROKER = os.getenv("MQTT_BROKER", default="localhost")
"""Host to connect to as a broker for MQTT telemetry"""

MQTT_PORT = int(os.getenv("MQTT_PORT", default=1883))
"""Port to connect to as a broker for MQTT telemetry"""

MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", default="media-server-api")
"""Formattable string used to genreate the MQTT client ID"""

MQTT_TOPIC = os.getenv("MQTT_TOPIC", default="autowatcher/reporting")
"""Topic to subscribe to for data gathering"""

DATETIME_FORMAT_STRING = os.getenv("DATETIME_FORMAT_STRING", default="%Y-%m-%d %H:%M:%S")
"""Format string for datetimes"""

INFLUX_URL = os.getenv("INFLUX_URL", default="http://localhost:8086")
"""URL to connect to InfluxDBv2 (as a telemetry database)"""

INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", default="nSDsQp9hnVDKOheerHe3ZGbdXhQgAR8IajVJt356xkXQ-SC1vxB4w75NCWTkrMi27t-OsBcVNRwBK4M2jiCWxQ==")
"""Token for authenticating with InfluxDB (as a telemetry database)"""

INFLUX_ORG = os.getenv("INFLUX_ORG", default="tuwien")
"""Token for authenticating with InfluxDB (as a telemetry database)"""

INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", default="telemetry")
"""Bucket to write data to in InfluxDB"""

INFLUX_MEASUREMENT = os.getenv("INFLUX_MEASUREMENT", default="jellyfin-qos")
"""Measurement for data stored in InfluxDB"""