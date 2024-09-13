from kaggle.api.kaggle_api_extended import KaggleApi
import logging
import os


def kaggle_downloader(
    kaggle_username: str, kaggle_key: str, kaggle_url: str, data_dir: str
) -> list:
    """
    This function interacts and authtenticate user with kaggleAPI and downloads datasets
    Returns list of names of datasets downloaded

    """
    if kaggle_username and kaggle_key:
        client = KaggleApi()
        client.authenticate()
        client.dataset_download_files(
            kaggle_url, data_dir, force=True, quiet=True, unzip=True
        )
        file_names = os.listdir(f"{data_dir}")
        logging.info(f"{len(file_names)} Datasets downloaded successfully from kaggle")
        return file_names
    else:
        raise ValueError("Kaggle credentials not found in environment variables.")
