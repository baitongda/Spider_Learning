# -*- coding:utf-8 -*-


from selenium import webdriver

import requests
from pickle import dump,load

class Login(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = "http://weixin.sogou.com/"


    def login(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_id("loginBtn").click()
        from time import sleep
        sleep(30)
        request = requests.session()
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            request.cookies.set(cookie['name'],cookie['value'])
        respon = request.get(self.url)
        respon.encoding='utf-8'
        with open('test.html','w') as f:
            f.write(respon.text)

    def access(self):
        request = requests.session()
        header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'IPLOC=JP; SUID=C8A23D6C7C20940A000000005B0942D8; SUV=1527333592995690; ABTEST=0|1527333594|v1; SNUID=761C83D3BFBAD2A5AEE2E4D2BF251F58; weixinIndexVisited=1; ppinf=5|1527337282|1528546882|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTYlOUUlOTclRTklOTIlQTYlRTYlQjMlQTJ8Y3J0OjEwOjE1MjczMzcyODJ8cmVmbmljazoyNzolRTYlOUUlOTclRTklOTIlQTYlRTYlQjMlQTJ8dXNlcmlkOjQ0Om85dDJsdUJuR3pSbllSQXR5Q1JCRjVPNXRDS0lAd2VpeGluLnNvaHUuY29tfA; pprdig=KDU9GBRwpuwesfb7fVo4JUuPkvdBQzSCnl7W6ApH00kDth9WP7YhRa_W6GYrszPAvkd2EYOpWeNRFi9mN_CTIf88K3tTPBH4dSasGl13XIkTaJJCk1sQCgnI_umIbxHutrtIS5G4B5YftsjdfKMCD3xSimXQN02Gio9RPW_qEO8; sgid=03-33140259-AVsJL5nYzPgF7NBtJFAlK00',
            'Host':'weixin.sogou.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        request.headers.update(header)
        url = "http://weixin.sogou.com/weixin?query=nba&hp=40&sut=6955&lkt=8%2C1527337472357%2C1527337476997&_sug_=y&sst0=1527337479426&oq=nb&stj0=0&stj1=4&stj=0%3B4%3B0%3B0&stj2=0&hp1=&_sug_type_=-1&s_from=input&ri=0&type=2&page=11&ie=utf8&w=01015002&dr=1"
        respon = request.get(url)
        respon.encoding='utf-8'
        with open('test.html','w') as f:
            f.write(respon.text)

def main():
    Login().access()

if __name__ == '__main__':
    main()