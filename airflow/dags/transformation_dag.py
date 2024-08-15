from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator


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
    "dbt_transform_raw",  # name of DAG in the UI
    default_args=default_args,
    description="A DAG to orchestrate the transformation process with dbt",
    schedule_interval=None,
    catchup=False,
) as dag:

    task_1 = BashOperator(
        task_id="dbt_transforms",
        bash_command="cd /opt/airflow/dbt && ls -a && dbt build --profiles-dir .",
    )

    task_1
