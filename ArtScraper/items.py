# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    date_str = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    art_content = scrapy.Field()
    pic =scrapy.Field()

