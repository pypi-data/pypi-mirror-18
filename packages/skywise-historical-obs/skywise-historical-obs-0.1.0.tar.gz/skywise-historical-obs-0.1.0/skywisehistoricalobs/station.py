from voluptuous import Schema, Any
from skywiserestclient.validation import (datetime, datetime_to_str,
                                          latitude as latitude_type,
                                          longitude as longitude_type)
from skywisehistoricalobs import HistoricalObsResource
from skywisehistoricalobs.observation import StationObservation


class Station(HistoricalObsResource):

    _path = '/stations/{latitude}/{longitude}'

    _deserialize = Schema({
        'id': unicode,
        'description': unicode,
        'location': {
            'latitude': latitude_type,
            'longitude': longitude_type,
            'elevation': float
        },
        'earliest_recorded_at': datetime,
        'latest_recorded_at': datetime,
        'distance': float
    })

    _serialize = Schema({
        'id': unicode,
        'description': unicode,
        'location': {
            'latitude': latitude_type,
            'longitude': longitude_type,
            'elevation': float
        },
        'earliest_recorded_at': datetime_to_str,
        'latest_recorded_at': datetime_to_str,
        'distance': float
    })

    _args = Schema({
        'limit': int,
        'radius': Any(float, int)
    })

    def __init__(self, **kwargs):
        super(Station, self).__init__(**kwargs)

    @classmethod
    def nearest(cls, latitude, longitude, **kwargs):
        return Station.find(latitude=latitude, longitude=longitude, **kwargs)

    def observations(self, **kwargs):
        return StationObservation.find(station_id=self.id, **kwargs)

