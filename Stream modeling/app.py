from Initialization import create_topics, create_threads, start_threads
import signal
import threading
import time
import sys

# List of company names
COMPANIES_NAMES_LIST = ["Google", "BNPParibas", "Alibaba", "Rosneft", "SHELL"]

# List of model types
MODEL_TYPE_NAMES = ['linear_regression_model', 'snarimax_model', 'srp_regression_model']

def main(companies_names_list, model_type_name):
    #Creating topics for companies
    topics_creation_status = create_topics(companies_names_list)
    
    if topics_creation_status:
        print("Topics created successfully")
    else:
        print("Topics creation failed")

    # Creating threads for data streaming and model training
    datastream_producers_threads, modeltrainer_consumer_threads = create_threads(companies_names_list, model_type_name)
    
    # Starting threads
    start_threads(datastream_producers_threads, modeltrainer_consumer_threads)
    
def select_model(model_list):
    # Displaying available models and asking for user input
    print("Select a model:")
    for i, model in enumerate(model_list, start=1):
        print(f"{i}. {model}")

    while True:
        try:
            choice = int(input("Enter the number of the model: "))
            if 1 <= choice <= len(model_list):
                return model_list[choice - 1]
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")

# Selecting a model from the available list
selected_model = select_model(MODEL_TYPE_NAMES)
print(f"The name of the selected model is: {selected_model}")

def signal_handler(sig, frame):
    print("\nCtrl+C detected. Terminating threads...")
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Executing the main function with selected parameters
main(COMPANIES_NAMES_LIST, selected_model)

