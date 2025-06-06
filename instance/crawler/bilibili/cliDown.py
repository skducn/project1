# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-11-11
# Description: 并发编程模式，下载文件
# https://blog.csdn.net/weixin_40025666/article/details/137108894
# bit BV1hV411Q7VV,BV1Ne411J7k7

# 获取bvid 字符串链接
# s_ = Bilibili_PO.getBvidStr("BV1bD421u7Ki")
# print(s_)  ,BV1Zb4y1P76M,BV1HV41197iW,BV1qK4y1i7JL,BV1NV411Q7Cw,...
# *****************************************************************

import threading, sys
from BilibiliPO import *
Bilibili_PO = BilibiliPO()


# 下载函数
def download_file(url):
    Bilibili_PO.downloadOne(url)
    # print(f"Downloaded {url} and done")


# 下载器类
class DownloaderThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        download_file(self.url)



# 创建并启动多个下载线程
l_ = sys.argv[1].split(",")
print(l_)


threads = []
for i, url in enumerate(l_):
    downloader = DownloaderThread(url)
    threads.append(downloader)
    downloader.start()

# 等待所有线程完成下载
for thread in threads:
    thread.join()

