# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IxdzsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class IxdzsItem(scrapy.Item):
    fiction_name = scrapy.Field()
    fiction_href = scrapy.Field()
    author = scrapy.Field()
    words = scrapy.Field()
    status = scrapy.Field()
    details = scrapy.Field()
    time_ = scrapy.Field()
    img_src = scrapy.Field()
    fiction_download_url = scrapy.Field()

    img_path = scrapy.Field()
    fiction_path = scrapy.Field()

