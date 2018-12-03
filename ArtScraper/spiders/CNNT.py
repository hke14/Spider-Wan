from datetime import datetime as dt
import scrapy
import re
import pymongo
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from ArtScraper.items import ArtscraperItem
from scrapy.crawler import CrawlerProcess, CrawlerRunner
import csv
class CNNSpider(scrapy.Spider):


    article = ""
    name = 'tech'
    allowed_domains = []

    start_urls = [
        "http://arabic.cnn.com/rss/cnnarabic_scitech.rss"


    ]



    def parse(self, response):

        articles = response.xpath('//channel/item')

        print("hello")

        for article in articles:
            item = ArtscraperItem()
            print ('hello')
            item['tag']='CNN'
            item['tagu']='http://cdn.marketplaceimages.windowsphone.com/v8/images/86d045cb-6436-47a0-a0de-1726e1fc0a80?imageType=ws_icon_medium'
            item['date'] = dt.today()
            item['date_str'] = article.xpath('pubDate/text()').extract_first()
            item['url'] = article.xpath('link/text()').extract_first()
            category1=article.xpath('link/text()').extract_first()
            result = re.search('http://arabic.cnn.com/(.*)/article', category1)
            try :
               result1=result.group(1)
            except:
                result1=None
            item['categorie'] = "tech"

            item['title'] = article.xpath('title/text()').extract_first()
            article.register_namespace('media', 'http://search.yahoo.com/mrss/')
            p= article.xpath('media:content/@url').extract_first()
            print (p)
            url = item['url']

            if not p:

             p="https://www.peacenaturals.com/wp-content/uploads/2014/08/cnn-logo.jpg"

            else :
                p = article.xpath('media:content/@url').extract_first()

            item['pic'] =p
            yield scrapy.Request(
                url,
                callback=self.parse_article,
                meta={'item': item},  # carry over our item
            )


    def parse_article(self, response):
        item = response.meta['item']
        pars = response.xpath("//div[@class='clearfix wysiwyg _2A-9LYJ7eK']/p/text()").extract()
        if not pars:
            pars ="Found no content"

      #  article = ' '.join(pars)

        keywords=response.xpath("//footer[@class='clearfix _1MbEDqOhpQ']/ul/*/a/text()").extract()

        item['keywords'] = keywords
        lexicon = dict()

        pars1 = '-'.join(pars)
        with open('spiders/ALL_lex.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                lexicon[row[0]] = int(row[1])


        score = 0
        for word in pars1.split(" "):
            if word in lexicon:
                score = score + lexicon[word]
            #
        item['score'] = score





        item['art_content'] = '-'.join(pars)

        print ("HHHH")
        yield item


class MongoPipeline(object):
    MONGO_URI = 'mongodb://gnr011:Kalash1@ds040309.mlab.com:40309/newsaggregartor'
    MONGO_DATABASE = 'newsaggregartor'

    collection_name = 'articles'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):


        self.db[self.collection_name].update_one({"title": title}, {
            "$set": {"art_content": item['art_content'], "date": item['date'], "date_str": item['date_str'],
                     "title": item['title'], "url": item['url'], "pic": item['pic'], "tag": item['tag'],
                     "categorie": item['categorie'], "tagu": item['tagu'], "keywords": item['keywords'],
                     "score": item['score']}},
                      upsert=True)
        return item
