import logging
import pymongo
from scrapy.exceptions import DropItem


class MongoPipeline(object):

    collection_name = 'articles'

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




        bbcDict = {}
        if item['title'] in self.title_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            bbcDict['art_content'] = item['art_content']
            bbcDict['date'] = item['date']
            bbcDict['date_str'] = item['date_str']
            bbcDict['title'] = item['title']
            bbcDict['url'] = item['url']
            bbcDict['pic']=item['pic']
            bbcDict['tag']=item['tag']
            self.title_seen.add(item['title'])
            title = item['title']
            bbcDict['categorie'] = item['categorie']
            self.db[self.collection_name].update_one({"title": title}, {"$set": {"art_content": item['art_content'], "date": item['date'], "date_str": item['date_str'], "title": item['title'], "url": item['url'], "pic": item['pic'],"tag": item['tag'],"categorie":item['categorie']}}, upsert=True)
            return item

       # self.db[self.collection_name].insert(dict(item))
       # logging.debug("Post added to MongoDB")
       # return item