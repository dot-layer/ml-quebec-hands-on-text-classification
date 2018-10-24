import re
import json
from bs4 import BeautifulSoup
import nltk.data
import spacy
import tqdm
import spacy


sent_tokenizer = nltk.data.load('tokenizers/punkt/french.pickle')
title_regex = re.compile(r"\<p\>\s+\<strong\>[A-Z\s«»#ÀÂÇÉÈÊËÎÏÔÛÙÜŸ’,\.?!-]+\<\/strong\>\<\/p\>")

nlp = spacy.load('fr')
tokenizer = nlp


def read_articles(filename):
    for a in json.load(open(filename)):
        yield a


def remove_subtitles(body):
    return title_regex.sub("", body)


def remove_wordpress_content(soup):
    if 'wp-comment' in str(soup):
        for div in soup.find_all("div", {'class':'wp-comment-body'}):
            div.decompose()
        soup.find('h3', id="wp-comments").decompose()
    return soup


def remove_style_tags(soup):
    if '<style' in str(soup):
        for div in soup.find_all("style"):
            div.decompose()
    return soup

def remove_credit_tags(soup):
    if 'class="credit"' in str(soup):
        for div in soup.find_all("div", {'class':'credit'}):
            div.decompose()
    return soup

def clean_body(body):
    body_without_subtitles = remove_subtitles(body)
    soup = BeautifulSoup(body_without_subtitles, 'html.parser')
    soup = remove_wordpress_content(soup)
    soup = remove_style_tags(soup)
    soup = remove_credit_tags(soup)
    return soup.get_text().replace("\n", "").strip()


def clean_title(title):
    title = BeautifulSoup(title, 'html.parser').get_text().replace("\n", "").strip()
    chars_to_replace = [' ', '/']
    for char in chars_to_replace:
        title = title.replace(char, '_')
    return title.lower()


def clean_article(article):
    title = clean_title(article['title'])
    body = clean_body(article['body'])
    author = article['author'].replace(' ', '-').lower()
    keywords = [[str(w).lower() for w in tokenizer(k)] for k in article['keywords']]
    sentences = sent_tokenizer.tokenize(body)
    nlped_sentences = tokenizer.pipe(sentences, n_threads=4)
    text = [[str(t).lower() for t in sentence] for sentence in nlped_sentences]
    return {
        "author": author,
        "title": title,
        "keywords": keywords,
        "text": text
    }


def main():
    articles = list(read_articles('./data/dataset-raw.json'))
    cleaned_articles = list()
    for a in tqdm.tqdm(articles):
        cleaned_article = clean_article(a)
        cleaned_articles.append(cleaned_article)
    json.dump(cleaned_articles, open('./dataset/dataset-clean.json', 'w', encoding='utf-8'), indent=True)


if __name__ == '__main__':
    main()
