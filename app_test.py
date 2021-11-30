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

import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st


DATA_coord = pd.read_csv(
    "/home/ecapi/code/e-capi/website_water_pollution/croquis_coord/PolygonConverted.csv",
    encoding_errors="ignore")

saone_data = generate_rivers_coordinates("Sane", DATA_coord)



st.dataframe(saone_data)


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

st.write(saone_data['color'])
saone_data['color'] = saone_data['color'].apply(hex_to_rgb)
st.write(saone_data['color'])


view_state = pdk.ViewState(latitude=45.7640, longitude=4.8357, zoom=10)

layer = pdk.Layer(type='PathLayer',
                  data=saone_data,
                  pickable=True,
                  get_color='color',
                  width_scale=20,
                  width_min_pixels=2,
                  get_path='path',
                  get_width=10)

r = pdk.Deck(layers=[layer],
             initial_view_state=view_state,
             tooltip={'text': '{name}'})

st.pydeck_chart(r)

#test

DATA_URL = "https://raw.githubusercontent.com/uber-common/deck.gl-data/master/website/bart-lines.json"
df = pd.read_json(DATA_URL)

st.dataframe(df)




def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


df['color'] = df['color'].apply(hex_to_rgb)
df['path2'] = saone_data['path']

view_state2 = pdk.ViewState(latitude=37.782556, longitude=-122.3484867, zoom=10)

layer2 = pdk.Layer(type='PathLayer',
                  data=df.head(1),
                  pickable=True,
                  get_color='color',
                  width_scale=20,
                  width_min_pixels=2,
                  get_path='path2',
                  get_width=5)

r = pdk.Deck(layers=[layer2],
             initial_view_state=view_state2,
             tooltip={'text': '{name}'})

st.pydeck_chart(r)
