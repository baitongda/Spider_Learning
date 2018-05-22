# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from io import BytesIO
from PIL import Image
from os import listdir

PHONE = '15914795353'
PASSWORD = '7218246weibo'
PATH = r'/home/linxs/_DOC/linxs/__My__DOC/Project/Python/Basic_Project/SpiderAction/Spider_Chapter05/weibo/'

class CrackGongGe(object):
    def __init__(self,user,passwd):
        self.url = 'https://passport.weibo.cn/signin/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,20)
        self.phone = user
        self.password = passwd
    

    def login_successfully(self):
        try:
            bool(WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'topBarWrap'))))
        except Exception as e:
            _ = e
            return False
    

    def login_failed(self):
        try:
            bool(WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.ID,'errMsg')),'用户名或密码错误'))
        except Exception as e:
            _ = e
            return False
    

    def get_cookies(self):
        return self.browser.get_cookies()
        
    def open(self):
        self.browser.get(self.url)
        input_user = self.wait.until(EC.presence_of_element_located((By.ID,'loginName')))
        input_pass = self.wait.until(EC.presence_of_element_located((By.ID,'loginPassword')))
        submit_btn = self.wait.until(EC.element_to_be_clickable((By.ID,'loginAction')))
        
        input_user.send_keys(self.phone)
        input_pass.send_keys(self.password)
        sleep(2)
        submit_btn.click()
        
    def get_screen_shot(self):
        screent_shot = self.browser.get_screenshot_as_png()
        screent_shot = Image.open(BytesIO(screent_shot))
        return screent_shot

    def get_captcha_image(self,name='captcha.png'):
        screen = self.get_screen_shot()
        position = self.get_position()
        x,y,width,height = position
        captcha = screen.crop((x,y,width,height))
        captcha.save(name)
        return captcha
        
    def get_position(self):
        try:
            img_elem = self.wait.until(EC.presence_of_element_located((By.ID,'patternCaptchaHolder')))
        except TimeoutException as e:
            print('Timeout ')
            _ = e
        sleep(2)
        location = img_elem.location
        size = img_elem.size
        x_,y_,width_,height_ = location['x'],location['y'],location['x'] + size['width'],location['y'] + size['height']
        return (x_,y_,width_,height_)

    def is_equal_pixel(self,image1,image2,x,y):
        threshold = 5
        pixel1 = image1.load()[x,y]
        pixel2 = image2.load()[x,y]
        ## 如何判断像素是否相等
        ## 两个像素点的差在阀值之内
        if abs(pixel1[0] - pixel2[0]) < threshold and \
            abs(pixel1[1] - pixel2[1]) < threshold and \
            abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def same_image(self,image,tempture):
        count = 0
        width = image.width
        height = image.height
        for i in range(width):
            for k in range(height):
                if self.is_equal_pixel(image,tempture,i,k):
                    count += 1
        threshole = 0.97
        result = float(count) / (width * height)
        print(result)
        if result > threshole:
            print("识别成功")
            return True
        return False
    
    def detect(self,image,templates_folder):
         for template_name in listdir(templates_folder):
            print("正在匹配:   {}".format(template_name))
            file_path = templates_folder + '{}'
            template = Image.open(file_path.format(template_name))
            if self.same_image(image,template):
                numbers = [int(number) for  number in list(template_name.split('.')[0])]
                print("拖动顺序:   {}".format(numbers))
                return numbers

    def move(self,numbers):
        dy = dx = 0
        circles = self.browser.find_elements_by_css_selector('.patt-wrap .patt-circ')
        for i in range(4):
            circle = circles[numbers[i] - 1]
            if i == 0:
                width = circle.size['width'] / 2
                height = circle.size['height'] / 2
                ActionChains(self.browser).move_to_element_with_offset(circle,width,height).click_and_hold().perform()
                
            else:
                times = 30
                for time in range(times):
                    _ = time
                    ActionChains(self.browser).move_by_offset(dx / times,dy / times).perform()
                    sleep(1 / times)
            if i == 3:
                ActionChains(self.browser).release().perform()
                
            else:
                dx = circles[numbers[i + 1] - 1].location['x'] - circle.location['x']
                dy = circles[numbers[i + 1] - 1].location['y'] - circle.location['y']                
                
    
    def main(self):
        self.open()
        if self.login_failed:
            return {
                'status':2,
                'content':'用户名密码错误'
            }
        if self.login_successfully:
            cookies = self.get_cookies()
            return {
                'status':1,
                'content':cookies
            }
        sleep(3)
        image = gongge.get_captcha_image()
        slide_orders = self.detect(image,PATH)
        if slide_orders:
            self.move(slide_orders)
            if self.login_successfully:
                # 需要验证码登录的情况
                cookies = self.get_cookies()
                return {
                    'status':1,
                    'content':cookies
                }
            else:
                return {
                    'status':3,
                    'content':'登录失败'
                }


if __name__ == '__main__':
    gongge = CrackGongGe(PHONE,PASSWORD)
    gongge.open()
    sleep(3)
    image = gongge.get_captcha_image()
    slide_orders = gongge.detect(image,PATH)
    print(slide_orders)
    if slide_orders:
        print(slide_orders)
        gongge.move(slide_orders)

    '''
    count = 0
    path = r'/home/linxs/_DOC/linxs/__My__DOC/Project/Python/Basic_Project/SpiderAction/Spider_Chapter05/weibo/{}.{}'
    while True:
        gongge.open()
        sleep(3)
        gongge.get_captcha_image(name=path.format(str(count),'png'))
        count += 1
    '''


