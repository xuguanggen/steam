#! /usr/bin/env python3
#coding=utf-8

import os
import re
import subprocess

from urllib.request import urlopen
from bs4 import BeautifulSoup

from prettytable import PrettyTable

from config import *
import requests





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

    fetch_discussion_user()


if __name__=='__main__':
    run()
    print("Success....")
