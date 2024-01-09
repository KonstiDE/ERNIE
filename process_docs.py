import os
import pickle as pkl
import pandas as pd

import config.config as cfg

from berts.defaultBERT import init_bert


def process_docs():
    documents = os.listdir(cfg.gdelt_out_path_about())

    docs = []

    for doc_file in documents:
        with open(os.path.join(cfg.gdelt_out_path_about(), doc_file), "rb") as d:
            document = pkl.load(d)

            if document.main_content_present():
                docs.append(document)

    df = pd.DataFrame([vars(doc) for doc in docs])

    init_bert(df)


if __name__ == '__main__':
    process_docs()
