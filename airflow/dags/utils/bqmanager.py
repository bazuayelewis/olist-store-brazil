import logging
from google.cloud import bigquery
from google.cloud.exceptions import Conflict


class BQManager:
    def __init__(self, project_id: str) -> None:
        self.project_id = project_id
        self.client = self._start_bq_client()

    def _start_bq_client(self):
        return bigquery.Client(self.project_id)

    def create_dataset(self, dataset_id: str) -> None:
        """
        This function creates a dataset and handles conflict errors
        """
        try:
            dataset_ref = self.client.dataset(dataset_id)
            self.client.create_dataset(dataset_ref)
            logging.info(f"Dataset {dataset_id} created successfully!")
        except Conflict:
            logging.info("Dataset already exists!!! Exiting as successful")
        except Exception as e:
            logging.error(f"Encountered issue creating the Dataset {dataset_id}: {e}")
            raise e

    def create_table(self, dataset_id: str, table_id: str) -> None:
        """
        This function creates a table and handles confilct errors
        """
        try:
            table_ref = self.client.dataset(dataset_id).table(table_id)
            table = bigquery.Table(table_ref)
            self.client.create_table(table)
            logging.info(f"Table {table_id} successfully created")
        except Conflict:
            logging.info("Table already exists!! Exiting as successful")
        except Exception as e:
            logging.error(f"Encountered issue creating the table {table_id}: {e}")
            raise e

    def load_to_bigquery(self, file_uri: str, dataset_id: str, table_id: str) -> None:
        """
        This function loads data from a gcs bucket using the file uri into bigquery
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        try:
            job_config = bigquery.LoadJobConfig(
                autodetect=True,
                create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            )
            load_job = self.client.load_table_from_uri(
                file_uri, table_ref, job_config=job_config
            )
            load_job.result()
            logging.info(f"Successfully loaded {file_uri} to {dataset_id} dataset")
        except Exception as e:
            logging.error(f"Error {e} occurred while uploading to bigquery")
            raise e
