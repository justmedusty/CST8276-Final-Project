from datetime import datetime

from pydantic import BaseModel


class GeoJSON(BaseModel):
    coordinates: tuple[float, float]
    """(<longitude>, <latitude>)"""

    type: str = "Point"

    def longitude(self) -> float:
        return self.coordinates[0]

    def latitude(self) -> float:
        return self.coordinates[1]


class WeatherData(BaseModel):
    license: str

    timestamp: datetime
    geolocation: GeoJSON

    dateTime: list
    location: dict
    warnings: dict | None
    currentConditions: dict
    forecastGroup: dict
    hourlyForecastGroup: dict
    yesterdayConditions: dict
    riseSet: dict
    almanac: dict


def weather_to_dict(weather):
    return {
        "_id": str(weather["_id"]),
        "license": weather["license"],

        "timestamp": weather["timestamp"],
        "geolocation": weather["geolocation"],
        "distanceToNearestStation": weather["dist"]["calculated"],

        "dateTime": weather["dateTime"],
        "location": weather["location"],
        "warnings": weather["warnings"],
        "currentConditions": weather["currentConditions"],
        "forecastGroup": weather["forecastGroup"],
        "hourlyForecastGroup": weather["hourlyForecastGroup"],
        "yesterdayConditions": weather["yesterdayConditions"],
        "riseSet": weather["riseSet"],
        "almanac": weather["almanac"],
    }




