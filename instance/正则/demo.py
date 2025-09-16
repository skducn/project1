# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-12-29
# Description: 正则表达式
# http://www.51testing.com/html/05/n-7803905.html
# 一些常用的元字符（如^, $, ., *, +, ?, {m,n}, [], (), |）以及特殊序列（如\d, \s, \w）对于构建有效的正则表达式至关重要。这些符号赋予了正则表达式强大的灵活性和表达能力。
# 元字符：
# ^：匹配字符串的开头。
# $：匹配字符串的结尾。
# .：匹配除换行符以外的任意字符。
# *：匹配前面的元素零次或多次。
# +：匹配前面的元素一次或多次。
# ?：匹配前面的元素零次或一次。
# *****************************************************************

"""
1，匹配邮箱

"""

import re

# todo findall,匹配邮箱
# 使用 r"" 创建原始字符串（raw string），避免反斜杠 \ 被转义
# email_pattern 是一个用于匹配电子邮件地址的正则表达式模式：
# [a-zA-Z0-9_.+-]+：匹配一个或多个字母、数字、下划线、点、加号或减号字符（邮箱用户名部分）
# @：匹配电子邮件地址中的@符号
# [a-zA-Z0-9-]+：匹配一个或多个字母、数字或减号字符（域名的第一部分）
# \.：匹配点号.（需要转义，因为.在正则表达式中有特殊含义）
# [a-zA-Z0-9-.]+：匹配一个或多个字母、数字、点号或减号字符（顶级域名部分）
email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
matches = re.findall(email_pattern, "Contact us at support@example.com or sales@company.org")
print(matches)  # ['support@example.com', 'sales@company.org']



# todo compile, 可以多次重用
# 使用预编译的对象可以提高性能，特别是当同一个模式被多次使用时
compiled_pattern = re.compile(email_pattern)  # 先编译
matches = compiled_pattern.findall("Contact us at support@example.com or sales@company.org")
print(matches)  # ['support@example.com', 'sales@company.org']


# todo match,匹配以Hello开头的字符串
# re.match() 特点：
# 只在字符串的开始位置进行匹配
# 如果模式在字符串开头匹配成功，返回匹配对象
# 如果不匹配，返回 None
result = re.match(r"Hello", "Hello world!")
print(result)  # <re.Match object; span=(0, 5), match='Hello'>
if result:
    print(1)
else:
    print(0)


# todo search,匹配整个字符串中是否包含world
# re.search()：
# 在整个字符串中搜索模式
# 只要字符串中任何位置匹配就会返回匹配对
result = re.search(r"world", "Hello world!")
if result:
    print(1)
else:
    print(0)


# todo sub,将匹配到的内容替换为指定的新字符串
# \d+：匹配连续的一个或多个数字字符
# re.sub()：全局替换，会替换所有匹配项，不仅仅是第一个
# 原始字符串 r"\d+"：避免反斜杠被Python转义
new_text = re.sub(r"\d+", "number", "There are 123 apples and 456 oranges.")
print(new_text)  # There are number apples and number oranges.



# todo split,按照匹配的模式分割字符串，并返回一个列表
# r"\W+" 是分割模式：
# \W：匹配非单词字符（相当于 [^a-zA-Z0-9_]
# \W+ 匹配一个或多个非单词字符（如空格、标点符号等),
# + 表示匹配前面的元素一次或多次
words = re.split(r"\W+", "Hello, how are you?")  #如果字符串末尾有分隔符，会生成一个空字符串元素，如?
print(words)  # ['Hello', 'how', 'are', 'you', '']
words = re.split(r"\W+", "你好，你怎么样")
print(words)  # ['你好', '你怎么样']




# todo 使用模式匹配的行为方式标志（flags）
# todo re.IGNORECASE 或 re.I：忽略大小写差异
case_insensitive_match = re.search("hello", "Hello World!", flags=re.IGNORECASE)
print(case_insensitive_match)  # <re.Match object; span=(0, 5), match='Hello'>
if case_insensitive_match:
    print(case_insensitive_match.group())
    # 如果匹配成功，使用 group() 方法获取匹配的文本内容
else:
    print(0)

# todo re.MULTILINE 或 re.M：多行模式，改变 ^ 和 $ 的行为
# 解释：MULTILINE 模式使 ^ 匹配每行的开始，$ 匹配每行的结束
text = """第一行内容
第二行内容
第三行内容"""
# 不使用 MULTILINE 标志
# result = re.findall(r"^第.*内容$", text)
# print("不使用 MULTILINE:", result)  # []
# 使用 MULTILINE 标志
result = re.findall(r"^第.*内容$", text, flags=re.MULTILINE)
print("使用 MULTILINE:", result)  # ['第一行内容', '第二行内容', '第三行内容']



# todo re.DOTALL 或 re.S：使 . 匹配包括换行符在内的所有字符
# 解释：DOTALL 模式使 . 能够匹配包括换行符在内的所有字符
text = """这是第一行
这是第二行
这是第三行"""
# 不使用 DOTALL 标志
# result = re.search(r"第一行.*第三行", text)
# print("不使用 DOTALL:", result)  # None
# 使用 DOTALL 标志
result = re.search(r"第一行.*第三行", text, flags=re.DOTALL)
print("使用 DOTALL:", result.group() if result else "无匹配")
# 这是第一行
# 这是第二行
# 这是第三行



# todo re.VERBOSE 或 re.X：详细模式，允许在正则表达式中添加注释和空白
# 解释：VERBOSE 模式允许在正则表达式中添加空白和注释，提高可读性
text = "联系电话: 138-1234-5678"
# 使用 VERBOSE 标志的详细模式
phone_pattern = r"""
    (\d{3})     # 区号：3位数字
    -           # 分隔符：连字符
    (\d{4})     # 前四位数字
    -           # 分隔符：连字符
    (\d{4})     # 后四位数字
"""

# 不使用 VERBOSE 标志会无法匹配（因为有空白和注释）
result = re.search(phone_pattern, text, flags=re.VERBOSE)
if result:
    print("区号:", result.group(1))      # 138
    print("前四位:", result.group(2))    # 1234
    print("后四位:", result.group(3))    # 5678
    print("完整号码:", result.group(0))  # 138-1234-5678









