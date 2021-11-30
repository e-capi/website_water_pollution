import requests
import pandas as pd
#beta
url2 = 'https://api-te5jtpgwkq-ew.a.run.app/stations'

response = requests.get(url2)
stations_list = response.json()


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


def generate_rivers_coordinates(river_name, df):

    df_river = df[["name", "PointID", "Longitude", "Latitude"]]
    df_river = df[df["name"] == str(river_name)].copy()

    #make a list of coordinates and put them together
    lat_list = df_river.Latitude.to_list()
    long_list = df_river.Longitude.to_list()

    coord_list = [[lon, lat] for lat, lon in zip(lat_list, long_list)]


    df_map = pd.DataFrame.from_dict({
        "name": [river_name],
        "color": ["#ed1c24"],
        "path": [coord_list]
    })
    return df_map
