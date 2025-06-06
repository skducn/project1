# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 获取东方财富网，上海和深圳今日涨停板票（包含9.5%以上）
# 步骤：
# 1, 1getStock.py （收盘后执行）, 爬取数据 ,保存3份（/Users/linghuchong/Desktop/stock/20250606.txt, 2025-06-06.json, all.json）
# /Users/linghuchong/Desktop/stock/20250606.txt 用于导入
# 2025-06-06.json 当天的涨停板票，备用
# all.json 记录历史涨停板票，当天收盘价，成交量，用于匹配

# 2，2compareStock.py （盘中执行）匹配现价与历史涨停板昨日价格，符合要求的输出。
# *****************************************************************
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

from PO.WebPO import *

from PO.ColorPO import *
Color_PO = ColorPO()

# from ConfigparserPO import *
# Configparser_PO = ConfigparserPO('config.ini')

from PO.LogPO import *
# Log_PO = LogPO(filename=Configparser_PO.DATA("logfile"), level="info")

# 带路径的文件
fileNameBycurrDate = str(Time_PO.getDateByMinus()) + ".json"  # 2025-06-06.json
fileNameByAll  = "all.json"
fileNameByPath = "/Users/linghuchong/Desktop/stock/" + str(Time_PO.getDateByMinus()) + ".txt"


def getLimitUp(l_area):
    s_ = ''
    d_curr = {}

    for area in l_area:
        tmp = 0
        # print(area)

        # 1, 东方财富网
        Web_PO = WebPO("noChrome")
        Web_PO.openURL(area)

        # 3, 获取总页数
        l_page = Web_PO.getTextByXs("//div[@class='qtpager']")
        pageTotal = l_page[0].split("…")[1].split(">")[0]

        # 4, 遍历页面

        for j in range(int(pageTotal)-1):
            # 5, 获取每行数据
            l_data = Web_PO.getTextByXs("//tbody/tr")
            l_data.pop(0)
            for i in l_data:
                d_ = {}
                l_ = i.split(" ")
                # 处理个别股票名中带有空格的票，如 "罗 牛 山"，转换成 "罗牛山"
                if l_[3] != '股吧':
                    l_1 = []
                    l_1.append(l_.pop(0))
                    l_1.append(l_.pop(0))
                    l_1.append(''.join(List_PO.split(l_, '股吧', 0)))
                    l_1.append('股吧')
                    l_2 = List_PO.split(l_, '股吧', 1)
                    l_ = l_1 + l_2

                # print(l_)  # ['1', '600805', '悦达投资', '股吧', '资金流', '数据', '5.34', '10.10%', '0.49', '70.91万', '3.72亿',
                # '10.31%', '5.34', '4.84', '4.84', '4.85', '1.82', '8.34%', '71.77', '1.04']
                d_['date'] = str(Time_PO.getDateByMinus())
                d_['code'] = l_[1]
                d_['name'] = l_[2]
                d_['todayStartPrice'] = l_[14]  # 今开
                d_['yesterdayEndPrice'] = l_[15]  # 昨收
                d_['volume'] = l_[9]  # 成交量
                # todo 条件是涨幅大于9.5，不包含ST
                # print(l_)
                l7 = float(l_[7].replace("%", ''))  # 涨跌幅
                # print(l7) 9.5
                # 判断涨跌幅是否大于9.5
                # if l7 > 9.5 and '白银' not in l_[2] :
                if l7 > 9.5 and 'ST' not in l_[2] :
                    s_ = s_ + l_[2] + ","
                    d_curr[l_[1]] = d_
                else:
                    tmp = 1
                    break
            if tmp == 1:
                break

            # 切换页数
            Web_PO.setTextByX("//form[@class='gotoform']/input[1]", j+2)
            # 点击GO
            # 绕过页面交互限制，通过执行 JS 脚本来点击目标元素：
            element = Web_PO.driver.find_element(By.XPATH, "//form[@class='gotoform']/input[2]")
            Web_PO.driver.execute_script("arguments[0].click();", element)
            sleep(2)

    try:
        with open("./history/" + fileNameBycurrDate, 'w', encoding='utf-8') as file:
            json.dump(d_curr, file, ensure_ascii=False, indent=4)
        Color_PO.outColor([{"35": f"数据已成功保存到 {fileNameBycurrDate}, 今日涨停数：{len(d_curr)}"}])

        # 保存到 "/Users/linghuchong/Desktop/stock/"，用于导入
        with open(fileNameByPath, 'w', encoding='utf-8') as file:
            file.write(s_)

        if os.path.exists(fileNameByAll):
            with open(fileNameByAll, 'r', encoding='utf-8') as file:
                d_all = json.load(file)
            d_all.update(d_curr)

        with open(fileNameByAll, 'w', encoding='utf-8') as file:
            json.dump(d_all, file, ensure_ascii=False, indent=4)
        Color_PO.outColor([{"35": f"数据已成功保存到 {fileNameByAll}, 合计涨停数：{len(d_all)}"}])
    except Exception as e:
        print(f"保存文件时出现错误: {e}")



# 判断当前时间，盘后执行
s_time = str(time.strftime("%H:%M:%S"))
if int(s_time[:2]) >= 15:
    getLimitUp(["https://quote.eastmoney.com/center/gridlist.html#sh_a_board_hzz",
                "https://quote.eastmoney.com/center/gridlist.html#sz_a_board_hzz"])
else:
    print("暂不执行，建议盘后执行！")