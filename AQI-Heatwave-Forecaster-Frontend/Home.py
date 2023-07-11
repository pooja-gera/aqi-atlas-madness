# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import requests
from PIL import Image
import json
import codecs
from pandas import json_normalize
import numpy as np
from streamlit_card import card
from datetime import date
import utils
import prophet
from prophet.serialize import model_from_json
import warnings
warnings.filterwarnings("ignore")


def print_top3(df):
    col_list = list(st.columns(3, gap="medium"))
    for i in range(len(col_list)):
        with col_list[i]:
            st.metric(pd.to_datetime(df['Date'].iloc[i]).strftime(
                '%B'), round(df['Predictions'].iloc[i], 2))


def get_statistics(df, feature):
    sorted_desc = df.sort_values('Predictions', ascending=False)
    st.header("Top 3 Months with highest {}".format(feature))
    print_top3(sorted_desc)
    sorted_asc = df.sort_values('Predictions', ascending=True)
    st.header("Top 3 Months with lowest {}".format(feature))
    print_top3(sorted_asc)


def display_model_details(city, forecast, feature):
    if feature == 'AQI':
        f = open(
            './descriptions/aqi/{}.json'.format(city))
        model_details = json.load(f)
        with fs.open('aqi/{}/{}_test.csv'.format(city, city)) as f:
            df_test = pd.read_csv(f, header=0)

    else:
        f = open(
            './descriptions/weather/{}.json'.format(city))
        model_details = json.load(f)
        with fs.open('weather/{}/{}_test.csv'.format(city, city)) as f:
            df_test = pd.read_csv(f, header=0)
    st.markdown("<hr>",
                unsafe_allow_html=True)
    st.header("MODEL USED")
    st.text("")
    st.subheader(model_details["model"]+" Time Series Model")
    st.text("")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.table(df_test)
    with col2:
        st.subheader('Evaluation Metrics')
        st.markdown("<hr>",
                    unsafe_allow_html=True)
        st.text("")
        col1, col2, col3 = st.columns(3, gap="large")
        actual = np.array(df_test['y_test'].tolist())
        predicted = np.array(df_test['y_pred'].tolist())
        error = actual-predicted
        # calculate RMSE
        rmse = np.sqrt(np.mean(error**2))

        # calculate MAE
        mae = np.mean(np.abs(error))

        # calculate MAPE
        mape = np.mean(np.abs(error / actual)) * 100
        with col1:
            st.metric('RMSE', round(rmse, 2), 0)
            st.metric('MAE', round(mae, 2), 0)
        with col2:
            st.metric('MAPE', round(mape, 2), 0)
            st.metric('Accuracy %', round(100-mape, 2), 0)
    st.header("MODEL EVALUATION INFERENCE")
    container1 = st.container()
    with container1:
        st.text("")
        st.write(model_details['evalutation_description'])
        st.text("")
    st.header("MODEL USAGE REASONING")
    container2 = st.container()
    with container2:
        st.text("")
        st.write(model_details['model_usage_reasoning'])
        st.text("")
    st.header("Predicted Vs Actual Values For Test set")
    fig = utils.linegraph(df_test['Date'], df_test['y_test'],
                          'Actual AQI', 'Date', 'AQI', df_test['y_pred'], 'AQI Predicted')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Inference", expanded=True):
        st.write("""
            The chart above shows the plot of the actual and the predicted values of testing data.The red line displays the predicted values and the blue lines represent the actual value of the feature. We have taken the last 20%  of the data for testing data.
        """)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("Forecasted Values")
    fig = utils.linegraph(forecast['Date'], forecast['Predictions'],
                          'AQI Forecasted', 'Date', 'AQI')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Inference", expanded=True):
        st.write("""
            The chart above shows the plot of the forecasted values for the months of 2023. These values are predicted using the trained models mentioned above.
        """)


def combined_linegraph(df, feature):
    with st.container():
        st.markdown("""---""")
        st.header("History Data and Forecasted Values")
        data = go.Scatter(
            x=df["Date"],
            y=df[feature],
            mode='lines',
            line={"color": "blue"},
            name="Historical Data"
        )

        pred = go.Scatter(
            x=df["Date"],
            y=df["Predictions"],
            mode='lines',

            line={"color": "green"},
            name="Forecast"
        )

        data = [data, pred]

        fig = go.Figure(data=data)
        st.plotly_chart(fig, use_container_width=True)


def display_history_and_forecasted(city, feature, forecast_df):
    if feature == 'AQI':
        future_url = "../data/AQI_Forecast_Monthly.xlsx"
        history_city = pd.read_excel(future_url, sheet_name=city)
        history_city = history_city.rename(columns={'DATE': 'Date'})
        forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
        df_res = pd.merge(history_city, forecast_df, on='Date', how='outer')
        combined_linegraph(df_res, 'AQI')
        with st.expander("Inference", expanded=True):
            st.write("""
                The chart above shows the plot of the historical data of AQI values and the forecasted values for the 12 months of 2023. The blue color line shows the historical data and the green line shows the forecasted values
            """)
    else:
        future_url = '../hackathon_forecasts_output/Heatwave_Forecast.xlsx'
        forecast_df = pd.read_excel(future_url, sheet_name=city)
        forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
        history_city['Date'] = pd.to_datetime(history_city['Date'])
        df_res = pd.merge(history_city, forecast_df, on='Date', how='outer')
        combined_linegraph(df_res, 'Max Temp (°C)')


def display_aqi(city, slider_col):
    future_url = "../data/AQI_Forecast_Monthly.xlsx"
    aqi_city = pd.read_excel(future_url, sheet_name=city)

    aqi_city = aqi_city[aqi_city['Date'] < '2024-01-01']
    aqi_city.rename(
        columns={'AQI_Predictions': 'Predictions'}, inplace=True)
    st.markdown("<hr>",
                unsafe_allow_html=True)
    st.text("")
    with slider_col:
        start_month, end_month = st.select_slider('Pick Month Range', options=(aqi_city['Date']), value=(
            aqi_city['Date'].iloc[0], aqi_city['Date'].iloc[-1]))
    aqi_city = aqi_city[(aqi_city['Date'] >=
                        start_month) & (aqi_city['Date'] <= end_month)]
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.table(aqi_city)
    with col2:
        st.subheader('{} Monthly Predictions'.format(city))
        fig = utils.linegraph(aqi_city['Date'],
                              aqi_city['Predictions'], 'AQI', 'Date', 'AQI')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    get_statistics(aqi_city, 'AQI')
    display_model_details(city, aqi_city, 'AQI')
    display_history_and_forecasted(city, 'AQI', aqi_city)


@st.cache_data
def load_prophet(city):
    with open('./models/{}_model.json'.format(city), 'r') as fin:
        m = model_from_json(fin.read())

    future_url = "../data/AQI_Forecast_Monthly.xlsx"
    forecasts = pd.read_excel(future_url, sheet_name=city)
    forecasts.drop(list(forecasts.columns)[0], axis=1, inplace=True)

    future = m.make_future_dataframe(periods=len(forecasts))
    fcst = m.predict(future)

    fig1 = prophet.plot.plot_plotly(m, fcst)
    st.plotly_chart(fig1, use_container_width=True)


def show_geomap():
    st.markdown("<hr>",
                unsafe_allow_html=True)
    st.subheader("Heatwave Occurences Count")
    st.text("")
    image = Image.open('./images/geomap.jpg')
    st.image(image, caption='Heatwave Frequencies for the given cities')


def display_heatwave(city, slider_col):
    future_url = '../hackathon_forecasts_output/Heatwave_Forecast.xlsx'
    weather_city = pd.read_excel(future_url, sheet_name=city)
    weather_city = weather_city[(
        weather_city['Date'] < '2024-01-01') & (weather_city['Date'] > '2022-12-01')]
    weather_city = weather_city.assign(
        Heatwave_Occurence=weather_city['Predictions'] > 40)
    st.markdown("<hr>",
                unsafe_allow_html=True)
    st.text("")
    with slider_col:
        start_month, end_month = st.select_slider('Pick Month Range', options=(weather_city['Date']), value=(
            weather_city['Date'].iloc[0], weather_city['Date'].iloc[-1]))
    weather_city = weather_city[(weather_city['Date'] >=
                                 start_month) & (weather_city['Date'] <= end_month)]
    col1, col2 = st.columns(2, gap="medium")
    weather_city['Month'] = pd.to_datetime(weather_city['Date']).apply(
        lambda x: x.strftime('%B'))
    with col1:
        weather_city['Heatwave'] = weather_city['Heatwave_Occurence'].apply(
            lambda x: 'Yes' if x else 'No')
        st.table(weather_city[['Date', 'Predictions', 'Heatwave']])
    with col2:
        st.subheader('{} Monthly Predictions'.format(city))
        fig = utils.linegraph(weather_city['Date'],
                              weather_city['Predictions'], 'AQI', 'Date', 'AQI')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("Heat Wave Occurence Count")
        st.metric('Heatwave Occurence Count',
                  weather_city['Heatwave_Occurence'].sum(), 0)
    with c2:
        st.subheader("Heat Wave Occurence Months")
        heatwave_months = weather_city[weather_city['Heatwave_Occurence'] == True]
        heatwave_months = heatwave_months[['Month', 'Predictions']]
        st.table(heatwave_months)
    st.markdown("<hr>",
                unsafe_allow_html=True)
    get_statistics(weather_city, 'Weather')
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Prophet Model Forecasts")
    load_prophet(city)
    display_model_details(city, weather_city, 'Weather')
    show_geomap()


# Config
st.set_page_config(page_title='Monthly Predictions',
                   page_icon=':bar_chart:', layout='wide')

st.markdown("<h1 style='text-align: center; color: black;font-size:50px'>ATLAS MADNESS HACK</h1><hr>",
            unsafe_allow_html=True)

st.title("MONTHLY PREDICTIONS : OUR OBJECTIVE")
st.text(" ")
# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Data Sources

# Filter
main_c1, main_c2 = st.columns(2, gap="medium")

with main_c1:
    col1, col2 = st.columns(2, gap="medium")
    city_list = ['Warangal', 'Karimnagar', 'Khammam', 'Nizamabad', 'Adilabad']
    with col1:
        city = st.selectbox(
            "Select City",
            city_list
        )

    with col2:
        options = st.selectbox(
            "Select the Feature To Be Predicted",
            ("Heatwave", "AQI")
        )

if options == 'AQI':
    display_aqi(city, main_c2)
else:
    display_heatwave(city, main_c2)
utils.get_initial()
