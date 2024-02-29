import os

from bertopic.vectorizers import OnlineCountVectorizer
from hdbscan import HDBSCAN
from umap import UMAP

from sklearn.cluster import MiniBatchKMeans

import repair
from language_dist import language_distribution
from modeling.dump_topics import dump_gkg_to_gpkg
from modeling.match_topics import match_topics_from_model
from modeling.visualize_topic_over_time import visualize_topics
from read_doc_test import doc_test_read

import config.config as cfg

from build_docs import build_docs

from process_docs import preprocess_docs, analyse_docs

if __name__ == '__main__':
    cfg.write_os_environments()

    # Data acquisition and preprocessing
    # build_docs(fetching_chunk_size=256, global_knowledge_graph_format=True)
    # preprocess_docs(chunk_size=10000, digits=False)
    #
    # Topic Modeling
    # analyse_docs(
    #     umap_model=UMAP(n_neighbors=15, n_components=3, metric="cosine"),
    #     hdbscan_model=MiniBatchKMeans(n_clusters=64),
    #     vectorizer_model=OnlineCountVectorizer(ngram_range=(1, 1)),
    #     nr_topics=64,
    #     n_gram_range=(1, 1)
    # )
    # label_topics()
    # match_topics_from_model()
    # language_distribution()
    # visualize_topics()
    dump_gkg_to_gpkg()

    # Analysis
    # doc_test_read()

