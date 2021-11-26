import requests
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
