# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class BaiduDownloaderMiddleware(object):
    cookies = [
        {
            "BDUSS": "1hMlV6ZVl4WnBqd0x5bmF-TWVac1RmRjU3NGFrb1BINVF3RkV0UUlNTi1TfnRaTVFBQUFBJCQAAAAAAAAAAAEAAAA8cC7Gua3B6cvJtcS5ysrCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH6-01l-vtNZZU;"},
        {
            "BDUSS": "0hUWU5oSlVub2RKNjBpSHNESGZoZk9rQVhJLS1SU1JkTFJnbGRVY29sYW1TfnRaSVFBQUFBJCQAAAAAAAAAAAEAAACARy7G1bKzve-~AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKa-01mmvtNZZ;"},
        {
            "BDUSS": "JjVjNhNktOblpLeThqblppT1Q2UTZFc35uY3NTbXpreDJ6Sk42M3NvR2hTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAADXNi7Gy6vX09H0vrC4owAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKG-01mhvtNZb3;"},
        {
            "BDUSS": "nRuZzMzR0pMOVp2N3JOa1dPVFk5Z35WS1hnNlhGQmtmQWFJRnFrMmlvUzdTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAAATSC7Gz8S67rro1dxzaGluZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALu-01m7vtNZM;"},
        {
            "BDUSS": "2llRWRyNGZjWHROVnFzUVZCUTN6TkdIZzZnWnpITn5hTzU3d0l2WklyV2ZTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAABURy7GaGVhdmVuwOfRxb3gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJ--01mfvtNZS;"},
        {
            "BDUSS": "mYzSkF-d0tJVzJkbkFEZ1ZITHhmSVJnYnBXRnk4MWQwYU1QflBmNmt3eVdTfnRaSVFBQUFBJCQAAAAAAAAAAAEAAAB~Ni7G0dTApcjxaGVhdmVuAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJa-01mWvtNZR;"},
        {
            "BDUSS": "V3WjVYYnVnNjlDTEd0YzRKWVRsS1lUQ3VMcG8xRE85ekMzMDduUVZ6UmRTfnRaSVFBQUFBJCQAAAAAAAAAAAEAAAChYi7GuavO9-j36tFmbHkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF2-01ldvtNZZX;"},
        {
            "BDUSS": "0JpVThpZFJUWVNpeU0tUUpxZDFhcm5RU3YzWlVOMDQwMFBYZ2hPQ2VTdC1TfnRaTVFBQUFBJCQAAAAAAAAAAAEAAABvRi7GtKbFrtf5venH2dTPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH6-01l-vtNZR;"},
        {
            "BDUSS": "k9HRlF4WWNoREkxdXBsUkpIc3g0NnVCQzI4TkdaNlo4MnRVLUcwZHNHbDZTfnRaTVFBQUFBJCQAAAAAAAAAAAEAAABURi7GxeHStryqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHq-01l6vtNZf;"},
    ]

    index = 0

    def process_request(self, request, spider):
        print('PROCESSING REQUEST!')

        if (self.index == int(len(self.cookies))):
            self.index = 0
        else:
            self.index += 1

        print(self.index)
        print(self.cookies[self.index])
        request.cookies = self.cookies[self.index]
        return

    # class ScrapyProjectSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


# class ScrapyProjectDownloaderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
