from datetime import datetime, date

from requests import Session
from media_server_api.service_controller import ServiceController, ControlException
from media_server_api.service_controller.jellyfin import config
from media_server_api.models.conf_param import ConfParam
from media_server_api.models.conf_param_type import ConfParamType
from media_server_api.models.conf_param_description import ConfParamDescription
from media_server_api.models.integer_range_conf_param import IntegerRangeConfParam


class JellyfinController(ServiceController):
    _TRANSCODING_KEY = "Transcoding"
    _CONNECTIVITY_KEY = "Connectivity"
    _API_ENDPOINTS = {
    _TRANSCODING_KEY: "/System/Configuration/encoding",
    _CONNECTIVITY_KEY: "/System/Info"
    }

    _CONFIGURATION_PARAMS = {
        "EncodingThreadCount": ConfParam(
            id="EncodingThreadCount",
            name="Number of threads used for encoding",
            type=ConfParamType.INTEGER_RANGE,
            description=IntegerRangeConfParam(min_value=-1, max_value=8)
        ),
        "EnableThrottling": ConfParam(
            id="EnableThrottling",
            name="Stop transcoding once it gets far ahead enough from the current playback position",
            type=ConfParamType.BOOLEAN,
            description=False
        ),
        "ThrottleDelaySeconds": ConfParam(
            id="ThrottleDelaySeconds",
            name="Number of seconds the transcoder must be ahead of the playback position to throttle",
            type=ConfParamType.INTEGER_RANGE,
            description=IntegerRangeConfParam(min_value=1)
        ),
        "EnableHardwareEncoding": ConfParam(
            id="EnableHardwareEncoding",
            name="Enable or disable hardware-acceleration transcoding",
            type=ConfParamType.BOOLEAN,
            description=False
        ),
        # HardwareAccelerationType causes issues on Jellyfin's side. Best left out for now.
        #"HardwareAccelerationType": ConfParam(
        #    id="HardwareAccelerationType",
        #    name="Type of hardware acceleration to use",
        #    type=ConfParamType.STRING_VALUE_LIST,
        #    description=["v4l2m2", "none"]
        #),
        "AllowHevcEncoding": ConfParam(
            id="AllowHevcEncoding",
            name="Enable HEVC transcoding",
            type=ConfParamType.BOOLEAN,
            description=False
        ),
        "AllowAv1Encoding": ConfParam(
            id="AllowAv1Encoding",
            name="Enable AV1 encoding",
            type=ConfParamType.BOOLEAN,
            description=False
        ),
        "EnableSegmentDeletion": ConfParam(
            id="EnableSegmentDeletion",
            name="Delete segments after being downloaded from the client",
            type=ConfParamType.BOOLEAN,
            description=False
        ),
        "SegmentKeepSeconds": ConfParam(
            id="SegmentKeepSeconds",
            name="Seconds to keep each segment for before being discarded",
            type=ConfParamType.INTEGER_RANGE,
            description=IntegerRangeConfParam(min_value=1)
        )
    }

    def __enter__(self):
        self._session = Session()
        self._session.headers.update({"Authorization": f'MediaBrowser Token="{config.JELLYFIN_API_KEY}"'})
        return self

    def _check_range(self, param_definition: ConfParam, param_value) -> bool:
        valid = True
        if param_definition.description.min_value is not None:
            valid = valid and param_definition.description.min_value <= param_value
        if valid and param_definition.description.max_value is not None:
            valid = param_definition.description.max_value >= param_value
        return valid
    

    def _validate_param(self, param_definition: ConfParam, param_value) -> bool:
        if param_definition.type == ConfParamType.BOOLEAN:
            return isinstance(param_value, bool)
        elif param_definition.type == ConfParamType.INTEGER_RANGE:
            return isinstance(param_value, int) and self._check_range(param_definition, param_value)
        elif param_definition.type == ConfParamType.RANGE:
            return isinstance(param_value, (int, float)) and self._check_range(param_definition, param_value)
        elif param_definition.type == ConfParamType.BYTE:
            return isinstance(param_value, (bytes, bytearray))
        elif param_definition.type == ConfParamType.DATETIME_RANGE:
            return isinstance(param_value, datetime) and self._check_range(param_definition, param_value)
        elif param_definition.type == ConfParamType.DATE_RANGE:
            return isinstance(param_value, date) and self._check_range(param_definition, param_value)
        elif param_definition.type == ConfParamType.BINARY:
            return True # No validation is done, as it is a file with no format
        elif param_definition.type == ConfParamType.BINARY_VALUE_LIST:
            return param_value in param_definition.description
        elif param_definition.type == ConfParamType.BYTE_VALUE_LIST:
            return isinstance(param_value, bytes) and param_value in param_definition.description
        elif param_definition.type == ConfParamType.DATE_VALUE_LIST:
            return isinstance(param_value, date) and param_value in param_definition.description
        elif param_definition.type == ConfParamType.DATETIME_VALUE_LIST:
            return isinstance(param_value, datetime) and param_value in param_definition.description
        elif param_definition.type == ConfParamType.INTEGER_VALUE_LIST:
            return isinstance(param_value, int) and param_value in param_definition.description
        elif param_definition.type == ConfParamType.NUMERIC_VALUE_LIST:
            return isinstance(param_value, (int, float)) and param_value in param_definition.description
        elif param_definition.type == ConfParamType.STRING_VALUE_LIST:
            return isinstance(param_value, str) and param_value in param_definition.description
        else:
            return False

    def discover_configuration(self) -> list[str]:
        return sorted(list(self._CONFIGURATION_PARAMS.keys()))

    def describe_param(self, param_id: str) -> ConfParam|None:
        return self._CONFIGURATION_PARAMS.get(param_id)

    def set_param_value(self, param_id: str, param_value) -> bool:
        # We assume that the caller already checked the param exists.
        # Else, they get a much deserved exception.
        # This also rejects setting undeclared params
        if isinstance(param_value, str) and ((param_value[0] == '"' and param_value[-1] == '"') or (param_value[0] == "'" and param_value[-1] == "'")):
            param_value = param_value[1:-1] # Remove starting-trailing quotes
        valid = self._validate_param(self._CONFIGURATION_PARAMS[param_id], param_value)
        if valid:
            valid = self._call_param_update(param_id, param_value)
        return valid

    def _call_param_update(self, param_id: str, param_value) -> bool: # TODO implement
        return self._session.post(f"{config.JELLYFIN_URL}{self._API_ENDPOINTS[self._TRANSCODING_KEY]}", json={param_id: param_value}).ok

    def get_param_value(self, param_id: str):
        if param_id in self._CONFIGURATION_PARAMS: # Security hole otherwise - Undeclared params could be queried
            param_val = self._call_param_get(param_id)
        else:
            param_val = None
        return param_val

    def _call_param_get(self, param_id: str):
        transcoding_req = self._session.get(f"{config.JELLYFIN_URL}{self._API_ENDPOINTS[self._TRANSCODING_KEY]}")
        if transcoding_req.ok and 'json' in transcoding_req.headers.get("content-type", ''):
            transcoding_conf = transcoding_req.json()
            return transcoding_conf.get(param_id)

    def check_connectivity(self) -> int:
        return self._session.get(f"{config.JELLYFIN_URL}{self._API_ENDPOINTS[self._CONNECTIVITY_KEY]}").status_code
    
    def __exit__(self, *exc):
        self._session.close()