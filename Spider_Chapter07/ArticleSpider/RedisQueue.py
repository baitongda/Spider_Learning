# -*- coding:utf-8 -*-

from config import *
from redis import StrictRedis
from pickle import * 
from WeixinRequest import WeixinReq
class RedisQueue():
    # redis storge string ,before return you should r-pickle to a Request object
    # to storge Request object to redis ,you shoule pickle it to string not a other object
    # this queue adapt first in first out.
    # add request to the last of redis
    # get request from the head of redis


    def __init__(self):
        self.db = StrictRedis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWD,decode_responses=False)
    
    def pop(self):
        
        try:
            if self.db.llen(REDIS_KEYS):
                return loads(self.db.lpop(REDIS_KEYS))
            else:
                return False
        except Exception as e:
            _ = e
            print(e)
            return False


    def add(self,request):
        if isinstance(request,WeixinReq):
            # judge it whether WeixinReq object ,only this type can return add to redis    
            return self.db.rpush(REDIS_KEYS,dumps(request))
        else:
            return False
    

    def empty(self):
        return self.db.llen(REDIS_KEYS) == 0





if __name__ == '__main__':
    pass