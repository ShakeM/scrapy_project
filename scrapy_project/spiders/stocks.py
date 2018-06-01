# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import StockItem


class StockSpider(scrapy.Spider):
    name = 'stock_spider'
    allowed_domains = ['xueqiu.com', 'szse.cn']
    custom_settings = {
        "ITEM_PIPELINES": {
            'scrapy_project.pipelines.StockPipeline': 300,
        }
    }
    index = 1
    formdata = {
        'ACTIONID': '7',
        'CATALOGID': '1815_stock',
        'tab1PAGENO': '1'
    }
    sh_url = 'https://xueqiu.com/stock/quote_order.json?size=90&order=desc&exchange=CN&stockType=sha&column=symbol%2Cname%2Ccurrent%2Cchg%2Cpercent%2Clast_close%2Copen%2Chigh%2Clow%2Cvolume%2Camount%2Cmarket_capital%2Cpe_ttm%2Chigh52w%2Clow52w%2Chasexist&orderBy=percent&_=1527824619829&page='
    sz_url = 'http://www.szse.cn/szseWeb/FrontController.szse'

    def start_requests(self):
        cookies = {'xq_a_token': "7023b46a2c20d7b0530b4e9725f7f869c8d16e7d"}

        for i in range(21):
            url = self.sh_url + str(i)
            request = scrapy.http.Request(url=url, cookies=cookies)
            yield request

        # B股
        url_b = 'https://xueqiu.com/stock/quote_order.json?page=1&size=90&order=desc&exchange=CN&stockType=shb&column=symbol%2Cname%2Ccurrent%2Cchg%2Cpercent%2Clast_close%2Copen%2Chigh%2Clow%2Cvolume%2Camount%2Cmarket_capital%2Cpe_ttm%2Chigh52w%2Clow52w%2Chasexist&orderBy=percent&_=1527829027884'
        request = scrapy.http.Request(url=url_b, cookies=cookies)
        yield request

    def parse(self, response):
        yield StockItem(code="000001", name="上证指数", symbol="SH000001", extra=["上证", "A股"])
        yield StockItem(code="000300", name="沪深300", symbol="SH000300", extra=["399300"])
        yield StockItem(code="399001", name="深证成指", symbol="SZ399001", extra=["深圳指数"])
        yield StockItem(code="399005", name="中小板指", symbol="SZ399005", extra=["中小板指数"])
        yield StockItem(code="399006", name="创业板指", symbol="SZ399006", extra=["创业板指数"])

        # Shanghai stock
        response_dict = json.loads(response.text)
        stocks = response_dict['data']
        print(stocks)

        for s in stocks:
            code = s[0].replace('SH', '')
            name = s[1]
            yield StockItem(code=code, name=name, symbol='SH' + code)

        start_urls = 'http://www.szse.cn/szseWeb/FrontController.szse'
        request = scrapy.FormRequest(self.sz_url, formdata=self.formdata, callback=self.parse_sz_page)

        yield request

    def parse_sz_page(self, response):
        codes = response.xpath('//*[@id="REPORTID_tab1"]/tr/td[2]/text()').extract()
        names = response.xpath('//*[@id="REPORTID_tab1"]/tr/td[3]/text()').extract()

        if len(codes) == 0:
            return

        for i, c in enumerate(codes):
            code = c
            name = names[i]

            item = StockItem(code=code, name=name, symbol='SZ' + code)
            yield item

        self.index += 1
        self.formdata["tab1PAGENO"] = str(self.index)

        yield scrapy.FormRequest(self.sz_url, formdata=self.formdata, callback=self.parse_sz_page)
