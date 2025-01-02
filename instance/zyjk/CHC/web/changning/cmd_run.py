# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-12-27
# Description: 社区健康管理中心 - 新泾镇社区卫生服务中心，执行自动上报
# 功能：程序运行时，如遇到中断或control+c时，将日志记录到logPO4.log中
# 执行main主程序，设置logPO4.log日志（info），将主程序main中需要记录的内容设置为 self.logger.info(XX), 当程序中断或control+c时，将日志记录到logPO4.log中

# python cmd_run.py 小猴子，小茄子
# 执行上报
#***************************************************************
import sys
sys.path.append("../../../../..")

from ChcWebPO import *
ChcWeb_PO = ChcWebPO("./LogPO4.log")

from multiprocessing import Pool, cpu_count
import time


def p_runTest(param):
    return ChcWeb_PO.runTest(param)


l_param = []
if "，" in sys.argv[1]:
    l_param = sys.argv[1].split("，")
else:
    l_param.append(sys.argv[1])
# print(l_param)


def main():
    try:
        time1 = time.time()

        # 获取cpu核数
        print("CPU cores: ", cpu_count())
        with Pool(cpu_count()) as pool:
            pool.map(p_runTest, l_param)

        time2 = time.time()
        pool.close()
        pool.join()
        print('总共耗时：' + str(int(time2 - time1)) + 's')

    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":

    main()










