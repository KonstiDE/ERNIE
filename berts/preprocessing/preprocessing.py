import re
import stopwordsiso

import pickle as pkl

from tqdm import tqdm
from nltk.tokenize import word_tokenize

call_emoji_free = lambda e: emoji_free_text(e)
call_url_free = lambda u: url_free_text(u)
call_hashtag_free = lambda h: hashtag_free_text(h)
call_hashtag_free_content = lambda hc: hashtag_free_text_content(hc)
call_at_free = lambda a: at_free_text(a)
call_at_free_content = lambda ac: at_free_text_content(ac)
call_punct_free = lambda p: punct_free_text(p)
call_digit_free = lambda d: digit_free_text(d)


def clean(
        df,
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
        stopwords_lang_codes=["en"],
        stopwords_custom=[],
        min_doc_length=5,
        duplicate_cleanup=True):

    if duplicates:
        df = df.drop_duplicates(subset="text")
        print("(1/10) Removed duplicates")
    else:
        print("(1/10) Skipped duplicates ")

    if emojis:
        df["text"] = df["text"].apply(call_emoji_free)
        print("(2/10) Removed Emojis")
    else:
        print("(2/10) Skipped Emojis")

    if urls:
        df["text"] = df["text"].apply(call_url_free)
        print("(3/10) Removed URLs")
    else:
        print("(3/10) Skipped URLs")

    if hashtags:
        if hashtags_content:
            df["text"] = df["text"].apply(call_hashtag_free_content)
        else:
            df["text"] = df["text"].apply(call_hashtag_free)

        print("(4/10) Removed Hashtags (Removed content: {})".format(hashtags_content))
    else:
        print("(4/10) Skipped Hashtags")

    if ats:
        if ats_content:
            df["text"] = df["text"].apply(at_free_text_content)
        else:
            df["text"] = df["text"].apply(at_free_text)

        print("(5/10) Removed @s (Removed content: {})".format(ats_content))
    else:
        print("(5/10) Skipped @s")

    if punctuation:
        df["text"] = df["text"].apply(call_punct_free)
        print("(6/10) Removed punctuation")
    else:
        print("(6/10) Skipped punctuation")

    if digits:
        df["text"] = df["text"].apply(call_digit_free)
        print("(7/10) Removed digits\n")
    else:
        print("(7/10) Skipped digits\n")

    if stopwords:
        documents_cleaned = []
        num_docs = len(df["text"].values.tolist())

        stopwords = list(stopwordsiso.stopwords(stopwords_lang_codes)) + stopwords_custom

        with tqdm(df["text"], total=num_docs) as t:
            for tweet in t:
                tokens = word_tokenize(tweet)
                tokens_cleaned = [word for word in tokens if word not in stopwords and len(set(word.lower())) > min_doc_length]

                tokens_cleaned_line = " ".join(tokens_cleaned)
                documents_cleaned.append(tokens_cleaned_line)

                t.set_postfix({"No stopswords": tokens_cleaned_line})

        df["cleaned_text"] = documents_cleaned
        print("(8/10) Removed stopwords and <= {} different characters (lower)".format(min_doc_length))
    else:
        print("(8/10) Skipped stopwords and min_doc_length")

    df = df[df["cleaned_text"] != ""]
    print("(9/10) Removed empties (default)")

    if duplicate_cleanup:
        df = df.drop_duplicates(subset="text")
        print("(10/10) Removed duplicates (after preprocessing)")
    else:
        print("(10/10) Skipped duplicates (after preprocessing)")

    return df


def emoji_free_text(text):
    regrex_pattern = re.compile(pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags=re.UNICODE
    )

    return regrex_pattern.sub(r'', text)


def url_free_text(text):
    return re.sub(r'https?:\/\/.*?', '', text)


def hashtag_free_text(text):
    return re.sub(r'#', '', text)


def hashtag_free_text_content(text):
    return re.sub(r'#\S+\b', '', text)


def at_free_text(text):
    return re.sub(r'@', '', text)


def at_free_text_content(text):
    return re.sub(r'@\S+\b', '', text)


def punct_free_text(text):
    return re.sub(r'[^\w\s]', '', re.sub(r'_', '', text))


def digit_free_text(text):
    return re.sub(r'[0-9]', '', text)


def save_preprocess(df):
    df = df[df["cleaned_text"].notna()]
    df.to_csv("preprocessed.csv")


def save_preprocessed_as_text(df):
    df = df[df["cleaned_text"].notna()]
    with open("preprocessed.txt", "w+") as f:
        for cleaned_line in df["cleaned_text"].values.tolist():
            f.write(cleaned_line + "\n")
