import os.path
import pickle as pkl
import random

import config.config as cfg

if __name__ == '__main__':
    with open(os.path.join(cfg.gdelt_out(), random.choice(os.listdir(cfg.gdelt_out()))), "rb+") as f:
        document = pkl.load(f)

        document.print_document()
        document.compare_cleaned_and_main()
