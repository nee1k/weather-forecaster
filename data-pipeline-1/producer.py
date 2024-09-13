import csv
from confluent_kafka import Producer
import json

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})

# Path to your CSV file
csv_file_path = '/home/exouser/data/weather_data.csv'

# Function to delivery report callback from Kafka
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Function to publish messages to Kafka
def publish_message(producer_instance, topic_name, key, value):
    try:
        # Convert value to JSON string
        value_str = json.dumps(value)
        producer_instance.produce(topic_name, key=key, value=value_str.encode('utf-8'), callback=delivery_report)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))

# Read CSV and publish each row to Kafka
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data = {
            "Timestamp": row['utc_timestamp'],
            "Temperature": row['AT_temperature'],
            "Direct Horizontal Radiation": row['AT_radiation_direct_horizontal'],
            "Diffuse Horizontal Radiation": row['AT_radiation_diffuse_horizontal']
        }
        publish_message(producer, 'austria_test_data', 'csvdata', data)

# Close the producer
producer.flush()  # Wait for all messages to be delivered
producer.close()