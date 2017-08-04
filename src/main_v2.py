#! /usr/bin/env python3
# -*- coding:utf-8 -*-


import sys
import os
import time


from multiprocessing import Process, Queue
from GetUserInfoUtils import Run

type = sys.getfilesystemencoding()


NumThreads = 100
url_head = "http://steamcommunity.com/"


def run_thread(url_batch, queue, f_out):
    for url in url_batch:
        url = url_head + url.strip()
        print(url)
        user_info = Run(url)
        f_out.write(str(user_info)+'\n')
    f_out.close()


if __name__=='__main__':
    src_file = sys.argv[1]
    res_file = sys.argv[2]
    f_url_in = open(src_file, 'r')
    url_list = []
    for url in f_url_in:
        url_list.append(url)
    f_url_in.close()

    f_out = open(res_file, 'w')
    idx = 0
    for url in url_list:
        url = url_head + url.strip()
        #Run(url)
        user_info = Run(url)
        f_out.write(str(user_info)+'\n')
        print(str(idx)+', completed....')
        time.sleep(10)
        idx += 1
    f_out.close()
