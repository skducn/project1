# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0 评估因素判断规则自动化,
# 需求：体重管理1.18
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r
# pip install pymssql==2.2.8
# pip install petl
# pip install sqlalchemy

#***************************************************************

from WeightPO import *
Weight_PO = WeightPO()


# todo 1, excel导入db
# Weight_PO.excel2db(Configparser_PO.FILE("case"), Configparser_PO.DB("table"))


# # todo 2, 运行主程序
# Weight_PO.main(Configparser_PO.DB_SQL("table"), 'error')  # 执行错误记录
Weight_PO.main(Configparser_PO.DB("table"), 'all')  # 执行全部记录
#
#
# # todo 3, 导出html
# ehr_rule_PO.db2html()


# # if c > 0:
# # #     # todo 4，如结果中有错误记录，则发邮件
# from PO.NetPO import *
# Net_PO = NetPO()
# Net_PO.sendEmail("测试组23", ['h.jin@zy-healthtech.com'], None,
#           "EHR规则自动化测试报告", "htmlFile", "<h3>您好，h.jin：</h3>", Configparser_PO.FILE("html"), """<br>
#    <h3>本邮件由智赢测试系统自动发出，请勿直接回复！</h3>
#    <h3>如您不愿意接收此类邮件，请联系我们，如有打扰请谅解。</h3>
#    <h3>谢谢</h3>
#    """)


# os.system("open " + Configparser_PO.FILE("html"))






