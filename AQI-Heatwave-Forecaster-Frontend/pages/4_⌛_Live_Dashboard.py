# Libraries
import streamlit as st
from data import get_data
import utils
import numpy as np
# Confit
st.set_page_config(page_title='AQI Weather Forecaster',
                   page_icon=':bar_chart:', layout='wide', initial_sidebar_state='collapsed')

st.markdown("<h1 style='text-align: center; color: black;font-size:50px'>ATLAS MADNESS HACK</h1><hr>",
            unsafe_allow_html=True)

city = st.selectbox("SELECT ANY ONE OF THE CITY ", ("Adilabad",
                    "Nizamabad", "Khammam", "Warangal", "Karimnagar"))

temp_unit = " °C"
wind_unit = " km/h"

line_aqi_fig, line_weather_fig, temp, current_weather, icon, forecast_dates, aqi_forecast, weather_forecast, current_aqi, condition = get_data(
    "Get current data", city)


def getWeatherIcon(condition):
    if (condition < 300):
        return '🌩'
    elif (condition < 400):
        return '🌧'
    elif (condition < 600):
        return '☔️'
    elif (condition < 700):
        return '☃️'
    elif (condition < 800):
        return '🌫'
    elif (condition == 800):
        return '☀️'
    elif (condition <= 804):
        return '☁️'
    else:
        return '🤷‍'


with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("___")

main_col1, main_col2 = st.columns(2)
with main_col1:
    st.markdown("# **:blue[Live Data]**")
    st.text(" ")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("TEMPERATURE", temp+temp_unit)

    with col2:
        st.metric("AQI", current_aqi)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "WEATHER", f"{current_weather}  {getWeatherIcon(condition)} ")

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.write("## Current Temperature➡️ ")
    # with col2:
    #    st.title(getWeatherIcon(condition))


with main_col2:
    gauge_chart = utils.gauge_chart(int(current_aqi))
    st.plotly_chart(gauge_chart, use_container_width=True)


st.markdown("___")
st.markdown("# **:blue[Weekly Forecast Data]**")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7, gap="medium")
with col1:
    st.subheader("{}".format(forecast_dates[0]))
    st.metric("TEMPERATURE", str(
        weather_forecast[0])+temp_unit, delta=round(weather_forecast[0]-float(temp), 2))
    st.metric("AQI", aqi_forecast[0], delta=round(
        aqi_forecast[0]-float(current_aqi), 2))

with col2:
    st.subheader("{}".format(forecast_dates[1]))
    st.metric("TEMPERATURE", str(
        weather_forecast[1])+temp_unit, delta=round(weather_forecast[1]-float(temp), 2))
    st.metric("AQI", aqi_forecast[1], delta=round(
        aqi_forecast[1]-float(current_aqi), 2))

with col3:
    st.subheader("{}".format(forecast_dates[2]))
    st.metric("TEMPERATURE", str(
        weather_forecast[2])+temp_unit, delta=round(weather_forecast[2]-float(temp), 2))
    st.metric("AQI", aqi_forecast[2], delta=round(
        aqi_forecast[2]-float(current_aqi), 2))

with col4:
    st.subheader("{}".format(forecast_dates[3]))
    st.metric("TEMPERATURE", str(
        weather_forecast[3])+temp_unit, delta=round(weather_forecast[3]-float(temp), 2))
    st.metric("AQI", aqi_forecast[3], delta=round(
        aqi_forecast[3]-float(current_aqi), 2))


with col5:
    st.subheader("{}".format(forecast_dates[4]))
    st.metric("TEMPERATURE", str(
        weather_forecast[4])+temp_unit, delta=round(weather_forecast[4]-float(temp), 2))
    st.metric("AQI", aqi_forecast[4], delta=round(
        aqi_forecast[4]-float(current_aqi), 2))


with col6:
    st.subheader("{}".format(forecast_dates[5]))
    st.metric("TEMPERATURE", str(
        weather_forecast[5])+temp_unit, delta=round(weather_forecast[5]-float(temp), 2))
    st.metric("AQI", aqi_forecast[5], delta=round(
        aqi_forecast[5]-float(current_aqi), 2))


with col7:
    st.subheader("{}".format(forecast_dates[6]))
    st.metric("TEMPERATURE", str(
        weather_forecast[6])+temp_unit, delta=round(weather_forecast[6]-float(temp), 2))
    st.metric("AQI", aqi_forecast[6], delta=round(
        aqi_forecast[6]-float(current_aqi), 2))

st.markdown("___")

st.markdown("# **:blue[Forecast Plots]**")
tab1, tab2 = st.tabs(["AQI Line Graph", "Weather Line Graph"])

with tab1:
    st.plotly_chart(line_aqi_fig, use_container_width=True)

with tab2:
    st.plotly_chart(line_weather_fig, use_container_width=True)
