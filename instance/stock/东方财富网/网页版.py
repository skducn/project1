# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-01-7
# Description: 东方财富网
# https://quote.eastmoney.com/zixuan/lite.html
# 获取页面数据
# *****************************************************************

import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from multiprocessing import Pool, cpu_count
import time

from PO.ListPO import *
List_PO = ListPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.WebPO import *
from PO.NewexcelPO import *
from PO.OpenpyxlPO import *

pathSH = "/Users/linghuchong/Downloads/51/Python/stock/sh"
pathSZ = "/Users/linghuchong/Downloads/51/Python/stock/sz"
s_currDate = str(Time_PO.getDateByMinus())

Web_PO = WebPO("chrome")
Web_PO.openURL("https://quote.eastmoney.com/zixuan/lite.html")
Web_PO.clkByX("/html/body/div[7]/img[1]",1)  # 广告
Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[2]/div/a[1]",3)  # 登陆
Web_PO.dwele('//span[@date-type="account" and text()="账号登录"]')   # 移动到登陆标签

Web_PO.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[1]/input", "13816109050")
Web_PO.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[2]/input", "Jinhao123")
Web_PO.clkByX("/html/body/div/div[2]/div/form[1]/div/div[4]/div/img[1]",2)  # 勾选
Web_PO.clkByX("/html/body/div/div[2]/div/form[1]/div/div[3]/div[1]/div/div[4]/div/div",2)  # 验证点击
Web_PO.quitIframe(2)


def main(group):
    # 获取列表页数据，保存文档

    l_all = []
    Web_PO.clkByX("/html/body/div[2]/div[3]/div[2]/ul/li[2]")  # 资金流向
    i_rowCount = Web_PO.getCountByXs("//table[@id='wltable']/tbody/tr")
    print(group, "-------------------------")
    for i in range(i_rowCount):
        s_code = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[3]/a')  # 代码
        # 忽略BK板块
        if "BK" not in s_code:
            s_name = Web_PO.getTextByX(
                '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[4]/a')  # 名称
            s_chg = Web_PO.getTextByX(
                '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[7]/span')  # 涨跌幅
            s_MCNI = Web_PO.getTextByX(
                '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[8]/span')  # 主力净流入
            s_chaoda = Web_PO.getTextByX(
                '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[10]/span')  # 超大单净占比
            s_da = Web_PO.getTextByX(
                '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[11]/span')  # 大单净占比
            s_zhong = Web_PO.getTextByX(
                '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[12]/span')  # 中单净占比
            s_xiao = Web_PO.getTextByX(
                '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[13]/span')  # 小单净占比
            l_ = [s_currDate, s_code, s_name, s_chg, s_MCNI, s_chaoda, s_da, s_zhong, s_xiao]  # 创建行数据列表
            l_all.append(l_)

            # 生成文件名，如 300009_安科生物.xlsx
            varFile = s_code + "_" + s_name + ".xlsx"

            # 将文件保存在sh或sz目录下
            if int(s_code) < 600000:
                varFile = pathSZ + "/" + varFile
                if os.access(varFile, os.F_OK):
                    Openpyxl_PO = OpenpyxlPO(varFile)
                else:
                    Newexcel_PO = NewexcelPO(varFile)
                    Openpyxl_PO = OpenpyxlPO(varFile)
                    Openpyxl_PO.setRows(
                        {1: ['日期', '代码', '名称', '涨跌幅', '主力净流入(亿)', '超大单净占比(%)', '大单净占比(%)', '中单净占比(%)', '小单净占比(%)']})
            else:
                varFile = pathSH + "/" + varFile
                if os.access(varFile, os.F_OK):
                    Openpyxl_PO = OpenpyxlPO(varFile)
                else:
                    Newexcel_PO = NewexcelPO(varFile)
                    Openpyxl_PO = OpenpyxlPO(varFile)
                    Openpyxl_PO.setRows(
                        {1: ['日期', '代码', '名称', '涨跌幅', '主力净流入(亿)', '超大单净占比(%)', '大单净占比(%)', '中单净占比(%)', '小单净占比(%)']})

            # 判断文件内容，如果日期不存在，则追加； 因为每个组里股票不去重。
            l_1 = Openpyxl_PO.getOneCol(1)
            if s_currDate not in l_1:
                Openpyxl_PO.appendRows(l_all)
            l_all = []


# todo 前6个组
l_group = Web_PO.getTextByXs("//ul[@id='zxggrouplist']/li")
# print(l_group)  # ['自选股', 'BK4', '全固态电池', '光刻机', '深空通讯和数据链', 'HBM']
for i in range(6):
    Web_PO.clkByX("/html/body/div[2]/div[3]/div[1]/div/ul[1]/li[" + str(i+1) + "]/a", 2)  # 点击组
    main(l_group[i])


# todo 更多组合
Web_PO.clkByX("/html/body/div[2]/div[3]/div[1]/div/ul[2]/li/div/a", 2)  # 更多组合
l_group = Web_PO.getTextByXs("//ul[@class='moregroupul bscroll']/li")
# print(l_group)  # ['商业航天', '医药商业', '玻璃基板', '锂矿概念']
i_moreGroupCount = Web_PO.getCountByXs("//ul[@class='moregroupul bscroll']/li")  # 获取数量
for i in range(i_moreGroupCount):
    Web_PO.clkByX("/html/body/div[2]/div[3]/div[1]/div/ul[2]/li/div/a", 2)  # 更多组合
    i_position = Web_PO.getPositionByXByText("//ul[@class='moregroupul bscroll']/li", l_group[i])  # 通过文本定位元素位置
    Web_PO.clkByX("//ul[@class='moregroupul bscroll']/li[" + str(i_position) + "]", 3)  # 点击组
    main(l_group[i])


# # 关闭页面
# Web_PO.cls()





