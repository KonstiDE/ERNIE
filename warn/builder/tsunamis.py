import json
import os
import re

from json import JSONDecodeError

import config.config as cfg

import geopandas as gpd

def analyse_tsunamis():
    files = os.listdir(cfg.warn_path_tsunamis())

    ms = []

    for file in files:
        with open(os.path.join(cfg.warn_path_tsunamis(), file)) as f:
            try:
                j = json.loads(
                    f.read()
                    .replace("経度", "long")
                    .replace("緯度", "lat")
                    .replace("震源地", "epicenter_loc")
                    .replace("深さ", "depth")
                    .replace("発表:", "timestamp_announcement:")
                    .replace("発生", "timestamp_occurence")
                    .replace("マグニチュード", "magnitude")
                    .replace("最大", "largest")
                    .replace("形態", "figure")
                    .replace("：", ": ")
                    .replace("km", "")
                    .replace("[JISHIN]", "")
                    .replace("ごく浅い", "2")
                    .replace("不明", "-1")
                    .replace("弱", "")
                )

                for i in range(len(j)):
                    for m in re.finditer('2023/', j[i]["text"]):
                        jl = list(j[i]["text"])
                        jl[m.start() + 10] = "-"
                        j[i]["text"] = "".join(jl)

                    m = {key: value for key, value in zip(*[iter(j[i]["text"].replace(": ", " ").split())] * 2)}

                    ms.append(m)
            except JSONDecodeError as _:
                pass

    df = gpd.GeoDataFrame.from_records(ms)

    df["long"] = df["long"].astype(float)
    df["lat"] = df["lat"].astype(float)
    df["depth"] = df["depth"].astype(float)
    df["magnitude"] = df["magnitude"].astype(float)
    df["largest"] = df["largest"].astype(float)

    df['geometry'] = gpd.points_from_xy(df['long'], df['lat'])
    df.set_geometry("geometry")
    df.set_crs("EPSG:4326")

    df.to_file("tsunamis.gpkg")

    f.close()
