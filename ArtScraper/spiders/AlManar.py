from datetime import datetime as dt
import scrapy
import re
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from ArtScraper.items import ArtscraperItem
from scrapy.crawler import CrawlerProcess, CrawlerRunner
import csv
class CNNSpider(scrapy.Spider):


    article = ""
    name = 'y'
    allowed_domains = []

    start_urls = ['http://www.almanar.com.lb/rss']



    def parse(self, response):

        articles = response.xpath('//channel/item')

        print("hello")

        for article in articles:
            item = ArtscraperItem()
            print ('hello')
            item['tag']='AlManar'
            item['tagu']='https://botw-pd.s3.amazonaws.com/styles/logo-thumbnail/s3/0018/9882/brand.gif?itok=S-xSS_yO'
            item['date'] = dt.today()
            item['date_str'] = article.xpath('pubDate/text()').extract_first()
            item['url'] = article.xpath('link/text()').extract_first()
            category1=article.xpath('link/text()').extract_first()
            result = re.search('http://arabic.cnn.com/(.*)/article', category1)
            try :
               result1=result.group(1)
            except:
                result1=None
            item['categorie'] = result1

            item['title'] = article.xpath('title/text()').extract_first()
            article.register_namespace('media', 'http://search.yahoo.com/mrss/')

            url = item['url']


            yield scrapy.Request(
                url,
                callback=self.parse_article,
                meta={'item': item},  # carry over our item
            )


    def parse_article(self, response):
        item = response.meta['item']
        pars = response.xpath("//div[@class='article-content']/p/text()").extract()
        if not pars:
            pars ="Found no content"

        p = response.xpath("//img[@class='img-responsive']/@src").extract_first()
        if not p:

            p = "https://botw-pd.s3.amazonaws.com/styles/logo-thumbnail/s3/0018/9882/brand.gif?itok=S-xSS_yO"

        else:
            p = response.xpath("//img[@class='img-responsive']/@src").extract_first()

        item['pic'] = p


        keywords=response.xpath("//div[@class='article-tags']/a/text()").extract()
        keyword=','.join(keywords)
        item['keywords'] = keywords
        lexicon = dict()

        pars1 = '-'.join(pars)
        with open('/Users/georgesrbeiz/Downloads/News-3-4/ArtScraper/ArtScraper/spiders/ALL_lex.csv', 'r') as csvfile:
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
