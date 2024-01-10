import os.path
from typing import Any

import numpy as np

from bertopic import BERTopic
from bertopic.representation import BaseRepresentation
from bertopic.vectorizers import OnlineCountVectorizer

from hdbscan import HDBSCAN

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from umap import UMAP

def read_text(path: str):
    with open(path, "r") as f:
        lines = f.readlines()
        line_no_break = []

        for line in lines:
            line_no_break.append(line.replace("\n", ""))

        return line_no_break

def analyse(preprocessed_file,
            river_app=False,
            river_conf=None,
            language: str = "english",
            top_n_words: int = 10,
            n_gram_range: tuple[int, int] = (1, 1),
            min_topic_size: int = 10,
            nr_topics: int | str | None = None,
            low_memory: bool = False,
            calculate_probabilities: bool = False,
            seed_topic_list: list[list[str]] | None = None,
            zeroshot_topic_list: list[str] | None = None,
            zeroshot_min_similarity: float = .7,
            embedding_model: Any = None,
            umap_model: UMAP | None = None,
            hdbscan_model: HDBSCAN | None = None,
            vectorizer_model: CountVectorizer | None = None,
            ctfidf_model: TfidfTransformer | None = None,
            representation_model: BaseRepresentation | None = None,
            verbose: bool = False):

    if river_conf is None:
        river_conf = {"chunk_size": 10}

    try:
        river_chunk = river_conf["chunk_size"]
    except KeyError as ke:
        raise Exception("Please provide the argument \"chunk_size: number\" in your river_conf map.")

    cleaned_texts = read_text(preprocessed_file)

    topic_model = BERTopic(
        language=language,
        top_n_words=top_n_words,
        n_gram_range=n_gram_range,
        min_topic_size=min_topic_size,
        nr_topics=nr_topics,
        low_memory=low_memory,
        calculate_probabilities=calculate_probabilities,
        seed_topic_list=seed_topic_list,
        zeroshot_topic_list=zeroshot_topic_list,
        zeroshot_min_similarity=zeroshot_min_similarity,
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        ctfidf_model=ctfidf_model,
        representation_model=representation_model,
        verbose=verbose)

    if river_app:
        doc_chunks = [cleaned_texts[i:i + river_chunk] for i in range(0, len(cleaned_texts), river_chunk)]

        topic_collection = []
        c = 0
        for docs in doc_chunks:
            topic_model.partial_fit(docs)
            topic_collection.extend(topic_model.topics_)
            c += river_chunk
            print("Embedded and transformed " + str(c) + " docs")

        topics, probs = topic_model.transform(cleaned_texts)

    else:
        topics, probs = topic_model.fit_transform(cleaned_texts)

    print(topics)
    print(probs)

    print(topic_model.get_topic_info())

    topic_model.save("model", save_embedding_model=False)


def analyse_bert(river_app=False,
        river_conf=None,
        language: str = "english",
        top_n_words: int = 10,
        n_gram_range: tuple[int, int] = (1, 1),
        min_topic_size: int = 10,
        nr_topics: int | str | None = None,
        low_memory: bool = False,
        calculate_probabilities: bool = False,
        seed_topic_list: list[list[str]] | None = None,
        zeroshot_topic_list: list[str] | None = None,
        zeroshot_min_similarity: float = .7,
        embedding_model: Any = None,
        umap_model: UMAP | None = None,
        hdbscan_model: HDBSCAN | None = None,
        vectorizer_model: CountVectorizer | None = None,
        ctfidf_model: TfidfTransformer | None = None,
        representation_model: BaseRepresentation | None = None,
        verbose: bool = False):

    os.environ["CUDA_VISIBLE_DEVICES"] = "MIG-f29aed64-88d8-567c-9102-1b0a7b4e0b3a"

    analyse(
        "preprocessed.txt",
        river_app=river_app,
        river_conf=river_conf,
        language=language,
        top_n_words=top_n_words,
        n_gram_range=n_gram_range,
        min_topic_size=min_topic_size,
        nr_topics=nr_topics,
        low_memory=low_memory,
        calculate_probabilities=calculate_probabilities,
        seed_topic_list=seed_topic_list,
        zeroshot_topic_list=zeroshot_topic_list,
        zeroshot_min_similarity=zeroshot_min_similarity,
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        ctfidf_model=ctfidf_model,
        representation_model=representation_model,
        verbose=verbose
    )






