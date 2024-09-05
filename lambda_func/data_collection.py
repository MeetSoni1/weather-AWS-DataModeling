import requests as rq
from datetime import datetime
import time
import pandas as pd
import sqlalchemy

#add logging
cap = pd.read_csv('country-capital-lat-long-population.csv')
cap.set_index('Capital City', inplace=True)

cities = ['Berlin', 'Oslo', 'Madrid', 'Rome', 'Paris', 'Athens', 'London', 'Vienna', 'Ottawa', 'Washington DC',
          'Brasilia', 'Moscow', 'Canberra', 'Wellington', 'Cape Town', 'Cairo', 'Seoul', 'Tokyo', 'Delhi']
def coord(city : str) -> str:
    # will read latitude and longitude from the database 'Area' table
    # SELECT latitude, longitude FROM Area WHERE country_capital == 'city'
    return str(cap['Longitude'].loc[city]), str(cap['Latitude'].loc[city])

long, lat = coord()

async def dataRequest():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={key}"

    resp = rq.get(url)
    print(resp.status_code)   # add in logging
    resp = resp.json()

async def dataCollection():
    pass

def dataCleaning():
    resp['main']['timestamp'] = resp['dt']

    a = datetime.fromtimestamp(resp['dt'])

    weather_data[str(a)] = resp['main']
    weather_data[str(a)]['city'] = city

    df = pd.DataFrame(weather_data)
    df = df.T
    df.reset_index(inplace=True)
    #Data validation(at the end) - check the types of the data matches the column data types in the database
    
def writeDatabase():
    engine = sqlalchemy.create_engine('***')
    try:
        df.to_sql(name = 'weather', con = engine, index=False, if_exists='append')
    except:
        print(error)