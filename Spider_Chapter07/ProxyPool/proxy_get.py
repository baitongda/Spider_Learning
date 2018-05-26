# -*- coding:utf-8 -*-

from utils_.utils_ import *
from time import sleep

# define a meta class to setting the number of crawler function and the count of that
class ProxyMetaClass(type):
    def __new__(cls,name,bases,attrs):
        attrs['__CrawleFunc__'] = []
        count = 0
        for k,v in attrs.items():
            if 'crawle' in k:
                attrs['__CrawleFunc__'].append(k)
                count += 1
        attrs['__CrawleCount__'] = count
        return type.__new__(cls,name,bases,attrs)



class Crawler(object,metaclass=ProxyMetaClass):
    def get_proxies(self,callack):
        proxies = []
        if callack == 'crawle_daili66':
            return self.process_daili66(callack)
        else:
            for proxy in eval("self.{}()".format(callack)):
                print("成功获取代理 {}".format(proxy))
                proxies.append(proxy)
            return proxies
    

    def process_daili66(self,callback):
        proxies = []
        for page_count in range(1,11):
            for proxy in eval("self.{}(page_count={})".format(callback,page_count)):
                print("成功获取代理 {}".format(proxy))
                proxies.append(proxy)
        return proxies


    def crawle_xiciproxy(self):
        start_url = "http://www.xicidaili.com/"
        html = get_pages(start_url,"xici")
        if html:
            return parse_xiciproxy(html)
        
    

    def crawle_daili66(self,page_count=1):
        start_url = "http://www.66ip.cn/{}.html"
        sleep(5)
        html = get_pages(start_url.format(page_count),website="66")
        if html:
            print("第{}页代理".format(page_count))
            return parse_66(html)
    

    def crawle_guobanjia(self):
        start_url = "http://www.goubanjia.com/"
        html = get_pages(start_url,'goubanjia')
        if html:
            return parse_guobanjia(html)
        pass





def MAIN():
    crawl = Crawler()
    crawl.get_proxies("crawle_daili66")


if __name__ == '__main__':
    MAIN()
