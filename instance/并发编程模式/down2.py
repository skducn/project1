# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-11-11
# Description: 并发编程模式，下载文件
# http://www.51testing.com/html/80/15326880-7803923.html
# 假设我们需要从多个URL下载文件，我们可以结合多线程和异步IO来实现这个任务。
# *****************************************************************

import threading
import asyncio
import aiohttp

# 异步下载文件的函数
async def download_file(session, url, file_name):
    async with session.get(url) as response:
        with open(file_name, 'wb') as f:
            f.write(await response.read())
    print(f"文件 {file_name} 下载完成")
# 多线程下载函数
def download_files_multithread(urls):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    # 创建HTTP会话
    async with aiohttp.ClientSession() as session:
        for url in urls:
            file_name = url.split('/')[-1]
            task = loop.create_task(download_file(session, url, file_name))
            tasks.append(task)
        # 等待所有任务完成
        loop.run_until_complete(asyncio.gather(*tasks))
# 主函数
def main():
    urls = [
        'https://example.com/file1.zip',
        'https://example.com/file2.zip',
        'https://example.com/file3.zip'
    ]

    # 创建并启动线程
    threads = []
    for i in range(len(urls)):
        thread = threading.Thread(target=download_files_multithread, args=(urls[i:i+1],))
        threads.append(thread)
        thread.start()
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    print("所有文件下载完成")
# 运行主函数
main()