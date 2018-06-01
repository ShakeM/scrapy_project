# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ScrapyProjectPipeline(object):
#     def process_item(self, item, spider):
#         return item

from scrapy.exporters import JsonLinesItemExporter
import os
import arrow
import yagmail
from scrapy_project.util.sql import Database, Stock


class StockPipeline(object):
    def __init__(self):
        self.fp = {}
        self.exporter = {}
        self.output_path = ''
        self.file_name = 'stock_%s.json' % arrow.now().format('YYYY-MM-DD_HH-mm-ss__X')
        self.new_count = 0
        self.count = 0

        self.session = Database().session()

    def open_spider(self, spider):
        # Make output folder
        this_folder_path = os.path.dirname(__file__)
        self.output_path = os.path.join(this_folder_path, 'output')

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        self.fp = open(os.path.join(self.output_path, self.file_name), 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        print('Crawl Start...' + str(spider.__class__))

    def process_item(self, item, spider):
        self.count += 1
        item['name'] = item['name'].replace('Ａ', 'A').replace('Ｂ', 'B').replace(' ', '')
        item['name'] = item['name'].replace('XD', '').replace('XR', '').replace('DR', '')
        item['extra'] = []

        # Extra stock name
        if 'B股' in item['name']:
            extra_name = item['name'].replace('B股', 'B')
            item['extra'].append(extra_name)
        if 'A' in item['name']:
            extra_name = item['name'].replace('A', '')
            item['extra'].append(extra_name)
        if '*' in item['name']:
            extra_name = item['name'].replace('*', '')
            item['extra'].append(extra_name)

        self.exporter.export_item(item)

        # Database
        item['extra'] = str(item['extra'])
        if not self.session.query(Stock).filter_by(**item).all():
            stock = Stock(**item)
            self.session.add(stock)
            self.new_count += 1

    def close_spider(self, spider):
        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        file_path = os.path.join(self.output_path, self.file_name).replace('\\', '/').replace('/', '//')
        yag.send('18616020643@163.com', '【' + str(self.new_count) + '】【' + str(self.count) +'】'+ self.file_name, file_path)
        print('Crawl Stop...' + str(spider.__class__))

        # Database
        self.session.commit()
        self.session.close()


class IndexPipeline(object):
    def __init__(self):
        self.fp = {}
        self.exporter = {}
        self.output_path = ''
        self.file_name = 'index_%s.json' % arrow.now().format('YYYY-MM-DD_HH-mm-ss__X')
        self.count = 0

    def open_spider(self, spider):
        # Make output folder
        this_folder_path = os.path.dirname(__file__)
        self.output_path = os.path.join(this_folder_path, 'output')

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        # Save
        self.fp = open(os.path.join(self.output_path, self.file_name), 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        print('Crawl Start...' + str(spider.__class__))

    def process_item(self, item, spider):
        self.count += 1
        print(item)
        self.exporter.export_item(item)

    def close_spider(self, spider):
        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        file_path = os.path.join(self.output_path, self.file_name).replace('\\', '/').replace('/', '//')
        yag.send('18616020643@163.com', '【' + str(self.count) + '】' + self.file_name, file_path)
        print('Crawl Stop...' + str(spider.__class__))
