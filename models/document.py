import os

import pickle as pkl
import config.config as cfg

from extract.extractor import extract_main_text


class Document:
    def __init__(self, location, location_result_count, long, lat, url, img_url, title, src_file, src_line):
        self.location = location
        self.location_result_count = location_result_count
        self.long = long
        self.lat = lat
        self.url = url
        self.img_url = img_url
        self.title = title

        self.src_file = src_file
        self.src_line = src_line
        self.main_content = "None"
        self.html_content = "None"
        self.cleaned_content = "None"

        self.topic_information = "None"

    def main_content_present(self):
        return self.main_content != "None" and self.main_content is not None

    def get_topic(self):
        return self.topic_information

    def compare_cleaned_and_main(self):
        print(self.main_content)
        print(self.cleaned_content)

    def print_topic(self):
        print(self.topic_information)

    def print_document(self, re=False):
        if re:
            return "{}, {}, {}, {}, {}".format(
                self.location,
                self.title,
                self.url,
                self.main_content_present(),
                self.topic_information
            )
        print("{}, {}, {}, {}, {}".format(
            self.location,
            self.title,
            self.url,
            self.main_content_present(),
            self.topic_information
        ))

    def extract(self):
        if not os.path.isfile(os.path.join(cfg.gdelt_out(), filename(self.src_file, self.src_line))):
            self.main_content, self.html_content = extract_main_text(self)
            return True

    def print_real_text(self):
        if self.main_content_present():
            print(self.main_content)
        else:
            print("***Does not have real content***")

    def save_document(self, i="+", p=False):
        with open(os.path.join(cfg.gdelt_out(), filename(self.src_file, self.src_line)), "w+b") as f:
            pkl.dump(self, f)
            f.close()

        if p:
            print("[{}] Saved document: [{}]".format(i, self.print_document(re=True)))


def filename(src_file, src_line):
    return "df_pkl_{}_{}".format(src_file, src_line)


def traceback(file_name):
    temporary_split = file_name.replace("df_pkl_", "").split("_")

    csv_file = "_".join([temporary_split[0], temporary_split[1], temporary_split[2]])
    csv_line = int(temporary_split[3])

    return csv_file, csv_line
