#! /usr/bin/env python3
#coding=utf-8


import sys
import os
import time


from multiprocessing import Process, Queue
from utils import get_pages

type = sys.getfilesystemencoding()


NumThreads = 200
url_head = "http://steamcommunity.com/"


def run_thread(url_batch, queue, f_out):
    for url in url_batch:
        name = url.strip().split('/')[1]
        url = url_head + url.strip()
        print(url)
        all_infos = get_pages(name, url)
        f_out.write(str(all_infos)+'\n')
    f_out.close()


if __name__=='__main__':
    File_path = '../data/url_uniq.txt'
    f_url_in = open(File_path, 'r')
    url_list = []
    for url in f_url_in:
        url_list.append(url)
    f_url_in.close()
    url_length = len(url_list)
    #print(str(url_length))
    num_urls_per_thread = int(url_length / NumThreads) if url_length % NumThreads ==0 else int(url_length / NumThreads) + 1
    #print(str(num_urls_per_thread))

    queue = Queue()
    for thread_idx in range(NumThreads):
        url_batch = []
        if thread_idx == NumThreads - 1:
            url_batch = url_list[thread_idx * num_urls_per_thread :]
        else:
            url_batch = url_list[thread_idx * num_urls_per_thread:(thread_idx + 1) * num_urls_per_thread]
        print(str(thread_idx)+":"+str(len(url_batch)))
        
        f_out = open('../data/userdata/thread_'+str(thread_idx)+'.csv', 'w')
        p = Process(target = run_thread, args=[url_batch, queue, f_out])
        p.start()
