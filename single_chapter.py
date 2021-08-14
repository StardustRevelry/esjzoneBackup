# ！/usr/bin/python
# -*-coding:utf-8-*-
import requests
import os
import re

# 网站url
url = 'https://www.esjzone.cc/forum/1543764573/26517.html'
# 保存文件的路径
file_path = 'D:/novels/'


# -------分--隔--线--------
# 函数定义
def requests_when_failed(this_url):
    NETWORK_STATUS = True  # 判断状态变量
    try:
        response = requests.post(this_url, timeout=5)
        if response.text != 'Connect failed: Too many connections':
            if response.status_code == 200:
                return response
    except requests.exceptions.Timeout:
        NETWORK_STATUS = False  # 请求超时改变状态

        if not NETWORK_STATUS:
            '''请求超时'''
            for i in range(1, 10):
                print('请求超时，第%s次重复请求')
                response = requests.post(this_url, timeout=5)
                if response.status_code == 200:
                    return response
    return -1


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


def save_text(url, file_path):
    # 发送http请求
    response = requests.get(url)
    # 编码方式
    response.encoding = 'utf-8'
    # 目标小说主页的网站源码
    html = response.text

    # 获取标题
    try:
        title = html.split("<h2>")[1].split("</h2>")[0]
    except:
        # 请求失败，重新请求
        response = requests_when_failed(url)
        if response == -1:
            print(url + "--请求失败")
            return
        response.encoding = 'utf-8'
        html = response.text
        title = html.split("<h2>")[1].split("</h2>")[0]

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
    except Exception as e:
        print('保存失败:{}'.format(e))


# 判断目录是否存在
if not os.path.exists(file_path):
    # 目录不存在创建，makedirs可以创建多级目录
    os.makedirs(file_path)
# 保存文件
# save_text(url, file_path)
