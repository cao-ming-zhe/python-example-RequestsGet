# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import re
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_doupo(url, f):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36'}
    res = requests.get(url, headers)
    if res.status_code == 200:
        contexts = re.findall('<p>(.*?)</p>', res.content.decode('utf-8'), re.S)
        for context in contexts:
            f.write(context + '\n')
    else:
        pass


def get_top_baidu():
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36'}
    try:
        res = requests.get("https://top.baidu.com/board?tab=teleplay", headers)
        soup = BeautifulSoup(res.text, 'lxml')
        styles = soup.select('div.content_1YWBm > div:nth-child(2)')
        actors = soup.select('div.content_1YWBm > div:nth-child(3)')
        contexts = soup.select('div.content_1YWBm > div.c-single-text-ellipsis.desc_3CTjT')
        for style, actor, context in zip(styles, actors, contexts):
            data = {
                '类型': style.get_text().split('：')[1],
                '演员': actor.get_text().split('：')[1],
                '简介': context.get_text().strip()
            }
            print(data)
    except ConnectionError:
        print("拒绝访问")


def get_qiusibaike():
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36'}
    try:
        res = requests.get("https://www.qiushibaike.com/text/", headers)
        selector = etree.HTML(res.text)
        # infos = selector.xpath('/html/body/div[1]/div/div[2]/div')
        # for info in infos:
        #     print(info.xpath('div[1]/a[2]/h2/text()')[0].strip())

        contexts = selector.xpath('//div[starts-with(@class,"article block untagged mb15")]/text()')
        for context in contexts:
            print(context)
    except ConnectionError:
        print("拒绝访问")


def get_playabc(url, f):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36',
        'cookie': 'JSESSIONID=0E4E971C361D20C12C9724638CD90EFB',
        'token': 'aee28e07e7dccec313312a266b958b9c_1639357733377'}

    try:
        res = requests.get(url, headers=headers)
        data = json.loads(res.text)
        for context in data.get("data"):
            parentName = context.get("parentName")
            phone = context.get("phone")
            adviser = ''
            name = ''
            birthday = ''
            if context.get("childs") is not None:
                if context.get("childs")[0].get("name") is not None:
                    name = context.get("childs")[0].get("name")
                if context.get("childs")[0].get("birthday") is not None:
                    birthday = context.get("childs")[0].get("birthday")

            if context.get("parentName") is not None:
                parentName = context.get("parentName")

            if context.get("phone") is not None:
                adviser = context.get("phone")

            if context.get("adviser") is not None:
                if context.get("adviser").get("name") is not None:
                    adviser = context.get("adviser").get("name")

            context = name + "," + birthday + "," + parentName + "," + phone + "," + adviser + '\n'
            context.replace(u'\xa0', u'')
            try:
                f.write(context)
            except Exception as ex:
                print(ex)

    except ConnectionError:
        print("拒绝访问")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    # get_top_baidu()

    file = open('C:/Users/MC010/Desktop/test.csv', 'a+')
    file.write("name,birthday,parentName,phone,adviser" + '\n')
    urls = [
        'http://jz.gymchina.com/franchise/market/getCaseList.json?start={}&size=20&uid=vaw5vb4t1kl2i62i&brandId=playabc&schoolId=qi44wa3juet25xps&t=1639105673360'.format(
            str(
                i * 20)) for i in range(0, 1702)]
    for url in urls:
        get_playabc(url, file)
        time.sleep(1)
    file.close()

    # get_qiusibaike()
    # file = open('C:/Users/MC010/Desktop/test.txt', 'a+')
    # urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(str(i)) for i in range(1, 20)]
    # for url in urls:
    #     get_doupo(url, file)
    #     time.sleep(1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
