__author__ = 'chenfeiyu'
from scrapy.item import Item, Field


class ErrorItem(Item):
    Type = Field()
    Message = Field()
    StatusCode = Field()


class TestItem(Item):
    SpiderName = Field()
    Error = Field()



