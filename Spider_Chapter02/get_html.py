# -*- coding:utf-8 -*-
import requests
import codecs




def get_res(url):
    respon = requests.get(url)
    with codecs.open('html/xx.html','w',encoding='utf-8') as file:
        file.write(respon.text)
    return respon


def main():
    url = 'https://github.com'
    response = get_res(url)
    return response


if __name__ == '__main__':
    main()
    