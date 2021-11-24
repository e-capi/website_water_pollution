import streamlit as st
import numpy as np
import pandas as pd
import requests

#Headers
st.markdown("""# Water Pollution
""")

st.markdown("# What are we analyzing today ? :")


#Dict with the stations ID to make the request to the API & selection box
dict_station = {"caluire": 6059500, "miribel": 6059509}
prediction_list = ["1", "3", "6", "9", "12", "24"]

columns = st.columns(2)
water_station = columns[0].selectbox(
    "Select you water station to analyze",
    list(dict_station.keys()))  #dict_statio.keys
prediction_time = columns[1].selectbox(
    "Select the amount of months to predict", (prediction_list))

#API requests

url = 'https://api-te5jtpgwkq-ew.a.run.app/predict'

params = {
    'station_id': dict_station.get(water_station),  # Station caluire #
    'predict_length': prediction_time,  # Period of prediction to analyse
}

response = requests.get(url, params=params)
st.write(response.json())

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
