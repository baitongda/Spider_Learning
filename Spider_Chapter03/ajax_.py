# -*- coding:utf-8 -*-
from urllib.parse import urlencode
import requests
from time import sleep
from pymongo import MongoClient
from pyquery import PyQuery as pq

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Host': 'm.weibo.cn',
    'Connection': 'keep-alive'
}

detail_urls = []
details = []

def get(base_url,parms):
    url = base_url.format(urlencode(parms))
    print(url)
    response = requests.get(url,headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        return None



def save_to_mongo(client,data):
    db = client['admin']
    db.authenticate('lingoogle','7218246.')
    db = client['weibo']
    collention = db['tangzhaolin']
    if isinstance(data,dict):
        collention.insert_one(data)


def get_detail(client,items):
    print(len(items))
    for item in items:
        data = {}
        mblog = item['mblog']
        data['attitudes_count'] = mblog['attitudes_count']
        data['comments_count'] = mblog['comments_count']
        data['created_at'] = mblog['created_at']
        data['reposts_count'] = mblog['reposts_count']
        data['platform'] = mblog['source']
        data['text'] = pq(mblog['text']).text()
        details.append(data)
        save_to_mongo(client,data)
    print('-----------------------------------------') 


def extract_url(client,items):
    get_detail(client,items)
    for item in items:
        try:
            link = item['scheme']
            if link not in detail_urls:
                detail_urls.append(link)
        except Exception as e:
            _ = e
            print('Extract Error! {}'.format(e))


def main():
    client = MongoClient()
    parms = {
    'uid': '3502179457',
    'luicode': '10000012',
    'lfid': '1005052145105594_-_FOLLOWERS',
    'featurecode': '20000320',
    'type': 'uid',
    'value': '3502179457',
    'containerid': '1076033502179457'
    }

    base = 'https://m.weibo.cn/api/container/getIndex?{}'
    content = get(base,parms)
    total = content['data']['cardlistInfo'].get('total')

    pages = total//10
    if total%10 != 0:
        pages = pages + 1

    for page in range(1,pages + 1):
        sleep(5)
        print('Get {} page'.format(page))
        parms['page'] = page
        content = get(base,parms)
        if content is not None:
            extract_url(client,content['data']['cards'])
    print(len(detail_urls),len(details))


if __name__ == '__main__':
    #print(1062%10)
    main()