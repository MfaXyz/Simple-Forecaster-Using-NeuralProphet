# Import Libraries
import pandas as pd
from neuralprophet import NeuralProphet
from neuralprophet import set_random_seed
import warnings
import plotly.graph_objs as go
warnings.filterwarnings("ignore")


def make_future(filename, freq, periods):
    # Import CSV File & Create Data Frame Based On EveryDay
    df_day = pd.read_csv(filename)
    df_day['ds'] = pd.to_datetime(df_day['ds'])
    df_day = df_day.dropna()

    # Use NeuralProphet For Training
    m = NeuralProphet(epochs=256)
    metrics = m.fit(df_day, freq=freq)

    # Forecast into the unknown future
    future = m.make_future_dataframe(df_day, periods=periods, n_historic_predictions=True)
    forecast = m.predict(future)

    # Plot Forecast
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat1'],
                             mode='lines',
                             name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['y'],
                             mode='markers',
                             name='Actual',
                             marker=dict(
                                 color='black',
                                 size=4)))
    forecast.drop('residual1', axis=1, inplace=True)
    forecast.drop('trend', axis=1, inplace=True)
    if 'season_yearly' in forecast:
        forecast.drop('season_yearly', axis=1, inplace=True)
    if 'season_weekly' in forecast:
        forecast.drop('season_weekly', axis=1, inplace=True)
    forecast.to_csv('forecast.csv', index=False)
    fig.write_html("Output.html")
