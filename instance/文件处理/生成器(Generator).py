# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: Python生成器(Generator)的概念和应用
# http://www.51testing.com/html/51/n-7803751.html
# Generator 的工作原理:
# 当调用一个生成器函数时，它并不会立即执行函数体，而是返回一个生成器对象。
# 只有在实际请求下一个值时，它才会执行到下一个 yield 语句。
# 　　·节省内存：不需要等待全部内容生成完毕
# 　　· 实时响应：用户可以立即看到部分结果
# 　　· 可中断：如果用户不需要更多结果，可以随时停止
# 　　高级用法：Generator 表达式和的双向通信 send 的魔法
# 1. 内存效率
# 适用场景：处理大型数据集、日志文件分析、数据流处理
# 优势：不需要将所有数据加载到内存中
# 2. 实时处理
# 适用场景：实时数据监控、传感器数据处理、网络数据流
# 优势：可以边生成边处理，实时响应
# 3. 惰性求值
# 适用场景：数学序列计算、数据管道处理、复杂计算优化
# 优势：只在需要时计算值，避免不必要的计算
# 4. 状态保持
# 适用场景：状态机实现、迭代算法、累积计算
# 优势：生成器函数可以保持内部状态，暂停和恢复执行
# 这些特性使得生成器成为Python中处理大数据、实现迭代器模式和构建高效数据处理管道的重要工具。
# *****************************************************************

# todo 1. 基础生成器函数 - 处理大文件
# 这是一个生成器函数，用于逐行读取日志文件
# 只有遇到包含"ERROR"的行才通过 yield 返回
# 不会将整个文件加载到内存中，节省内存空间
def read_log_file(filename):
    with open(filename) as f:
        for line in f:
            if "ERROR" in line:
                yield line


# 无论日志文件多大，内存占用都很小。
def process_error_logs(log_file):
    error_count = 0
    for error_line in read_log_file(log_file):
        print(f"发现错误: {error_line.strip()}")
        error_count += 1
    print(f"总共发现 {error_count} 个错误")

# 使用方式
# process_error_logs("application.log")

# *****************************************************************

# todo 2. 无限序列生成器
# 创建一个无限计数器生成器
# 每次调用 next() 或在for循环中使用时，返回下一个数字
# 函数在 yield 处暂停，下次调用时从暂停处继续执行
def counter():
    print("Starting")
    i = 0
    while True:
        print(f"Generating {i}")
        yield i  # 类似于return i
        i += 1

# 创建生成器对象
c = counter()
print("Generator created")

# 获取前三个值
print(next(c))  # 打印 "Starting" 和 "Generating 0"，返回 0
print(next(c))  # 打印 "Generating 1"，返回 1
print(next(c))  # 打印 "Generating 2"，返回 2


# 实际使用示例
def get_first_n_even_numbers(n):
    count = 0
    for num in counter():
        if num % 2 == 0:  # 偶数
            yield num
            count += 1
            if count >= n:
                break

# 获取前5个偶数
even_numbers = list(get_first_n_even_numbers(5))
print(even_numbers)  # [0, 2, 4, 6, 8]
# *****************************************************************

# todo 3. 双向通信生成器 - 平均值计算器
# 这是一个可以接收外部值的生成器
# yield 不仅返回值，还能接收通过 send() 方法发送的值
# 实现了动态计算平均值的功能
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

print("生成器已启动，等待第一个值")
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