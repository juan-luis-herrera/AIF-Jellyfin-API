import os

SLO_FILE = os.getenv("SLO_FILE", default="slos.json")
"""File storing the SLO definitions"""

INFLUX_URL = os.getenv("INFLUX_URL", default="http://localhost:8086")
"""URL to connect to InfluxDBv2 (as a telemetry database)"""

INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", default="december")
"""Token for authenticating with InfluxDB (as a telemetry database)"""

INFLUX_ORG = os.getenv("INFLUX_ORG", default="tuwien")
"""Token for authenticating with InfluxDB (as a telemetry database)"""

INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", default="telemetry")
"""Bucket to write data to in InfluxDB"""