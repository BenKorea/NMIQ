import pandas as pd
import pydicom
import psycopg2
from sqlalchemy import create_engine
from a2_filter_dicom_files_by_description import patient_protocol_files
from a0_extracted_dicom_tag_information import tag_information, subtag_information
from Making_Dose_Report_Table import convert_data_types



def extract_data(dicom_files, tag_information):
    data = []
    for dicom_data in dicom_files:
        row = {}
        for tag, desc, _ in tag_information:
            value = dicom_data.get(tag, None)
            row[desc] = value.value if value is not None else None
        data.append(row)
    return pd.DataFrame(data)

df_tags = extract_data(patient_protocol_files, tag_information)
# Convert data types
convert_data_types(df_tags, df_tags)


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

conn = connect_to_database()
if conn:
    save_dataframe_to_database(df_tags, conn, "Dose_Report")
    conn.close()
    print("Database connection closed.")