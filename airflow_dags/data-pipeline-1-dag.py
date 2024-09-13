from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import subprocess

def read_kafka():
    # Path to your producer.py script
    path_to_script = '/consumer.py'
    
    # Command to execute the Python script
    command = ['python', path_to_script]
    
    # Execute the command
    response = subprocess.run(command, capture_output=True, text=True)
    
    # Log output and errors
    print("Output:", response.stdout)
    if response.returncode != 0:
        print("Errors:", response.stderr)
        raise Exception("Failed to run producer.py")
    else:
        print("producer.py ran successfully")

def clean_data():
    # Path to your producer.py script
    path_to_script = '/clean-data.py'
    
    # Command to execute the Python script
    command = ['python', path_to_script]
    
    # Execute the command
    response = subprocess.run(command, capture_output=True, text=True)

    # Log output and errors
    print("Output:", response.stdout)
    if response.returncode != 0:
        print("Errors:", response.stderr)
        raise Exception("Failed to run producer.py")
    else:
        print("producer.py ran successfully")

def load_postgres():
    # Path to your producer.py script
    path_to_script = '/producer.py'
    
    # Command to execute the Python script
    command = ['python', path_to_script]
    
    # Execute the command
    response = subprocess.run(command, capture_output=True, text=True)
    
    # Log output and errors
    print("Output:", response.stdout)
    if response.returncode != 0:
        print("Errors:", response.stderr)
        raise Exception("Failed to run producer.py")
    else:
        print("producer.py ran successfully")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 25),
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_cleaning_dag',
    default_args=default_args,
    description='A DAG for data cleaning operations',
    schedule_interval='@daily',  # Run once a day
)

task1 = PythonOperator(
    task_id='Data_Reading_Kafka',
    python_callable=read_kafka,
    dag=dag,
)

task2 = PythonOperator(
    task_id='Data_cleaning_Spark',
    python_callable=clean_data,
    dag=dag,
)

task3 = PythonOperator(
    task_id='Data_Loading_Spark',
    python_callable=clean_data,
    dag=dag,
)