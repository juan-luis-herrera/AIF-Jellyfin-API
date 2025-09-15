#!/usr/bin/env python3

import connexion
from flask_cors import CORS

from media_server_api import encoder, api_bridge
from media_server_api.service_controller.jellyfin import JellyfinController

def main():
    with JellyfinController() as controller:
        api_bridge.CONTROLLER = controller
        app = connexion.App(__name__, specification_dir='./openapi/')
        app.app.json_encoder = encoder.JSONEncoder
        app.add_api('openapi.yaml',
                    arguments={'title': 'Service API'},
                    pythonic_params=True)

        # add CORS support
        CORS(app.app)

        app.run(port=8080)


if __name__ == '__main__':
    main()
