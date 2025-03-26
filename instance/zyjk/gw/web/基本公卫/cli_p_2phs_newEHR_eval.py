# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 并发创建居民健康档案
# *****************************************************************

import sys,os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_dir)
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('../config.ini')

from multiprocessing import Pool, cpu_count
import time

from PO.FilePO import *
File_PO = FilePO()


# 1.2.3 更新居民健康档案
def p_main(param):
    return main(param[0], param[1], param[2])

def main(user, password, d_param):
    # 1，登录
    Gw_PO.login('http://192.168.0.203:30080/#/login', user, password)
    # 菜单
    Web_PO.opnLabel('http://192.168.0.203:30080/phs/HealthRecord/Personal')
    Web_PO.swhLabel(1)

    # todo 3 新增
    # 表：T_EHR_INFO
    # 转义函数名
    d_param['身份证号码'] = eval(d_param['身份证号码'])
    d_param['姓名'] = eval(d_param['姓名'])
    d_param['本人电话'] = eval(d_param['本人电话'])
    d_param['联系人姓名'] = eval(d_param['联系人姓名'])
    d_param['联系人电话'] = eval(d_param['联系人电话'])
    d_param['家庭情况']['户主姓名'] = eval(d_param['家庭情况']['户主姓名'])
    d_param['家庭情况']['户主身份证号'] = eval(d_param['家庭情况']['户主身份证号'])
    d_param['建档日期'][0] = eval(d_param['建档日期'][0])
    d_param['建档日期'][1] = eval(d_param['建档日期'][1])
    d_param['建档日期'][2] = eval(d_param['建档日期'][2])
    print(user, d_param)

    Gw_PO.phs_healthrecord_personal_new({'button': '仅保存', 'data': d_param})

if __name__ == "__main__":

    time1 = time.time()

    # 获取cpu核数
    print("最大CPU cores: ", cpu_count())
    Gw_PO.logger.info("CPU cores: ", str(cpu_count()))

    # 使用不同账号并发N个
    N = 8
    if N > int(cpu_count()):
        N = cpu_count()
    print("并发 => ", N)
    with Pool(N) as pool:
        pool.map(p_main,
                 [('11011', 'HHkk2327447', File_PO.jsonfile2dict("./phs/newEHR_01.json")),
                  ('11012', 'Jinhao123', File_PO.jsonfile2dict("./phs/newEHR_02.json")),
                  ('11013', 'Jinhao123', File_PO.jsonfile2dict("./phs/newEHR_03.json")),
                  ('11014', 'Jinhao123', File_PO.jsonfile2dict("./phs/newEHR_04.json")),
                  ('11015', 'Jinhao123', File_PO.jsonfile2dict("./phs/newEHR_05.json")),
                  ('11016', 'Jinhao123', File_PO.jsonfile2dict("./phs/newEHR_06.json")),
                  ('11017', 'Jinhao123', File_PO.jsonfile2dict("./phs/newEHR_07.json")),
                  ('11018', 'Jinhao123', File_PO.jsonfile2dict("./phs/newEHR_08.json"))])

    time2 = time.time()
    pool.close()
    pool.join()
    print('并发: ', N, '线程, 总耗时: ' + str(int(time2 - time1)) + '秒')
    Gw_PO.logger.info('并发: ', N, '线程, 总耗时: ' + str(int(time2 - time1)) + '秒')
    Gw_PO.logger.info('-'.center(50, "-"))
