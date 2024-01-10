import os
import pickle as pkl
from typing import Any

import pandas as pd
from bertopic.representation import BaseRepresentation
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from umap import UMAP

import config.config as cfg

from berts.defaultBERT import (
    analyse_bert
)
from preprocessing.preprocessing import clean, save_preprocessed_as_text


def preprocess_docs(
        duplicates=True,
        emojis=True,
        urls=True,
        hashtags=True,
        hashtags_content=True,
        ats=True,
        ats_content=True,
        punctuation=True,
        digits=True,
        stopwords=True,
        stopwords_lang_codes=None,
        stopwords_custom=None,
        min_doc_length=5,
        duplicate_cleanup=True):

    if stopwords_custom is None:
        stopwords_custom = []
    if stopwords_lang_codes is None:
        stopwords_lang_codes = ["en"]
    documents = os.listdir(cfg.gdelt_out_path_about())

    docs = []

    for doc_file in documents:
        with open(os.path.join(cfg.gdelt_out_path_about(), doc_file), "rb") as d:
            document = pkl.load(d)

            if document.main_content_present():
                docs.append(document)

    df = pd.DataFrame([vars(doc) for doc in docs])

    if not os.path.isfile("preprocessed.txt"):
        cleaned_df = clean(df,
                        duplicates=duplicates,
                        emojis=emojis,
                        urls=urls,
                        hashtags=hashtags,
                        hashtags_content=hashtags_content,
                        ats=ats,
                        ats_content=ats_content,
                        punctuation=punctuation,
                        digits=digits,
                        stopwords=stopwords,
                        stopwords_lang_codes=stopwords_lang_codes,
                        stopwords_custom=stopwords_custom,
                        min_doc_length=min_doc_length,
                        duplicate_cleanup=duplicate_cleanup)
        save_preprocessed_as_text(cleaned_df)


def analyse_docs(
        BERT_key="default",
        river_app=False,
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

    if BERT_key == "default":
        analyse_bert(
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
            verbose=verbose)


if __name__ == '__main__':
    analyse_docs()
