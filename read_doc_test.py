import os.path
import pickle as pkl

import config.config as cfg


def doc_test_read():
    with open(os.path.join(cfg.gdelt_out(), "gn_pkl_240102_10260"), "r+b") as d:
        gkgnode = pkl.load(d)
        d.close()

        gkgnode.print_document()


if __name__ == '__main__':
    doc_test_read()
