import scrapy

class StockItem(scrapy.Item):
    symbol = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    extra = scrapy.Field()

