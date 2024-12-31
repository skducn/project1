# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-12-27
# Description: 社区健康管理中心 - 新泾镇社区卫生服务中心，执行自动上报
#***************************************************************
from ChcWebPO import *
ChcWeb_PO = ChcWebPO()

from multiprocessing import Pool
import time


from PO.LogPO2 import *
Log_PO2 = LogPO2("./LogPO2.log")


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
    return ChcWeb_PO.getIdcardTest(param[0], param[1], param[2])

def p_runTest(param):
    return ChcWeb_PO.runTest(param[0], param[1], param[2])

# 程序的主要部分
def main():
    try:
        Log_PO2.logger.info('Program started')
        # 模拟程序运行
        while True:
            # 每隔一段时间执行一些操作

            Log_PO2.logger.info("666")
            time1 = time.time()
            # 假设有 4 个 CPU 核心
            with Pool(4) as pool:
                # squared_numbers = pool.map(p_getIdcard, [('lbl', 'HHkk2327447', "小茄子"), ('lbl', 'HHkk2327447', "小猴子")])
                pool.map(p_runTest, [('lbl', 'HHkk2327447', File_PO.jsonfile2dict("小茄子.json")),
                                     ('lbl', 'HHkk2327447', File_PO.jsonfile2dict("小猴子.json"))])
            # print(squared_numbers)
            time2 = time.time()
            pool.close()
            pool.join()
            print('总共耗时：' + str(time2 - time1) + 's')

    except Exception as e:
        Log_PO2.logger.error('An error occurred: {}'.format(e))
        sys.exit(1)

if __name__ == "__main__":

    main()
    # time1 = time.time()
    # # 假设有 4 个 CPU 核心
    # with Pool(4) as pool:
    #     # squared_numbers = pool.map(p_getIdcard, [('lbl', 'HHkk2327447', "小茄子"), ('lbl', 'HHkk2327447', "小猴子")])
    #     pool.map(p_runTest, [('lbl', 'HHkk2327447', File_PO.jsonfile2dict("小茄子.json")), ('lbl', 'HHkk2327447', File_PO.jsonfile2dict("小猴子.json"))])
    # # print(squared_numbers)
    # time2 = time.time()
    # pool.close()
    # pool.join()
    # print('总共耗时：' + str(time2 - time1) + 's')









