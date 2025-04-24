# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-5-25
# Description: map(function，iterable) 函数式编程工具
# https://www.cnblogs.com/lincappu/p/8179475.html
# map() 是 Python 内置的高阶函数，它可以对一个可迭代对象（如列表）中的每个元素执行某个操作，返回一个新的迭代器。简单来说，就是“批量处理”。
# map() 不改变原有的 list，返回一个新的 list。
# python3中map()返回iterators类型
# 迭代器：range(5)，map(str, '5678')，filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])
# ********************************************************************************************************************

# todo map

print("1，生成0-4的倍数".center(100, "-"))
print(list(map(lambda x: x ** 2, range(5))))  # [0,1,4,9,16]

print("2，元素的大小写处理，如首字母大写，其余字母小写，全部大写".center(100, "-"))
# 元素首字母大写，其余字母小写
print(list(map(lambda s:s[0:1].upper() + s[1:].lower(), ['adam', 'LISA', 'barT'])))  # ['Adam', 'Lisa', 'Bart']
# # 去掉多余空格并转为大写+！
print([f"{word.upper()}!" for word in map(str.strip, ['   apple', 'banana  ', '   cherry   '])])  # ['APPLE!', 'BANANA!', 'CHERRY!']
# # 去掉多余空格并转为小写
print(list(map(lambda x: x.strip().lower(), [" Hello ", "WORLD! ", " Python ", "123", ""])))  # ['hello', 'world!', 'python', '123', '']




print("3, 将列表里的数字型字符串转换成int/float/str".center(100, "-"))
print(list(map(int, ['1', '2', '3', 444])))  # [1, 2, 3, 444]
print(list(map(float, ['1', '2', '0.03', 444])))  # [1.0, 2.0, 0.03, 444.0]
print(list(map(str, ['1', '2', '0.03', 444])))  # ['1', '2', '0.03', '444']

print("4，对列表里的值求绝对值".center(100, "-"))
print(list(map(abs, [-1, 2, -5])))  # [1, 2, 5]

print("5，将字符串打散成列表".center(100, "-"))
list1 = []
for i in map(str, '5678'):
    list1.append(i*2)
print(list1)  # ['55', '66', '77', '88']
print(list(map(str, '5678')))  # ['5', '6', '7', '8']

print("6，获取列表中偶数的平方".center(100, "-"))
filtered = filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])  # 就是x除以2余数为0 ,代表能被2整除
# print(filtered)  # <filter object at 0x7f9aec478be0>
squared = list(map(lambda x: x**2, filtered))
print(squared)  # [4, 16]

print("7，处理多个可迭代对象".center(100, "-"))
# 将两个列表中的对应元素相加
print(list(map(lambda x, y: x + y, [1, 2, 3], [4, 5, 6]))) # [5, 7, 9]
# 将两个列表中的对应元素开平方
print(list(map(lambda x, y: x**y, [3, 4, 5], [1, 2, 2])))  # 3，16，25

# ********************************************************************************************************************
# filter() 是 Python 中一个非常实用的内置函数，用来过滤序列中的元素。它接收两个参数：一个是函数（用于判断条件），另一个是可迭代对象。只有满足条件的元素才会被保留下来。
# todo filter

print("filter1，筛选出其中的所有偶数".center(100, "-"))
print(list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])))  # [2, 4, 6]
print([x**2 for x in filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6])])  # [4, 16, 36]

print("filter2，从字符串列表中筛选出长度大于 5 的单词".center(100, "-"))
print(list(filter(lambda word: len(word) > 5, ["apple", "banana", "cherry", "date", "fig"])))  # ['banana', 'cherry']

print("filter3，过滤掉空字符串".center(100, "-"))
print(list(filter(None, [" Hello ", "WORLD! ", " Python ", "123", "", None])))  # [' Hello ', 'WORLD! ', ' Python ', '123']

# ********************************************************************************************************************
# todo reduce
# 基本逻辑是：从左到右依次对序列中的元素进行累积操作。
# reduce 不仅能完成基础的累加、累乘，还能应对各种复杂场景。

from functools import reduce, partial

print("reduce1，列表里元素求和".center(100, "-"))
print(reduce(lambda x, y: x + y, [1,2,3], 0))  # 6    //0是初始值，为了解决如果输入列表为空，reduce 默认会报错。

print("reduce2，字符串拼接,将列表所有元素拼接起来".center(100, "-"))
print(reduce(lambda x, y: f"{x}_{y}", ["apple", "banana", "cherry"]))  # apple_banana_cherry

print("reduce3, partial为函数预先填充部分参数".center(100, "-"))
# functools.partial 是一个强大的工具，可以为函数预先填充部分参数。结合 reduce，可以让代码更加简洁和高效！来看个例子：
def add(x, y, z):
    return x + y + z

# 使用partial固定z的值
add_with_z = partial(add, z=10)

# 使用reduce计算列表求和，并加上固定的z值
result = reduce(add_with_z, [1, 2, 3, 4])
print(result)  # 输出: 40

# reduce 函数的工作原理是：先从序列 [1, 2, 3, 4] 中取出前两个元素 1 和 2，调用 add_with_z(1, 2)，也就是 add(1, 2, 10)，得到结果 13；
# 接着将这个结果 13 与序列中的下一个元素 3 作为参数再次调用 add_with_z，即 add_with_z(13, 3)，也就是 add(13, 3, 10)，得到结果 26；
# 再将 26 与序列中的下一个元素 4 作为参数调用 add_with_z，即 add_with_z(26, 4)，也就是 add(26, 4, 10)，最终得到结果 40。

print("reduce4，计算词频".center(100, "-"))
words = ['hello', 'world', 'hello', 'python', 'world']
# 使用 reduce 计算词频
print(reduce(lambda d, w: {**d, w: d.get(w, 0) + 1}, words, {}))  # {'hello': 2, 'world': 2, 'python': 1}
# 工作原理是:
# 第一次迭代
# 从列表 words 中取出第一个单词 'hello'。
# 此时 d 是初始值空字典 {}，w 是 'hello'。
# 执行匿名函数 {**d, w: d.get(w, 0) + 1}：
# d.get(w, 0) 尝试从字典 d 中获取键 w 对应的值，如果键不存在则返回 0。由于 d 是空字典，所以 d.get('hello', 0) 返回 0。
# d.get(w, 0) + 1 就是 0 + 1 = 1。
# {**d, w: d.get(w, 0) + 1} 会将 w 作为键，1 作为值添加到字典 d 中，得到 {'hello': 1}。
# 第二次迭代
# 从列表 words 中取出第二个单词 'world'。
# 此时 d 是上一次迭代得到的字典 {'hello': 1}，w 是 'world'。
# 执行匿名函数 {**d, w: d.get(w, 0) + 1}：
# d.get('world', 0) 返回 0，因为字典 d 中没有 'world' 这个键。
# d.get(w, 0) + 1 就是 0 + 1 = 1。
# {**d, w: d.get(w, 0) + 1} 会将 'world' 作为键，1 作为值添加到字典 d 中，得到 {'hello': 1, 'world': 1}。
# 第三次迭代
# 从列表 words 中取出第三个单词 'hello'。
# 此时 d 是上一次迭代得到的字典 {'hello': 1, 'world': 1}，w 是 'hello'。
# 执行匿名函数 {**d, w: d.get(w, 0) + 1}：
# d.get('hello', 0) 返回 1，因为字典 d 中 'hello' 键对应的值是 1。
# d.get(w, 0) + 1 就是 1 + 1 = 2。
# {**d, w: d.get(w, 0) + 1} 会更新字典 d 中 'hello' 键对应的值为 2，得到 {'hello': 2, 'world': 1}。
# 第四次迭代
# 从列表 words 中取出第四个单词 'python'。
# 此时 d 是上一次迭代得到的字典 {'hello': 2, 'world': 1}，w 是 'python'。
# 执行匿名函数 {**d, w: d.get(w, 0) + 1}：
# d.get('python', 0) 返回 0，因为字典 d 中没有 'python' 这个键。
# d.get(w, 0) + 1 就是 0 + 1 = 1。
# {**d, w: d.get(w, 0) + 1} 会将 'python' 作为键，1 作为值添加到字典 d 中，得到 {'hello': 2, 'world': 1, 'python': 1}。
# 第五次迭代
# 从列表 words 中取出第五个单词 'world'。
# 此时 d 是上一次迭代得到的字典 {'hello': 2, 'world': 1, 'python': 1}，w 是 'world'。
# 执行匿名函数 {**d, w: d.get(w, 0) + 1}：
# d.get('world', 0) 返回 1，因为字典 d 中 'world' 键对应的值是 1。
# d.get(w, 0) + 1 就是 1 + 1 = 2。
# {**d, w: d.get(w, 0) + 1} 会更新字典 d 中 'world' 键对应的值为 2，得到 {'hello': 2, 'world': 2, 'python': 1}。

# ********************************************************************************************************************
#todo 使用生成器表达式替代列表推导式

# 当我们用map或filter处理大数据时，内存占用可能是个问题。这时候可以使用生成器表达式来节省内存！生成器只在需要时生成值，内存占用更小！
# 假设我们有一个超大的数据集
data = range(1000000)
# 使用生成器表达式代替列表推导式
result = map(lambda x: x * 2, (x for x in data if x % 2 == 0))
# 输出前10个结果
print(list(result)[:10])  # [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]



