#using official image
FROM apache/airflow:2.10.2-python3.12

#
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#get back to airflow user
USER airflow

#constraint files to build dependencies correctlly
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.12.txt"

#copy requirements
COPY requirements.txt /requirements.txt
COPY --chown=airflow:0 . /opt/airflow

#installing requirements
RUN pip install --no-cache-dir -r /requirements.txt --constraint "${CONSTRAINT_URL}"

#Path to files
ENV PYTHONPATH="/opt/airflow"

#point workdir
WORKDIR /opt/airflow
