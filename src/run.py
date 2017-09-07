
# -*- coding:utf-8 -*-


import os
import re
import subprocess
import json
import time

import urllib.request
import urllib.error
from urllib.request import urlopen
from urllib.error import HTTPError

from bs4 import BeautifulSoup

import requests
import sys
import re

type = sys.getfilesystemencoding()

headers = {
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
}

f_out = open('game_url_20170905.csv','a')

def get_gameurlList(url):
    req = urllib.request.Request(url, headers=headers)
    response = urlopen(req).read()
    # response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response, "lxml")
    gameurl_hrefs = bsObj.findAll('a',{'href':re.compile("^http://store.steampowered.com/app/")})[3:]

    url_set = set()
    for gameurl in gameurl_hrefs:
        gameurl = gameurl.attrs['href']
        if gameurl.find("//?") != -1:
            continue
        f_out.write(gameurl+'\n')
        # print(gameurl)
        url_set.add(gameurl)

    print(str(len(url_set)))
    # return bsObj



def get_BsFromHtml(htmlPath):
    html = open(htmlPath, 'r')
    htmlpage = html.read()
    bsObj = BeautifulSoup(htmlpage, 'lxml')
    return bsObj

if __name__ == '__main__':
    for pageIdx in range(1,1320):
        get_gameurlList('http://store.steampowered.com/search/?page='+str(pageIdx))
        print(str(pageIdx))
    print("Success....")
    f_out.close()
