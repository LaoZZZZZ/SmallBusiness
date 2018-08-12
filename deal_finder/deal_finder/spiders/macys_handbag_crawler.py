import scrapy

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from data_model.handbag import HandBag


class MacysHandBagCrawler(scrapy.Spider):
    name = "macys_handbag_crawler"

    def __init__(self):
        self.url_prefix = "https://www.macys.com/"

    def start_requests(self):
        urls = [
            'https://www.macys.com/shop/handbags-accessories/handbags?id=27686&edge=hybrid',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css("li.productThumbnailItem"):
            bag = HandBag(self.url_prefix)
            bag.parseFromWebContent(item)
            yield bag.__dict__
        next_page = response.css("li.next-page div.icon-ui-chevron-right-gr-huge a::attr(href)").extract()
        if next_page:
            for page in next_page:
                page_url = response.urljoin(self.url_prefix + '/' + page)
                yield scrapy.Request(page_url, callback=self.parse)        
        