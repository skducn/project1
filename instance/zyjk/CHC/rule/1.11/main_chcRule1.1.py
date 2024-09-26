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


# r = ChcRulePO("健康干预_已患疾病单病")
r = ChcRulePO("健康干预_已患疾病组合")

# 按id执行
r.runId([1])  # s3  {'prefixICD': {'高血压': 'I14'}}
# r.runId([135])  # s3 {'prefixICD': {'高血压': 'I15', '冠心病': 'I25.1', '慢性胃炎': 'K29.5'}}

# r.runId([49])  # s4 {'prefixICD': {'心律失常': 'I45'}, 'assessValue': {'非维生素K拮抗口服抗凝药物服药史': 'XB01AE'}}
# r.runId([151])  # s4 {'prefixICD': {'高血压': 'I11', '冠心病': 'I25.1', '心律失常': 'I49'}, 'assessValue': {'胺碘酮服药史': 'XC01BD'}}

# r.runId([109])  # s5 {'prefixICD': {'高血压': 'I13', '糖尿病': 'E13'}, 'assessValue': {'血脂异常': '2.3'}}
# r.runId([153])  # s4 {'血脂异常': '2.3', 'assessValue': {'胺碘酮服药史': 'XC01BD'}, 'prefixICD': {'高血压': 'I11', '冠心病': 'I25.1', '心律失常': 'I44'}}




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
