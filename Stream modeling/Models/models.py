from river import compose
from river import preprocessing
from river import tree
from river import ensemble
from river import linear_model
from river import optim
from river import time_series

# Function to create a linear regression model
def create_linear_regression_model():
    # Function to extract timestamp date as a feature
    def get_timestamp_date(x):
        return {'timestamp_date': x}

    # Constructing a pipeline for linear regression
    model = compose.Pipeline(
        ('timestamp_date', compose.FuncTransformer(get_timestamp_date)),    
        ('scale', preprocessing.StandardScaler()),  # Scaling the features
        ('lin_reg', linear_model.LinearRegression(intercept_lr=0, optimizer=optim.SGD(0.03)))  # Linear regression model
    )

    # Scaling the target variable (regression target)
    model = preprocessing.TargetStandardScaler(regressor=model)
    return model

# Function to create a SNARIMAX time series model
def create_snarimax_model():
    # Function to extract timestamp date as a feature
    def get_timestamp_date(x):
        return {'timestamp_date': x}

    # Constructing a pipeline for SNARIMAX time series modeling
    model = compose.Pipeline(
        ('timestamp_date', compose.FuncTransformer(get_timestamp_date)),    
        ('scale', preprocessing.StandardScaler()),  # Scaling the features
        ('snarimax_reg', time_series.SNARIMAX(p=1, d=1, q=0))  # SNARIMAX model for time series
    )

    return model

# Function to create an ensemble SRPRegressor model
def create_srp_regression_model():
    # Function to extract timestamp date as a feature
    def get_timestamp_date(x):
        return {'timestamp_date': x}
    
    # Base model for the ensemble - Hoeffding Adaptive Tree Regressor
    base_model = tree.HoeffdingAdaptiveTreeRegressor(grace_period=50)

    # Constructing a pipeline for ensemble regression with SRPRegressor
    model = compose.Pipeline(
        ('timestamp_date', compose.FuncTransformer(get_timestamp_date)),    
        ('scale', preprocessing.StandardScaler()),  # Scaling the features
        ('srp_reg', ensemble.SRPRegressor(
            model=base_model,  # Base model for the ensemble
            training_method="patches",  # Training method for the ensemble
            n_models=3,  # Number of models in the ensemble
            seed=42  # Seed for reproducibility
        ))
    )

    # Scaling the target variable (regression target)
    model = preprocessing.TargetStandardScaler(regressor=model)
    return model
