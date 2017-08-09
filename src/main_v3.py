#! /usr/bin/env python3
#coding=utf-8


import sys
import os
import time as t
from time import time
import subprocess

from multiprocessing import Process, Queue
from utils import get_pages

type = sys.getfilesystemencoding()


NumThreads = 300
url_head = "http://steamcommunity.com/"


def run_thread(url_batch, queue, f_out, thread_idx):
    for url in url_batch:
        url = url_head + url.strip()
        subprocess.run("node test/index.js '"+url+"' "+f_out, shell=True, check=True)
        #time.sleep(1)
    #print(str(thread_idx)+"\tSuccess")

if __name__=='__main__':
    start_time = time()
    f_in = sys.argv[1]
    f_url_in = open(f_in, 'r')
    url_list = []
    for url in f_url_in:
        url_list.append(url)
    f_url_in.close()
    url_length = len(url_list)
    num_urls_per_thread = int(url_length / NumThreads) if url_length % NumThreads ==0 else int(url_length / NumThreads) + 1
    
    queue = Queue()
    for thread_idx in range(NumThreads):
        url_batch = []
        if thread_idx == NumThreads - 1:
            url_batch = url_list[thread_idx * num_urls_per_thread :]
        else:
            url_batch = url_list[thread_idx * num_urls_per_thread:(thread_idx + 1) * num_urls_per_thread]
        #print(str(thread_idx)+":"+str(len(url_batch)))
    
        f_out = '../data/userdata/thread_'+str(thread_idx)+'.csv'
        p = Process(target = run_thread, args=[url_batch, queue, f_out, thread_idx])
        p.start()
        t.sleep(0.5)
    end_time = time()
    #print("Completed.....")
    print("Time:\t"+str((end_time - start_time)/60)+' minutes')
