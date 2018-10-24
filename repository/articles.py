import pickle
from typing import List, Tuple
import logging
import json
from domain.article import Article


def load_articles(path='./data/dataset-clean.json') -> List[Article]:
    logging.info("Loading dataset...")
    dataset = json.load(open(path, encoding='utf-8'))
    logging.info("Loaded {} articles".format(len(dataset)))
    for article_json in dataset:
        yield Article(
            article_json['author'],
            article_json['title'],
            article_json['keywords'],
            article_json['text']
        )


def load_splitted_articles(data_folder='./data') -> Tuple[List[Article], List[Article], List[Article]]:
    train_examples = pickle.load(open('{}/train.pickle'.format(data_folder), 'rb'))
    valid_examples = pickle.load(open('{}/valid.pickle'.format(data_folder), 'rb'))
    test_examples = pickle.load(open('{}/test.pickle'.format(data_folder), 'rb'))
    return train_examples, valid_examples, test_examples


if __name__ == '__main__':
    logger = logging.getLogger().setLevel(logging.INFO)
    articles = list(load_articles())
    print(articles[0])
    print(articles[0].get_top_k_keywords())
