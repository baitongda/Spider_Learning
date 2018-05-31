# -*- coding:utf-8 -*-



# appium config
SERVER = "http://localhost:4723/wd/hub"
PLATFORM = "Android"
DEVICE = "NEM_AL10"
PACKAGE_WECHAT = "com.tencent.mm"
ACTIVITY_WECHAT=".ui.LauncherUI"
PACKAGE_SINA="com.sina.weibo"
ACTIVITY_SINA=".MainTabActivity"
USERNAME = "643995048"
PASSWORD = "123456789xke."
TIMEOUT=20

DESIRE_CAP = {
    'platformName':PLATFORM,
    'deviceName':DEVICE,
    'appActivity':ACTIVITY_SINA,
    'appPackage':PACKAGE_SINA
}


# MONGO Config
HOST = "localhost"
PORT = 27017
COLLECTION = "we_moments"



# slide moments
START_X=300
START_Y=300
DISTANCE=550