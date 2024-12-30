# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-12-30
# Description: numba 是一个开源库，可以将 Python 代码即时编译成机器码，从而提高性能。
# http://www.51testing.com/html/80/15326880-7803860.html
# https://blog.csdn.net/weixin_45977690/article/details/133886829
# github主页：https://github.com/numba/numba
# 在线文档：https://numba.readthedocs.io/en/stable/index.html
# numba非常适合于使用了numpy数组、函数和循环的代码，使用的方法就是装饰器，用它！用的好时间节省个几十倍。numba的可使用范围：
# 操作系统：Windows(64bit), OSX, Linux(64bit).
# 架构：x86, x86_64, ppc64le, armv8l(aarch64), M1 / Arm64.
# GPU：NvidiaCUDA.
# CPython
# NumPy版本：1.22~1.25

# *****************************************************************

import numba, time
import numpy as np


def cal_sum(a):
    result = 0
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            result += a[i, j]
    return result

start = time.perf_counter()
a = np.random.random((5000, 5000))
result = cal_sum(a)
end = time.perf_counter()
print("原始代码耗时：{}s".format((end - start)))

#OUT:
#原始代码耗时：5.725140199996531s



@numba.jit(nopython=True)
def cal_sum(a):
    result = 0
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            result += a[i, j]
    return result


start = time.perf_counter()
a = np.random.random((5000, 5000))
result = cal_sum(a)
end = time.perf_counter()
print("加速后耗时：{}s".format((end - start)))

# OUT:
# 加速后耗时：0.2892118000017945s





