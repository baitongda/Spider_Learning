# -*- coding:utf-8 -*-

from time import *
from config import *
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import re
from pymongo import MongoClient as MC

class Sina:
    

    def __init__(self):
        self.app = webdriver.Remote(SERVER,desired_capabilities=DESIRE_CAP)
    




if __name__ == '__main__':
    sina = Sina()
    
