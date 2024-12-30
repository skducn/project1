# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-12-30
# Description: 并发编程模式，并行处理文件,加速文件读取与操作。
# 使用 asyncio 进行异步编程
# asyncio 是 Python 3.4 引入的异步 I/O 框架，可以提高网络请求、文件读写等 I/O 密集型任务的性能。
# http://www.51testing.com/html/80/15326880-7803860.html
# *****************************************************************

from PO.WebPO import *
Web_PO = WebPO("chrome")

import asyncio
async def fetch_data(url):
    # 模拟网络请求
    await asyncio.sleep(3)
    print(url)
    Web_PO.openURL(url)
    return f"Data from {url}"
async def main():
    urls = ["http://www.baidu.com", "http://www.jd.com", "http://www.163.com"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)
# 运行异步主程序
asyncio.run(main())

