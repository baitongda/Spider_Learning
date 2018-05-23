# -*- coding:utf-8 -*-

MAX_SCORE=100
MIN_SCORE=0
INITIAL_SCORE=10
HOST="127.0.0.1"
PORT=6379
PASSWD=None

REDIS_KEY="proxies"             # A sorted set datastructure to save proxies

PROXY_POOL_THRESHOLD = 10000


TEST_URL = ""
VAILD_STATUS_CODE = [200]
BATCH_SIZE=100