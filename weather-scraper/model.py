from dataclasses import dataclass
from datetime import datetime


@dataclass
class GeoJSON:
    """A GeoJSON compliant obj"""
    coordinates: list[float, float]
    """(<longitude>, <latitude>)"""

    type: str = "Point"

    def to_dict(self) -> dict[str, str]:
        return {
            "type": self.type,
            "coordinates": self.coordinates
        }


@dataclass
class WeatherStation:
    name: str
    """The name of the station: from metadata.station"""

    code: str
    """Province or territory code"""

    sid: str
    """Weather station id"""

    geolocation: GeoJSON | None
    """The location of the weather station"""

    last_forecast_time: datetime | None = None
    """The datetime of the last forecast scraped"""
