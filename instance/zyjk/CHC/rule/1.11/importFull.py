# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-3-8
# Description: 全量更新表（删除旧表，插入新表）
# 将规则用例【chcRuleCase1.11.xlsx】导入db
# 规则：自动将SheetName转为拼音字母，并添加前缀a_, 如"健康评估: => a_jinhaogaoge
# 注意：excel表中要有id值，程序会将id转为自增id
# ChcRule_PO.importFull('评估疾病表')  # 将"评估疾病表"导入数据库
# # 生成"评估疾病表"中身份证
#***************************************************************
from ChcRulePO import *
ChcRule_PO = ChcRulePO()

# ChcRule_PO.importFull('测试规则')
# ChcRule_PO.importFull('疾病取值判断')

# 创建规则名列表
# ChcRule_PO.crtRuleList()

ChcRule_PO.importFull('评估因素取值')
# ChcRule_PO.importFull('健康干预_已患疾病单病')
# ChcRule_PO.importFull('健康干预_已患疾病组合')
# ChcRule_PO.importFull('健康评估')
# ChcRule_PO.importFull('健康干预_孕产妇')
# ChcRule_PO.importFull('疾病评估_已患和高风险')
# ChcRule_PO.importFull('健康干预_其他分类')
# ChcRule_PO.importFull('健康干预')
# ChcRule_PO.importFull("中医体质辨识")










