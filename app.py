from inspect import indentsize
from re import L
from pandas.core.indexes.base import Index
import streamlit as st
import numpy as np
import pandas as pd
import requests
from settings import dict_station, prediction_list, url
from plotting import plot_24

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

response = requests.get(url, params=params).json()
# st.write(response) # leave this here

#Response to DF
df_predict = pd.DataFrame(response)
st.write(df_predict)

#_____________________________Plotting__________________________________________

forecast = pd.Series(response.get("forecast"))
upper = pd.Series(response.get("upper"))
lower = pd.Series(response.get("lower"))

forecast = pd.DataFrame(forecast)
upper = pd.DataFrame(upper)
lower = pd.DataFrame(lower)


df_predict.index = pd.to_datetime(df_predict.index)
forecast.index = pd.to_datetime(forecast.index)
upper.index = pd.to_datetime(upper.index) #try to put in the method (upper.index, index = index) 2d being the variable defined on the function
lower.index = pd.to_datetime(lower.index)
print(lower)

df = df_predict.asfreq(freq = 'MS', method = 'pad')
forecast = forecast.asfreq(freq = 'MS', method = 'pad')
upper = upper.asfreq(freq='MS', method='pad')
lower = lower.asfreq(freq='MS', method='pad')


# _


#@st.cache #TB implement
st.pyplot(plot_24(df, prediction_time, upper, lower))





#_______________________________________________________________________________

#Our model graph (TBD)
st.markdown("## This could be our model :")
@st.cache
def prediction_model_():

    return pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Time', 'Series', 'other']
        )

df = prediction_model_()
st.line_chart(df)

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
