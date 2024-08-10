from sandbox import load_data_to_postgresql, postgres_to_gcs
from config import *
from airflow.operators.python import get_current_context

def etl_main():
    data_path = DATA_PATH
    connection_string = CONNECTION_STRING
    
    column_list = load_data_to_postgresql(data_path, connection_string)
    return column_list

def etl_psql_to_gcs():
    context = get_current_context()
    col_list = context['ti'].xcom_pull(task_ids='test')
    connection_id = AIRFLOW_CONN_POSTGRES_CONN_ID
    bucket_name = BUCKET_NAME
    postgres_to_gcs(col_list, connection_id, bucket_name)

if __name__ == '__main__':
    etl_main()
    etl_psql_to_gcs()
    
    