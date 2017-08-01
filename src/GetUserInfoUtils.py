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




####从一个成员组的某一个页面中获取当前页面中成员的信息链接
def fetch_urls_from_single_page(htmlpage_path, f_out):
    html = open(htmlpage_path , "r")
    htmlpage = html.read()
    bsObj = BeautifulSoup(htmlpage)
    user_hrefs_id = bsObj.findAll('a',{'href':re.compile("^http://steamcommunity.com/id/")})
    user_hrefs_profile = bsObj.findAll('a',{'href':re.compile("^http://steamcommunity.com/profiles/")})

    user_url_set = set()
    for user_href in user_hrefs_id:
        user_url = user_href.attrs['href']
        user_url_set.add("id/"+user_url.strip().split('/')[-1])

    for user_href in user_hrefs_profile:
        user_url = user_href.attrs['href']
        user_url_set.add("profiles/"+user_url.strip().split('/')[-1])

    for user_url in user_url_set:
        f_out.write(user_url+'\n')
    #print(str(len(user_url_set)))
    subprocess.run("rm "+htmlpage_path, shell=True, check=True)
    return user_url_set


#### get each discussion content
def fetch_discussion_user():
    f_discussion_in = open(DISCUSSION_INFO_PATH,'r')
    
    for group_info in f_discussion_in.readlines():
        if group_info.find('/app/') != -1:
            continue
        group_info = group_info.strip().split('\t')
        
        group_name = group_info[0]
        member_url = group_info[1].replace("/discussions/","#members")
        

        print(member_url)
        response = urlopen(member_url)
        bsObj = BeautifulSoup(response)
        num_members = 0
        if bsObj.find('span',{'class':'count oversized'}) == None:
            num_members = int((bsObj.find('a',{'href':member_url}).find('span',{'class':'count'}).text.strip().replace(',','')))
        else:
            num_members = int(bsObj.find('span',{'class':'count oversized'}).text.replace(',','').strip())
        num_pages = int((num_members / NUM_MEMBERS_PER_PAGE) + 1) if num_members % NUM_MEMBERS_PER_PAGE != 0 else int(num_members / NUM_MEMBERS_PER_PAGE)
        print(str(num_members)+':'+str(num_pages))

        group_dir = "../data/"+group_name.replace(" ","")
        if not os.path.exists(group_dir):
            os.makedirs(group_dir)

        user_file = group_dir + "/user_url.txt"
        f_out = open(user_file,'a')

        user_url_set = set()
        for pageIdx in range(1, num_pages+1):
            page_url = member_url + "/?p="+str(pageIdx)+"&content_only=true"
            page_url = page_url.replace('#','/')
            pageIdx_html = group_dir + "/" + str(pageIdx) + ".html"
            subprocess.run("node getPagehtml.js '"+page_url+"' "+pageIdx_html, shell=True, check=True)
            user_url_set = user_url_set.union(fetch_urls_from_single_page(pageIdx_html,f_out))
            print(group_name+":\t"+str(pageIdx))
            #print("total "+str(pageIdx)+":\t"+str(len(user_url_set)))
        print(group_name+":\t"+str(len(user_url_set)))
        f_out.close()
    f_discussion_in.close()


def run():
    #url = 'http://www.steamcommunity.com/discussions/'
    #fetch_discussion(url)

    #fetch_discussion_user()
    headers = {
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Proxy-Connection":"keep-alive"
            }
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
    headers = {
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Proxy-Connection":"keep-alive"
            }
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
    headers = {
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
            "Proxy-Connection":"keep-alive"
            }
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


if __name__=='__main__':
    run()
    #get_usergroups()
    #get_userfriends()
    print("Success....")
