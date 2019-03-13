# -*- coding: utf-8 -*-
import scrapy
from allRencaiInfoScrapy.items import qianrenPlanItem
import codecs
import json

class PlanSpider(scrapy.Spider):
    name = '1000plan_search'
    # find_url = []
    # unfind_url = []

    def start_requests(self):
        allowed_domains = ['http://www.1000plan.org']
        start_urls = []
        base_url = 'http://www.1000plan.org/wiki/index.php?search-fulltext-title-'
        unfind_qianren = json.load(codecs.open('./unfind_url.json', 'r', encoding='utf-8'))
        for person in unfind_qianren:
            query_condition = person['unfind_name']  + '--all-0-within-time-desc-1'
            request = scrapy.Request(url=(base_url + str(query_condition)), callback=self.search)
            request.meta['url'] = base_url + str(query_condition)
            request.meta['name'] = person['unfind_name']
            request.meta['department_and_job'] = person['unfind_depart']
            person['feature'] = u'青年千人计划'
            request.meta['origin_info'] = person
            yield request

    def search(self, response):
        origin_url = response.meta["url"]
        search_result_list = response.css('.col-dl a ::attr(href)').extract()
        if search_result_list:
            base_url = 'http://www.1000plan.org/wiki/'
            find_url = base_url + search_result_list[0]
            item = qianrenPlanItem()
            item['find_url'] = find_url
            item['name'] = response.meta['name']
            item['origin_info'] = response.meta['origin_info']
            yield item





