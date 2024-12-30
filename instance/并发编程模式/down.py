# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-11-11
# Description: 并发编程模式，下载文件
# *****************************************************************

import threading
import requests
import os


# 下载函数
def download_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {url} and saved to {save_path}")


# 下载器类
class DownloaderThread(threading.Thread):
    def __init__(self, url, save_path):
        threading.Thread.__init__(self)
        self.url = url
        self.save_path = save_path

    def run(self):
        download_file(self.url, self.save_path)


# /Users/linghuchong/Downloads/video/bilibili/
# 创建保存文件的目录
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)


# 创建并启动多个下载线程
threads = []
file_urls = [
    "https://www.example.com/file1.txt",
    "https://www.example.com/file2.txt",
    "https://www.example.com/file3.txt"
]
for i, url in enumerate(file_urls):
    file_name = f"file{i + 1}.txt"
    save_path = os.path.join(download_dir, file_name)
    downloader = DownloaderThread(url, save_path)
    threads.append(downloader)
    downloader.start()

# 等待所有线程完成下载
for thread in threads:
    thread.join()

print("All downloads completed!")