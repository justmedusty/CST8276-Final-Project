import os

from dotenv import load_dotenv
from pymongo import MongoClient, GEOSPHERE

"""
This assumes that all documents have the following structure
{
    "timestamp": <timestamp>
    "geolocation": GeoJSON
}

We create a time-series collection, and add a geo-spatial index on geo-location.

Note: timestamp MUST be a top-level field
Note: geo-location field conforms to the GeoJSON format. 
"""

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

client = MongoClient(MONGO_URL)
db = client[MONGO_DB]

db.create_collection(
    MONGO_COLLECTION,
    timeseries={
        "timeField": "timestamp",
        "granularity": "minutes"
    }
)

collection = db[MONGO_COLLECTION]

collection.create_index([("geolocation", GEOSPHERE)])
