# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from datetime import datetime as dt
import scrapy
from ArtScraper.items import ArtscraperItem

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
            item['date'] = dt.today()
            item['date_str'] = article.xpath('pubDate/text()').extract_first()
            item['url'] = article.xpath('link/text()').extract_first()
            item['title'] = article.xpath('title/text()').extract_first()
            article.register_namespace('media', 'http://search.yahoo.com/mrss/')
            pic = article.xpath('media:thumbnail/@url').extract_first()
            item['pic'] = pic
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
        pars = response.xpath("//div[@class='story-body']/div[@class='story-body__inner']/p/text()").extract()
        if not pars:
            pars = response.xpath("//div[@class='story-body']/p/text()").extract()
        item['art_content'] = '-'.join(pars)
        print ("HHHH")
        yield item