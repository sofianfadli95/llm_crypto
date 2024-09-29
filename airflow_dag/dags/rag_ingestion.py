from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import json

default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'vector_database_ingestion_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

# Adjusted for Docker: Accessing data in the mounted folder
def extract_data(**kwargs):
    data_source = "/opt/airflow/data"  # Path inside the container
    list_json = []
    for file_name in os.listdir(data_source):
        print(os.path.join(data_source, file_name))
        with open(os.path.join(data_source, file_name), 'r') as file:
            list_json.append(json.load(file))
    return list_json

def setup_elasticsearch(list_json, **kwargs):
    ELASTIC_URL = "http://localhost:9200"
    INDEX_NAME="crypto-questions"
    print("Setting up Elasticsearch...")
    es_client = Elasticsearch(ELASTIC_URL)

    index_settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "answer": {"type": "text"},
                "question": {"type": "text"},
                "id": {"type": "keyword"},
                "question_answer_vector": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        },
    }

    es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    es_client.indices.create(index=INDEX_NAME, body=index_settings)
    print(f"Elasticsearch index '{INDEX_NAME}' created")
    return es_client, list_json

# Pinecone ingestion using API key from environment
def index_documents(es_client, list_json, **kwargs):
    MODEL_NAME = 'multi-qa-MiniLM-L6-cos-v1'
    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    INDEX_NAME="crypto-questions"
    print("Indexing documents...")
    for json_element in list_json:
        for doc in json_element:
            question = doc["question"]
            answer = doc["answer"]
            doc["question_answer_vector"] = model.encode(question + " " + answer).tolist()
            es_client.index(index=INDEX_NAME, document=doc)
        print(f"Indexed {len(list_json)} documents")
    return "Ingestion successful"

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    provide_context=True,
    dag=dag
)

setup_elasticsearch_task = PythonOperator(
    task_id='setup_elasticsearch',
    python_callable=setup_elasticsearch,
    op_args=['{{ ti.xcom_pull(task_ids="extract_task") }}'],
    provide_context=True,
    dag=dag
)

index_documents_task = PythonOperator(
    task_id='index_documents',
    python_callable=index_documents,
    op_args=['{{ ti.xcom_pull(task_ids="setup_elasticsearch_task") }}'],
    provide_context=True,
    dag=dag
)

extract_task >> setup_elasticsearch_task >> index_documents_task
