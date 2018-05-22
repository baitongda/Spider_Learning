# -*- coding:utf-8 -*-
import urllib
from http.cookiejar import CookieJar,MozillaCookieJar,LWPCookieJar

def get_cookie():
    c = CookieJar()
    c_manage = urllib.request.HTTPCookieProcessor(c)
    opener = urllib.request.build_opener(c_manage)
    response = opener.open('http://www.baidu.com')
    for item in c:
        print('{} =  {}'.format(item.name,item.value))
    


def save_cookie_on_file(path):
    # 第一种保存cookie到文件的方式
    #cookie = MozillaCookieJar(path)
    
    # 第二种保存cookie到文件的方式
    cookie = LWPCookieJar(path)
    cookie_manage = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookie_manage)
    response = opener.open('https://www.baidu.com')
    cookie.save(ignore_discard=True,ignore_expires=True)


def use_cookies_local(filename):
    cookie = LWPCookieJar()
    cookie.load('cookies.txt',ignore_discard=True,ignore_expires=True)
    cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookie_handler)
    response = opener.open('https://www.baidu.com')
    print(response.read().decode('utf-8'))


def main():
    path = r'cookies.txt'
    #save_cookie_on_file(path)
    use_cookies_local(path)


if __name__ == '__main__':
    main()