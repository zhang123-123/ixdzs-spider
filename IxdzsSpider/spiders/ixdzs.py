# -*- coding: utf-8 -*-
import scrapy


class IxdzsSpider(scrapy.Spider):
    name = 'ixdzs'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
