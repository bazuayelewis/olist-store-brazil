from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from main import extract_data, elt_local_to_psql, elt_psql_to_gcs, elt_gcs_to_bq
from config import *

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 8, 1),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


# Define the DAG
with DAG(
    "elt-psql-to-bigquery",  # name of DAG in the UI
    default_args=default_args,
    description="A DAG to orchestrate the end-to-end elt process",
    schedule_interval=None,
    catchup=False,
) as dag:

    task_1 = PythonOperator(
        task_id="kaggle_datasets_download", python_callable=extract_data
    )

    task_2 = PythonOperator(
        task_id="postgres_ingestion", python_callable=elt_local_to_psql
    )

    task_3 = PythonOperator(task_id="gcs_upload", python_callable=elt_psql_to_gcs)
    task_4 = PythonOperator(task_id="bigquery_upload", python_callable=elt_gcs_to_bq)

    task_5 = TriggerDagRunOperator(
        task_id="trigger_dbt_dag", trigger_dag_id="dbt_transform_raw"
    )

    task_1 >> task_2 >> task_3 >> task_4 >> task_5
