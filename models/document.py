import os

import pickle as pkl
import config.config as cfg
import uuid

from extract.extractor import extract_main_text

class Document:
    def __init__(self, location, location_result_count, long, lat, url, img_url, date, title):
        self.location = location
        self.location_result_count = location_result_count
        self.long = long
        self.lat = lat
        self.url = url
        self.img_url = img_url
        self.title = title

        self.date = date
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
        self.main_content, self.html_content = extract_main_text(self)

    def print_real_text(self):
        if self.main_content_present():
            print(self.main_content)
        else:
            print("***Does not have real content***")

    def save_document(self, i="+", p=False):
        with open(os.path.join(cfg.gdelt_out_path_about(), "df_pkl_{}".format(uuid.uuid4())), "wb+") as file:
            pkl.dump(self, file)

        if p:
            print("[{}] Saved document: [{}]".format(i, self.print_document(re=True)))
