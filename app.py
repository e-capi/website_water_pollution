from inspect import indentsize
from re import L
from pandas.core.indexes.base import Index
import streamlit as st
import numpy as np
import pandas as pd
import requests
from settings import prediction_list, url
from plotting import map_plot, model_plot
import time
from functions import *
from PIL import Image

import streamlit.components.v1 as components
import pydeck as pdk

#CSS SETUP
st.set_page_config(layout="wide",
                   page_icon=Image.open('images/icon_lewagon.png'),
                   page_title="Water Pollution",
                   initial_sidebar_state="collapsed",
                   )

CSS = """
.stApp {
    background-image: url(https://wallpaperaccess.com/full/2133933.jpg);
    background-size: cover;
    font-family: system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji;
}

h1 {
    padding:0;
    font-weight: 600;
}

h2 {
    padding:0;
}

.table {
    --bs-table-striped-bg:rgb(240, 242, 246)!important;
}

.block-container {
    background-color: #ffffff;
    padding: 1rem 1rem!important;
    margin: 1rem 10rem!important;
    box-shadow: 0 0 20px #0000001f;
    border-radius: 8px;
}
"""
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

#__________________________________Logo_________________________________________

lewagon = Image.open('images/lewagon_600x.png')
water_logo = Image.open('images/logo_100x.jpg')
# water_wave = Image.open('images/water-wave_1f30a.png')

#Headers
columns = st.columns(3)
columns[0].image(water_logo, use_column_width=False)
columns[1].markdown(""" # Predict Water Pollution
""")
logo1 = columns[2].image(lewagon, use_column_width=False)

# st.markdown("## Slow the flow ... save the H2O ")

#_______________________________________________________________________________

with st.container():
    col_pred = st.columns((3, 12))
    col_pred[0].markdown("### Select a water station to analyse: ")
    water_station = col_pred[1].selectbox(
        "", collect_name_station_2())  #dict_statio.keys

    if water_station:
        latest_iteration = st.empty()
        bar = st.progress(0)

        time.sleep(.55)
        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f'{i+1}% Complete')
            bar.progress(i + 1)
            time.sleep(.03)
        # st.success('Completed!')

        #text below plot
    # if water_station:
    #     f'Calculating the Water pollution for **{water_station.capitalize()}**' #in the next **{prediction_time} months ...**'

    # predict_button = st.button("💧 Predict ")

    # if predict_button:
    #     latest_iteration = st.empty()
    #     bar = st.progress(0)

    #     for i in range(100):
    #         # Update the progress bar with each iteration.
    #         latest_iteration.text(f'{i+1}% Complete')
    #         bar.progress(i + 1)
    #         time.sleep(0.05)
    #     st.success('Completed!')

    #     #text below plot
    # if predict_button or water_station:
    #     f'Calculating the Water pollution for **{water_station.capitalize()}**' #in the next **{prediction_time} months ...**'

cont_col1, cont_col2 = st.columns((3, 2))

with cont_col1:

    with st.container():
        #Options boxes
        with st.expander("Prediction Model: ", expanded=True):
            # col1, col2 = st.columns(2)
            # with col1:

            #model
            # st.markdown("## Prediction Model:")
            placeholder_model_plot = st.empty()

            #progression bar

with st.container():
    placeholder_map = st.empty()

#API response

id_station = give_id_from_station_name_2(dict_station_2, water_station)

#NOT WORKING RN
params = {
    'station_id': id_station,  #choose key and give backs the id
    # 'predict_length': prediction_time,
}

# st.write(dict_station.get(water_station))
response = requests.get(url, params=params)

# Dictionaries from the response
response_dict = response.json()

#_____________________________Plotting__________________________________________

placeholder_model_plot.pyplot(
    model_plot(id_station, water_station, response_dict))

#__________________________MAP__________________________________________________
with cont_col2:
    with st.container():
        with st.expander("Map Visualization: ", expanded=True):

            #Lat and Long with the api
            st.markdown("## Water Station Location")

            water_station_lat = dict_station_2.get(id_station).get("coord")[0]
            water_station_lon = dict_station_2.get(id_station).get("coord")[1]

            st.pydeck_chart(
                map_plot(water_station_lat, water_station_lon, water_station))

st.success('Prediction Successful !')

#__________________socials_________________________

# st.markdown(
#     "![GitHub Repo stars](https://img.shields.io/github/stars/e-capi/website_water_pollution?label=water_Pollution&style=social)"
# )

#_______________________________END_____________________________________________
