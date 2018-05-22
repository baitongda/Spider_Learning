# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from time import sleep

class ActChains_(object):
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(chrome_options=self.option)
        self.driver.implicitly_wait(10)

    def act_chains_test(self,url):
        browser = self.driver
        browser.get(url)
        browser.switch_to_frame('iframeResult')
        source = browser.find_element_by_id('draggable')
        target = browser.find_element_by_id('droppable')
        action_chains = ActionChains(browser)
        action_chains.drag_and_drop(source,target)
        action_chains.perform()
        browser.switch_to_alert().accept()
        sleep(10)
    
    def get_text(self,url):
        browser = self.driver
        browser.get(url)
        button = browser.find_element_by_id('zu-top-add-question')
        print(button.text)
        print(button.get_attribute('class'))
        print(button.id)
        print(button.tag_name)
        print(button.location)
        print(button.size)
    
    def parently_wait(self,url):
        browser = self.driver
        browser.get(url)
        wait = WebDriverWait(browser,10)
        try:
            input_btn = wait.until(EC.presence_of_all_element_located((By.ID,'q')))
            clicked_ = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn-search.tb-bg')))
        except Exception as e:
            _ = e
            self.driver.close()
        print(input_btn,clicked_)
    

    def forward_and_back(self,urls):
        u_one,u_two,u_three = urls
        browser = self.driver
        browser.get(u_one)
        browser.get(u_two)
        browser.get(u_three)
        sleep(3)
        browser.back()
        sleep(2)
        browser.forward()
        sleep(4)

    def get_cookies(self,url):
        browser = self.driver
        browser.get(url)
        pprint(browser.get_cookies())
        browser.add_cookie({'name':'name','domain':'www.zhihu.com','value':'germay'})
        print('-------------------------------')
        pprint(browser.get_cookies())
        browser.delete_all_cookies()
        pprint(browser.get_cookies())
    

    def swith_to_options(self,urls):
        one,two,three = urls
        browser = self.driver
        browser.get(one)
        browser.execute_script('window.open()')
        print(browser.window_handles)
        browser.switch_to_window(browser.window_handles[1])
        browser.get(two)
        sleep(4)
        browser.switch_to_window(browser.window_handles[0])
        browser.get(three)
        sleep(5)
        browser.quit()


    def exceptions_process(self,url):
        brower = self.driver
        brower.implicitly_wait(15)
        try:
            brower.get(url)
            #sleep(20)
            brower.find_element_by_id('xxx')
        except TimeoutError as t:
            print('Time Out {}'.format(t.args))
        except NoSuchElementException as n:
            print('Can not find the Element {}'.format(n.args))
        finally:
            brower.quit()

def main():
    chain = ActChains_()
    #url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
    #chain.act_chains_test(url)
    #url = 'https://www.zhihu.com/explore'
    #chain.get_text(url)
    #url = 'https://www.taobao.com'
    #chain.parently_wait(url)
    #urls = ('https://taobao.com','https://zhihu.com','https://www.python.org')
    #chain.forward_and_back(urls)
    #url = 'https://www.zhihu.com/explore'
    #chain.get_cookies(url)
    #urls = ('https://taobao.com','https://zhihu.com','https://www.baidu.com')
    #chain.swith_to_options(urls)
    url = 'https://www.zhihu.com'
    chain.exceptions_process(url)
    pass

if __name__ == '__main__':
    main()