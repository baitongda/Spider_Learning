# -*- coding:utf-8 -*-


import aiohttp
import asyncio



async def main():
    connector = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get('https://www.sohu.com') as resp:
            print(resp.status)
            print(await resp.text())

loop = asyncio.get_event_loop()
tasks = [main(),main()]
loop.run_until_complete(asyncio.wait(tasks))
