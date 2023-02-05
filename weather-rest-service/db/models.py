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







