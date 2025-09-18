FROM python:3.13-slim

LABEL org.opencontainers.image.authors="Juan Luis Herrera <j.gonzalez@dsg.tuwien.ac.at>"
LABEL org.opencontainers.image.version="0.0.1"
LABEL org.opencontainers.image.title="MQTT2TSDB hook"
LABEL org.opencontainers.image.description="Small service to write time-series data to a database from an incoming MQTT stream."

WORKDIR /hook
COPY * /hook/
RUN pip3 install -r requirements.txt --no-cache-dir

ENTRYPOINT [ "python3" ]
CMD [ "mqtt_hook.py" ]