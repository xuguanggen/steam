#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import os
import re

import urllib.request
from urllib.request import urlopen

from bs4 import BeautifulSoup


from config import *
import sys
type = sys.getfilesystemencoding()



headers = {
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        "Proxy-Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    }


def get_BeautifulSoup(url):
    req = urllib.request.Request(url, headers = headers)
    response = urlopen(req).read()
    #response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response,"lxml")
    return bsObj


def IsHaveAllInfo(url):
    bsObj = get_BeautifulSoup(url)
    if bsObj.find('div', {'class':'profile_private_info'}) != None:
        return 0

    if bsObj.find('a',{'href': url+'/badges/'}) != None and bsObj.find('a',{'href': url+'/games/?tab=all'}) != None and bsObj.find('a',{'href': url+'/groups/'}) != None and bsObj.find('a',{'href': url+'/friends/'}) != None:
        return 1
    else:
        return 0
    return 0

if __name__=='__main__':
    url=sys.argv[1]
    url_head='http://steamcommunity.com/'
    url = url_head + url
    value = IsHaveAllInfo(url)
    if value == 1:
        sys.exit(1)
    else:
        sys.exit(0)
    sys.exit(0)
