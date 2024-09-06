CREATE TABLE city_coordinates(
    city_name VARCHAR(100) PRIMARY KEY,
    country VARCHAR(100),
    latitude FLOAT CHECK (latitude BETWEEN -90 AND 90),
    longitude FLOAT CHECK (longitude BETWEEN -180 AND 180)
);

CREATE TABLE weather_main(
    record_time DATETIME,
    city_name VARCHAR(100),
    PRIMARY KEY (record_time, city_name)
);

CREATE TABLE temperature_data (
    record_time DATETIME,
    city_name VARCHAR(100),
    temp FLOAT,
    feels_like FLOAT,
    temp_min FLOAT,
    temp_max FLOAT,
    PRIMARY KEY (record_time, city_name)
);

CREATE TABLE pressure_humidity_data (
    record_time DATETIME,
    city_name VARCHAR(100),
    pressure FLOAT,
    humidity FLOAT,
    sea_level FLOAT,
    grnd_level FLOAT,
    PRIMARY KEY (record_time, city_name)
);

CREATE TABLE wind_clouds_visibility_data (
    record_time DATETIME,
    city_name VARCHAR(100),
    visibility FLOAT,
    wind_speed FLOAT,
    wind_deg FLOAT,
    clouds FLOAT,
    PRIMARY KEY (record_time, city_name)
);

CREATE TABLE precipitation_data (
    record_time DATETIME,
    city_name VARCHAR(100),
    rain FLOAT DEFAULT 0,
    snow FLOAT DEFAULT 0,
    PRIMARY KEY (record_time, city_name)
);

CREATE TABLE area(
    city_name VARCHAR(100) PRIMARY KEY NOT Null,
    country_code VARCHAR(5),
    timezone INT
);

CREATE TABLE general_weather(
    record_time DATETIME,
    city_name VARCHAR(100),
    general VARCHAR(100),
    sunrise INT,
    sunset INT,
    PRIMARY KEY (record_time, city_name)
);