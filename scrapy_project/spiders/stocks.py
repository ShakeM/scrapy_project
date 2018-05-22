# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import StockItem


class ShSpider(scrapy.Spider):
    name = 'sh_spider'
    allowed_domains = ['sse.com.cn']
    custom_settings = {
        "ITEM_PIPELINES": {
            'scrapy_project.pipelines.StockPipeline': 300,
        }
    }
    start_urls = [
        'http://yunhq.sse.com.cn:32041/v1/sh1/list/exchange/equity?select=code,name,open,high,low,last,prev_close,chg_rate,volume,amount,tradephase,change,amp_rate&order=&begin=1&end=9999']

    def parse(self, response):
        response_dict = json.loads(response.text)
        stocks = response_dict['list']

        for s in stocks:
            code = s[0]
            name = s[1]
            yield StockItem(code=code, name=name)

        return


class SzSpider(scrapy.Spider):
    name = 'sz_spider'
    allowed_domains = ['szse.cn']
    custom_settings = {
        "ITEM_PIPELINES": {
            'scrapy_project.pipelines.StockPipeline': 300,
        }
    }

    start_urls = ['http://www.szse.cn/szseWeb/FrontController.szse']
    index = 1
    formdata = {
        'ACTIONID': '7',
        'CATALOGID': '1815_stock',
        'tab1PAGENO': '1'
    }

    def start_requests(self):
        request = scrapy.FormRequest(self.start_urls[0], formdata=self.formdata, callback=self.parse_page)
        yield request

    def parse_page(self, response):
        codes = response.xpath('//*[@id="REPORTID_tab1"]/tr/td[2]/text()').extract()
        names = response.xpath('//*[@id="REPORTID_tab1"]/tr/td[3]/text()').extract()

        if len(codes) == 0:
            return

        for i, c in enumerate(codes):
            code = c
            name = names[i]

            item = StockItem(code=code, name=name)
            yield item

        self.index += 1
        self.formdata["tab1PAGENO"] = str(self.index)

        yield scrapy.FormRequest(self.start_urls[0], formdata=self.formdata, callback=self.parse_page)
