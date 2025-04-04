# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-2-8
# Description: 基本公卫 - 高血压管理 - 高血压随访 应用
# *****************************************************************
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName, '高血压随访')


# todo requirement：检查所有记录，生成2025-02-17的随访日期，且下一次随访日期设置为2025-6-15
# 分析，遍历所有随访记录，如果没有2025-02-17的随访日期，就引用上一次随访新增；否则忽略。

# 格式化日期
visitDate = '2025-02-17'
l_visitDate = []
l_1 = visitDate.split("-")
for i in l_1:
    l_visitDate.append(int(i))
print(l_visitDate)  # [2025, 2, 17]

visitNextDate = '2025-06-15'
l_visitNextDate = []
l_1 = l_visitNextDate.split("-")
for i in l_1:
    l_visitNextDate.append(int(i))
print(l_visitNextDate)  # v[2025, 6, 15]


# 获取记录数和页数
# print(Gw_PO.pagination(1))  # {'totalRecord': 17, 'totalPage': 2, 'gotoPage': 2}
try:
    d_page = Gw_PO.pagination(1)
    total_pages = d_page.get('totalPage', 1)
except Exception as e:
    print(f"Error fetching pagination details: {e}")
    total_pages = 1


# 遍历所有页
for j in range(d_page['totalPage']):
    Gw_PO.pagination(j+1)
    sleep(2)
    ele2 = Web_PO.getSuperEleByX("//tbody", ".")
    i_recordCount = Web_PO.eleGetCountByTag(ele2, "tr")
    # print(i_recordCount)
    # 遍历所有的记录，点击编辑
    for i in range(i_recordCount):
        if Web_PO.eleIsEleExistByX(ele2, ".//tr[" + str(i+1) + "]/td[15]/div/button[2]"):
            print("第" + str(j+1) + "页, 第" + str(i+1) + "条，" + Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]/div/span"))
            Web_PO.eleClkByX(ele2, ".//tr[" + str(i+1) + "]/td[15]/div/button[2]")

            # 获取当前患者的所有随访日期
            Web_PO.zoom(50)
            ele = Web_PO.getEleByClassName("formList")
            l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input",'div:nth-last-of-type(1)')
            print('随访记录 => ', l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
            Web_PO.zoom(100)

            # 检查随访日期 2025-02-17 是否存在
            if visitDate not in l_followUp_date:
                # 1，随访日期中没有 2025-02-17，引用上一次记录
                print("引入上次新增, ", visitDate)
                Gw_PO.phs_hypertension_gxyjob_operation({'operate': '编辑', 'index': {'operate2': '引入上次新增'},
                                                      "value": {'随访日期': l_visitDate, '下次随访日期': l_visitNextDate}})
            else:
                # 2，随访日期中有 2025-02-17，跳过
                print("跳过, ", visitDate)

            ele = Web_PO.getSuperEleByX("//span[text()='关闭']", ".")
            Web_PO.eleClkByX(ele, ".", 2)
        else:
            print("[warning, 无编辑], 第" + str(j+1) + "页, 第" + str(i+1) + "条，" + Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]/div/span"))


