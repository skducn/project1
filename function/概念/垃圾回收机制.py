# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-1-18
# Description: 垃圾回收机制
# python内都是对象，变量都是对象的引用，这有点像C语言的指针。
# sys.getrefcount() 可以查询对象的引用计数, 返回计数总是比实际多1，因为包含了调用此函数的临时计数。
# 默认在对应引用计数为0的时候，python内部的垃圾回收机制会将此对象所占用的内存收回。
# ********************************************************************************************************************

import sys
a = 100
print(sys.getrefcount(a))  # 5
b = a
print(sys.getrefcount(a))  # 6

class Test():
  def __init__(self):
    pass

t = Test()
k = Test()
t._self = t
print(sys.getrefcount(t))  # 3
print(sys.getrefcount(k))  # 2

# del(k)
# print(sys.getrefcount(k))  # NameError: name 'k' is not defined
#
# del(t)
# print(sys.getrefcount(t._self))  # 2


import sys

# 创建一个对象并分配内存
a1 = [1, 2, 3, 4]  # 赋值
b1 = a1  # 赋值
b12 = a1  # 赋值

# 获取对象引用次数，比实际多1次。
refcount = sys.getrefcount(a1)

# 输出引用次数
print("Reference count of a is:", refcount)