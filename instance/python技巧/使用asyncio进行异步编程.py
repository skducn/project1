# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 　　对于I/O密集型任务，使用asyncio可以提高程序的响应速度。
# *****************************************************************

import asyncio

# 不推荐：同步等待
def sync_fetch():
    import time
    time.sleep(1)
    return "Data fetched"


async def fetch_data():
    await asyncio.sleep(1)
    return "Data fetched"

# 推荐：异步等待
async def main():
    result = await fetch_data()
    print(result)
asyncio.run(main())  # 输出: Data fetched






