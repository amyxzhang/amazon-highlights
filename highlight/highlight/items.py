from scrapy.item import Item, Field

class HighlightItem(Item):
    text = Field()
    title = Field()
    num = Field()
    book_link = Field()
    highlight_link = Field()
    author = Field()
