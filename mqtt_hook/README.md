# MQTT hook

This is a small submodule for transporting data from MQTT to a time-series database.

## How it works

The MQTT hook subscribes to a given topic on MQTT. When it receives a message on that topic, it sends the message to a database connector to save it on the time-series database. The database connector is equipped with a message interpreter, which unmarshalls the payload of the MQTT message and converts it into a time-series entry, formatted according to the provided configuration.

## Basic architecture

- The project is expected to have one hook only (Class `mqtt_hook.MQTTHook`).
- The hook is created with a list of database connectors that it will feed into (class `database.DatabaseConnector`).
- Each database connector is created with an interpreter (class `interpret.MessageInterpreter`).
- When a MQTT message is received, the hook passes it into the database connector, which relies on the interpreter to create its corresponding entry.

## Currently supported connectors and interpreters

- InfluxDB (`database.InfluxDBConnector`). Its interpreters must inherit from `interpret.MessageInterpreterInflux`. As of now, the current interpreters are available:
    - JSON (`interpret.MessageInterpreterJSONInflux`).

## Hook configuration

### Interpreter configuration

The interpreter can be configured with a JSON file. There are keywords for some MQTT data that is not in the message payload:

- `$TOPIC` will load the message topic.
- `$MID` will load the message ID.
- `$TS` will load the message timestamp.

#### MessageInterpreterJSONInflux configuration format

```json
{
    "measurement": "<NAME-OF-THE-MEASUREMENT>",
    "tags": [
        {
            "name": "<JSON-ATTRIBUTE-TO-LOAD>",
            "label": "<NAME-OF-TAG-IN-INFLUXDB>", // Optional, the value of name is used if none provided
            "default": "<DEFAULT-TAG-VALUE>"
        },
        //...
    ],
    "fields": [
        {
            "name": "<JSON-ATTRIBUTE-TO-LOAD>",
            "label": "<NAME-OF-TAG-IN-INFLUXDB>", // Optional, the value of name is used if none provided
            "default": "<DEFAULT-TAG-VALUE>"
        },
        //...
    ],
    "time": {
        "name": "<JSON-ATTRIBUTE-TO-LOAD>",
        "format": "<DATETIME-FORMAT-STRING>",
        "timezone": "<TZ-DATABASE-TIMEZONE-NAME>" // Optional, Europe/Vienna is assumed if none provided
    }
}
```

You can navigate across levels of the JSON objects received using `/`. For example:

```json
{
    "description": "This is an example telemetry object",
    "data": {
        "value": "The value you would like to store"
    }
}
```

Using the name `data/value` in your tag/field, the hook will load `"The value you would like to store"` in the appropriate tag/field of the InfluxDB `Point`.


### Environment configuration

Check `config.py` for the environment variables used by the hook.