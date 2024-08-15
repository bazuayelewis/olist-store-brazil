from utils.kaggle_manger import kaggle_downloader
from utils.psql_manager import load_data_to_psql, extract_from_psql
from config import *
from airflow.operators.python import get_current_context
from utils.gcsmanager import GCSManager
from utils.bqmanager import BQManager
import logging


def extract_data():
    kaggle_url = KAGGLE_URL
    data_path = DATA_DIR
    file_list = kaggle_downloader(kaggle_url, data_path)
    return file_list


def elt_local_to_psql():
    context = get_current_context()
    file_list = context["ti"].xcom_pull(task_ids="kaggle_datasets_download")
    data_path = DATA_DIR
    connection_string = CONNECTION_STRING

    column_list = load_data_to_psql(file_list, data_path, connection_string)
    return column_list


def elt_psql_to_gcs():
    context = get_current_context()
    col_list = context["ti"].xcom_pull(task_ids="postgres_ingestion")
    client = GCSManager(PROJECT_ID)
    client.create_bucket(BUCKET_NAME)
    file_uri = []
    for table_name in col_list:
        olist_data = extract_from_psql(table_name, CONNECTION_STRING)
        uri = client.upload_to_gcs_bucket(
            BUCKET_NAME, blob_name=table_name, data=olist_data
        )
        file_uri.append(uri)
    return file_uri


def elt_gcs_to_bq():
    context = get_current_context()
    uri_list = context["ti"].xcom_pull(task_ids="GCS_upload")
    client = BQManager(PROJECT_ID)
    client.create_dataset(DATASET_ID)
    for file_uri in uri_list:
        table_id = file_uri.split("/")[-1]
        client.create_table(DATASET_ID, table_id)
        client.load_to_bigquery(file_uri, DATASET_ID, table_id)
    logging.info(f"All {len(uri_list)} files loaded to {DATASET_ID}")


if __name__ == "__main__":
    extract_data()
    elt_local_to_psql()
    elt_psql_to_gcs()
    elt_gcs_to_bq()
