#! /usr/bin/env python
#coding=utf-8

############ 根据用户的url链接获取其信息 ###############################################
#1 用户名
#2 个人签名
#3 主页链接
#4 级别
#5 徽章的数量（徽章的名称,徽章的等级）
#6 游戏的数量 （游戏的名称，游戏时长）
#7 参加组的数量
#8 好友数量 （好友名称，好友链接）


import os
import re
import subprocess
import json

import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup

from prettytable import PrettyTable

from config import *
import requests
import sys
type = sys.getfilesystemencoding()



headers = {
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        "Proxy-Connection":"keep-alive"
}

def get_BeautifulSoup(url):
    req = urllib.request.Request(url, headers = headers)
    response = urlopen(req).read()
    response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response)
    return bsObj



def get_user_basicInfo(url):
    bsObj = get_BeautifulSoup(url)
    title = bsObj.find('title').text.strip().split('::')[1].replace(' ','')
    desc_meta = bsObj.find('meta', {'name':'Description'})
    desc = "NULL" if desc_meta == None else desc_meta.attrs['content']
    return [title, desc]


def run():

    #fetch_discussion_user()
    url = "http://www.steamcommunity.com/id/afarnsworth"
    req = urllib.request.Request(url, headers=headers)
    #req = urllib.request.Request(url)
    #response = urlopen("http://steamcommunity.com/id/afarnsworth",headers)
    response = urlopen(req)
    bsObj = BeautifulSoup(response)
    user_name = bsObj.find('title').text.strip()
    print(user_name)
    badges_url = bsObj.find('a',{'href':'http://steamcommunity.com/id/afarnsworth/badges'})
    print(badges_url.attrs['href'])
    #req = urllib.request.Request(badges_url.attrs['href'])
    req = urllib.request.Request(badges_url.attrs['href'],headers=headers)
    response = urlopen(req).read()
    response = response.decode("UTF-8").encode(type)
    bsObj = BeautifulSoup(response)
    level = bsObj.find('span',{'class':'friendPlayerLevelNum'}).text.strip()
    jingyan_value = bsObj.find('span',{'class':'profile_xp_block_xp'}).text.strip()
    print(str(level))
    print(str(jingyan_value))
    badget_infos = bsObj.findAll('div',{'class':'badge_info_description'})
    idx = 0
    for xx in badget_infos:
        title = xx.find('div',{'class':'badge_info_title'}).text.strip().replace(' ','').replace('^M','').replace('\t','')
        jingyan_value = xx.findAll('div')[1].text.strip().replace(' ','').replace('^M','').replace('\r','').replace('\n','').replace('\t','')
        print(str(idx)+":\t"+title+":\t"+jingyan_value)
        idx += 1
    print('========================================================================')
    game_url = "http://steamcommunity.com/id/afarnsworth/games/?tab=all"
    req = urllib.request.Request(game_url, headers=headers)
    response = urlopen(req).read()
    response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response)
    game_js = bsObj.find('script', {'language':'javascript'})
    print("JS length:\t"+str(len(game_js)))
    gamelist_json = game_js.text.strip().split('\n')[0].split('=')[1].replace('\r','')[1:-1]
    data = json.loads(gamelist_json)
    #print(str((data[0])))
    for x in data:
        appid = str(x['appid']) if "appid" in x.keys() else "NULL"
        name = str(x['name']) if "name" in x.keys() else "NULL"
        hours = str(x['hours']) if "hours" in x.keys() else "NULL"
        hours_forever = str(x['hours_forever']) if "hours_forever" in x.keys() else "NULL"
        print('\t'.join([appid, name, hours, hours_forever]))



def get_usergroups():
    print("=========================获取每个用户所属的组============================================")
    group_url = "http://steamcommunity.com/id/afarnsworth/groups/"
    req = urllib.request.Request(group_url, headers=headers)
    response = urlopen(req).read()
    response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response)

    groups_a = bsObj.findAll('a', {'class':'linkTitle'})
    for x in groups_a:
        print(x.text.strip()+"\t"+x.attrs['href'].strip())


def get_userfriends():
    print("=========================获取每个用户所有的朋友名字及其链接===============================")
    friend_url =  "http://steamcommunity.com/id/afarnsworth/friends/"
    req = urllib.request.Request(friend_url, headers=headers)
    response = urlopen(req).read()
    response = response.decode("UTF-8").encode(type)
    bsObj = BeautifulSoup(response)

    #friends_div = bsObj.find('div', {'id':'memberList'})
    friends_div = bsObj.findAll('div', {'class': re.compile("^friendBlock persona")})
    print(str(len(friends_div)))
    idx = 0
    for friend in friends_div:
        friend_href = friend.find('a', {'class':'friendBlockLinkOverlay'}).attrs['href'].strip().replace('\n','')
        friend_name = friend.find('div',{'class':'friendBlockContent'}).text.strip().split('\r')[0].split('\n')[0]
        print(str(idx)+"\t"+friend_name+"\t"+friend_href)
        idx += 1


def Run(url):
    req = urllib.request.Request(url, headers = headers)
    response = urlopen(req).read()
    response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response)
    if bsObj.find('div', {'class':'profile_private_info'}) != None:
        print("保密")




if __name__=='__main__':
    get_user_basicInfo("http://steamcommunity.com/id/afarnsworth/")
    #run()
    #get_usergroups()
    #get_userfriends()
    print("Success....")
