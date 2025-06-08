# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-06-07
# Description: 周线买卖策略
# *****************************************************************

import akshare as ak
from datetime import datetime, timedelta
import mplfinance as mpf
import os
import sys
from PO.TimePO import *
Time_PO = TimePO()


def get_stock_weekly_volume(qty, d_weekly):

    # 获取指定股票的周线成交量数据
    # d_weekly = {1: '20250606', 2: '20250530', 3: '20250523', 4: '20250516', 5: '20250509', 6: '20250502'}

    # d_ = {}
    # # # 获取股票代码列表
    # # l_stock_code = ["603906"]
    # l_stock_code = ["603906", '603758', '300607']
    # #
    # for i in l_stock_code:
    #     l_all = []
    #     for k, v in d_weekly.items():
    #         d_1 = {}
    #         if k <= qty:
    #             # 获取股票周线数据
    #             l_ = ak.stock_zh_a_hist(symbol=i, period="weekly", start_date=v, end_date=v, adjust="qfq")
    #             # 代码，名称，周日期，开盘，收盘，最高，最低，成交量，成交金额，振幅，涨幅，涨跌，换手率
    #             # ['600671', '天目药业', '2025-05-30', '12.41', '12.88', '12.96', '12.14', '177028', '221437875.00', '6.64', '4.29', '0.53', '14.54']
    #             d_1['date'] = l_[2]
    #             d_1['name'] = l_[1]
    #             if float(l_[3]) > float(l_[4]):
    #                 d_1['price'] = l_[3]
    #             else:
    #                 d_1['price'] = l_[4]
    #             # d_1['startPrice'] = l_[3] # 开盘价
    #             # d_1['endPrice'] = l_[4]  # 收盘价
    #             d_1['volume'] = l_[7]  # 成交量
    #             d_1['amplitude'] = l_[9]  # 振幅
    #             l_all.append(d_1)
    #     d_[i] = l_all
    # print(d_)
    # # {'603906': [{'date': '2025-06-06', 'name': '龙蟠科技', 'price': '13.73', 'volume': '3512132', 'amplitude': '19.11'}, {'date': '2025-05-30', 'name': '龙蟠科技', 'price': '11.98', 'volume': '1668763', 'amplitude': '10.63'}, {'date': '2025-05-23', 'name': '龙蟠科技', 'price': '12.32', 'volume': '1926624', 'amplitude': '14.01'}], '603758': [{'date': '2025-06-06', 'name': '秦安股份', 'price': '13.10', 'volume': '422045', 'amplitude': '10.65'}, {'date': '2025-05-30', 'name': '秦安股份', 'price': '12.86', 'volume': '403563', 'amplitude': '6.20'}, {'date': '2025-05-23', 'name': '秦安股份', 'price': '13.98', 'volume': '949777', 'amplitude': '12.22'}], '300607': [{'date': '2025-06-06', 'name': '拓斯达', 'price': '34.33', 'volume': '1233173', 'amplitude': '10.58'}, {'date': '2025-05-30', 'name': '拓斯达', 'price': '34.21', 'volume': '1820996', 'amplitude': '11.58'}, {'date': '2025-05-23', 'name': '拓斯达', 'price': '38.00', 'volume': '2642238', 'amplitude': '13.57'}]}

    # 测试
    d_ = {'603906': [{'date': '2025-06-06', 'name': '龙蟠科技', 'price': '13.73', 'volume': '3512132', 'amplitude': '19.11'}, {'date': '2025-05-30', 'name': '龙蟠科技', 'price': '11.98', 'volume': '1668763', 'amplitude': '10.63'}, {'date': '2025-05-23', 'name': '龙蟠科技', 'price': '12.32', 'volume': '1926624', 'amplitude': '14.01'}], '603758': [{'date': '2025-06-06', 'name': '秦安股份', 'price': '13.10', 'volume': '422045', 'amplitude': '10.65'}, {'date': '2025-05-30', 'name': '秦安股份', 'price': '12.86', 'volume': '403563', 'amplitude': '6.20'}, {'date': '2025-05-23', 'name': '秦安股份', 'price': '13.98', 'volume': '949777', 'amplitude': '12.22'}], '300607': [{'date': '2025-06-06', 'name': '拓斯达', 'price': '34.33', 'volume': '1233173', 'amplitude': '10.58'}, {'date': '2025-05-30', 'name': '拓斯达', 'price': '34.21', 'volume': '1820996', 'amplitude': '11.58'}, {'date': '2025-05-23', 'name': '拓斯达', 'price': '38.00', 'volume': '2642238', 'amplitude': '13.57'}]}

    for k, v in d_.items():
        # v = [{'date': '20250606', 'name': '龙蟠科技', 'price': '13.73', 'volume': '3512132', 'amplitude': '19.11'},
        # {'date': '20250530', 'name': '龙蟠科技', 'price': '11.98', 'volume': '1668763', 'amplitude': '10.63'}]}


            if float(v[1]['amplitude']) < 0 and float(v[0]['amplitude']) > 0 and \
                    float(v[1]['volume']) > float(v[0]['volume']) and \
                    float(v[1]['price'])*0.99 < float(v[0]['price']):
                # todo 买方1: 两周lh背离（涨跌判断l或h）
                # 这里的最高价(开盘价和收盘价比较那个大就是最高价)
                # 上周成交量 > 本周成交量，上周最高价*0.99 < 本周最高价(开盘价和收盘价那个大就是最高价)，输出。
                # float(l_1[3]) < 0 and float(l_1[7]) > 0  振幅，上周绿，本周红
                # float(l_1[2]) > float(l_1[6]) 上周成交量大于本周成交
                # (float(l_1[1]) * 0.99) < float(l_1[5]) 上周最高价*0.99 < 本周最高价(开盘价和收盘价那个大就是最高价)
                if int(k) >= 600000  and int(k) < 700000:
                    print("https://xueqiu.com/S/SH" + str(k), v[0]['name'], "买方1: 两周lh背离（涨跌判断l或h）")
                else:
                    print("https://xueqiu.com/S/SZ" + str(k), v[0]['name'], "买方1: 两周lh背离（涨跌判断l或h）")

            elif float(v[1]['volume']) < float(v[0]['volume']) and \
                    float(v[1]['price'])*0.99 < float(v[0]['price']):
                # todo 买方2: 两周lh / hh正比（上升通道5线处买，底部反弹时等2周横盘缩量买）
                # 上周成交量 < 本周成交量，上周最高价 * 0.99 < 本周最高价，输出。
                if int(k) >= 600000  and int(k) < 700000:
                    print("https://xueqiu.com/S/SH" + str(k), v[0]['name'], "买方2: 两周lh / hh正比（上升通道5线处买，底部反弹时等2周横盘缩量买）")
                else:
                    print("https://xueqiu.com/S/SZ" + str(k), v[0]['name'], "买方2: 两周lh / hh正比（上升通道5线处买，底部反弹时等2周横盘缩量买）")



            elif float(v[2]['amplitude']) < 0 and float(v[1]['amplitude']) > 0 and float(v[0]['amplitude']) > 0 and \
                float(v[1]['volume']) > float(v[0]['volume']) and \
                float(v[1]['price']) * 0.99 < float(v[0]['price']) and \
                float(v[2]['volume']) > float(v[0]['volume']) and \
                float(v[2]['price']) * 0.99 < float(v[0]['price']):
                # 三周
                # todo 买方3: 三周lhh背离（涨跌判断l或h）
                # 上周成交量 > 本周成交量，上周最高价* 0.99 < 本周最高价，
                # 上上周成交量 > 本周最高价, 上上周最高价 * 0.99 < 本周最高价，输出。
                # ['2025-04-11', '9.97', '669789', '-10.32', '2025-04-18', '9.62', '401198', '0.21',
                # '2025-04-25', '9.60', '270139', '1.16']
                # float(l_1[3]) < 0 and float(l_1[7]) > 0 and float(l_1[11]) > 0 and \  lhh
                    # elif float(l_1[3]) < 0 and float(l_1[7]) > 0 and float(l_1[11]) > 0 and \
            #         float(l_1[6]) > float(l_1[10]) and \
            #         (float(l_1[5]) * 0.99) < float(l_1[9]) and \
            #         float(l_1[2]) > float(l_1[10]) and \
            #         (float(l_1[1]) * 0.99) < float(l_1[9]) :
                if int(k) >= 600000 and int(k) < 700000:
                    print("https://xueqiu.com/S/SH" + str(k), v[0]['name'], "买方3: 三周lhh背离（涨跌判断l或h）")
                else:
                    print("https://xueqiu.com/S/SZ" + str(k), v[0]['name'], "买方3: 三周lhh背离（涨跌判断l或h）")

        # # elif len(l_1) == 16:
        #     # 4周
        #     # todo 买方4: 4周lhhh背离（涨跌判断l或h）
        #     # 上周成交量 > 本周成交量，上周最高价* 0.99 < 本周最高价，
        #     # 上上周成交量 > 本周最高价, 上上周最高价 * 0.99 < 本周最高价
        #     # 上上周成交量 > 本周最高价, 上上周最高价 * 0.99 < 本周最高价，输出。
        #     # ['2025-04-11', '9.97', '669789', '-10.32', '2025-04-18', '9.62', '401198', '0.21',
        #     # '2025-04-25', '9.60', '270139', '1.16', '2025-04-30', '9.74', '192992', '1.46']
        #     if float(l_1[3]) < 0 and float(l_1[7]) > 0 and float(l_1[11]) > 0 and float(l_1[15]) > 0 and \
        #             float(l_1[2]) > float(l_1[14]) and \
        #             (float(l_1[1]) * 0.99) < float(l_1[13]) :
        #         if int(k) >= 600000 and int(k) < 700000:
        #             print("https://xueqiu.com/S/SH" + str(k), info[1])
        #         else:
        #             print("https://xueqiu.com/S/SZ" + str(k), info[1])
        #
        # elif len(l_1) == 20:
        #     # 5周
        #     # todo 买方5: 5周lhhhh背离（涨跌判断l或h）
        #     # ['2025-04-11', '9.97', '669789', '-10.32', '2025-04-18', '9.62', '401198', '0.21',
        #     # '2025-04-25', '9.60', '270139', '1.16', '2025-04-30', '9.74', '192992', '1.46',
        #     # '2025-05-09', '9.75', '323039', '4.52']
        #     # print(999)
        #     # print(float(l_1[2]) , float(l_1[18]))
        #     # print((float(l_1[1]) * 0.99) , float(l_1[17]))
        #     if float(l_1[3]) < 0 and float(l_1[7]) > 0 and float(l_1[11]) > 0 and float(l_1[15]) > 0 and float(l_1[19]) > 0 and \
        #             float(l_1[2]) > float(l_1[18]) and \
        #             (float(l_1[1]) * 0.99) < float(l_1[17]):
        #         if int(k) >= 600000 and int(k) < 700000:
        #             print("https://xueqiu.com/S/SH" + str(k), info[1])
        #         else:
        #             print("https://xueqiu.com/S/SZ" + str(k), info[1])


if __name__ == "__main__":

    from datetime import datetime

    l_fridays = Time_PO.get_fridays_until_today(datetime(2025, 5, 1))
    # print(l_fridays)  # ['20250502', '20250509', '20250516', '20250523', '20250530', '20250606']

    # 逆序排列日期列表并转换为字典
    d_fridays = {i + 1: date for i, date in enumerate(reversed(l_fridays))}
    # print(d_fridays)  # {1: '20250606', 2: '20250530', 3: '20250523', 4: '20250516', 5: '20250509', 6: '20250502'}

    # 获取两周周数据
    get_stock_weekly_volume(3, d_fridays)

    # # 获取3周周数据
    # get_stock_weekly_volume("20250523", "20250530", "20250606")

    # get_stock_weekly_volume("20250411", "20250418", "20250425")


    # get_stock_weekly_volume("20250411", "20250418", "20250425", "20250430")
    # get_stock_weekly_volume("20250411", "20250418", "20250425", "20250430", "20250509")