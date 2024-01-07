# Data-Stream-Processing

## Overview:

This project focuses on stock market forecasting for five prominent companies from different countries: Alibaba (China), BNP Paribas (France), Google (United States), Rosneft (Russia), and Shell (Netherlands/United Kingdom). The forecasting is conducted using two distinct approaches :
* Stream modleing : Using Kafka for messaging , and training some online models from river ML library : **Linear Regression**, **SNARIMAX** and **SRP Regressor (base model: Hoeffding Adaptive Tree Regressor)**.
  Kafka Architecture is organized as follows:
  ![image](https://github.com/jawharmohammed/Data-Stream-Processing/assets/72218345/d81078a4-ad54-45f9-833f-d7e7d6e986b8)
  
* Batch learning : Using Time Series processing and analysis techniques leveraging three main models : **LSTM**, **ARIMA** and **PROPHET**.

## Project STructure:

* Batch modeling :
  * Data files
  * Batch_modeling.ipynb : Jupyter notebook for batch modeling, containing code and documentation.
* Stream modeling :
  * Consumers:
    * ModelTrainer_Consumer.py : Python script responsible for consuming data and training financial models.
    * PredictionPlotter_Consumer.py : Python script responsible for consuming prediction data and generating plots.
  
