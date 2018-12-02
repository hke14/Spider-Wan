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
    name = 'middle'
    allowed_domains = []

    start_urls = [
        "https://arabic.cnn.com/api/v1/rss/middle-east/rss.xml/"


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
            item['categorie'] = "middle-east"

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

        temp = open("/Users/georgesrbeiz/Downloads/News-3-4/ArtScraper/ArtScraper/keywords", 'r').read().splitlines()

        print(temp)

        # contained = [x for x in temp if x in article]
        #
        # contained = list(set(contained))
        #
        # with open("match", "a") as f:
        #     for s in contained:
        #         f.write(str(s) + "\n")
        #
        # keywords = ','.join(contained)
        #
        # print(keywords)

        keywords=response.xpath("//footer[@class='clearfix _1MbEDqOhpQ']/ul/*/a/text()").extract()
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

        temp = open("/Users/georgesrbeiz/Downloads/News-3-4/ArtScraper/ArtScraper/keywords", 'r').read().splitlines()




        item['art_content'] = '-'.join(pars)

        print ("HHHH")
        yield item
