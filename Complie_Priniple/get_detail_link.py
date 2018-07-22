# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlencode
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'NTESSTUDYSI=db169379c7ad4015ad9c485520ba9745; EDUWEBDEVICE=0351fa0c622a4317aa7250aca68580ef; utm="eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|"; mp_MA-A976-948FFA05E931_hubble=%7B%22sessionReferrer%22%3A%20%22https%3A%2F%2Fwww.icourse163.org%2Flearn%2FHIT-1002123007%3Ftid%3D1002655021%23%2Flearn%2Fcontent%22%2C%22updatedTime%22%3A%201532242580146%2C%22sessionStartTime%22%3A%201532242580135%2C%22sendNumClass%22%3A%20%7B%22allNum%22%3A%201%2C%22errSendNum%22%3A%200%7D%2C%22deviceUdid%22%3A%20%2228d98e28-cb29-42b3-8891-992a08bd1ea1%22%2C%22persistedTime%22%3A%201532242580131%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22da_screen%22%2C%22time%22%3A%201532242580146%7D%2C%22sessionUuid%22%3A%20%22fd7336ee-d4be-4176-9920-d6671ab7b535%22%7D; __utma=63145271.199769740.1532242581.1532242581.1532242581.1; __utmc=63145271; __utmz=63145271.1532242581.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=63145271.5.8.1532242602601; STUDY_SESS="PyyWwUSOWvc4ZyVKAOffw5PwSz3ya2vFZnkBCOEqiOOEdUtKxS+imUvzes6CaLkUnglSezILxl5O2iBhc/0L7KFqyjsNn37i9uaLB5NujwTSqk1HiI3rKj7FgAj80b4q6a1DOOyu+AYX4hV4+I78tP/Qd+37+Ms5wswsF7ZDv17yxKi23BMA/0rclhqYQLpb8WQLi3xTJ45sq/acjsEWiA=="; STUDY_INFO="cakelinxs@outlook.com|11|1143031303|1532242617574',
    'DNT': '1',
    'Host': 'www.icourse163.org',
    'Referer': 'https://www.icourse163.org/passport/reg/icourseLogin.do',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}


pages = {
    "1333":5,"1324":5,
    "1341":7,"1351":3,
    "1357":4,"1364":4,
    "1371":5,"1379":4,
    "1386":2,"1391":2,
    "1396":2,"1401":2,
    "1406":3,"1412":4,
    "1419":7,"1429":4,
    "1436":3,"1442":2,
    "1447":6,"1456":6
}

class GetDetailLink:
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(headers)
        self.urls = []
        self.video_links = []
        self.driver = webdriver.Chrome()
        self.timout = 20
        self.wait = WebDriverWait(self.driver,self.timout)
        self.path = 'video_source_link.txt'
        self.url = "https://www.icourse163.org/learn/HIT-1002123007?tid=1002655021#/learn/content?{}"
        self.form_data = {
            "type":"detail",
            "sm":1,
            "id":""
        }
        


    def get_links(self):
        for key,data in pages.items():
            for i in range(data):
                id = "100377" + str(int(key) + i)
                self.form_data['id'] = id
                url = self.url.format(urlencode(self.form_data))
                if url not in self.urls:
                    self.urls.append(url)
        return self.urls



    def dumps_url_file(self,path):
        with open(path,'w') as file:
            file.write("\n".join(self.video_links))

    def extracted_video_urls(self):
        for url in self.urls:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"ux-video-player")))
            sleep(4)
            responsde = self.driver.page_source
            pattern = re.compile('<video(.*?)<source(.*?)src="(.*?)"')
            match_result = pattern.search(responsde)
            if match_result:
                match_result = match_result.group(3)
                if match_result not in self.video_links:
                    self.video_links.append(match_result)
                    print(match_result)

    def load_links_file(self):
        with open(self.path,'r') as file:
            try:
                video_source_urls = file.read().split("\n")
                return video_source_urls
            except Exception as e:
                print(e.args)
                print("read文件内容出错")
        

if __name__ == '__main__':
    obj = GetDetailLink()
    # obj.get_links()
    # obj.extracted_video_urls()
    # path = 'video_source_link.txt'
    # obj.dumps_url_file(path)
    print(obj.load_links_file())
    obj.driver.quit()