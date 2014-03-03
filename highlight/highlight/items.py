# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class HighlightItem(Item):
    text = Field()
    title = Field()
    num = Field()
    book_link = Field()
    highlight_link = Field()
    author = Field()
