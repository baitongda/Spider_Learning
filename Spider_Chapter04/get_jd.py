# -*- coding:utf-8 -*-

import requests
from pyquery import PyQuery as pq
from urllib.request import quote
from urllib.parse import urlencode
from time import sleep
import codecs

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': '__jda=122270672.1525757325841884816464.1525757326.1525757326.1525757326.1; __jdc=122270672; __jdv=122270672|direct|-|none|-|1525757325841; __jdu=1525757325841884816464; PCSYCityID=country_2429; xtest=2067.cf6b6759; ipLoc-djd=53283-53456-0-0; rkv=V0500; 3AB9D23F7A4B3C9B=FIJKHONLVSJDVT3VIDCSBJLSZQKMSWL7EAJTGT3RROUIMGQKHF3U2FEWZT2QLWQEYFOKDPP3DZYFYWMO5BHEAEAWBA; qrsc=3; __jdb=122270672.7.1525757325841884816464|1.1525757326',
    'DNT': '1',
    'Host': 'search.jd.com',
    'Referer': 'http://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page=3&s=61&click=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

base_search = "http://search.jd.com/Search?{}"
base_ajax_items  = 'http://search.jd.com/s_new.php?{}'





def get_code(html):
    doc = pq(html)
    lis = doc('.gl-item').items()
    codes = []
    for li in lis:
        spu = li.attr('data-spu')
        if spu:
            codes.append(spu)
    return ','.join(codes)


def parse_pre_30(html):
    doc = pq(html)
    titles = doc('#J_goodsList > ul > li').items()
    for title in  titles:
        text = title('div > div.p-name.p-name-type-2 > a > em').text()
        print(text)
        print("--------------------")


def parse_next_30(html):
    doc = pq(html)
    lis = doc('.gl-item').items()
    for li in lis:
        text = li('div > div.p-name.p-name-type-2 > a > em').text()
        print(text)
        print('********************')




def get_pages_count(html):
    pages = 0
    doc = pq(html)
    texts = doc('#J_topPage > span > i').items()
    for text in texts:
        counts = text.text()
        if counts:
            pages = counts
            break
    return int(pages)


def scraping_jd(codes,page,jsons):
    search = base_search.format(urlencode(jsons))
    res = requests.get(search,headers=headers)
    res.encoding = 'utf-8'    
    parse_pre_30(res.text)
    codes = get_code(res.text)
    jsons['page'] = 2 * page
    jsons['tpl'] = "3_M"
    jsons['scrolling'] = 'y'
    jsons['show_items'] = codes
    ajax_items_link = base_ajax_items.format(urlencode(jsons))
    res = requests.get(ajax_items_link,headers=headers)
    res.encoding = 'utf-8'
    parse_next_30(res.text)
    print("Page {} Successfully".format(page))



def main():
    jsons = {
        'keyword':input("输入关键字:    "),
        'enc':'utf-8',
        'qrst':'1',
        'stop':'1',
        'vt':'2',
        'cid2':'653',
        'cid3':'655',
        'page':'1',
        's':'1',
        'click':'0'
    }

    search = base_search.format(urlencode(jsons))
    res = requests.get(search,headers=headers)
    res.encoding = 'utf-8' 
    codes = get_code(res.text)
    total = get_pages_count(res.text)
    for page in range(1,total + 1):
        scraping_jd(codes,page,jsons)
        sleep(5)
        if page == 5:
            break
    



    '''
    search = base_search.format(urlencode(jsons))
    res = requests.get(search,headers=headers)
    res.encoding = 'utf-8'    
    parse_pre_30(res.text)
    codes = get_code(res.text)
    
    jsons['page'] = 2 * page
    jsons['tpl'] = "3_M"
    jsons['scrolling'] = 'y'
    jsons['show_items'] = codes
    ajax_items_link = base_ajax_items.format(urlencode(jsons))
    res = requests.get(ajax_items_link,headers=headers)
    res.encoding = 'utf-8'
    parse_next_30(res.text)
    print("Page {} Successfully".format(page))
    '''

if __name__ == '__main__':
    main()