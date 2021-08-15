# ！/usr/bin/python
# -*-coding:utf-8-*-
import sys
from time import sleep

import requests
import os
import re
from single_chapter import save_text

# 网站url
url = input('url:')  # 'https://www.esjzone.cc/detail/1543764680.html'
# 保存文件的路径
global_file_path = input('file_path:')  # 'D://novels/'

flag = 0
# -------分--隔--线--------
while flag == 0:
    try:
        # 发送http请求
        response = requests.get(url)
        # 编码方式
        response.encoding = 'utf-8'
        # 请求失败，重新请求
        requests_times = 0
        while len(response.text) < 100 | flag < 10:
            print(url + '请求失败,开始第 {} 次重新请求'.format(flag + 1))
            sleep(0.2)
            response = requests.get(url)
            requests_times = requests_times + 1

        # 目标小说主页的网站源码
        html = response.text
    except Exception as e:
        print(e)
        input('任意按键退出')
        sys.exit(0)

    # 获取小说标题
    try:
        novel_title = html.split("<h2")[1].split("</h2>")[0]
        novel_title = novel_title[28:]
        file_path = global_file_path + novel_title + '/'
    except:
        input('请求失败，任意按键退出')
        sys.exit(0)

    # 获取所有章节的url
    chapterList = html.split("chapterList")[1].split("tab-pane fade")[0]
    # print(chapterList)

    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
    chapter_url_list = re.findall(pattern, chapterList)
    formatList = []
    for url in chapter_url_list:
        # if url[:28] == 'https://www.esjzone.cc/forum' | url[:28] == 'https://esjzone.cc/forum':
        if re.search('esjzone.cc/forum', url) is not None:
            if url not in formatList:
                formatList.append(url)

    # 判断目录是否存在
    if not os.path.exists(file_path):
        # 目录不存在创建，makedirs可以创建多级目录
        os.makedirs(file_path)
    # 保存文件
    fail_url = []
    for index, url in enumerate(formatList):
        success_or_not = save_text(url, file_path, index + 1)
        if not success_or_not:
            fail_url.append(url)
        sleep(0.1)

    while fail_url:
        print('正在重新下载保存失败的链接')
        temp_url = []
        i = -1
        for url in fail_url:
            flag = save_text(url, file_path, i)
            i = i - 1
            if not flag:
                temp_url.append(url)
            sleep(0.1)
        fail_url = temp_url

    temp = input('\n\n输入新的url继续下载或enter键退出\n')
    if temp == '':
        print(temp)
        flag = 1
    else:
        url = temp

    # print(temp)
input('press any key to exit')
