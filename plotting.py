import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd
from functions import generate_rivers_coordinates
from rivers import DATA_coord
import pydeck as pdk
import streamlit as st


def plot_538(lower, upper, forecast, initial):

    # We keep only 36 month of the initial series
    initial = initial[-36:]

    # We add to forecast, lower and upper the last point of initial
    # to join the two curves
    lower = pd.concat([initial[-1:],lower])
    upper = pd.concat([initial[-1:],upper])
    forecast = pd.concat([initial[-1:],forecast])

    with plt.style.context('fivethirtyeight'):

        fig = plt.figure(figsize=(12,5))
        ax = plt.axes()

        ax.set_facecolor("white")
        fig.patch.set_facecolor('white')
        for location in ['left','right','bottom','top']:
            ax.spines[location].set_visible(False)

        plt.plot(initial,label='Data History')
        plt.plot(forecast,label='Data Prediciton ')
        plt.fill_between(lower.index,lower,upper,color='k',alpha=.10)

        plt.xticks(rotation=50)

        plt.title('Nitrate Concentration (mg/L)')
        plt.legend()
        plt.ylim(bottom=-1,top=(ax.get_ylim()[1]+4))
        # plt.show()


    return fig


#________________________________MAP Plotting___________________________________


#prepare the River path data
DATA_coord = pd.read_csv(
    "/home/ecapi/code/e-capi/website_water_pollution/croquis_coord/PolygonConverted.csv",
    encoding_errors="ignore")

saone_data_path = generate_rivers_coordinates("Saône", DATA_coord)


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


saone_data_path['color'] = saone_data_path['color'].apply(hex_to_rgb)

view_state = pdk.ViewState(latitude=45.7640, longitude=4.8357,
                           zoom=10)  #initial map point of view

layer = pdk.Layer(type='PathLayer',
                  data=saone_data_path,
                  pickable=True,
                  get_color='color',
                  width_scale=20,
                  width_min_pixels=2,
                  get_path='path',
                  get_width=10)

#prepare the stations data
df_station = pd.read_pickle(
    "/home/ecapi/code/e-capi/website_water_pollution/croquis_coord/stationsdf.pickle"
)
df_station["coord"] = df_station["coord"].apply(lambda x: (x[1], x[0]))
df_station["exits_radius"] = 300

layer_2 = pdk.Layer(
    "ScatterplotLayer",
    df_station,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=10,
    line_width_min_pixels=1,
    get_position="coord",
    get_radius="exits_radius",
    get_fill_color=[255, 140, 0],
    get_line_color=[0, 0, 0],
)

r = pdk.Deck(layers=[layer_2, layer],
             initial_view_state=view_state,
             tooltip={'text': '{label}'},
             map_style="road")

st.pydeck_chart(r)
