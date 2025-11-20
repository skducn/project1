# https://akshare.akfamily.xyz/data/stock/stock.html#id14

import akshare as ak

# stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
# print(stock_zh_a_spot_em_df)

stock_sh_a_spot_em_df = ak.stock_sh_a_spot_em()
print(stock_sh_a_spot_em_df)

# 保存到Excel文件
stock_sh_a_spot_em_df.to_excel('/Users/linghuchong/Desktop/stock/stock_data.xlsx', index=False)

print("数据已保存到 stock_data.xlsx 文件中")

