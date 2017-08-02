#! /usr/bin/env python3
#coding=utf-8

################# 多线程爬取用户信息 ###########################

import sys
import os
import time


from multiprocessing import Process, Queue
from GetUserInfoUtils import Run

type = sys.getfilesystemencoding()


NumThreads = 200
url_head = "http://steamcommunity.com/"

def receive_threadMsg(queue):
    while(True):
        msg = queue.get()
        if (msg == 'Done'):
            break

def run_thread(url_batch, queue):
    for url in url_batch:
        url = url_head + url.strip()
        Run(url)

    queue.put('Done')


if __name__=='__main__':
    File_path = '../data/SteamTradingCardsGroup/user_url.txt'
    f_url_in = open(File_path, 'r')
    url_list = []
    for url in f_url_in:
        url_list.append(url)
    f_url_in.close()
    url_length = len(url_list)
    print(str(url_length))
    num_urls_per_thread = int(url_length / NumThreads) if url_length % NumThreads ==0 else int(url_length / NumThreads) + 1
    print(str(num_urls_per_thread))

    
    for thread_idx in range(NumThreads):
        url_batch = []
        if thread_idx == NumThreads - 1:
            url_batch = url_list[thread_idx * num_urls_per_thread :]
        else:
            url_batch = url_list[thread_idx * num_urls_per_thread:(thread_idx + 1) * num_urls_per_thread]
        print(str(thread_idx)+":"+str(len(url_batch)))

        queue = Queue()
        receive_p = Process(target = receive_threadMsg, args=((queue),))
        receive_p.daemon = True
        receive_p.start()

        _start = time.time()
        run_thread(url_batch, queue)
        receive_p.join()
        print("Thread "+str(thread_idx)+" completed, Time:\t"+(str((time.time() - _start)/3600)))
