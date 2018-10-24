import scrapy

mtl_authors = [
    'richard-martineau',
    'michel-girard',
    'joseph-facal',
    'sophie-durocher',
    'mathieu-bock-cote',
    'remi-nadeau',
    'fatima-houda-pepin',
    'gilles-brien',
    'lise-ravary',
    'maxim-martin',
    'antoine-robitaille',
    'marie-eve-doyon',
    'michel-beaudry',
    'patrick-campeau',
    'josee-legault',
    'steve-fortin',
    'julien-cabana',
    'pierre-martin',
    'guy-fournier',
    'remi-nadeau',
    'jonathan-trudeau',
    'karina-marceau',
    'marjorie-champagne',
    'claude-villeneuve',
    'loic-tasse',
    'mario-dumont',
    'denise-bombardier',
    'isabelle-marechal',
    'martine-desjardins',
    'nathalie-elgrably-levy',
    'gilles-proulx',
    'rejean-parent',
    'richard-desjardins',
    'alain-dufresne'
]

qc_authors = [
    'michel-hebert',
    'jose-theodore',
    'loic-tasse',
    'marc-de-foy',
    'richard-latendresse',
    'john-limniatis',
    'rodger-brulotte',
    'guy-fournier',
    'michel-bergeron',
    'jerome-landry',
    'denis-gravel',
    'camil-bouchard',
    'leo-paul-lauzon',
    'youri-chassin',

]

# Example link for an author:
# 'http://www.journaldemontreal.com/auteur/richard-martineau/page/1?pageSize=100&ajax=true'

class Spider(scrapy.Spider):
    name = 'ml-quebec-2018-spider'

    start_urls = [
        'http://www.journaldemontreal.com/auteur/{}/page/{}?pageSize=100&ajax=true'.format(author, i) for i in range(320) for author in mtl_authors
    ]

    start_urls += [
        'http://www.journaldequebec.com/auteur/{}/page/{}?pageSize=100&ajax=true'.format(author, i) for i in range(320) for author in qc_authors
    ]

    def parse(self, response):
        for article in response.css('article.archive > a'):
            yield response.follow(article, self.parse_article)

    def parse_article(self, response):
        title = response.css('h1').extract_first()
        body = response.css('div.article-main-txt').extract_first()
        meta = response.xpath("//meta[@name='news_keywords']/@content")[0].extract().split(',')
        author = response.xpath("//meta[@name='author']/@content")[0].extract()
        yield {
            'title': title,
            'body': body,
            'keywords': meta,
            'author': author
        }
