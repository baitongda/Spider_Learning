# -*- coding:utf-8 -*-
from requests import Request




class WeixinReq(Request):
    def __init__(self,url,callback,headers=None,timeout=15,method='get',need_proxy=False,fail_time=0):
        Request.__init__(self,method=method,url=url,headers=headers)
        self.timeout = timeout
        self.fail_time = fail_time
        self.need_proxy = need_proxy
        self.callback = callback




