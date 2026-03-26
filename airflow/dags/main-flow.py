from airflow.sdk import DAG
from datetime import datetime
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.python.operators.python import PythonOperator
from airflow.providers.bash.poerators.bash import BashOperator
import sys
import os

sys.path.append('/opt/airflow')
from training.db.load_data import main_load_data

with DAG(
    dag_id="fraud-system-pipeline",
    start_date=datetime(2026, 3, 7),
    schedule_interval=False,
    catchup=False
    
) as dag:
    
    load_data = PythonOperator(
        task_id="load_data",
        python_callable=main_load_data
        
    )
    
    
    train_model = DockerOperator(
        task_id="train_model",
        image="fraud-ml-system_training",
        command="python ../training/train.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )


    make_migrations = BashOperator(
        task_id="migrate",
        bash_command="alembic revision --autogenerate"
    )

    load_data  >> train_model


