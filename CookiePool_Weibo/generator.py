 # -*- coding:utf-8 -*-
import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from Hash_opt import RedisClient
from check import WeiboVerifyCookie
from picture_code_ import CrackGongGe
from config import *

class CookieGenator(object):

    def __init__(self,website):
        self.website = website
        self.accounts = RedisClient('accounts',website)
        self.cookies = RedisClient('cookies',website)
        self.init_browser()
    

    def init_browser(self):
        if BROWSER_TYPE == 'Chrome':
            self.broswer = webdriver.Chrome()
            
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps['phantomjs.page.setting.userAgent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36"
            self.broswer = webdriver.PhantomJS(desired_capabilities=caps)
            self.broswer.set_window_size(1400,800)
            
        
    

    def __del__(self):
        self.close()


    def close(self):
        try:
            self.broswer.close()
            del self.broswer
        except TypeError:
            print("Browser not opened")
    
    def process_item(self,cookies):
        dict_ = {}
        for cook in cookies:
            dict_[cook['name']] = cook['value']
        return dict_
        
    

    def run(self,accounts,cookies):
        for user in accounts:
            password = self.accounts.get(user)
            print(user,password)
            if not user  in cookies:
                result = self.new_cookies(user,password)
                print(result)
                if result['status'] == 1:
                    result_proccess_item = self.process_item(result['content'])
                    self.cookies.set(user,json.dumps(result_proccess_item))
                    print("成功写入")
                if result['status'] == 2:
                    print(result['content'])
                    self.accounts.delete(user)
                    print("删除成功")
        else:
            print("所有帐号都已成功获取cookies")        
        pass
    
    def new_cookies(self,username,password):
        raise NotImplementedError
        
    


class WeiboCookieGen(CookieGenator):
    def new_cookies(self,username,password):
        return CrackGongGe(username,password,self.broswer).main()
        

    def __init__(self,website="weibo"):
        CookieGenator.__init__(self,website)

if __name__ == "__main__":
    weibo_gen = WeiboCookieGen()
    weibo_gen.run(weibo_gen.accounts.username(),weibo_gen.cookies.username())