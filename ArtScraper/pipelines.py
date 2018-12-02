import logging
from typing import BinaryIO

import pymongo
from scrapy.exceptions import DropItem
import os


class MongoPipeline(object):
    collection_name = 'articles'
    collection_name1 = 'false_keywords'
    collection_name2='world'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.title_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        ## how to handle each post

            if item['title'] in self.title_seen:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.title_seen.add(item['title'])
                title = item['title']
                self.db[self.collection_name].update_one({"title": title}, {
                    "$set": {"art_content": item['art_content'], "date": item['date'], "date_str": item['date_str'],
                             "title": item['title'], "url": item['url'], "pic": item['pic'], "tag": item['tag'],
                             "categorie": item['categorie'], "tagu": item['tagu'], "keywords": item['keywords'],"score" :item['score']}},
                                                         upsert=True)
                # self.db[self.collection_name].update_one({"title": title}, {
                #     "$set": {"art_content": item['art_contentc'], "date": item['datec'], "date_str": item['date_strc'],
                #              "title": item['title'], "url": item['urlc'], "pic": item['picc'], "tag": item['tagc'],
                #              "categorie": item['categoriec'], "tagu": item['taguc'], "keywords": item['keywordsc'],
                #              "score": item['scorec']}},
                #                                           upsert=True)

                keywords = item['keywords']
                for keyword in keywords:
                    if self.db[self.collection_name1].find({"keyword": keyword}).count() > 0:
                        #increment frequency
                        self.db[self.collection_name1].update(
                            {"keyword": keyword},
                            {"$inc" : {"frequency": int(1)}}
                        )
                    else:
                        self.db[self.collection_name1].update_one({"keyword": keyword},
                                                                  {"$set": {"keyword": keyword, "frequency": 1}},
                                                                  upsert=True)
                # self.db[self.collection_name].update(
                #     {},
                #     {"$set": {"related_articles": []}},
                #     upsert=True, multi=True
                # )


            return item
