# -*- coding: utf-8 -*-
# import os
import scrapy
import sqlite3
# import bloomfilter
from urllib.parse import urljoin
from ..items import IxdzsItem


class XuhuanSpider(scrapy.Spider):
    name = 'xuhuan'
    allowed_domains = ['aixdzs.com']
    start_urls = ['https://www.aixdzs.com/sort/1/index_0_0_0_1.html']
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 16,
        "DOWNLOAD_DELAY": 1,
        "COOKIES_ENABLED": False,
        "#DOWNLOADER_MIDDLEWARES": {
            'IxdzsSpider.rand_agent.UserAgentMiddleware': 543,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        },
        "ITEM_PIPELINES": {
           'IxdzsSpider.pipelines.ImagePipeline': 298,
           'IxdzsSpider.pipelines.FilePipeline': 299,
           'IxdzsSpider.pipelines.SqlitePipeline': 300,
        },
        "DB_NAME": "xuhuan.sqlite",
        # 图片下载
        # 图片存储路径
        "IMAGES_STORE": "imgs",
        # 图片下载地址
        "IMAGES_URLS_FIELD": "img_src",
        # 文件下载
        # 文件存储路径
        "FILES_STORE": "爱下电子书",
        # 图片下载地址
        "FILES_URLS_FIELD": "fiction_download_url",
    }
    select_result = []
    # def __init__(self):
    #     if os.path.exists("Ixdzs.quchong"):
    #         self.bloom = bloomfilter.Bloomfilter("Ixdzs.quchong")
    #     else:
    #         self.bloom = bloomfilter.Bloomfilter(100000)

    def parse(self, response):
        db_name = ""
        if self.custom_settings["DB_NAME"]:
            db_name = self.custom_settings["DB_NAME"]
        else:
            db_name = "db.sqlite"
        con = sqlite3.connect(db_name)
        sql1 = """
            select fiction_name from xuhuan
        """
        result = con.execute(sql1)
        list1 = result.fetchall()
        for a in list1:
            XuhuanSpider.select_result.append(a[0])
        print(XuhuanSpider.select_result)
        yield scrapy.Request(
            url=response.url,
            callback=self.parse_all_page,
            dont_filter=True,
            meta={}
        )

    def parse_all_page(self, response):
        all_page = response.xpath("//a[text() = '末页']/@href").get()
        all_page = all_page.split("_")[-1].split(".")[0]
        for page in range(1, int(all_page) + 1):
            page_url = response.url.replace("1.html", f"{page}.html")
            print(page_url)
            yield scrapy.Request(
                url=page_url,
                callback=self.parse_one_page,
                dont_filter=True,
                meta={}
            )

    def parse_one_page(self, response):
        fictions = response.xpath("//div[@class='box_k mt15']/ul/li")
        for fiction in fictions:
            fiction_href = fiction.xpath("div[2]/h2/a/@href").get()
            # if self.bloom.test(fiction_href):
            #     print("小说已下载")
            # self.bloom.add(fiction_href)
            # self.bloom.save("Ixdzs.quchong")
            fiction_name = fiction.xpath("div[2]/h2/a/text()").get()
            if not fiction_name or not fiction_href:
                continue
            if fiction_name in XuhuanSpider.select_result:
                print("小说已下载")
                continue
            fiction_href = urljoin(response.url, fiction_href)
            author = fiction.xpath("div[2]/p/span[@class='l1']/a/text()").get()
            words = fiction.xpath("div[2]/p/span[@class='l2']/text()").get()
            words = words[3:]
            status = fiction.xpath("div[2]/p/span[@class='l3']/i/text()").get()
            details = fiction.xpath("div[2]/p[@class='b_intro']/text()").get()
            details = details.strip().replace("\n", "").replace("\r", "")
            time_ = fiction.xpath("div[2]/p/span[@class='l5']/i/text()").get()
            img_src = fiction.xpath("div[1]/a/img/@src").get()
            fiction_download_url = fiction_href + fiction_href.split("/")[-2] + ".epub"
            fiction_download_url = fiction_download_url.replace("https://www", "http://d18").replace("/d/", "/")
            print(fiction_name, fiction_href, author, words, status, details, time_, img_src, fiction_download_url)
            item = IxdzsItem()
            item["fiction_name"] = fiction_name
            item["fiction_href"] = fiction_href
            item["author"] = author
            item["words"] = words
            item["status"] = status
            item["details"] = details
            item["time_"] = time_
            item["img_src"] = [img_src]
            item["fiction_download_url"] = [fiction_download_url]
            item["img_path"] = ""
            item["fiction_path"] = ""
            yield item

    def parse_detail(self, response):
        pass
