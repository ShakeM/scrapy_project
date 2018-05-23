# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import IndexItem


class BaiduIndexSpider(scrapy.Spider):
    name = 'baidu_index'
    allowed_domains = ['baidu.com']
    start_urls = ['']

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_project.middlewares.BaiduDownloaderMiddleware': 543,
        },
        "ITEM_PIPELINES": {
            'scrapy_project.pipelines.IndexPipeline': 300,
        }
    }

    # cookies = {
    #     'BDUSS': '5veUhpWlkxU3NtYVJodGtya1pYd1pzWDB0fmsyUU8tZ3U3bUpkcXAzUE5WU3BiQVFBQUFBJCQAAAAAAAAAAAEAAADQkClfS2ltd2hvZXZlcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM3IAlvNyAJbMn'}

    def start_requests(self):
        # Create 0-9 a-z
        demo_words = list(range(10))
        for i in range(26):
            demo_words.append(chr(i + ord('a')))

        five_words = []
        for i in range(len(demo_words)):
            five = demo_words[i * 5:i * 5 + 5]
            if not five: break

            five_words.append(five)

        for f in five_words:
            url = self.join_url(f)
            request = scrapy.http.Request(url=url, callback=self.get_password)
            yield request

    def get_password(self, response):
        print(response.text)
        data_json = json.loads(response.text)
        uniqid = data_json['uniqid']

        request = scrapy.http.Request(url='http://index.baidu.com/Interface/api/ptbk?uniqid=' + uniqid,
                                      meta={'data': data_json['data']},
                                      callback=self.parse_json)
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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
