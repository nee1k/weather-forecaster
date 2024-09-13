# WeatherFlowAnalytics

## Resource creation:
 Execute below docker commands under each resource directory to up the resources.
 Kafka creation: docker-compose up -d
 Airflow creation: docker-compose up -d
 Spark creation: docker-compose up -d
  Postgres creation: docker-compose up -d

## Execution of Data Pipelines:
 Created and placed airflow dag under /dags folder of airflow.
 Triggering airflow dags. 
1.	Data_Extraction_Kafka_to_Postgres
2.	Sarima_Model_Training

Querying postgres db for visualization.
