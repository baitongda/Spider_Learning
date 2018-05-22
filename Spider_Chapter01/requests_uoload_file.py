# -*- coding:utf-8 -*-

import requests


file = {'file':open(r'/home/linxs/image.png','rb')}
respon = requests.post('https://httpbin.org/post',data=file)
print(respon.text)
