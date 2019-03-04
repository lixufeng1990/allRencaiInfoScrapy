# -*- coding: utf-8 -*-
import scrapy
from allRencaiInfoScrapy.items import AllrencaiinfoscrapyItem
from allRencaiInfoScrapy.items import rencaiBasicItem
import codecs
import json

class RencaiSpider(scrapy.Spider):
    name = 'qianren_url_filter'
    # find_url = []
    # unfind_url = []

    def start_requests(self):
        allowed_domains = ['https://baike.baidu.com']
        start_urls = []
        base_url = 'https://baike.baidu.com/search/none?word='
        all_people = json.load(codecs.open('allRencaiInfoScrapy/data/all_qianren.json', 'r', encoding='utf-8'))
        for person in all_people[:5]:
            # query_condition = 'intitle:('+person['name']+'),'+person['department'][:2]
            query_condition = person['name']+person['department'][:4]
            request = scrapy.Request(url=(base_url + str(query_condition)), callback=self.parse)
            request.meta['url'] = base_url + str(query_condition)
            request.meta['name'] = person['name']
            request.meta['department_and_job'] = person['department']
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
                request = scrapy.Request(url= url, callback=self.spbaike)
                request.meta['origin_info'] = response.meta["origin_info"]
                yield request
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

    def spbaike(self, response):
        origin_info = response.meta['origin_info']
        basicItem = rencaiBasicItem()
        basicItem['name'] = origin_info['name']
        basicItem['url'] = response.url
        description = response.css('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.lemma-summary > div ::text').extract()
        if len(description) != 0:
                description_ = ''
                for des in description:
                    description_ += des
                basicItem['description'] = description_.replace('\n','').replace('\xa0','')
        else:
            description = response.css('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.para').extract()
            if len(description) != 0:
                description_ = ''
                for des in description:
                    description_ += des
                basicItem['description'] = description_.replace('\n', '').replace('\xa0', '')
        taglist_ = response.css('.taglist::text').extract()
        if len(taglist_) > 0:  # taglist
            taglist = ''
            for tag in taglist_:
                taglist += tag.replace('\n','')+','
            taglist = taglist[:-1]
            basicItem['taglist'] = taglist
        datalist1 = response.css('div.basic-info.cmn-clearfix > dl > dt::text').extract()  # infoboxAttributes
        datalist2 = response.css('div.basic-info.cmn-clearfix > dl > dd::text').extract()  # infoboxAttributesValue
        infobox_dict = {}
        if len(datalist1) != 0 and len(datalist2) != 0:
            for i in range(len(datalist1)):
                infobox_dict[datalist1[i].replace('\xa0','')] = datalist2[i].strip()
            basicItem['infobox'] = infobox_dict
        datalist3 = response.css('.title-text ::text').extract()  # 详细信息
        if len(datalist3) != 0:
            detail_header = []
            detail_content = ''
            pos = 0
            while(pos < len(datalist3)-1):
                detail_header.append(datalist3[pos]+datalist3[pos+1])
                pos += 2
            detail_header.append('百度百科内容由网友')
            datalist4 = response.css('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div ::text').extract()
            for data in datalist4:
                detail_content += data
            detail_content = detail_content.replace('\n','').replace('\xa0','').replace('编辑','')
            length = len(detail_header)
            content_dict = {}
            for i in range(0,length-1):
                begin = detail_content.find(detail_header[i])
                end = detail_content.find(detail_header[i+1])
                content_dict[detail_header[i].replace(origin_info['name'],'')] = detail_content[begin+len(detail_header[i]):end]
            basicItem['content'] = content_dict
        basicItem['origin_info'] = origin_info
        yield basicItem

    def samename_process(self, response):
        url = 'https://baike.baidu.com/item/{}?force=1'.format(name)
        url = url + name
        character_list = []
        wb_data = requests.get(url, headers=headers).content
        soup = BeautifulSoup(wb_data, 'lxml')
        character = soup.select('.para > a')
        if len(character) > 0:
            for char in character:
                node = {}
                if char.get('href') is not None:
                    node['name'] = char.get_text()
                    node['url'] = char.get('href').replace('/item/', '')
                    if (name in node['name']) and ('pic' not in node['url']):
                        character_list.append(node)
        if len(character_list) > 0:
            return character_list
        else:
            info = spbaike(name)
            if info is False:
                return False
            else:
                return info