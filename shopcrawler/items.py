# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field()
    title = scrapy.Field()
    origin_price = scrapy.Field()
    current_price = scrapy.Field()
    in_stock = scrapy.Field()
    product_id = scrapy.Field()
    productType = scrapy.Field()
    image_url = scrapy.Field()
    upc = scrapy.Field()
    department = scrapy.Field()
    average_review_rate = scrapy.Field()
    review_num = scrapy.Field()
    currency = scrapy.Field()
    brand = scrapy.Field()
    pass
