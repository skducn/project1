# 1, 1getStock.py （收盘后执行）, 爬取数据 ,保存3份（/Users/linghuchong/Desktop/stock/20250606.txt, 2025-06-06.json, all.json）
# /Users/linghuchong/Desktop/stock/20250606.txt 用于导入
# 2025-06-06.json 当天的涨停板票，备用
# all.json 记录历史涨停板票，当天收盘价，成交量，用于匹配

# 2，2compareStock.py （盘中执行）匹配现价与历史涨停板昨日价格，符合要求的输出。