# import opendatasets as od
import pandas as pd
from sqlalchemy import create_engine
import re
import os
import logging
from datetime import datetime
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# Configuring Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


def _get_table_names(file_name: str) -> str:
    match = re.search(r"olist_(.*?)_dataset.csv", file_name)
    if match:
        table_name = match.group(1)
    else:
        other_match = other_match = re.search(r"^(.*)\.csv$", file_name)
        if other_match:
            table_name = other_match.group(1)
        else:
            logging.error(f"No matching pattern found for {file_name}")
    return table_name


def load_data_to_postgresql(data_path: str, connection_string: str) -> list:
    logging.info("Loading CSV files to PostgreSQL database")
    try:
        engine = create_engine(connection_string)
        file_names = os.listdir(data_path)
        column_list = []
        for file in file_names:
            table_name = _get_table_names(file)
            df = pd.read_csv(f"{data_path}/{file}")
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            column_list.append(table_name)
            logging.info(f"Table {table_name} from {file} file loaded successfully")
    except Exception as e:
        logging.error(f"Error loading data to PostgreSQL: {e}")
        raise e
    print("Data successfuly loaded to PostgreSQL database")
    return column_list

def postgres_to_gcs(column_list: list, connection_id: str, bucket_name: str):
    for table_name in column_list:
        cur_time=datetime.now()
        PostgresToGCSOperator(
            task_id="postgres_to_gcs",
            postgres_conn_id=connection_id,
            sql=f"select * from {table_name}",
            bucket=bucket_name,
            filename=f"{table_name}_{cur_time}",
            export_format="CSV",
            
        )