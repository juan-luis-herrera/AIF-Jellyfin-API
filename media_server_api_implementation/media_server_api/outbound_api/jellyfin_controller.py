from datetime import datetime, date

import requests
from media_server_api import config
from media_server_api.models.conf_param import ConfParam
from media_server_api.models.conf_param_type import ConfParamType
from media_server_api.models.conf_param_description import ConfParamDescription
from media_server_api.models.integer_range_conf_param import IntegerRangeConfParam

_TRANSCODING_KEY = "Transcoding"
_API_ENDPOINTS = {
    _TRANSCODING_KEY: "/System/Configuration/encoding"
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
    "HardwareAccelerationType": ConfParam(
        id="HardwareAccelerationType",
        name="Type of hardware acceleration to use",
        type=ConfParamType.STRING_VALUE_LIST,
        description=["v4l2m2", "none"]
    ),
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
    
_HEADERS = {"Authorization": f'MediaBroswer Token="{config.JELLYFIN_API_KEY}"'}

def _check_range(param_definition: ConfParam, param_value) -> bool:
    valid = True
    if param_definition.description.min_value is not None:
        valid = valid and param_definition.description.min_value <= param_value
    if valid and param_definition.description.max_value is not None:
        valid = param_definition.description.max_value >= param_value
    return valid

def _validate_param(param_definition: ConfParam, param_value) -> bool:
    if param_definition.type == ConfParamType.BOOLEAN:
        return isinstance(param_value, bool)
    elif param_definition.type == ConfParamType.INTEGER_RANGE:
        return isinstance(param_value, int) and _check_range(param_definition, param_value)
    elif param_definition.type == ConfParamType.RANGE:
        return isinstance(param_value, (int, float)) and _check_range(param_definition, param_value)
    elif param_definition.type == ConfParamType.BYTE:
        return isinstance(param_value, (bytes, bytearray))
    elif param_definition.type == ConfParamType.DATETIME_RANGE:
        return isinstance(param_value, datetime) and _check_range(param_definition, param_value)
    elif param_definition.type == ConfParamType.DATE_RANGE:
        return isinstance(param_value, date) and _check_range(param_definition, param_value)
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
