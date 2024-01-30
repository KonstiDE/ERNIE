import os.path

import bertopic
from bertopic import BERTopic

import config.config as cfg

from berts.helper.bert_helper import read_text


def match_topics_from_model():
    topic_model = BERTopic.load(os.path.join(cfg.base_path(), "model"))

    texts = read_text("preprocessed.txt")


if __name__ == '__main__':
    match_topics_from_model()
