# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 在优化代码之前，先使用cProfile找出瓶颈所在。
# *****************************************************************

import cProfile
def profile_me():
    total = 0
    for i in range(1000000):
        total += i
    return total

cProfile.run('profile_me()')






