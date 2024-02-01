import os

from bertopic import BERTopic
import pandas as pd

import pickle

import config.config as cfg


def label_topics():
    topic_model = BERTopic.load(os.path.join(cfg.base_path(), "model"))
    pd.set_option('display.max_rows', None)

    print(topic_model.get_topic_info())

    custom_topics = {}

    for i in range(len(topic_model.get_topic_info())):
        os.system('clear')
        print("----------------------------")
        print("Topics already created: ")
        print(set(custom_topics.values()))
        print("----------Topic " + str(i) + "----------")
        print(topic_model.get_topic(i))
        print("----------------------------")
        topic = input()
        custom_topics[i] = topic

    topic_model.set_topic_labels(custom_topics)

    with open('custom_topics.pkl', 'wb+') as f:
        pickle.dump(custom_topics, f)

    topic_model.save("model_custom_topics", save_embedding_model=False)
