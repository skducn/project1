# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-3-11
# Description: 基本公卫 - 老年人健康管理 - 简易智力检查查询
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '简易智力检查查询')


# todo 1 查询
Gw_PO.phs_snr_intelligence_query({"身份证号": "110101195901015999"})
# Gw_PO.phs_snr_intelligence_query({"姓名": "胡成", "身份证号": "110101195901015999", '出生日期': [[2025,1,1],[2025,2,2]], '评估日期': [[2025,1,13],[2025,2,12]],
#     "管理机构": "招远市卫健局", '是否仅查询机构': '是',"现住址": ["泉山街道", "花园社区居民委员会", "123"]})


# todo 2 导出
# Gw_PO.export("/Users/linghuchong/Desktop/phs_snr_intelligence.xls")


# todo 3 操作 - 详情
# Gw_PO.phs_snr_intelligence_operation({'operate': '详情', 'option': {"身份证号": "110101193801014615"}})


# todo 4 操作 - 编辑 (简易智力检查查询)
# Gw_PO.phs_snr_intelligence_operation({'operate': '编辑', 'option': {"身份证号": "110101195901015999"}})
# Gw_PO.phs_snr_intelligence_operation({'operate': '编辑', 'data': {
#     "1.时间定力 (5)": {"今年是哪一年?": "0", "现在是什么季节": "0", "现在是几月份": "0", "今天是几号": "0", "今天是星期几": "0"},
#     "2.地点定向力 (5)": {"我们现在在哪个国家?": "0", "我们现在在哪个城市": "0", "我们现在在城市的哪一部分": "0", "我们现在在哪个建筑物": "0", "我们现在在第几层": "0"},
#     "3.即刻回忆 (3)": {"皮球": "0", "国旗": "0", "树": "0"},
#     "4.注意力与计算力 (5)": {"100减7等于? 93": "0", "100减7等于? 86": "0", "100减7等于? 79": "0", "100减7等于? 72": "0", "100减7等于? 65": "0"},
#     "5.回忆能力 (3)": {"皮球": "0", "国旗": "0", "树": "0"},
#     "6.命名能力 (2)": {"问:这是什么? 展示 (铅笔)": "0", "问:这是什么? 展示 (手表)": "0"},
#     "7.语言重复能力 (1)": {"说:我现在让你重复我说的。准备好了吗？瑞雪兆丰年。你说一遍 ": "0"},
#     "8.理解力 (3)": {"左手拿着这张纸": "0", "把它对折": "0", "把它放在你的右腿上": "0"},
#     "9.阅读能力 (1)": {"闭上你的眼睛": "0"},
#     "10.写的能力 (1)": {"说:写一个句子。": "0"},
#     "11.画画的能力 (1)": {"说:照下图画。 ": "0"}
# }})

# # todo 5 操作 - 删除
Gw_PO.phs_snr_intelligence_operation({'operate': '删除', 'option': {"身份证号": "110101195901015999"}})

