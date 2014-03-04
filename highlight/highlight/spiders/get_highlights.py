from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from highlight.items import HighlightItem


class HighlightSpider(Spider):
    name = "highlight"
    allowed_domains = ["kindle.amazon.com"]
    start_urls = [
        "https://kindle.amazon.com/most_popular/",
    ]

    def parse(self, response):
        sel = Selector(response)
        highlights = sel.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " listRow ")]')
        for highlight in highlights:
            item = HighlightItem()
            item['text'] = highlight.xpath('div/div/div/div')[0].xpath('span/text()').extract()[0]
            item['num'] = int(highlight.xpath('div/div/div/div')[1].xpath('text()').re('[0-9]+')[0])
            item['title'] = highlight.xpath('div/div/div/div')[2].xpath('span/a/text()').extract()[0]
            item['highlight_link'] = highlight.xpath('div/div/div/div')[2].xpath('span/a/@href').extract()[0]
            item['author'] = highlight.xpath('div/div/div/div')[2].xpath('span')[1].xpath('text()').extract()[0][4:]
            item['book_link'] = highlight.xpath('div/div/div/div/div/a/@href')[0].extract()
            yield item
            
        next_link = sel.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " readingPagination ")]')
        
        next_link = next_link.xpath('div/a')[-1].xpath('@href').extract()[0]
        yield Request(next_link, callback=self.parse)
        
