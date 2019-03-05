#coding=utf-8
#python3
import jieba.posseg as pseg
import json
import codecs
import time
import requests
from bs4 import BeautifulSoup
def spbaike(name, url):
    headers = {
        'Host': 'baike.baidu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    }
    time.sleep(0.1)
    info = {}
    info['name'] = name
    info['url'] = url
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
        detail_header.append('百度百科内容由网友')
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
        # print('姓名为:'+name+' 节点不存在！')
        return False
    else:
        return info


