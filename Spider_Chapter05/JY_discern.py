# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from io import BytesIO
from PIL import Image

EMAIL = "cakelinxs@outlook.com"
PASS = "linxs572"

class CrackGesest(object):
    def __init__(self):
        self.email = EMAIL
        self.password = PASS
        self.driver = webdriver.Chrome()
        self.url = "https://auth.geetest.com/login/"
        self.wait = WebDriverWait(self.driver,20)
        pass
    
    def get_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_radar_tip')))
        return button

    def get_position(self):
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_canvas_img')))
        sleep(2)
        location = img.location
        size = img.size
        x_,y_,width_,height_ = location['x'],location['y'],location['x'] + size['width'],location['y'] + size['height']
        return (x_,y_,width_,height_)
    
    def get_screenshot(self):
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot
    

    def get_geetest_img(self,name='captcha.png'):
        x,y,width,height = self.get_position()
        screenshot = self.get_screenshot()
        plt = screenshot.crop((x,y,width,height))
        plt.save(name)
    
    def get_slide_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_slider_button')))
        return button
    
    def click_slide(self,button):
        try:
            button.click()
        except Exception as e:
            _ = e
            print("Error in Click Slide Button")
    
    def is_pixels_eq(self,image1,image2,x,y):
        pixel1 = image1.load()[x,y]
        pixel2 = image2.load()[x,y]

        # why to set threshold and why threshold is 60??
        ## ??????
        ## ??????

        threshold = 60

        if abs(pixel1[0] - pixel2[0]) < threshold and \
            abs(pixel1[1] - pixel2[1]) < threshold and \
            abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False
    
        

    def get_gap(self,image1,image2):
        left = 60
        for i in range(left,image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixels_eq(image1,image2,i,j):
                    left = i
                    return left
        return left

    # 获取移动轨迹
    def get_track(self,distance):
        current = 0     # 当前位移
        track = []      # 记录轨迹
        v = 0           # 设置初速度
        mid = distance * 4 / 5
        t = 0.2

        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * t * t
            current += move
            track.append(round(move))
        return track
    

    def move_to_gap(self,slider_btn,track):
        
        ActionChains(self.driver).click_and_hold(slider_btn).perform()
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x,yoffset=0).perform()
        sleep(1)
        ActionChains(self.driver).release().perform()
        pass

    def get_submit_btn(self):
        submit = self.driver.find_element_by_xpath(r'//*[@id="base"]/div[2]/div/div[3]/div/div/form/div[5]/div/button/span')
        ActionChains(self.driver).click(submit).perform()


    def login(self):
        self.driver.find_element_by_xpath('//*[@id="base"]/div[2]/div/\
                div[3]/div/div/form/div[1]/div/div[1]/input').send_keys(geet.email)
        sleep(3)
        self.driver.find_element_by_xpath('//*[@id="base"]/div[2]/div/\
                div[3]/div/div/form/div[2]/div/div[1]/input').send_keys(geet.password)
        sleep(3)

    def verify_slider_code(self):
        ## 获取验证码图片
        self.get_geetest_img()
        sleep(3)

        ## 点击出现滑块并截图
        slide_btn = self.get_slide_button()
        self.click_slide(slide_btn)
        self.get_geetest_img(name='captcha2.png')
        sleep(2)

        ## 打开图片作为Image对象
        image1 = Image.open('captcha.png')
        image2 = Image.open('captcha2.png')


        distance = self.get_gap(image1,image2)
        tract = self.get_track(distance - 6)
        self.move_to_gap(slide_btn,tract)
        sleep(5)


    def main(self):
        self.driver.get(geet.url)
        sleep(5)
        self.login()

        ## 找到点击按钮
        btn = self.get_button()
        btn.click()
        sleep(3)

        self.verify_slider_code()

        try:
            success = geet.wait.until(EC.text_to_be_present_in_element\
                        ((By.CLASS_NAME,'geetest_success_radar_tip_content'),'验证成功'))
        except Exception as e:
            _ = e
            sleep(3)
            self.verify_slider_code()
        geet.get_submit_btn()
        sleep(20)
        self.driver.get_screenshot_as_file('result.png')
        self.driver.quit()    
        
        


if __name__ == '__main__':
    geet = CrackGesest()
    geet.main()
    print("Successfully")

