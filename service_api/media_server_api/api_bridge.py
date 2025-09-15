from media_server_api.service_controller import ServiceController

## As proper dependency injection for the OpenAPI server is not an option, this module replaces it.
## These variables are read and used by the API. They have hints on what to populate them with.
## To populate them, go to the __main__ module. They are populated within the main() function.

CONTROLLER : ServiceController