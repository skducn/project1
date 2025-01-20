# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: numpy是一个专门用于科学计算的库，它提供了高效的数组操作功能。
# *****************************************************************

import numpy as np
# 不推荐：使用纯Python列表进行矩阵乘法
matrix_a = [[1, 2], [3, 4]]
matrix_b = [[5, 6], [7, 8]]
result = [[0, 0], [0, 0]]
for i in range(len(matrix_a)):
    for j in range(len(matrix_b[0])):
        for k in range(len(matrix_b)):
            result[i][j] += matrix_a[i][k] * matrix_b[k][j]

# 推荐：使用numpy进行矩阵乘法
matrix_a_np = np.array(matrix_a)
matrix_b_np = np.array(matrix_b)
result_np = np.dot(matrix_a_np, matrix_b_np)
print(result)  # 输出: [[19, 22], [43, 50]]
print(result_np)  # 输出: [[19 22] [43 50]]






