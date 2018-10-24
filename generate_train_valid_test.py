import logging
import math
import pickle

import numpy as np

from repository.articles import load_articles
np.random.seed(42)


def split_examples(examples):
    np.random.shuffle(examples)
    num_data = len(examples)
    train_split_percent = 0.8
    valid_split_percent = 0.1
    num_train_samples = math.floor(train_split_percent * num_data)
    num_valid_samples = math.floor(valid_split_percent * num_data)
    train_dataset = examples[:num_train_samples]
    valid_dataset = examples[num_train_samples:num_train_samples + num_valid_samples]
    test_dataset = examples[num_train_samples + num_valid_samples:]
    return train_dataset, valid_dataset, test_dataset


def main():
    articles_by_authors = dict = {}
    articles = load_articles()

    for a in articles:
        if a.author not in articles_by_authors:
            articles_by_authors[a.author] = []
        articles_by_authors[a.author].append(a)

    full_train = list()
    full_valid = list()
    full_test = list()
    num_excluded_authors = 0
    for author, articles in articles_by_authors.items():
        if author != '' and len(articles) > 50:
            logging.info("Num articles for {}: {}".format(author, len(articles)))
            train, valid, test = split_examples(articles)
            full_train += train
            full_valid += valid
            full_test += test
        else:
            num_excluded_authors += 1

    logging.info("Num excluded authors: {}".format(num_excluded_authors))
    logging.info("Num articles in train: {}".format(len(full_train)))
    logging.info("Num articles in valid: {}".format(len(full_valid)))
    logging.info("Num articles in test: {}".format(len(full_test)))
    pickle.dump(full_train, open('data/train.pickle', 'wb'))
    pickle.dump(full_valid, open('data/valid.pickle', 'wb'))
    pickle.dump(full_test, open('data/test.pickle', 'wb'))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
