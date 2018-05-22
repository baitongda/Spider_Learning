# -*- coding:utf-8 -*-
from urllib.parse import urlparse,urlsplit,urlunparse,\
        urlunsplit,urljoin,urlencode,parse_qs,parse_qsl,\
        quote,unquote




def link_process():
    link = 'http://www.baidu.com'
    url = 'www.baidu.com'
    data_ = ['https','www.baidu.com','index.html','user','id=123','frangment']
    data = ['https','www.baidu.com','index.html;user','id=123','frangment']
    print(urlparse(link,scheme='https'))
    print(urlparse(url,scheme='https'))
    print(urlsplit(link,scheme='https'))
    print(urlsplit(url,scheme='https'))
    print(urlunparse(data_))
    print(urlunsplit(data))
    print(urljoin('https://ww.baidu.com','index.html'))
    print(urljoin('https://www.baidu.com','http://lincoding.club/index.html'))


    pass


def link_parm_process():
    url = 'https://www.baidu.com/index.html?x=1&y=2'
    parms = urlsplit(url).query
    print(parms)
    print(urlencode({'x':1,'y':2}))

    print('************************')

    # 反序列化


    # 字典形式

    print('Dict : {}'.format(parse_qs(parms)))


    # 列表格式
    print('List : {}'.format(parse_qsl(parms)))


def link_chinese_code_process():
    # 将URL中的的中文转换成URL编码
    url = 'https://www.baidu.com/index.html?query={}'
    result = quote(url.format('中文'))
    print(result)
    result = unquote(result)
    print(result)
    pass




def main():
    #link_process()
    #link_parm_process()
    link_chinese_code_process()

if __name__ == '__main__':
    main()