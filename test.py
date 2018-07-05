# -*- coding:utf-8 -*-

from selenium import webdriver
from time import sleep


firefox = webdriver.Firefox()
firefox.get("http://www.baidu.com")
sleep(10)
firefox.quit()