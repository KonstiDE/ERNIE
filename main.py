import os

from bertopic.vectorizers import OnlineCountVectorizer
from hdbscan import HDBSCAN
from umap import UMAP

from build_docs import build_docs
from process_docs import preprocess_docs, analyse_docs

from modeling.match_topics import match_topics_from_model
from modeling.label_topics import label_topics
from modeling.visualize_topic_over_time import visualize_topics

from language_dist import language_distribution

import config.config as cfg

if __name__ == '__main__':
    cfg.write_os_environments()

    # build_docs(fetching_chunk_size=16)
    # preprocess_docs(chunk_size=1000)
    # analyse_docs(
    #     BERT_key="davanstrien/chat_topics",
    #     umap_model=UMAP(),
    #     hdbscan_model=HDBSCAN(),
    #     vectorizer_model=OnlineCountVectorizer(ngram_range=(1, 1)),
    #     nr_topics=128
    # )

    # label_topics()
    # match_topics_from_model()
    # language_distribution()
    visualize_topics()
