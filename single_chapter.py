# ！/usr/bin/python
# -*-coding:utf-8-*-
from time import sleep

import requests
import os
import re

# # 网站url
# url = 'https://www.esjzone.cc/forum/1543764680/21073.html'
# # 保存文件的路径
# file_path = 'D:/novels/'

# -------分--隔--线--------
# 函数定义
def filter_tags(htmlstr):
    s = re.sub(r'</?\w+[^>]*>', '', htmlstr)
    s = replaceCharEntity(s)  # 替换实体
    return s


def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': '', '160': '',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"''"', '34': '"'}
    re_charEntity = re.compile(r'&#?(?P<name>\w+);')  # 命名组,把 匹配字段中\w+的部分命名为name,可以用group函数获取
    sz = re_charEntity.search(htmlstr)
    while sz:
        # entity=sz.group()
        key = sz.group('name')  # 命名组的获取
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)  # 1表示替换第一个匹配
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def save_text(url, file_path,number):
    # 发送http请求
    response = requests.get(url)
    # 编码方式
    response.encoding = 'utf-8'
    # 请求失败，重新请求
    flag = 0
    while len(response.text) < 100 | flag < 10:
        print(url + '请求失败,开始第 {} 次重新请求'.format(flag + 1))
        sleep(0.2)
        response = requests.get(url)
        flag = flag + 1
    # 目标小说主页的网站源码
    html = response.text

    # 获取标题
    try:
        title = html.split("<h2>")[1].split("</h2>")[0]
    except:
        # 请求失败，重新请求
        print(url + '请求失败')
        return False

    # 获取正文
    text_with_html_format = html.split("forum-content mt-3")[1].split("single-post-meta m-t-20 file-text")[0]
    text_with_html_format = text_with_html_format[9:-12]

    # 正则过滤html标签
    text = filter_tags(text_with_html_format)

    # 保存txt文档
    try:
        # 保存数据到文件
        with open(file_path + title + '.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print(title + ' 保存成功!')
        return True
    except Exception as e:
        print('保存失败:{}'.format(e))
        try:
            text = title + '\n\n' + text
            with open(file_path + str(number) + '.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            print(title+'   已重新保存到:\n' + str(number) + '.txt')
            return True
        except:
            print('重新保存失败')
            return False


# # 判断目录是否存在
# if not os.path.exists(file_path):
#     # 目录不存在创建，makedirs可以创建多级目录
#     os.makedirs(file_path)
# # 保存文件
# save_text(url, file_path)
