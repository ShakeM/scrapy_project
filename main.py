from scrapy import cmdline

# cmdline.execute("scrapy crawl sh_spider".split())
# cmdline.execute("scrapy crawl sz_spider".split())


import os
#
os.system('scrapy crawl stock_spider')
os.system('scrapy crawl baidu_index')
