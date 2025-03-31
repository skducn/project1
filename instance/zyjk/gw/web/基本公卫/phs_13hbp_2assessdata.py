# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 评分信息查询
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '评分信息查询')


# # todo 1 查询
Gw_PO.phs_hbp_assessdata_query({"身份证号": "340203202407017263"})
# Gw_PO.phs_hbp_assessdata_query({"管理机构":["玲珑卫生院", "玲珑镇大蒋家村卫生室"], "档案状态": "在档", "姓名": "刘长春", "身份证号":"110101199001012256",
#                                   "得分范围": [1,30], "评分日期":[[2025,1,2],[2025,1,3]], "现住址":["泉山街道", "花园社区居民委员会","123"], "是否兑换": "是",
#                                   "人群分类": ["残疾人", "儿童"]})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_hbp_assessdata.xlsx")


# todo 3 详情（未处理）
# Gw_PO.phs_hbp_assessdata_operation({'operate': '详情', 'option': {"身份证号": "370685198705183027"}})
# Gw_PO.phs_hbp_assessdata_operation({'operate': '详情', 'data': {
# Gw_PO.phs_hbp_assessdata_detail()
# # 判断查询数量，并点击详情
# if s_qty == 1: Web_PO.eleClkByX(ele2, ".//button[1]", 2)
# # 详情页(null)
# getattr(Gw_PO, s_func + '_detail')()


# # todo 4 修改（未处理）
# Gw_PO.phs_hbp_assessdata_operation({'operate': '修改', 'option': {"身份证号": "370685198705183027"}})
# Gw_PO.phs_hbp_assessdata_modify()
# if s_qty == 1: Web_PO.eleClkByX(ele2, ".//button[2]", 2)
# # 修改页(null)
# getattr(Gw_PO, s_func + '_modify')({"积分": [[['所有人', '1', '健康素养'], [2025,1,2], 10], [["所有人", '5', "查询档案"], [2025,2,2],2]],
#                      '评分日期': [2025, 1, 3], '是否兑换': "是"})


# todo 5 删除