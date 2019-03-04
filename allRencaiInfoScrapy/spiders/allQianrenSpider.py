# -*- coding: utf-8 -*-
import scrapy
from allRencaiInfoScrapy.items import AllrencaiinfoscrapyItem
import codecs
import json

class RencaiSpider(scrapy.Spider):
    name = 'qianren_url'
    # find_url = []
    # unfind_url = []

    def start_requests(self):
        allowed_domains = ['https://baike.baidu.com']
        start_urls = []
        base_url = 'https://baike.baidu.com/search/none?word='
        all_people = json.load(codecs.open('allRencaiInfoScrapy/data/all_qianren.json', 'r', encoding='utf-8'))
        for person in all_people:
            # query_condition = 'intitle:('+person['name']+'),'+person['department'][:2]
            query_condition = person['name']+person['department'][:4]
            request = scrapy.Request(url=(base_url + str(query_condition)), callback=self.parse)
            request.meta['url'] = base_url + str(query_condition)
            request.meta['name'] = person['name']
            request.meta['department_and_job'] = person['department']
            person['feature'] = u'千人计划'
            request.meta['origin_info'] = person
            yield request

    def parse(self, response):
        origin_url = response.meta["url"]
        url = response.css('.search-list a::attr(href)').extract_first()
        if url:
            name_list = response.css('.search-list dd:nth-child(2) a ::text').extract()
            name = ''
            for name_part in name_list:
                name += name_part
            name = name.replace('_百度百科','')
            if "(" in name:
                start_pos = name.find('(')
                name = name[:start_pos]
            real_name = response.meta["name"]
            if "(" in real_name:
                real_name = real_name[:real_name.find('(')]
            if name == real_name:
                # self.find_url.append(origin_url)
                if 'http' not in url:
                    url = 'https://baike.baidu.com' + url
                item = AllrencaiinfoscrapyItem()
                item['find_flag'] = True
                item['origin_url'] = origin_url
                item['find_name'] = response.meta["name"]
                item['find_depart'] = response.meta["department_and_job"]
                item['status'] = response.status
                item['url'] = url
                item['origin_info'] = response.meta['origin_info']
                # json.dump(self.find_url, codecs.open('find_url.json', 'w', encoding='utf-8'), ensure_ascii=False)
                yield item
            else:
                item = AllrencaiinfoscrapyItem()
                item['find_flag'] = False
                item['origin_url'] = origin_url
                item['unfind_name'] = response.meta["name"]
                item['unfind_depart'] = response.meta["department_and_job"]
                item['status'] = response.status
                item['baidu_find_other_name'] = name
                item['origin_info'] = response.meta['origin_info']
                yield item
        else:
            # self.unfind_url.append(origin_url)
            # json.dump(self.unfind_url, codecs.open('unfind_url.json', 'w', encoding='utf-8'), ensure_ascii=False)
            item = AllrencaiinfoscrapyItem()
            item['find_flag'] = False
            item['origin_url'] = origin_url
            item['unfind_name'] = response.meta["name"]
            item['unfind_depart'] = response.meta["department_and_job"]
            item['status'] = response.status
            item['origin_info'] = response.meta['origin_info']
            yield item