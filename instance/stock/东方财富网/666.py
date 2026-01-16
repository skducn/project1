# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-01-7
# Description: 东方财富网 666
# https://quote.eastmoney.com/zixuan/lite.html
# 获取每个组列表页数据，保存到文件
# path = "/Users/linghuchong/Downloads/51/Python/stock/BK4"
# *****************************************************************

from PO.TimePO import *
Time_PO = TimePO()

from PO.WebPO import *
from PO.NewexcelPO import *
from PO.OpenpyxlPO import *

path = "/Users/linghuchong/Downloads/51/Python/stock/666"
s_currDate = str(Time_PO.getDateByMinus())

# Web_PO = WebPO("noChrome")
Web_PO = WebPO("chrome")
Web_PO.openURL("https://quote.eastmoney.com/zixuan/")
Web_PO.clkByX("/html/body/div[5]/img[1]", 1)  # 广告
Web_PO.clkByX("/html/body/div[1]/div[2]/div[3]/a[1]",3)  # 登陆
Web_PO.dwele('//span[@date-type="account" and text()="账号登录"]')   # 移动到登陆标签
Web_PO.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[1]/input", "13816109050")
Web_PO.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[2]/input", "Jinhao123")
Web_PO.clkByX("/html/body/div/div[2]/div/form[1]/div/div[4]/div/img[1]",2)  # 勾选
Web_PO.clkByX("/html/body/div/div[2]/div/form[1]/div/div[3]/div[1]/div/div[4]/div/div", 2)  # 验证点击
Web_PO.quitIframe(2)
Web_PO.clkByX("/html/body/div[2]/div[2]/div/div[2]/div",1)  # 关闭右
Web_PO.clkByX("/html/body/div[2]/div[1]/div[3]/div[1]/div",1)  # 关闭下




def main():
    # 获取列表页数据，保存文档

    l_all = []
    i_rowCount = Web_PO.getCountByXs("//div[@id='table_m']/table/tbody/tr")
    print(43, i_rowCount)

    a = int(i_rowCount / 18)
    s = 0
    # for i in range(i_rowCount):
    for i in range(18):
        s_code = Web_PO.getTextByX("/html/body/div[2]/div[1]/div[2]/div[3]/div/div/div[3]/div/div/table/tbody/tr[" + str(i + 1) + "]/td[2]/a")  # 代码
        s_name = Web_PO.getTextByX("/html/body/div[2]/div[1]/div[2]/div[3]/div/div/div[3]/div/div/table/tbody/tr[" + str(i + 1) + "]/td[3]/a")
        s_4 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[5]/span")  # 最新价
        s_5 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[6]/span")  # 涨跌幅
        s_12 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[13]/span")  # 换手率
        s_14 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[15]/span")  # 量比
        s_15 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[16]/span")  # 市盈率
        s_17 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[18]/span")  # 所属行业
        s_18 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[19]/span")  # 流通股
        s_19 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[20]/span")  # 所属概念
        s_20 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[21]/span")  # 流通市值
        s_21 = Web_PO.getTextByX("//div[@id='table_m']/table/tbody/tr[" + str(i + 1) + "]/td[22]/span")  # 主力流入
        print(s_code, s_name, s_4, s_5, s_12, s_14, s_15, s_17, s_18, s_19, s_20, s_21)

    Web_PO.scrollElementToBottom("//div[@id='table_m']")
   

        # s = 16


        # # s_code = Web_PO.getTextByX('/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[3]/a')  # 代码
        # # 忽略BK板块
        # if "BK" in s_code:
        #     s_name = Web_PO.getTextByX(
        #         '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[4]/a')  # 名称
        #     s_chg = Web_PO.getTextByX(
        #         '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[7]/span')  # 涨跌幅
        #     s_MCNI = Web_PO.getTextByX(
        #         '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[8]/span')  # 主力净流入
        #     s_chaoda = Web_PO.getTextByX(
        #         '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[10]/span')  # 超大单净占比
        #     s_da = Web_PO.getTextByX(
        #         '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[11]/span')  # 大单净占比
        #     s_zhong = Web_PO.getTextByX(
        #         '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[12]/span')  # 中单净占比
        #     s_xiao = Web_PO.getTextByX(
        #         '/html/body/div[2]/div[3]/div[3]/table/tbody/tr[' + str(i + 1) + ']/td[13]/span')  # 小单净占比
        #     l_ = [s_currDate, s_code, s_name, s_chg, s_MCNI, s_chaoda, s_da, s_zhong, s_xiao]  # 创建行数据列表
        #     l_all.append(l_)
        #
        #     # 生成文件名，如 300009_安科生物.xlsx
        #     varFile = s_code + "_" + s_name + ".xlsx"
        #
        #     # 将文件保存在sh或sz目录下
        #     varFile = path + "/" + varFile
        #     if os.access(varFile, os.F_OK):
        #         Openpyxl_PO = OpenpyxlPO(varFile)
        #     else:
        #         Newexcel_PO = NewexcelPO(varFile)
        #         Openpyxl_PO = OpenpyxlPO(varFile)
        #         Openpyxl_PO.setRows(
        #             {1: ['日期', '代码', '名称', '涨跌幅', '主力净流入(亿)', '超大单净占比(%)', '大单净占比(%)', '中单净占比(%)', '小单净占比(%)']})
        #
        #     # 判断文件内容，如果日期不存在，则追加； 因为每个组里股票不去重。
        #     l_1 = Openpyxl_PO.getOneCol(1)
        #     if s_currDate not in l_1:
        #         Openpyxl_PO.appendRows(l_all)
        #     l_all = []


# todo 666
l_group = Web_PO.getTextByXs("//ul[@id='zxggrouplist']/li")
print(l_group)  # ['自选股', 'BK4', '全固态电池', '光刻机', '深空通讯和数据链', 'HBM']
# Web_PO.clkByX("/html/body/div[2]/div[3]/div[1]/div/ul[1]/li[2]/a", 2)  # 点击组
Web_PO.clkByX("/html/body/div[2]/div[1]/div[2]/div[1]/div/ul[1]/li[3]", 2)  # 点击组 666
main()


