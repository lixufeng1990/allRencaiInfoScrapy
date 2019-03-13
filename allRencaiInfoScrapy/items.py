# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllrencaiinfoscrapyItem(scrapy.Item):
    origin_info = scrapy.Field()
    origin_url = scrapy.Field()
    url = scrapy.Field()
    find_name = scrapy.Field()
    find_depart = scrapy.Field()
    find_birthDay = scrapy.Field()
    unfind_name = scrapy.Field()
    unfind_depart = scrapy.Field()
    unfind_birthDay = scrapy.Field()
    find_flag = scrapy.Field()
    status = scrapy.Field()
    baidu_find_other_name = scrapy.Field()
    pass

class rencaiBasicItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    origin_info = scrapy.Field()
    description = scrapy.Field()
    taglist = scrapy.Field()
    infobox = scrapy.Field()
    content = scrapy.Field()
    pass

class qianrenPlanItem(scrapy.Item):
    name = scrapy.Field()
    find_url = scrapy.Field()
    origin_info = scrapy.Field()
    pass
