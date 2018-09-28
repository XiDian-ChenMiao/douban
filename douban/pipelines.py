# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from douban.settings import MONGO_HOST, MONGO_PORT, MONGO_DB_NAME, MONGO_DB_COLLECTION


class DoubanPipeline(object):
    """
    deal with the item from spider
        :param object: 
    """
    def __init__(self):
        host = MONGO_HOST
        port = MONGO_PORT
        dbname = MONGO_DB_NAME
        collection = MONGO_DB_COLLECTION
        client = MongoClient(host=host, port=port)
        db = client[dbname]
        self.post = db[collection]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
