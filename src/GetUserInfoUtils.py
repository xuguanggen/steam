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





def get_level_experValue(url):
    bsObj = get_BeautifulSoup(url)
    badges_url = ""
    if bsObj.find('a',{'href': url+'/badges'}) == None:
        return ["NULL"] * 4
    else:
        badges_url = bsObj.find('a',{'href': url+'/badges'}).attrs['href']
    
    bsObj = get_BeautifulSoup(badges_url)
    level_span = bsObj.find('span',{'class':'friendPlayerLevelNum'})
    experience_span = bsObj.find('span',{'class':'profile_xp_block_xp'})
    remain_div = bsObj.find('div', {'class':'profile_xp_block_remaining'})

    level = "0" if level_span == None else level_span.text.strip()
    experience_value = "0" if experience_span == None else experience_span.text.strip().split(' ')[0].replace(',','')
    remain_info = "NULL" if remain_div == None else remain_div.text.strip()
    
    badget_infos = bsObj.findAll('div',{'class':'badge_info_description'})
    if badget_infos == None:
        return [ level, experience_value, remain_info, "NULL"]

    badget_info_list = []
    for badget in badget_infos:
        badget_name = badget.find('div',{'class':'badge_info_title'}).text.strip().replace(' ','').replace('^M','').replace('\t','')
        badget_value = badget.findAll('div')[1].text.strip().replace(' ','').replace('^M','').replace('\r','').replace('\n','').replace('\t','')
        badget_info = badget_name + ":" + badget_value
        badget_info_list.append(badget_info)
    
    badget_info_str = "|".join(badget_info_list)
    print(level)
    print(experience_value)
    print(remain_info)
    print(badget_info_str)
    return [ level, experience_value, remain_info, badget_info_str]


def get_usergames(url):
    game_url = url+"/games/?tab=all"
    bsObj = get_BeautifulSoup(game_url)
    game_js = bsObj.find('script', {'language':'javascript'})
    if game_js == None:
        return ""
    print("JS length:\t"+str(len(game_js)))
    if game_js.text == "":
        return ""
    gamelist_json = game_js.text.strip().split('\n')[0].split('=')[1].replace('\r','')[1:-1]
    src_data = json.loads(gamelist_json)
    #print(str((data[0])))
    game_list = []
    for game in src_data:
        appid = str(game['appid']) if "appid" in game.keys() else "NULL"
        name = str(game['name']) if "name" in game.keys() else "NULL"
        hours = str(game['hours']) if "hours" in game.keys() else "NULL"
        hours_forever = str(game['hours_forever']) if "hours_forever" in game.keys() else "NULL"
        #print('\t'.join([appid, name, hours, hours_forever]))
        this_game_info = ",".join([appid, name, hours, hours_forever])
        game_list.append(this_game_info)

    game_info = "|".join(game_list)
    print(game_info)
    return game_info



def get_usergroups(url):
    print("=========================获取每个用户所属的组============================================")
    group_url = url+"/groups/"
    bsObj = get_BeautifulSoup(group_url)
    if bsObj == None:
        return "NULL"
    groups_a = bsObj.findAll('a', {'class':'linkTitle'})
    if groups_a == None:
        return "NULL"

    group_list = []
    for group in groups_a:
        group_info = group.text.strip()+":"+group.attrs['href'].strip()
        group_list.append(group_info)
    
    groups_info = "|".join(group_list)
    #print(groups_info)
    return groups_info


def get_userfriends(url):
    print("=========================获取每个用户所有的朋友名字及其链接===============================")
    friend_url =  url+"/friends/"
    bsObj = get_BeautifulSoup(friend_url)
    if bsObj == None:
        return "NULL"

    friends_div = bsObj.findAll('div', {'class': re.compile("^friendBlock persona")})
    if friends_div == None:
        return "NULL"
    friend_list = []
    for friend in friends_div:
        friend_href = friend.find('a', {'class':'friendBlockLinkOverlay'}).attrs['href'].strip().replace('\n','')
        friend_name = friend.find('div',{'class':'friendBlockContent'}).text.strip().split('\r')[0].split('\n')[0]
        friend_info = friend_name+","+friend_href
        friend_list.append(friend_info)

    friends_info = "|".join(friend_list)
    print(friends_info)
    return friends_info

def Run(url):
    req = urllib.request.Request(url, headers = headers)
    response = urlopen(req).read()
    response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response)
    if bsObj.find('div', {'class':'profile_private_info'}) != None:
        print("保密")
        return  get_user_basicInfo + ["NULL"] * 7
    
    user_basicInfo = get_user_basicInfo(url)
    level_experValue = get_level_experValue(url)
    games_info  = get_usergames(url)
    groups_info = get_usergroups(url)
    friends_info = get_userfriends(url)
    
    all_infos = []
    all_infos += user_basicInfo
    all_infos += level_experValue
    all_infos.append(games_info)
    all_infos.append(groups_info)
    all_infos.append(friends_info)
    print('\n\nAll infos:\n')
    print((str(all_infos)))
    return all_infos


if __name__=='__main__':
    #get_user_basicInfo("http://steamcommunity.com/id/afarnsworth/")
    #get_level_experValue("http://steamcommunity.com/id/afarnsworth")
    #get_game_list("http://steamcommunity.com/id/afarnsworth")
    #get_userfriends("http://steamcommunity.com/id/afarnsworth")
    #Run("http://steamcommunity.com/id/afarnsworth")
    #Run("http://steamcommunity.com/id/76561198407744512")
    get_user_basicInfo("http://steamcommunity.com/id/76561198407744512")
    #get_game_list("http://steamcommunity.com/id/76561198407744512")
    #get_usergroups("http://steamcommunity.com/id/76561198407744512")
    #get_usergroups("http://steamcommunity.com/id/afarnsworth")
    #get_level_experValue("http://steamcommunity.com/id/76561198407744512")
    #get_userfriends("http://steamcommunity.com/id/76561198407744512")
    #run()
    #get_usergroups()
    #get_userfriends()
    print("Success....")
