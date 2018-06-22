# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TencentPipeline(object):
    # 爬虫启动时执行一次
    def open_spider(self, spider):
        self.f = open("tencent.json", "w")

    # 必须实现的，用来处理每一个item数据
    def process_item(self, item, spider):
        item = json.dumps(dict(item))
        self.f.write(item + "\n")
        return item

    # 爬虫关闭时执行一次
    def close_spider(self, spider):
        self.f.close()


