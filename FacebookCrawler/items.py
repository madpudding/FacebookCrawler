# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FacebookcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FacebookPosts(scrapy.Item):  # facebook post表单提交数据
    task = scrapy.Field()
    keyword = scrapy.Field()
    type = scrapy.Field()
    timestamp = scrapy.Field()
    post_data = scrapy.Field()
