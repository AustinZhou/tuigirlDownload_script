# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuigirlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    category_name=scrapy.Field()
    
    detail_name=scrapy.Field()
    
    imagefilename=scrapy.Field()
    download_link=scrapy.Field()
