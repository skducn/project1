import akshare as ak
import pandas as pd
from datetime import datetime

# -------------------------- 配置参数 --------------------------
TARGET_DATE = "2025-11-17"  # 目标日期（格式：YYYY-MM-DD，需为交易日）
SAVE_PATH = "上海A股收盘价_单日期.xlsx"

# --------------------------------------------------------------

# 1. 获取指定日期的上海A股日线数据
def get_sh_close_price(date):
    try:
        # 获取上海A股股票列表
        stock_list = ak.stock_info_sh_name_code()

        # # 检查实际返回的列名
        # print("股票列表列名:", stock_list.columns.tolist())
        # print("股票数量:", len(stock_list))
        # 添加详细调试信息
        print("股票列表形状:", stock_list.shape)
        print("股票列表列名:", stock_list.columns.tolist())
        if not stock_list.empty:
            print("前3行数据:")
            print(stock_list.head(3))

        # 如果列名不同，需要相应调整
        # 常见的列名可能是: '证券代码', '证券简称' 等

        # 存储所有股票数据
        all_stocks_data = []

        # 遍历股票列表获取每只股票的数据
        for index, row in stock_list.iterrows():
            try:
                # 根据实际列名调整
                stock_code = row.iloc[0]  # 第一列通常是代码
                stock_name = row.iloc[1]  # 第二列通常是名称

                # 获取单只股票的历史数据
                stock_df = ak.stock_zh_a_hist(symbol=stock_code,
                                              period="daily",
                                              start_date=date,
                                              end_date=date,
                                              adjust="qfq")

                # 如果有数据且收盘价大于0，则添加到结果中
                if not stock_df.empty and len(stock_df) > 0 and stock_df["收盘"].iloc[0] > 0:
                    stock_data = {
                        "ts_code": stock_code,
                        "name": stock_name,
                        "close": stock_df["收盘"].iloc[0],
                        "vol": stock_df["成交量"].iloc[0] if "成交量" in stock_df.columns else 0
                    }
                    all_stocks_data.append(stock_data)

            except Exception as e:
                continue

        # 转换为DataFrame
        result = pd.DataFrame(all_stocks_data)
        return result
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return pd.DataFrame()

# 2. 主流程执行
if __name__ == "__main__":
    print(f"正在获取 {TARGET_DATE} 上海A股收盘价...")
    # 获取数据
    close_data = get_sh_close_price(TARGET_DATE)
    print(f"成功获取 {len(close_data)} 只股票的收盘价")

    # 保存到Excel
    close_data.to_excel(SAVE_PATH, index=False)
    print(f"数据已保存到：{SAVE_PATH}")

    # 打印前5条数据预览
    print("\n数据预览：")
    print(close_data.head())
