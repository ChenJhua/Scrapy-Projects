# -*- coding: utf-8 -*-
import scrapy
import json
from Douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['douyucdn.cn']

    global base_url
    base_url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?&limit=100&offset="

    offset = 0
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = json.loads(response.body.decode())['data']

        if not node_list:
            return

        for node in node_list:
            item = DouyuItem()

            item['room_link'] = 'http://www.douyu.com/' + node['room_id']
            item['image_link'] = node['vertical_src']
            item['nick_name'] = node['nickname']
            item['anchor_city'] = node['anchor_city']

            yield item
        self.offset += 100
        yield scrapy.Request(url=base_url+str(self.offset), callback=self.parse)
