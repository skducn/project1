# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description:
# *****************************************************************

# 不推荐：手动计算列表元素之和
def sum_list_manual(lst):
    total = 0
    for num in lst:
        total += num
    return total

# 推荐：使用内置sum函数
def sum_list_builtin(lst):
    return sum(lst)












