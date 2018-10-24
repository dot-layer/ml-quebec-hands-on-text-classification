from typing import List

from nltk.corpus import stopwords

def french_stopwords():
    sw = set(stopwords.words('french'))
    other_sw = {
        'l’',
        "l\'",
        "d’",
        "d\'",
        "qu’","«", "!", "\"", "»", ".", "l\'", "d\'", "qu\'", "c\'", "n\'", "l’", "j\'", "s\'", "...",
        ',', '-', '.', '.-', ':', 'les'
    }
    sw = sw.union(other_sw)
    return sw

stopwords = french_stopwords()


class Article:
    def __init__(self, author: str, title: str, keywords: List[str], text: List[str]):
        self.author = author
        self.title = title
        self.keywords = keywords
        self.text = text

    def to_json(self):
        return {
            "author": self.author,
            "title": self.title,
            "keywords": self.keywords,
            "text": self.text
        }


    def get_keywords(self):
        return [[word for word in keyword if word not in stopwords] for keyword in self.keywords]

    def get_sentences(self):
        return [s for s in self.text if len(s) < 100]

    def get_sentences_with_keywords(self):
        top_keywords = set([s for k in self.get_top_k_keywords() for s in k[0]])
        sentences_with_keywords = list()
        for sentence in self.text:
            all_keywords_in_sentence = set()
            for keyword in self.get_keywords():
                keyword_set = set(keyword)
                sentence_set = set(sentence)
                keywords_in_sentence = keyword_set.intersection(sentence_set)
                keywords_not_in_top = keywords_in_sentence - (keywords_in_sentence & top_keywords)
                all_keywords_in_sentence = all_keywords_in_sentence.union(keywords_not_in_top)
            if len(all_keywords_in_sentence):
                sentences_with_keywords.append([sentence, all_keywords_in_sentence, top_keywords])
        return sentences_with_keywords



    def get_top_k_keywords(self, k=3):
        article_bow = [word for line in self.text for word in line]
        keywords_to_consider = self.get_keywords()
        counts = {}
        for tw in keywords_to_consider:
            count_key = tuple(tw)
            for w in tw:
                if w not in stopwords:
                    num_in_body = sum([1 for word in article_bow if word == w])
                    if count_key not in counts:
                        counts[count_key] = num_in_body
                    else:
                        counts[count_key] += num_in_body
        keywords_importance = sorted(counts.items(), key=lambda kv: -kv[1])
        # keywords_importance = [(k.split(), v) for k, v in keywords_importance]
        return keywords_importance[:max(0, k)]


    def __repr__(self):
        return "Author: {}\n".format(self.author) +\
        "Title: {}\n".format(self.title) +\
        "Keywords: {}\n".format(", ".join([' '.join(k) for k in self.keywords])) +\
        "Body:\n{}".format("\n".join([" ".join(sentence) for sentence in self.text]))
