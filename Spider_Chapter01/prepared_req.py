# -*- coding:utf-8 -*-
from requests import Request,Session


def main():
    url = 'https://httpbin.org/post'
    data = {
        'name':'linxs'
    }
    header = {
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    
    # 先生成一个Request对象
    # 然后作为session.prepared_request的参数生成一个PreparedRequest
    # 最后调用session的send方法发起请求
    session = Session()
    req =  Request('POST',url=url,data=data,headers=header)
    prepared_req = session.prepare_request(req)
    res = session.send(prepared_req)
    print(res.text)
if __name__ == '__main__':
    main()