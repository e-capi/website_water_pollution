import requests
import pandas as pd
#beta
url2 = 'https://api-te5jtpgwkq-ew.a.run.app/stations' #fichier local
response = requests.get(url2)
stations_list = response.json()

url_local = "croquis_coord/stationsdf.pickle"
df_station = pd.read_pickle("croquis_coord/stationsdf.pickle")
dict_station_2 = df_station.to_dict(orient="index")
# ____________________________________
#Collect the label and id from our list of dict stations
def collect_name_id_station(stations_list=stations_list):
    water_stations_id = {}
    for station in stations_list:
        water_stations_id[station["label"]] = station["id"]
    return water_stations_id


def collect_name_coord_station(stations_list=stations_list):
    water_stations_coord = {}
    for station in stations_list:
        water_stations_coord[station["label"]] = station["coord"]
    return water_stations_coord
#___________________________________

def collect_name_station_2(dict_satation_2 = dict_station_2):
    return [dict_station_2.get(x).get("label") for x in dict_station_2]

def give_id_from_station_name_2(dict_station_2, water_station):
    for id in dict_station_2:
        if dict_station_2.get(id).get("label") == water_station:
            return id


def collect_coord_station_2(dict_satation=dict_station_2):
    return [dict_station_2.get(x).get("coord") for x in dict_station_2]


#__________________________________

#__________________________________


def generate_rivers_coordinates(river_name, df):

    df_river = df[["label", "PointID", "Longitude", "Latitude"]]
    df_river = df[df["label"] == str("Sane")].copy()

    #make a list of coordinates and put them together
    lat_list = df_river.Latitude.to_list()
    long_list = df_river.Longitude.to_list()

    coord_list = [[lon, lat] for lat, lon in zip(lat_list, long_list)]


    df_map = pd.DataFrame.from_dict({
        "label": [river_name],
        "color": ["#7e8dbd"],
        "path": [coord_list]
    })
    return df_map


def create_a_dict_from_df(df):
    dictionary = df.to_dict(orient="index")
    return dictionary


def generate_saone_coordinates():

    return pd.read_pickle('croquis_coord/saone_trace.pickle')
