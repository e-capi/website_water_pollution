import streamlit as st
import numpy as np
import pandas as pd


st.markdown("""# Water Pollution
""")

st.markdown("# What are we analyzing today ? :")

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

columns = st.columns(2)
water_station = columns[0].selectbox("Select you water station to analyze", ("Rhône", "toton", "tata"))
prediction_time = columns[1].selectbox("Select the amount of months to predict", ("1", "3", "6", "9", "12", "24"))
