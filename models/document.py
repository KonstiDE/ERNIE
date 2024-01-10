import os

import pickle as pkl
import config.config as cfg

from extract.extractor import extract_main_text

class Document:
    def __init__(self, location, location_result_count, long, lat, url, img_url, title, src_file: str, src_line):
        self.location = location
        self.location_result_count = location_result_count
        self.long = long
        self.lat = lat
        self.url = url
        self.img_url = img_url
        self.title = title

        self.src_file = src_file
        self.src_line = src_line
        self.main_content = None
        self.html_content = None

    def main_content_present(self):
        return self.main_content is not None

    def print_document(self, re=False):
        if re:
            return "{}, {}, {}, {}".format(self.location,self.title,self.url,self.main_content_present())
        print("{}, {}, {}, {}".format(
            self.location,
            self.title,
            self.url,
            self.main_content_present()
        ))

    def extract(self):
        if not os.path.isfile(os.path.join(cfg.gdelt_out(), "df_pkl_{}_{}".format(self.src_file, self.src_line))):
            self.main_content, self.html_content = extract_main_text(self)
            return True
        return False

    def print_real_text(self):
        if self.main_content_present():
            print(self.main_content)
        else:
            print("***Does not have real content***")

    def save_document(self, i="+", p=False):
        with open(os.path.join(cfg.gdelt_out(), "df_pkl_{}_{}".format(self.src_file, self.src_line)), "wb+") as f:
            pkl.dump(self, f)

        if p:
            print("[{}] Saved document: [{}]".format(i, self.print_document(re=True)))
