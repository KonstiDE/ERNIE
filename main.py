import os

from bertopic.vectorizers import OnlineCountVectorizer
from hdbscan import HDBSCAN
from umap import UMAP

from build_docs import build_docs
from process_docs import preprocess_docs, analyse_docs

if __name__ == '__main__':
    default_n_threads = 1
    os.environ['OPENBLAS_NUM_THREADS'] = f"{default_n_threads}"
    os.environ['MKL_NUM_THREADS'] = f"{default_n_threads}"
    os.environ['OMP_NUM_THREADS'] = f"{default_n_threads}"

    os.environ["CUDA_VISIBLE_DEVICES"] = "MIG-f29aed64-88d8-567c-9102-1b0a7b4e0b3a"

    # build_docs(fetching_chunk_size=16)
    # preprocess_docs(chunk_size=1000)
    analyse_docs(
        BERT_key="davanstrien/chat_topics",
        umap_model=UMAP(),
        hdbscan_model=HDBSCAN(),
        vectorizer_model=OnlineCountVectorizer(ngram_range=(1, 1)),
        nr_topics=10
    )
