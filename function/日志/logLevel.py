# coding: utf-8
# ***************************************************************
# Author     : John
# Date       : 2023-12-29
# Description: logging 日志模块
# https://zhuanlan.zhihu.com/p/476549020
# logging模块的主要组成部分分为Logger、Handler和Formatter三个部分。
# - Logger：用于记录日志消息的对象，可以定义多个Logger，每个Logger可以绑定多个Handler。
# - Handler：用于将Logger产生的日志消息输出到指定的位置，可以将日志信息输出到文件、屏幕、邮件等。
# - Formatter：用于设置输出日志消息的格式，可以定义不同的格式。

# todo basicConfig()方法进行基本配置
# filename参数，用于设置输出到的文件名。日志信息将会输出到指定的文件中。否则默认控制台输出
# level参数设置了日志级别，只有高于该级别的日志才会输出；
# format参数设置了日志输出的格式；
# datefmt参数设置了日志输出的日期格式。

# 严重程度的级别依次是DEBUG<INFO<WARNING<ERROR<CRITICAL
# ***************************************************************

import logging
logging.warning('3333')  # //输出3333
logging.info('I told you so')  # //不打印
logging.debug(' you so')  # //不打印
logging.error(' 4444')  # 输出4444
logging.critical(' 5555')  # 输出5555