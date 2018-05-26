#  -*- coding:utf-8 -*-


import requests

def main():
    api_url = "http://{}:{}@{}:{}"
    host = "http-dyn.abuyun.com"
    port = "9020"
    user = "H36E5BU7Z7S947YD"
    pass_ = "601B13BF18C7D672"
    proxies = {'http':api_url.format(user,pass_,host,port)}
    response = requests.get("http://weixin.sogou.com/",proxies=proxies)
    print(response.status_code)
    

if __name__ == '__main__':
    while True:
        main()