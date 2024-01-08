import os.path
import pickle as pkl

import config.config as cfg

if __name__ == '__main__':
    with open(os.path.join(cfg.gdelt_out_path_about(), "df_pkl_bc7cc64f-fc51-4c3f-8158-97d973b24c92"), "rb+") as f:
        document = pkl.load(f)

        document.print_document()
        document.print_real_text()