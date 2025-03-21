import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'  # Unique spider name.
    allowed_domains = ['example.com']
    start_urls = ['http://example.com']

    def parse(self, response):
        # Extract title as an example.
        title = response.css('title::text').get()
        yield {'title': title}

        # Follow links (if needed):
        for next_page in response.css('a::attr(href)').getall():
            if next_page is not None:
                yield response.follow(next_page, self.parse)
