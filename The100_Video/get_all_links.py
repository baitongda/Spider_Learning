# -*- coding:utf-8 -*-

from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from j.Api import js


class GetVideoLink:
    def __init__(self):
        self.url = "https://share.weiyun.com/da9194d53005ef7303302fc7b294aec7"
        self.timeout = 20
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver,self.timeout)
        self.data = {"url":"","size":""}
        self.sizes = []
    
    # open the website
    def open(self):
        self.driver.get(self.url)
    
    # close the browser
    def close(self):
        self.driver.quit()


    # get size of all the video
    def get_videos_size(self):
        size_list = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/'\
                    'div[1]/ul/li/div/div[2]/span[2]/span')
        for size in size_list:
            size = size.text
            try:
                size = size.split(' ')[0]
                size = float(size)
                if size not in self.sizes:
                    self.sizes.append(size)
            except Exception as e:
                print("Something wrong")
                print(e.args)
                self.driver.quit()
            


    # enter the video page
    def enter(self):
        chrome = self.driver
        tv_series_name_xpath = '//*[@id="app"]/div/div[2]/div/div/div/div[2]/'\
                    'div[1]/div[2]/div[1]/ul/li/div/div[1]/div[3]/a'
        season_xpath = '//*[@id="app"]/div/div[2]/div/div/div/div[2]/div[1]/'\
                    'div[2]/div[1]/ul/li[1]/div/div[1]/div[3]/a'
        self.wait.until(EC.presence_of_element_located((By.XPATH,tv_series_name_xpath)))
        chrome.find_element_by_xpath(tv_series_name_xpath).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH,season_xpath)))
        chrome.find_element_by_xpath(season_xpath).click()
        sleep(1)
        self.get_videos_size()
        self.open_play_page()

    # get play page source
    def get_source(self,main_handle,handles):
        try:
            if main_handle != handles[1]:
                self.driver.switch_to_window(handles[1])
                return self.driver.page_source
        except Exception as e:
            print("something wrong")
            print(e.args)


    # open the play page
    def  open_play_page(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'list-group')))
        play_link_xpath = '//*[@id="app"]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/'\
                        'div[1]/ul/li/div/div[1]/div[3]/a'
        play_links = self.driver.find_elements_by_xpath(play_link_xpath)
        main_handle = self.driver.current_window_handle
        while play_links:
            element = play_links.pop()
            element.click()
            handls = self.driver.window_handles
            self.extract_link(self.get_source(main_handle, handls))
            sleep(3)
            if main_handle != self.driver.current_window_handle:
                self.driver.close()
            self.driver.switch_to_window(main_handle)
            
            
    # extract the link
    def extract_link(self,pagesource):
        pattern = re.compile(r'<video(.*?)src="(.*?)"')
        detail_url = pattern.search(pagesource)
        if detail_url:
            detail_url = detail_url.group(2)
        size = self.sizes.pop()
        self.data["url"] = "{}".format(detail_url)
        self.data["size"] = "{}".format(size)
        self.write_to_file(self.data)

    # write to the file by json
    def write_to_file(self,result):
        with open('the100.txt','a') as f:
            f.write("{}\n".format(result))
    
    # load the file 
    def load_txt(self):
        datas = []
        with open('the100.txt','r') as f:
            string = f.read().split('\n')
        for l in string:
            if l != '':
                data = eval(str(l))
                if data not in datas:datas.append(data)
        return datas 

if __name__ == '__main__':
    test = GetVideoLink()
    test.open()
    test.enter()
    test.close()