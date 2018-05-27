# -*- coding:utf-8 -*-
import random
from redis import StrictRedis
from config import *

'''
RedisClient的作用是设置type:value的键值对，可以是用户名和密码的映射，也可以是与cockle的映射
然后存储到redis中
'''

class RedisClient(object):
    def __init__(self,type_,website):
        self.client = StrictRedis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASS)
        self.website = website
        self.type = type_

    def name(self):
        return "{type}:{website}".format(type=self.type,website=self.website)
        
    

    def set(self,username,value):
        return self.client.hset(self.name(),username,value)
        
    
    def delete(self,username):
        self.client.hdel(self.name(),username)
        
    

    def count(self):
        return self.client.hlen(self.name())
        
    
    def get(self,username):
        return self.client.hget(self.name(),username)
        
    


    def username(self):
        print(self.client.hkeys(self.name()))
        return self.client.hkeys(self.name())
        
    

    def all(self):
        return self.client.hgetall(self.name())
        
    

    def random(self):
        return random.choice(self.client.hvals(self.name()))
        
