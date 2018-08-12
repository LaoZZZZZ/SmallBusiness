import json
import re

class HandBag(object):
    def __init__(self):
        self.brand = ''
        self.item_id = ''
        self.category_id = ''
        self.current_price = -1.0
        self.regular_price = -1.0
        self.url = ''
        self.name = ''
        self.description = ''
        self.review_stats = {}
        self.is_last_act = False
        self.special_offers = []
        self.price_pattern = "\$\d+\.*\d*"
    # content: A Selector.
    def parseFromWebContent(self, content):
        product_detail = content.css("div.productDetail")
        # get link
        identity = content.css("div.productThumbnail")
        self.item_id = content.css("div.productThumbnail::attr(id)").extract_first()
        if identity:
            self.url = identity.css("div.productThumbnailImage").css("a::attr(href)").extract_first()

        if product_detail:
            #self.url = product_detail.css("a.tag::href")
            actual_detail = json.loads(product_detail.css("script::text").extract_first())
            if 'detail' in actual_detail:
                detail = actual_detail['detail']
                self.brand = detail['brand']
                self.name = detail['name']
                self.description = detail['description']
                self.review_stats = detail['reviewStatistics']
        price_info = content.css("div.priceInfo")
        if price_info:
            special_offers = price_info.css("div.specialOffers.span.priceTypeText::text")
            for special_offer in special_offers.extract():
                self.special_offers.append(special_offer)
                try:
                    if re.match("LAST ACT", self.special_offer[-1]):
                        self.is_last_act = True
                except Exception as exp:
                    print(self.special_offer)
                    print(exp)
            # get regular price and current price.
            regular_price = price_info.css('span.regular::text')
            if regular_price:
                self.regular_price = re.search(self.price_pattern, regular_price.extract_first()).group(0)

            # Get current price if it is different from regular price.
            discount_prices = price_info.css('span.discount::text').extract()
            if discount_prices:
                for p in discount_prices:
                    if not p.strip():
                        continue
                    if '-' not in p:
                        self.current_price = re.search(self.price_pattern, p).group(0)
                    else:
                        self.discount = re.search('\d*\.*\d*', p).group(0)
            else:
                self.current_price = regular_price
                self.discount = 0