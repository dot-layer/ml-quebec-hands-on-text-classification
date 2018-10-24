import pickle

def main():
    with open('./data/fasttext_training_data.txt', 'w') as handle_data:
        train_dataset = pickle.load(open('./data/train.pickle', 'rb'))
        for article in train_dataset:
            for sentence in article.text:
                handle_data.write("{} ".format(" ".join(sentence)))


if __name__ == '__main__':
    main()
