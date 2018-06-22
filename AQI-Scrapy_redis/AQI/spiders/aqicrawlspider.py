# coding=utf-8

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from AQI.items import AqiItem


class AqiCrawlSpider(CrawlSpider):
    name = 'aqicrawlspider'
    allowed_domains = ['aqistudy.cn']

    base_url = "https://www.aqistudy.cn/historydata/"
    global base_url
    start_urls = [base_url]

    rules = [
        # 发送每个城市的链接，返回该城市所有月份的响应
        Rule(LinkExtractor(allow=r'monthdata')),
        # 提取某个城市所有月份的链接并发送，返回该月所有天的数据
        Rule(LinkExtractor(allow=r'daydata'), callback="parse_day"),
    ]

    def parse_day(self, response):
        # 根据标题下标获取城市名
        title = response.xpath("//h2[@id='title']/text()").extract_first()
        city_name = title[:title.find(u'空气')]

        node_list = response.xpath('//tbody/tr')
        node_list.pop(0)
        for node in node_list:
            item = AqiItem()
            item['city'] = city_name
            item['date'] = node.xpath('./td[1]/text()').extract_first()
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            item['level'] = node.xpath('./td[3]/span/text()').extract_first()
            item['pm2_5'] = node.xpath('./td[4]/text()').extract_first()
            item['pm10'] = node.xpath('./td[5]/text()').extract_first()
            item['so2'] = node.xpath('./td[6]/text()').extract_first()
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            item['no2'] = node.xpath('./td[8]/text()').extract_first()
            item['o3'] = node.xpath('./td[9]/text()').extract_first()
            yield item

