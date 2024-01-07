import time
from kafka import KafkaProducer
import json
import pandas as pd

# Constants for Kafka configuration
PORT = 9092
TIME_TO_SLEEP_BETWEEN_MESSAGES = 1
REFERENCE_DATE = '2018-01-01'
SUFFIX_1 = "_model_training" 

# Function to create a Kafka producer
def create_datastream_producer():
    producer = KafkaProducer(bootstrap_servers='localhost:{}'.format(PORT))
    return producer

# Function to push data to a specific Kafka topic
def pushing_data(producer, topic_1, data):
    for index, row in data.iterrows():
        row_dict = row.to_dict()
        producer.send(topic_1, json.dumps(row_dict).encode())
        time.sleep(TIME_TO_SLEEP_BETWEEN_MESSAGES)

# Function to handle data streaming for a specific company
def datastream_producer(company_name):
    datastream_producer = create_datastream_producer()
    topic_1 = "{}{}".format(company_name, SUFFIX_1)
    data_filename = "data_files/{}_1d.pkl".format(company_name)

    # Reading data from file and preparing it for streaming
    with open(data_filename, mode='rb') as file:
        data = pd.read_pickle(file)
        data.reset_index(inplace=True)
        reference_date = pd.to_datetime(REFERENCE_DATE)
        data['Date'] = (data['Date'] - reference_date).dt.days
    
    # Pushing data to the specified Kafka topic
    pushing_data(datastream_producer, topic_1, data)

