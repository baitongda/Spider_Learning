# -*- coding:utf-8 -*-

import requests
import codecs
from pyquery import PyQuery as PQ


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}


def get_pages(url,website="66"):
    response = requests.get(url,headers=headers)
    if website == 'goubanjia':
        response.encoding='utf-8'
    elif website == '66' or website == 'xici':
        response.encoding='gb2312'
    with open('xx.html','w') as f:
        f.write(response.text)
    return  response.text


def parse_66(html):
    doc = PQ(html)
    trs = doc("#main > div > div:nth-child(1) > table > tr")
    for tr in trs.items():
        ip = tr('td:nth-child(1)').text()
        port = tr('td:nth-child(2)').text()
        if not ip == 'ip' and not port == 'port':
            yield ':'.join([ip,port])


def parse_xiciproxy(html):
    doc = PQ(html)
    trs = doc('#ip_list  > tr').items()
    for tr in trs:
        colspan = tr.find('th').attr('colspan')
        class_name = tr.attr('class')
        if not colspan and class_name != 'subtitle':
            proxy_info = tr.text().split("\n")
            if proxy_info:
                yield ":".join([proxy_info[0],proxy_info[1]])
            



def parse_guobanjia(html):
    doc = PQ(html)
    tds = doc('#services > div > div.row > div > div > div > table > tbody > tr > td.ip')
    for td  in tds.items():
        td.find('p').remove()
        yield ''.join(td.text().split("\n"))



def main():
    
    start_url = "http://www.xicidaili.com/"
    html = get_pages(start_url,'goubanjia')
    for ip in parse_xiciproxy(html):
        print(ip)
 

if __name__ == '__main__':
    main()