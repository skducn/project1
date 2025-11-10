# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-11-15
# Description: 压缩与解压
# 十个 Python文件压缩与解压实战技巧 http://www.51testing.com/html/43/n-7803343.html
# 通用的压缩和解压缩函数
# 在处理未知压缩类型时，可以利用第三方库如patool自动识别并操作压缩文件。
# pip3 install patool
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import patoolib


# 压缩zip，注意zip文件不能存咋
# patoolib.create_archive('/Users/linghuchong/Downloads/51/Python/project/PO/zip/example1.zip', ['readme.ini','zip.py'])

# 解压zip
# patoolib.extract_archive('/Users/linghuchong/Downloads/51/Python/project/PO/zip/example1.zip', outdir='/Users/linghuchong/Downloads/51/Python/project/PO/2/')
