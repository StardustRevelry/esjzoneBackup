# ！/usr/bin/python
# -*-coding:utf-8-*-
from asyncio import sleep

import requests
import os
import re
from single_chapter import save_text

# 网站url
url = ''
# 保存文件的路径
file_path = ''

# -------分--隔--线--------
# 发送http请求
response = requests.get(url)
# 编码方式
response.encoding = 'utf-8'
# 目标小说主页的网站源码
html = response.text
# print(html)
# 获取小说标题
novel_title = html.split("<h2")[1].split("</h2>")[0]
novel_title = novel_title[29:]
file_path = file_path+novel_title+'/'

# 获取所有章节的url
chapterList = html.split("chapterList")[1].split("tab-pane fade")[0]
# print(chapterList)

pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    # 匹配模式
chapter_url_list = re.findall(pattern, chapterList)
formatList = []
for url in chapter_url_list:
    if url[:22] == 'https://www.esjzone.cc':
        if url not in formatList:
            formatList.append(url)

# 判断目录是否存在
if not os.path.exists(file_path):
    # 目录不存在创建，makedirs可以创建多级目录
    os.makedirs(file_path)
# 保存文件
for url in formatList:
    save_text(url, file_path)
    sleep(500)

