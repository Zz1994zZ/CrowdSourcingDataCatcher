#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import random



# -------------------------------------------------------公用方法----------------------------------------------------
class CommanCalss:
    def __init__(self):
        self.header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        self.testurl="www.baidu.com"

    def getresponse(self,url):
        html = requests.get(url, headers=self.header).text
        return html

    def _is_alive(self,proxy):
        try:
            resp=0
            for i in range(3):
                req=requests.get(self.testurl, proxies=proxy)
                # 访问
                resp = req.status_code
            if resp == 200:
                return True
        except:
            return False



 # -------------------------------------------------------代理池----------------------------------------------------
class ProxyPool:
    def __init__(self,proxy_finder):
        self.pool=[]
        self.proxy_finder=proxy_finder
        self.cominstan=CommanCalss()

    def get_proxies(self):
        self.pool=self.proxy_finder.find()
        for p in self.pool:
            if self.cominstan._is_alive(p):
                continue
            else:
                self.pool.remove(p)

    def get_one_proxy(self):
        proxy_ip=random.choice(self.pool)
        proxies = {'http': proxy_ip}
        return proxies

    def writeToTxt(self,file_path):
        try:
            fp = open(file_path, "w+")
            for item in self.pool:
                fp.write(str(item) + "\n")
            fp.close()
        except IOError:
            print("fail to open file")


#-------------------------------------------------------获取代理方法----------------------------------------------------
#定义一个基类
class IProxyFinder:
    def __init__(self):
        self.pool = []

    def find(self):
        return

#西祠代理爬取
class XiciProxyFinder(IProxyFinder):
    def __init__(self, url):
        super(XiciProxyFinder,self).__init__()
        self.url=url
        self.cominstan = CommanCalss()

    def find(self):
        for i in range(1, 10):
            print(self.url + str(i))
            content = self.cominstan.getresponse(self.url + str(i))
            soup = BeautifulSoup(content)
            ips = soup.findAll('tr')
            for x in range(2, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                if tds == []:
                    continue
                ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
                self.pool.append(ip_temp)
        time.sleep(1)
        return  self.pool

#kuaidaili代理爬取
class KDLProxyFinder(IProxyFinder):
    def __init__(self, url):
        super(KDLProxyFinder,self).__init__()
        self.url=url
        self.cominstan = CommanCalss()

    def find(self):
        for i in range(1, 10):
            print(self.url + str(i))
            content = self.cominstan.getresponse(self.url + str(i))
            soup = BeautifulSoup(content)
            ips = soup.findAll('tr')
            for i in range(1, len(ips)):
                tds=ips[i].findAll('td')
                ip = tds[0].string
                port= tds[1].string
                ip_temp = ip + ":" + port
                self.pool.append(ip_temp)
            time.sleep(1)
        return  self.pool