from voluptuous import Schema, Optional, Any
from skywiserestclient.validation import datetime, datetime_to_str
from skywisehistoricalobs import HistoricalObsResource


def _parameter_list_to_str(l):
    return ",".join(l)


_deserialize_obs = Schema({
    "id": unicode,
    "recorded_at": datetime,
    "measurements": [Schema({
        "parameter": unicode,
        "value": Any(float, int),
        "unit": unicode
    })],
    Optional("metar"): unicode,
    Optional("weather"): unicode
})


_serialize_obs = Schema({
    "id": unicode,
    "recorded_at": datetime_to_str,
    "measurements": [Schema({
        "parameter": unicode,
        "value": Any(float, int),
        "unit": unicode
    })],
    Optional("metar"): unicode,
    Optional("weather"): unicode
})


class StationObservation(HistoricalObsResource):

    _path = '/stations/{station_id}/observations'

    _deserialize = _deserialize_obs

    _serialize = _serialize_obs

    _args = Schema({
        "start": datetime_to_str,
        "end": datetime_to_str,
        "parameters": _parameter_list_to_str
    })
