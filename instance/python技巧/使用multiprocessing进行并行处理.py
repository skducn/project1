# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 如果你的任务是可以并行化的，那么使用multiprocessing模块可以显著提高性能。
# *****************************************************************

import multiprocessing

def square(x):
    return x ** 2

# 不推荐：串行处理
results_serial = [square(i) for i in range(10)]

# 推荐：并行处理
pool = multiprocessing.Pool()
results_parallel = pool.map(square, range(10))
pool.close()
pool.join()







