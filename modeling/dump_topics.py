import os
import pandas as pd
import geopandas as gpd
import pickle as pkl

from shapely import Point

import config.config as cfg

from tqdm import tqdm


def dump_gkg_to_gpkg():
    files = os.listdir(cfg.gdelt_out())

    corrupted_files = 0

    loop = tqdm(files)

    document_map = []

    for c, file in enumerate(loop):
        with open(os.path.join(os.path.join(cfg.gdelt_out()), file), "rb") as f:
            try:
                document = pkl.load(f)
                f.close()

                if document.topic_information is not None and \
                        document.locations is not None and \
                        document.source_name is not None and \
                        document.themes is not None and \
                        str(document.themes[0:3]).__contains__("NATURAL_DISASTER_") and \
                        document.url is not None:
                    if len(document.locations) > 0:
                        location_split = document.locations[0].split("#")
                        domain = document.source_name.split(".")[-1]

                        international_domains = ["com", "net", "org", "eu", "info", "lat", "cat"]

                        if location_split[2] == "JA":
                            try:
                                document_map.append({
                                    "fid": c,
                                    "date": document.date,
                                    "url": document.url,
                                    "src_country": document.source_name if domain in international_domains else domain,
                                    "src_domain": document.source_name,
                                    "target_country": location_split[2],
                                    "latitude": float(location_split[5]),
                                    "longitude": float(location_split[6]),
                                    "topic": document.topic_information,
                                    "trace_file": document.src_file,
                                    "trace_line": document.src_line
                                })
                            except ValueError as _:
                                pass


            except EOFError as _:
                corrupted_files += 1
                loop.set_postfix_str("Corrupted files: {}".format(corrupted_files))

    df = pd.DataFrame(document_map)

    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    gdf.to_file("disasters_url.gpkg", driver="GPKG")
