#! /usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import os
import time
import subprocess

from multiprocessing import Process, Queue
from utils import get_pages

type = sys.getfilesystemencoding()


url_head = "http://steamcommunity.com/"




if __name__=='__main__':
    file_in = sys.argv[1]
    file_name = file_in.strip().split('/')[-1]
    f_url_in = open(file_in, 'r')
    url_list = []
    for url in f_url_in:
        url_list.append(url)
    f_url_in.close()

    f_out = open('../data/result/result_'+file_name+'.csv', 'w')
    
    for i in range(len(url_list)):
        print(file_name+'-'+str(i))
        url = url_list[i]
        name = url.strip().split('/')[1]
        url = url_head + url.strip()
        user_info = get_pages(name, url)
        if user_info == 'NULL':
            continue
        f_out.write(str(user_info)+'\n')
    f_out.close()
    print(str(file_in)+'\t completed.....')
