# -*- coding:utf-8 -*-

MAX_SCORE=100
MIN_SCORE=0
INITIAL_SCORE=10
# redis
HOST="127.0.0.1"
PORT=6379
PASSWD=None
REDIS_KEY="proxies"             # A sorted set datastructure to save proxies


PROXY_POOL_THRESHOLD = 10000
TEST_URL = "http://weixin.sogou.com/weixin?type=2&s_from=input&query=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98s"
VAILD_STATUS_CODE = [200]
BATCH_SIZE=100

# Flask API
API_HOST="127.0.0.1"
API_PORT=5000

#process switch
CHECKUP_PROCESS=True
GETTER_PROCESS=True
API_PROCSS=True

# cycle
CYCLE_CHECKUP=20
CYCLE_GETTER=20
