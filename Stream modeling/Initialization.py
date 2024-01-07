from Topics.ModelTraining_Topic import create_modeltraining_topics
from Topics.PredictionPlot_Topic import create_predictionplot_topics
from Producer.DataStream_Producer import datastream_producer
from Consumers.ModelTrainer_Consumer import modeltrainer_consumer
import threading

PORT = 9092

def create_topics(companies_names_list):
    # Creating topics for model training and prediction plots
    modeltraining_topics_creation_status = create_modeltraining_topics(companies_names_list)
    #print(modeltraining_topics_creation_status)
    predictionplot_topics_creation_status = create_predictionplot_topics(companies_names_list)
    #print(predictionplot_topics_creation_status)
    
    # Returning True if both topics are created successfully
    if modeltraining_topics_creation_status and predictionplot_topics_creation_status:
        return True
    return False

def create_threads(companies_names_list, model_type_name):
    datastream_producers_threads = []
    modeltrainer_consumer_threads = []
    
    # Creating threads for data streaming and model training for each company
    for company_name in companies_names_list:
        datastream_producers_thread = threading.Thread(target=datastream_producer, args=(company_name,))
        modeltrainer_consumer_thread = threading.Thread(target=modeltrainer_consumer, args=(company_name, model_type_name))
        datastream_producers_threads.append(datastream_producers_thread)
        modeltrainer_consumer_threads.append(modeltrainer_consumer_thread)
    
    print("Threads created successfully")
    return datastream_producers_threads, modeltrainer_consumer_threads

def start_threads(datastream_producers_threads, modeltrainer_consumer_threads):
    # Starting the consumer threads (model training)
    for consumer_thread in modeltrainer_consumer_threads:
        consumer_thread.start()

    # Starting the producer threads (data streaming)
    for producer_thread in datastream_producers_threads:
        producer_thread.start()
