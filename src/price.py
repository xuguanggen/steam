
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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}


headers_goto = {
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Cookie":"mature_content=1; steamCountry=CN%7C505b3bb88d334209198d1361a65afa7d; browserid=1171354790251995836; XPR[search]=0_0_0; sessionid=db949a2dfbb75fa730f757e2; _gat_app=1; snr=1_5_9__205|http%3A%2F%2Fstore.steampowered.com%2Fsearch%2F%3Fterm%3D; app_impressions=378649@1_7_7_204_150_1|378648@1_7_7_204_150_1|292030@1_7_7_204_150_1|475550@1_7_7_204_150_1|268500@1_7_7_204_150_1|655550@1_200_4__201|346110@1_4_4__118|616560@1_4_4__139|265930@1_4_4__139|418240@1_4_4__139|221680@1_4_4__43|595140@1_4_4__139|369990@1_4_4__139|107410@1_4_4__139|292030:378649:378648@1_4_4__139|674750@1_4_4__tab-PopularNewReleases|434460@1_4_4__tab-PopularNewReleases|593380@1_4_4__tab-PopularNewReleases|346110@1_4_4__tab-PopularNewReleases|635200@1_4_4__tab-PopularNewReleases|381020@1_4_4__tab-PopularNewReleases|515220@1_4_4__tab-PopularNewReleases|589120@1_4_4__tab-PopularNewReleases|271590@1_7_7_230_150_1|730@1_7_7_230_150_1|433850@1_7_7_230_150_1|578080@1_7_7_230_150_1|570@1_7_7_230_150_1; recentapps=%7B%22346110%22%3A1504107568%2C%22268500%22%3A1504107551%2C%22578080%22%3A1504107522%7D; timezoneOffset=28800,0; _ga=GA1.2.206593339.1504107542; _gid=GA1.2.2087375590.1504107542"
}

headers_birthday = {
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Cookie":"browserid=1108298056224311180; ASP.NET_SessionId=i011hijhkcpduv2oh1gqx1gw; steamCountry=CN%7C0e4d2bef8f61cbf3f092a27add44efb9; sessionid=045a5a5ea1b87132f030a820; app_impressions=383980@1_4_4__43|359550@1_4_4__100|489830@1_4_4__139|358040@1_4_4__100|641990@1_4_4__100; birthtime=722448001; lastagecheckage=23-November-1992; recentapps=%7B%22271590%22%3A1503452759%2C%22295110%22%3A1503408274%2C%22701180%22%3A1503387527%2C%22675260%22%3A1503300327%2C%22203160%22%3A1503287918%2C%22385800%22%3A1502674384%2C%22206420%22%3A1502630264%2C%22230410%22%3A1502629453%2C%22215280%22%3A1502624518%2C%228880%22%3A1502529423%7D; timezoneOffset=28800,0; _ga=GA1.2.214342574.1498031951; _gid=GA1.2.2052555264.1503387598; _gat_app=1"
}

f_in = open('game_url_20170905.csv','r')
f_out = open('game_info_20170905.csv','a', encoding='utf-8')



def get_gameInfo(url):
    req = urllib.request.Request(url, headers=headers)
    response = urlopen(req).read()
    # response = response.decode('UTF-8').encode(type)
    bsObj = BeautifulSoup(response, "lxml")

    game_id = url.strip().split('/')[4]

    game_recent_pingjia = ''
    game_recent_num = ''
    game_recent_rate = ''
    game_all_pingjia = ''
    game_all_num = ''
    game_all_rate = ''
    game_label = ''
    price = ''
    release_date = ''
    all_pingce = -1
    pos_pingce = -1
    h = bsObj.find('h2')
    # print(h.text.strip())
    if h != None and '该产品内容可能不适合所有年龄段，或不宜在工作期间访问。' == h.text.strip():
        req = urllib.request.Request(url, headers=headers_goto)
        response = urlopen(req).read()
        # response = response.decode('UTF-8').encode(type)
        bsObj = BeautifulSoup(response, "lxml")
    elif h != None and '请输入您的生日：' == h.text.strip():
        req = urllib.request.Request(url, headers=headers_birthday)
        response = urlopen(req).read()
        # response = response.decode('UTF-8').encode(type)
        bsObj = BeautifulSoup(response, "lxml")

    div_game_name = bsObj.find('div',{'class':'apphub_AppName'})
    if div_game_name == None:
        return
    game_name = div_game_name.text.strip()
    div_game_summary = bsObj.findAll('div', {'class': 'user_reviews_summary_row'})
    div_game_pingjia = bsObj.findAll('span',{'class': re.compile('game_review_summary')})[0:2]
    div_tags = bsObj.find('div',{'class':'glance_tags popular_tags'})

    if div_tags != None:
        div_game_label = div_tags.findAll('a',{'href': re.compile("^http://store.steampowered.com/tag/")})
        if div_game_label != None:
            label_list = []
            for div in div_game_label:
                #     print(div.text.strip())
                label_list.append(div.text.strip())
            game_label = ','.join(label_list)


    game_new_summary = ''
    if div_game_summary != None:
        if len(div_game_summary) >= 2:
            game_new_summary = div_game_summary[0].attrs['data-store-tooltip']
            game_all_summary = div_game_summary[1].attrs['data-store-tooltip']
        elif len(div_game_summary) == 1:
            game_all_summary = div_game_summary[0].attrs['data-store-tooltip']

    if game_new_summary != '':
        game_recent_num = game_new_summary.strip().split(' ')[3].replace(',','')
        game_recent_rate = game_new_summary.strip().split(' ')[-2]

    if game_all_summary != '' and game_all_summary != '无用户评测':
        if len(game_all_summary.strip().split(' ')) >= 2:
            game_all_num = game_all_summary.strip().split(' ')[0].replace(',', '')
            game_all_rate = game_all_summary.strip().split(' ')[-2]


    if div_game_pingjia != None:
        if len(div_game_pingjia) >= 2:
            game_recent_pingjia = div_game_pingjia[0].text.strip()
            game_all_pingjia = div_game_pingjia[1].text.strip()
        elif len(div_game_pingjia) == 1:
            game_all_pingjia = div_game_pingjia[0].text.strip()




    div_price = bsObj.find('div', {'class': 'game_purchase_price price'})
    if div_price != None:
        price = div_price.text.strip()
    else:
        div_price = bsObj.find('div', {'class': 'discount_final_price'})
        if div_price != None:
            price = div_price.text.strip()
        else:
            price = 'unknown'


    div_date = bsObj.find('span', {'class': 'date'})
    if div_date != None:
        release_date = div_date.text.strip()
    else:
        release_date = 'unknown'

    div_prefix_pingce = bsObj.find('div',{'class':'summary column'})
    if div_prefix_pingce != None and div_prefix_pingce.text.strip() != '无用户评测':
        div_pingce = bsObj.findAll('span', {'class':'user_reviews_count'})
        if div_pingce != None:
            all_pingce = int(div_pingce[0].text.strip().replace(')','').replace('(','').replace(',',''))
            pos_pingce = int(div_pingce[1].text.strip().replace(')','').replace('(','').replace(',',''))


    gameInfo = {
        'statis_date': time.strftime('%Y%m%d',time.localtime()),
        'id': game_id,
        'name': game_name,
        'recent_pj': game_recent_pingjia,
        'recent_num': game_recent_num,
        'recent_rate': game_recent_rate,
        'all_pj': game_all_pingjia,
        'all_num': game_all_num,
        'all_rate': game_all_rate,
        'label': game_label,
        'price': price,
        'release_date': release_date,
        'all_pingce': all_pingce,
        'pos_pingce' : pos_pingce
    }
    # print(str(gameInfo))
    f_out.write(str(gameInfo)+'\n')

def get_BsFromHtml(htmlPath):
    html = open(htmlPath, 'r')
    htmlpage = html.read()
    bsObj = BeautifulSoup(htmlpage, 'lxml')
    return bsObj

if __name__ == '__main__':
    print('fuck')
    # get_gameInfo('http://store.steampowered.com/app/577800/NBA_2K18/')
    # get_gamePrice('http://store.steampowered.com/app/295110','295110')
    # get_gamePrice('http://store.steampowered.com/app/588040', '58840')
    # get_gameInfo('http://store.steampowered.com/app/203160/Tomb_Raider/')
    # get_gameInfo('http://store.steampowered.com/app/22380/Fallout_New_Vegas/?snr=1_7_7_230_150_6')

    # url_header = 'http://store.steampowered.com/app//'
    # if url_header.find('//'):
        # print('fuck u')



    idx = 0
    for url in f_in:
        if idx <= 27005:
            idx += 1
            continue
        url = url.strip()
        get_gameInfo(url)
        print(str(idx))
        idx += 1

    print("Success....")
    f_in.close()
    f_out.close()