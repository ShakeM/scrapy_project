# -*- coding: utf-8 -*-
import scrapy
from ..items import IndexItem
import yagmail

import os, json, re
from scrapy_project.util import verify
from functools import reduce


class BaiduIndexSpider(scrapy.Spider):
    name = 'baidu_index'
    allowed_domains = ['baidu.com']
    start_urls = ['']

    cookies = [
        {
            "BDUSS": "1hMlV6ZVl4WnBqd0x5bmF-TWVac1RmRjU3NGFrb1BINVF3RkV0UUlNTi1TfnRaTVFBQUFBJCQAAAAAAAAAAAEAAAA8cC7Gua3B6cvJtcS5ysrCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH6-01l-vtNZZU;"},
        {
            "BDUSS": "0hUWU5oSlVub2RKNjBpSHNESGZoZk9rQVhJLS1SU1JkTFJnbGRVY29sYW1TfnRaSVFBQUFBJCQAAAAAAAAAAAEAAACARy7G1bKzve-~AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKa-01mmvtNZZ;"},
        {
            "BDUSS": "ndMNTNmVmZDRWY4V2VvaWNFUzgwT1JMLTl2NGd5V2RLNUR5ZkJUZWtGdDdTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAAAncC7GvOHOysT9y6vX0wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHu-01l7vtNZU;"},
        {
            "BDUSS": "k9HRlF4WWNoREkxdXBsUkpIc3g0NnVCQzI4TkdaNlo4MnRVLUcwZHNHbDZTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAABURi7GxeHStryqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHq-01l6vtNZf;"},
        {
            "BDUSS": "1h1VlJ0N3RFfjRnU2NGbi1VZnFnfjNVaHRVeWlZMG5mdkRFUnBiMX54ZzRraGxhTVFBQUFBJCQAAAAAAAAAAAEAAAB9b3TJxKb0yYNoucjH2wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgF8lk4BfJZZ;"},
        {
            "BDUSS": "VLeGk0UFRFaU9tLUhDQmFaMWJFd2ktQ0k3fkxJWUR5TnNETHYwV25wczVraGxhTVFBQUFBJCQAAAAAAAAAAAEAAABWTnTJb2u-o9bZyuYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADkF8lk5BfJZbn;"},
        {
            "BDUSS": "l0TkR-fms3OTBtdzZNcn4tVUZWc0xlem5XUkEzYzBlMTJEbWw1LVlSN2RraGxhTVFBQUFBJCQAAAAAAAAAAAEAAAC-UXTJZ2~S84HMyLsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN0F8lndBfJZdn;"},
        {
            "BDUSS": "Fp6dExzMVNiN0F4N3NXSkhOSkJHQjFpZVBGUkRoTWgtZ3hrLW1uaXdjZmZraGxhTVFBQUFBJCQAAAAAAAAAAAEAAADFUXTJsNfR8rXHusbltAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN8F8lnfBfJZW;"},
        {
            "BDUSS": "ERIS1dPeU9JWXRBeXhJRnE0dGpCUnJmRHJZVkxNRjJwSGxOTVVXeEpBa2hreGxhTVFBQUFBJCQAAAAAAAAAAAEAAABDU3TJyOXRxbXEt-K6zeL5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEG8lkhBvJZe;"},
        {
            "BDUSS": "1d1bGFkZzRsMn44fk5ScU5DVzBBWFg5eS1Yb0xKa1FqR2ZTcDh3WkotVWpreGxhTVFBQUFBJCQAAAAAAAAAAAEAAABNU3TJsdnUxs611q646AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACMG8lkjBvJZR;"},
        {
            "BDUSS": "UycW1xYWQzdkVrNjhSdUZ4fnFpNEtkREt5a1JURUxlNGZrN0ZseXN1c2hreGxhTVFBQUFBJCQAAAAAAAAAAAEAAABAU3TJuvHcx9HFdGltZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEG8lkhBvJZa2;"},
        {
            "BDUSS": "UJzVDQ3MEFDRnlEQThKNEg2UDQzTG53RW9nRkxvSnVJRjY1TnZZaGw0OXdraGxhSVFBQUFBJCQAAAAAAAAAAAEAAAC~cHTJzOzQq9LCsLLWvgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAF8llwBfJZb;"},
        {
            "BDUSS": "0wVjEwZEdsbDBFRDdwQnVLcmlhanhZUHBiaXlhcHU4aVBCQktrenozQ2lreGxhTVFBQUFBJCQAAAAAAAAAAAEAAACLaXTJwabSucO3ZnJlZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKIG8lmiBvJZeG;"},
        {
            "BDUSS": "m1lWENQcDAzZ0tBRFNhWFdiQnI0VkpyelZYeEhFR0VCTXcwaHJsZ2hHZHFsQmxhTVFBQUFBJCQAAAAAAAAAAAEAAAAFe3TJ6trK6bX7tKvG5gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGoH8llqB~JZc;"},
        {
            "BDUSS": "Ex6Uk9IaFMycWpGOTcyMGgzenpCSTA0V1IzWG9KU3JzY345eXZvTXA3NUtsUmxhTVFBQUFBJCQAAAAAAAAAAAEAAAChlnTJt6rI49TGzOzo0gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEoI8llKCPJZe;"},
        {
            "BDUSS": "NLcHBPUWhjalo0SFFveTR2ZDZXY3JsflhHOURtfmVlNDBLa3pud0xWTDlsUmxhTVFBQUFBJCQAAAAAAAAAAAEAAABe0XTJc2t52a6yycGrAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP0I8ln9CPJZR0;"},
        {
            "BDUSS": "V6Q3VGQ3dHVUNwNGQ4eVU2TmF3TXMtQUFONjA3cUVvfllpSWh1SjcxQ0FsUmxhTVFBQUFBJCQAAAAAAAAAAAEAAADGl3TJZmx5w6~EycC8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAI8lmACPJZTl;"},
        {
            "BDUSS": "JraDlsb1cwaVBra3RCaDlFQVN5WE1XTGpxLXJpZG92TmpiLTlRamlCai1sUmxhSVFBQUFBJCQAAAAAAAAAAAEAAADBqHTJs6y8tu~xxO7R4wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP4I8ln-CPJZUT;"},
        {
            "BDUSS": "JjTjdnRGhlOHAyTVNIU0w5NFpaRGxielYyZjIzNDFqLU53VElRa35vTH5sUmxhTVFBQUFBJCQAAAAAAAAAAAEAAAB76HTJy-XS1M2utcTAz7OyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP8I8ln~CPJZfl;"},
        {
            "BDUSS": "N-NHBDaUcxRlZLTkZlQ09NOHgyQ091YnhEUG9QNEVEc1ZQb1NxR0JHdmNsaGxhTVFBQUFBJCQAAAAAAAAAAAEAAAAo7XTJxKrP47vcZ3JlYXQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANwJ8lncCfJZUV;"},
        {
            "BDUSS": "V6czczSVNkRkpkb0NxYkJmY3lnd1dybjRtZHM2YlF5UzF5SWtoYndNcmJsaGxhSVFBQUFBJCQAAAAAAAAAAAEAAAAi7XTJ0v7H7cqrc3VubnkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANsJ8lnbCfJZZ1;"},
        {
            "BDUSS": "NadkpydzZRa0RpLXJPLUN-NnVBU0VJYU9KNnM0QkRveEQ1OGxmTzBKZDJseGxhTVFBQUFBJCQAAAAAAAAAAAEAAABty3TJwM3CzLqjbGlmZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHYK8ll2CvJZUD;"},
        {
            "BDUSS": "h6MVREU3UzREUtZFl0UHhGNnFYTVhReEJjcUUwcXJ5VX5vSVo0c2VoRDJseGxhTVFBQUFBJCQAAAAAAAAAAAEAAACA23TJy6zAyrXEs9nD7ua6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPYK8ln2CvJZY1;"},
        {
            "BDUSS": "2l2RTNnbTNUQjM2MlJwN3lCRlNmSkNzamVRV1BNdkJhamhkek8wcEdhRDJseGxhTVFBQUFBJCQAAAAAAAAAAAEAAACC23TJyf7Q49bxZ3JlYXQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPYK8ln2CvJZc;"}
    ]

    index = 0
    custom_settings = {
        # "DOWNLOADER_MIDDLEWARES": {
        #     'scrapy_project.middlewares.BaiduDownloaderMiddleware': 543,
        # },
        "ITEM_PIPELINES": {
            'scrapy_project.pipelines.IndexPipeline': 300,
        }
    }

    def start_requests(self):
        # Read output
        this_folder = os.path.dirname(__file__)
        parent_folder = os.path.dirname(this_folder)
        output_path = os.path.join(parent_folder, 'output')

        file_name = self.get_newest_stock_file()
        file_path = os.path.join(output_path, file_name)
        print(os.path.exists(file_name))

        fp = open(file_path, 'r', encoding='utf-8')
        lines = fp.readlines()

        words = []
        for l in lines:
            obj = json.loads(l)
            words.append(obj['code'])
            words.append(obj['name'])
            words += obj['extra']

        # Group 5
        five_words = []
        for i in range(len(words)):
            five = words[i * 5:i * 5 + 5]
            if not five: break
            five_words.append(five)

        # Create 0-9 a-z
        demo_words = list(range(10))
        for i in range(26):
            demo_words.append(chr(i + ord('a')))

        # Group 5
        for i in range(len(demo_words)):
            five = demo_words[i * 5:i * 5 + 5]
            if not five: break
            five_words.append(five)

        for f in five_words:
            url = self.__join_url(f)
            cookie = self.get_cookie()
            request = scrapy.http.Request(url=url, callback=self.get_password, meta={'cookie': cookie})
            request.cookies = cookie
            yield request

    def get_password(self, response):
        cookie = response.meta['cookie']
        data_json = json.loads(response.text)
        uniqid = data_json['uniqid']

        request = scrapy.http.Request(url='http://index.baidu.com/Interface/api/ptbk?uniqid=' + uniqid,
                                      meta={'data': data_json['data']},
                                      callback=self.parse_json)
        request.cookies = cookie
        yield request

    def parse_json(self, response):
        password = json.loads(response.text)['data']

        data = response.meta['data']
        for obj in data:
            index = obj['index'][0]
            index['_pc'] = self.__decipher(index['_pc'], password)
            index['_all'] = self.__decipher(index['_all'], password)
            index['_wise'] = self.__decipher(index['_wise'], password)
            item = IndexItem(word=obj['key'],
                             period=obj['index'][0]['period'],
                             pc=index['_pc'],
                             all=index['_all'],
                             wise=index['_wise'],
                             )
            # print(item)
            yield item

    def __decipher(self, ciphertext, password):
        """
        >>> BaiduIndexSpider().__decipher('8N8NIN0NsN0N0NoNoNINyNoNoNhN-NIN-NINONhNhN8N-Ns','k8.y-Oh0N2IZsog.5-07861,+4%329')
        '5,5,4,1,3,1,1,2,2,4,0,2,2,6,7,4,7,4,8,6,6,5,7,3'
        """
        length = int(len(password) / 2)

        psw_dict = {}
        for i in range(length):
            psw_dict[password[i]] = password[length + i]

        text_list = list(ciphertext)
        result = []
        for text in text_list:
            text and result.append(psw_dict[text])

        result_str = "".join(result)
        return result_str

    def __join_url(self, words):
        # 全国 北京 上海 广州 深圳
        url = 'http://index.baidu.com/Interface/Newwordgraph/getLive?'

        for w in words:
            url += 'wordlist%5B%5D=' + str(w) + '&'

        return url

    def get_cookie(self):

        print('PROCESSING REQUEST!')

        if (self.index == int(len(self.cookies)) - 1):
            self.index = 0
        else:
            self.index += 1

        print(self.index)
        print(self.cookies[self.index])
        return self.cookies[self.index]

    @classmethod
    def get_newest_stock_file(self):
        this_folder = os.path.dirname(__file__)
        parent_folder = os.path.dirname(this_folder)
        output_path = os.path.join(parent_folder, 'output')
        files = os.listdir(output_path)

        stock_files = list(filter(lambda x: 'stock' in x, files))

        newest_stock_file = reduce(lambda a, b: a if int((re.findall('(?<=__).*(?=.json)', a) or ['0'])[0]) >
                                                     int((re.findall('(?<=__).*(?=.json)', b) or ['0'])[0]) else b,
                                   stock_files)
        return newest_stock_file


if __name__ == '__main__':
    aa = BaiduIndexSpider.get_newest_stock_file()
    print(aa)
    # import doctest
    #
    # doctest.testmod()
