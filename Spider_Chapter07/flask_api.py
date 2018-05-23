# -*- coding:utf-8 -*-

from proxy_store import RedisClient
from flask import Flask,g
__all__ = ['app']
app=Flask(__name__)



@app.route("/")
def index():
    return "<h2>Welcome to Proxy Pool System</h2>"
    



def get_conn():
    if not hasattr(g,"redis"):
        g.redis = RedisClient()
    return g.redis

@app.route('/count')
def get_count():
    conn = get_conn()
    return conn.count()
    


@app.route('/random')
def random():
    conn = get_conn()
    return conn.random()



if __name__ == '__main__':
    app.run()