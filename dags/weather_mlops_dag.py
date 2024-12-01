from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys
import os

# Ensure the project root is in Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_data_collection():
    """
    Execute data collection script
    """
    result = subprocess.run([sys.executable, '/mnt/c/Users/shahz/MLOPS/classtask7/WeatherPrediction/WeatherPredictonModel/collect_data.py'], 
                             capture_output=True, 
                             text=True, 
                             cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.returncode != 0:
        raise Exception(f"Data collection failed: {result.stderr}")
    print(result.stdout)

def run_data_preprocessing():
    """
    Execute data preprocessing script
    """
    result = subprocess.run([sys.executable, '/mnt/c/Users/shahz/MLOPS/classtask7/WeatherPrediction/WeatherPredictonModel/preprocess_data.py'], 
                             capture_output=True, 
                             text=True, 
                             cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.returncode != 0:
        raise Exception(f"Data preprocessing failed: {result.stderr}")
    print(result.stdout)

def run_model_training():
    """
    Execute model training script
    """
    result = subprocess.run([sys.executable, '/mnt/c/Users/shahz/MLOPS/classtask7/WeatherPrediction/WeatherPredictonModel/train_model.py'], 
                             capture_output=True, 
                             text=True, 
                             cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.returncode != 0:
        raise Exception(f"Model training failed: {result.stderr}")
    print(result.stdout)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_mlops_pipeline',
    default_args=default_args,
    description='Weather Data MLOps Pipeline',
    schedule_interval=timedelta(days=1),  # Run daily
    catchup=False
) as dag:

    data_collection_task = PythonOperator(
        task_id='data_collection',
        python_callable=run_data_collection,
        dag=dag,
    )

    data_preprocessing_task = PythonOperator(
        task_id='data_preprocessing',
        python_callable=run_data_preprocessing,
        dag=dag,
    )

    model_training_task = PythonOperator(
        task_id='model_training',
        python_callable=run_model_training,
        dag=dag,
    )

    # Set task dependencies
    data_collection_task >> data_preprocessing_task >> model_training_task