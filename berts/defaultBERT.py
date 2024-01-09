import os

from preprocessing.preprocessing import (
    clean,
    save_preprocessed_as_text
)

def init_bert(doc_df):
    cleaned_df = clean(doc_df)
    save_preprocessed_as_text(cleaned_df)


