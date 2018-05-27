# -*- coding:utf-8 -*-

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASS = None

BROWSER_TYPE = 'Chrome'
GENERATOR_MAP = {
    'weibo':'WeiboCookieGen'
}

TEST_MAP = {
    'weibo':'WeiboVerifyCookie'
}

TEST_URL_MAP = {
    'weibo':'https://m.weibo.cn/'
}

API_ADDRESS = 'localhost'
API_PORT = 5555

CYCLE = 120

GENERATOR_PROCESS = True
TEST_PROCESS = True
API_PROCESS = True