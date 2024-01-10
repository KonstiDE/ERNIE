import json
import os
import re

from json import JSONDecodeError

import config.config as cfg

import geopandas as gpd
import pandas as pd
import numpy as np

from plotting.wrapper import wrap_plot as mplot

def analyse_earthquakes(to_file=False):
    files = os.listdir(cfg.warn_path_earthquakes())

    ms = []

    for file in files:
        with open(os.path.join(cfg.warn_path_earthquakes(), file)) as f:
            try:
                j = json.loads(
                    f.read()
                    .replace("経度", "long")
                    .replace("緯度", "lat")
                    .replace("震源地", "epicenter_loc")
                    .replace("震源深さ", "epicenter_depth")
                    .replace("発生日時", "timestamp")
                    .replace("マグニチュード", "magnitude")
                    .replace("最大震度", "maximum_intensity")
                    .replace("：", ": ")
                    .replace("[EEW]", "")
                    .replace("km", "")
                )

                for i in range(len(j)):
                    for m in re.finditer('2023/', j[i]["text"]):
                        jl = list(j[i]["text"])
                        jl[m.start() + 10] = "-"
                        j[i]["text"] = "".join(jl)

                    for m in re.finditer('2024/', j[i]["text"]):
                        jl = list(j[i]["text"])
                        jl[m.start() + 10] = "-"
                        j[i]["text"] = "".join(jl)

                    m = {key: value for key, value in zip(*[iter(j[i]["text"].replace(": ", " ").split())] * 2)}

                    ms.append(m)
                    print(m)
            except JSONDecodeError as _:
                pass

    df = gpd.GeoDataFrame.from_records(ms)

    df["long"] = df["long"].astype(float)
    df["lat"] = df["lat"].astype(float)
    df["magnitude"] = df["magnitude"].astype(float)
    df["epicenter_depth"] = df["epicenter_depth"].astype(float)

    df['geometry'] = gpd.points_from_xy(df['long'], df['lat'])
    df.set_geometry("geometry", inplace=True)
    df.set_crs("EPSG:4326")

    if to_file:
        df.to_file("earthquakes.gpkg")

    f.close()

    df = pd.DataFrame(df)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["timestamp"] = df["timestamp"].dt.round('1d')

    timestamp_data = df.groupby(by=["timestamp", "magnitude"])

    print(timestamp_data.head())

    mplot(timestamp_data["timestamp"], timestamp_data["maxmag"], color="orange", plot_type="line", grid="--")
