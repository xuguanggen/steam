#! /usr/bin/env python
#coding=utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup

from prettytable import PrettyTable

from config import *




def fetch_discussion(url):
    response = urlopen(url)
    bsObj = BeautifulSoup(response)

    f_discussion_out = open(DISCUSSION_INFO_PATH,'w')
    for item in bsObj.findAll('a', {'class':'recent_game_discussion quasi_official_group'}):
        href = item.attrs['href']
        if href.find('1840') != -1 or href.find('211') != -1:
            continue
        discussion_name = item.find('div','recent_game_discussion_name ellipsis').text.strip()
        discussion_count = item.find('div', 'recent_game_discussion_count ellipsis').text.strip().split(' ')[0].replace(",",'')
        group = '\t'.join([discussion_name, href, discussion_count])
        f_discussion_out.write(group+'\n')

    f_discussion_out.close()


####从一个讨论组的某一个页面中获取当前页面帖子的链接
def fetch_urls_from_single_page(url):
    response = urlopen(url)
    bsObj = BeautifulSoup(response)
    
    url_list = []
    for discussion_item in bsObj.findAll('a', {'class':'forum_topic_overlay'}):
        discussion_href = discussion_item.attrs['href']
        print(discussion_href)
        url_list.append(discussion_href)
    
    return url_list


#### get each discussion content
def fetch_discussion_content():
    f_discussion_in = open(DISCUSSION_INFO_PATH,'r')
    for discussion_group_info in f_discussion_in.readlines():
        discussion_group_info = discussion_group_info.strip().split('\t')
        
        discussion_group_name = discussion_group_info[0]
        discussion_group_url = discussion_group_info[1]
        
        response = urlopen(discussion_group_url)
        bsObj = BeautifulSoup(response)

        url_list = fetch_urls_from_single_page(discussion_group_url)

        div = (bsObj.find('div',{'class':'forum_paging_controls'}))
        pagetotal_id = div.attrs['id'].replace('pagecontrols','footerpagetotal')
        
        num_discussions = int(bsObj.find('span', {'id':pagetotal_id}).text.replace(',',''))
        num_pages = int((num_discussions / NUM_PAGE) + 1) if num_discussions % NUM_PAGE != 0 else int(num_discussions / NUM_PAGE)
        print(str(num_discussions)+','+str(num_pages))

        for pageIdx in range(2, num_pages+1):
            page_url = discussion_group_url + "?fp="+str(pageIdx)
            url_list += fetch_urls_from_single_page(page_url)

        print(str(len(url_list)))
 

        #break
    f_discussion_in.close()

def run():
    #url = 'http://www.steamcommunity.com/discussions/'
    #fetch_discussion(url)

    fetch_discussion_content()


if __name__=='__main__':
    run()
    print("Success....")
