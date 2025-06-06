# 获取某个股票（600671），昨天的开盘价，收盘价，成交量，换手率

import akshare as ak
from datetime import datetime, timedelta
import sys
# 计算昨天的日期
today = datetime.now()
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y%m%d')
yesterday_formatted = yesterday.strftime('%Y-%m-%d')

# print(yesterday_formatted)
# print(yesterday.strftime('%Y%m%d'))
# sys.exit(0)

# 获取上证指数历史行情数据
# stock_data = ak.index_zh_a_hist(symbol="600671", period="daily")
stock_data = ak.index_zh_a_hist(symbol="600671", period="daily", start_date=yesterday.strftime('%Y%m%d'), end_date=yesterday.strftime('%Y%m%d'))
print(stock_data)


# 筛选出昨天的数据
filtered_data = stock_data[stock_data['日期'] == yesterday_formatted]

if not filtered_data.empty:
    latest_data = filtered_data.iloc[0]
    open_price = latest_data['开盘']
    close_price = latest_data['收盘']
    volume = latest_data['成交量']
    hsl = latest_data['换手率']
    print(f"昨天（{yesterday_str}）开盘价：{open_price} 收盘价：{close_price} 成交量：{volume} 换手率：{hsl}")
else:
    print(f"未能获取到 {yesterday_str} 的股票数据，请检查日期或网络连接。")


