# import opendatasets as od
import pandas as pd
from sqlalchemy import create_engine
import re
import logging


# Configuring Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


def _get_table_names(file_name: str) -> str:
    """
    This function takes the names of datasets and extracts words to be used as table names

    """
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


def load_data_to_psql(file_names: list, data_path: str, connection_string: str) -> list:
    """
    This function reads the csv files and writes each one into a table in the database.
    Returns a list of table names extracted from each csv file name
    """
    logging.info("Loading CSV files to PostgreSQL database")
    try:
        engine = create_engine(connection_string)
        table_list = []
        for file in file_names:
            table_name = _get_table_names(file)
            df = pd.read_csv(f"{data_path}/{file}")
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            table_list.append(table_name)
            logging.info(f"Table {table_name} from {file} file loaded successfully")
    except Exception as e:
        logging.error(f"Error loading data to PostgreSQL: {e}")
        raise e
    return table_list


def extract_from_psql(table_name: str, connection_string: str):
    """
    This function queries the database and stores the result in a dataframe
    Returns a dataframe
    """
    engine = create_engine(connection_string)
    sql_query = f"select * from {table_name}"
    data = pd.read_sql(sql_query, engine)
    return data
