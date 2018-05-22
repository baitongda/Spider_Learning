# -*- coding:utf-8 -*-
from proxy_get import Crawler
from proxy_store import RedisClient
from config import * 

class Getter(object):
    def __init__(self):
        self.db = RedisClient()
        self.crawler = Crawler()
    

    def is_over_threshold(self):
        if self.db.count() >= PROXY_POOL_THRESHOLD:
            return True
        return False
    



    def storge_to_redis(self,proxies):
        if isinstance(proxies,list):
            for proxy in proxies:
                self.db.add(proxy)
    



    def run(self):
        print("获取器开始执行")
        if not self.is_over_threshold():
            print(self.crawler.__CrawleCount__)
            for callback_index in range(self.crawler.__CrawleCount__):
                callback = self.crawler.__CrawleFunc__[callback_index]   
                proxies = self.crawler.get_proxies(callback)
                self.storge_to_redis(proxies)




    

if __name__ == '__main__':
    get = Getter()
    get.run()