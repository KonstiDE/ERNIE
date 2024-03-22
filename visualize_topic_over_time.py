import os
import pickle as pkl
import sys

import pandas as pd
from tqdm import tqdm

from plotting.wrapper import wrap_plot as plot

import models


def visualize_topics(chunk_size=100000):
    with open(os.path.join("custom_topics.pkl"), "rb") as t:
        custom_topics = pkl.load(t)

        dfs = []

        documents = os.listdir("data/out/noto")

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
                with open(os.path.join("data/out/noto", doc_file), "rb") as d:
                    try:
                        document = pkl.load(d)

                        if document.topic_information is not None:
                            docs.append(document)

                    except EOFError as _:
                        corrupted_files += 1
                        loop.set_postfix_str("Corrupted files: {}".format(corrupted_files))

                    d.close()

            chunk_df = pd.DataFrame([vars(doc) for doc in docs])
            dfs.append(chunk_df)

            c += 1

        df = pd.concat(dfs)

        df["date"] = pd.to_datetime(df["date"], format="%Y%m%d%H%M%S")
        df["date"] = df["date"].dt.round('1d')

        while True:
            print(set(custom_topics.values()))
            topic = input("Which topic to you want to plot over time?")

            group_holidays = df.groupby(by="src_file")["topic_information"].apply(
                lambda x: (x == topic).sum()).reset_index(
                name="count")
            plot(group_holidays["src_file"], group_holidays["count"], plot_type="line",
                 color="orange", legend=True, legenddata=["Topic \"{}\"".format(topic)])


if __name__ == '__main__':
    visualize_topics()
