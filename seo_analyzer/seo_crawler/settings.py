# seo_crawler/settings.py

BOT_NAME = 'seo_crawler'

SPIDER_MODULES = ['seo_crawler.spiders']
NEWSPIDER_MODULE = 'seo_crawler.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1
COOKIES_ENABLED = False
USER_AGENT = 'seo_crawler (+http://www.example.com)'
