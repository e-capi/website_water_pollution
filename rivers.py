import pandas as pd

DATA_coord = pd.read_csv(
    "/home/ecapi/code/e-capi/website_water_pollution/croquis_coord/PolygonConverted.csv",
    encoding_errors="ignore")

df = DATA_coord[["name", "PointID", "Longitude", "Latitude"]]


#here

