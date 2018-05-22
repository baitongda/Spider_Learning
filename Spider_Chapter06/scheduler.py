# -*- coding:utf-8 -*-

from multiprocessing import Process
from flask_api import app
from generator import *
from check import *
from time import sleep
from config import *

'''
GENERATOR_MAP = {return broswer
    'weibo':'WeiboCookieGen'
}

TEST_MAP = {
    'weibo':'WeiboVerifyCookie'
}
'''


class Scheduler(object):

    @staticmethod
    def api():
        print("API接口开始运行")
        app.run(host=API_ADDRESS,port=API_PORT)
        
    
    @staticmethod
    def generate_cookies(cycle=CYCLE):
        weibo_cookies = WeiboCookieGen(website="weibo")
        accounts = weibo_cookies.accounts.username()
        cookies_ = weibo_cookies.cookies.username()
        print("开始生成cookies")
        while True:
            try:
                for website,cls_ in GENERATOR_MAP.items():
                    print(website,cls_)
                    generator = eval("{}('{}')".format(cls_,website))
                    generator.run(accounts,cookies_)
                    print("生成完成")
                    #generator.close()
                    sleep(cycle)
                pass
            except Exception as e:
                raise e
        pass
    

    @staticmethod
    def verify_cookies(cycle=CYCLE):
        print("开始检查cookies")
        while True:
            try:
                for website,cls_ in TEST_MAP.items():
                    print(website,cls_)
                    tester = eval("{}('{}')".format(cls_,website))
                    #print("{}({})".format(cls_,website))
                    #print(type(tester))
                    tester.run()
                    print("检查完成")
                    sleep(cycle)
            except Exception as e:
                print(e.args)
        pass
    

    def run(self):
        if GENERATOR_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()
        
        if TEST_PROCESS:
            generator_process = Process(target=Scheduler.generate_cookies)
            generator_process.start()
        
        if API_PROCESS:
            verify_process = Process(target=Scheduler.verify_cookies)
            verify_process.start()
        # start three process to run methods abrove
        pass




if __name__ == '__main__':
    sch = Scheduler()
    sch.run()