# -*- coding:utf-8 -*-
import requests
import re
import json
from time import sleep


## json模块的作用是把dict序列化成字符串



def get_page(url):
    try:
        header = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url,headers=header)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print(e.message)
        return None



def parse_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)">.*?name"><a.*?>(.*?)</a>.*?star.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>'
                            ,re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'name':item[2],
            'logo':item[1],
            'mark':item[4] + item[5],
            'time':item[3]
        }
    

def wirte_to_csv(data):
    with open('csv/maoyan_top.csv','a') as f:
        f.write(json.dumps(data,ensure_ascii=False) + "\n")



def main(offset):
    link = 'https://maoyan.com/board/4?offset={}'.format(offset)
    html = get_page(link)
    for it in parse_page(html):
        wirte_to_csv(it)



if __name__ == '__main__':
    for i in range(0,10):
        main(i*10)
        sleep(2)
    print('Write Successfully')
