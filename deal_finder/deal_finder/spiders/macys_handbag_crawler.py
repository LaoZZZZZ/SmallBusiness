import scrapy

class MacysHandBagCrawler(scrapy.Spider):
    name = "macys_handbag_crawler"

    def start_requests(self):
        urls = [
            'https://www.macys.com/shop/handbags-accessories?id=26846',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'deals-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
