import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from kafka import KafkaConsumer
import pandas as pd
import json
import threading

# Initialize Dash app
app = dash.Dash(__name__)
COLUMNS=['date', 'y_true','y_pred','MAPE']
REFERENCE_DATE = '2018-01-01'

historical_data = {
    'Google_prediction_plot': pd.DataFrame(columns=COLUMNS),
    'BNPParibas_prediction_plot': pd.DataFrame(columns=COLUMNS),
    'Alibaba_prediction_plot': pd.DataFrame(columns=COLUMNS),
    'Rosneft_prediction_plot': pd.DataFrame(columns=COLUMNS),
    'SHELL_prediction_plot': pd.DataFrame(columns=COLUMNS)
}

# Function to generate plot based on data
def generate_plots(data, producer_name):
    company_names = {
        'Google_prediction_plot': 'Google',
        'BNPParibas_prediction_plot': 'BNP Paribas',
        'Alibaba_prediction_plot': 'Alibaba',
        'Rosneft_prediction_plot': 'Rosneft',
        'SHELL_prediction_plot': 'SHELL'
    }

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=data["date"], y=data["y_true"], mode='lines', name="y_true", line=dict(color='blue')))
    fig1.add_trace(go.Scatter(x=data["date"], y=data["y_pred"], mode='lines', name='y_pred', line=dict(color='red')))
    fig1.update_layout(
        title=company_names.get(producer_name, producer_name),  # Use company name if available, else use topic name
        width=1500, 
        height=600,
        xaxis_title='Date',
        yaxis_title='Y True / Y Pred'
    )

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data["date"], y=data["MAPE"], mode='lines', name="MAPE", line=dict(color='green')))
    fig2.update_layout(
        title=f"{company_names.get(producer_name, producer_name)} - Mean Absolute Percentage Error (MAPE)",
        width=1500, 
        height=600,
        xaxis_title='Date',
        yaxis_title='MAPE (%)'
    )

    return fig1,fig2

# Update the threads to store fetched data in 'historical_data' variable
def update_plot_for_topic(topic, plot_id_y, plot_id_mape):
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092')

    def update_plot():
        for i,message in enumerate(consumer):
            data = json.loads(message.value.decode())
            if (i<10 and data["date"]<5) or i>=10:
                new_point_df = pd.DataFrame(columns=COLUMNS)
                reference_date = pd.to_datetime(REFERENCE_DATE)
                point_date = reference_date + pd.to_timedelta(data["date"], unit='D')
                new_point_df.loc[0] = [point_date, data["y_true"], data["y_pred"],data["MAPE"]]
                historical_data[topic] = pd.concat([historical_data[topic], new_point_df])

                # Generate both types of plots
                plot_y, plot_mape = generate_plots(historical_data[topic], topic)
                # Update the Dash app with the new figures
                app.callback(Output(plot_id_y, 'figure'))(lambda x: plot_y)
                app.callback(Output(plot_id_mape, 'figure'))(lambda x: plot_mape)

    thread = threading.Thread(target=update_plot)
    thread.daemon = True
    thread.start()

# Dash app layout - Define multiple graph elements for each plot
app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=10000,
        n_intervals=0
    ),
    html.Div(id='trigger-update', style={'display': 'none'}),
    html.Div([
        dcc.Graph(id='Google_y_plots'),  # Update IDs to reflect company names
        dcc.Graph(id='Google_mape_plot')
    ]),
    html.Div([
        dcc.Graph(id='BNPParibas_y_plots'),
        dcc.Graph(id='BNPParibas_mape_plot')
    ]),
    html.Div([
        dcc.Graph(id='Alibaba_y_plots'),
        dcc.Graph(id='Alibaba_mape_plot')
    ]),
    html.Div([
        dcc.Graph(id='Rosneft_y_plots'),
        dcc.Graph(id='Rosneft_mape_plot')
    ]),
    html.Div([
        dcc.Graph(id='SHELL_y_plots'),
        dcc.Graph(id='SHELL_mape_plot')
    ])
])

# Create threads for each Kafka topic and associated plot
for topic, plot_y_id, plot_mape_id in [
    ("Google_prediction_plot", 'Google_y_plots', 'Google_mape_plot'),
    ("BNPParibas_prediction_plot", 'BNPParibas_y_plots', 'BNPParibas_mape_plot'),
    ("Alibaba_prediction_plot", 'Alibaba_y_plots', 'Alibaba_mape_plot'),
    ("Rosneft_prediction_plot", 'Rosneft_y_plots', 'Rosneft_mape_plot'),
    ("SHELL_prediction_plot", 'SHELL_y_plots', 'SHELL_mape_plot')
]:
    update_plot_for_topic(topic, plot_y_id, plot_mape_id)  # Use the topic name for the plot ID

# Callback to update all figures when interval changes
@app.callback(
    Output('Google_y_plots', 'figure'),
    Output('Google_mape_plot', 'figure'),
    Output('BNPParibas_y_plots', 'figure'),
    Output('BNPParibas_mape_plot', 'figure'),
    Output('Alibaba_y_plots', 'figure'),
    Output('Alibaba_mape_plot', 'figure'),
    Output('Rosneft_y_plots', 'figure'),
    Output('Rosneft_mape_plot', 'figure'),
    Output('SHELL_y_plots', 'figure'),
    Output('SHELL_mape_plot', 'figure'),
    Input('interval-component', 'n_intervals'), # Update when interval changes
    Input('trigger-update', 'children')
)
def update_all_plots(n,_):
    all_figures = []
    for topic in ["Google_prediction_plot", "BNPParibas_prediction_plot", "Alibaba_prediction_plot", "Rosneft_prediction_plot", "SHELL_prediction_plot"]:
        y_plots, mape_plot = generate_plots(historical_data[topic], topic)
        all_figures.extend([y_plots, mape_plot])
    return tuple(all_figures)

# Run the Dash app
def start_predictionplotter_consumers():
    app.run_server(debug=True)


start_predictionplotter_consumers()