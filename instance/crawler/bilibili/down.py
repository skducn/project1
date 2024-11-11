# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-11-11
# Description: 多线程，下载文件
# https://blog.csdn.net/weixin_40025666/article/details/137108894
# *****************************************************************

import threading
from BilibiliPO import *
Bilibili_PO = BilibiliPO()

file_urls = ["BV1qK4y1i7JL", "BV1HV41197iW"]


# 下载函数
def download_file(url):
    Bilibili_PO.downloadOne(url)
    print(f"Downloaded {url} and done")


# 下载器类
class DownloaderThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        download_file(self.url)



# 创建并启动多个下载线程
threads = []
for i, url in enumerate(file_urls):
    downloader = DownloaderThread(url)
    threads.append(downloader)
    downloader.start()

# 等待所有线程完成下载
for thread in threads:
    thread.join()

print("All downloads completed!")