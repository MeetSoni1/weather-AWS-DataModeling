from datetime import datetime
import pandas as pd

def dataPrep(data):
    def create_df(dict):
        df = pd.DataFrame(dict.items())
        df = df.set_index(0).T.reset_index(drop=True)
        return df
    
    record_time = datetime.fromtimestamp(data['dt'])   # -> datetime.datetime
    city_name = data['name'].lower()   #-> str

    # 'weather_main' Table
    weather_main_dict = {'record_time': record_time, 'city_name':city_name}
    weather_main_df = create_df(weather_main_dict)

    # 'temperature_data' Table
    temp = data['main']['temp']   # -> float
    feels_like = data['main']['feels_like']   # -> float
    temp_min = data['main']['temp_min']   # -> float
    temp_max = data['main']['temp_max']   # -> float

    temp_dict = {'record_time': record_time, 'city_name':city_name, 'temp': temp, 'feels_like': feels_like, 'temp_min':  temp_min, 'temp_max':  temp_max}
    temp_df = create_df(temp_dict)

    # 'pressure_humidity_data' Table
    pressure = data['main']['pressure']   # -> int
    humidity = data['main']['humidity']   # -> int
    sea_level = data['main']['sea_level']   # -> int
    grnd_level = data['main']['grnd_level']   # -> int

    pressure_humidity_dict = {'record_time': record_time, 'city_name':city_name,'pressure':  pressure, 'humidity':  humidity, 'sea_level': sea_level, 'grnd_level': grnd_level}
    pressure_humidity_df = create_df(pressure_humidity_dict)

    # 'wind_clouds_visibility_data' Table
    wind_speed = data['wind']['speed']   # -> float
    wind_deg = data['wind']['deg']   # -> int
    try:
        wind_gust = data['wind']['gust']   # -> float
    except:
        wind_gust = None
    clouds = data['clouds']['all']   # -> int
    visibility = data['visibility']   # -> int

    wind_clouds_visibility_dict = {'record_time':record_time, 'city_name':city_name, 'visibility':visibility, 'wind_speed':wind_speed, 'wind_deg':wind_deg, 'wind_gust':wind_gust, 'clouds':clouds}
    wind_clouds_visibility_df = create_df(wind_clouds_visibility_dict)

    # 'precipitation_data' Table
    try:    
        rain = data['rain']['1h']   # -> float
    except:
        rain = None

    try:
        snow = data['snow']['1h']   # -> float
    except:
        snow = None

    precipitation_dict = {'record_time': record_time, 'city_name':city_name, 'rain':rain, 'snow':snow}
    precipitation_df = create_df(precipitation_dict)

    # 'area' Table
    city_name = data['name']   #-> str
    country_code = data['sys']['country']   #-> str
    timezone = data['timezone']   #-> str

    area_dict = {'city_name': city_name, 'country_code':country_code, 'timezone':timezone}
    area_df = create_df(area_dict)

    # 'general_weather' Table
    general = data['weather'][0]['main']   #-> str
    sunrise = data['sys']['sunrise']   #-> str
    sunset = data['sys']['sunset']   #-> str

    general_weather_dict = {'record_time': record_time, 'city_name': city_name,'general':general, 'sunrise':sunrise, 'sunset':sunset}
    general_weather_df = create_df(general_weather_dict)

    #Data validated - checked the types of the data that should matche the column data types in the database
    
    return weather_main_df, temp_df, pressure_humidity_df, wind_clouds_visibility_df, precipitation_df, area_df, general_weather_df