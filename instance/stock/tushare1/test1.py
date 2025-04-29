# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 获取某股票某日的收盘价，开盘价，成交量
# 数据源：all.xlsx 获取上海和深圳股票代码，遍历获取上一日和当天的收盘价，开盘价，成交量，市盈率PE，市净率PB，换手率TR，量比VR
# 判断，当天收盘价 大于 上一日的开盘价，且成交量小于上一日的票。
# *****************************************************************

import tushare as ts
import pandas as pd
from datetime import datetime, timedelta

# 设置 tushare 的 token，需要替换为你自己在 tushare 官网注册后获取的 token
# ts.set_token('your_token_here')
# pro = ts.pro_api()
pro = ts.pro_api('894e80b70503f5cda0d86f75820c5871ff391cf7344e55931169bb2a')

# 获取昨天的日期
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

try:
    # 获取上海 A 股所有股票列表
    stock_list = pro.stock_basic(exchange='SSE', list_status='L', fields='ts_code')

    # 获取昨天所有上海 A 股的行情数据
    df_daily = pro.daily(trade_date=yesterday)

    # 获取昨天所有上海 A 股的基本面数据
    df_basic = pro.daily_basic(trade_date=yesterday)

    # 合并行情数据和基本面数据
    result_df = pd.merge(df_daily, df_basic, on='ts_code')

    # 提取需要的列
    result_df = result_df[['ts_code', 'open', 'close', 'vol', 'amount', 'pe', 'volume_ratio']]

    # 重命名列
    result_df.columns = ['股票代码', '开盘价', '收盘价', '成交量', '成交额', '市盈率', '量比']

    # 将结果保存到 Excel 文件
    excel_file_path = f'shanghai_a_stocks_{yesterday}.xlsx'
    result_df.to_excel(excel_file_path, index=False)
    print(f'数据已成功保存到 {excel_file_path}')

except Exception as e:
    print(f"发生错误: {e}")
