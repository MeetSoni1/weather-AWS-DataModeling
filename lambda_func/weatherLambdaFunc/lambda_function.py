from datetime import datetime
import logging
import asyncio

import aiohttp
import pandas as pd
import sqlalchemy

from data_collection import dataCollection, cities
from data_prep import dataPrep
from write_database import create_engine, writeDatabase

def lambda_handler():
    # Data Collection
    logging.info('Start collecting data.')
    t_start = datetime.now()

    weatherData = asyncio.run(dataCollection())
    
    t_end = datetime.now() - t_start
    logging.info('Data collection completed.')    
    logging.info(f"Total time taken to retrive API data: {t_end}")
    
    # Data Cleaning
    processed_weatherData = []
    logging.info('Start cleaning data.')
    t_start = datetime.now()

    for city_data in weatherData:
        processed_weatherData.append(dataPrep(city_data))

    t_end = datetime.now() - t_start    
    logging.info('Data cleaning completed.')    
    logging.info(f"Total time taken to clean data: {t_end}")    

    # Write to Database
    logging.info('Start writing to Database.')
    t_start = datetime.now()

    engine = create_engine()
    for processed_city_data in processed_weatherData:
        writeDatabase(processed_city_data, engine)

    t_end = datetime.now() - t_start    
    logging.info('Writing to Database completed.')    
    logging.info(f"Total time taken to write data in Database: {t_end}")  