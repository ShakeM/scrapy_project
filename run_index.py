from scrapy_project.util import verify
import yagmail
from scrapy_project.spiders.baidu_index import BaiduIndexSpider
from scrapy_project.spiders import baidu_index
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    b = baidu_index.BaiduIndexSpider()
    cookies = b.cookies

    if verify.bdusses(cookies):
        process = CrawlerProcess(get_project_settings())
        process.crawl(BaiduIndexSpider)
        process.start()
    else:
        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        yag.send('18616020643@163.com', 'Cookie Fail')

    if not verify.bdusses(cookies):
        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        yag.send('18616020643@163.com', 'Cookie Fail')
