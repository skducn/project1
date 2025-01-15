# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-26
# Description   : Logging 日志模块
# python中logging日志模块详解， https://www.cnblogs.com/xianyulouie/p/11041777.html
# *********************************************************************
import signal
import sys
import logging
from time import sleep

class LogPO2(object):

    def __init__(self, varFile):

        # 配置日志
        logging.basicConfig(filename=varFile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        # logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    # 定义信号处理函数
    def handle_signal(self, signum):
        self.logger.info('Received signal: {}'.format(signal.Signals(signum).name))
        self.logger.info('Program is terminating...')
        # 在这里可以添加额外的清理代码或日志记录
        sys.exit(0)

    # 注册信号处理函数
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)


    # 程序的主要部分
    def main(self):
        try:
            self.logger.info('Program started')
            # 模拟程序运行
            while True:
                # 每隔一段时间执行一些操作
                sleep(2)
                self.logger.info("444")
                print(123)

        except Exception as e:
            self.logger.error('An error occurred: {}'.format(e))
            sys.exit(1)


if __name__ == '__main__':

    Log_PO2 = LogPO2("./tt.log")
    Log_PO2.main()