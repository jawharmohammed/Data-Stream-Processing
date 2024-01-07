from kafka import KafkaProducer, KafkaConsumer
from river import metrics
from time import perf_counter
from Models.models import create_linear_regression_model, create_srp_regression_model, create_snarimax_model
import json
import csv
import threading

# Kafka configurations
PORT = 9092
TARGET_VARIABLE = "Close"
SUFFIX_1 = "_model_training" 
SUFFIX_2 = "_prediction_plot" 
HORIZON = 1
lock = threading.Lock()

# Function to create a Kafka consumer for model training
def create_modeltrainer_consumer(company_name):
    topic_1 = "{}{}".format(company_name, SUFFIX_1)
    consumer_group_1 = "{}{}".format(company_name, SUFFIX_1)
    consumer = KafkaConsumer(topic_1, bootstrap_servers='localhost:{}'.format(PORT), group_id=consumer_group_1)
    return consumer

# Function to create a Kafka producer for storing predictions
def create_corr_producer():
    producer = KafkaProducer(bootstrap_servers='localhost:{}'.format(PORT))
    return producer

# Function to update model and compute metrics for a new data point
def modelling_new_point(model, model_type_name, metrics_dict, stock_market):
    x = stock_market["Date"]
    y = stock_market[TARGET_VARIABLE]

    # Handling missing data and updating the model
    if y:
        if model_type_name == 'linear_regression_model':
            y_pred = model.predict_one(x)
        elif model_type_name == 'snarimax_model':
            y_pred = model.forecast(HORIZON)[0]
        elif model_type_name == 'srp_regression_model':
            y_pred = model.predict_one(x)

        temps = perf_counter()  
        model.learn_one(x, y)
        temps_cpu = perf_counter() - temps
        
        # Updating error metrics
        MAE = metrics_dict['MAE'].update(y, y_pred).get()
        RMSE = metrics_dict['RMSE'].update(y, y_pred).get()
        MAPE = metrics_dict['MAPE'].update(y, y_pred).get()
                
        # Constructing data for prediction result
        predict_result = {}
        #print("Day ",x ,"learned by model .")
        predict_result["date"] = x
        predict_result["y_true"] = y
        predict_result["y_pred"] = y_pred
        predict_result["CPU_time"] = temps_cpu
        predict_result["MAE"] = MAE  
        predict_result["RMSE"] = RMSE  
        predict_result["MAPE"] = MAPE           
        return predict_result

# Function to model consumer behavior: receiving messages and updating the model
def modelling(model, model_type_name, consumer, producer, company_name):
    result_to_store = False
    metrics_dict = {"MAE": metrics.MAE(), "RMSE": metrics.RMSE(), 'MAPE': metrics.MAPE()}
    topic_2 = "{}{}".format(company_name, SUFFIX_2)
    csv_file_name = f"predictions_data_files/{company_name}_predictions.csv"
    
    for message in consumer:
        stock_market = json.loads(message.value.decode())
        if result_to_store: 
            predict_result = modelling_new_point(model, model_type_name, metrics_dict, stock_market)
            #print(predict_result["date"])
            producer.send(topic_2, json.dumps(predict_result).encode())
            with open(csv_file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                if file.tell() == 0:  # Write keys as the first row if the file is empty
                    writer.writerow(predict_result.keys())
                writer.writerow(predict_result.values()) 
        else:
            result_to_store = True
            x = stock_market["Date"]
            y = stock_market[TARGET_VARIABLE]
            if y:
                model.learn_one(x, y)

# Function to handle the model trainer consumer
def modeltrainer_consumer(company_name, model_type_name):
    consumer = create_modeltrainer_consumer(company_name)
    producer = create_corr_producer()
    if model_type_name == 'linear_regression_model':
        model = create_linear_regression_model()
    elif model_type_name == 'snarimax_model':
        model = create_snarimax_model()
    elif model_type_name == 'srp_regression_model':
        model = create_srp_regression_model()
    
    modelling(model, model_type_name, consumer, producer, company_name)

