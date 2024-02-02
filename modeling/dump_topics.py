import os
import pandas as pd
import geopandas as gpd
import pickle as pkl

from shapely import Point

import config.config as cfg

from tqdm import tqdm


def dump_topics_to_gpkg(topic_to_filter=None):
    files = os.listdir(os.path.join(cfg.gdelt_out(), "../about/"))

    corrupted_files = 0

    loop = tqdm(files)

    document_map = []

    with open(os.path.join(cfg.base_path(), "custom_topics.pkl"), 'rb') as t:
        print("Loading custom topics...")
        topic_dictionary = pkl.load(t)

        c = 0
        for file in loop:
            with open(os.path.join(os.path.join(cfg.gdelt_out(), "../about/"), file), "rb") as f:
                try:
                    document = pkl.load(f)
                    f.close()

                    if document.topic_information is not None:
                        translated_topic = topic_dictionary[document.topic_information] if document.topic_information > 0 else "spam"
                        document_map.append({
                            "index": c,
                            "longitude": document.long,
                            "latitude": document.lat,
                            "topic": translated_topic,
                            "topic_index": document.topic_information
                        })


                except EOFError as _:
                    corrupted_files += 1
                    loop.set_postfix_str("Corrupted files: {}".format(corrupted_files))

            c += 1

    df = pd.DataFrame(document_map)

    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    gdf.to_file("topics.gpkg", driver="GPKG")
