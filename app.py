from inspect import indentsize
from re import L
from pandas.core.indexes.base import Index
import streamlit as st
import numpy as np
import pandas as pd
import requests
from settings import dict_station, prediction_list, url
from plotting import plot_538, r
import time
from functions import *
from PIL import Image



import streamlit.components.v1 as components
import pydeck as pdk

st.set_page_config(
    layout="wide",
    page_icon=Image.open('images/icon_lewagon.png'),
    page_title= "Water Pollution",
    initial_sidebar_state="collapsed"

    )

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

#Request info from the user

# with st.sidebar:

#     water_station = st.selectbox(
#         "Select you water station to analyze",
#         list(dict_station.keys()))  #dict_statio.keys

#     prediction_time = st.selectbox("Select the amount of months to predict",(prediction_list))

with st.sidebar:

    water_station = st.selectbox("Select you water station to analyze",
                                 collect_name_station_2())  #dict_statio.keys

    prediction_time = st.selectbox("Select the amount of months to predict",
                                   (prediction_list))



col1, col2 = st.columns(2)


# with col2:

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'{i+1}% Complete')
    bar.progress(i + 1)
    # time.sleep(0.05)
st.success('Completed!')

placeholder_time_series_plot = st.empty()

placeholder_map = st.empty()

#Plotting with timer WTBD /!\
if prediction_time or water_station:

    f'Calculating the Water pollution for **{water_station.capitalize()}** in the next **{prediction_time} months ...**'


# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()

# chart = st.line_chart(np.zeros(shape=(1,1)))
# x = np.arange(0, 100*np.pi, 0.1)

# for i in range(1, 101):
#     y = np.sin(x[i])
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows([y])
#     progress_bar.progress(i)
#     time.sleep(0.05)

# progress_bar.empty()



#_______________________________________________________________________________

#API response
# params = {
#     'station_id': dict_station.get(water_station),  #choose key and give backs the id
#     'predict_length': prediction_time,  # ""
# }
id_station = give_id_from_station_name_2(dict_station_2, water_station)

params = {
    'station_id': id_station,  #choose key and give backs the id
    'predict_length': prediction_time,  #
}

# st.write(dict_station.get(water_station))
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
placeholder_time_series_plot.pyplot(
    plot_538(lower=lower, upper=upper, forecast=forecast, initial=initial))



#_______________________________________________________________________________


#This could be our viz map (TBD) we would need the lat and long /// put in plotting file

#Lat and Long with the api
st.markdown("## Water Station Location")

# water_station_lat = collect_name_coord_station().get(water_station)[1]
# water_station_lon = collect_name_coord_station().get(water_station)[0]

water_station_lat = dict_station_2.get(id_station).get("coord")[1]
water_station_lon = dict_station_2.get(id_station).get("coord")[0]



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


#__________________________MAP__________________________________________________


st.pydeck_chart(r)

#_______________________________END_____________________________________________
