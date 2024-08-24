from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Define a simple function that prints the current date
def print_date():
    from datetime import datetime
    print(f"Current date and time: {datetime.now()}")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'example_dag',
    default_args=default_args,
    description='A simple test DAG',
    schedule_interval=timedelta(days=1),
)

# Define a task using the PythonOperator
print_date_task = PythonOperator(
    task_id='print_date_task',
    python_callable=print_date,
    dag=dag,
)

# Set the task in the DAG
print_date_task
