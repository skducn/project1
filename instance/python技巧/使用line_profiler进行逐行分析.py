# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: line_profiler可以帮助你找到具体哪一行代码最耗时。
# 安装line_profiler
# pip install line_profiler
# *****************************************************************

@profile
def function_to_profile():
    a = 2
    b = 3
    c = a + b
    return c

function_to_profile()







