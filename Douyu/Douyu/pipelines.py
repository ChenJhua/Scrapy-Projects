# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
import logging
from scrapy.pipelines.images import ImagesPipeline
from .settings import IMAGES_STORE


class DouyuImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("-"*30)
        print(123123, item['image_link'])
        yield scrapy.Request(item['image_link'])

    def item_completed(self, results, item, info):
        # print(results)
        source_path = IMAGES_STORE + [x['path'] for ok, x in results if ok][0]

        item['image_path'] = IMAGES_STORE + item['nick_name'] + ".jpg"
        try:
            os.rename(source_path, item['image_path'])
        except Exception as e:
            logging.error("Images %s Rename Failed!" % source_path)
            print(e)

        return item


# class DouyuPipeline(object):
#     def process_item(self, item, spider):
#         return item
