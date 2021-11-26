from inspect import indentsize
from re import L
from pandas.core.indexes.base import Index
import streamlit as st
import numpy as np
import pandas as pd
import requests
from settings import dict_station, prediction_list, url
from plotting import plot_538

#Headers

st.markdown("""# Water Pollution
""")

st.markdown("# What are we analyzing today ? :")

#_______________________________________________________________________________

#Request info from the user


columns = st.columns(2)
water_station = columns[0].selectbox(
    "Select you water station to analyze",
    list(dict_station.keys()))  #dict_statio.keys
prediction_time = columns[1].selectbox(
    "Select the amount of months to predict", (prediction_list))

#_______________________________________________________________________________

#API response
params = {
    'station_id': dict_station.get(water_station),  # imported from app.py
    'predict_length': prediction_time,  # ""
}

response = requests.get(url, params=params)

    # Dictionaries from the response

response_dict = response.json()

initial_dict = response_dict['initial']
forecast_dict = response_dict['forecast']
lower_dict = response_dict['lower']
upper_dict = response_dict['upper']

    # Pandas Series from dictionaries

lower = pd.Series(lower_dict,index=lower_dict.keys())
upper = pd.Series(upper_dict,index=upper_dict.keys())
forecast = pd.Series(forecast_dict,index=forecast_dict.keys())
initial = pd.Series(initial_dict,index=initial_dict.keys())

    # Index convertion to timestamp

lower.index = pd.to_datetime(lower.index)
upper.index = pd.to_datetime(upper.index)
forecast.index = pd.to_datetime(forecast.index)
initial.index = pd.to_datetime(initial.index)

#_____________________________Plotting__________________________________________

#@st.cache how do we put the cache if the function is constructed in another file ?
st.pyplot(plot_538(lower=lower, upper=upper, forecast=forecast, initial=initial))


#_______________________________________________________________________________


#This could be our viz map (TBD) we would need the lat and long
#We could also use a folium
st.markdown("## This could be our map")
@st.cache
def get_map_data():

    return pd.DataFrame(
            np.random.randn(1, 2) / [50, 50] + [45.7640, 4.8357],
            columns=['lat', 'lon']
        )

df = get_map_data()
st.map(df)

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
