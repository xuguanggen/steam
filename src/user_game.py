
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
import json

from bs4 import BeautifulSoup

import requests
import sys
import re

type = sys.getfilesystemencoding()

headers = {
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}

headers_goto = {
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Cookie":"mature_content=1; browserid=1108298056224311180; lastagecheckage=23-November-1992; ASP.NET_SessionId=fj1j3tqqqfjpuvdx5hsal1os; steamCountry=CN%7C2f44e44f3171dd981d3463aba73f9966; sessionid=cef5355178eac8b680b8bd49; app_impressions=244210@1_4_4__43|110800:110810@1_4_4__100|271590@1_4_4__139|404590@1_4_4__139|363930@1_4_4__139|12100:12120:12110@1_4_4__139|322110@1_4_4__tab-PopularNewReleases|639470@1_4_4__tab-PopularNewReleases|361800@1_4_4__tab-PopularNewReleases|641990@1_4_4__tab-PopularNewReleases|701180@1_4_4__tab-PopularNewReleases; recentapps=%7B%22295110%22%3A1503408269%2C%22701180%22%3A1503387527%2C%22675260%22%3A1503300327%2C%22203160%22%3A1503287918%2C%22385800%22%3A1502674384%2C%22206420%22%3A1502630264%2C%22230410%22%3A1502629453%2C%22215280%22%3A1502624518%2C%228880%22%3A1502529423%2C%22570%22%3A1502416974%7D; timezoneOffset=28800,0; _ga=GA1.2.214342574.1498031951; _gid=GA1.2.2052555264.1503387598; _gat_app=1"
}

headers_birthday = {
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Cookie":"browserid=1108298056224311180; ASP.NET_SessionId=i011hijhkcpduv2oh1gqx1gw; steamCountry=CN%7C0e4d2bef8f61cbf3f092a27add44efb9; sessionid=045a5a5ea1b87132f030a820; app_impressions=383980@1_4_4__43|359550@1_4_4__100|489830@1_4_4__139|358040@1_4_4__100|641990@1_4_4__100; birthtime=722448001; lastagecheckage=23-November-1992; recentapps=%7B%22271590%22%3A1503452759%2C%22295110%22%3A1503408274%2C%22701180%22%3A1503387527%2C%22675260%22%3A1503300327%2C%22203160%22%3A1503287918%2C%22385800%22%3A1502674384%2C%22206420%22%3A1502630264%2C%22230410%22%3A1502629453%2C%22215280%22%3A1502624518%2C%228880%22%3A1502529423%7D; timezoneOffset=28800,0; _ga=GA1.2.214342574.1498031951; _gid=GA1.2.2052555264.1503387598; _gat_app=1"
}

#f_in = open('../data/url_uniq.txt','r')
f_out = open('user_game.csv','a', encoding='utf-8')



def get_UserGame(user_url, game_html):
    #game_url = user_url+'/games/?tab=all'
    #req = urllib.request.Request(game_url, headers=headers)
    #response = urlopen(req).read()
    ## response = response.decode('UTF-8').encode(type)
    #bsObj = BeautifulSoup(response, "lxml")

    bsObj = get_BsFromHtml(game_html)
    div_private = bsObj.find('div',{'class':'profile_private_info'})
    div_error = bsObj.find('p',{'class':'sectionText'})
    if div_private != None or div_error != None:
        return
    user_name = bsObj.find('title').text.strip().split('::')[1].replace(' ','')
    div_games = bsObj.find('script',{'language':'javascript'})
    game_infos = ''
    if div_games != None
        src_data = json.loads(div_games.text.strip().split('\n')[0].split('=')[1].replace('\r','')[1:-1])
        game_list = []
        for game in src_data:
            appid = str(game['appid']) if 'appid' in game.keys() else 'NULL'
            playhours = str(game['hours_forever']).replace(',','') if 'hours_forever' in game.keys() else 'NULL'
            game_info = ','.join([appid,playhours])
            game_list.append(game_info)
        game_infos = '|'.join(game_list)
    else:
        game_infos = ''

    info_list = []
    info_list.append(user_name)
    info_list.append(user_url)
    info_list.append(game_infos)
    f_out.write(str(info_list)+'\n')


def get_BsFromHtml(htmlPath):
    html = open(htmlPath, 'r')
    htmlpage = html.read()
    bsObj = BeautifulSoup(htmlpage, 'lxml')
    return bsObj

if __name__ == '__main__':
    print('fuck')
    user_url = sys.argv[1]
    game_html = sys.argv[2]
    get_UserGame(user_url, game_html)
    # get_UserGame('http://steamcommunity.com/id/tomqbui')
    # get_gamePrice('http://store.steampowered.com/app/295110','295110')
    # get_gamePrice('http://store.steampowered.com/app/588040', '58840')
    # get_gameInfo('http://store.steampowered.com/app/203160/Tomb_Raider/')
    # get_gameInfo('http://store.steampowered.com/app/22380/Fallout_New_Vegas/?snr=1_7_7_230_150_6')

   # url_header = 'http://steamcommunity.com/'
   # idx = 0
   # for id in f_in:
   #     id = id.strip()
   #     user_url = url_header + id
   #     get_UserGame(user_url)
   #     print(str(idx))
   #     idx += 1

   # print("Success....")
   # f_in.close()
   # f_out.close()
