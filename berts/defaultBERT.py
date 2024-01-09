import os.path

import numpy as np

from bertopic import BERTopic
from bertopic.vectorizers import OnlineCountVectorizer

from hdbscan import HDBSCAN

from sklearn.cluster import MiniBatchKMeans

from umap import UMAP

from preprocessing.preprocessing import (
    clean,
    save_preprocessed_as_text
)

def read_text(path: str):
    with open(path, "r") as f:
        lines = f.readlines()
        line_no_break = []

        for line in lines:
            line_no_break.append(line.replace("\n", ""))

        return line_no_break

def analyse(preprocessed_file):
    cleaned_texts = read_text(preprocessed_file)

    river_chunk = 10
    num_topics = 10

    doc_chunks = [cleaned_texts[i:i + river_chunk] for i in range(0, len(cleaned_texts), river_chunk)]

    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')
    cluster_model = MiniBatchKMeans(n_clusters=num_topics)
    vectorizer_model = OnlineCountVectorizer(ngram_range=(1, 1))
    # hdbscan_model = HDBSCAN()

    # Prepare model
    topic_model = BERTopic(
        embedding_model="all-MiniLM-L6-v2",
        verbose=True,
        umap_model=umap_model,
        hdbscan_model=cluster_model,
        vectorizer_model=vectorizer_model
    )

    c = 0
    topics = []
    for docs in doc_chunks:
        topic_model.partial_fit(docs)
        c += river_chunk
        topics.extend(topic_model.topics_)
        print("Embedded " + str(c) + " docs")

    print(topic_model.get_topic_info())

    topic_model.topics_ = topics
    topic_model.save("model", save_embedding_model=False)


def init_bert(doc_df):
    os.environ["CUDA_VISIBLE_DEVICES"] = "MIG-f29aed64-88d8-567c-9102-1b0a7b4e0b3a"

    if not os.path.isfile("preprocessed.txt"):
        cleaned_df = clean(doc_df)
        save_preprocessed_as_text(cleaned_df)

    analyse("preprocessed.txt")






