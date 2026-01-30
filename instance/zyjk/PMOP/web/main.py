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


# todo c1，参数设置，检索"用户管理-密码连续失败锁定"，编辑
# Pmop_PO.clkMenu('参数设置')
# # 检索"用户管理-密码连续失败锁定"
# Pmop_PO.setInput("label", "参数名称:", 3, "用户管理-密码连续失败锁定")
# Pmop_PO.clkByTagUpButton("span", "查询")
# Pmop_PO.clkTextByOne("//tbody/tr", "span", "编辑")
# # 编辑
# Pmop_PO.setInput("label", "参数名称", 3, "用户管理-密码连续失败锁定123")
# Pmop_PO.setInput("label", "参数键名", 3, "sys.account.pwdLockNum456")
# Pmop_PO.setTextarea("label", "参数键值", 2, "54")
# Pmop_PO.setTextarea("label", "备注", 2, "51231234")
# Pmop_PO.clkButton("取 消")


# todo c2，角色管理，检索"UI测试"，编辑
Pmop_PO.clkMenu('角色管理')
# 检索"222"
Pmop_PO.setInput("角色名称:", 3, "UI测试")
Pmop_PO.clkButton("查询")
Pmop_PO.clkTextByOne("编辑")
# [编辑角色]
Pmop_PO.setInput("角色名称", 3, "555")
# Pmop_PO.setInput(" 权限字符 ", 3, "LockNum456")
Pmop_PO.setInput("角色顺序", 4, "6")
# 编辑 - 菜单权限
Pmop_PO.sltCheckBoxOne("展开/折叠", True)
# Pmop_PO.sltCheckBoxOne("父子联动", False)
# 编辑 - 菜单权限 - 全选第一层
Pmop_PO.sltCheckBoxMore(["数据导入"], True)
# Pmop_PO.sltCheckBoxMore(["专病中心"], True)
# Pmop_PO.sltCheckBoxMore(["系统管理"], False)
# Pmop_PO.sltCheckBoxMore(["系统日志"], False)
# 编辑 - 菜单权限 - 全选第二层
# Pmop_PO.sltCheckBoxMore(["专病中心", "患者详情"], False)
# Pmop_PO.sltCheckBoxMore(["基础配置", "扩展字段管理"], False)
# 编辑 - 菜单权限 - 全选第三层
# Pmop_PO.sltCheckBoxMore(["数据导入", "外部数据导入", ["删除", "刷新"]], True)
# Pmop_PO.sltCheckBoxMore(["专病中心", "患者详情", ["诊断删除", "就诊详情"]], False)
# Pmop_PO.sltCheckBoxMore(["专病中心", "患者详情", ["诊断删除", "就诊详情"]], False)
# Pmop_PO.sltCheckBoxMore(["专病中心", "患者详情", ["起搏器随访附件"]], True)
# Pmop_PO.sltCheckBoxMore(["系统日志", "登录日志", ["登录查询"]], False)
# Pmop_PO.sltCheckBoxMore(["基础配置", "扩展字段管理", ["扩展字段删除", "扩展字段新增"]], False)
# Pmop_PO.sltCheckBoxMore(["基础配置", "标签管理", ["标签删除", "标签新增"]], False)
Pmop_PO.setTextarea("备注", 2, "51231234")
Pmop_PO.clkButton("取 消")





# Pmop_PO.clkCheckBox("span", "外部数据导入", True)
# Pmop_PO.clkCheckBox("span", "专病中心", False)


# Pmop_PO.clkCheckBox("span", "全选/全不选", False)
# Pmop_PO.clkCheckBox("span", "父子联动", False)




# 打开菜单
# Cdrd_PO.clkMenu('角色管理')
# Cdrd_PO.clkMenu('菜单管理')

# 患者发现 - CDRD患者检索.ini
# Pmop_PO.clkMenu('CDRD患者检索.ini')


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


