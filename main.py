from scrapy import cmdline

# cmdline.execute("scrapy crawl sh_spider".split())
# cmdline.execute("scrapy crawl sz_spider".split())


import os

os.system('scrapy crawl sh_spider')
os.system('scrapy crawl sz_spider')
# os.system('scrapy crawl baidu_index')
