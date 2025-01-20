# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description:
# *****************************************************************

# 不推荐：使用for循环创建平方数列表
squares_loop = []
for i in range(10):
    squares_loop.append(i ** 2)

# 推荐：使用列表推导式
squares_comprehension = [i ** 2 for i in range(10)]











