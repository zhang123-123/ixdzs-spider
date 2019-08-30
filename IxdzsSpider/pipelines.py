# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline


class IxdzsspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    # def file_path(self, request, response=None, info=None):
    #     url = request.url
    #     file_type = url.split(".")[-1]
    #     a = url.split("/")[-1]
    #     path_name = f'full/{a}.{file_type}'
    #     return path_name

    def item_completed(self, results, item, info):
        if results[0][1]:
            item["img_path"] = "imgs/" + results[0][1]["path"]
        else:
            item["img_path"] = "图片下载失败"
        print("11111111", results)
        # item["img_path"] = "imgs" + results[0][1]["path"]
        return item


class FilePipeline(FilesPipeline):
    def item_completed(self, results, item, info):
        print("333333", results)
        if results[0][1]:
            item["fiction_path"] = "爱下电子书/" + results[0][1]["path"]
        else:
            item["fiction_path"] = "小说下载失败"
        return item


class SqlitePipeline(object):
    def __init__(self, db_name):
        if not db_name:
            db_name = "db.sqlite"
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def close_spider(self):
        self.cur.close()
        self.con.close()
        self.cur = None
        self.con = None

    def process_item(self, item, spider):
        key_info = ""
        value_type = ""
        keys = ""
        values = []
        for key, value in item.items():
            if isinstance(value, str):
                value_type = "varchar(255)"
            elif isinstance(value, int):
                value_type = "integer"
            elif isinstance(value, float):
                value_type = "float"
            elif isinstance(value, list):
                value = value[0]
                value_type = "varchar(255)"
            key_info += f"{key} {value_type},"
            keys += f"{key},"
            values.append(value)
        key_info = key_info[:-1]
        keys = keys[:-1]
        sql1 = f"""create table if not exists {spider.name}(
            id integer primary key autoincrement,
            {key_info}
        )"""
        self.cur.execute(sql1)
        wenhao = "?," * len(values)
        sql2 = f"""
           insert into {spider.name} ({keys}) values ({wenhao[:-1]})
        """
        print(sql1)
        print(sql2)
        print(values)
        self.cur.execute(sql2, values)
        self.con.commit()

        return item

    @classmethod
    def from_settings(cls, settings):
        db_name = settings['DB_NAME']
        return cls(db_name)

