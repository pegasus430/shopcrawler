# -*- coding: utf-8 -*-

import json
import scrapy
import urlparse

from scrapy.http import Request

from shopcrawler.items import ShopcrawlerItem


class Walmart(scrapy.Spider):
    name = 'walmart_crawler'
    allowed_domains = ['www.walmart.com']

    HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

    SEARCH_URL = "https://www.walmart.com/search/api/preso?prg=desktop&query=" \
                 "{search_term}&page={page_num}&cat_id=0"

    def __init__(self, *args, **kwargs):
        super(Walmart, self).__init__(*args, **kwargs)
        search_term = kwargs.get('search_term', None)
        if not search_term:
            # Set default search_term=laptop
            self.search_term = 'laptop'

    def start_requests(self):
        if self.search_term:
            request = Request(
                self.SEARCH_URL.format(search_term=self.search_term, page_num=1),
                callback=self.parse_product,
                headers=self.HEADER
            )
            yield request
        else:
            yield scrapy.Request(url=self.START_URL, callback=self.parse_product, headers=self.HEADER)

    def parse_product(self, response):
        product_lists = []
        products_info = json.loads(response.body)

        products = products_info.get('items', None)
        if products:
            for product in products:
                item = ShopcrawlerItem()

                url = self._parse_url(product)
                item['url'] = url

                current_price = self._parse_price(product)
                item['current_price'] = current_price

                origin_price = self._parse_origin_price(product)
                item['origin_price'] = origin_price

                title = self._parse_title(product)
                item['title'] = title

                in_stock = self._parse_stock_status(product)
                item['in_stock'] = in_stock

                product_id = self._parse_product_id(product)
                item['product_id'] = product_id

                productType = self._parse_product_type(product)
                item['productType'] = productType

                image_url = self._parse_image_url(product)
                item['image_url'] = image_url

                upc = self._parse_upc(product)
                item['image_url'] = upc

                department = self._parse_department(product)
                item['department'] = department

                review_num = self._parse_numReviews(product)
                item['review_num'] = review_num

                average_review_rate = self._parse_average_rate(product)
                item['average_review_rate'] = average_review_rate

                currency = self._parse_currency(product)
                item['currency'] = currency

                brand = self._parse_brand(product)
                item['brand'] = brand

                product_lists.append(item)

        return product_lists

    @staticmethod
    def _parse_url(product):
        url = product.get('productPageUrl')
        return urlparse.urljoin('https://www.walmart.com', url) if url else None

    @staticmethod
    def _parse_price(product):
        offerPrice = product.get('primaryOffer', {}).get('offerPrice')
        return offerPrice if offerPrice else None

    @staticmethod
    def _parse_origin_price(product):
        title = product.get('primaryOffer', {}).get('listPrice')
        return title if title else None

    @staticmethod
    def _parse_title(product):
        title = product.get('title')
        return title if title else None

    @staticmethod
    def _parse_stock_status(product):
        stock_status = product.get('inventory', {}).get('availableOnline')
        price_available = product.get('showPriceAsAvailable')
        return bool(stock_status and price_available)

    @staticmethod
    def _parse_product_id(product):
        title = product.get('productId')
        return title if title else None

    @staticmethod
    def _parse_product_type(product):
        product_type = product.get('productType')
        return product_type if product_type else None

    @staticmethod
    def _parse_image_url(product):
        link = product.get('imageUrl')
        return link if link else None

    @staticmethod
    def _parse_upc(product):
        upc = product.get('upc')
        return upc if upc else None

    @staticmethod
    def _parse_department(product):
        department = product.get('department')
        return department if department else None

    @staticmethod
    def _parse_numReviews(product):
        numReviews = product.get('numReviews')
        return numReviews if numReviews else None

    @staticmethod
    def _parse_average_rate(product):
        avg_rate = product.get('customerRating')
        return avg_rate if avg_rate else None

    @staticmethod
    def _parse_currency(product):
        currency = product.get('primaryOffer', {}).get('currencyCode')
        return currency if currency else None

    @staticmethod
    def _parse_brand(product):
        brand = product.get('brand')
        return brand[0] if brand else None
