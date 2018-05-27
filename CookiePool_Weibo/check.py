# -*- coding:utf-8 -*-

from requests.exceptions import ConnectionError
import requests
import json
from Hash_opt import RedisClient
from config import *

class VerifyCookie(object):

    def __init__(self,website="default"):
        self.website = website
        self.accounts = RedisClient("accounts",self.website)
        self.cookies = RedisClient("cookies",self.website)
    
    

    def test(self,username,cookie):
        raise NotImplementedError
        
    
    def run(self):
        cookies_group = self.cookies.all()
        for username,cookie in cookies_group.items():
            if isinstance(cookie,bytes):
                cookie = bytes.decode(cookie)
                self.test(username,cookie)


class WeiboVerifyCookie(VerifyCookie):
    def __init__(self,website="weibo"):
        VerifyCookie.__init__(self,website=website)
        
    
    def test(self,username,cookie):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'm.weibo.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        try:
            cookie = json.loads(cookie)
            pass
        except TypeError as e:
            _ = e
            print("删除 {} cookies".format(username))
            #self.cookies.delete(username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url,headers=header,cookies=cookie,timeout=20,allow_redirects=False)
            if response.status_code == 200:
                print("{} cookie 有效".format(username))
                with open('xx.html','w') as f:
                    f.write(response.text)
            else:
                print(response.status_code)
                print("{} Cookie 无效".format(username))
                print("Delete Cookies")
                #self.cookies.delete(username)
        except ConnectionError as e:
            _ = e
            print("连接异常")

        pass



def main():
    dict_ = {'xxx':'fff','fsdfs':'ssss'}
    for d,l in  dict_.items():
        print(d,l)
    tester = WeiboVerifyCookie(website="weibo")
    tester.run()
if __name__ == '__main__':
    main()