# -*-  coding:utf-8 -*-

from time import *
from config import *
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
from pymongo import MongoClient as MC
import login_wechat

class Moment:
    def __init__(self):
        self.app = webdriver.Remote(SERVER,desired_capabilities=DESIRE_CAP)
        self.db = MC(HOST,PORT)
        self.collection = self.db[COLLECTION]
        self.wait = WebDriverWait(self.app,TIMEOUT)


    def date_convert(self,date):
        if re.match(r'\d+分钟前',date):
            mintue = re.match(r'(\d+)',date).group(1)
            date = strftime('%Y年-%m月-%d日',localtime(time()-float(mintue) * 60))

        if re.match(r'\d+小时前',date):
            hour = re.match(r'(\d+)',date).group(1)
            date = strftime('%Y年-%m月-%d日',localtime(time()-float(hour) * 60 * 60))   

        if re.match(r'昨天',date):
            date = strftime('%Y年-%m月-%d日',localtime(time() - 24 * 60 * 60))
            
        if re.match(r'\d+天前',date):
            days = re.match(r'(\d+)',date).group(1)
            date = strftime('%Y年-%m月-%d日',localtime(time() - float(days) * 24 * 60 * 60))
        return date
    

    def crawl_moment(self):
        while True:
            sleep(5)
            self.app.swipe(START_X,START_Y + DISTANCE,START_X,START_Y)
            self.parse()
            sleep(3)
            print('-' * 30)

            #break

    

    def parse(self):
        try:
            items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@resource-id="com.tencent.mm:id/ddn"]//android.widget.FrameLayout')))
            for item in items:
                content = item.find_element_by_id('com.tencent.mm:id/deq').get_attribute('text')
                nickname = item.find_element_by_id('com.tencent.mm:id/apv').get_attribute('text')
                print(nickname)
                print(content)
        except Exception as e:
            _ = e
            pass

    def login(self):
        login_wechat.run(self.app,self.wait)
    

    def enter_moment(self):
        xpath_discover = '//android.widget.LinearLayout/'\
                    'android.widget.RelativeLayout[3]/android.widget.LinearLayout'
        xpath_moment = '//android.widget.LinearLayout/com.tencent.mm.ui.mogic.WxViewPager/'\
                        'android.widget.FrameLayout/android.widget.RelativeLayout/android.widget'\
                        '.ListView/android.widget.LinearLayout[1]'
        discover_btn = login_wechat.get_element(self.wait,(By.XPATH,xpath_discover))
        discover_btn.click() if discover_btn is not None else "enter discover page error"
        moment_btn = login_wechat.get_element(self.wait,(By.XPATH,xpath_moment))
        moment_btn.click() if moment_btn is not None else "enter moment page failed"



if __name__ == '__main__':
    m = Moment()
    m.login()
    sleep(30)
    m.enter_moment()
    m.crawl_moment()