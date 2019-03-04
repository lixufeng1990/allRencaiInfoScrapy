# -*- coding: utf-8 -*-
import scrapy
from allRencaiInfoScrapy.items import AllrencaiinfoscrapyItem
import codecs
import json

class RencaiSpider(scrapy.Spider):
    name = 'rencai_url'
    # find_url = []
    # unfind_url = []

    def start_requests(self):
        allowed_domains = ['https://baike.baidu.com']
        start_urls = []
        base_url = 'https://baike.baidu.com/search/none?word='
        # qingke_people = json.load(codecs.open('allRencaiInfoScrapy/data/all_qianren.json', 'r', encoding='utf-8'))
        # qingke_people = json.load(codecs.open('allRencaiInfoScrapy/data/15th_qingke_candidate.json', 'r', encoding='utf-8'))
        qingke_people = json.load(codecs.open('allRencaiInfoScrapy/data/all_qingke.json', 'r', encoding='utf-8'))
        for person in qingke_people:
            query_condition = "%2B" + person['name'] + "-" + person['department_and_job'][:4]
            request = scrapy.Request(url=(base_url + str(query_condition)), callback=self.parse)
            request.meta['url'] = base_url + str(query_condition)
            request.meta['name'] = person['name']
            request.meta['department_and_job'] = person['department_and_job']
            yield request

    def parse(self, response):
        origin_url = response.meta["url"]
        url = response.css('.search-list a::attr(href)').extract_first()
        if url:
            # self.find_url.append(origin_url)
            if 'http' not in url:
                url = 'https://baike.baidu.com' + url
            item = AllrencaiinfoscrapyItem()
            item['url'] = url
            item['origin_url'] = origin_url
            item['find_flag'] = True
            item['find_name'] = response.meta["name"]
            item['find_depart'] = response.meta["department_and_job"]
            # json.dump(self.find_url, codecs.open('find_url.json', 'w', encoding='utf-8'), ensure_ascii=False)
            yield item
        else:
            # self.unfind_url.append(origin_url)
            # json.dump(self.unfind_url, codecs.open('unfind_url.json', 'w', encoding='utf-8'), ensure_ascii=False)
            item = AllrencaiinfoscrapyItem()
            item['origin_url'] = origin_url
            item['find_flag'] = False
            item['unfind_name'] = response.meta["name"]
            item['unfind_depart'] = response.meta["department_and_job"]
            yield item






