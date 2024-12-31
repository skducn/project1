# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-26
# Description   : Logging 日志模块
# python中logging日志模块详解， https://www.cnblogs.com/xianyulouie/p/11041777.html
# *********************************************************************

from PO.LogPO2 import *
Log_PO2 = LogPO2("./LogPO2.log")


# 程序的主要部分
def main():
    try:
        Log_PO2.logger.info('Program started')
        # 模拟程序运行
        while True:
            # 每隔一段时间执行一些操作
            sleep(2)
            Log_PO2.logger.info("666")
            print(123)

    except Exception as e:
        Log_PO2.logger.error('An error occurred: {}'.format(e))
        sys.exit(1)


main()