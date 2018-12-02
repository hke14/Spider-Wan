import re
from datetime import datetime as dt
import scrapy
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from ArtScraper.items import ArtscraperItem
from scrapy.crawler import CrawlerProcess, CrawlerRunner
import csv


class PostSpider(scrapy.Spider):
    article = ""
    name = 'craww'
    allowed_domains = []

    start_urls = [
        'http://www.aljazeera.net/aljazeerarss/be46a341-fe26-41f1-acab-b6ed9c198b19/e6aef64d-084c-42f0-8269-abe48e0cd154']

    def parse(self, response):

        articles = response.xpath('//channel/item')

        for article in articles:
            item = ArtscraperItem()
            print('hello')
            item['tag'] = 'AlJazeera'
            item[
                'tagu'] = 'https://is3-ssl.mzstatic.com/image/thumb/Purple125/v4/a4/46/fc/a446fc8c-c1c3-8d5b-c914-7bf768f2e0b1/AppIcon-1x_U007emarketing-85-220-6.png/246x0w.jpg'
            item['date'] = dt.today()
            item['date_str'] = article.xpath('pubDate/text()').extract_first()
            item['url'] = article.xpath('link/text()').extract_first()
            item['title'] = article.xpath('title/text()').extract_first()
            article.register_namespace('media', 'http://search.yahoo.com/mrss/')
            catergories = article.xpath('guid/text()').extract_first()

            result = re.search('http://www.bbc.co.uk/arabic/(.*)-', catergories)

            try:
                result1 = result.group(1)
            except:
                result1 = None
            item['categorie'] = result1

            url = item['url']

            yield scrapy.Request(
                url,
                callback=self.parse_article,
                meta={'item': item},  # carry over our item
            )

    def parse_article(self, response):
        item = response.meta['item']

        jaz = 'http://www.aljazeera.net'
        p = response.xpath("//div[@id='mediaSection']//@src").extract_first()
        if not p:
            p = 'https://cdn.worldvectorlogo.com/logos/aljazeere-tv.svg'
        else:
            p = jaz + p

        item['pic'] = p

        key = response.xpath("//div[@class='tags']/ul/*/a/text()").extract()
        lexicon = dict()
        pars = response.xpath("//div[@id='DynamicContentContainer']//span//text()").extract()
        pars1 = '-'.join(pars)
        with open('ArtScraper/spiders/ALL_lex.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                lexicon[row[0]] = int(row[1])

        # Use lexicon to score tweets
        score = 0
        for word in pars1.split(" "):
            if word in lexicon:
                score = score + lexicon[word]
            #
        item['score'] = score

        item['art_content'] = '-'.join(pars)
        with open("keywords", "a") as f:
            for s in key:
                f.write(str(s) + "\n")

        keywords = ','.join(key)

        item['keywords'] = key

        print("HHHH")
        yield item
