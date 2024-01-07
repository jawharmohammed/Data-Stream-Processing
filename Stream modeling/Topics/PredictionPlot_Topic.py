from kafka.admin import KafkaAdminClient, NewTopic

# Constants for Kafka configuration
PORT = 9092
CLIENT_ID = "Project_DataStream"
NUM_PARTITIONS = 1
REPLICATION_FACTOR = 1

# Suffix for the prediction plot topic
SUFFIX_2 = "_prediction_plot" 

# Function to create a prediction plot topic for a specific company
def create_predictionplot_topic(admin_client, company_name):
    # Generating the topic name based on the company name and suffix
    topic_name_2 = "{}{}".format(company_name, SUFFIX_2)
    
    # Creating a new topic with specified configurations
    new_topic = NewTopic(name=topic_name_2, num_partitions=NUM_PARTITIONS, replication_factor=REPLICATION_FACTOR)
    
    # Creating the topic using the admin client
    admin_client.create_topics([new_topic], validate_only=False)
    return 

# Function to create prediction plot topics for a list of companies
def create_predictionplot_topics(companies_names_list):
    # Creating an admin client for Kafka
    admin_client = KafkaAdminClient(bootstrap_servers="localhost:{}".format(PORT), client_id=CLIENT_ID)
    
    # Iterating through each company to create prediction plot topics
    for company_name in companies_names_list:
        create_predictionplot_topic(admin_client, company_name)

    # Returning True as an indicator of successful topic creation
    return True
