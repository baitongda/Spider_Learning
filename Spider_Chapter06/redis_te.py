import random
from redis import StrictRedis




class Redis_Client(object):
    def __init__(self,website="default",type="account"):
        self.website = website
        self.type = type
        self.client = StrictRedis(host="127.0.0.1",port=6379)
        pass
    

    def name(self):
        return "{type}:{name}".format(type=self.type,name=self.website)
        pass
    

    def set(self,username,value):
        return self.client.hset(self.name(),username,value)
        pass
    

    def get(self,username):
        return self.client.get(username)
        pass
    

    def all(self):
        return self.client.hgetall(self.name())
        pass
    

    def delete(self,username):
        return self.client.hdel(self.name(),username)
        pass
    
    def count(self):
        return self.client.hlen(self.name())
        pass
    

    def random(self):
        return random.choice(self.client.hvals(self.name()))
        pass
    

    def usernames(self):
        return self.client.hkeys(self.name())
