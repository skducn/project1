# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 本年度未评
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '本年度未评')


# todo 1 查询
Gw_PO.phs_hbp_noassessdata_query({"身份证号":"110101199001012256", "人群分类": ["残疾人", "儿童"]})
# Gw_PO.phs_hbp_noassessdata_query({"管理机构":["玲珑卫生院", "玲珑镇大蒋家村卫生室"], "档案状态": "在档", "姓名": "刘长春", "身份证号":"110101199001012256",
#                      "现住址":["泉山街道", "花园社区居民委员会","123"], "人群分类": ["残疾人", "儿童"]})



# todo 2 批量评分（未处理）
# Gw_PO.phs_hbp_noassessdata_batch()

# 点击批量评分，先选择记录，点击批量评分
# getattr(Gw_PO, s_func + '_batch')({'身份证号': ['340203202407017263']})
# getattr(Gw_PO, s_func + '_batch')({'身份证号': ['110101194301191302', '340203202407018290']}
# getattr(Gw_PO, s_func + '_batch')({'身份证号': "all"})

# 翻页用于批量评分
# Web_PO.setTextBackspaceEnterByX("/html/body/div[1]/div/div[3]/section/div/main/div[3]/div/span[3]/div/input", 2)  # 切换到第2页
# Web_PO.setTextBackspaceEnterByX("/html/body/div[1]/div/div[3]/section/div/main/div[3]/div/span[3]/div/input", 12) # 切换到第12页
# Web_PO.setTextBackspaceEnterByX("/html/body/div[1]/div/div[3]/section/div/main/div[3]/div/span[3]/div/input", 13) # 切换到第13页
# Web_PO.setTextBackspaceEnterByX("/html/body/div[1]/div/div[3]/section/div/main/div[3]/div/span[3]/div/input", 4) # 切换到第4页



# todo 3 新增（未处理）
# Gw_PO.phs_hbp_noassessdata_operation({'operate': '新增', 'option': {"身份证号": "370685198705183027"}})
# Gw_PO.phs_hbp_noassessdata_operation({'operate': '新增', 'data': {

# Gw_PO.phs_hbp_noassessdata_new()
# 判断查询数量，并点击新增
# if s_qty == 1: Web_PO.eleClkByX(ele2, ".//button", 2)
# (use to testing)
# Web_PO.opnLabel("http://192.168.0.203:30080/phs/hbp/components/add?id&ehrId=375&singInfoId&type=edit&routeType=1")
# Web_PO.swhLabel(2)
# 新增详情页
# getattr(Gw_PO, s_func + '_new')({'评分日期': [2025, 1, 3], '是否兑换': "是"})
# getattr(Gw_PO, s_func + '_new')({"积分": [[['所有人', '1', '健康素养'], [2025,1,2], 10], [["所有人", '5', "查询档案"], [2025,2,2],2], [["高血压、糖尿病病友", '13', "按时用药"],[2025,4,1],1]],
#                      '评分日期': [2025, 1, 3], '是否兑换': "是"})



