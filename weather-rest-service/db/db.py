import json
import os
from typing import Mapping

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from db.models import WeatherData, weather_to_dict

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
WEATHER_COLLECTION = os.getenv("WEATHER_COLLECTION")


def client() -> MongoClient[Mapping[str, any] | any]:
    return MongoClient(MONGO_URL)


def ping() -> bool:
    """Pings Mongo server for a health check"""
    try:
        client().admin.command('ping')
        return True
    except ConnectionFailure:
        return False


def db() -> Database[Mapping[str, any] | any]:
    return client()[MONGO_DB]


def weather_collection() -> Collection[Mapping[str, any] | any]:
    return db()[WEATHER_COLLECTION]


def find(lon: float, lat: float):
    try:  # TODO, find most recent doc of nearest weather station
        doc = weather_collection(

        ).aggregate([
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "key": "geolocation",
                    "spherical": True,
                    "distanceField": "distanceFromWeatherStation"
                }
            },
            {
                "$sort": {"distanceFromWeatherStation": 1, "timestamp": -1}
            }
        ]).next()
        return weather_to_dict(doc)
    except:  # TODO, exception handling
        pass


def insert(data: WeatherData):
    try:
        weather_collection().insert_one(data.dict())
    except:  # TODO exception handling
        pass

