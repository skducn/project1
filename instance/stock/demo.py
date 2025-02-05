# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description:
# *****************************************************************



from yfinance import download
import pandas as pd

# 获取历史数据（包括实时数据）
# apple_data = download('蓝色光标', start_date='2023-01-01', end_date='2023-12-31')

import yfinance as yf

# # 获取历史数据
symbol = "蓝色光标"
start_date = "2025-01-27"
end_date = "2025-01-27"
#
# data = yf.download(symbol, start_date, end_date)
data = yf.download(symbol, start_date, end_date, requestlimit=100)

print(data)

# from yahoo_finance import Share
#
# share = Share(symbol, start_date='2023-01-01')
# data = share.history(start_date='2025-01-27', end_date='2025-01-27')
#
# print(data)











