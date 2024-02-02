import os
import pickle as pkl

import pandas as pd
from tqdm import tqdm

import config.config as cfg

from datetime import datetime

from plotting.wrapper import wrap_plot as plot


def visualize_topics(chunk_size=100000):
    with open(os.path.join(cfg.base_path(), "custom_topics.pkl"), "rb") as t:
        custom_topics = pkl.load(t)

        dfs = []

        documents = os.listdir(os.path.join(cfg.gdelt_out(), "../about/"))

        file_chunks = [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]

        c = 1
        for file_chunk in file_chunks:
            print("-" * 16)
            print("Batch {} of {}".format(c, len(file_chunks)))
            print("-" * 16)
            loop = tqdm(file_chunk)

            docs = []

            corrupted_files = 0

            for doc_file in loop:
                with open(os.path.join(os.path.join(cfg.gdelt_out(), "../about/"), doc_file), "rb") as d:
                    try:
                        document = pkl.load(d)

                        if document.topic_information is not None:
                            # Only temporary attribute change, do not mess with the file!!
                            document.topic_information = "spam" if int(document.topic_information) < 0 else custom_topics[document.topic_information]

                            docs.append(document)

                    except EOFError as _:
                        corrupted_files += 1
                        loop.set_postfix_str("Corrupted files: {}".format(corrupted_files))

                    d.close()

            chunk_df = pd.DataFrame([vars(doc) for doc in docs])
            dfs.append(chunk_df)

            c += 1

        df = pd.concat(dfs)

        df["src_file"] = df["src_file"].str.replace("_1d", "")
        df["src_file"] = pd.to_datetime(df["src_file"], format="%Y-%m-%d_%H-%M-%S")
        df["src_file"] = df["src_file"].dt.round('1d')

        while True:
            print(set(custom_topics.values()))
            topic = input("Which topic to you want to plot over time?")

            group_holidays = df.groupby(by="src_file")["topic_information"].apply(
                lambda x: (x == topic).sum()).reset_index(
                name="count")
            plot(group_holidays["src_file"], group_holidays["count"], plot_type="line",
                 color="orange", legend=True, legenddata=["Topic \"{}\"".format(topic)],
                 vertical_line_date=datetime(2023, 9, 15))
