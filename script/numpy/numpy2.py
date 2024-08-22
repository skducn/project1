﻿# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: # numpy
# https://blog.csdn.net/weixin_40040404/article/details/80776678
# https://www.cnblogs.com/q735613050/p/9130312.html
# http://www.voidcn.com/article/p-cylcldlk-btm.html
# https://zhuanlan.zhihu.com/p/99889912
# http://www.uml.org.cn/python/201811131.asp  多维数组
# *****************************************************************

'''
1.1 数据源是list时，array和asarray一样，复制一个副本，占用新的内存。
1.2, 数据源是numpy.ndarray时，array()复制一个副本，占用新的内存，而 asarray() 沿用原数据源内存地址。
1.3 asarray() 转换数据类型（float32或int32）
1.4 asarray() 判断元素，符合条件更新为1，否则为0"

2, array() 将数据转为数组

3.1, arange() 生成序列数组(默认int32)
3.2, arange().reshape 生成序列多维数组

4，np.ones() 返回一个全1的n维数组及运算后的值

5，维度与维数

6，N 数组矩阵列相加与行相加

7，数组统计（平均数、合计、平铺）

8，三维数组（面、直线、点）

9，empty()并不能保证返回所有是0的数组，某些情况下，会返回为初始化的垃圾数值

10.1，astype()类型转换
10.2，astype() 如果是把float变为int，小数点后的部分会被丢弃
10.3，astype() 把string里的数字变为实际的数字
10.4，astype() 用其他数组的dtype直接来制定类型
10.5，用类型的缩写，比如u4就代表unit32

11，数组和标量之间的运算

12，数组的索引和切片
13，数组的索引和切片2

14，布尔型索引

15，花式索引是一个NumPy术语，它指的是利用整数数组进行索引。

16，数组转置和轴对换

17, swapaxes方法，需要接受一对轴编号
'''

import numpy as np

print("1.1 数据源是list时，array和asarray一样，复制一个副本，占用新的内存。".center(100, "-"))
list1 = [[1], [2], [3]]
b = np.array(list1)
c = np.asarray(list1)
list1[2] = 55
print(list1)
# [[1], [2], 55]
print(b)
# [[1]
#  [2]
#  [3]]
print(c)
# [[1]
#  [2]
#  [3]]

print("1.2, 数据源是numpy.ndarray时，array()复制一个副本，占用新的内存，而 asarray() 沿用原数据源内存地址。".center(100, "-"))
a = np.zeros((2, 3))
print(type(a))  # <类与实例 'numpy.ndarray'>
b = np.array(a)  # 复制副本
c = np.asarray(a)  # 沿用源数据地址
a[0][0] = 1
print(a)
# [[1. 0. 0.]
#  [0. 0. 0.]]
print(b)
# [[0. 0. 0.]
#  [0. 0. 0.]]
print(c)
# [[1. 0. 0.]
#  [0. 0. 0.]]


print("1.3 asarray() 转换数据类型（float32或int32）".center(100, "-"))
l = [55, 66]
print(np.asarray(l))  # [55 66]
print(np.asarray(l).dtype)  # int32
f = np.asarray(l, "f")
print(f.dtype)  # float32
print(f)  # [55. 66.]
i = np.asarray(l, "i")
print(i.dtype)  # int32
print(i)  # [55 66]


print("1.4 asarray() 判断元素，符合条件更新为1，否则为0".center(100, "-"))
data = np.asarray([[51, 2], [-3, 0]])
data1 = np.asarray(data > 0, "i")
print(data1)
# [[1 1]
#  [0 0]]
data2 = np.asarray(data < -1, "i")
print(data2)
# [[0 0]
#  [1 0]]
data3 = np.asarray(data > 0, "f")
print(data3)
# [[1. 1.]
#  [0. 0.]]


print("2, array() 将数据转为数组".center(100, "-"))
data = [1, 2, 3]
print(np.array(data))  # [1 2 3]
print(type(np.array(data)))  # <类与实例 'numpy.ndarray'>
print(np.array(data).dtype)  # int32

data = ((9, 10), (11.15, 12))
print(np.array(data))
# [[ 9 10]
#  [11 12]]
print(type(np.array(data)))  # <类与实例 'numpy.ndarray'>
print(np.array(data).dtype)  # float64
print(data[1][0])  # 11.15

data = "4,5,678"
print(np.array(data))  # 4,5,678
print(type(np.array(data)))  # <类与实例 'numpy.ndarray'>
print(np.array(data).dtype)  # <U7

data = {"a": 88, "b": 123}
print(np.array(data))  # {'a': 88, 'b': 123}
print(type(np.array(data)))  # <类与实例 'numpy.ndarray'>
print(np.array(data).dtype)  # object


print("3.1, arange() 生成序列数组(默认int32)".center(100, "-"))
print(np.arange(10))  # [0 1 2 3 4 5 6 7 8 9]
print(np.arange(1, 10))  # [1 2 3 4 5 6 7 8 9]
print(np.arange(1, 10, 3))  # [1 4 7]
print(np.arange(1, 10, 3)[2])  # 7
a = np.arange(1, 13)
print(a)  # [ 1  2  3  4  5  6  7  8  9 10 11 12]
print(type(a))  # <类与实例 'numpy.ndarray'>
print(a.dtype)  # int32

print("3.2, arange().reshape 生成序列多维数组".center(100, "-"))
a = np.arange(1, 25).reshape(4, 2, 3)  # reshape表示重新定义维度，如：4个2行3列的多维数组
print(a)
# [[[ 1  2  3]
#   [ 4  5  6]]
#
#  [[ 7  8  9]
#   [10 11 12]]
#
#  [[13 14 15]
#   [16 17 18]]
#
#  [[19 20 21]
#   [22 23 24]]]


print("4，np.ones() 返回一个全1的n维数组及运算后的值".center(100, "-"))
# numpy.ones(shape, dtype=None, order='C')
# shape : 数组的形状，例如 (2, 3) 或 2.
# dtype : 数组的数据类型，默认为float64. (i = int32, f = float32)
# order : 数组元素在内存中的排列方式，默认 'C’表示C语言排列方式，或者‘F’表示 Fortran 语言排列方式.
a = np.ones(5)
print(a)  # [1. 1. 1. 1. 1.]
print(a.dtype)  # float64

b = np.ones(5, "i")  # 等同于 b = np.ones(5,dtype=np.int32)
print(b)  # [1 1 1 1 1]
print(b.dtype)  # int32

c = np.ones(5, dtype=np.int64)
print(c)  # [1 1 1 1 1]
print(c.dtype)  # int64

d = np.ones(5, "f")  # array([1., 1., 1., 1., 1.], dtype=float32)
print(d)  # [1. 1. 1. 1. 1.]
print(d.dtype)  # float32

e = np.ones((3, 5))  # array([[1.],[1.],[1.]])
print(e)  # //输出的shape，3行5列的二维数组
# [[1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1.]
#  [1. 1. 1. 1. 1.]]
print(e.dtype)  # float64

f = np.ones([3, 4, 2], "i")
print(f)
# [[[1 1]
#   [1 1]
#   [1 1]
#   [1 1]]
#
#  [[1 1]
#   [1 1]
#   [1 1]
#   [1 1]]
#
#  [[1 1]
#   [1 1]
#   [1 1]
#   [1 1]]]
print(f.dtype)  # int32
print(np.ones(5)/5)   #  [0.2 0.2 0.2 0.2 0.2]


print("5，维度与维数".center(100, "-"))
M = np.array(((np.arange(3)), (np.arange(3))))
print(M)  # [[0, 1, 2],[0, 1, 2]]
print(M.shape)  # (2, 3)
print(M.ndim)  # 2    //二维


print("6，N 数组矩阵列相加与行相加".center(100, "-"))
a = [0, 1, 2]
b = [2, 1, 3]
c = [5, 5, 1]
x = np.array([a, b, c])
arr_a = np.sum(x, axis=0)  # /列相加
arr_b = np.sum(x, axis=1)  # 行相加
print(arr_a)  # [7 7 8]
print(arr_b)  # [3 6 11]
print(type(arr_a))  # <类与实例 'numpy.ndarray'>
for i in range(len(arr_b)):
    print(arr_b[i])
# 3
# 6
# 11


print("7，数组统计（平均数、合计、平铺）".center(100, "-"))
x = np.array([1, 2, 3])
print(x.mean())   # 2.0  //平均数
print(x.sum())   # 6  //合计
print(np.tile(x, 1))  # [1,2,3]  //不变
print(np.tile(x, 2))   # [1,2,3,1,2,3]   //维度不变，值扩大2倍
print(np.tile(x, 4))   # [1 2 3 1 2 3 1 2 3 1 2 3]  //维度不变，值扩大4倍
print(np.tile(x, (1, 2)))   # [1,2,3,1,2,3]  //维度不变，值扩大2倍
print(np.tile(x, (2, 2)))   # [1,2,3,1,2,3],[1,2,3,1,2,3]  //维度扩大2倍，值扩大2倍
print(np.tile(x, (2, 1)))   # [1,2,3],[1,2,3]  //维度扩大2倍，值不变



print("8，三维数组（面、直线、点）".center(100, "-"))
x = np.arange(27)
x = np.reshape(x, (3,3,3))
print('第1个水平面', x[0])
print('第2个水平面', x[1])
print('第3个水平面', x[2])
print('第1个面的第一个直线 ', x[0][0])
print('第1个面的第二个直线', x[0][1])
print('第1个面的第三个直线', x[0][2])
print("第1个面的第一条直线的第一个点",x[0][0][0])
print("第1个面的第一条直线的第二个点",x[0][0][1])
print("第1个面的第一条直线的第三个点",x[0][0][2])



print("9，empty()并不能保证返回所有是0的数组，某些情况下，会返回为初始化的垃圾数值".center(100, "-"))
print(np.empty(5))  # [5.e-324 5.e-324 5.e-324 5.e-324 5.e-324]


print("10.1，astype()类型转换".center(100, "-"))
a = np.array([1, 2, 3, 432323123123, 5])
print(a.dtype)  # int64
print(a.astype(np.float64))  # [1.00000000e+00 2.00000000e+00 3.00000000e+00 4.32323123e+11 5.00000000e+00]
a = a.astype(np.float64)
print(a.dtype)  # float64


print("10.2，astype() 如果是把float变为int，小数点后的部分会被丢弃".center(100, "-"))
arr = np.array([3.7, -1.2, -2.6, 0.5, 12.9, 10.1])
print(arr.astype(np.int32))  # [ 3 -1 -2  0 12 10]


print("10.3，astype() 把string里的数字变为实际的数字".center(100, "-"))
# numpy.string_类型，这种类型的长度是固定的，所以可能会直接截取部分输入而不给警告。
numeric_strings = np.array(['1.25', '-9.6', '42'], dtype=np.string_)
print(numeric_strings)  # [b'1.25' b'-9.6' b'42']
print(numeric_strings.dtype)  # |S4
print(numeric_strings.astype(float))  # [ 1.25 -9.6  42.  ]


print("10.4，astype() 用其他数组的dtype直接来制定类型".center(100, "-"))
i = np.arange(10)
calibers = np.array([.22, .270, .357, .380, .44, .50], dtype=np.float64)
print(i.astype(calibers.dtype))  # [0. 1. 2. 3. 4. 5. 6. 7. 8. 9.]


print("10.5，用类型的缩写，比如u4就代表unit32".center(100, "-"))
empty_unit32 = np.ones(2, dtype='u4')
print(empty_unit32)  # [1 1]

# astype总是会返回一个新的数组。



print("11，数组和标量之间的运算".center(100, "-"))
# 数组可对数据执行批量运算，叫矢量化。
# 大小相等的数组之间的任何算术运算都会将运算应用到元素级
arr = np.array([[1., 2., 3.], [4., 5., 6.]])
print(arr * arr)
# [[ 1.  4.  9.]
#  [16. 25. 36.]]
print(arr + arr)
# [[ 2.  4.  6.]
#  [ 8. 10. 12.]]
print(arr - arr)
# [[0. 0. 0.]
 # [0. 0. 0.]]
# 数组与标量的算术运算也会将那个标量值传播到各个元素
print(1/arr)
# [[1.         0.5        0.33333333]
#  [0.25       0.2        0.16666667]]
# 不同大小的数组之间的运算叫做广播（broadcasting）


print("12，数组的索引和切片".center(100, "-"))
# 当将一个标量值赋给一个切片时（如arr[5:8]=12），该值会自动传播（“广播”）到整个选区。
# 和Python列表不同的是，数组切片是原始数组的视图，数据不会被复制，任何修改都会反应到源数组上。
arr = np.arange(10)
print(arr[5])
print(arr[5:8])  #[5 6 7]
arr[5:8] = 12
print(arr)  # [ 0  1  2  3  4 12 12 12  8  9]
arr_slice = arr[5:8]
arr_slice[1] = 12345
print(arr)  # [    0     1     2     3     4    12 12345    12     8     9]
arr_slice[:] = 64
print(arr)  # [ 0  1  2  3  4 64 64 64  8  9]

# 若想得到ndarray切片的一份副本，就需要显式地进行复制操作，例如arr[5:8].copy()
x = arr[5:8].copy()
x[1] = 100
print(x)  # [ 64 100  64]
print(arr)  # [ 0  1  2  3  4 64 64 64  8  9]

# 对比一下列表，列表不能修改源值
list1 = [0,1,2,3,4,5,6,7,8,9]
print(list1[5])  # 5
print(list1[5:8])  # [5, 6, 7]
# list1[5:8] = 12  # 报错，列表不能修改源值


# 在一个二维数组中，各索引位置上的元素不再是标量而是一维数组
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
print(arr2d[2])  # [7 8 9]
# 有两种方式可以访问单一元素
print(arr2d[2][1])  # 8
print(arr2d[2, 1])  # 8

# 二维数组的索引方式
# 对于多维数组，如果省略后面的索引，返回的将是一个低纬度的多维数组。例如，一个2 x 2 x 3数组
arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(arr3d)

print(arr3d[0])
# [[1 2 3]
#  [4 5 6]]
old_values = arr3d[0].copy()
arr3d[0] = 42
print(arr3d)
# [[[42 42 42]
#   [42 42 42]]
#
#  [[ 7  8  9]
#   [10 11 12]]]
arr3d[0] = old_values
print(arr3d)
# [[[ 1  2  3]
#   [ 4  5  6]]
#
#  [[ 7  8  9]
#   [10 11 12]]]

print(arr3d[1, 0])  # [7 8 9]



print("13，数组的索引和切片2".center(100, "-"))
# 高维对象可以在一个或多个轴上进行切片，也可以跟整数索引混合使用
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[:2])
# [[1 2 3]
#  [4 5 6]]

# 可以一次传入多个切片，就像传入多个索引那样
print(arr2d[:2, 1:])
# [[2 3]
#  [5 6]]

# 只有冒号表示选取整个轴
print(arr2d[:, :1])
# [[1]
#  [4]
#  [7]]

# 对切片表达式的赋值操作也会扩散到整个选区
arr2d[:2, 1:] = 0
print(arr2d)
# [[1 0 0]
#  [4 0 0]
#  [7 8 9]]


print("14，布尔型索引".center(100, "-"))
# 假设我们有一个用于存储数据的数组以及一个存储姓名的数组（含有重复项）
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
print(names)
data = np.random.randn(7, 4)
print(data)
# [[-2.34855984  0.60140943  0.88565013  0.30843226]
#  [-0.52308663 -1.12606964 -2.12439878 -0.02875487]
#  [ 0.88405453  0.68538785 -0.36494087  0.50133198]
#  [ 0.50277154 -0.45819724 -0.071283   -1.29432949]
#  [-0.35414704 -2.00963552 -1.42991937 -1.02512503]
#  [ 0.69890024  0.08899635 -0.4599453  -0.18272094]
#  [ 0.29821388 -0.44016851  0.60537766  0.64073442]]
# 假设每个名字对应data数组中的一行，我们想要选出对应于名字'Bob'的所有行。
# 和算术运算一样，数组的比较运算（如==）也是矢量化的。因此，对names和字符串“Bob”的比较运算会产生一个布尔型数组
print(names == 'Bob')  # [ True False False  True False False False]
print(data[names == 'Bob'])
# [[-2.34855984  0.60140943  0.88565013  0.30843226]
#  [ 0.50277154 -0.45819724 -0.071283   -1.29432949]]

# 布尔型数组的长度必须跟被索引的轴长度一致。还可以将布尔型数组跟切片、整数（或整数序列）混合使用
print(data[names == 'Bob', 2:])
# [[0.88565013  0.30843226]
#  [-0.071283   -1.29432949]]
print(data[names == 'Bob', 3])  # [0.30843226 -1.29432949]

# 选中除了'Bob'外的所有行，可以用!=或者~
print(names != 'Bob')  # [False  True  True False  True  True  True]
print(data[~(names == 'Bob')])
# [[-0.52308663 -1.12606964 -2.12439878 -0.02875487]
#  [ 0.88405453  0.68538785 -0.36494087  0.50133198]
#  [-0.35414704 -2.00963552 -1.42991937 -1.02512503]
#  [ 0.69890024  0.08899635 -0.4599453  -0.18272094]
#  [ 0.29821388 -0.44016851  0.60537766  0.64073442]]

# 选取两个需要组合应用多个布尔条件，如&（与）、|（或）之类的布尔运算符。
mask = (names == 'Bob') | (names == 'Will')
print(mask)  # [ True False  True  True  True False False]
print(data[mask])

# 通过布尔型索引选取数组中的数据，总是创建数据的副本，即使返回一摸一样的数组也是如此。
# 通过布尔型数组设置值是一种常用手段，为了将data中的所有负值设置为0，只需：
data[data<0] = 0
print(data)
# [[0.         1.56369405 1.11394279 0.        ]
#  [0.         0.         1.28624161 0.        ]
#  [0.38986112 0.57910395 0.         0.        ]
#  [0.         0.45989738 0.         0.        ]
#  [0.08456205 0.         0.         0.67110231]
#  [1.02876436 0.49500124 1.92055802 0.        ]
#  [1.47424771 1.53172034 1.62923524 0.        ]]

# 通过一维布尔数组设置整行或列的值也很简单
data[names != 'Joe'] = 7
print(data)
# [[7.         7.         7.         7.        ]
#  [0.11025506 0.         0.02535764 0.68250182]
#  [7.         7.         7.         7.        ]
#  [7.         7.         7.         7.        ]
#  [7.         7.         7.         7.        ]
#  [0.         0.02585592 0.         0.19849679]
#  [0.         0.         0.         1.02212549]]


print("15，花式索引是一个NumPy术语，它指的是利用整数数组进行索引。".center(100, "-"))
# 花式索引跟切片不同，总是将数据复制到新数组中。
arr = np.empty((8, 4))
for i in range(8):
    arr[i] = i
print(arr)
# [[0. 0. 0. 0.]
#  [1. 1. 1. 1.]
#  [2. 2. 2. 2.]
#  [3. 3. 3. 3.]
#  [4. 4. 4. 4.]
#  [5. 5. 5. 5.]
#  [6. 6. 6. 6.]
#  [7. 7. 7. 7.]]

# 为了以特定顺序选取子集，只需传入一个指定顺序的整数列表或ndarray即可
print(arr[[4, 3, 0, 6]])
# [[4. 4. 4. 4.]
#  [3. 3. 3. 3.]
#  [0. 0. 0. 0.]
#  [6. 6. 6. 6.]]

# 使用负数索引将从末尾开始选行
print(arr[[-3, -5, -7]])
# [[5. 5. 5. 5.]
#  [3. 3. 3. 3.]
#  [1. 1. 1. 1.]]

# 一次传入多个索引数组会有一点特别。其返回的是一个一维数组（如：[1, 5, 7, 2]），其中的元素对应各个索引元组（如：[0, 3, 1, 2]）
arr = np.arange(32).reshape((8, 4))
print(arr)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]
#  [12 13 14 15]
#  [16 17 18 19]
#  [20 21 22 23]
#  [24 25 26 27]
#  [28 29 30 31]]
print(arr[[1, 5, 7, 2], [0, 3, 1, 2]])  # [ 4 23 29 10]  //不论数组有多少维，花式索引的结果总是一维。

# 选取矩阵的行列子集,任意排列
# 将每一行元素，按照[0, 3, 1, 2]顺序配列
print(arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]])
# [[ 4  7  5  6]
#  [20 23 21 22]
#  [28 31 29 30]
#  [ 8 11  9 10]]
# 分析：先从arr中选出[1, 5, 7, 2]这四行，然后[:, [0, 3, 1, 2]]表示选中所有行，但是列的顺序要按0,3,1,2来排。


print("16，数组转置和轴对换".center(100, "-"))
# 转置是重塑的一种特殊形式，其返回源数据的视图（不会进行任何复制操作）。有两种方式，一是transpose方法，二是T属性。
arr = np.arange(15).reshape((3, 5))
print(arr)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]]
print(arr.T)
# [[ 0  5 10]
#  [ 1  6 11]
#  [ 2  7 12]
#  [ 3  8 13]
#  [ 4  9 14]]


# arr = np.random.randn(6,3)
# print(arr)
# print(np.dot(arr.T,arr))

# 对于高维数组，transpose需要得到一个由轴编号组成的元组才能对这些轴进行转置（比较费查克拉）
# 分析：https://blog.csdn.net/weixin_42229626/article/details/81700977
# 原理：一级元素2个（arr[0], arr[1]），二级元素4个(arr[0][0],arr[0][1],arr[1][0],arr[1][1])，三级元素16个(arr[0][0][0],arr[0][0][1]...)。
# 也就是说 每个最基层的元素都可以用 3个数字来表达..用一个元祖来表现就是 (X,Y,Z)
# 对每一个基层元素的元祖表达式,即:(X,Y,Z)进行转置.
# 转置方式为:(0,1,2) >>> (1,0,2)
# 也就是每一个元素都是 (X,Y,Z) >>> (Y,X,Z)
arr = np.arange(16).reshape((2, 2, 4))
print(arr)
# [[[ 0  1  2  3]
#   [ 4  5  6  7]]
#
#  [[ 8  9 10 11]
#   [12 13 14 15]]]
print(arr.transpose((1, 0, 2)))
# [[[ 0  1  2  3]
#   [ 8  9 10 11]]
#
#  [[ 4  5  6  7]
#   [12 13 14 15]]]
print(arr.transpose((0, 2, 1)))
# [[[ 0  4]
#   [ 1  5]
#   [ 2  6]
#   [ 3  7]]
#
#  [[ 8 12]
#   [ 9 13]
#   [10 14]
#   [11 15]]]
print(arr.transpose((2, 1, 0)))
# [[[ 0  8]
#   [ 4 12]]
#
#  [[ 1  9]
#   [ 5 13]]
#
#  [[ 2 10]
#   [ 6 14]]
#
#  [[ 3 11]
#   [ 7 15]]]
print(arr.transpose((2, 0, 1)))
# [[[ 0  4]
#   [ 8 12]]
#
#  [[ 1  5]
#   [ 9 13]]
#
#  [[ 2  6]
#   [10 14]]
#
#  [[ 3  7]
#   [11 15]]]


print("17, swapaxes方法，需要接受一对轴编号".center(100, "-"))
# swapaxes也是返回数据的视图（不会进行任何复制操作）。
print(arr.swapaxes(1, 2))  # 等同于 print(arr.transpose((0, 2, 1)))
# [[[ 0  4]
#   [ 1  5]
#   [ 2  6]
#   [ 3  7]]
#
#  [[ 8 12]
#   [ 9 13]
#   [10 14]
#   [11 15]]]

print(arr)


# print("8，随机生成N行M列的二维数组".center(100, "-"))
# arr = np.random.rand(4, 4)
# # [[0.50398151 0.49137049 0.57337883 0.8637965 ]
# #  [0.45352152 0.02176194 0.09520183 0.86945503]
# #  [0.56745522 0.65480827 0.02221036 0.90495728]
# #  [0.70681986 0.19456123 0.5346386  0.95599382]]
# print(arr)

print("18, ones_like(数组)".center(100, "-"))
arr = np.arange(6)  # array([0, 1, 2, 3, 4, 5])
print(np.ones_like(arr))  # array([1, 1, 1, 1, 1, 1])



ary = np.arange(27).reshape(3,3,3)
print(ary)
print(ary[...,2])


a, *b, c = range(1, 11)
print(*b)


l = [[1, 2, 3], [4, 5, 6,333], (9,5), {"abc":123},"jinhao",str(66),[7, 8, 9]]
flattened = [e for sublist in l for e in sublist]
print(flattened)

# l = [[1, 2, 3], [4, 5, 6,333]]
l = [[[1, 2, 3], [4, 5, 6,333]]]
print(sum(l, []))


nums = [1, 3, 7]
print(sum(nums))



