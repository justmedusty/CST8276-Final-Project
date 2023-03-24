from fastapi import FastAPI, HTTPException

from db.db import ping, insert, find
from db.models import WeatherData

app = FastAPI()


@app.get("/health", status_code=204)
async def health():
    """MongoDB server health check.
    Returns 204 if the server is available, else 503.
    """
    if not ping():
        raise HTTPException(status_code=503, detail="Service not available")


@app.post("/weather", status_code=204)
async def weather(data: WeatherData):
    insert(data)


@app.get("/weather", status_code=200)
async def weather(loc: dict):
    """e.g., GET /weather?lon=100.8&lat=73.5"""
    return find(loc["lon"], loc["lat"])

