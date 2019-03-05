import codecs
import json
import filter_sameName
import getContent_by_url

# data_file_path = "./qingkeUrl.json"
# data_file_path = "../../qianrenUrl.json"
data_file_path = "./allQingkeUrl.json"
# data_file_path = "./allFemaleUrl.json"
find_url_path = "../../find_url.json"
unfind_url_path = "../../unfind_url.json"
all_rencai_info_path = "../../all_rencai_info.json"

if __name__ == "__main__":
    all_data = json.load(codecs.open(data_file_path,'r',encoding='utf-8'))
    find_urls = []
    unfind_urls = []
    for data in all_data:
        if data['find_flag']:
            find_urls.append(data)
        else:
            unfind_urls.append(data)
    filter = filter_sameName.filter()
    filter_result = filter.filter_list(unfind_urls)
    find_urls += filter_result[0]
    unfind_urls = filter_result[1]

    print("unfind urls num:",str(len(unfind_urls)))
    print("unfind urls rate:",str(len(unfind_urls)/(len(unfind_urls)+len(find_urls))))
    json.dump(find_urls, codecs.open(find_url_path,'w',encoding='utf-8'),ensure_ascii=False)
    json.dump(unfind_urls, codecs.open(unfind_url_path,'w',encoding='utf-8'),ensure_ascii=False)

    all_rencai_info = []
    for url in find_urls:
        get_info = getContent_by_url.spbaike(url['find_name'], url['url'])
        if get_info:
            get_info['basic_info'] = url['origin_info']
            all_rencai_info.append(get_info)

    json.dump(all_rencai_info, codecs.open(all_rencai_info_path, 'w', encoding='utf-8'), ensure_ascii=False)
