import os
import pickle as pkl

import config.config as cfg

from tqdm import tqdm

import fasttext
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(repo_id="facebook/fasttext-language-identification", filename="model.bin")
model = fasttext.load_model(model_path)


def language_distribution():
    files = os.listdir(os.path.join(cfg.gdelt_out(), "../about/"))

    lang_dist = {}
    corrupted_files = 0

    loop = tqdm(files)

    for file in loop:
        with open(os.path.join(os.path.join(cfg.gdelt_out(), "../about/"), file), "rb") as f:
            try:
                document = pkl.load(f)
                f.close()

                if document.main_content_present():
                    lang = str(
                        model.predict(document.main_content.replace("\n", " "))[0][0]
                    ).split("__")[2].split("_")[0]

                    if lang not in lang_dist.keys():
                        lang_dist[lang] = 1
                    else:
                        lang_dist[lang] += 1
            except EOFError as _:
                corrupted_files += 1
                loop.set_postfix_str("Corrupted files: {}".format(corrupted_files))

    print(lang_dist)
