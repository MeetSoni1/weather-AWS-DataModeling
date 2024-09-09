import pandas as pd
import sqlalchemy

# Defining RDS database parameters
username = '***'
password = '***'
host = '***'
port = '3306'
database = '***'

# Create the SQLAlchemy engine for MySQL
engine = sqlalchemy.create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

# Read the local CSV file into a pandas DataFrame
df = pd.read_csv('/city_lat_long_lookup_table.csv')

# Write the DataFrame to the MySQL database
try:
    with engine.connect() as conn:
        print("Connection to database was successful.")
        df.to_sql(name='city_coordinates', con=conn.connection , index=False , if_exists='append')
except Exception as e:
    print(f"Error writing to the database: {e}")