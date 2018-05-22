# -*- coding:utf-8 -*-
import json
from flask import g,Flask
from Hash_opt import RedisClient
from config import *
__all__ = ['app']
app=Flask(__name__)




def get_conn():
    for map_ in GENERATOR_MAP:
        if not hasattr(g,map_):
            setattr(g,"{}_cookies".format(map_),eval("RedisClient({},'{}')".format("cookies",map_)))
            setattr(g,"{}_accounts".format(map_),eval("RedisClient({},'{}')".format("accounts",map_)))
    return g


@app.route("/")
def index():
    return "<h2>Welcome to Cookies Pool System</h2>"


@app.route("/<website>/count")
def count(website):
    g = get_conn()
    cookies_list = getattr(g,"{}_cookies".format(website))
    count_ = cookies_list.count()

    return json.dumps({"status":1,"count":count_})
    
    


@app.route("/<website>/add/<username>/<password>")
def add_attr(website,username,password):
    g = get_conn()
    getattr(g,"{}_accounts".format(website)).set(username,password)
    # 添加成功返回状态main()
    return {"status":1}



@app.route("/<website>/random")
def random(website):
    g = get_conn()
    cookies_list = getattr(g,"{}_cookies".format(website))
    return cookies_list.random()



def run():
    app.run()

if __name__ == '__main__':
    app.run(host="0.0.0.0")