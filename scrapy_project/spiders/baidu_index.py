# -*- coding: utf-8 -*-
import scrapy
import json


class BaiduIndexSpider(scrapy.Spider):
    name = 'baidu_index'
    allowed_domains = ['baidu.com']
    start_urls = ['']
    cookies = {
        'BDUSS': '5veUhpWlkxU3NtYVJodGtya1pYd1pzWDB0fmsyUU8tZ3U3bUpkcXAzUE5WU3BiQVFBQUFBJCQAAAAAAAAAAAEAAADQkClfS2ltd2hvZXZlcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM3IAlvNyAJbMn'}

    def start_requests(self):
        request = scrapy.http.Request(url='http://index.baidu.com/Interface/Newwordgraph/getLive?wordlist[0]=北京',
                                      cookies=self.cookies,
                                      callback=self.get_password)
        yield request

    def get_password(self, response):
        response_json = json.loads(response.text)
        uniqid = response_json['uniqid']

        request = scrapy.http.Request(url='http://index.baidu.com/Interface/api/ptbk?uniqid=' + uniqid,
                                      cookies=self.cookies,
                                      meta={'json': response_json},
                                      callback=self.parse_json)
        yield request

    def parse_json(self, response):
        ciphertext = response.meta['json']['data'][0]['index'][0]['_pc']
        password = json.loads(response.text)['data']
        plaintext = self.decipher(ciphertext,password)
        print(plaintext)

    # 8N8NIN0NsN0N0NoNoNINyNoNoNhN-NIN-NINONhNhN8N-Ns
    # k8.y-Oh0N2IZsog.5-07861,+4%329
    def decipher(self, ciphertext, password):
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
