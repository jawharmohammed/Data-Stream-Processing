# Data-Stream-Processing

## Overview

This project focuses on stock market forecasting for five prominent companies from different countries: Alibaba (China), BNP Paribas (France), Google (United States), Rosneft (Russia), and Shell (Netherlands/United Kingdom). The forecasting is conducted using two distinct approaches:

### Stream Modeling

Using Kafka for messaging and training some online models from the river ML library: **Linear Regression**, **SNARIMAX**, and **SRP Regressor (base model: Hoeffding Adaptive Tree Regressor)**.

#### Kafka Architecture

![Kafka Architecture](https://github.com/jawharmohammed/Data-Stream-Processing/assets/72218345/d81078a4-ad54-45f9-833f-d7e7d6e986b8)

### Batch Learning

Using Time Series processing and analysis techniques leveraging three main models: **LSTM**, **ARIMA**, and **PROPHET**.

## Project Structure

### Batch Modeling

- Data files
- Batch_modeling.ipynb: Jupyter notebook for batch modeling, containing code and documentation.

### Stream Modeling

- Consumers
  - ModelTrainer_Consumer.py: Python script responsible for consuming data, training financial models, and producing to the next topic.
  - PredictionPlotter_Consumer.py: Python script responsible for consuming prediction data and generating plots.
- Images: Folder containing images related to different models used in stream modeling for all companies.
- Models
  - models.py: Python script containing river streaming models for forecasting.
- Producer
  - DataStream_Producer: Python script containing the data stream producer.
- Topics: Folder containing scripts related to the creation of the Kafka topics.
- data_files: Folder containing data files used in stream modeling.
- predictions_data_files: Folder to store prediction values and metrics after running the code.

## Usage

1. Clone this repository.

### Batch Modeling

- Open and run the Batch_modeling.ipynb notebook for batch modeling.

### Stream Modeling

1. Run Zookeeper on a terminal:
    ```bash
    bin/zookeeper-server-start.sh config/zookeeper.properties
    ```

2. Run Kafka on a terminal:
    ```bash
    bin/kafka-server-start.sh config/server.properties
    ```

3. Run the dashboard on a separate terminal (directory of file to run: "./Consumers"):
    ```bash
    python3 PredictionPlotter_Consumer.py
    ```

4. Run the application on a separate terminal (on the base directory):
    ```bash
    python3 app.py
    ```

5. When you run the application, you can choose which streaming model you want to use.

### Contributors: 
* Mohammed JAWHAR
* Mohamad EL OSMAN
