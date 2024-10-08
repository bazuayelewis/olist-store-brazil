import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
DATA_DIR = "./data"
OWNER = "olistbr"
DATASET = "brazilian-ecommerce"
KAGGLE_KEY = os.getenv("KAGGLE_KEY")
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_URL = f"{OWNER}/{DATASET}"
DATA_PATH = f"{DATA_DIR}/{DATASET}"
CONNECTION_STRING = os.getenv("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN")
GOOGLE_AUTH_CRED = os.getenv("AIRFLOW_GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("PROJECT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME", "olist_store_brazil")
DATASET_ID = os.getenv("DATASET_ID", "olist_store_brazil_raw")
LOCATION = os.getenv("LOCATION", "europe-west1")
