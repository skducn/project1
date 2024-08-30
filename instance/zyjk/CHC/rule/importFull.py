# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-3-8
# Description: 全量更新到数据库
# 将规则用例（chcRuleCase.xlsx）导入db
# 规则：自动将SheetName转为拼音字母，并添加前缀a_, 如"健康评估: => a_jinhaogaoge
# 注意：excel表中要有id值，程序会将id转为自增id
#***************************************************************
from ChcRulePO import *
ChcRule_PO = ChcRulePO()


# ver 1.11

# [FILE]
# case = chcRuleCase1.11.xlsx
# # ChcRule_PO.importFull('评估疾病表')
# # # 初始化疾病身份证
# ChcRule_PO.initDiseaseIdcardAll('评估疾病表')

# [FILE]
# case = chcRuleCase.xlsx
# ChcRule_PO.importFull('疾病身份证')
# # # 疾病身份证
# ChcRule_PO.initDiseaseIdcardAll('疾病身份证')



# # ver old
# # ChcRule_PO.importFull('健康评估')
# ChcRule_PO.importFull('健康干预')
# # ChcRule_PO.importFull("中医体质辨识")
# # ChcRule_PO.importFull('疾病评估')
# # ChcRule_PO.importFull('儿童健康干预')

# ChcRule_PO.importFull('测试规则')

# # ChcRule_PO.importFull('temporaryTable')


ChcRule_PO.importFull('评估因素取值')


