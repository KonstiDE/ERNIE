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

    print("Building Dataframe in batches of 10000 docs...")
    documents = os.listdir(cfg.gdelt_out())

    file_chunks = [documents[i:i + 100000] for i in range(0, len(documents), 100000)]

    df = None

    docs = {}

    for file_chunk in file_chunks:
        loop = tqdm(file_chunk)

        for doc_file in loop:
            with open(os.path.join(cfg.gdelt_out(), doc_file), "rb") as d:
                document = pkl.load(d)

                if document.main_content_present():
                    try:
                        lang_code = Detector(document.main_content[:10000], quiet=True).language.code

                        if lang_code not in docs.keys():
                            docs[lang_code] = 1
                        else:
                            docs[lang_code] = docs[lang_code] + 1
                    except Warning as _:
                        pass
                    #docs.append(document)

            d.close()

        #chunk_df = pd.DataFrame([vars(doc) for doc in docs])

        #if df is None:
        #    df = chunk_df
        #else:
        #    df = pd.concat([df, chunk_df], ignore_index=True)

        #docs = None
    print(docs)

    lang_dist = {'ja': 943685, 'en': 284204, 'id': 4268, 'zh_Hant': 21092, 'ru': 4288, 'de': 957, 'hi': 24558, 'zh': 23150,
     'ar': 7230, 'ko': 10457, 'es': 8074, 'ta': 189, 'pt': 2397, 'hu': 320, 'da': 75, 'it': 2594, 'fr': 3144, 'ro': 685,
     'th': 2032, 'no': 166, 'pl': 306, 'sq': 46, 'bg': 532, 'iw': 1279, 'el': 941, 'tr': 645, 'nl': 436, 'mk': 93,
     'uk': 523, 'kk': 13, 'sr': 263, 'ur': 98, 'mn': 288, 'lt': 189, 'cs': 138, 'hr': 199, 'vo': 22, 'gl': 24, 'sv': 50,
     'fi': 52, 'ml': 75, 'bn': 93, 'te': 9, 'fa': 126, 'ba': 14, 'lv': 25, 'crs': 23, 'hy': 26, 'vi': 74, 'mr': 37,
     'sl': 31, 'et': 2, 'un': 31, 'ms': 3, 'ca': 19, 'sk': 14, 'az': 5, 'is': 4, 'tt': 2, 'zzp': 1, 'pa': 3, 'nn': 1}

    exit(11)

    os.environ["CUDA_VISIBLE_DEVICES"] = "MIG-f29aed64-88d8-567c-9102-1b0a7b4e0b3a"

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

    os.environ["CUDA_VISIBLE_DEVICES"] = "MIG-f29aed64-88d8-567c-9102-1b0a7b4e0b3a"

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
    #     river_conf={"chunk_size": 1000},
    #     nr_topics=10,
    #     umap_model=UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine'),
    #     hdbscan_model=MiniBatchKMeans(n_clusters=10),
    #     vectorizer_model=OnlineCountVectorizer(ngram_range=(1, 1))
    # )
