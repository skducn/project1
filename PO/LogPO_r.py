# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2020-4-26
# Description   : Logging 日志模块
# python中logging日志模块详解， https://www.cnblogs.com/xianyulouie/p/11041777.html
# *********************************************************************

import logging
from logging import handlers

from PO.TimePO import *
Time_PO = TimePO()


class ReverseFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        try:
            msg = self.format(record)
            with open(self.baseFilename, 'r+', encoding=self.encoding) as f:
                content = f.read()
                f.seek(0, 0)
                f.write(msg + '\n' + content)
        except Exception:
            self.handleError(record)


# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 创建 ReverseFileHandler
handler = ReverseFileHandler('app.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)




if __name__ == "__main__":

    # level = warning, 表示只显示level及之后的日志，如：显示 warning, error，critical

    log = LogPO("data/bi_" + Time_PO.getDate() + ".log", level="warning")
    log.logger.debug("debug1") # 不会生成
    log.logger.info("info2")  # 不会生成
    log.logger.warning("警告3")
    log.logger.error("报错4")
    log.logger.critical("严重5")

    # 生成error, critical的日志
    logError = LogPO("data/bi_error" + Time_PO.getDate() + ".log", level="error")
    logError.logger.error("error213123123")
