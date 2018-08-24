#  coding:utf-8 -*-
import requests
import re
import threading
from urllib.parse import urlparse
from get_detail_link import GetDetailLink
import aiohttp
import time
import asyncio


class Download:
    def __init__(self):
        self.store_dir = "{}.mp4"
        self.session = requests.session()
        self.getter = GetDetailLink()
        self.queue = []
        self.file_list = []

    def get_requests_queue(self):
        self.queue = self.getter.load_links_file()
    

    def get_filenames(self):
        filenames = self.getter.get_links()
        for l in range(len(filenames)):
            if filenames[l].split("id="):
                filenames[l] = filenames[l].split("id=")[2]
                if "&" in filenames[l]:
                    filenames[l] = filenames[l][:filenames[l].index("&")]
        self.file_list = filenames
        return filenames



async def fetch(session,url):
    async with session.get(url) as response:
        return await response.read()


async def write(name,html):
     with open(name,'wb') as f:
         f.write(html)
     print("write Success")

async def download(name,url):
    # print(f"download:{url}")
    async with aiohttp.ClientSession() as session:
        html = await fetch(session,url)
        name = r"/home/linxs/Videos/Complie/{}.mp4".format(name)
        await write(name,html)
        await session.close()



if __name__ == '__main__':
    start = time.time()
    d = Download()
    d.get_requests_queue()
    d.get_filenames()
    loop = asyncio.get_event_loop()
    for i in range(8):
        tasks = [download(d.file_list[k],d.queue[k]) for k in range(i*10,(i+1)*10)]
        tasks = [asyncio.ensure_future(task) for task in tasks]
        loop.run_until_complete(asyncio.wait(tasks))
    # tasks = [download(d.file_list[i],d.queue[i]) for i in range(10)]
    # tasks = [asyncio.ensure_future(task) for task in tasks]
    # loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print(f"Cos : {end-start}")
    
    