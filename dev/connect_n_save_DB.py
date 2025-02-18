import psycopg2
from sqlalchemy import create_engine

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres" # Update this with your actual password
        )
        print("PostgreSQL database connection established successfully.")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while connecting to PostgreSQL database: {error}")
        return None

def save_dataframe_to_database(df, conn, table_name):
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/postgres') # Update this with your actual password
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Data has been successfully added to the PostgreSQL database table {table_name}.")

