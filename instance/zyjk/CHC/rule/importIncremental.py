# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-3-8
# Description: 增量 导入数据库
# 将规则用例（chcRuleCase.xlsx）导入db
# 规则：自动将SheetName转为拼音字母，并添加前缀a_, 如"健康评估: => a_jinhaogaoge
#***************************************************************
from ChcRulePO import *
ChcRule_PO = ChcRulePO()


ChcRule_PO.importIncremental('健康评估')
# ChcRule_PO.importIncremental('健康干预')
# ChcRule_PO.importIncremental("中医体质辨识")
# ChcRule_PO.importIncremental('疾病评估')
# ChcRule_PO.importIncremental('儿童健康干预')






