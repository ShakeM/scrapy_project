# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ScrapyProjectPipeline(object):
#     def process_item(self, item, spider):
#         return item

import yagmail
from scrapy_project.util.sql import Database, Stock, update_tables

from config import DATABASE_URL


class StockPipeline(object):
    def __init__(self):
        self.fp = {}
        self.update_count = 0
        self.insert_count = 0

        self.db = Database(DATABASE_URL)
        self.session = self.db.session()

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):

        #
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
        if 'N' in item['name']:
            extra_name = item['name'].replace('N', '')
            item['extra'].append(extra_name)

        # Database
        item['extra'] = str(item['extra'])

        result = self.session.query(Stock).filter(Stock.symbol == item['symbol']).first()
        if result:
            if result.name == item['name']:
                pass
            elif item['name'] in result.name:
                # 上交所纠错
                pass
            else:
                self.update_count += 1

                extra = eval(result.extra)
                result.extra = extra.append(item['name'])
        else:
            self.insert_count += 1

            stock = Stock(**item)
            self.session.add(stock)

    def close_spider(self, spider):
        # Database
        self.session.commit()
        self.session.close()

        update_tables(self.db)

        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        yag.send('18616020643@163.com', '新增数量【' + str(self.insert_count) + '】')
        print('Crawl Stop...' + str(spider.__class__))
