import os
import pickle as pkl
from typing import Any

import pandas as pd
from bertopic.representation import BaseRepresentation
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from tqdm import tqdm
from umap import UMAP
import shutup

import config.config as cfg

from berts.configurableBERT import analyse_bert as fresh_bert
from berts.ultrafastBERT import analyse_bert as pre_bert

from preprocessing.preprocessing import clean, save_preprocessed_as_text

shutup.please()


def preprocess_docs(
        chunk_size=100,
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
        files = []

        corrupted_files = 0

        for doc_file in loop:
            with open(os.path.join(cfg.gdelt_out(), doc_file), "rb") as d:
                try:
                    document = pkl.load(d)

                    if document.main_content_present():
                        docs.append(document)
                        files.append(doc_file)

                except EOFError as _:
                    corrupted_files += 1
                    loop.set_postfix_str("Corrupted files: {}".format(corrupted_files))

            d.close()

        chunk_df = pd.DataFrame([vars(doc) for doc in docs])
        chunk_df["filename"] = files

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
        for filename, cleaned_content in zip(
                cleaned_df["filename"].values.tolist(), cleaned_df["main_content"].values.tolist()
        ):
            with open(os.path.join(cfg.gdelt_out(), filename), "rb") as d:
                document = pkl.load(d)
                d.close()
                document.set_cleaned_content(cleaned_content)

        print("Done, now saving to preprocessing file...")
        save_preprocessed_as_text(cleaned_df)
        c += 1



def analyse_docs(
        BERT_key=None,
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
        verbose: bool = True):

    fresh_bert(
        pretrained_model=BERT_key,
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
    pass
