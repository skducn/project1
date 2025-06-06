# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 爬取东方财富网深圳数据
# 步骤：
# 1, 爬取数据，如# {3: ['3', '600179', '安通控股', '股吧', '资金流', '数据', '2.73', '-8.39%', '-0.25', '118.55万', '3.27亿', '5.03%', '2.85', '2.70', '2.83', '2.98', '4.04', '3.17%', '11.96', '1.05'],
# 2, 保存到sz.json
# *****************************************************************
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.styles.stylesheet")

from PO.WebPO import *

from PO.ColorPO import *
Color_PO = ColorPO()

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
jsonFile = Configparser_PO.DATA("json_sz")

from PO.LogPO import *
Log_PO = LogPO(filename=Configparser_PO.DATA("logfile"), level="info")


# 1, 东方财富网
Web_PO = WebPO("noChrome")
Web_PO.openURL(Configparser_PO.DATA("url_sz") )

# 2, 涨跌幅降序
element = Web_PO.driver.find_element(By.XPATH, "//div[@class='quotetable']/table/thead/tr/th[6]")
Web_PO.driver.execute_script("arguments[0].click();", element)

# 3, 获取总页数
l_page = Web_PO.getTextByXs("//div[@class='qtpager']")
# print(l_page) # ['123…83>转到']
pageTotal = l_page[0].split("…")[1].split(">")[0]
# print(pageTotal)  # 83

# 4, 获取页数据
d_all = {}
for j in range(int(pageTotal)-1):
    print(j)

    # 5, 获取每行
    l_data = Web_PO.getTextByXs("//tbody/tr")
    l_data.pop(0)
    for i in l_data:
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
        # todo 条件是跌的(跌幅在1-8个点); 换手率小于10; 市盈率大于0且小于100；
        l7 = int(float(l_[7].replace("%", ''))) # 涨跌幅
        # print(l7)
        # l7 = l_[7].replace("%", '').replace("-", '')  # 涨跌幅
        l17 = l_[17].replace("%", '')  # 换手率
        if l7 > -8 and l7 < -1 and float(l17) < 10 and float(l_[18]) > 0 and float(l_[18]) < 200:
            d_all[int(l_[0])] = l_

        # 判断涨跌幅是否大于0，大于0则退出循环
        if l7 >= -1:
            # print(d_all)
            # {3: ['3', '600179', '安通控股', '股吧', '资金流', '数据', '2.73', '-8.39%', '-0.25', '118.55万', '3.27亿', '5.03%', '2.85', '2.70', '2.83', '2.98', '4.04', '3.17%', '11.96', '1.05'],
            print("合计：",len(d_all))
            try:
                # 打开文件并写入 JSON 数据
                with open(jsonFile, 'w', encoding='utf-8') as file:
                    # 使用 json.dump 将字典写入文件
                    json.dump(d_all, file, ensure_ascii=False, indent=4)
                # print(f"数据已成功保存到 {jsonFile}")
                Color_PO.outColor([{"35": f"数据已成功保存到 {jsonFile}"}])
            except Exception as e:
                print(f"保存文件时出现错误: {e}")

            exit(0)

    # 切换页数
    Web_PO.setTextByX("//form[@class='gotoform']/input[1]", j+2)
    # 点击GO
    # 绕过页面交互限制，通过执行 JS 脚本来点击目标元素：
    element = Web_PO.driver.find_element(By.XPATH, "//form[@class='gotoform']/input[2]")
    Web_PO.driver.execute_script("arguments[0].click();", element)

