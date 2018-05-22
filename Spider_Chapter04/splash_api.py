# -*- coding:utf-8 -*-

import requests
from pprint import pprint
from urllib.request import quote

def render_png(url):
    response = requests.get(url)
    with open('render.png','wb') as img:
        img.write(response.content)


def render_har(url):
    respinse = requests.get(url)
    pprint(respinse.text)


def execute_(lua_script):
    url = "http://localhost:8050/execute?lua_source={}".format(quote(lua_script))
    response = requests.get(url)
    print(response.text)

def main():
    lua = '''
        function main(splash,args)
            local treat = require("treat")
            local response = splash:http_get("http://httpbin.org/get")
            return {
                html=treat.as_string(response.body),
                status=response.status,
                url=response.url
            }
        end
    '''
    execute_(lua)

if __name__ == '__main__':
    main()