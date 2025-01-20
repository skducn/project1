# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 对于耗时的函数调用，可以使用functools.lru_cache来缓存结果，避免重复计算。
# *****************************************************************
import functools

# 不推荐：每次调用都重新计算
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 推荐：使用缓存
@functools.lru_cache(maxsize=None)
def fibonacci_cached(n):
    if n <= 1:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)
print(fibonacci(30))  # 较慢
print(fibonacci_cached(30))  # 较快






