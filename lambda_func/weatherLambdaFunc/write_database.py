import pandas as pd
import sqlalchemy

def create_engine():
    username = '***'
    password = '***'
    host = '***'
    port = '3306'
    database = '***'

    # Create the SQLAlchemy engine for MySQL
    engine = sqlalchemy.create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')
    return engine

def writeDatabase(city_data, engine):
    try:
        city_data[0].to_sql(name = 'weather_main', con = engine.connect().connection, index=False, if_exists='append')   # -> 'weather_main' Table
        city_data[1].to_sql(name = 'temperature_data', con = engine.connect().connection, index=False, if_exists='append')   # -> 'temperature_data' Table
        city_data[2].to_sql(name = 'pressure_humidity_data', con = engine.connect().connection, index=False, if_exists='append')   # -> 'pressure_humidity_data' Table
        city_data[3].to_sql(name = 'wind_clouds_visibility_data', con = engine.connect().connection, index=False, if_exists='append')   # -> 'wind_clouds_visibility_data' Table
        city_data[4].to_sql(name = 'precipitation_data', con = engine.connect().connection, index=False, if_exists='append')   # -> 'precipitation_data' Table
        city_data[5].to_sql(name = 'region', con = engine.connect().connection, index=False, if_exists='append')   # -> 'region' Table
        city_data[6].to_sql(name = 'day_length', con = engine.connect().connection, index=False, if_exists='append')   # -> 'day__length' Table

    except Exception as e:
        print(e)