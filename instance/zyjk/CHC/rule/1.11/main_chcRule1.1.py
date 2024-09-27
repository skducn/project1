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
# r.runStep(4)
# r.runStep(5)

r = ChcRulePO("健康干预_已患疾病单病")
r.runId([6])  # s1  {'prefixICD': {'肝硬化': 'K74.4''}, 'VISITTYPECODE': '31'}
# r.runId([2])  # s1  {'prefixICD': {'慢性鼻炎': 'J31.0'}}
# r.runId([3])  # s1 {'prefixICD': {'颈椎病': 'M47.101'}}
# r.runId([4])  # s1 {'prefixICD': {'慢性胃炎': 'K29.6'}}
# r.runId([7])
# r.runId([8])  s2 {'prefixICD': {'慢性肾脏病': 'I15'}}


# r = ChcRulePO("健康干预_已患疾病组合")
# r.runId([107])  # s3 {'prefixICD': {'高血压': 'I13', '糖尿病': 'E11'}}
# r.runId([108])  # s3 {'prefixICD': {'癫痫': 'G41', '肝癌': 'C22'}}

# r.runId([137])  # {'assessValue': {'血脂异常': '2.3'}, 'prefixICD': {'高血压': 'I14', '冠心病': 'I25.1', '慢性胃炎': 'K29.4'}}
# r.runId([138])  # 反 s5,{'assessValue': {'血脂异常': '2.3'}, 'prefixICD': {'妊娠合并肝病': 'O26.6', '子宫平滑肌瘤': 'D25'}}

# r.runId([121])  # s4
# r.runId([122])  # s4 fan {'assessValue': {'胺碘酮服药史': 'XC01BD'}, 'prefixICD': {'系统性红斑狼疮': 'M32', '乳腺癌': 'C50'}}
# r.runId([153])  # s4 {'血脂异常': '2.3', 'assessValue': {'胺碘酮服药史': 'XC01BD'}, 'prefixICD': {'高血压': 'I12', '冠心病': 'I25.1', '心律失常': 'I44'}}
# r.runId([154])  # s4 {'血脂异常': '2.3', 'assessValue': {'胺碘酮服药史': 'XC01BD'}, 'prefixICD': {'帕金森病': 'G20', '妊娠合并子宫瘢痕': 'O34.2'}}



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
