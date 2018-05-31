# -*- coding:utf-8 -*-
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import *
from time import sleep


def get_element(wait,locator):
    try :
        element = wait.until(EC.presence_of_element_located(locator))
        return element
    except Exception as e:
        _ = e
        return None

def get_elements(wait,locator):
    try:
        elements = wait.until(EC.presence_of_all_elements_located(locator))
        return elements
    except Exception as e:
        _ = e
        return None 


def qq_login(wait,username,password):
    choose_qq_btn = get_element(wait,(By.ID,'com.tencent.mm:id/bwm'))
    choose_qq_btn.click() if choose_qq_btn is not None else "choose error"
    eles = get_elements(wait,(By.ID,'com.tencent.mm:id/hx'))
    if eles:
        eles[0].send_keys(username)
        eles[1].send_keys(password)
    submit_btn = get_element(wait,(By.ID,'com.tencent.mm:id/bwn'))
    submit_btn.click() if submit_btn is not None else "login error"


def run(driver,wait):
    # open wechat
    server = SERVER
    desires_cap = {
        'platformName':PLATFORM,
        'deviceName':DEVICE,
        'appPackage':PACKAGE_WECHAT,
        'appActivity':ACTIVITY_WECHAT
    }
    #driver = webdriver.Remote(server,desired_capabilities=desires_cap)
    #wait = WebDriverWait(driver,20)

    # 允许存储权限
    storge_perm = get_element(wait,(By.ID,\
            'com.android.packageinstaller:id/permission_allow_button'))
    storge_perm.click() if storge_perm is not None else "storge permission error"

    # 允许电话权限
    phone_perm = get_element(wait,(By.ID,\
            'com.android.packageinstaller:id/permission_allow_button'))
    phone_perm.click() if phone_perm is not None else "phone permission error"

    # 点击登录按钮
    login_btn = get_element(wait,(By.ID,'com.tencent.mm:id/d1w'))
    login_btn.click() if login_btn is not None else "login btn error"

    # 使用QQ登录
    qq_login(wait,USERNAME,PASSWORD)

if __name__ == '__main__':
    pass    