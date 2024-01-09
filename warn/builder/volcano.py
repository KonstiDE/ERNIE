import json
import os
import re

from json import JSONDecodeError

import config.config as cfg

import geopandas as gpd

import shutup
shutup.please()

def analyse_volcanos():
    files = os.listdir(cfg.warn_path_volcanos())

    ms = []

    for file in files:
        with open(os.path.join(cfg.warn_path_volcanos(), file)) as f:
            try:
                j = json.loads(f.read())

                for i in range(len(j)):
                    ms.append(j[i])
            except JSONDecodeError as _:
                pass

    df = gpd.GeoDataFrame.from_records(ms)

    df["longitude"] = df["longitude"].astype(float)
    df["latitude"] = df["latitude"].astype(float)
    df["volcanoid"] = df["volcanoid"].astype(float)

    df['geometry'] = gpd.points_from_xy(df['longitude'], df['latitude'])
    df.set_geometry("geometry")
    df.set_crs("EPSG:4326")

    df.to_file("volcanos.gpkg")

    f.close()
