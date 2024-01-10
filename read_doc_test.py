import os.path
import pickle as pkl

import config.config as cfg

if __name__ == '__main__':
    with open(os.path.join(cfg.gdelt_out(), "df_pkl_0005d2bb-30a3-42b2-becd-21d310164386"), "rb+") as f:
        document = pkl.load(f)

        document.print_document()
        print(document.date)