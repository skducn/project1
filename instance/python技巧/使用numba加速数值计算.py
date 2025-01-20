# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 　　numba可以通过即时编译技术加速数值计算。
# *****************************************************************

import numba

@numba.jit
def fast_sum(a, b):
    return a + b

# 不推荐：纯Python加法
def slow_sum(a, b):
    return a + b

print(slow_sum(10, 20))  # 输出: 30
print(fast_sum(10, 20))  # 输出: 30







