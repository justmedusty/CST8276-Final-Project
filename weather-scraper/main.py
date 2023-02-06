import asyncio
# making sure this comment pushes
from scrape import scrape_station_details, scrape_weather_stations

stations = asyncio.run(scrape_station_details())

while True:
    asyncio.run(scrape_weather_stations(stations))
