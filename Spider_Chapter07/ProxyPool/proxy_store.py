# -*- coding:utf-8 -*-

from redis import StrictRedis
from random import choice
from config import *
from error import PoolEmptyError


class RedisClient(object):
    def __init__(self):
        '''
        decode_responses参数设置为true，写入的value值为str，否则为字节型
        '''
        self.db = StrictRedis(host=HOST,port=PORT,password=PASSWD,decode_responses=True)
        pass


    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
            
        else:
            result = self.db.zrevrange(REDIS_KEY,MIN_SCORE,MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    

    def add(self,proxy,score=INITIAL_SCORE):
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)
        
    

    def decrease(self,proxy):
        # 获取proxy对应的分数
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print("代理 {} , 分数 {} , 减1".format(proxy,score))
            return self.db.zincrby(REDIS_KEY,proxy,-1)
            
        else:
            print("代理 {} , 当前分数 {} , 移除".format(proxy,score))
            self.db.zrem(REDIS_KEY,proxy)
            
        
    

    def exists(self,proxy):
        return not self.db.zscore(REDIS_KEY,proxy) == None
        
    

    def max(self,proxy):
        print("代理 {} , 可用 ， 设置为{}".format(proxy,MAX_SCORE))
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)
        

    

    def count(self):
        return self.db.zcard(REDIS_KEY)
        
    

    def all(self):
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)
        
    