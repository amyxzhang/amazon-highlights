# Scrapy settings for highlight project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'highlight'

SPIDER_MODULES = ['highlight.spiders']
NEWSPIDER_MODULE = 'highlight.spiders'

ITEM_PIPELINES = {
    'highlight.pipelines.HighlightMySQLPipeline': 100,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'highlight (+http://www.yourdomain.com)'
