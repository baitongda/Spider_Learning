# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from ChaojiYing_ import Chaojiying_Client
from selenium.webdriver import ActionChains 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import os
from io import BytesIO
from PIL import Image

PHONE = '15914795353'
PASSWORD = '7218246.'
CHAOJIYING_USERNAME = 'linxs572'
CHAOJIYING_PASSWORD = '7218246.'
CHAOJIYING_SOFTID = 896501
CHAOJIYING_KIND = 9004


class CrackTouClick(object):
    def __init__(self):
        self.url = 'https://www.jianshu.com/sign_in'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,20)
        self.phone_num = PHONE
        self.password = PASSWORD
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME,CHAOJIYING_PASSWORD,CHAOJIYING_SOFTID)
    

    def open(self):
        chrome = self.browser
        chrome.get(self.url)
        username_input = self.wait.until(EC.presence_of_element_located((By.ID,'session_email_or_mobile_number')))
        pass_input = self.wait.until(EC.presence_of_element_located((By.ID,'session_password')))
        username_input.send_keys(self.phone_num)
        pass_input.send_keys(self.password)
        pass

    def get_touclick_btn(self):
        touclick_btn = self.wait.until(EC.element_to_be_clickable((By.ID,'sign-in-form-submit-btn')))
        return touclick_btn
    

    def get_image_element(self):
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_widget')))
        return element
    

    def get_img_postition(self):
        element = self.get_image_element()
        location = element.location
        size = element.size
        print(location)
        print(size)
        x_,y_,width_,height_ = location['x'],location['y'],location['x'] + size['width'],location['y'] + size['height']
        return (x_,y_,width_,height_)
    



    def get_screen_shot(self,locations):
        x,y,width,height = locations
        screent_shot = self.browser.get_screenshot_as_png()
        screent_shot = Image.open(BytesIO(screent_shot))
        screent_shot = screent_shot.crop((x,y,width,height))
        return screent_shot



    def get_points(self,captcha_result):
        points = captcha_result.get('pic_str').split('|')
        #locations = [[int(num) for num in point.split(',')] for point in points]
        locations = []
        for p in points:
            locations.append([int(num) for num in p.split(',')])
        print(locations)
        return locations


    def touch_click_words(self,touch_click_element,locations):
        orders = input('Orders:    ')
        orders = orders.split(',')
        for order in orders:
            x = locations[int(order)]
            ActionChains(self.browser).move_to_element_with_offset(touch_click_element,x[0],x[1]).click().perform()
            sleep(2)


    def get_submit_verify_btn(self):
        verify_btn = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_commit_tip')))
        return verify_btn




def main():
    touclick = CrackTouClick()
    touclick.open()
    click_btn = touclick.get_touclick_btn()
    click_btn.click()
    sleep(20)

    pos = touclick.get_img_postition()
    captcha = touclick.get_screen_shot(pos)
    byte_io = BytesIO()
    captcha.save(byte_io,format='PNG')
    CHAOJIYING_KIND = input('Kind:    ')
    CHAOJIYING_KIND = int(CHAOJIYING_KIND)
    result = touclick.chaojiying.PostPic(byte_io.getvalue(),CHAOJIYING_KIND)
    print(result)
    
    clicked_location = touclick.get_points(result)
    img_ele = touclick.get_image_element()
    touclick.touch_click_words(img_ele,clicked_location)
    touclick.get_submit_verify_btn().click()
    sleep(20)
    pass

if __name__ == '__main__':
    main()
