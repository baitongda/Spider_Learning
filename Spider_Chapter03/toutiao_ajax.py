# -*- coding:utf-8 -*-

from pyquery import PyQuery as pq
from pymongo import MongoClient as mc
from time import sleep
from urllib.parse import urlencode,quote
import requests
from selenium import webdriver
import re
from hashlib import md5
import os
import pprint

detail_urls = []
img_urls = []
folders = []

def get_photo_items(url,parms,headers):
    ## 提取所有列表
    offset = 20
    while True:
        link = url.format(urlencode(parms))
        print(link)
        sleep(5)
        res = requests.get(link,headers=headers).json()
        has_more = res['has_more']
        datas = res['data']
        extract_article_link(datas)
        if has_more == 1:
            try:
                offset_ = int(parms['offset'])
                parms['offset'] = str(offset_ + offset)
            except Exception as e:
                print('Error {}'.format(e.args))
        if has_more == 0:
            break



def extract_article_link(items):
    
    ## 提取列表里面的详情页面和标题

    for item in items:
        pprint.pprint(item)
        article_url = item['article_url']
        title = item['title']
        if title not in folders:
            folders.append(title)
        if article_url not in detail_urls:
            detail_urls.append((article_url,title))
    print('detail_urls {} '.format(len(detail_urls)))
    print('folders {}'.format(len(folders)))





def extract_img_link(html=None):
    ## 提取所有的img链接
    
    doc = pq(html)
    items = doc('.image-item-inner').items()
    print(items)
    for it in items:
        img_link = it.children().eq(0).attr('data-src')
        if img_link not in img_urls:
            print(img_link)
            img_urls.append(img_link)
   

    

def download_photo(driver,url,title):
    
    ## 使用selenium去获取详情页的源代码，获取所有img，写到列表中
    driver.get(url)
    sleep(4)
    extract_img_link(driver.page_source)
    for i in  range(0,len(img_urls) - 1):
        _ = i
        ulr_ = img_urls.pop()
        download(ulr_,title)
    pass

def download(url,fold):
    dir_ = '/home/linxs/Pictures/{}'.format(fold)
    if not os.path.exists(dir_):
        os.mkdir(dir_)
    print('Start Save')
    response = requests.get(url)
    filename = md5(response.content).hexdigest() 
    path = '/home/linxs/Pictures/{0}/{1}.jpg'.format(fold,filename)
    if not os.path.exists(path):
        with open(path,'wb') as img:
            img.write(response.content)
    print('Save Successfully')

    
    

def get_dirver():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=option)
    return driver



def main():
    header = {
        'cookie': 'tt_webid=6550567558617302535; tt_webid=6550567558617302535; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=1631b6302a35e4-0a727eda68ac21-3b72025b-100200-1631b6302a417c; tt_webid=6550567558617302535; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; CNZZDATA1259612802=1788441275-1525170622-https%253A%252F%252Fwww.google.com%252F%7C1525176040; __tasessionId=m2m04xsah1525180736319',
        'dnt': '1',
        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }

    url = 'https://www.toutiao.com/search_content/?{}'
    parms = {
        'offset': '0',
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery',

    }
    get_photo_items(url,parms,header)
    driver = get_dirver()
    length = len(detail_urls)
    if length > 0:
        for i in range(length - 1):
            url_,title = detail_urls[i]
            download_photo(driver,url_,title)

if __name__ == '__main__':
    #extract_img_link()
    main()
    '''
    url = 'https://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=3&from=gallery'
    res = requests.get(url).json()
    pprint.pprint(res)
    datas = res.get('data')
    print(len(datas))
    pattern = re.compile(r'(http|https).*?//toutiao.com/group/(.*?)')
    for data in datas:
        if pattern.match(data.get('article_url')):
            print(data.get('article_url'))

    '''