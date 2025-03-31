# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-5
# Description: 基本公卫 - 健康档案管理 - 健康教育活动
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '健康教育活动')


# todo 1 查询
Gw_PO.phs_healtheducation_healthactivity_query({"活动地点": "上海"})
# Gw_PO.phs_healtheducation_healthactivity_query({"活动日期":[[2025,1,2], [2025,2,4]], "活动地点": "上海", "活动形式": "开展咨询活动", "活动主题": "普法宣传", "主讲人": "阿依达"})


# todo 2 新增
# Gw_PO.phs_healtheducation_healthactivity_operation({'operate': '新增', 'data': {
#     '活动时间': [2025, 1, 3], '活动地点': "上海",
#     '活动形式': "开展咨询活动",
#     '活动主题': "普法宣传", '活动人数': "12", '组织者': "白嫖",
#     '主讲人': "阿依达", '主讲人单位': "上海白月光公司", '职称': "专家",
#     '接受健康教育人员类别': "妇女",
#     '健康教育资源发放种类': "音像资料",
#     '健康教育资源发放数量': "12",
#     '活动内容': "宣传教育",
#     '活动总结评价': "良好",
#     '存档资料类型': [['图片', '签到表'], ["/Users/linghuchong/Desktop/16.jpg","/Users/linghuchong/Desktop/17.jpg"]],
#     '填表人': 'test1', '负责人':'jh', '填表时间':[2025,3,4]
# }})

# todo 3 查看
Gw_PO.phs_healtheducation_healthactivity_operation({'operate': '查看', 'option': {"主讲人": "阿依达"}})
# Gw_PO.phs_healtheducation_healthactivity_operation({'operate': '编辑', 'data': {
    # '活动时间': [2025, 1, 3], '活动地点': "上海",
    # '活动形式': "开展咨询活动",
    # '活动主题': "普法宣传", '活动人数': "12", '组织者': "白嫖",
    # '主讲人': "阿依达", '主讲人单位': "上海白月光公司", '职称': "专家",
    # '接受健康教育人员类别': "妇女",
    # '健康教育资源发放种类': "音像资料",
    # '健康教育资源发放数量': "12",
    # '活动内容': "宣传教育",
    # '活动总结评价': "良好",
    # '存档资料类型': [['印刷', '其他资料'], ["/Users/linghuchong/Desktop/16.jpg","/Users/linghuchong/Desktop/17.jpg"]],
    # '填表人': 'test1', '负责人':'jh', '填表时间':[2025,3,4]
# }})