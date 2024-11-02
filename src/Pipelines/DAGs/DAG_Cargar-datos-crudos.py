from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from functions.registrar_archivo import registrar_archivos_procesados
from functions.desanidar_misc import desanidar_misc 

#######################################################################################
# PARÁMETROS
#######################################################################################

nameDAG_base      = 'Procesamiento_ETL_Google'
project_id        = 'neon-gist-439401-k8'
dataset           = '1'
owner             = 'Mauricio Arce'
GBQ_CONNECTION_ID = 'bigquery_default'
bucket_name       = 'datos-crudos'

default_args = {
    'owner': owner,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

#######################################################################################
# DEFINICIÓN DEL DAG
#######################################################################################

with DAG(
    dag_id=nameDAG_base,
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    inicio = DummyOperator(task_id='inicio')

    registrar_archivos = PythonOperator(
        task_id='registrar_archivos_procesados',
        python_callable=registrar_archivos_procesados,
        op_kwargs={
            'bucket_name': bucket_name,
            'prefix': 'g_sitios/',
            'project_id': project_id,
            'dataset': dataset
        }
    )

    desanidar_columna = PythonOperator(
        task_id='desanidar_misc',
        python_callable=desanidar_misc,
        op_kwargs={
            'project_id': project_id,
            'dataset': dataset
        }
    )

    fin = DummyOperator(task_id='fin')

    # Estructura del flujo de tareas
    inicio >> registrar_archivos >> desanidar_columna >> fin
