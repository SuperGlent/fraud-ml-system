from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
import sys
import os

#add path for import 
sys.path.append('/opt/airflow')
from training.db.load_data import main_load_data

#creating DAG
with DAG(
    dag_id="fraud-system-pipeline",
    start_date=datetime(2026, 4, 1),
    schedule_interval="@once",
    catchup=False
    
) as dag:
    
    #load data to database task
    load_data = PythonOperator(
        task_id="load_data",
        python_callable=main_load_data
        
    )
    
    #training moel with mlflow in isolated container
    train_model = DockerOperator(
        task_id="train_model",
        image="fraud-ml-system-training",
        command="python train.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="fraud-ml-system_default", #has to be docker-compose network, because of service on default bridge will have no access to the network
        mount_tmp_dir=False,
        environment={"DB_USERNAME": os.environ.get("DB_USERNAME"), "DB_PASSWORD": os.environ.get("DB_PASSWORD")}
    )

    #task sequence
    load_data  >> train_model


