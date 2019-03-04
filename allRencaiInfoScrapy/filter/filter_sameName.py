#coding=utf-8
#python3
import jieba.posseg as pseg
import json
import codecs
import time
import requests
from bs4 import BeautifulSoup
import getContent_by_url

# data_file_path = "./qingkeUrl.json"
data_file_path = "../../qianrenUrl.json"
# data_file_path = "./allQingkeUrl.json"
# data_file_path = "./allFemaleUrl.json"
find_url_path = "../../find_url.json"
unfind_url_path = "../../unfind_url.json"

class filter():
    filter_bank = {}

    def samename_process(self, name):
        url = 'https://baike.baidu.com/item/{}?force=1'.format(name)
        url = url + name
        character_list = []
        headers = {
            'Host': 'baike.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        }
        wb_data = requests.get(url, headers=headers).content
        soup = BeautifulSoup(wb_data, 'lxml')
        character = soup.select('.para > a')
        if len(character) > 0:
            for char in character:
                node = {}
                if char.get('href') is not None:
                    node['name'] = char.get_text()
                    node['url'] = 'https://baike.baidu.com/item/'+char.get('href').replace('/item/', '')
                    if (name in node['name']) and ('pic' not in node['url']):
                        character_list.append(node)
        if len(character_list) > 0:
            return character_list
        else:
            info = getContent_by_url.spbaike(name, url)
            if info:
                return [{'name':name, 'url':url}]
            else:
                return False

    def get_page_text(self, url):
        headers = {
            'Host': 'baike.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        }
        time.sleep(0.1)
        wb_data = requests.get(url, headers=headers).content
        soup = BeautifulSoup(wb_data, 'lxml')
        page_text = soup.select('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div ')
        detail_content = ''
        for data in page_text:
            detail_content += data.get_text()
        detail_content = detail_content.replace('\n', '').replace('\xa0', '').replace('编辑', '')
        return detail_content

    def filter_name_by_info(self, name, infomatin):
        filter_result = {}
        if name in self.filter_bank.keys():
            page_list = self.filter_bank[name]
            best_score = 0
            best_url = ''
            for page in page_list:
                score = 0
                print("filter name: " + name + ", looking page: " + page[0])
                page_text = page[1]
                for key in infomatin:
                    if (key != 'name') and (infomatin[key] in page_text):
                        score += 1
                if score > best_score:
                    best_score = score
                    best_url = page[0]
            if not best_score:
                return best_url
            else:
                return False
        else:
            character_list = self.samename_process(name)
            if character_list:
                self.filter_bank[name] = []
                best_score = 0
                best_url = ''
                for item in character_list:
                    score = 0
                    print("looking page: "+item['url'])
                    page_text = self.get_page_text(item['url'])
                    self.filter_bank[name].append((item['url'], page_text))
                    for key in infomatin:
                        if (key != 'name') and (infomatin[key] in page_text):
                            score += 1
                    if score > best_score:
                        best_score = score
                        best_url = item['url']
                if best_score:
                    return best_url
                else:
                    return False
            else:
                return False

    def filter(self, all_unfind_data):
        find_urls = []
        count = 0
        for data in all_unfind_data:
            print("have process people num: " + str(count))
            filter_result = self.filter_name_by_info(data['unfind_name'], data['origin_info'])
            if filter_result:
                data['url'] = filter_result
                data['find_flag'] = True
                data['find_name'] = data['unfind_name']
                find_urls.append(data)
                all_unfind_data.remove(data)
            count += 1

        return (find_urls, all_unfind_data)