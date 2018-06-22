# -*- coding: utf-8 -*-
import scrapy

from Tencent.items import TencentItem, PositionItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    offset = 0
    base_url = "https://hr.tencent.com/position.php?&start="
    # print(base_url + str(offset))
    # start_urls = [base_url + str(offset)]
    # 充分利用scrapy的高并发，并发量取决于带宽和高并发
    # 通过start_urls构建所有的url地址，并发送出去

    start_urls = ["https://hr.tencent.com/position.php?&start=" + str(page) for page in range(0, 3771, 10)]
    # print(start_urls)

    def parse(self, response):
        node_list = response.xpath('//tr[@class="odd"]|//tr[@class="even"]')
        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract_first()
            item['position_link'] = "https://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = node.xpath("./td[2]/text()").extract_first()
            item['people_number'] = node.xpath("./td[3]/text()").extract_first()
            item['work_location'] = node.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = node.xpath("./td[5]/text()").extract_first()
            # meta的作用是将当前方法里的变量通过字典的方式传递给回调函数，回调函数中通过response.meta属性来获取字典数据
            yield item

            yield scrapy.Request(url=item['position_link'], callback=self.parse_page)

    def parse_page(self, response):
        item = PositionItem()
        item["position_zhize"] = "\n".join(response.xpath("//ul[@class='squareli']")[0].xpath("./li/text()").extract())
        item["position_yaoqiu"] = "\n".join(response.xpath("//ul[@class='squareli']")[1].xpath("./li/text()").extract())

        yield item





