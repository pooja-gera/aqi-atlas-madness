# Libraries
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
from streamlit_card import card
from datetime import date
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title='About Us',
                   page_icon=':people_hugging:', layout='wide', initial_sidebar_state='collapsed')
st.markdown("<h1 style='text-align: center; color: black;font-size:50px'>ATLAS MADNESS HACK</h1><hr>",
            unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("OUR APPLICATION'S MAJOR FEATURES")
st.write("""
    1. Dynamic Forecasting of AQI and Temperature Data using live data.
    2. Using a scheduler based approach of training the models based on the live data.
    3. Live Dashboard for each Tier 2 city in Telangana with various filters.
    4. Real Time Capturing of Data using Web Scraping Strategy.
    5. Displaying our EDA and various statistical analysis and visuals showing the effectiveness and scalabilty of our predictions
""")
st.subheader("OUR NEXT APPROACHES TOWARDS SETTING UP OUR START UP")
st.write("""
    1. Our major objective of building up our startup application is towards building a an application towards our environment
    2. So on our first approach we have a plan to capture user emails and details of people visiting our page and sending them daily alerts on the AQI and heatwave levels
    3. We have also planned to send our forecasted values as an idea about the future days so that people can take precautionary messages accordingly.
    4. We have also planned to create a complete dashboard by generating a lot of KPI measures and make people aware about the statistics of their places.
    5. Maintain a good quality of the data and provide paid reliable data source endpoints to fetch the reliable data maintained. 
""")
st.markdown("<hr>", unsafe_allow_html=True)
st.header("ABOUT US - TEAM APK ;)")
st.markdown("<hr>", unsafe_allow_html=True)
user1_col1, padding, user1_col2 = st.columns((6, 1, 15), gap="small")
with user1_col1:
    ashish = Image.open('./images/arjun.jpeg')
    # ashish = ashish.resize((400, 500))
    st.image(ashish, caption="Team Member 1 - Arjun")
with user1_col2:
    st.header("Arjun Dhawan")
    st.write("""Hello This is Arjun Dhawan, from Thapar University currently pursuing my 4th year MSc Data Science course at PSG College of Technology.\n
    AREAS OF INTEREST : Backend/Core/DevOps\n
    WORK EXPERIENCE   : Intern at Saptang Labs,IITM\n
    GITHUB PROFILE    : https://github.com/arjundvn24\n
    LINKEDIN URL      : https://www.linkedin.com/in/arjun-dhawan-2002/\n 
    """)
st.markdown("<hr>", unsafe_allow_html=True)
user2_col1, padding, user2_col2 = st.columns((15, 1, 6), gap="small")
with user2_col2:
    jega = Image.open('./images/kt.jpeg')
    # jega = jega.resize((400, 500))
    st.image(jega, caption="Team Member 2 - Karan")
with user2_col1:
    st.header("Karan Taneja")
    st.write("""Hello This is Karan Taneja, from Thapar University\n
    WORK EXPERIENCE   : Intern at INDMoney\n
    GITHUB PROFILE    : https://www.github.com/karantaneja01\n
    LINKEDIN URL      : https://www.linkedin.com/in/karantaneja01/\n
    """)
st.markdown("<hr>", unsafe_allow_html=True)
user3_col1, padding, user3_col2 = st.columns((6, 1, 15), gap="small")
with user3_col1:
    jega = Image.open('./images/pooja.jpg')
    # jega = jega.resize((400, 500))
    st.image(jega, caption="Team Member 3 - Pooja")
with user3_col2:
    st.header("Pooja Gera")
    st.write("""Hello This is Pooja Gera, from IGDTUW\n
    AREAS OF INTEREST : Machine Learning\n
    WORK EXPERIENCE   : Summer Intern at Microsoft\n
    GITHUB PROFILE    : https://www.github.com/pooja-gera\n
    LINKEDIN URL      : https://www.linkedin.com/in/pooja-gera\n
    """)
