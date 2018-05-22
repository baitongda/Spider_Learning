# -*- coding:utf-8 -*-
import requests
import codecs
from pyquery import PyQuery as pq


def get_html(url):
    header = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/51.0.2830.34'
    }
    res = requests.get(url,headers=header)
    return res.text

def sava(data):
    with codecs.open('content/data.txt','a',encoding='utf-8') as file:
        file.write(data + "\n")
    print('Write Successfully')


def main():
    url = 'https://www.zhihu.com/explore'
    html = get_html(url)
    items = pq(html)('.explore-feed').items()
    for item in items:
        question = item.find('h2').text()
        author = item.find('.author-link').text()
        answer = pq(item.find('.content').html()).text()
        data = {'q':question,'a':author,'an':answer}
        sava(str(data))
        #sava(str(data) + "\n")
    pass

if __name__ == '__main__':
    main()