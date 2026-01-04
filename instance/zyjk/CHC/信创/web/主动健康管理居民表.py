# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-12-22
# Description: 社区健康5G 信创1.0 - 表与表
# 需求：/Users/linghuchong/Desktop/智赢健康/信创/主动健康管理居民表.png
#***************************************************************
from PO.SqlserverPO import *
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "utf8")

SFZH = "420204202201016739"

# todo 签约信息表
QYYH = Sqlserver_PO.select("SELECT * FROM QYYH where SFZH='%s'" % (SFZH))
print("QYYH =>", QYYH)

# todo 主动健康管理居民表
HP_PERSON = Sqlserver_PO.select("SELECT * FROM HP_PERSON where ID_CARD='%s'" % (SFZH))
print("HP_PERSON =>", HP_PERSON)
print("HP_PERSON[0]['ID'] =>", HP_PERSON[0]['ID'])
print("HP_PERSON[0]['SERVICE_DOC_ID'] =>", HP_PERSON[0]['SERVICE_DOC_ID'])
print("HP_PERSON[0]['PLAN_ID'] =>", HP_PERSON[0]['PLAN_ID'])

# todo 居民VIP登记日志表
VIP_PERSON_LOG = Sqlserver_PO.select("SELECT * FROM VIP_PERSON_LOG where PERSON_ID='%s'" % (HP_PERSON[0]['ID']))
print("VIP_PERSON_LOG =>", VIP_PERSON_LOG)

# todo 文章发送明细表
ARTICLE_SENDING_DETAILS = Sqlserver_PO.select("SELECT * FROM ARTICLE_SENDING_DETAILS where PERSON_ID='%s'" % (HP_PERSON[0]['ID']))
print("ARTICLE_SENDING_DETAILS =>", ARTICLE_SENDING_DETAILS)
print("ARTICLE_SENDING_DETAILS[0]['ARTICLE_SEEDING_ID'] =>", ARTICLE_SENDING_DETAILS[0]['ARTICLE_SEEDING_ID'])

# todo 文章发送记录表(无数据)
ARTICLE_SENDING = Sqlserver_PO.select("SELECT * FROM ARTICLE_SENDING where ARTICLE_ID='%s'" % (ARTICLE_SENDING_DETAILS[0]['ARTICLE_SEEDING_ID']))
print("ARTICLE_SENDING =>", ARTICLE_SENDING)
# print("ARTICLE_SENDING[0]['ARTICLE_ID'] =>", ARTICLE_SENDING[0]['ARTICLE_ID'])
#
# # todo 文章表（无数据）
# ARTICLE_INFO = Sqlserver_PO.select("SELECT * FROM ARTICLE_INFO where ARTICLE_ID='%s'" % (ARTICLE_SENDING[0]['ARTICLE_ID']))
# print("ARTICLE_INFO =>", ARTICLE_INFO)

# # todo 短信发送明细表（无数据）
# MESSAGE_SENDING_DETAILS = Sqlserver_PO.select("SELECT * FROM MESSAGE_SENDING_DETAILS where PERSON_ID='%s'" % (HP_PERSON[0]['ID']))
# print("MESSAGE_SENDING_DETAILS =>", MESSAGE_SENDING_DETAILS)
# print("MESSAGE_SENDING_DETAILS[0]['MESSAGE_SEEDING_ID'] =>", MESSAGE_SENDING_DETAILS[0]['MESSAGE_SEEDING_ID'])
#
# # todo 短信发送记录表（无数据）
# MESSAGE_SENDING = Sqlserver_PO.select("SELECT * FROM MESSAGE_SENDING where ID='%s'" % (MESSAGE_SENDING_DETAILS[0]['MESSAGE_SEEDING_ID']))
# print("MESSAGE_SENDING =>", MESSAGE_SENDING)
# print("MESSAGE_SENDING[0]['MESSAGE_ID'] =>", MESSAGE_SENDING[0]['MESSAGE_ID'])
#
# # # todo 短信模版数据表（无数据）
# MESSAGE_TEMPLATES = Sqlserver_PO.select("SELECT * FROM MESSAGE_TEMPLATES where ID='%s'" % (MESSAGE_SENDING[0]['MESSAGE_ID']))
# print("MESSAGE_TEMPLATES =>", MESSAGE_TEMPLATES)

# # todo 设备发放表
DEVICES_SEEDING = Sqlserver_PO.select("SELECT * FROM DEVICES_SEEDING where PERSON_ID='%s'" % (HP_PERSON[0]['ID']))
print("DEVICES_SEEDING =>", DEVICES_SEEDING)
print("DEVICES_SEEDING[0]['DEVICES_ID'] =>", DEVICES_SEEDING[0]['DEVICES_ID'])

# todo 设备管理表
DEVICES_MANAGE = Sqlserver_PO.select("SELECT * FROM DEVICES_MANAGE where DEVICES_ID='%s'" % (DEVICES_SEEDING[0]['DEVICES_ID']))
print("DEVICES_MANAGE =>", DEVICES_MANAGE)


# # todo 主动健康小程序用户信息表（无数据）
# HP_PERSON_WEIXIN = Sqlserver_PO.select("SELECT * FROM HP_PERSON_WEIXIN where PERSON_ID='%s'" % (HP_PERSON[0]['ID']))
# print("HP_PERSON_WEIXIN =>", HP_PERSON_WEIXIN)
# print("HP_PERSON_WEIXIN[0]['PERSON_ID'] =>", HP_PERSON_WEIXIN[0]['PERSON_ID'])

# # todo 主动健康血压记录表
person_id = '44'
# PERSON_BP_RECORD = Sqlserver_PO.select("SELECT * FROM PERSON_BP_RECORD where PERSON_ID='%s'" % (HP_PERSON_WEIXIN[0]['PERSON_ID']))
PERSON_BP_RECORD = Sqlserver_PO.select("SELECT * FROM PERSON_BP_RECORD where PERSON_ID='%s'" % (person_id))
print("PERSON_BP_RECORD =>", PERSON_BP_RECORD)

# # todo 主动健康血糖记录表
person_id = '83'
# PERSON_GLU_RECORD = Sqlserver_PO.select("SELECT * FROM PERSON_GLU_RECORD where PERSON_ID='%s'" % (HP_PERSON_WEIXIN[0]['PERSON_ID']))
PERSON_GLU_RECORD = Sqlserver_PO.select("SELECT * FROM PERSON_GLU_RECORD where PERSON_ID='%s'" % (person_id))
print("PERSON_GLU_RECORD =>", PERSON_GLU_RECORD)

# # todo 主动健康油盐糖血压记录表
person_id = '83'
# PERSON_FLAVORING_RECORD = Sqlserver_PO.select("SELECT * FROM PERSON_FLAVORING_RECORD where PERSON_ID='%s'" % (HP_PERSON_WEIXIN[0]['PERSON_ID']))
PERSON_FLAVORING_RECORD = Sqlserver_PO.select("SELECT * FROM PERSON_FLAVORING_RECORD where PERSON_ID='%s'" % (person_id))
print("PERSON_FLAVORING_RECORD =>", PERSON_FLAVORING_RECORD)

# # # todo 互联网医院预约信息表（无数据）
# ONLINE_APPOINTMENT = Sqlserver_PO.select("SELECT * FROM ONLINE_APPOINTMENT where APPOINTMENTER_ID='%s'" % (HP_PERSON_WEIXIN[0]['PERSON_ID']))
# print("ONLINE_APPOINTMENT =>", ONLINE_APPOINTMENT)

# # # todo 主动健康居民交流问题表（无数据）
# PERSON_COMMUNICATE = Sqlserver_PO.select("SELECT * FROM PERSON_COMMUNICATE where QUESTIONER_ID='%s'" % (HP_PERSON_WEIXIN[0]['PERSON_ID']))
# # print("PERSON_COMMUNICATE =>", PERSON_COMMUNICATE)
# # print("PERSON_COMMUNICATE[0]['ID'] =>", PERSON_COMMUNICATE[0]['ID'])

# # # todo 主动健康患者交流问题回答内容表（无数据）
# PERSON_COMMUNICATE_ANSWER = Sqlserver_PO.select("SELECT * FROM PERSON_COMMUNICATE_ANSWER where CONSULTING_ID='%s'" % (PERSON_COMMUNICATE[0]['ID']))
# # print("PERSON_COMMUNICATE_ANSWER =>", PERSON_COMMUNICATE_ANSWER)
# # print("PERSON_COMMUNICATE_ANSWER[0]['ID'] =>", PERSON_COMMUNICATE_ANSWER[0]['ID'])

# # # todo 主动健康问题交流图片记录表（无数据），没有链接外键 ？？？
# PERSON_COMMUNICATE = Sqlserver_PO.select("SELECT * FROM CONSULTING_PIC_CONTENT_WEIXIM where ?='%s'" % (PERSON_COMMUNICATE_ANSWER[0]['ID']))
# # print("PERSON_COMMUNICATE =>", PERSON_COMMUNICATE)


# # # todo 评估表
T_ASSESS_INFO = Sqlserver_PO.select("SELECT * FROM T_ASSESS_INFO where ID_CARD='%s'" % (SFZH))
print("T_ASSESS_INFO =>", T_ASSESS_INFO)


# # # todo 居民问题交流记录表
CONSULTING_RECORD = Sqlserver_PO.select("SELECT * FROM CONSULTING_RECORD where PERSON_ID_CARD='%s' and SERVICE_DOC_ID='%s'" % (SFZH, HP_PERSON[0]['SERVICE_DOC_ID']))
print("CONSULTING_RECORD =>", CONSULTING_RECORD)
print("CONSULTING_RECORD[0]['ID'] =>", CONSULTING_RECORD[0]['ID'])

# # # todo 居民问题交流详细内容表
CONSULTING_CONTENT = Sqlserver_PO.select("SELECT * FROM CONSULTING_CONTENT where CONSULTING_ID='%s'" % (CONSULTING_RECORD[0]['ID']))
print("CONSULTING_CONTENT =>", CONSULTING_CONTENT)
print("CONSULTING_CONTENT[0]['ID'] =>", CONSULTING_CONTENT[0]['ID'])

# # # todo 问题交流图片原图表（无数据）
CONSULTING_PIC_CONTENT = Sqlserver_PO.select("SELECT * FROM CONSULTING_PIC_CONTENT where CONSULTING_CONTENT_ID='%s'" % (CONSULTING_CONTENT[0]['ID']))
print("CONSULTING_PIC_CONTENT =>", CONSULTING_PIC_CONTENT)


# # # todo 健康管理计划执行表
HP_PLAN_EXECUTION = Sqlserver_PO.select("SELECT * FROM HP_PLAN_EXECUTION where PERSON_ID='%s' and PLAN_ID='%s'" % (HP_PERSON[0]['ID'],HP_PERSON[0]['PLAN_ID']))
print("HP_PLAN_EXECUTION =>", HP_PLAN_EXECUTION)
print("HP_PLAN_EXECUTION[0]['PLAN_ID'] =>", HP_PLAN_EXECUTION[0]['PLAN_ID'])

# # # todo 健康管理计划表
HP_PLAN = Sqlserver_PO.select("SELECT * FROM HP_PLAN where ID='%s'" % (HP_PLAN_EXECUTION[0]['PLAN_ID']))
print("HP_PLAN =>", HP_PLAN)
print("HP_PLAN[0]['ID'] =>", HP_PLAN[0]['ID'])

# # # todo 健康管理计划项目对照表
HP_PLAN_ITEM = Sqlserver_PO.select("SELECT * FROM HP_PLAN_ITEM where PLAN_ID='%s'" % (HP_PLAN[0]['ID']))
print("HP_PLAN_ITEM =>", HP_PLAN_ITEM)
print("HP_PLAN_ITEM[0]['ITEM_ID'] =>", HP_PLAN_ITEM[0]['ITEM_ID'])

# # # todo 健康管理项目
HP_ITEM = Sqlserver_PO.select("SELECT * FROM HP_ITEM where ITEM_ID='%s'" % (HP_PLAN_ITEM[0]['ITEM_ID']))
print("HP_ITEM =>", HP_ITEM)
print("HP_ITEM[0]['ITEM_ID'] =>", HP_ITEM[0]['ITEM_ID'])
print("HP_ITEM[0]['ITEM_CATEGORY'] =>", HP_ITEM[0]['ITEM_CATEGORY'])
print("HP_ITEM[0]['ITEM_TYPE'] =>", HP_ITEM[0]['ITEM_TYPE'])

# # # todo 健康管理项目类别表
HP_ITEM_TYPE = Sqlserver_PO.select("SELECT * FROM HP_ITEM_TYPE where ITEM_CATEGORY='%s' and ITEM_TYPE='%s'" % (HP_ITEM[0]['ITEM_CATEGORY'],HP_ITEM[0]['ITEM_TYPE']))
print("HP_ITEM_TYPE =>", HP_ITEM_TYPE)