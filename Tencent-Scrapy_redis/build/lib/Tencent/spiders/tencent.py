# -*- coding: utf-8 -*-
import scrapy

from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    offset = 0
    # start_urls = [base_url + str(offset)]
    # 充分利用scrapy的高并发，并发量取决于带宽和高并发
    # 通过start_urls构建所有的url地址，并发送出去
    # start_urls = [base_url_a+"0"]
    b_url = "https://hr.tencent.com/position.php?&start="
    global b_url
    start_urls = [b_url + str(i) for i in range(0, 3771, 10)]
    # start_urls = ["https://hr.tencent.com/position.php?&start=" + str(i) for i in range(0, 3771, 10)]

    # start_us = [str(page) for page in range(0, 3771, 10)]
    # start_urls = []
    # for s in start_us:
    #     start_urls.append(base_url+s)
    print(start_urls)

    def parse(self, response):
        node_list = response.xpath('//tr[@class="odd"]|//tr[@class="even"]')
        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract_first()
            item['position_link'] = node.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = node.xpath("./td[2]/text()").extract_first()
            item['people_number'] = node.xpath("./td[3]/text()").extract_first()
            item['work_location'] = node.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = node.xpath("./td[5]/text()").extract_first()

            yield item

        # if self.offset < 3830:
        #     self.offset += 10
        #     url = self.base_url + str(self.offset)
        #     yield scrapy.Request(url, callback=self.parse)

        # 如果返回真则表示到了最后一页；如果返回None，表示还没到最后一页
        # 通过下一页连接处理多页，只用于可以点击下一页的情况，并不能使用高并发
        # if not response.xpath("//a[@class='noactive' and @id='next']").extract_first():
        #     next_url = "https://hr.tencent.com/" + response.xpath("//a[@id='next']/@href").extract_first()
        #     yield scrapy.Request(next_url, callback=self.parse)
