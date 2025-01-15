# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-12-27
# Description: 社区健康管理中心 - 新泾镇社区卫生服务中心，执行自动上报
# 功能：程序运行时，如遇到中断或control+c时，将日志记录到logPO4.log中
# 执行main主程序，设置logPO4.log日志（info），将主程序main中需要记录的内容设置为 self.logger.info(XX), 当程序中断或control+c时，将日志记录到logPO4.log中
#***************************************************************
from ChcWebPO import *
ChcWeb_PO = ChcWebPO("./LogPO5.log")

from multiprocessing import Pool, cpu_count
import time

# 获取家庭医生列表顺序名单
# print(ChcWeb_PO.getDocTest('lbl', 'HHkk2327447')) # 测试环境  # {'小茄子': 1, '小猴子': 2, '111': 3, '自动化': 4}
# print(ChcWeb_PO.getDoc('xj', '12345678'))

# 获取身份证字典，将身份证保存到文件
# print(ChcWeb_PO.getIdcardTest('lbl', 'HHkk2327447', "小茄子"))  # {'小茄子': {1: ['110101198907071506', '110101201602029686'}}
# print(ChcWeb_PO.getIdcard('xj', '12345678', "小茄子"))

# 执行上报
# ChcWeb_PO.runTest('lbl', 'HHkk2327447', File_PO.jsonfile2dict("小茄子.json"))
# ChcWeb_PO.run('xj', '12345678', File_PO.jsonfile2dict("小茄子.json"))

# 性能分析是识别代码瓶颈的关键步骤
# import cProfile
# cProfile.run("ChcWeb_PO.getIdcardTest('lbl', 'HHkk2327447', '小茄子')")


# # 封装getIdcardTest函数
def p_getIdcard(param):
    return ChcWeb_PO.getIdcardTest(param)

def p_runTest(param):
    return ChcWeb_PO.runTest(param)


# 程序的主要部分
def main():
    try:
        time1 = time.time()
        # 获取cpu核数
        # print("CPU cores: ", cpu_count())
        # ChcWeb_PO.logger.info("CPU cores: "+ str(cpu_count()))

        # with Pool(2) as pool:
        #     squared_numbers = pool.map(p_getIdcard, ["小茄子", "小猴子"])
        # print("test", squared_numbers)

        # 假设有 4 个 CPU 核心
        with Pool(2) as pool:
            pool.map(p_runTest, ["小茄子.json", "小猴子.json"])

        time2 = time.time()
        pool.close()
        pool.join()
        print('总共耗时：' + str(time2 - time1) + 's')

    except:
        sys.exit(1)

if __name__ == "__main__":

    main()










