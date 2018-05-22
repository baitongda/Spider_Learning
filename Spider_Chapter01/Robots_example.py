# -* coding:utf-8 -*-
from urllib.robotparser import RobotFileParser

search_url = 'https://toutiao.io/subjects?utf8=%E2%9C%93&q=gfgf'
link = 'https://toutiao.io/posts/hot/7'
rp = RobotFileParser('https://toutiao.io/robots.txt')

# read包括读取和分析机器人协议
rp.read()
print(rp.can_fetch('*',r"https://toutiao.io"))
print(rp.can_fetch('*',link))
