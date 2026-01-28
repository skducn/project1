# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-01-7
# Description: 每日板块涨幅 获取BK4
# https://quote.eastmoney.com/zixuan/lite.html
# 获取每个组列表页数据，保存到文件
# *****************************************************************

from PO.TimePO import *
Time_PO = TimePO()

from PO.NewexcelPO import *
from PO.OpenpyxlPO import *

import login
Web_PO = login.create_logged_web_instance("chrome")

# 定义 XPath 常量
GROUP_LIST_XPATH = "//ul[@id='zxggrouplist']/li"
GROUP_ITEM_XPATH_TEMPLATE = "/html/body/div[2]/div[3]/div[1]/div/ul[1]/li[{}]/a"
FUNDS_FLOW_XPATH = "/html/body/div[2]/div[3]/div[2]/ul/li[2]"
CHANGE_PERCENT_XPATH = "/html/body/div[2]/div[3]/div[3]/table/thead/tr/th[7]/a"
d_title = {1: ['代码', '名称', '涨跌幅', '主力净流入(亿)', '超大单净占比(%)', '大单净占比(%)', '中单净占比(%)', '小单净占比(%)']}
s_currDate = str(Time_PO.getDateByMinus())
s_file = "/Users/linghuchong/Downloads/51/Python/stock/每日板块涨幅.xlsx"


def main(s_group):
    l_all = []

    # 1，点击组，如 BK4
    l_group = Web_PO.getTextByXs(GROUP_LIST_XPATH)
    i_index = l_group.index(s_group) + 1
    Web_PO.clkByX(GROUP_ITEM_XPATH_TEMPLATE.format(i_index), 2)  # 点击组

    # 2，点击资金流向、涨跌幅
    Web_PO.clkByX(FUNDS_FLOW_XPATH, 2)  # 资金流向
    Web_PO.clkByX(CHANGE_PERCENT_XPATH, 2)  # 涨跌幅

    # 3，遍历所有数据
    all_codes = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[3]/a")
    all_names = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[4]/a")
    all_chgs = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[7]/span")
    all_mcnis = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[8]/span")
    all_chaodas = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[10]/span")
    all_das = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[11]/span")
    all_zhongs = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[12]/span")
    all_xiaos = Web_PO.getTextByXs("//table[@id='wltable']/tbody/tr/td[13]/span")
    i_rowCount = Web_PO.getCountByXs("//table[@id='wltable']/tbody/tr")
    for i in range(i_rowCount):
        s_code = all_codes[i]
        if "BK" in s_code:
            l_ = [
                s_code,
                all_names[i],
                all_chgs[i],
                all_mcnis[i],
                all_chaodas[i],
                all_das[i],
                all_zhongs[i],
                all_xiaos[i]
            ]
            l_all.append(l_)

    # 4，保存
    # 4。1，判断文件是否存在
    if os.access(s_file, os.F_OK):
        Openpyxl_PO = OpenpyxlPO(s_file)
        Openpyxl_PO.addSheet(s_currDate, overwrite=True)
    else:
        NewexcelPO(s_file, s_currDate)
        Openpyxl_PO = OpenpyxlPO(s_file, s_currDate)

    # 4。2 检查是否已有标题行，如果没有则添加
    try:
        first_cell_value = Openpyxl_PO.getCell(1, 1)  # 获取第一行第一列的值
        if first_cell_value is None or first_cell_value != '代码':
            # 如果标题行不存在或不匹配，则写入标题
            Openpyxl_PO.setRows(d_title)
    except:
        # 如果获取不到值（例如新文件），则写入标题
        Openpyxl_PO.setRows(d_title)

    # 4。3 追加数据
    Openpyxl_PO.appendRows(l_all)


# todo main
time_start = time.time()
main('BK4')
time_end = time.time()
total_seconds = time_end - time_start
# 转换为分钟和秒
minutes = int(total_seconds // 60)
seconds = total_seconds % 60
print(f"耗时: {minutes} 分 {seconds:.0f} 秒")




