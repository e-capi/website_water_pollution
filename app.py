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

st.set_page_config(layout="centered",
                   page_icon=Image.open('images/icon_lewagon.png'),
                   page_title="Water Pollution",
                   initial_sidebar_state="collapsed")

#UPPER banner

#__________________________________Logo_________________________________________

lewagon = Image.open('images/lewagon.png')
#ankorstore = Image.open('images/ankorstore.png')

columns = st.columns(2)

logo1 = columns[0].image(lewagon, use_column_width=False)
#logo2 = columns[1].image(ankorstore, use_column_width=False)

#Headers

st.markdown("""# Water Pollution
""")

st.markdown("## Slow the flow ... save the H2O")

#_______________________________________________________________________________

#Container model plot
with st.container():
    #Options boxes
    with st.expander("Choose your station: "):
        col1, col2 = st.columns(2)
        with col1:
            water_station = st.selectbox(
                "Select you water station to analyze",
                collect_name_station_2())  #dict_statio.keys
        with col2:
            predict_button = st.button("Predict")
        #     prediction_time = st.selectbox(
        #         "Select the amount of months to predict", (prediction_list))

        #model
        placeholder_model_plot = st.empty()

        #progression bar

        if predict_button:
            latest_iteration = st.empty()
            bar = st.progress(0)

            for i in range(100):
                # Update the progress bar with each iteration.
                latest_iteration.text(f'{i+1}% Complete')
                bar.progress(i + 1)
                time.sleep(0.05)
            st.success('Completed!')

            #text below plot
        if predict_button or water_station:

            f'Calculating the Water pollution for **{water_station.capitalize()}**'  #in the next **{prediction_time} months ...**'

with st.container():
    placeholder_map = st.empty()

#API response

id_station = give_id_from_station_name_2(dict_station_2, water_station)

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
with st.container():
    with st.expander("Map Visualization: "):

        #Lat and Long with the api
        st.markdown("## Water Station Location")

        water_station_lat = dict_station_2.get(id_station).get("coord")[0]
        water_station_lon = dict_station_2.get(id_station).get("coord")[1]

        st.pydeck_chart(map_plot(water_station_lat, water_station_lon))

#_______________________________________________________________________________

#Button for background image
CSS = """
h1 {
    color: red;
}
.stApp {
    background-image: url(https://wallpaperaccess.com/full/2133933.jpg);
    background-size: cover;
}
"""

if st.checkbox('Inject CSS'):
    st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

#_______________________________END_____________________________________________
