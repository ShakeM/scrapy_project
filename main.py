from scrapy_project.util import verify
import yagmail
from scrapy_project.spiders.baidu_index import BaiduIndexSpider
from scrapy_project.spiders.stocks import StockSpider
from scrapy_project.spiders import baidu_index
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

if __name__ == '__main__':
    b = baidu_index.BaiduIndexSpider()
    cookies = b.cookies

    if verify.bdusses(cookies):
        configure_logging()
        runner = CrawlerRunner()

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(StockSpider)
            yield runner.crawl(BaiduIndexSpider)
            reactor.stop()


        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished
    else:
        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        yag.send('18616020643@163.com', 'Cookie Fail')

    if not verify.bdusses(cookies):
        yag = yagmail.SMTP('54jsy@163.com', '56304931a', 'smtp.163.com')
        yag.send('18616020643@163.com', 'Cookie Fail')
