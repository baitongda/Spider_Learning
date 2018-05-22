# -*- coding:utf-8 -*-
import requests





def dl_png(url):
    response = requests.get(url)
    with open('xx.png','wb') as img:
        img.write(response.content)



def main():
    url = 'https://p3.pstatp.com/origin/tuchong.fullscreen/14321588_tt'
    dl_png(url)

if __name__ == '__main__':
    main()