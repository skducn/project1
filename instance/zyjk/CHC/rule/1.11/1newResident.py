# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-9-5
# Description: 新建居民（签约信息表、基本信息表、患者主索引表）
# 参数是人群分类，按照分类创建
# {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}

# [USER]
# user = lbl
# password = HHkk2327447
# d_getUserInfo = {"doctorName": "小茄子", "wkno": "1231231", "orgCode": "0000001", "orgName": "静安精神病院"}
#***************************************************************

from ChcPO import *
Chc_PO = ChcPO()

Chc_PO.newResident(1)
Chc_PO.newResident(2)
Chc_PO.newResident(3)
Chc_PO.newResident(4)
Chc_PO.newResident(5)
Chc_PO.newResident(6)
Chc_PO.newResident(7)



