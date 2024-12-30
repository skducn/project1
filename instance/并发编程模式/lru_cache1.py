# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-12-30
# Description: 使用 functools.lru_cache 缓存函数结果
# functools.lru_cache 可以缓存函数的返回值，避免重复计算，提高性能。
# http://www.51testing.com/html/80/15326880-7803860.html
# *****************************************************************

import functools

@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
# 第一次调用会计算
print(fibonacci(10))  # 输出: 55

# 第二次调用会直接返回缓存结果
print(fibonacci(10))  # 输出: 55，但速度更快


