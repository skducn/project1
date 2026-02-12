# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-8-4
# Description: 专病库
# 需求gitlab：http://192.168.0.241/cdrd_product_doc/product_doc
# *****************************************************************
# from CdrdPO import *
# logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
# Cdrd_PO = CdrdPO(logName)

import os
from CdrdPO import *

# 设置日志文件路径为当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
logName = os.path.join(script_dir, os.path.basename(__file__).split('.')[0] + ".log")

Cdrd_PO = CdrdPO(logName)

from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()

# 登录
Cdrd_PO.login()

# 打开菜单
# Cdrd_PO.opnMenu('角色管理')
Cdrd_PO.opnMenu('菜单管理')

# 进入：专病中心 - 患者列表
# Cdrd_PO.opnMenu('患者列表')
print("peter在哪里")

Cdrd_PO.quit()


# # 遍历获取每页所有患者详情页url
# # 获取页数
# varPage = 3
# for i in range(varPage):
#     # 获取患者详情页url （默认第一页）
#     d_all = Cdrd_PO.getUrlByPatient(i+1)
#     # 前往第N页
#     if i < varPage-1:
#         Cdrd_PO.setPage(i+2)
# print(d_all)

# 获取患者总数
# self.getPatientCount()

# # 登出
# Cdrd_PO.logout()


