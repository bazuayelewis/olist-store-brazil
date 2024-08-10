from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from main import etl_main, etl_psql_to_gcs
from airflow.operators.python import task, get_current_context

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 8, 1),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


# Define the DAG
with DAG(
    "elt-psql-to-bigquery",  # name of DAG in the UI
    default_args=default_args,
    description="A DAG to orchestrate the elt process",
    schedule_interval=None,
    catchup=False,
) as dag:

    task_1 = PythonOperator(
        task_id='test',
        python_callable=etl_main
    )
    
    task_2 = PythonOperator(
        task_id='GCS_upload',
        python_callable=etl_psql_to_gcs
    )
 
    task_1 >> task_2
