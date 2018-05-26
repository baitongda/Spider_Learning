# -*- coding:utf-8 -*-


# run ---- execute the task
# test_single_proxy ---- check the proxy
# init ---- inititate the proxy set

from config import *
from proxy_store import RedisClient
import aiohttp
import asyncio
from time import sleep
from aiohttp import ClientError,ClientConnectorError
import requests

class CheckUp(object):
    def __init__(self):
        self.db = RedisClient()
    


    def run(self):
        # get all proxies
        # get event loop
        # split proxies to serval part
        # pack a task list
        # call run to exec asynic

        print("Start test")
        try:
            proxies = self.db.all()
            loop = asyncio.get_event_loop()
            for i in range(0,len(proxies),BATCH_SIZE):
                tasks_proxies = proxies[i:i + BATCH_SIZE]
                tasks = [self.check_single_proxy(proxy) for proxy in tasks_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sleep(3)
        except Exception as e:
            _ = e
            print(e.args)
            print("CheckUp occurs Error")

    async def check_single_proxy(self,proxy):
        connection = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=connection) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy 
                print(real_proxy)
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15) as response:
                    print("Status Code {} ".format(response.status))
                    print("*****************************")
                    if response.status in VAILD_STATUS_CODE:
                        self.db.max(proxy)
                        print("Proxy can use")
                    else:
                        self.db.decrease(proxy)
                        print("Proxy requests faild")
            except (ClientError,AttributeError,TimeoutError,ClientConnectorError):
                self.db.decrease(proxy)
                print("Proxy doesnt work")
