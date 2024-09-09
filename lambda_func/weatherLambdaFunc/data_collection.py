import json
import asyncio
from datetime import datetime
import boto3
import sqlalchemy
import aiohttp
import requests
import pandas as pd
import logging

from write_database import create_engine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fetch API key from SSM parameter Store
aws_client = boto3.client('ssm')
response = aws_client.get_parameter(Name='/weather/tf_openWeatherAPI', WithDecryption=True)
key = response['Parameter']['Value']

# List of countries to process
cities = ['berlin', 'oslo', 'madrid', 'rome', 'paris', 'athens', 'london', 'vienna', 'ottawa-gatineau', 'washington, d.c.', 'mexico city', 'hong kong', 'moscow', 'canberra', 'wellington', 'cape town', 'cairo', 'seoul', 'tokyo', 'delhi']

engine = create_engine()
mycursor = engine.cursor()

def coord(city: str) -> tuple:
    try:
        mycursor.execute(f"SELECT latitude, longitude FROM city_coordinates WHERE capital_city = '{city}'")
        result = mycursor.fetchone()
        if result:
            latitude, longitude = result
            logging.info(f"Coordinates for {city}: {latitude}, {longitude}")
            return longitude, latitude
        else:
            logging.error(f"No coordinates found for {city}")
            return None, None
    except Exception as e:
        logging.error(f"Error fetching coordinates for {city} from RDS Database: {e}")
        return None, None

async def dataRequest(city):
    long, lat = coord(city)
    if not lat or not long:
        logging.error(f"Skipping {city} due to missing coordinates.")
        return {}

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={key}"
    logging.info(f"Sending data request for {city}: {url}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                logging.info(f"Response status for {city}: {response.status}")
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f"Failed to fetch data for {city}, status code: {response.status}")
                    return {}
    except Exception as e:
        logging.error(f"Error fetching data for {city}: {e}")
        return {}

async def dataCollection():
    logging.info('Start collecting data.')

    t_start = datetime.now()
    tasks = [dataRequest(city) for city in cities]
    results = await asyncio.gather(*tasks)
    t_end = datetime.now() - t_start

    logging.info('Data collection completed.')    
    logging.info(f"Total time taken to retrive API data: {t_end}")
    return results