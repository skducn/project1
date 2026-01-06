# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-1-6
# Description: 17.2.5 全表最大值的位置 375页
# https://gairuo.com/p/pandas-book-dataset
# 需求：获取最大值位置的列名
# axes[1] - 获取列索引，axes[0] 是行索引
# .columns - 直接访问DataFrame的列索引
# .tolist() - 将Index对象转换为Python列表
# 这样就可以获得包含最大值的列名 ['B', 'C']。
# ********************************************************************************************************************
import pandas as pd

df = pd.DataFrame({'A':[1,2,4,5,-6],'B':[2,4,8,2,1],'C':[2,-1,8,4,4]},
                  index=['x','y','z','h','i'])

# 获取整个数据框的最大值（8）
# 双重最大值：第一个 .max() 获取每列的最大值，第二个 .max() 获取所有列最大值中的最大值
print(df.max().max())  # 8

# 创建布尔掩码，将等于最大值的位置保留，其他位置设为NaN
print(df[df == df.max().max()])
#     A    B    C
# x NaN  NaN  NaN
# y NaN  NaN  NaN
# z NaN  8.0  8.0
# h NaN  NaN  NaN
# i NaN  NaN  NaN

print(df[df==df.max().max()]
      .dropna(how='all')
      .dropna(how='all', axis=1)
)
#      B    C
# z  8.0  8.0

print(df[df==df.max().max()]
      .dropna(how='all')
      .dropna(how='all', axis=1)
      .axes
)
# [Index(['z'], dtype='object'), Index(['B', 'C'], dtype='object')]

# 获取列名列表
max_cols = df[df==df.max().max()].dropna(how='all').dropna(how='all', axis=1).axes[1].tolist()
print(max_cols)  # ['B', 'C']

# 通过 columns 属性获取
result_df = df[df==df.max().max()].dropna(how='all').dropna(how='all', axis=1)
max_cols = result_df.columns.tolist()
print(max_cols)  # ['B', 'C']



def find_max_column_recursive(df):
      """
      递归查找最大值对应的列名
      如果最大值出现在多个列中，则比较这些列的次大值，直到找到唯一列
      """
      while True:
            # 获取当前数据框的最大值
            max_val = df.max().max()

            # 找到包含最大值的列
            max_cols = df[df == max_val].dropna(how='all').dropna(how='all', axis=1).columns.tolist()

            if len(max_cols) == 1:
                  # 如果只有一个列包含最大值，返回该列名
                  return max_cols[0]
            elif len(max_cols) > 1:
                  # 如果有多个列包含最大值，提取这些列继续比较
                  df = df[max_cols]

                  # 对这些列进行排序，找出在最大值相同情况下，次大值更高的列
                  # 首先移除最大值，然后查找剩余值的最大值
                  df_without_max = df.where(df != max_val)

                  # 如果移除最大值后仍有值，则继续比较次大值
                  if df_without_max.count().sum() > 0:
                        # 获取次大值
                        remaining_max = df_without_max.max().max()
                        if pd.notna(remaining_max):  # 确保次大值不是NaN
                              # 找到包含次大值的列
                              sub_max_cols = df_without_max[df_without_max == remaining_max].dropna(how='all').dropna(
                                    how='all', axis=1).columns.tolist()

                              if len(sub_max_cols) == 1:
                                    return sub_max_cols[0]
                              else:
                                    # 继续在次大值相同的列中查找
                                    df = df[sub_max_cols]
                                    continue
                        else:
                              # 如果没有次大值，返回第一个列名（或者可以根据其他逻辑选择）
                              return max_cols[0]
                  else:
                        # 如果移除最大值后没有剩余值，说明所有列的最大值都相同且没有其他值
                        return max_cols[0]
            else:
                  # 如果没有找到最大值列（理论上不会发生）
                  return None


def find_max_column_optimized(df):
      """
      优化版本：通过排序方式查找最大值列
      """
      # 获取每列的最大值
      col_max_values = df.max()

      # 按最大值降序排序
      sorted_cols = col_max_values.sort_values(ascending=False)

      # 找到最大值相同的列
      max_value = sorted_cols.iloc[0]
      max_cols = sorted_cols[sorted_cols == max_value].index.tolist()

      if len(max_cols) == 1:
            return max_cols[0]

      # 如果有多个列具有相同的最大值，继续比较这些列
      current_df = df[max_cols]

      while len(current_df.columns) > 1:
            # 获取当前数据框的最大值
            current_max = current_df.max().max()

            # 找到包含最大值的列
            max_cols = current_df[current_df == current_max].dropna(how='all').dropna(how='all',
                                                                                      axis=1).columns.tolist()

            if len(max_cols) == 1:
                  return max_cols[0]

            # 移除当前最大值，继续比较剩余值
            current_df = current_df.where(current_df != current_max)

            # 移除全为NaN的列
            current_df = current_df.dropna(axis=1, how='all')

            if current_df.empty:
                  # 如果所有列都为空，返回原列中的第一个
                  return max_cols[0]

      return current_df.columns[0] if len(current_df.columns) > 0 else None



print("原始数据:")
print(df)
print()

# 测试优化版本
result = find_max_column_optimized(df)
print(f"通过递归比较找到的最大值列: {result}")


# 详细分析过程
def detailed_analysis(df):
      """
      详细分析查找过程
      """
      print("详细分析过程:")
      print(f"1. 获取每列的最大值: {df.max().to_dict()}")

      # 获取包含全局最大值的列
      max_val = df.max().max()
      max_cols = df[df == max_val].dropna(how='all').dropna(how='all', axis=1).columns.tolist()
      print(f"2. 全局最大值 {max_val} 出现在列: {max_cols}")

      if len(max_cols) > 1:
            print(f"3. 需要在列 {max_cols} 中进一步比较")
            # 比较这些列的其他值
            subset_df = df[max_cols]
            print(f"4. 子数据框:\n{subset_df}")

            # 移除最大值后继续比较
            without_max = subset_df.where(subset_df != max_val)
            print(f"5. 移除最大值后的数据:\n{without_max}")

            if without_max.count().sum() > 0:
                  next_max = without_max.max().max()
                  next_max_cols = without_max[without_max == next_max].dropna(how='all').dropna(how='all',
                                                                                                axis=1).columns.tolist()
                  print(f"6. 次大值 {next_max} 出现在列: {next_max_cols}")


detailed_analysis(df)
