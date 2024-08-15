from google.cloud import storage
import logging


class GCSManager:
    def __init__(self, project_id: str) -> None:
        self.project_id = project_id
        self.client = self._start_gcs_client()

    def _start_gcs_client(self):
        return storage.Client(self.project_id)

    def create_bucket(
        self,
        bucket_name: str,
        storage_class: str = "STANDARD",
        location: str = "europe-west1",
    ) -> None:
        """
        This function creates a bucket in GCS with a default storage class and location.
        It checks if the bucket already exists and if not creates a new bucket
        """
        try:
            self.client.get_bucket(bucket_name)
            logging.info(f"Bucket {bucket_name} already exists!")
        except:
            bucket = self.client.bucket(bucket_name)
            bucket.storage_class = storage_class
            bucket.location = location
            bucket.create()
            logging.info(f"{bucket_name} created successfully!")

    def upload_to_gcs_bucket(
        self,
        bucket_name: str,
        blob_name: str,
        data,
        content_type="text/csv",
    ) -> str:
        """
        This function uploads data into GCS bucket and returns a gsutil URI
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        csv_string = data.to_csv(index=False)
        blob.upload_from_string(csv_string, content_type)
        logging.info(f"Successfully uploaded {blob_name} to GCS")
        return f"gs://{bucket_name}/{blob_name}"
