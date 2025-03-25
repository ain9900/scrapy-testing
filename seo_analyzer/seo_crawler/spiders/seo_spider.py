import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import re
from collections import defaultdict

class SEOCrawlerSpider(scrapy.Spider):
    name = 'seo_spider'

    def __init__(self, url=None, *args, **kwargs):
        super(SEOCrawlerSpider, self).__init__(*args, **kwargs)
        self.base_url = url
        self.start_urls = []
        self.visited_urls = set()
        self.discovered_links = set()
        self.domain = urlparse(url).netloc
        self.image_usage = defaultdict(set)  # Tracks which pages use each image URL

    def start_requests(self):
        robots_url = urljoin(self.base_url, '/robots.txt')
        yield scrapy.Request(robots_url, callback=self.parse_robots, errback=self.fallback_to_homepage)

    def parse_robots(self, response):
        sitemap_urls = re.findall(r'Sitemap:\s*(.+)', response.text, re.IGNORECASE)
        if sitemap_urls:
            for sitemap_url in sitemap_urls:
                if sitemap_url.endswith('.xml'):
                    yield scrapy.Request(sitemap_url, callback=self.parse_sitemap)
                elif sitemap_url.endswith('.txt'):
                    yield scrapy.Request(sitemap_url, callback=self.parse_txt_sitemap)
        else:
            yield from self.fallback_to_homepage(None)

    def parse_sitemap(self, response):
        if "<sitemapindex" in response.text:
            sitemap_urls = re.findall(r'<loc>(.*?)</loc>', response.text)
            for sitemap_url in sitemap_urls:
                if sitemap_url.endswith('.xml'):
                    yield scrapy.Request(sitemap_url, callback=self.parse_sitemap)
                elif sitemap_url.endswith('.txt'):
                    yield scrapy.Request(sitemap_url, callback=self.parse_txt_sitemap)
        else:
            urls = re.findall(r'<loc>(.*?)</loc>', response.text)
            for url in urls:
                yield scrapy.Request(url, callback=self.parse)

    def parse_txt_sitemap(self, response):
        lines = response.text.strip().splitlines()
        valid_urls = [line.strip() for line in lines if line.startswith('http')]
        for url in valid_urls:
            yield scrapy.Request(url, callback=self.parse)

    def fallback_to_homepage(self, failure):
        yield scrapy.Request(self.base_url, callback=self.parse)

    def parse(self, response):
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Numbered HTML tags extraction
        all_tags = {}
        tag_count = defaultdict(int)
        for tag in soup.find_all():
            tag_name = tag.name
            tag_count[tag_name] += 1
            numbered_tag = f"{tag_name}-{tag_count[tag_name]}"
            all_tags[numbered_tag] = str(tag)

        internal_links = []
        external_links = []
        broken_links = []
        image_issues = []

        for link in soup.find_all('a', href=True):
            full_url = urljoin(response.url, link['href'])
            if full_url.startswith('mailto:') or full_url.startswith('tel:'):
                continue
            if full_url in self.discovered_links:
                continue
            self.discovered_links.add(full_url)
            if urlparse(full_url).netloc == self.domain:
                internal_links.append({
                    "from_page": response.url,
                    "link_url": full_url
                })
            else:
                external_links.append({
                    "from_page": response.url,
                    "link_url": full_url
                })
            try:
                res = requests.head(full_url, timeout=5)
                if res.status_code >= 400:
                    broken_links.append({
                        "from_page": response.url,
                        "link_url": full_url,
                        "status": res.status_code
                    })
            except Exception:
                broken_links.append({
                    "from_page": response.url,
                    "link_url": full_url,
                    "status": "Error"
                })

        for img in soup.find_all('img', src=True):
            src = urljoin(response.url, img['src'])
            alt = img.get('alt', '').strip()
            self.image_usage[src].add(response.url)
            try:
                res = requests.head(src, timeout=5)
                status = res.status_code
            except Exception:
                status = "Error"
            image_issues.append({
                "from_page": response.url,
                "src": src,
                "alt": alt if alt else None,
                "status": status,
                "is_duplicate": len(self.image_usage[src]) > 1,
                "used_on_pages": sorted(list(self.image_usage[src]))
            })

        yield {
            'url': response.url,
            'all_tags': all_tags,
            'internal_links': internal_links,
            'external_links': external_links,
            'broken_links': broken_links,
            'image_issues': image_issues
        }

        for link in internal_links:
            link_url = link["link_url"]
            if link_url not in self.visited_urls:
                yield scrapy.Request(link_url, callback=self.parse)
