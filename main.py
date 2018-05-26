from scrapy import cmdline
from scrapy_project.util import verify
import yagmail
import os
import re
from functools import reduce
from scrapy_project.spiders import baidu_index

if __name__ == '__main__':
    b = baidu_index.BaiduIndexSpider()
    cookies = b.cookies

    if verify.bdusses(cookies):
        os.system('scrapy crawl stock_spider')
        os.system('scrapy crawl baidu_index')
        pass
    else:
        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        yag.send('18616020643@163.com', 'Cookie失败')

    if not verify.bdusses(cookies):
        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        yag.send('18616020643@163.com', 'Cookie失败')
