import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
AIRFLOW_CONN_POSTGRES_CONN_ID=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
DATA_DIR = './data'
URL = 'https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce'
DATA_PATH = './data/brazilian-ecommerce'
CONNECTION_STRING=f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
GOOGLE_AUTH_CRED=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
BUCKET_NAME='olist_store_brazil'