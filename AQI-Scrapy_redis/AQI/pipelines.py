# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import json
from scrapy.exporters import CsvItemExporter
import pymongo
import redis


class AqiPipeline(object):
    def process_item(self, item, spider):
        item['time'] = str(datetime.utcnow())
        item['source'] = spider.name
        return item


class AqiJsonPipeline(object):
    def open_spider(self, spider):
        self.f = open("aqi.json", "w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item)) + "\n"
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()


class AqiCsvPipeline(object):
    def open_spider(self, spider):
        # 创建文件对象
        self.f = open("aqi.csv", "wb")
        # 创建csv文件读写对象，用来将item数据写入到指定的文件中
        self.csv_exporter = CsvItemExporter(self.f)
        # 开始csv数据读写
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        # 将item数据通过csv文件读写对象，写入到csv文件中
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 结束csv文件读写
        self.csv_exporter.finish_exporting()
        # 关闭文件，将内存缓冲区的数据写入到磁盘中
        self.f.close()


class AqiMongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db = self.client['AQI_DATA']
        self.collection = self.db['aqi']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class AqiRedisPipeline(object):
    def open_spider(self, spider):
        self.client = redis.Redis(host="127.0.0.1", port=6379)

    def process_item(self, item, spider):
        content = json.dumps(dict(item))
        self.client.lpush("aqi", content)
        return item

