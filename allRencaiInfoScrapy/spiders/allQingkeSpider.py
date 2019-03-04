# -*- coding: utf-8 -*-
import scrapy
from allRencaiInfoScrapy.items import AllrencaiinfoscrapyItem
import codecs
import json

class RencaiSpider(scrapy.Spider):
    name = 'allQingke_url'
    # find_url = []
    # unfind_url = []

    def start_requests(self):
        allowed_domains = ['https://baike.baidu.com']
        start_urls = []
        base_url = 'https://baike.baidu.com/search/none?word='
        qingke_people = json.load(codecs.open('allRencaiInfoScrapy/data/all_qingke.json', 'r', encoding='utf-8'))
        for person in qingke_people:
            if person['work_department'] in ['(已出国)','已出国']:
                # query_condition = "%2B" + person['name'] + "-" + person['speciality'] + "-" + person['birthDay']
                query_condition = 'intitle:'+person['name'] +' +'+ person['birthDay'][:4] + person['speciality']
            else:
                # query_condition = "%2B" + person['name'] + "-" + person['work_department'][:5]
                query_condition = 'intitle:'+person['name']+ ' +' + person['work_department'][:3]
            request = scrapy.Request(url=(base_url + str(query_condition)), callback=self.parse)
            request.meta['url'] = base_url + str(query_condition)
            request.meta['name'] = person['name']
            request.meta['birthDay'] = person['birthDay']
            request.meta['department_and_job'] = person['work_department']
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
            item['find_birthDay'] = response.meta["birthDay"]
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
            item['unfind_birthDay'] = response.meta["birthDay"]
            item['unfind_depart'] = response.meta["department_and_job"]
            yield item






