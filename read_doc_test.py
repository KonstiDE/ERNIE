import os.path
import pickle as pkl
import random

from tqdm import tqdm

import config.config as cfg


def doc_test_read():
    with open(os.path.join(cfg.gdelt_out(), "df_pkl_2023-09-26_12-00-02_1d_1"), "r+b") as d:
        document = pkl.load(d)
        d.close()

        document.print_real_text()
        print(document.cleaned_content)


if __name__ == '__main__':
    doc_test_read()
