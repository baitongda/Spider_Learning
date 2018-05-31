#-*- coding:utf-8 -*-



# MYSQL config
MYSQL_HOST="127.0.0.1"
MYSQL_PORT=3306
MYSQL_PASSWD="linxs"
MYSQL_USER="root"

MYSQL_DB="weixin"



# REDIS config

REDIS_HOST="127.0.0.1"
REDIS_PORT=6379
REDIS_KEYS="weixin"
REDIS_PASSWD=None


# 
VALID_CODE=[200]
MAX_FAIL_TIME=3



# 阿步云代理
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
proxyUser = "HT3G8Z28YV41BCID"
proxyPass = "E5F02CE0DC05F0E7"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
}

PROXIES = {
    "http"  : proxyMeta
}


# 搜狗允许爬取的最大页数
MAX_PAGE=100