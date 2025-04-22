# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-05-4
# Description:  www.akshare.xyz
# conda activate py310
# pip install aksare
# https://ke.qq.com/webcourse/index.html?r=1683091325369#cid=5835909&term_id=106048134&taid=13742014157360261&type=3072&source=PC_COURSE_DETAIL&vid=387702306339866276
# *****************************************************************
import akshare as ak
import pandas as pd

# 指定股票代码
stock_code = '600019'  # 替换为你需要的股票代码
# 指定日期范围
start_date = '2025-04-17'  # 替换为你需要的开始日期
end_date = '2025-04-18'  # 替换为你需要的结束日期

# 获取历史行情数据
stock_data = ak.stock_zh_a_hist(symbol=stock_code, start_date=start_date, end_date=end_date)
if not stock_data.empty:
    # 选择开盘价、收盘价列
    result_data = stock_data[['开盘价', '收盘价']]
    print(result_data)