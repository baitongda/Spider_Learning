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





class Spider(object):
    header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'SUID=23FFEBB7771A910A000000005B0F617E; PHPSESSID=uas1uh0cjm17ro884eq2hat2c2; SUIR=1527734654; SUID=757BEAB72613910A000000005B0F617F; SUV=009B2727B7EA7B755B0F6181CE803530; JSESSIONID=aaaiY5dGpNuzNc_55Xjnw; ABTEST=6|1527223113|v1; weixinIndexVisited=1; ppinf=5|1527734969|1528944569|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTYlOUUlOTclRTklOTIlQTYlRTYlQjMlQTJ8Y3J0OjEwOjE1Mjc3MzQ5Njl8cmVmbmljazoyNzolRTYlOUUlOTclRTklOTIlQTYlRTYlQjMlQTJ8dXNlcmlkOjQ0Om85dDJsdUJuR3pSbllSQXR5Q1JCRjVPNXRDS0lAd2VpeGluLnNvaHUuY29tfA; pprdig=YovjITos3EUSS9XXyUYyERH_DYXDM0Km7QKsVT00BTr9SkSj50W41EogXGGvxHi1kPpiPB0TYATW5IhVzkqEiCZnoEyJWhtKF2sW-rWSHz0QZNWQwS-itbi0rmKeqjHPFsam3-zZHLtByPmR15ZRA8R1j6GNegjL9YAE4L5VQaA; sgid=03-33140259-AVsJNBJDcREZjIhcg1IPR1g; sct=3; IPLOC=CN4401; ppmdig=152775221700000010ac9146001c50d66e863d817bc1d426; seccodeErrorCount=1|Thu, 31 May 2018 07:42:13 GMT; SNUID=70ABB8E354513928D9535A6854585EFE; seccodeRight=success; successCount=1|Thu, 31 May 2018 07:42:28 GMT; refresh=1s',
        'Host':'weixin.sogou.com',
        'If-Modified-Since':'Thu, 31 May 2018 12:31:52 +0800',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    detail_header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'rewardsn=; wxtokenkey=777',
        'Host':'mp.weixin.qq.com',
        'If-Modified-Since':'Thu, 31 May 2018 12:31:52 +0800',
        'Referer':'http://weixin.sogou.com/weixin?type=2&query=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98&ie=utf8&s_from=input&_sug_=n&_sug_type_=&w=01015002&oq=&ri=0&sourceid=sugg&sut=234&sst0=1527741110250&lkt=1%2C1527741110147%2C1527741110147',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    base_url = "http://weixin.sogou.com/weixin"
    keyword = '数据挖掘'
    session = Session()
    session.headers.update(header)
    queue = RedisQueue()
    mysql = MySQL()

    def start(self):
        url = self.base_url + '?' + urlencode({'type':2,'query':self.keyword})
        print(url)
        weixin_req = WeixinReq(url,self.parse_index,need_proxy=True,headers=self.header)
        if  isinstance(weixin_req,requests.Request):
            self.queue.add(weixin_req)

    def parse_index(self,response):
        doc = PQ(response)
        #next_ = doc('#sogou_next').attr('href')
        #print(next_)
        lis = doc('#main > div.news-box > ul > li').items()
        for li in lis:
            url = li('div > h3 > a').attr('href')
            if url:
                print("detail url     {}".format(url))
                yield WeixinReq(url,self.parse_detail,need_proxy=True,headers=self.detail_header)

            


    def parse_detail(self,response):
        print("parse detail")
        try:
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
        except Exception as e:
            _ = e
            pass

    def get_proxy(self):
        api_url = 'http://localhost:5000/random'
        try:
            response = requests.get(api_url)
            if response.status_code in VALID_CODE:
                ip_port = response.text
                print(ip_port)
                proxy = {
                    'http':'http://{}'.format(ip_port),
                    'https':'https://{}'.format(ip_port)
                }
                return proxy
            return None
        except Exception as e:
            return None


    def get_proxy_by_aby(self):
        proxies = PROXIES
        return proxies


    def request(self,req): 
        try:
            proxy = self.get_proxy_by_aby()
            if proxy:
                return self.session.send(self.session.prepare_request(req),timeout=req.timeout,proxies=proxy,allow_redirects=True)
            else:
                return  self.session.send(self.session.prepare_request(req),timeout=req.timeout)
           
        except (ConnectionError,ReadTimeout) as e:
            print(e.args)
            return False
    


    def index(self,url):
        req = WeixinReq(url,self.parse_index,headers=self.header)
        if isinstance(req,requests.Request):
            self.queue.add(req)



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
                        if isinstance(result,WeixinReq):
                            self.queue.add(result)
                            
                        if isinstance(result,dict):
                            self.mysql.insert('article',result)
                else:
                    print(results)
                    self.error(weixin_req)
            else:
                self.error(weixin_req)
                        
    
    def run(self,page=1):
        parrms = {
            'type':2,
            'query':self.keyword,
            '_sug_type_':'',
            '_sug_':'n',
            's_from':'input',
            'ie':'utf8'
        }
        for i in range(1,MAX_PAGE + 1):
            print("正在抓取第{}页".format(i))
            parrms['page']=i
            url = self.base_url + '?' + urlencode(parrms)
            self.index(url)
            self.scheduler()
            print("成功抓取第{}页".format(i))
            sleep(1)

if __name__ == '__main__':

    spider = Spider()
    spider.run()
  