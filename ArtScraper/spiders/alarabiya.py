
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
    name = 'arabiya'
    allowed_domains = []

    start_urls = ['https://www.alarabiya.net/.mrss/ar.xml']



    def parse(self, response):

        articles = response.xpath('//channel/item')

        for article in articles:
            item = ArtscraperItem()
            print ('hello')
            item['tag']='Albayan'
            item['tagu']='https://cache.albayan.ae/polopoly_fs/7.3261637.1541065594!/image/image.png_gen/derivatives/default/image.png'
            item['date'] = dt.today()
            item['date_str'] = article.xpath('pubDate/text()').extract_first()
            item['url'] = article.xpath('link/text()').extract_first()
            item['title'] = article.xpath('title/text()').extract_first()
            article.register_namespace('media', 'http://search.yahoo.com/mrss/')
            catergories = article.xpath('guid/text()').extract_first()


            result = re.search('http://www.bbc.co.uk/arabic/(.*)-', catergories)




            try :
               result1=result.group(1)
            except:
                result1=None
            item['categorie'] = result1


            url = item['url']


            yield scrapy.Request(
                url,
                callback=self.parse_article,
                meta={'item': item},  # carry over our item
            )

    def parse_article(self, response):
        item = response.meta['item']




        p = response.xpath("body/section[2]/section[1]/div[1]/article[1]/figure[1]/img[1]/@src").extract_first()
        if not p:
            p = 'https://cache.albayan.ae/polopoly_fs/7.3261637.1541065594!/image/image.png_gen/derivatives/default/image.png'
        else:
            p=p

        item['pic'] = p

        key = response.xpath("//div[@class='tags']/ul/*/a/text()").extract()
        lexicon = dict()
        pars= response.xpath("//*[@id='articledetails']/p/text()").extract()
        pars1='-'.join(pars)
        with open('ALL_lex.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                lexicon[row[0]] = int(row[1])

        # Use lexicon to score tweets
        score = 0
        for word in pars1.split(" "):
            if word in lexicon:
                score = score + lexicon[word]
            #
        item['score']=score



        item['art_content'] ='-'.join(pars)

        keywords = ','.join(key)

        item['keywords'] = keywords

        print ("HHHH")
        yield item



