# import requests
import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd
from functions import *
from rivers import DATA_coord
import pydeck as pdk
import streamlit as st
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta



#______________________________Model________________________________________

def model_plot(id_station, water_station, json_response):
    #Convert the response to a DF
    preddf = pd.DataFrame(json_response)
    preddf.date = pd.to_datetime(preddf.date)
    preddf.set_index('date', inplace=True)

    # Used Variables
    today = date.today()
    rmse = 2.19
    station_name = water_station


    #Plot
    with plt.style.context('fivethirtyeight'):

        fig = plt.figure(figsize=(12, 5.3))
        ax = plt.gca()

        # Date Format
        dt_fmt = mdates.DateFormatter('%y-%m-%d')
        ax.xaxis.set_major_formatter(dt_fmt)

        # Prediction Plot
        plt.title(f'{station_name}\n Nitrate Pollution Prediction')
        plt.plot(preddf.index, preddf.prediction)
        plt.ylabel('Concentration (mg/L)')

        # Plots the rmse delta
        plt.fill_between(preddf.index,
                        preddf.prediction - rmse,
                        preddf.prediction + rmse,
                        color='k',
                        alpha=.05)

        # Plots the today line
        ax.axvline(x=today, ymin=0., ymax=0.9, c='red', alpha=0.6, linewidth=2)
        ax.text(today - timedelta(1),
                0,
                "Today",
                alpha=1,
                ha='center',
                color='red',
                rotation=90)  # center

        # Background color
        fig.patch.set_facecolor('white')  # Figure Background
        ax.set_facecolor('white')  # Axe Background
        for location in ['left', 'right', 'bottom', 'top']:  # Disable spines
            ax.spines[location].set_visible(False)

        plt.xticks(rotation=25)

        plt.ylim(bottom=-1)
        plt.ylim(top=plt.ylim()[1] + 3)
        print(plt.xlim())
        # plt.show()
    return fig


#________________________________MAP Plotting___________________________________


#prepare the River path data
def map_plot(water_station_lat, water_station_lon, water_station):
    DATA_coord = pd.read_csv(
        "croquis_coord/PolygonConverted.csv",
        encoding_errors="ignore")

    #saone_data_path = generate_rivers_coordinates("Saône", DATA_coord)
    saone_data_path = generate_saone_coordinates()

    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


    saone_data_path['color'] = saone_data_path['color'].apply(hex_to_rgb)


    view_state = pdk.ViewState(latitude=water_station_lat, longitude=water_station_lon,
                            zoom=8)  #initial map point of view

    layer = pdk.Layer(type='PathLayer',
                    data=saone_data_path,
                    pickable=True,
                    get_color='color',
                    width_scale=20,
                    width_min_pixels=2,
                    get_path='path',
                    get_width=30)

    #prepare the stations data
    df_station = pd.read_pickle(
        "croquis_coord/stationsdf.pickle"
    )
    df_station["coord"] = df_station["coord"].apply(lambda x: (x[1], x[0]))
    df_station["mean_station_radius"] = df_station["mean_station"] * 120

    df_station_chosen_station = df_station[df_station["label"] == water_station] #to put the water station
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
        get_radius="mean_station_radius",
        get_fill_color=[64, 64, 64],
        get_line_color=[30, 30, 30],
    )

    layer_3 = pdk.Layer(
        "ScatterplotLayer",
        df_station_chosen_station,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=1,
        radius_max_pixels=10,
        line_width_min_pixels=1,
        get_position="coord",
        get_radius="mean_station_radius",
        get_fill_color=[45, 131, 39],
        get_line_color=[69, 192, 60],
    )


    r = pdk.Deck(
        layers=[layer, layer_2, layer_3],
        initial_view_state=view_state,
        tooltip={'text': '{label}\n{mean_station}'
                 },  #put the prediction instead of the moyen
        map_style="road")

    return r
# ____________________________________________________________________
# def plot_538(lower, upper, forecast, initial):

#     # We keep only 36 month of the initial series
#     initial = initial[-36:]

#     # We add to forecast, lower and upper the last point of initial
#     # to join the two curves
#     lower = pd.concat([initial[-1:],lower])
#     upper = pd.concat([initial[-1:],upper])
#     forecast = pd.concat([initial[-1:],forecast])

#     with plt.style.context('fivethirtyeight'):

#         fig = plt.figure(figsize=(12,5))
#         ax = plt.axes()

#         ax.set_facecolor("white")
#         fig.patch.set_facecolor('white')
#         for location in ['left','right','bottom','top']:
#             ax.spines[location].set_visible(False)

#         plt.plot(initial,label='Data History')
#         plt.plot(forecast,label='Data Prediciton ')
#         plt.fill_between(lower.index,lower,upper,color='k',alpha=.10)

#         plt.xticks(rotation=50)

#         plt.title('Nitrate Concentration (mg/L)')
#         plt.legend()
#         plt.ylim(bottom=-1,top=(ax.get_ylim()[1]+4))
#         # plt.show()


#     return fig
