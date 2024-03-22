import os.path

import pickle as pkl
from tqdm import tqdm

import bertopic
from bertopic import BERTopic

import config.config as cfg

from berts.helper.bert_helper import read_text


def match_topics_from_model(chunk_size=100000):
    print("Loading topic model...")
    topic_model = BERTopic.load("model")

    if os.path.isfile(os.path.join(cfg.base_path(), "custom_topics.pkl")):
        with open(os.path.join(cfg.base_path(), "custom_topics.pkl"), 'rb') as f:
            print("Loading custom topics...")
            topic_dictionary = pkl.load(f)

            print("Reading texts...")
            file_names, _ = read_text("preprocessed.txt")

            print(len(file_names))
            print(len(topic_model.topics_))

            print("Applying topics to files from the model")
            loop = tqdm(zip(topic_model.topics_, file_names))

            corrupted_files = 0

            for topic_index, doc_file in loop:
                with open(os.path.join(cfg.gdelt_out(), doc_file), "rb") as d:
                    try:
                        document = pkl.load(d)

                        try:
                            if topic_index < 0:
                                topic = "spam"
                            else:
                                topic = topic_dictionary[int(topic_index)]

                            d.close()
                            document.topic_information = topic
                            document.save_document()
                        except ValueError as _:
                            raise Exception("Error in translating the topic index. Did you ran label_topics() first?")

                    except EOFError as _:
                        corrupted_files += 1
                        loop.set_postfix_str("Coruppted files: {}".format(corrupted_files))

    else:
        print("No file of custom topics found, execute label_topics() first!")


if __name__ == '__main__':
    match_topics_from_model()
