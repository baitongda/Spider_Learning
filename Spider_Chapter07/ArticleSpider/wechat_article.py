# -*- coding:utf-8 -*-

from WeixinRequest import WeixinReq
from config import *
from mysql import MySQL
from RedisQueue import RedisQueue
from urllib.parse import urlencode
from requests import Session
import requests
from requests import ReadTimeout,ConnectionError
from pyquery import PyQuery as PQ
from pprint import pprint
import re
from random import choice
import json
from time import sleep

header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'IPLOC=JP; SUID=C8A23D6C7C20940A000000005B0942D8; SUV=1527333592995690; ABTEST=0|1527333594|v1; SNUID=761C83D3BFBAD2A5AEE2E4D2BF251F58; weixinIndexVisited=1; ppinf=5|1527337282|1528546882|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTYlOUUlOTclRTklOTIlQTYlRTYlQjMlQTJ8Y3J0OjEwOjE1MjczMzcyODJ8cmVmbmljazoyNzolRTYlOUUlOTclRTklOTIlQTYlRTYlQjMlQTJ8dXNlcmlkOjQ0Om85dDJsdUJuR3pSbllSQXR5Q1JCRjVPNXRDS0lAd2VpeGluLnNvaHUuY29tfA; pprdig=KDU9GBRwpuwesfb7fVo4JUuPkvdBQzSCnl7W6ApH00kDth9WP7YhRa_W6GYrszPAvkd2EYOpWeNRFi9mN_CTIf88K3tTPBH4dSasGl13XIkTaJJCk1sQCgnI_umIbxHutrtIS5G4B5YftsjdfKMCD3xSimXQN02Gio9RPW_qEO8; sgid=03-33140259-AVsJL5nYzPgF7NBtJFAlK00',
    'Host':'weixin.sogou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}




class Spider(object):
    base_url = "http://weixin.sogou.com/weixin"
    keyword = '数据挖掘'
    session = Session()
    queue = RedisQueue()
    mysql = MySQL()

    def start(self):
        url = self.base_url + '?' + urlencode({'type':2,'query':self.keyword})
        print(url)
        self.session.headers.update(header)
        weixin_req = WeixinReq(url,self.parse_index,need_proxy=True)
        if  isinstance(weixin_req,requests.Request):
            self.queue.add(weixin_req)

    def parse_index(self,response):
        doc = PQ(response)
        next_ = doc('#sogou_next').attr('href')
        lis = doc('#main > div.news-box > ul > li').items()
        
        for li in lis:
            url = li('div > h3 > a').attr('href')
            if url:
                print("detail url     {}".format(url))
                yield WeixinReq(url=url,need_proxy=True,callback=self.parse_detail)
            
        
        if next_:
            next_ = self.base_url + str(next_)
            print("next     {}".format(next_))
            yield WeixinReq(next_,self.parse_index,need_proxy=True)
        






    def parse_detail(self,response):
        doc = PQ(response)
        title = doc('#activity-name').text()
        wechat = doc('#profileBt > a').text()
        nickname = doc('#meta_content > span.rich_media_meta.rich_media_meta_text').text()
        date = re.search(r'var(.*?)publish_time(.*?)"(.*?)"',response).group(3)
        content = doc('#js_content').text()
        data = {
            'title':re.search(r'if(.*?)else(.*?)"(.*?)"',title).group(3),
            'content':content,
            'date':date,
            'wechat':wechat,
            'nickname':nickname
        }
        yield data

    def get_proxy(self):
        info = {'H36E5BU7Z7S947YD':'601B13BF18C7D672','H55GOW59F41256CD':'0898C1DD44D3CD85'}
        users = ['H36E5BU7Z7S947YD','H55GOW59F41256CD']
        api_url = "http://{}:{}@{}:{}"
        host = "http-dyn.abuyun.com"
        port = "9020"
        user = choice(users)
        pass_ = info.get(user)
        proxies = {'http':api_url.format(user,pass_,host,port)}
        test_url = "http://weixin.sogou.com/weixin?type=2&query=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98&\
                    ie=utf8&s_from=input&_sug_=y&_sug_type_=&w=01019900&sut=5185&sst0=1527316635442&lkt\
                    =1%2C1527316635340%2C1527316635340"
        response = requests.get(test_url,proxies=proxies)
        if response.status_code in VALID_CODE:
            return proxies
        return False

    def request(self,req): 
        self.session.headers.update(header)
        try:
            proxy = self.get_proxy()
            if proxy:
                print(proxy)
                return self.session.send(req.prepare(),timeout=req.timeout,allow_redirects=True,proxies=proxy)
            else:
                return  self.session.send(req.prepare(),timeout=req.timeout,allow_redirects=True)
           
        except (ConnectionError,ReadTimeout) as e:
            print(e.args)
            return False
    


    def error(self,req):
        req.fail_time = req.fail_time + 1
        print("req faild time {}".format(req.fail_time))
        if req.fail_time < MAX_FAIL_TIME:
            self.queue.add(req)

    def scheduler(self):
        while not self.queue.empty():
            weixin_req = self.queue.pop()
            callback = weixin_req.callback
            print("Schedule    {}".format(weixin_req.url))
            respon = self.request(weixin_req)
            if not isinstance(respon,bool):
                print(respon.status_code)
            else:
                print("bool")
            if respon and respon.status_code in VALID_CODE:
                results = list(callback(respon.text))
                if results:
                    for result in results:
                        print("New Result     {}".format(result))
                        if isinstance(result,WeixinReq):
                            self.queue.add(result)
                            
                        if isinstance(result,dict):
                            self.mysql.insert('article',result)
                else:
                    self.error(weixin_req)
            else:
                self.error(weixin_req)
                        
    




if __name__ == '__main__':
    spider = Spider()
    spider.start()
    spider.scheduler()