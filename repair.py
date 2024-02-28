import os
import models.document as doc

import config.config as cfg
import pickle as pkl

from tqdm import tqdm

import build_docs as build


def start_repair():
    files = os.listdir(cfg.gdelt_out())

    loop = tqdm(files)

    corrupted_files = 0

    for file in loop:
        try:
            with open(os.path.join(cfg.gdelt_out(), file), "rb") as f:
                pkl.load(f)
                f.close()

        except EOFError as eof:
            corrupted_files += 1
            loop.set_postfix_str("Corrupted files: {}".format(corrupted_files))

            os.remove(os.path.join(cfg.gdelt_out(), file))

            csv_file, csv_line = doc.traceback(file)
            build.extract_single_trace_df(csv_file, csv_line)


