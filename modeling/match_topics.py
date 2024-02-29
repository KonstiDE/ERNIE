import os.path

import pickle as pkl
from tqdm import tqdm

import bertopic
from bertopic import BERTopic

import config.config as cfg

from berts.helper.bert_helper import read_text


def match_topics_from_model(chunk_size=100000):
    print("Loading topic model...")

    if os.path.isfile(os.path.join(cfg.base_path(), "custom_topics.pkl")):
        with open(os.path.join(cfg.base_path(), "custom_topics.pkl"), 'rb') as f:
            print("Loading custom topics...")
            topic_dictionary = pkl.load(f)

            print(topic_dictionary)
            print(len(topic_dictionary.keys()))

            print("Reading texts...")
            file_names, _ = read_text("preprocessed.txt")

            print("Applying topics to files in batches of {}...".format(chunk_size))
            file_chunks = [file_names[i:i + chunk_size] for i in range(0, len(file_names), chunk_size)]

            c = 1
            for file_chunk in file_chunks:
                print("-" * 16)
                print("Batch {} of {}".format(c, len(file_chunks)))
                print("-" * 16)
                loop = tqdm(file_chunk)

                corrupted_files = 0

                for topic_index, doc_file in enumerate(loop):
                    with open(os.path.join(cfg.gdelt_out(), doc_file), "rb") as d:
                        try:
                            if topic_index - 1 > 0:
                                document = pkl.load(d)
                                d.close()
                                document.topic_information = topic_dictionary[int(document.topic_information)]
                                document.save_document()

                        except EOFError as _:
                            corrupted_files += 1
                            loop.set_postfix_str("Coruppted files: {}".format(corrupted_files))

                        d.close()
                c += 1
    else:
        print("No file of custom topics found, execute label_topics() first!")


if __name__ == '__main__':
    match_topics_from_model()
