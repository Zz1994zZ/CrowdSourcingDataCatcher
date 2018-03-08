#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import queue
from User import User
from Writer import Writer
import threading
import traceback
from bs4 import BeautifulSoup
from proxy import KDLProxyFinder, ProxyPool
from pybloom import BloomFilter

basePageURL = 'https://www.proginn.com/'
baseUserURL = 'https://www.proginn.com/wo/'
userQueue = queue.Queue()
writer = Writer()
working = 1
myFilter = BloomFilter(capacity=150000, error_rate=0.0000001)
finder = KDLProxyFinder("http://www.kuaidaili.com/free/inha/")
# finder = XiciProxyFinder("http://www.xicidaili.com/wn/")
ppool_instance = ProxyPool(finder)
ppool_instance.get_proxies()


# headers = {
#     'Cookie': 'UM_distinctid=15f80e3cfdd43-08fecc7b7f450d-8383667-100200-15f80e3cfde45c; client_id=5a3bb7e3dc6b2; x_access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI4ODI2OCIsImN0aW1lIjoxNTEzODYzMTkwLCJleHAiOjE1MTY0NTUxOTB9.AkbrWfEjN82MoOZKZC1QJ_Dif4y0ySPxKaZDWGPiDcw; 48421=48421; XSRF-TOKEN=eyJpdiI6ImpJSXRlU3VMSnNzT3puZHlVdWdCWGc9PSIsInZhbHVlIjoiU1lJV0dWdEVqcHduMjlFMkZIOVBXSXc0VjlHNmcwMjF3QjRRZ1dKRVNrbkNOXC9mMWZwblQyTExvZzlPXC9kWkM4cXBZRjFpTVJjaU9YaTJJa1QzNlV1QT09IiwibWFjIjoiZGI5MGY3YWE1MmJhZmJlZmRmMjdiYTA5YjM2MDI3NzliY2M4ZmY3MDE3MjQyODQ0NzU0ODEyZGZlZGMxMGNiNSJ9; laravel_session=eyJpdiI6IjlvY0Iya3dnSDZ2ZDJoUktORlhZM1E9PSIsInZhbHVlIjoia1BoYlQwejJ4QVFNTXgxaE5mS05qRjR5TzIzZUVkQURkNDd5dU5GcjVvVTFvYWdLXC8wR1dLNUxCNXBwMUJqeE80ZFExRURqUDU4K05BOTVickJsOHZBPT0iLCJtYWMiOiIyNjNhMjhkYmQzMzdkNTU4NGRjMjE5YmU1NGQ0ZWZkNWE2YTNlNTEyN2E2YmM4M2ZhZjJjYTdhNmQ2ZWFiOTllIn0%3D; fed34112b737c4245348174f9344d1d3b8814ad4=eyJpdiI6IkU1R2piV1lVeWJFaWZhTXlsdTk4UEE9PSIsInZhbHVlIjoicEQyMnd0UnQ4TkpMZlEwYTNDbVlNWENteWVyajVBYzI3dnFtME5ud3pBK1JyVGxpVUxSTUtlcGJ6SzJQVGlWQnlpczB4VXZCTW45VFZpd1F1ZU5MNHZBYUFzdUFGeGE0VExGc3ExQmRKcHBicGU0Vlh5bXIram5XaGdVMUMrOWxxaWkzRFVldEFWdmlMK01LSlZJa1VqYU82MkplRndcL2creEdjaEZoY1ltbVlLTzFwQloyVGFFZjdFWFN6M3VISGNUKzdwXC9mbzJzVGxQQk44dzBDcTNkSis2T2FJZnhcL25mUlBPVHZhRHBXeFpOaFwvSTFiSlZiUEhIVDdSTjZ5bGwxSUpwZmpweklEekZQZkdGSzNZdVFwaUtMV2RYOEdzMlZHMHNpNUZvXC94R1pGNFRqMHozYkdNaFlMMWJkT2ZaVG9waGF2ZjNwUnpBbDFLc3BFMDIwVWVxWmRNSGZCM2ZnZWhRTnlcL3hueUJBV3FWWkVVa3g0SkNzRXRoTnFvYVpkNWtpQnR6RGI1Q1RJUVR0T0dJbTFSUCtXTVNlTjFTUzJrWElyQlBZeE1KRW94R1dybGJzSTl1WVwvZlNydE9lenpERjUxNGJsM0pCaE5wSDNpVXNoNlNtSkJaSmtcL1NwanVFdFdrQmtxd0diUT0iLCJtYWMiOiJhOWIxZjEzOGE4YmI0MjM1Mzc3ODYzYzkxYzViMTIyYjUxZmVkZWExMjkwYzQxN2VjODg1ZmUyY2U0ZmM0MWI3In0%3D; CNZZDATA1261469621=1194602006-1509690624-%7C1513924663; Hm_lvt_c92adf6182a39eb23c24cf43abc3f439=1512022434,1513863024; Hm_lpvt_c92adf6182a39eb23c24cf43abc3f439=1513925804',
#     'Referer': 'https://www.proginn.com/wo/60153'
# }
def handleHTML(html, user):
    try:
        soup = BeautifulSoup(html)
        tag = soup.find(class_='nickname')
        user.nickname = tag.a.string
        # tag = soup.find(class_='introduction')
        # if(len(tag.contents)==3):
        #     user.city = "未知"
        #     user.work = tag.contents[2]
        # else:
        #     user.city = tag.contents[2]
        #     user.work = tag.contents[4]
        # tag = soup.find(class_='hire-info')
        # tags = tag.find_all('p')
        # user.price=tags[0].span.string
        # user.workPlace=tags[1].string
        # user.workTime=tags[2].string
        skills = soup.find_all(class_='skill')
        skillList = {}
        for skill in skills:
            name = skill.find(class_='name').string
            level = skill.find(class_='progress').div['class']
            skillList[name] = level
        user.skillList = skillList
        writer.save(user)
        # writer.updateSkills(user)

    except:
        print(id, '出错')
        traceback.print_exc()


def writeData():
    while (not userQueue.empty()) or working == 1:
            user = userQueue.get()
            req = requests.get(baseUserURL + user.id, proxies=ppool_instance.get_one_proxy())
            html = req.text
            handleHTML(html, user)
def upData():
            user = userQueue.get()
            req = requests.get(baseUserURL + user.id, proxies=ppool_instance.get_one_proxy())
            html = req.text
            handleHTML(html, user)


def getURL():
    for i in range(0, 9300):
        URL = basePageURL + str(i) + '/?sort=1'
        req = requests.get(URL, proxies=ppool_instance.get_one_proxy())
        html = req.text
        soup = BeautifulSoup(html)
        pageUsers = soup.find_all(class_='item J_user')
        for userTag in pageUsers:
            user = User()
            try:
                user.id = userTag.find(class_='info')['userid']
                if user.id in myFilter:
                    continue
                workInfo = userTag.find(class_='work-time')
                user.workPlace = workInfo.div.contents[3].string
                user.workTime = workInfo.find_all('div')[1].contents[3].string
                user.price = userTag.find(class_='price').string
                myFilter.add(id)
                userQueue.put(user)
            except:
                print(user.id, '出错,page=', i)
                # traceback.print_exc()
                continue
    global working
    working = 0


def getHTML(URL):
    req = requests.get(URL, proxies=ppool_instance.get_one_proxy())
    html = req.text
    return html
def init():
    list = writer.getUserList()
    for id in list:
        myFilter.add(id[0])
if __name__ == '__main__':
    # 把已经爬好的id加到过滤器中
    init()
    t = threading.Thread(target=getURL)
    t.start()
    for i in range(1, 5):
        tReader = threading.Thread(target=writeData)
        tReader.setDaemon(True)
        tReader.start()
        # -------------------------------------------------------测试----------------------------------------------------
        # handleHTML(getHTML('https://www.proginn.com/wo/141649'),'1233')
        # print(ppool_instance.get_one_proxy())
