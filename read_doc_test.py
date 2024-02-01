import os.path
import pickle as pkl
import random

import config.config as cfg

if __name__ == '__main__':
    with open(os.path.join(os.path.join(cfg.gdelt_out(), "../about/"), random.choice(os.listdir(os.path.join(cfg.gdelt_out(), "../about/")))), "rb+") as f:
        document = pkl.load(f)

        document.print_document()
