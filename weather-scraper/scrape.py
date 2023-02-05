import json
from collections.abc import Iterable

import aiohttp
import xmltodict
from aiohttp import ClientResponseError
from datetime import datetime, timezone

from model import WeatherStation, GeoJSON
from util import clean_keys, coord_to_float, get_nested_val, POST_URL

TIMESTAMP_READ_FMT = "%Y%m%d%H%M%S"
TIMESTAMP_WRITE_FMT = "%Y-%m-%dT%H:%M:%S%z"


async def scrape_station_details():
    """Get weather station details."""
    url: str = "https://dd.weather.gc.ca/citypage_weather/xml/siteList.xml"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            sites = xmltodict.parse(await response.text())["siteList"]["site"]
            return [
                WeatherStation(
                    name=site["nameEn"],
                    code=site["provinceCode"],
                    sid=site["@code"],
                    geolocation=None
                )
                for site in sites
            ]


async def scrape_weather(
        station: WeatherStation,
        language: str = "e") -> dict:
    """
    Scrapes, cleans, and adds GeoJSON coords/timestamp to raw weather data.
    :param station: The station from which to scrape
    :param language: The language to scrape in ('e' or 'f')
    :return: Clean weather data
    """
    url: str = f"https://dd.weather.gc.ca/citypage_weather/xml" \
               f"/{station.code}/{station.sid}_{language}" \
               f".xml"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                response.raise_for_status()
                weather = xmltodict.parse(await response.text())["siteData"]

                # some xml cleanup
                try:
                    del weather["@xmlns:xsi"]
                    del weather["@xsi:noNamespaceSchemaLocation"]
                except KeyError as err_k:
                    print("Could not delete xml tags", err_k)

                clean_keys(weather)

                # add timestamp
                try:
                    raw_timestamp = weather["dateTime"][0]["timeStamp"]
                    timestamp = datetime.strptime(
                        raw_timestamp, TIMESTAMP_READ_FMT
                    )
                    weather["timestamp"] = timestamp.astimezone(timezone.utc)\
                        .strftime(TIMESTAMP_WRITE_FMT)
                except (KeyError, IndexError) as err_k:
                    print("Could not create timestamp", err_k)
                    return

                # add geolocation
                coord_paths = [
                    ["location", "name"],
                    ["currentConditions", "station"],
                ]

                for path in coord_paths:
                    try:
                        ddict = get_nested_val(weather, path)

                        lon = coord_to_float(ddict["lon"])
                        lat = coord_to_float(ddict["lat"])

                        weather["geolocation"] = GeoJSON([lon, lat]).to_dict()
                    except (KeyError, TypeError) as err:
                        print("Could not create geolocation", err)
                        return

                # post
                await session.post(POST_URL, json=weather)

            except ClientResponseError as err_r:
                print("failed:", url, err_r)


async def scrape_weather_stations(weather_stations: Iterable[WeatherStation]):
    for idx, station in enumerate(weather_stations):
        await scrape_weather(station)

