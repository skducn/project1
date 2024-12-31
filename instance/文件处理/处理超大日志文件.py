# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: Generator
# http://www.51testing.com/html/51/n-7803751.html
# Generator 的工作原理: 当调用一个生成器函数时，它并不会立即执行函数体，而是返回一个生成器对象。只有在实际请求下一个值时，它才会执行到下一个 yield 语句。
# 　　·节省内存：不需要等待全部内容生成完毕
# 　　· 实时响应：用户可以立即看到部分结果
# 　　· 可中断：如果用户不需要更多结果，可以随时停止

# 　　高级用法：Generator 表达式和的双向通信 send 的魔法

# *****************************************************************

def read_log_file(filename):
    with open(filename) as f:
        for line in f:
            if "ERROR" in line:
                yield line


# # 使用方式
# # 无论日志文件多大，内存占用都很小。
# for error in read_log_file("huge.log"):
#     # process_error(error)
#     print(error)

# *****************************************************************
#
# def counter():
#     print("Starting")
#     i = 0
#     while True:
#         print(f"Generating {i}")
#         yield i  # 类似于return i
#         i += 1
#
# # 创建生成器对象
# c = counter()  # 此时不会打印任何内容
# print("Generator created")
#
# # 获取前三个值
# print(next(c))  # 打印 "Starting" 和 "Generating 0"，返回 0
# print(next(c))  # 打印 "Generating 1"，返回 1
# print(next(c))  # 打印 "Generating 2"，返回 2

# *****************************************************************

def averager():
    total = 0
    count = 0
    average = None
    while True:
        # yield 在这里扮演双重角色：
        # 1. 向外返回 average 值 , 类似于return average
        # 2. 接收外部发送的 value
        value = yield average
        if value is None:
            break
        total += value
        count += 1
        average = total / count

avg = averager()          # 创建生成器对象，但函数体还未开始执行

# 启动生成器，运行到第一个 yield，返回 None
next(avg)

print("第二步：生成器已启动，等待第一个值")
print(avg.send(10))      # 1. send(10) 将 10 传给 value
                         # 2. 计算 average = 10/1 = 10.0
                         # 3. 到达 yield，返回 10.0
                         # 4. 生成器暂停，等待下一个值
print(avg.send(20))      # 1. value 获得值 20
                         # 2. 计算 average = 30/2 = 15.0
                         # 3. yield 返回 15.0
print(avg.send(30))      # 1. value 获得值 30
                         # 2. 计算 average = 60/3 = 20.0
                         # 3. yield 返回 20.0