# Libraries
import pandas as pd
import requests
from utils import bargraph, linegraph, get_request_data, get_current_aqi
import numpy as np
import streamlit as st
sheets_name = {'Adilabad': 0,
               'Nizamabad': 1,
               'Khammam': 2,
               'Warangal': 3,
               'Karimnagar': 4}

# Data Sources
# @st.cache(ttl=1000, allow_output_mutation=True)


@st.cache_data
def get_data(query, city_name=None):
    if query == 'Transactions Overview':
        return pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/579714e6-986e-421a-85dd-c32a8b41b25c/data/latest')
    elif query == "Get current data":

        api = "9b833c0ea6426b70902aa7a4b1da285c"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api}"
        response = requests.get(url)
        x = response.json()

        weatherforecast_url = "../data/WeatherForecastDaily.xls"
        df_weather = pd.read_excel(
            weatherforecast_url, sheet_name=sheets_name[city_name])
        df_weather['Predictions'] = np.round(
            df_weather['Predictions']).astype(int)

        aqiforecast_url = "../data/AQI_forecast_DAILY.xls"
        df_aqi = pd.read_excel(
            aqiforecast_url, sheet_name=sheets_name[city_name])
        df_aqi['Predictions'] = np.round(df_aqi['Predictions']).astype(int)

        forecast_dates = df_weather['Date'].to_list()[:7]
        aqi_forecast = df_aqi['Predictions'].to_list()[:7]
        weather_forecast = df_weather['Predictions'].to_list()[:7]
        current_aqi = get_current_aqi(city_name)
        for i in range(len(forecast_dates)):
            date = pd.to_datetime(forecast_dates[i], format="%Y-%m-%d")
            date = date.day_name()
            forecast_dates[i] = date

        try:

            cel = 273.15
            icon = x["weather"][0]["icon"],
            condition = x['weather'][0]['id']
            current_weather = x["weather"][0]["description"].title()
            temp = str(round(x["main"]["temp"]-cel))
            line_aqi_fig = linegraph(
                forecast_dates, aqi_forecast, "AQI", "DATES", "AQI")
            line_weather_fig = linegraph(
                forecast_dates, weather_forecast, "WEATHER", "DATES", "WEATHER")

            return line_aqi_fig, line_weather_fig, temp, current_weather, icon, forecast_dates, aqi_forecast, weather_forecast, current_aqi, condition

        except Exception as e:
            print("Error message "+str(e))

    # elif query == "dashboard-aqi":
    #     df_aqi = get_request_data(aqi_url, cityname=city_name)

    #     df_aqi.replace('-', np.nan, inplace=True)
    #     df_aqi['DATE'] = pd.to_datetime(
    #         df_aqi['DATE'], format='%Y/%m/%d').dt.date
    #     df_aqi['DATE'] = pd.to_datetime(
    #         df_aqi['DATE'])

    #     for col in df_aqi.columns.to_list()[1:]:
    #         df_aqi[col] = df_aqi[col].astype("float64")
    #     return df_aqi

    elif query == "dashboard-weather":
        aqi_url = "../data/WeatherHistoryDaily.xls"
        df_weather = pd.read_excel(aqi_url, sheet_name=city_name)
        df_weather.rename(columns={'Date': 'DATE'}, inplace=True)
        df_weather['DATE'] = pd.to_datetime(df_weather['DATE'])

        df_weather['DATE'] = df_weather['DATE'].dt.strftime('%Y-%m-%d')

        df_weather.replace('-', np.nan, inplace=True)
        df_weather['DATE'] = pd.to_datetime(
            df_weather['DATE'], format='%Y/%m/%d').dt.date
        df_weather['DATE'] = pd.to_datetime(
            df_weather['DATE'])

        for col in df_weather.columns.to_list()[1:]:
            df_weather[col] = df_weather[col].astype("float64")

        return df_weather, df_weather.columns.to_list()[1:]

    return None
