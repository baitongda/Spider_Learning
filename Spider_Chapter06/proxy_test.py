# -*- coding:utf-8 -*-


from selenium import webdriver




def main():
    proxy = "127.0.0.1:1080"
    option = webdriver.ChromeOptions()
    option.add_argument('--proxy-server=http://{}'.format(proxy))
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://www.google.com')
    import time
    time.sleep(10)
    pass

if __name__ == '__main__':
    main()  