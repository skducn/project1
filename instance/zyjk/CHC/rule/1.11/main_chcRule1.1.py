# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-8-30
# Description: CHC规则主程序 1.1
# 【腾讯文档】社区健康规则自动化v1.11
# https://docs.qq.com/sheet/DYmtPV0dUa1NSdHNt?tab=h940rl

# http://192.168.0.243:8010/
#***************************************************************
from ChcRulePO import *

# # 健康评估,健康干预,中医体质辨识,疾病评估,儿童健康干预
# r = ChcRulePO("评估因素取值")
r = ChcRulePO("健康干预_已患疾病单病")

# 按id执行
r.runId([4])

# 按id区间执行
# r.runIdArea([31])

# 按rule执行
# r.runRule(['s1'])
# r.runRule(['r9', 'r2'])

# 按result执行
# r.runResult("error")
# r.runResult("all")

# 依据updateDate时间执行（执行库中非2024-07-19的规则）
# r.runDate("2024-07-19")
# r.runDate()  # 默认是当天日期

# 按当前日期执行几天以前的规则（如执行3天以前的规则，即最近3天执行过的规则忽略）
# r.runDateAgo(-3)

# 执行几天以前且状态是error的规则
# r.runDateAgoResult(-3, 'error')
