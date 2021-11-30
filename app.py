from inspect import indentsize
from re import L
from pandas.core.indexes.base import Index
import streamlit as st
import numpy as np
import pandas as pd
import requests
from settings import dict_station, prediction_list, url
from plotting import plot_538
import time
from functions import collect_name_coord_station, generate_rivers_coordinates
from PIL import Image
from rivers import DATA_coord


import streamlit.components.v1 as components
import pydeck as pdk

icon_lewagon = Image.open('images/icon_lewagon.png')

st.set_page_config(
    layout="wide",
    page_icon=icon_lewagon,
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

with st.sidebar:

    water_station = st.selectbox(
        "Select you water station to analyze",
        list(dict_station.keys()))  #dict_statio.keys

    prediction_time = st.selectbox("Select the amount of months to predict",(prediction_list))



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
params = {
    'station_id': dict_station.get(water_station),  #choose key and give backs the id
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
placeholder_time_series_plot.pyplot(
    plot_538(lower=lower, upper=upper, forecast=forecast, initial=initial))



#_______________________________________________________________________________


#This could be our viz map (TBD) we would need the lat and long /// put in plotting file
#We could also use a folium
st.markdown("## Water Station Location")
water_station_lat = collect_name_coord_station().get(water_station)[1]
water_station_lon = collect_name_coord_station().get(water_station)[0]


@st.cache
def get_map_data():

    return pd.DataFrame(
            np.random.randn(1, 2) / [50, 50] + [water_station_lat, water_station_lon],
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


#_______________________LINKS___________________________________________________

DATA_coord = pd.read_csv(
    "/home/ecapi/code/e-capi/website_water_pollution/croquis_coord/PolygonConverted.csv",
    encoding_errors="ignore")

saone_data = generate_rivers_coordinates("Sane", DATA_coord)

st.dataframe(saone_data)


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


saone_data['color'] = saone_data['color'].apply(hex_to_rgb)


view_state = pdk.ViewState(latitude=water_station_lat, longitude=water_station_lon, zoom=7) #map initial coords

layer = pdk.Layer(type='PathLayer',
                  data=saone_data,
                  pickable=True,
                  get_color='color',
                  width_scale=20,
                  width_min_pixels=2,
                  get_path='path',
                  get_width=30)

r = pdk.Deck(layers=[layer],
             initial_view_state=view_state,
             tooltip={'text': '{name}'})

st.pydeck_chart(r)



#_______________________________END_____________________________________________
