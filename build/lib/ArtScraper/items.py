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
    tag = scrapy.Field()
    categorie = scrapy.Field()
    tagu=scrapy.Field()
    keywords=scrapy.Field()
    score=scrapy.Field()
    frequency=scrapy.Field()
    #ctaegories
    datec = scrapy.Field()
    date_strc = scrapy.Field()
    urlc = scrapy.Field()
    titlec = scrapy.Field()
    art_contentc = scrapy.Field()
    picc = scrapy.Field()
    tagc = scrapy.Field()
    categoriec = scrapy.Field()
    taguc = scrapy.Field()
    keywordsc = scrapy.Field()
    scorec = scrapy.Field()
