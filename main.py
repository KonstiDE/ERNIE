from bertopic.vectorizers import OnlineCountVectorizer
from hdbscan import HDBSCAN
from umap import UMAP

import repair
from read_doc_test import doc_test_read

import config.config as cfg

from build_docs import build_docs

from process_docs import preprocess_docs, analyse_docs

if __name__ == '__main__':
    cfg.write_os_environments()

    # Data acquisition and preprocessing
    build_docs(fetching_chunk_size=16)
    # preprocess_docs(chunk_size=1000)
    #
    # Topic Modeling
    # analyse_docs(
    #     umap_model=UMAP(),
    #     hdbscan_model=HDBSCAN(),
    #     vectorizer_model=OnlineCountVectorizer(ngram_range=(1, 1)),
    #     nr_topics=10
    # )
    # label_topics()
    # match_topics_from_model()
    # language_distribution()
    # visualize_topics()
    # dump_topics_to_gpkg()

    # Analysis
    # doc_test_read()

