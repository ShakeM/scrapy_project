# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import IndexItem

import os
import json


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
            "BDUSS": "mYzSkF-d0tJVzJkbkFEZ1ZITHhmSVJnYnBXRnk4MWQwYU1QflBmNmt3eVdTfnRaSVFBQUFBJCQAAAAAAAAAAAEAAAB~Ni7G0dTApcjxaGVhdmVuAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJa-01mWvtNZR;"},
        {
            "BDUSS": "ndMNTNmVmZDRWY4V2VvaWNFUzgwT1JMLTl2NGd5V2RLNUR5ZkJUZWtGdDdTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAAAncC7GvOHOysT9y6vX0wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHu-01l7vtNZU;"},
        {
            "BDUSS": "k9HRlF4WWNoREkxdXBsUkpIc3g0NnVCQzI4TkdaNlo4MnRVLUcwZHNHbDZTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAABURi7GxeHStryqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHq-01l6vtNZf;"},
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

    # cookies = {
    #     'BDUSS': '5veUhpWlkxU3NtYVJodGtya1pYd1pzWDB0fmsyUU8tZ3U3bUpkcXAzUE5WU3BiQVFBQUFBJCQAAAAAAAAAAAEAAADQkClfS2ltd2hvZXZlcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM3IAlvNyAJbMn'}

    def start_requests(self):
        # Read output
        this_folder = os.path.dirname(__file__)
        parent_folder = os.path.dirname(this_folder)
        output_path = os.path.join(parent_folder, 'output')

        file_name = 'stock_2018-05-23_13-01-05_1527051665.json'
        file_path = os.path.join(output_path, file_name)
        print(os.path.exists(file_name))

        fp = open(file_path, 'r', encoding='utf-8')
        lines = fp.readlines()

        words = []
        for l in lines:
            obj = json.loads(l)
            words.append(obj['code'])

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
            url = self.join_url(f)
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
            index['_pc'] = self.decipher(index['_pc'], password)
            index['_all'] = self.decipher(index['_all'], password)
            index['_wise'] = self.decipher(index['_wise'], password)
            item = IndexItem(word=obj['key'],
                             period=obj['index'][0]['period'],
                             pc=index['_pc'],
                             all=index['_all'],
                             wise=index['_wise'],
                             )
            # print(item)
            yield item

    def decipher(self, ciphertext, password):
        """
        >>> BaiduIndexSpider().decipher('8N8NIN0NsN0N0NoNoNINyNoNoNhN-NIN-NINONhNhN8N-Ns','k8.y-Oh0N2IZsog.5-07861,+4%329')
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

    def join_url(self, words):
        # 全国 北京 上海 广州 深圳
        url = 'http://index.baidu.com/Interface/Newwordgraph/getLive?'

        for w in words:
            url += 'wordlist%5B%5D=' + str(w) + '&'

        return url

    def get_cookie(self):

        print('PROCESSING REQUEST!')

        if (self.index == int(len(self.cookies))-1):
            self.index = 0
        else:
            self.index += 1

        print(self.index)
        print(self.cookies[self.index])
        return self.cookies[self.index]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
