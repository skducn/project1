# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: # textwrap 调整换行符的位置来格式化文本
# __all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
# 官网：https://docs.python.org/zh-cn/3.8/library/textwrap.html
# 学习：https://www.cnblogs.com/wj5633/p/6931187.html
# 学习：https://blog.csdn.net/zwbzwbzwbzwbzwbzwb/article/details/52824154
# *****************************************************************
import sys
sys.path.append("./")
from PO.StrPO import *
Str_PO = StrPO()
print(Str_PO.isChinese("测试"))  # True //字符串全部是中文

d = {
 "diastolicBloodPressure": 91,
 "heartRate": 66,
 "measurementDate": "2021-03-23 17:01",
 "systolicPressure": 121,
 "id": ""
}

print(d)
#
# # #!/usr/bin/python
# # # -*- coding: UTF-8 -*-
# # import sys
# # sys.path.append("C:\MySoftware\Automagica2.0\pkgs")
#
# #引入automagica 模块
# from automagica import *
# #引入selenium 模块
# from selenium import webdriver
#
# #创建chrome浏览器实例，跳转到百度首页
# #browser = Chrome()
# browser = webdriver.Chrome()
# browser.get('https://baidu.com/')
# #获取搜索输入框，嵌入关键字automagica
# search_input = browser.find_element_by_name('wd')
# search_input.send_keys("automagica")
# #获取检索按钮，点击
# search_btn = browser.find_element_by_id('su')
# search_btn.click()
#
# #
# # from pyzbar.pyzbar import decode
# # from PIL import Image
# # path = "1.png"
# # img = Image.open(path)
# # bar = decode(img)[0]
# # result = bar.data.decode()
# # print(result)
#
#
# # import redis
# # r1=redis.Redis(host='192.168.0.213', password='', port=6379, db=0, decode_responses=False)
# # for i in r1.keys():
# #     if len(i) == 32:
# #         s2 = str(i, encoding="utf-8")
# #         break
# # print(s2)
#
#
#
#
#
#
# # import textwrap
# #
# # text = """abcdefg
# # hijklmn
# # opqrstuvwxyz
# # """
# #
# # # todo: fill() 调整换行符,每行显示给定宽度，注意下一行前会有空格
# # print("fill() 调整换行符,每行显示给定宽度".center(100, "-"))
# # print(textwrap.fill(text, width=6))
# # # abcdef
# # # g hijk
# # # lmn op
# # # qrstuv
# # # wxyz
# #
# #
# # # todo:dedent() 去除缩进
# # print("dedent()去除缩进".center(100, "-"))
# # sample_text = '''    aaabbb    cccddd'''
# # print(textwrap.dedent(sample_text))
# # # aaabbb    cccddd
# #
# #
# # # todo:indent() 给定前缀
# # print(":indent() 给定前缀".center(100, "-"))
# # print(textwrap.indent(text, prefix='----'))
# # # ----abcdefg
# # # ----hijklmn
# # # ----opqrstuvwxyz
# # s = 'hello\n\n \nworld'
# #
# # # 默认忽略空白符（包括任何行结束符）组成的行（\n）
# # print(textwrap.indent(s, '+ '))
# # # + hello
# # #
# # # + world
# #
# # # 函数对象 = lambda 参数：表达式
# # print(textwrap.indent(s, '+ ', lambda line: True))
# # # + hello
# # # +
# # # +
# # # + world
# #
# #
# # # todo:首行缩进，其余行添加前缀22，每行限制字符10个。
# # print("首行缩进，其余行添加前缀22，每行限制字符10个。".center(100, "-"))
# # # subsequent_indent:初始化除了第一行的所有行
# # detent_text = textwrap.dedent(text).strip()
# # print(textwrap.fill(detent_text, initial_indent='  ', subsequent_indent='22', width=10))
# # #   abcdefg
# # # 22hijklmn
# # # 22opqrstuv
# # # 22wxyz
# #
# #
# # # todo:shorten() 多余的省略号
# # print("shorten() 多余的省略号".center(100, "-"))
# # print(textwrap.shorten(text, width=20))
# # # abcdefg [...]
# # print(textwrap.shorten("Hello world", width=10, placeholder="..."))
# # # Hello...
# #
# # # todo:wrap() 将一个字符串按照width的宽度进行切割，切割后返回list
# # print("wrap() 将一个字符串按照width的宽度进行切割，切割后返回list".center(100, "-"))
# # print(textwrap.wrap(text, width=10))
# # # ['abcdefg', 'hijklmn op', 'qrstuvwxyz']
# # # 分析：结果并不是保证了每个list元素都是按照width的，因为不但要考虑到width，也要考虑到空格（换行），也就是一个单词。
# #
# # sample_text = 'aaabbbcccdddeeeedddddfffffggggghhhhhhkkkkkkk'
# # print(textwrap.wrap(sample_text, width=5))
# # # ['aaabb', 'bcccd', 'ddeee', 'edddd', 'dffff', 'fgggg', 'ghhhh', 'hhkkk', 'kkkk']
# #
# #
# # print("定义 类与实例 textwrap.TextWrapper(…)".center(100, "-"))
# # # 类与实例 textwrap.TextWrapper(…) # 这个类的构造函数接受一系列的关键字参数来初始化自己的属性信息
# # sample_text = '''aaa'''
# # textWrap = textwrap.TextWrapper()
# # textWrap.initial_indent = 'bbb'
# # print(textWrap.wrap(sample_text))
# # # ['bbbaaa']
# #
# # sample_text = '''aaa
# # kkk
# # jjj'''
# # textWrap = textwrap.TextWrapper(width = 2)
# # textWrap.initial_indent = 'bbb'
# # textWrap.subsequent_indent = 'ccc'
# # print(textWrap.wrap(sample_text))
# # # ['bbba', 'ccca', 'ccca', 'ccck', 'ccck', 'ccck', 'cccj', 'cccj', 'cccj']
# #
# #
# #
# # a = ["welcome,linuxmi.com,33"]
# # for i in a:
# #     print(i.count(',') + 1)
# #
# #
# # import numpy as np
# # #创建数组
# # a = np.array([2,1,0,5])
# # print(a)
# # print(a[:3])
# # print(a.min())
# # a.sort()
# # b = np.array([1,2,3],[4,5,6])
# print(b*b)