# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-12-30
# Description: 使用 memoryview 减少内存复制
# memoryview 对象允许你创建对同一内存块的多个视图，从而减少内存复制，提高性能。
# http://www.51testing.com/html/80/15326880-7803860.html
# *****************************************************************

import numpy as np

# 创建一个 numpy 数组
arr = np.array([1, 2, 3, 4, 5])
# 创建一个 memoryview 对象
mv = memoryview(arr)
# 修改 memoryview 对象会影响原数组
mv[0] = 10
print(arr)  # 输出: [10  2  3  4  5]

