# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-12-27
# Description: 社区健康管理中心 - 新泾镇社区卫生服务中心，执行自动上报
#***************************************************************
from ChcWebPO import *
ChcWeb_PO = ChcWebPO()

# 获取家庭医生列表顺序名单
# print(ChcWeb_PO.getDocTest('lbl', 'HHkk2327447')) # 测试环境  # {'小茄子': 1, '小猴子': 2, '111': 3, '自动化': 4}
# print(ChcWeb_PO.getDoc('xj', '12345678'))


# 获取身份证字典，将身份证保存到文件
print(ChcWeb_PO.getIdcardTest('lbl', 'HHkk2327447', "小茄子"))  # {'小茄子': {1: ['110101198907071506', '110101201602029686'}}
# print(ChcWeb_PO.getIdcard('xj', '12345678', "小茄子"))


# 执行上报
ChcWeb_PO.runTest('lbl', 'HHkk2327447', File_PO.jsonfile2dict("小茄子.json"))
# ChcWeb_PO.run('xj', '12345678', File_PO.jsonfile2dict("小茄子.json"))






