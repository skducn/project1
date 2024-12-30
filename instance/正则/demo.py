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

import re

# 字符串前加上字母r以表示这是一个原始字符串（raw string），这样可以避免反斜杠转义问题。
email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

matches = re.findall(email_pattern, "Contact us at support@example.com or sales@company.org")
print(matches)  # ['support@example.com', 'sales@company.org']

# match 匹配以Hello开头的字符串，匹配到返回1，否则返回0
result = re.match(r"Hello", "Hello world!")
if result:
    print(1)
else:
    print(0)

# search 匹配整个字符串中是否包含world，匹配到返回1，否则返回0
result = re.search(r"world", "Hello world!")
if result:
    print(1)
else:
    print(0)

# sub 将匹配到的内容替换为指定的新字符串
new_text = re.sub(r"\d+", "number", "There are 123 apples and 456 oranges.")
print(new_text)  # There are number apples and number oranges.

# split 按照匹配的模式分割字符串，并返回一个列表
words = re.split(r"\W+", "Hello, how are you?")
words = re.split(r"\W+", "你好，你怎么样？")  # ['你好', '你怎么样', '']
print(words)  # ['Hello', 'how', 'are', 'you', '']

# 为了提高性能，特别是当你多次使用同一个正则表达式时，你可以先编译它
compiled_pattern = re.compile(email_pattern)
matches = compiled_pattern.findall("Contact us at support@example.com or sales@company.org")
print(matches)  # ['support@example.com', 'sales@company.org']


# 使用标志（Flags）
# 不区分大小写
case_insensitive_match = re.search("hello", "Hello World!", flags=re.IGNORECASE)
if case_insensitive_match:
    print(case_insensitive_match.group())
else:
    print(0)










