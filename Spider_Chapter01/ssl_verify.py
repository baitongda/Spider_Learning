# -*- coding:utf-8 -*-
import requests


def main():
    try:
        res = requests.get('https://www.12306.cn')
    except requests.exceptions.SSLError as e:
        print('SSL Error')
    res = requests.get('https://www.12306.cn',verify=False)
    print(res.status_code)
    try:
        res = requests.get('https://baidu.om',timeout=1)
    except requests.exceptions.Timeout as e:
        print('Timeout Error')
    except requests.exceptions.ConnectionError as e:
        print('Connection Failed')
if __name__ == '__main__':
    main()