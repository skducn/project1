# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-26
# Description   : Logging 日志模块
# python中logging日志模块详解， https://www.cnblogs.com/xianyulouie/p/11041777.html
# *********************************************************************

import os, time

from PO.LogPO import *
# _path = os.path.dirname(__file__)  # 获取当前文件路径
Log_PO = LogPO('nohup.out',level="debug")


# 创建方法生成日志
def generation_log():
    for i in range(20):
        # Log_PO.info(i)
        Log_PO.logger.info(i)
        time.sleep(1)


# 读取日志并返回
def red_logs():
    # log_path = f'{_path}/log.log'  # 获取日志文件路径
    log_path = f'nohup.out'  # 获取日志文件路径
    with open(log_path, 'rb') as f:
        # log_size = os.path.getsize(log_path)  # 获取日志大小
        log_size = 100
        offset = -100
        # 如果文件大小为0时返回空
        if log_size == 0:
            return ''
        while True:
            # 判断offset是否大于文件字节数,是则读取所有行,并返回
            if (abs(offset) >= log_size):
                f.seek(-log_size, 2)
                data = f.readlines()
                return data
            # 游标移动倒数的字节数位置
            data = f.readlines()
            # 判断读取到的行数，如果大于1则返回最后一行，否则扩大offset
            if (len(data) > 1):
                return data
            else:
                offset *= 2
