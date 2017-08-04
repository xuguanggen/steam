#! /usr/bin/env python3
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

from prettytable import PrettyTable

from config import *
import requests
import sys
type = sys.getfilesystemencoding()



headers = {
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        "Proxy-Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    }

#headers = {
#        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
#        "Proxy-Connection":"keep-alive",
#        "User-Agent": "super happy flair bot by /u/spladug"
#    }
def get_BeautifulSoup(url):
    req = urllib.request.Request(url, headers = headers)
    response = urlopen(req).read()
    #response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response,"lxml")
    return bsObj


def get_BsFromHtml(htmlPath):
    html = open(htmlPath, 'r')
    htmlpage = html.read()
    bsObj = BeautifulSoup(htmlpage, 'lxml')
    return bsObj



#############################################################################

def get_user_basicInfo_page(url):
    bsObj = get_BeautifulSoup(url)
    title = bsObj.find('title').text.strip().split('::')[1].replace(' ','')
    desc_meta = bsObj.find('meta', {'name':'Description'})
    desc = "NULL" if desc_meta == None else desc_meta.attrs['content']
    print(title)
    return [title, desc]

def get_userbadges_page(htmlPath, url):
    bsObj = get_BsFromHtml(htmlPath)
    
    level_span = bsObj.find('span',{'class':'friendPlayerLevelNum'})
    experience_span = bsObj.find('span',{'class':'profile_xp_block_xp'})
    remain_div = bsObj.find('div', {'class':'profile_xp_block_remaining'})

    level = "NULL" if level_span == None else level_span.text.strip()
    experience_value = "NULL" if experience_span == None else experience_span.text.strip().split(' ')[1].replace(',','')
    
    next_level = "NULL"
    remain_exper_value = "NULL"
    if remain_div != None:
        next_level = remain_div.text.strip().split(' ')[-1].replace(',','')
        remain_exper_value = remain_div.text.strip().split(' ')[0].replace(',','')


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
    return [ level, experience_value, next_level, remain_exper_value, badget_info_str]

def get_usergroups_page(htmlPath):
    #print("=========================get users groups============================================")
    bsObj = get_BsFromHtml(htmlPath)
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


def get_usergames_page(htmlPath):
    bsObj = get_BsFromHtml(htmlPath)
    game_js = bsObj.find('script', {'language':'javascript'})
    if game_js == None:
        return ""
    #print("JS length:\t"+str(len(game_js)))
    if game_js.text == "":
        return ""
    gamelist_json = game_js.text.strip().split('\n')[0].split('=')[1].replace('\r','')[1:-1]
    src_data = json.loads(gamelist_json)
    #print(str((data[0])))
    game_list = []
    for game in src_data:
        appid = str(game['appid']) if "appid" in game.keys() else "NULL"
        name = str(game['name']) if "name" in game.keys() else "NULL"
        hours_forever = str(game['hours_forever']) if "hours_forever" in game.keys() else "NULL"
        #print('\t'.join([appid, name, hours, hours_forever]))
        this_game_info = ",".join([appid, name, hours_forever])
        game_list.append(this_game_info)

    game_info = "|".join(game_list)
    #print(game_info)
    return game_info


def get_userfriends_page(htmlPath):
    #print("=========================get friends name and url===============================")
    bsObj = get_BsFromHtml(htmlPath)
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
    #print(friends_info)
    return friends_info









def get_pages(name, url):
    bsObj = get_BeautifulSoup(url)
    print(url)
    if bsObj.find('div', {'class':'profile_private_info'}) != None:
        print("Secret:\t"+url)
        return

    title = bsObj.find('title').text.strip().split('::')[1].replace(' ','')
    desc_meta = bsObj.find('meta', {'name':'Description'})
    desc = "NULL" if desc_meta == None else desc_meta.attrs['content']

    ##### find badges
    badges_info = "NULL"
    
    if bsObj.find('a',{'href': url+'/badges/'}) != None:
        badges_url = url + '/badges'
        badge_html = '../pages/'+name+'_badge.html'
        subprocess.run("node getPagehtml.js '"+badges_url+"' "+badge_html, shell=True, check=True)
        badges_info = get_userbadges_page(badge_html, url)
        subprocess.run("rm "+badge_html, shell=True, check=True)
    else:
        print("badges not found...")

    #### find games
    games_info = "NULL"
    
    if bsObj.find('a',{'href': url+'/games/?tab=all'}) != None:
        game_url = url + '/games/?tab=all'
        game_html = '../pages/'+name+'_game.html'
        subprocess.run("node getPagehtml.js '"+game_url+"' "+game_html, shell=True, check=True)
        games_info = get_usergames_page(game_html)
        subprocess.run("rm "+game_html, shell=True, check=True)
    else:
        print("games not found...")


    #### find groups
    groups_info = "NULL"
    
    if bsObj.find('a',{'href': url+'/groups/'}) != None:
        group_url = url + '/groups'
        group_html = '../pages/'+name+'_group.html'
        subprocess.run("node getPagehtml.js '"+group_url+"' "+group_html, shell=True, check=True)
        groups_info = get_usergroups_page(group_html)
        subprocess.run("rm "+group_html, shell=True, check=True)
    else:
        print("groups not found...")


    #### find friends
    friends_info = "NULL"
    
    if bsObj.find('a',{'href': url+'/friends/'}) != None:
        friend_url = url + '/friends'
        friend_html = '../pages/'+name+'_friend.html'
        subprocess.run("node getPagehtml.js '"+friend_url+"' "+friend_html, shell=True, check=True)
        friends_info = get_userfriends_page(friend_html)
        #subprocess.run("rm "+friend_html, shell=True, check=True)
    else:
        print("friends not found...")


    all_infos = []
    all_infos.append(title)
    all_infos.append(desc)
    all_infos += badges_info
    all_infos.append(games_info)
    all_infos.append(groups_info)
    all_infos.append(friends_info)

    #print(str(all_infos))
    return all_infos

if __name__=='__main__':
    #get_user_basicInfo("http://steamcommunity.com/id/afarnsworth/")
    #get_level_experValue("http://steamcommunity.com/id/afarnsworth")
    #get_usergames("http://steamcommunity.com/id/afarnsworth")
    #get_userfriends("http://steamcommunity.com/id/afarnsworth")
    #Run("http://steamcommunity.com/id/afarnsworth")
    get_pages('gishyfishy',"http://steamcommunity.com/id/gishyfishy")
    #Run("http://steamcommunity.com/id/0000681_222")
    #Run("http://steamcommunity.com/id/76561198407744512")
    #get_user_basicInfo("http://steamcommunity.com/id/76561198407744512")
    #get_game_list("http://steamcommunity.com/id/76561198407744512")
    #get_usergroups("http://steamcommunity.com/id/76561198407744512")
    #get_usergroups("http://steamcommunity.com/id/afarnsworth")
    #get_level_experValue("http://steamcommunity.com/id/76561198407744512")
    #get_userfriends("http://steamcommunity.com/id/76561198407744512")
    #run()
    #get_usergroups()
    #get_userfriends()
    print("Success....")
