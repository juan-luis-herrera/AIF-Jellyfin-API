#!/usr/bin/env python3
import logging

import connexion
from flask_cors import CORS
from gunicorn.app.base import BaseApplication

from media_server_api import encoder, api_bridge, config
from media_server_api.service_controller.jellyfin import JellyfinController
from media_server_api.slo_controller import InfluxDBSLOController
from media_server_api.slo_controller.parser import JSONSLOParser

class GunicornWorkaround(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                 if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    with JellyfinController() as controller:
        api_bridge.SERVICE_CONTROLLER = controller
        with InfluxDBSLOController(JSONSLOParser) as slo_controller:
            api_bridge.SLO_CONTROLLER = slo_controller
            app = connexion.App(__name__, specification_dir='./openapi/')
            app.app.json_encoder = encoder.JSONEncoder
            app.add_api('openapi.yaml',
                        arguments={'title': 'Service API'},
                        pythonic_params=True)

            # add CORS support
            CORS(app.app)

            gunicorn_options = {
                "bind": f"{config.LISTEN_HOST}:80",
                "workers": config.WORKERS,
                "log-level": config.LOG_LEVEL
            }

            GunicornWorkaround(app.app, gunicorn_options).run()

            #app.run(port=80)
            
if __name__ == '__main__':
    main()
