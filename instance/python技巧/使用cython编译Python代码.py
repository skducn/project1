# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 　　cython可以将Python代码编译成C代码，从而提高执行速度。
# *****************************************************************

# 不推荐：纯Python代码
def slow_function(n):
    return sum(i * i for i in range(n))

# 推荐：使用Cython编译
# 在文件slow_function.pyx中定义
# def fast_function(int n):
#     cdef int i, result = 0
#     for i in range(n):
#         result += i * i
#     return result
# # 编译并导入
# from distutils.core import setup
# from Cython.Build import cythonize
# setup(ext_modules=cythonize("slow_function.pyx"))
# from slow_function import fast_function
# print(slow_function(1000000))  # 较慢
# print(fast_function(1000000))  # 较快







