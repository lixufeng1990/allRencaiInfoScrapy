#coding=utf-8
#python3
import jieba.posseg as pseg
import json
import codecs
import time
import requests
from bs4 import BeautifulSoup
def spbaike(name = 'scholar',other_url = 0):
    headers = {
        'Host': 'baike.baidu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    }
    time.sleep(0.1)
    info = {}
    url = 'https://baike.baidu.com/item/'
    if name != 'scholar':
        url = url+name
    else:
        url = url +other_url
    wb_data = requests.get(url,headers=headers).content
    soup = BeautifulSoup(wb_data,'lxml')
    description = soup.select('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.lemma-summary > div ')
    if len(description) != 0:
            description_ = ''
            for des in description:
                description_ += des.get_text()
            info['description'] = description_.replace('\n','').replace('\xa0','')
    else:
        description = soup.select('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.para')
        if len(description) != 0:
            description_ = ''
            for des in description:
                description_ += des.get_text()
            info['description'] = description_.replace('\n', '').replace('\xa0', '')
    taglist_ = soup.select('.taglist')
    if len(taglist_) > 0:  # taglist
        taglist = ''
        for tag in taglist_:
            taglist += tag.get_text().replace('\n','')+','
        taglist = taglist[:-1]
        info['taglist'] = taglist
    datalist1 = soup.select('div.basic-info.cmn-clearfix > dl > dt')  # infoboxAttributes
    datalist2 = soup.select('div.basic-info.cmn-clearfix > dl > dd')  # infoboxAttributesValue
    if len(datalist1) != 0 and len(datalist2) != 0:
        for i in range(len(datalist1)):
            info[datalist1[i].get_text().replace('\xa0','')] = datalist2[i].get_text().strip()
    datalist3 = soup.select('.title-text')  # 详细信息
    if len(datalist3) != 0:
        detail_header = []
        detail_content = ''
        for data in datalist3:
            detail_header.append(data.get_text())
        detail_header.append('词条标签')
        datalist4 = soup.select('body > div.body-wrapper > div.content-wrapper > div > div.main-content > div ')
        for data in datalist4:
            detail_content += data.get_text()
        detail_content = detail_content.replace('\n','').replace('\xa0','').replace('编辑','')
        length = len(detail_header)
        for i in range(0,length-1):
            begin = detail_content.find(detail_header[i])
            end = detail_content.find(detail_header[i+1])
            info[detail_header[i].replace(name,'')] = detail_content[begin+len(detail_header[i]):end]
    if len(info) == 0:
        print('姓名为:'+name+' 节点不存在！')
        return False
    else:
        return info
def samename_process(name):
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


if __name__=='__main__':
    data_path = 'scholar_info.txt'
    name_list = []
    scholar_nodes = []
    nodeid = 0
    url = 'https://baike.baidu.com/item/'
    # with codecs.open(data_path,'r',encoding='utf-8') as foo:
    #     for line in foo.readlines():
    #         name = line.split('\t')[0]
    #         name_list.append(name)
    name_list = ['邹鸿生']
    for name in name_list:
        character_list = samename_process(name)
        if character_list is False:
            info = spbaike(name=name)
            if info is not False:
                info['name'] = name
                info['id'] = nodeid
                info['url'] = url + name
                nodeid += 1
                scholar_nodes.append(info)
        else:
            if type(character_list) is not list:
                info = character_list
                info['name'] = name
                info['id'] = nodeid
                info['url'] = url + name
                nodeid += 1
                scholar_nodes.append(info)
            else:
                for item in character_list:
                    print(nodeid,name,url+item['url'])
                    info = spbaike(other_url=item['url'])
                    if info is not False:
                        info['name'] = name
                        info['id'] = nodeid
                        info['url'] = url+item['url']
                        nodeid += 1
                        scholar_nodes.append(info)
    json_data = json.dumps({"nodes":scholar_nodes},ensure_ascii=False)
    with codecs.open('scholar_detail.json','w',encoding='utf-8') as foo:
        foo.write(json_data)
'''
body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.lemma-summary > div:nth-child(1)
body > div.body-wrapper > div.content-wrapper > div > div.main-content > div.para
body > div.body-wrapper > div.before-content > div > ul > li:nth-child(2) > a
'''


