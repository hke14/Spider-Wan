# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
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
    name = 'crawly'
    allowed_domains = []

    start_urls = ['http://feeds.bbci.co.uk/arabic/rss.xml']



    def parse(self, response):
        # get the subreddit from the URL
        #sub = response.url.split('/')[4]

        #Get the title

        # parse thru each of the posts
        articles = response.xpath('//channel/item')
        #response.selector.register_namespace('media', 'http://search.yahoo.com/mrss/')
        #pics = response.xpath('//channel/item/media:thumbnail/@url').extract()
        print("hello")
        #print(pics[0])
        #i = 0
        for article in articles:
            item = ArtscraperItem()
            print ('hello')
            item['tag']='BBC'
            item['tagu']='https://services.tegrazone.com/sites/default/files/app-icon/6776_asset_iOS_200_forPrint_iOS-Icon.png'
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

            if result1 in 'middleeast':
                result1='middle-east'
            if result1 in 'sports':
                result1='sport'
            if result1 in 'science-and-tech':
                result1='tech'

            item['categorie'] = result1
            pic = article.xpath('media:thumbnail/@url').extract_first()
            item['pic'] = pic
            #i += 1
            url = item['url']


            yield scrapy.Request(
                url,
                callback=self.parse_article,
                meta={'item': item},  # carry over our item
            )


    def parse_article(self, response):
        item = response.meta['item']
        pars = response.xpath("//div[@class='story-body']/div[@class='story-body__inner']/p/text()").extract()
        if not pars:
            pars = response.xpath("//div[@class='story-body']/p/text()").extract()





        lexicon = dict()

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
        item['score']=score

        article = '-'.join(pars)

        item['art_content'] = article

        keywords = response.xpath("//div[@class='tags-container']/ul/*/a/text()").extract()

        keyword = ','.join(keywords)

        item['keywords'] = keyword

        print ("HHHH")
        yield item



