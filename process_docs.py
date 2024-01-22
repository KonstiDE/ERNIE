import os
import pickle as pkl
from typing import Any



import pandas as pd
from bertopic.representation import BaseRepresentation
from bertopic.vectorizers import OnlineCountVectorizer
from hdbscan import HDBSCAN
from polyglot.detect import Detector
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from tqdm import tqdm
from umap import UMAP
import shutup

import config.config as cfg

from berts.defaultBERT import (
    analyse_bert
)
from preprocessing.preprocessing import clean, save_preprocessed_as_text

shutup.please()


def preprocess_docs(
        chunk_size=100000,
        duplicates=True,
        emojis=False,
        urls=True,
        hashtags=True,
        hashtags_content=True,
        ats=True,
        ats_content=True,
        punctuation=True,
        digits=False,
        stopwords=True,
        stopwords_lang_codes=None,
        stopwords_custom=None,
        min_doc_length=5,
        duplicate_cleanup=True):

    if stopwords_custom is None:
        stopwords_custom = []
    if stopwords_lang_codes is None:
        stopwords_lang_codes = ["en"]

    if os.path.isfile("preprocessed.txt"):
        reply = input("There is already a preprocessed file, do you wnt to delete it? (y/n)")

        if reply == "y":
            os.remove("preprocessed.txt")
            print("Deleted preprocessed.txt")

    print("Building Dataframe in batches of {} docs...".format(chunk_size))
    documents = os.listdir(cfg.gdelt_out())

    file_chunks = [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]

    c = 1
    for file_chunk in file_chunks:
        print("-"*16)
        print("Batch {} of {}".format(c, len(file_chunks)))
        print("-" * 16)
        loop = tqdm(file_chunk)

        docs = []

        for doc_file in loop:
            with open(os.path.join(cfg.gdelt_out(), doc_file), "rb") as d:
                document = pkl.load(d)

                if document.main_content_present():
                    docs.append(document)

            d.close()

        chunk_df = pd.DataFrame([vars(doc) for doc in docs])

        cleaned_df = clean(chunk_df,
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

        print("Applying cleaned text to chunk of documents...")
        i = 0
        for row in cleaned_df.rows:
            docs[i].cleaned_content = row["cleaned_content"]
            i += 1

        save_preprocessed_as_text(cleaned_df)
        c += 1


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
    preprocess_docs()
    # analyse_docs(
    #     river_app=False,
    #     river_conf={"chunk_size": 10000},
    #     nr_topics=200,
    #     umap_model=UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine'),
    #     hdbscan_model=HDBSCAN(),
    #     vectorizer_model=OnlineCountVectorizer(ngram_range=(1, 1))
    # )
