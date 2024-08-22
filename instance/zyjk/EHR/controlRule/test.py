# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-10-25
# Description: 2.3.1 质控规则自动化脚本
# 测试依据：D:\1zy\6 研发二部\1 电子健康档案\2.3.1\V2.3.1开发测试任务.xlsx
# 测试sql，小月，质控规则自动化测试2.3.1.11docx(6).docx
# 测试文档 autoRule2.3.1.xlsx
# *****************************************************************

from instance.zyjk.EHR.controlRule.PageObject.RulePO import *
R = RulePO()

for i in range(R.max_row-1):
    if R.l_isRun[0][i] != 'N' and R.l_exec[0][i] !=  None:
        exec(R.l_exec[0][i])

if platform.system() == 'Darwin':
    os.system("open ./config/autoRule2.3.1.xlsx")
if platform.system() == 'Windows':
    os.system("start .\\config\\autoRule2.3.1.xlsx")


