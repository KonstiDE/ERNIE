import re

import JapaneseTokenizer
import stopwordsiso
import jieba
import torch.cuda

from polyglot.detect import Detector
from konlpy.tag import Kkma
from transformers import pipeline

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-ja-en")

from transformers import MarianMTModel, MarianTokenizer

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(device)

tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ja-en")
model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-ja-en")
model.to(device)

from tqdm import tqdm


call_emoji_free = lambda e: emoji_free_text(e)
call_url_free = lambda u: url_free_text(u)
call_hashtag_free = lambda h: hashtag_free_text(h)
call_hashtag_free_content = lambda hc: hashtag_free_text_content(hc)
call_at_free = lambda a: at_free_text(a)
call_at_free_content = lambda ac: at_free_text_content(ac)
call_punct_free = lambda p: punct_free_text(p)
call_digit_free = lambda d: digit_free_text(d)

whitespace_exp = re.compile(r'\w+')
#mecab_wrapper = JapaneseTokenizer.KyteaWrapper()
#kkma = Kkma()


def clean(
        df,
        duplicates=True,
        emojis=False,
        urls=True,
        hashtags=True,
        hashtags_content=True,
        ats=True,
        ats_content=True,
        punctuation=True,
        digits=True,
        stopwords=True,
        stopwords_lang_codes=[],
        stopwords_custom=[],
        min_doc_length=5,
        duplicate_cleanup=True):

    if duplicates:
        df = df.drop_duplicates(subset="main_content")
        print("(1/10) Removed duplicates")
    else:
        print("(1/10) Skipped duplicates ")

    if emojis:
        df["main_content"].apply(call_emoji_free)
        print("(2/10) Removed Emojis\n")
    else:
        print("(2/10) Skipped Emojis\n")

    if stopwords:
        stopwords = list(stopwordsiso.stopwords(["en"])) + stopwords_custom

        documents_cleaned = []
        num_docs = len(df["main_content"].values.tolist())

        with tqdm(df["main_content"], total=num_docs) as t:
            for doc_text in t:
                doc_text_chunks = [doc_text[i:i + 512] for i in range(0, len(doc_text), 512)]

                complete = []

                for doc_text_chunk in doc_text_chunks:
                    tokens = tokenizer(doc_text_chunk, return_tensors="pt")
                    tokens = {key: value.to(device) for key, value in tokens.items()}
                    translation_ids = model.generate(**tokens)
                    translation_ids = translation_ids.to("cpu")
                    tokens = tokenizer.batch_decode(
                        translation_ids[0],
                        skip_special_tokens=True,
                        clean_up_tokenization_spaces=False
                    )

                    tokens_cleaned = [word for word in tokens if word not in stopwords]
                    tokens_cleaned = " ".join(tokens_cleaned)
                    complete.append(tokens_cleaned)

        df["main_content"] = documents_cleaned
        print("(3/10) Removed stopwords")
    else:
        print("(3/10) Skipped stopwords")

    if urls:
        df["main_content"].apply(call_url_free)
        print("(4/10) Removed URLs")
    else:
        print("(4/10) Skipped URLs")

    if hashtags:
        if hashtags_content:
            df["main_content"].apply(call_hashtag_free_content)
        else:
            df["main_content"].apply(call_hashtag_free)

        print("(5/10) Removed Hashtags (Removed content: {})".format(hashtags_content))
    else:
        print("(5/10) Skipped Hashtags")

    if ats:
        if ats_content:
            df["main_content"].apply(at_free_text_content)
        else:
            df["main_content"].apply(at_free_text)

        print("(6/10) Removed @s (Removed content: {})".format(ats_content))
    else:
        print("(6/10) Skipped @s")

    if punctuation:
        df["main_content"].apply(call_punct_free)
        print("(7/10) Removed punctuation")
    else:
        print("(7/10) Skipped punctuation")

    if digits:
        df["main_content"].apply(call_digit_free)
        print("(8/10) Removed digits")
    else:
        print("(8/10) Skipped digits")

    df = df[df["main_content"] != ""]
    print("(9/10) Removed empties (default)")

    if duplicate_cleanup:
        df = df.drop_duplicates(subset="main_content")
        print("(10/10) Removed duplicates (after preprocessing)")
    else:
        print("(10/10) Skipped duplicates (after preprocessing)")

    return df


def emoji_free_text(text):
    emoji_pattern = re.compile(
        "[\U0001F3FB-\U0001F3FF * # \U0001F600 \U0001F603 \U0001F604 \U0001F601 \U0001F606 \U0001F605 \U0001F923 \U0001F602 \U0001F642 \U0001F643 \U0001FAE0 \U0001F609 \U0001F60A \U0001F607 \U0001F970 \U0001F60D \U0001F929 \U0001F618 \U0001F617 \u263A \U0001F61A \U0001F619 \U0001F972 \U0001F60B \U0001F61B \U0001F61C \U0001F92A \U0001F61D \U0001F911 \U0001F917 \U0001F92D \U0001FAE2 \U0001FAE3 \U0001F92B \U0001F914 \U0001FAE1 \U0001F910 \U0001F928 \U0001F610 \U0001F611 \U0001F636 \U0001FAE5 \U0001F60F \U0001F612 \U0001F644 \U0001F62C \U0001F925 \U0001FAE8 \U0001F60C \U0001F614 \U0001F62A \U0001F924 \U0001F634 \U0001F637 \U0001F912 \U0001F915 \U0001F922 \U0001F92E \U0001F927 \U0001F975 \U0001F976 \U0001F974 \U0001F635 \U0001F92F \U0001F920 \U0001F973 \U0001F978 \U0001F60E \U0001F913 \U0001F9D0 \U0001F615 \U0001FAE4 \U0001F61F \U0001F641 \u2639 \U0001F62E \U0001F62F \U0001F632 \U0001F633 \U0001F97A \U0001F979 \U0001F626-\U0001F628 \U0001F630 \U0001F625 \U0001F622 \U0001F62D \U0001F631 \U0001F616 \U0001F623 \U0001F61E \U0001F613 \U0001F629 \U0001F62B \U0001F971 \U0001F624 \U0001F621 \U0001F620 \U0001F92C \U0001F608 \U0001F47F \U0001F480 \u2620 \U0001F4A9 \U0001F921 \U0001F479-\U0001F47B \U0001F47D \U0001F47E \U0001F916 \U0001F63A \U0001F638 \U0001F639 \U0001F63B-\U0001F63D \U0001F640 \U0001F63F \U0001F63E \U0001F648-\U0001F64A \U0001F48C \U0001F498 \U0001F49D \U0001F496 \U0001F497 \U0001F493 \U0001F49E \U0001F495 \U0001F49F \u2763 \U0001F494 \u2764 \U0001FA77 \U0001F9E1 \U0001F49B \U0001F49A \U0001F499 \U0001FA75 \U0001F49C \U0001F90E \U0001F5A4 \U0001FA76 \U0001F90D \U0001F48B \U0001F4AF \U0001F4A2 \U0001F4A5 \U0001F4AB \U0001F4A6 \U0001F4A8 \U0001F573 \U0001F4AC \U0001F5E8 \U0001F5EF \U0001F4AD \U0001F4A4 \U0001F44B \U0001F91A \U0001F590 \u270B \U0001F596 \U0001FAF1-\U0001FAF4 \U0001FAF7 \U0001FAF8 \U0001F44C \U0001F90C \U0001F90F \u270C \U0001F91E \U0001FAF0 \U0001F91F \U0001F918 \U0001F919 \U0001F448 \U0001F449 \U0001F446 \U0001F595 \U0001F447 \u261D \U0001FAF5 \U0001F44D \U0001F44E \u270A \U0001F44A \U0001F91B \U0001F91C \U0001F44F \U0001F64C \U0001FAF6 \U0001F450 \U0001F932 \U0001F91D \U0001F64F \u270D \U0001F485 \U0001F933 \U0001F4AA \U0001F9BE \U0001F9BF \U0001F9B5 \U0001F9B6 \U0001F442 \U0001F9BB \U0001F443 \U0001F9E0 \U0001FAC0 \U0001FAC1 \U0001F9B7 \U0001F9B4 \U0001F440 \U0001F441 \U0001F445 \U0001F444 \U0001FAE6 \U0001F476 \U0001F9D2 \U0001F466 \U0001F467 \U0001F9D1\U0001F471 \U0001F468\U0001F9D4 \U0001F469 \U0001F9D3 \U0001F474 \U0001F475 \U0001F64D \U0001F64E \U0001F645 \U0001F646 \U0001F481 \U0001F64B \U0001F9CF \U0001F647 \U0001F926 \U0001F937 \U0001F46E \U0001F575 \U0001F482 \U0001F977 \U0001F477 \U0001FAC5 \U0001F934 \U0001F478 \U0001F473 \U0001F472 \U0001F9D5 \U0001F935 \U0001F470 \U0001F930 \U0001FAC3 \U0001FAC4 \U0001F931 \U0001F47C \U0001F385 \U0001F936 \U0001F9B8 \U0001F9B9 \U0001F9D9-\U0001F9DF \U0001F9CC \U0001F486 \U0001F487 \U0001F6B6 \U0001F9CD \U0001F9CE \U0001F3C3 \U0001F483 \U0001F57A \U0001F574 \U0001F46F \U0001F9D6 \U0001F9D7 \U0001F93A \U0001F3C7 \u26F7 \U0001F3C2 \U0001F3CC \U0001F3C4 \U0001F6A3 \U0001F3CA \u26F9 \U0001F3CB \U0001F6B4 \U0001F6B5 \U0001F938 \U0001F93C-\U0001F93E \U0001F939 \U0001F9D8 \U0001F6C0 \U0001F6CC \U0001F46D \U0001F46B \U0001F46C \U0001F48F \U0001F491 \U0001F5E3 \U0001F464 \U0001F465 \U0001FAC2 \U0001F46A \U0001F463 \U0001F9B0 \U0001F9B1 \U0001F9B3 \U0001F9B2 \U0001F435 \U0001F412 \U0001F98D \U0001F9A7 \U0001F436 \U0001F415 \U0001F9AE \U0001F429 \U0001F43A \U0001F98A \U0001F99D \U0001F431 \U0001F408 \U0001F981 \U0001F42F \U0001F405 \U0001F406 \U0001F434 \U0001FACE \U0001FACF \U0001F40E \U0001F984 \U0001F993 \U0001F98C \U0001F9AC \U0001F42E \U0001F402-\U0001F404 \U0001F437 \U0001F416 \U0001F417 \U0001F43D \U0001F40F \U0001F411 \U0001F410 \U0001F42A \U0001F42B \U0001F999 \U0001F992 \U0001F418 \U0001F9A3 \U0001F98F \U0001F99B \U0001F42D \U0001F401 \U0001F400 \U0001F439 \U0001F430 \U0001F407 \U0001F43F \U0001F9AB \U0001F994 \U0001F987 \U0001F43B \U0001F428 \U0001F43C \U0001F9A5 \U0001F9A6 \U0001F9A8 \U0001F998 \U0001F9A1 \U0001F43E \U0001F983 \U0001F414 \U0001F413 \U0001F423-\U0001F427 \U0001F54A \U0001F985 \U0001F986 \U0001F9A2 \U0001F989 \U0001F9A4 \U0001FAB6 \U0001F9A9 \U0001F99A \U0001F99C \U0001FABD \U0001FABF \U0001F438 \U0001F40A \U0001F422 \U0001F98E \U0001F40D \U0001F432 \U0001F409 \U0001F995 \U0001F996 \U0001F433 \U0001F40B \U0001F42C \U0001F9AD \U0001F41F-\U0001F421 \U0001F988 \U0001F419 \U0001F41A \U0001FAB8 \U0001FABC \U0001F40C \U0001F98B \U0001F41B-\U0001F41D \U0001FAB2 \U0001F41E \U0001F997 \U0001FAB3 \U0001F577 \U0001F578 \U0001F982 \U0001F99F \U0001FAB0 \U0001FAB1 \U0001F9A0 \U0001F490 \U0001F338 \U0001F4AE \U0001FAB7 \U0001F3F5 \U0001F339 \U0001F940 \U0001F33A-\U0001F33C \U0001F337 \U0001FABB \U0001F331 \U0001FAB4 \U0001F332-\U0001F335 \U0001F33E \U0001F33F \u2618 \U0001F340-\U0001F343 \U0001FAB9 \U0001FABA \U0001F344 \U0001F347-\U0001F34D \U0001F96D \U0001F34E-\U0001F353 \U0001FAD0 \U0001F95D \U0001F345 \U0001FAD2 \U0001F965 \U0001F951 \U0001F346 \U0001F954 \U0001F955 \U0001F33D \U0001F336 \U0001FAD1 \U0001F952 \U0001F96C \U0001F966 \U0001F9C4 \U0001F9C5 \U0001F95C \U0001FAD8 \U0001F330 \U0001FADA \U0001FADB \U0001F35E \U0001F950 \U0001F956 \U0001FAD3 \U0001F968 \U0001F96F \U0001F95E \U0001F9C7 \U0001F9C0 \U0001F356 \U0001F357 \U0001F969 \U0001F953 \U0001F354 \U0001F35F \U0001F355 \U0001F32D \U0001F96A \U0001F32E \U0001F32F \U0001FAD4 \U0001F959 \U0001F9C6 \U0001F95A \U0001F373 \U0001F958 \U0001F372 \U0001FAD5 \U0001F963 \U0001F957 \U0001F37F \U0001F9C8 \U0001F9C2 \U0001F96B \U0001F371 \U0001F358-\U0001F35D \U0001F360 \U0001F362-\U0001F365 \U0001F96E \U0001F361 \U0001F95F-\U0001F961 \U0001F980 \U0001F99E \U0001F990 \U0001F991 \U0001F9AA \U0001F366-\U0001F36A \U0001F382 \U0001F370 \U0001F9C1 \U0001F967 \U0001F36B-\U0001F36F \U0001F37C \U0001F95B \u2615 \U0001FAD6 \U0001F375 \U0001F376 \U0001F37E \U0001F377-\U0001F37B \U0001F942 \U0001F943 \U0001FAD7 \U0001F964 \U0001F9CB \U0001F9C3 \U0001F9C9 \U0001F9CA \U0001F962 \U0001F37D \U0001F374 \U0001F944 \U0001F52A \U0001FAD9 \U0001F3FA \U0001F30D-\U0001F310 \U0001F5FA \U0001F5FE \U0001F9ED \U0001F3D4 \u26F0 \U0001F30B \U0001F5FB \U0001F3D5 \U0001F3D6 \U0001F3DC-\U0001F3DF \U0001F3DB \U0001F3D7 \U0001F9F1 \U0001FAA8 \U0001FAB5 \U0001F6D6 \U0001F3D8 \U0001F3DA \U0001F3E0-\U0001F3E6 \U0001F3E8-\U0001F3ED \U0001F3EF \U0001F3F0 \U0001F492 \U0001F5FC \U0001F5FD \u26EA \U0001F54C \U0001F6D5 \U0001F54D \u26E9 \U0001F54B \u26F2 \u26FA \U0001F301 \U0001F303 \U0001F3D9 \U0001F304-\U0001F307 \U0001F309 \u2668 \U0001F3A0 \U0001F6DD \U0001F3A1 \U0001F3A2 \U0001F488 \U0001F3AA \U0001F682-\U0001F68A \U0001F69D \U0001F69E \U0001F68B-\U0001F68E \U0001F690-\U0001F699 \U0001F6FB \U0001F69A-\U0001F69C \U0001F3CE \U0001F3CD \U0001F6F5 \U0001F9BD \U0001F9BC \U0001F6FA \U0001F6B2 \U0001F6F4 \U0001F6F9 \U0001F6FC \U0001F68F \U0001F6E3 \U0001F6E4 \U0001F6E2 \u26FD \U0001F6DE \U0001F6A8 \U0001F6A5 \U0001F6A6 \U0001F6D1 \U0001F6A7 \u2693 \U0001F6DF \u26F5 \U0001F6F6 \U0001F6A4 \U0001F6F3 \u26F4 \U0001F6E5 \U0001F6A2 \u2708 \U0001F6E9 \U0001F6EB \U0001F6EC \U0001FA82 \U0001F4BA \U0001F681 \U0001F69F-\U0001F6A1 \U0001F6F0 \U0001F680 \U0001F6F8 \U0001F6CE \U0001F9F3 \u231B \u23F3 \u231A \u23F0-\u23F2 \U0001F570 \U0001F55B \U0001F567 \U0001F550 \U0001F55C \U0001F551 \U0001F55D \U0001F552 \U0001F55E \U0001F553 \U0001F55F \U0001F554 \U0001F560 \U0001F555 \U0001F561 \U0001F556 \U0001F562 \U0001F557 \U0001F563 \U0001F558 \U0001F564 \U0001F559 \U0001F565 \U0001F55A \U0001F566 \U0001F311-\U0001F31C \U0001F321 \u2600 \U0001F31D \U0001F31E \U0001FA90 \u2B50 \U0001F31F \U0001F320 \U0001F30C \u2601 \u26C5 \u26C8 \U0001F324-\U0001F32C \U0001F300 \U0001F308 \U0001F302 \u2602 \u2614 \u26F1 \u26A1 \u2744 \u2603 \u26C4 \u2604 \U0001F525 \U0001F4A7 \U0001F30A \U0001F383 \U0001F384 \U0001F386 \U0001F387 \U0001F9E8 \u2728 \U0001F388-\U0001F38B \U0001F38D-\U0001F391 \U0001F9E7 \U0001F380 \U0001F381 \U0001F397 \U0001F39F \U0001F3AB \U0001F396 \U0001F3C6 \U0001F3C5 \U0001F947-\U0001F949 \u26BD \u26BE \U0001F94E \U0001F3C0 \U0001F3D0 \U0001F3C8 \U0001F3C9 \U0001F3BE \U0001F94F \U0001F3B3 \U0001F3CF \U0001F3D1 \U0001F3D2 \U0001F94D \U0001F3D3 \U0001F3F8 \U0001F94A \U0001F94B \U0001F945 \u26F3 \u26F8 \U0001F3A3 \U0001F93F \U0001F3BD \U0001F3BF \U0001F6F7 \U0001F94C \U0001F3AF \U0001FA80 \U0001FA81 \U0001F52B \U0001F3B1 \U0001F52E \U0001FA84 \U0001F3AE \U0001F579 \U0001F3B0 \U0001F3B2 \U0001F9E9 \U0001F9F8 \U0001FA85 \U0001FAA9 \U0001FA86 \u2660 \u2665 \u2666 \u2663 \u265F \U0001F0CF \U0001F004 \U0001F3B4 \U0001F3AD \U0001F5BC \U0001F3A8 \U0001F9F5 \U0001FAA1 \U0001F9F6 \U0001FAA2 \U0001F453 \U0001F576 \U0001F97D \U0001F97C \U0001F9BA \U0001F454-\U0001F456 \U0001F9E3-\U0001F9E6 \U0001F457 \U0001F458 \U0001F97B \U0001FA71-\U0001FA73 \U0001F459 \U0001F45A \U0001FAAD \U0001F45B-\U0001F45D \U0001F6CD \U0001F392 \U0001FA74 \U0001F45E \U0001F45F \U0001F97E \U0001F97F \U0001F460 \U0001F461 \U0001FA70 \U0001F462 \U0001FAAE \U0001F451 \U0001F452 \U0001F3A9 \U0001F393 \U0001F9E2 \U0001FA96 \u26D1 \U0001F4FF \U0001F484 \U0001F48D \U0001F48E \U0001F507-\U0001F50A \U0001F4E2 \U0001F4E3 \U0001F4EF \U0001F514 \U0001F515 \U0001F3BC \U0001F3B5 \U0001F3B6 \U0001F399-\U0001F39B \U0001F3A4 \U0001F3A7 \U0001F4FB \U0001F3B7 \U0001FA97 \U0001F3B8-\U0001F3BB \U0001FA95 \U0001F941 \U0001FA98 \U0001FA87 \U0001FA88 \U0001F4F1 \U0001F4F2 \u260E \U0001F4DE-\U0001F4E0 \U0001F50B \U0001FAAB \U0001F50C \U0001F4BB \U0001F5A5 \U0001F5A8 \u2328 \U0001F5B1 \U0001F5B2 \U0001F4BD-\U0001F4C0 \U0001F9EE \U0001F3A5 \U0001F39E \U0001F4FD \U0001F3AC \U0001F4FA \U0001F4F7-\U0001F4F9 \U0001F4FC \U0001F50D \U0001F50E \U0001F56F \U0001F4A1 \U0001F526 \U0001F3EE \U0001FA94 \U0001F4D4-\U0001F4DA \U0001F4D3 \U0001F4D2 \U0001F4C3 \U0001F4DC \U0001F4C4 \U0001F4F0 \U0001F5DE \U0001F4D1 \U0001F516 \U0001F3F7 \U0001F4B0 \U0001FA99 \U0001F4B4-\U0001F4B8 \U0001F4B3 \U0001F9FE \U0001F4B9 \u2709 \U0001F4E7-\U0001F4E9 \U0001F4E4-\U0001F4E6 \U0001F4EB \U0001F4EA \U0001F4EC-\U0001F4EE \U0001F5F3 \u270F \u2712 \U0001F58B \U0001F58A \U0001F58C \U0001F58D \U0001F4DD \U0001F4BC \U0001F4C1 \U0001F4C2 \U0001F5C2 \U0001F4C5 \U0001F4C6 \U0001F5D2 \U0001F5D3 \U0001F4C7-\U0001F4CE \U0001F587 \U0001F4CF \U0001F4D0 \u2702 \U0001F5C3 \U0001F5C4 \U0001F5D1 \U0001F512 \U0001F513 \U0001F50F-\U0001F511 \U0001F5DD \U0001F528 \U0001FA93 \u26CF \u2692 \U0001F6E0 \U0001F5E1 \u2694 \U0001F4A3 \U0001FA83 \U0001F3F9 \U0001F6E1 \U0001FA9A \U0001F527 \U0001FA9B \U0001F529 \u2699 \U0001F5DC \u2696 \U0001F9AF \U0001F517 \u26D3 \U0001FA9D \U0001F9F0 \U0001F9F2 \U0001FA9C \u2697 \U0001F9EA-\U0001F9EC \U0001F52C \U0001F52D \U0001F4E1 \U0001F489 \U0001FA78 \U0001F48A \U0001FA79 \U0001FA7C \U0001FA7A \U0001FA7B \U0001F6AA \U0001F6D7 \U0001FA9E \U0001FA9F \U0001F6CF \U0001F6CB \U0001FA91 \U0001F6BD \U0001FAA0 \U0001F6BF \U0001F6C1 \U0001FAA4 \U0001FA92 \U0001F9F4 \U0001F9F7 \U0001F9F9-\U0001F9FB \U0001FAA3 \U0001F9FC \U0001FAE7 \U0001FAA5 \U0001F9FD \U0001F9EF \U0001F6D2 \U0001F6AC \u26B0 \U0001FAA6 \u26B1 \U0001F9FF \U0001FAAC \U0001F5FF \U0001FAA7 \U0001FAAA \U0001F3E7 \U0001F6AE \U0001F6B0 \u267F \U0001F6B9-\U0001F6BC \U0001F6BE \U0001F6C2-\U0001F6C5 \u26A0 \U0001F6B8 \u26D4 \U0001F6AB \U0001F6B3 \U0001F6AD \U0001F6AF \U0001F6B1 \U0001F6B7 \U0001F4F5 \U0001F51E \u2622 \u2623 \u2B06 \u2197 \u27A1 \u2198 \u2B07 \u2199 \u2B05 \u2196 \u2195 \u2194 \u21A9 \u21AA \u2934 \u2935 \U0001F503 \U0001F504 \U0001F519-\U0001F51D \U0001F6D0 \u269B \U0001F549 \u2721 \u2638 \u262F \u271D \u2626 \u262A \u262E \U0001F54E \U0001F52F \U0001FAAF \u2648-\u2653 \u26CE \U0001F500-\U0001F502 \u25B6 \u23E9 \u23ED \u23EF \u25C0 \u23EA \u23EE \U0001F53C \u23EB \U0001F53D \u23EC \u23F8-\u23FA \u23CF \U0001F3A6 \U0001F505 \U0001F506 \U0001F4F6 \U0001F6DC \U0001F4F3 \U0001F4F4 \u2640 \u2642 \u26A7 \u2716 \u2795-\u2797 \U0001F7F0 \u267E \u203C \u2049 \u2753-\u2755 \u2757 \u3030 \U0001F4B1 \U0001F4B2 \u2695 \u267B \u269C \U0001F531 \U0001F4DB \U0001F530 \u2B55 \u2705 \u2611 \u2714 \u274C \u274E \u27B0 \u27BF \u303D \u2733 \u2734 \u2747 \u00A9 \u00AE \u2122 \U0001F51F-\U0001F524 \U0001F170 \U0001F18E \U0001F171 \U0001F191-\U0001F193 \u2139 \U0001F194 \u24C2 \U0001F195 \U0001F196 \U0001F17E \U0001F197 \U0001F17F \U0001F198-\U0001F19A \U0001F201 \U0001F202 \U0001F237 \U0001F236 \U0001F22F \U0001F250 \U0001F239 \U0001F21A \U0001F232 \U0001F251 \U0001F238 \U0001F234 \U0001F233 \u3297 \u3299 \U0001F23A \U0001F235 \U0001F534 \U0001F7E0-\U0001F7E2 \U0001F535 \U0001F7E3 \U0001F7E4 \u26AB \u26AA \U0001F7E5 \U0001F7E7-\U0001F7E9 \U0001F7E6 \U0001F7EA \U0001F7EB \u2B1B \u2B1C \u25FC \u25FB \u25FE \u25FD \u25AA \u25AB \U0001F536-\U0001F53B \U0001F4A0 \U0001F518 \U0001F533 \U0001F532 \U0001F3C1 \U0001F6A9 \U0001F38C \U0001F3F4 \U0001F3F3 \U0001F1E6-\U0001F1FF 0-9]",
        flags=re.UNICODE)
    return emoji_pattern.sub(r'', str(text))


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
    df = df[df["main_content"].notna()]
    df.to_csv("preprocessed.csv")


def save_preprocessed_as_text(df):
    df = df[df["main_content"].notna()]
    with open("preprocessed.txt", "w+") as f:
        for cleaned_line in df["main_content"].values.tolist():
            f.write(cleaned_line + "\n~~~~~~~~~~~~~~~~caipi~~~~~~~~~~~~~~~~")

        f.close()
