import json
import os
from json import JSONDecodeError

import config.config as cfg

import geopandas as gpd

import shutup
shutup.please()

def analyse_earthquakes():
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
                    ji = j[i]["text"].index("2023/")
                    jl = list(j[i]["text"])
                    jl[ji + 10] = "-"
                    j[i]["text"] = "".join(jl)

                    m = {key: value for key, value in zip(*[iter(j[i]["text"].replace(": ", " ").split())] * 2)}

                    ms.append(m)
            except JSONDecodeError as _:
                pass

    df = gpd.GeoDataFrame.from_records(ms)

    df["long"] = df["long"].astype(float)
    df["lat"] = df["lat"].astype(float)
    df["magnitude"] = df["magnitude"].astype(float)
    df["epicenter_depth"] = df["epicenter_depth"].astype(float)

    df['geometry'] = gpd.points_from_xy(df['long'], df['lat'])
    df.set_geometry("geometry")
    df.set_crs("EPSG:4326")

    df.to_file("shape.gpkg")

    f.close()
