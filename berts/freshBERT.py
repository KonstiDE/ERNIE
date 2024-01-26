import os.path
from typing import Any

import numpy as np
import scipy.sparse
from tqdm import tqdm

import pickle as pkl

import config.config as cfg

from berts.helper.bert_helper import read_text

from bertopic import BERTopic
from bertopic.representation import BaseRepresentation
from bertopic.vectorizers import OnlineCountVectorizer

from hdbscan import HDBSCAN

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from umap import UMAP

import shutup
shutup.please()


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

    print("Checking Arguments...")
    if river_conf is None:
        river_conf = {"chunk_size": 1000}

    try:
        river_chunk = river_conf["chunk_size"]
    except KeyError as ke:
        raise Exception("Please provide the argument \"chunk_size: number\" in your river_conf map.")

    print("Reading text...")
    file_names, cleaned_texts = read_text(preprocessed_file)

    print("Initializing model")
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

    print("Strarting embedding process")
    if river_app:
        doc_chunks = [cleaned_texts[i:i + river_chunk] for i in range(0, len(cleaned_texts), river_chunk)]

        topic_collection = []
        c = 0
        for docs in doc_chunks:
            try:
                print("Embedding the next " + str(river_chunk) + " docs...")
                topic_model.partial_fit(docs)
            except scipy.sparse.SparseEfficiencyWarning as sew:
                pass

            topic_collection.extend(topic_model.topics_)
            c += river_chunk
            print("Embedded " + str(c) + " docs.")

        print("Transforming now...")
        topics, probs = topic_model.transform(cleaned_texts)

    else:
        print("Attempting to embed {} documents...".format(len(cleaned_texts)))
        topics, probs = topic_model.fit_transform(cleaned_texts)

    print(topics)
    print(probs)

    print(topic_model.get_topic_info())

    topic_model.save("model", save_embedding_model=False)

    print("Applying topics to documents (in batches if > 100.000 docs)... This could take a while.")
    file_chunks = [file_names[i:i + 100000] for i in range(0, len(file_names), 100000)]

    c = 1
    for file_chunk in file_chunks:
        print("-" * 16)
        print("Batch {} of {}".format(c, len(file_chunks)))
        print("-" * 16)

        print("Applying...")

        for doc_file, topic in zip(file_chunk, topics):
            with open(os.path.join(cfg.gdelt_out(), doc_file), "rb") as d:
                document = pkl.load(d)
                d.close()
                document.set_topic(topic)

        c += 1


def analyse_bert(river_app=False,
                 river_conf=None,
                 language: str = "multilingual",
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
