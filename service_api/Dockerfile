FROM python:3-alpine

ENV WORKERS=1
ENV LISTEN_HOST=0.0.0.0
ENV LOG_LEVEL=info

WORKDIR /serviceapi

COPY requirements.txt /serviceapi

RUN pip3 install --no-cache-dir -r requirements.txt

COPY media_server_api /serviceapi/media_server_api

EXPOSE 80

ENTRYPOINT [ "python3" ]

CMD [ "-m", "media_server_api" ]