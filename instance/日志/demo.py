# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description: 当程序中断时，将日志保存到app.log
# 参考zyjk - chc - web - changning的main()
# *****************************************************************

import signal
import sys
import logging
from time import sleep

# 配置日志
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# 定义信号处理函数
def handle_signal(signum, frame):
    logger.info('Received signal: {}'.format(signal.Signals(signum).name))
    logger.info('Program is terminating...')
    # 在这里可以添加额外的清理代码或日志记录
    sys.exit(0)


# 注册信号处理函数
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


# 程序的主要部分
def main():
    try:
        logger.info('Program started')
        # 模拟程序运行
        while True:
            # 每隔一段时间执行一些操作
            sleep(2)
            logger.info(123)
            print(123)

    except Exception as e:
        logger.error('An error occurred: {}'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()












