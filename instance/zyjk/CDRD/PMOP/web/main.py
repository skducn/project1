# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-8-4
# Description: 患者运营管理平台	Patient Management Operation Platform（PMOP）
# 需求gitlab：http://192.168.0.241/cdrd_product_doc/product_doc
# *****************************************************************

from PmopPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Pmop_PO = PmopPO(logName)

from PO.TimePO import *
time_PO = TimePO()
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()

# 登录
Pmop_PO.login()

# 打开菜单
# Cdrd_PO.clkMenu('角色管理')
# Cdrd_PO.clkMenu('菜单管理')

# 患者发现 - 患者检索
# Pmop_PO.clkMenu('患者检索')


Pmop_PO.clkMenu('参数设置')
# 查询参数名称
Pmop_PO.setTextByTagUpDiv3Input("label", "参数名称:", "用户管理-密码连续失败锁定")
Pmop_PO.clkByTagUpButton("span", "查询")
Pmop_PO.clkBySearchOne("//tbody/tr", "编辑")
# 修改参数
Pmop_PO.setTextByTagUpDiv3Input("label", "参数名称", "用户管理-密码连续失败锁定1")
Pmop_PO.setTextByTagUpDiv3Input("label", "参数键名", "sys.account.pwdLockNum2")
Pmop_PO.setTextByTagUpDiv3Textarea("label", "参数键值", "54")
Pmop_PO.setTextByTagUpDiv3Textarea("label", "备注", "51231234")




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




# 登出
# Cdrd_PO.logout()


