# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-4
# Description: 基本公卫 - 老年人健康管理 - 老年人专项登记
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '老年人专项登记')


# todo 1 查询
Gw_PO.phs_snr_special_query({"身份证号": "370685195905183027"})
# Gw_PO.phs_snr_special_query({"管理机构": "招远市卫健局", '是否仅查询机构': '否', "档案状态": "在档", "姓名": "胡成",
#                              '性别': '男', "身份证号": "341226199708114773",'出生日期': [[1960,1,1], [1962,3,2]],
#                              "现住址": ["泉山街道", "花园社区居民委员会", "123"]})


# todo 2 导出(.xls)
# Gw_PO.export("/Users/linghuchong/Desktop/phs_snr_special.xlsx")


# todo 3 批量登记
# Gw_PO.phs_snr_special_operation({'operate': '批量登记', 'option': 'all', 'data': {}})
# Gw_PO.phs_snr_special_operation({'operate': '批量登记', 'option': {"身份证号": "370685195905183027"}, 'data': {}})



# # todo 4 专项登记
# Gw_PO.phs_snr_special_operation({'operate': '专项登记', 'option': {"身份证号": "110101195901018874"}})
# Gw_PO.phs_snr_special_operation({'operate': '专项登记', 'data': {
#     '生活赡养': ['本人', '其他'], '护理情况': "子女", '登记日期': [2025, 2, 2]}})




