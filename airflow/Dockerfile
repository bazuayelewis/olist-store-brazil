# Base image
FROM apache/airflow:2.9.3-python3.10

ENV AIRFLOW_HOME=/opt/airflow
WORKDIR $AIRFLOW_HOME

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file into the container and package dependencies
COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.10.txt"



