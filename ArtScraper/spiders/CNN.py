from datetime import datetime as dt
import scrapy
import re
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from ArtScraper.items import ArtscraperItem
from scrapy.crawler import CrawlerProcess, CrawlerRunner

class CNNSpider(scrapy.Spider):


    article = ""
    name = 'craw'
    allowed_domains = []

    start_urls = ['https://arabic.cnn.com/api/v1/rss/middle-east/rss.xml']



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
            item['tag']='https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwj035DStrveAhVEWBoKHeFGC4UQjRx6BAgBEAU&url=https%3A%2F%2Farabic.cnn.com%2F&psig=AOvVaw1mC94uTkLfynpQpO6NQK0a&ust=1541444529463748'
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
            #i += 1
            url = item['url']
            #xpath("//w:gridCol", namespaces={
            #    'w': 'http://schemas.microsoft.com/office/word/2003/wordml',
            #})

            yield scrapy.Request(
                url,
                callback=self.parse_article,
                meta={'item': item},  # carry over our item
            )
            #request = scrapy.Request(url, callback=self.parse_article)
            #request.meta['item'] = item
            #yield request

    def parse_article(self, response):
        item = response.meta['item']
        pars = response.xpath("//div[@class='clearfix wysiwyg _2A-9LYJ7eK']/p/text()").extract()
        if not pars:
            pars ="Found no content"
        item['art_content'] = '-'.join(pars)
        item['pic'] = response.xpath("//picture[@class='picture']/img[@class='default-image flipboard-image']/@src").extract()
        print ("HHHH")
        yield item
