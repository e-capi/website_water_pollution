from functions import collect_name_id_station
#Dict with the stations ID to make the request to the API & selection box
dict_station = collect_name_id_station() #TB filled
dict_lat_lon = "_"
prediction_list = ["1", "3", "6", "9", "12", "24"]


#API requests
url = 'https://api-te5jtpgwkq-ew.a.run.app/predict'

