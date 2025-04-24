# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-11
# Description: 基本公卫 - 老年人健康管理 - 老年人自理能力评估查询
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '老年人自理能力评估查询')


# todo 1 查询
Gw_PO.phs_snr_selfcareassess_query({"身份证号": "110101193801014615"})
# Gw_PO.phs_snr_selfcareassess_query({"姓名": "胡成", "身份证号": "330101194811111550", '出生日期': [[2025,1,1],[2025,2,2]], '评估日期': [[2025,1,13],[2025,2,12]],
#     "管理机构": "招远市卫健局", '是否仅查询机构': '是',"现住址": ["泉山街道", "花园社区居民委员会", "123"]})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_snr_selfcareassess.xls")



# todo 3 操作 - 详情
# Gw_PO.phs_snr_selfcareassess_operation({'operate': '详情', 'option': {"身份证号": "110101193801014615"}})


# todo 4 操作 - 编辑 (老年人生活自理能力评估表)
Gw_PO.phs_snr_selfcareassess_operation({'operate': '编辑', 'option': {"身份证号": "110101193801014615"}})
Gw_PO.phs_snr_selfcareassess_operation({'operate': '编辑', 'data': {
    "进餐：使用餐具将饭菜送入口、咀嚼、吞咽等活动":" 需要协助，如切碎、搅拌食 物等(3) ",
    "梳洗：梳头、洗脸、刷牙、剃须洗澡等活动":" 独立完成(0) ",
    "穿衣：穿衣裤、袜子、鞋子等活动":" 完全需要帮助(5) ",
    "如厕：小便、大便等活动及自控":" 完全需要帮助(10) ",
    "活动：站立、室内行走、上下楼梯、户外活动": " 借助较大的外力才能完成站立、行走，不能上下楼梯(5) "}
    })

# # todo 5 操作 - 删除
# Gw_PO.phs_snr_selfcareassess_operation({'operate': '删除', 'option': {"身份证号": "110101193801014615"}})

