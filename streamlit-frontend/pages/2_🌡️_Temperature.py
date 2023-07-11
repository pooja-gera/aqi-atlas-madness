# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import requests

import json
import codecs
from pandas import json_normalize
import numpy as np
from streamlit_card import card
from datetime import date
from scipy.stats import skew
from datetime import datetime
# Global Variables
theme_plotly = "streamlit"  # None or streamlit


def calc_skew(df, target):

    skewness = skew(df[target])

    # determine skewness type based on skewness coefficient
    if skewness > 0:
        return "The Temperature data is right-skewed"
    elif skewness < 0:
        return "The Temperature data is left-skewed"
    else:
        return "The Temperature data is normally distributed"


def get_statistics(df, target):
    median = np.mean(df[target].values)
    max = np.max(df[target].values)
    min = np.min(df[target].values)
    return min, median, max


def print_3(stat, names):
    col_list = list(st.columns(3, gap="medium"))
    for i in range(len(col_list)):
        with col_list[i]:
            # print(df['Predictions'].iloc[i])
            st.metric(names[i], f"{int(np.round(stat[i]))} °C")


def display_daily(city):

    history_url = "./data/WeatherHistoryDaily.xls"
    future_url = "./data/WeatherForecastDaily.xls"
    df_hist = pd.read_excel(history_url, sheet_name=city)
    # df_hist['DATE']=datetime.strptime(df_hist['DATE'],'%Y-%m-%d').toDate()
    df_hist['DATE'] = pd.to_datetime(df_hist['DATE'])
    df_hist['DATE'] = df_hist['DATE'].dt.strftime('%Y-%m-%d')
    df_hist['AQI'] = np.round(df_hist['Max Temp'])
    print(df_hist)
    df_fut = pd.read_excel(future_url, sheet_name=city)
    df_fut.rename(columns={'Date': 'DATE'}, inplace=True)
    df_fut['DATE'] = pd.to_datetime(df_fut['DATE'])
    df_fut['DATE'] = df_fut['DATE'].dt.strftime('%Y-%m-%d')
    print(df_fut)
    df_fut['Predictions'] = np.round(df_fut['Predictions'])

    df_res = pd.merge(df_hist, df_fut, on='DATE', how='outer')
    # st.write(df_res)
    with st.container():

        st.subheader("Daily Temperature Predictions")
        st.markdown("""---""")

        data = go.Scatter(
            x=df_res["DATE"],
            y=df_res["Max Temp"],
            mode='lines',
            name="Data values"
        )

        pred = go.Scatter(
            x=df_res["DATE"],
            y=df_res["Predictions"],
            mode='lines',

            line={"color": "#9467bd"},
            name="Forecast"
        )

        data = [data, pred]

        layout = go.Layout(title="Temperature Forecast")

        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.text(' ')
        st.text(' ')
        st.markdown('---')

    with st.container():
        st.subheader("Daily Temperature Data Statistics")

        st.markdown('---')
        res = get_statistics(df_hist, 'Max Temp')
        stat = ['Minimum', 'Median', 'Maximum']
        print_3(res, stat)
        fig = px.histogram(df_hist, x="Max Temp",
                           title='Temperature Distribution', marginal='box')
        st.plotly_chart(fig, use_container_width=True)
        min_date = df_hist.loc[df_hist['Max Temp'] == res[0], 'DATE'].iloc[0]
        max_date = df_hist.loc[df_hist['Max Temp'] == res[2], 'DATE'].iloc[0]
        with st.expander("**Inference**", expanded=True):

            st.markdown(
                f"""
                        
                        - **Minimum Temperature for {city} was on {min_date}**
                        - **Maximum Temperature for {city} was on {max_date}**
                        - **{calc_skew(df_hist,'Max Temp')}**
                        """
            )


def display_monthly(city):

    history_url = "./data/WeatherHistoryMonthly.xls"
    future_url = "./data/WeatherForecastMonthly.xls"
    df_hist = pd.read_excel(history_url, sheet_name=city)
    # df_hist['DATE']=datetime.strptime(df_hist['DATE'],'%Y-%m-%d').toDate()
    df_hist.rename(columns={'DATE': 'Date'}, inplace=True)
    df_hist['Date'] = pd.to_datetime(df_hist['Date'])
    df_hist['Date'] = df_hist['Date'].dt.strftime('%Y-%m-%d')
    df_hist['AQI'] = np.round(df_hist['Max Temp'])
    print(df_hist)
    df_fut = pd.read_excel(future_url, sheet_name=city)
    df_fut['Date'] = pd.to_datetime(df_fut['Date'])
    df_fut['Date'] = df_fut['Date'].dt.strftime('%Y-%m-%d')
    print(df_fut)
    df_fut['Predictions'] = np.round(df_fut['Predictions'])

    df_res = pd.merge(df_hist, df_fut, on='Date', how='outer')

    with st.container():
        st.text(' ')
        st.text(' ')
        st.markdown('---')
        st.subheader("Monthly Temperature Predictions")
        st.markdown("""---""")

        data = go.Scatter(
            x=df_res["Date"],
            y=df_res["Max Temp"],
            mode='lines',
            name="Data values"
        )

        pred = go.Scatter(
            x=df_res["Date"],
            y=df_res["Predictions"],
            mode='lines',

            line={"color": "#9467bd"},
            name="Forecast"
        )

        data = [data, pred]

        layout = go.Layout(title="Temperature Forecast")

        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

        st.text(' ')
        st.text(' ')
        st.markdown('---')

    with st.container():

        st.subheader("Monthly Temperature Data Statistics")
        st.markdown('---')
        res = get_statistics(df_hist, 'Max Temp')
        stat = ['Minimum', 'Median', 'Maximum']
        print_3(res, stat)
        fig = px.histogram(df_hist, x="Max Temp",
                           title='Temperature Distribution', marginal='box')
        st.plotly_chart(fig, use_container_width=True)
        min_date = df_hist.loc[df_hist['Max Temp'] == res[0], 'Date'].iloc[0]
        max_date = df_hist.loc[df_hist['Max Temp'] == res[2], 'Date'].iloc[0]
        with st.expander("**Inference**", expanded=True):

            st.markdown(
                f"""
                        - **Minimum Temperature for {city} was on {datetime.strptime(min_date,'%Y-%m-%d').strftime('%B %Y')}**
                        - **Maximum Temperature for {city} was on {datetime.strptime(max_date,'%Y-%m-%d').strftime('%B %Y')}**
                        - **{calc_skew(df_hist,'Max Temp')}**
                        """
            )


st.set_page_config(page_title='Temperature',
                   page_icon=':bar_chart:', layout='wide')
st.markdown("<h1 style='text-align: center; color: black;font-size:50px'>ATLAS MADNESS HACK</h1><hr>",
            unsafe_allow_html=True)

st.text("")
st.text("")

st.title("🌡️ TEMPERATURE")
st.text(" ")
st.text(" ")

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


city_list = ['Adilabad', 'Warangal', 'Karimnagar', 'Khammam', 'Nizamabad']
city = st.selectbox(
    "Select City",
    city_list
)

display_daily(city)

display_monthly(city)
