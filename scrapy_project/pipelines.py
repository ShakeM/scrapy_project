# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ScrapyProjectPipeline(object):
#     def process_item(self, item, spider):
#         return item

from scrapy.exporters import JsonLinesItemExporter
from .spiders.stocks import StockSpider
import os
import arrow


class StockPipeline(object):
    def __init__(self):
        self.fp = {}
        self.exporter = {}
        self.output_path = ''
        self.full_time = arrow.now().format('YYYY-MM-DD_HH-mm-ss_X')

    def open_spider(self, spider):
        # Make output folder
        this_folder_path = os.path.dirname(__file__)
        self.output_path = os.path.join(this_folder_path, 'output')

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        file_name = 'stock_%s.json' % self.full_time

        self.fp = open(os.path.join(self.output_path, file_name), 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        print('Crawl Start...' + str(spider.__class__))

    def process_item(self, item, spider):

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

    def close_spider(self, spider):
        print('Crawl Stop...' + str(spider.__class__))


class IndexPipeline(object):
    def __init__(self):
        self.fp = {}
        self.exporter = {}
        self.output_path = ''
        self.full_time = arrow.now().format('YYYY-MM-DD_HH-mm-ss_X')

    def open_spider(self, spider):
        # Make output folder
        this_folder_path = os.path.dirname(__file__)
        self.output_path = os.path.join(this_folder_path, 'output')

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        file_name = 'index_%s.json' % self.full_time
        # Save
        self.fp = open(os.path.join(self.output_path, file_name), 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        print('Crawl Start...' + str(spider.__class__))

    def process_item(self, item, spider):
        print(item)
        self.exporter.export_item(item)
