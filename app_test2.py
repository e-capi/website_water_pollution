from inspect import indentsize
from re import L, escape
from pandas.core.indexes.base import Index
import streamlit as st
import numpy as np
import pandas as pd
import requests
from settings import prediction_list, url
from plotting import map_plot
import time
from functions import collect_coord_station_2, give_id_from_station_name_2, collect_name_station_2, generate_rivers_coordinates, dict_station_2
import streamlit.components.v1 as components
import pydeck as pdk

with st.sidebar:

    water_station = st.selectbox("Select you water station to analyze",
                                 collect_name_station_2())  #dict_statio.keys

    prediction_time = st.selectbox("Select the amount of months to predict",
                                   (prediction_list))

id_station = give_id_from_station_name_2(dict_station_2, water_station)

params = {
    'station_id': id_station,  #choose key and give backs the id
    'predict_length': prediction_time  #
}

# st.write(water_station) #name
# st.write(dict_station_2)#.get(water_station))
response = requests.get(url, params=params)

response_dict = response.json()

st.write(response_dict)

water_station_lat = dict_station_2.get(id_station).get("coord")[0]
water_station_lon = dict_station_2.get(id_station).get("coord")[1]

st.pydeck_chart(
    map_plot(water_station_lat=water_station_lat,
             water_station_lon=water_station_lon))
