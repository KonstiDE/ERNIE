from visualize_topic_over_time import visualize_topics

import config.config as cfg

if __name__ == '__main__':
    cfg.write_os_environments()

    # Data acquisition and preprocessing
    # build_docs(fetching_chunk_size=256, global_knowledge_graph_format=True)
    # preprocess_docs(chunk_size=100000)
    #
    # Topic Modeling
    # analyse_docs(
    #     umap_model=UMAP(n_neighbors=15, n_components=3, metric="cosine"),
    #     hdbscan_model=HDBSCAN(min_cluster_size=64),
    #     vectorizer_model=OnlineCountVectorizer(ngram_range=(1, 1)),
    #     nr_topics=128,
    #     n_gram_range=(1, 1),
    # )
    # label_topics()
    # match_topics_from_model()
    # language_distribution()
    visualize_topics()
    # dump_gkg_to_gpkg()

    # Analysis
    # doc_test_read()

