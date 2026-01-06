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

df = pd.DataFrame({'A':[1,2,4,5,-6],'B':[2,4,8,2,1],'C':[2,8,-1,4,4]},
                  index=['x','y','z','h','i'])


def find_max_column_comprehensive(df):
      """
      综合比较方案：递归查找最大值列，如果最大值相同则比较次大值，以此类推直到找到唯一列
      """

      # 递归比较函数
      def compare_columns_recursive(dataframe):
            # 获取当前数据框的最大值
            current_max = dataframe.max().max()

            # 找到包含当前最大值的列
            max_cols = dataframe[dataframe == current_max].dropna(how='all').dropna(how='all', axis=1).columns.tolist()

            if len(max_cols) == 1:
                  # 如果只有一个列包含最大值，返回该列名
                  return max_cols[0]
            elif len(max_cols) > 1:
                  # 如果有多个列包含相同的最大值，移除当前最大值后继续比较
                  remaining_df = dataframe[max_cols].where(dataframe[max_cols] != current_max)

                  # 移除全为NaN的列
                  remaining_df = remaining_df.dropna(axis=1, how='all')
                  # print(remaining_df)

                  if not remaining_df.empty:
                        # 如果还有剩余数据，继续递归比较
                        return compare_columns_recursive(remaining_df)
                  else:
                        # 如果移除当前最大值后没有剩余数据，说明这些列的值完全相同
                        # 返回第一个列名（或可以按其他规则选择）
                        return max_cols[0]
            else:
                  # 理论上不会到达这里
                  return None

      return compare_columns_recursive(df)


def find_max_column_by_ranking(df):
      """
      排名比较方案：通过排序排名来比较列
      """
      # 创建一个用于比较的副本
      df_copy = df.copy()
      result_col = None

      while not df_copy.empty:
            # 获取当前最大值
            current_max = df_copy.max().max()

            if pd.isna(current_max):
                  # 如果最大值是NaN，说明所有值都已处理完
                  break

            # 找到包含当前最大值的列
            max_cols = df_copy[df_copy == current_max].dropna(how='all').dropna(how='all', axis=1).columns.tolist()

            if len(max_cols) == 1:
                  # 找到唯一列，返回
                  result_col = max_cols[0]
                  break
            elif len(max_cols) > 1:
                  # 仍有多个列具有相同值，移除当前值继续比较
                  df_copy = df_copy[max_cols].where(df_copy[max_cols] != current_max)
                  df_copy = df_copy.dropna(axis=1, how='all')
                  # print(df_copy)
            else:
                  # 没有找到最大值列（理论上不会发生）
                  break

      return result_col if result_col else df.columns[0]


def find_max_column_with_detailed_comparison(df):
      """
      详细比较方案：构建每列的值序列进行比较
      """
      # 为每列构建值的排序序列
      column_sequences = {}

      print(df.columns)  # Index(['A', 'B', 'C'], dtype='object')

      for col in df.columns:
            # 获取该列的所有值并按降序排列
            # kind='mergesort' - 使用归并排序确保稳定性，相同值的相对位置不变
            sorted_values = df[col].sort_values(ascending=False, kind='mergesort')  # 对每列进行降序排序，使用稳定排序算法
            column_sequences[col] = sorted_values.values  # 将排序后的值存储到字典中
      print(104, column_sequences)  # 104 {'A': array([ 5,  4,  2,  1, -6]), 'B': array([8, 4, 2, 2, 1]), 'C': array([ 8,  4,  4,  2, -1])}

      # 比较每列的值序列，从最大值开始逐个比较
      max_length = max(len(seq) for seq in column_sequences.values())
      # print(111, max_length)  # 5

      for i in range(max_length):
            # 获取当前比较位置的值
            current_values = {}
            for col, seq in column_sequences.items():
                  # print(col, seq)
                  if i < len(seq):
                        current_values[col] = seq[i]
                  else:
                        # 如果该列的值已比较完，用负无穷表示（最小值）
                        current_values[col] = float('-inf')

            # 找到当前比较位置的最大值
            max_current_val = max(current_values.values())
            print(126, max_current_val) # 8 8 4

            # 找到具有最大值的列
            max_cols = [col for col, val in current_values.items() if val == max_current_val]
            print(max_cols)

            if len(max_cols) == 1:
                  # 找到唯一列
                  return max_cols[0]
            elif len(max_cols) > 1:
                  # 继续比较下一位置
                  continue

      # 如果所有值都相同，返回第一列
      return df.columns[0]


def find_max_column_with_dataframe_comparison(df):
      """
      DataFrame比较方案：使用pandas的排序功能进行比较
      """
      # 创建一个包含所有列值的比较框架
      # 将每列按降序排序，然后比较整个序列
      sorted_series = {}

      for col in df.columns:
            sorted_series[col] = df[col].sort_values(ascending=False, kind='mergesort').reset_index(drop=True)

      # 创建比较DataFrame
      comparison_df = pd.DataFrame(sorted_series)

      # 按行进行比较，从第一行开始（最大值）
      for idx in comparison_df.index:
            row_values = comparison_df.loc[idx]
            max_val = row_values.max()
            max_cols = row_values[row_values == max_val].index.tolist()

            if len(max_cols) == 1:
                  return max_cols[0]
            elif len(max_cols) > 1:
                  # 继续比较下一行
                  continue
            else:
                  break

      # 如果所有值都相同，返回第一列
      return df.columns[0]


# 测试数据

print("原始数据:")
print(df)
print()

# 测试各种优化版本
print(f"综合比较方案（采用递归方式，逐层移除当前最大值后继续比较剩余值）: {find_max_column_comprehensive(df)}")
print(f"排名比较方案（使用循环结构，逐步移除当前最大值进行比较）: {find_max_column_by_ranking(df)}")
print(f"详细比较方案（为每列构建降序排列的值序列，逐位置比较）: {find_max_column_with_detailed_comparison(df)}")
print(f"DataFrame比较方案: {find_max_column_with_dataframe_comparison(df)}")

# 总体对比
# 性能：排名比较方案 > 综合比较方案 > 详细比较方案
# 内存：详细比较方案 > 综合比较方案 > 排名比较方案
# 可读性：详细比较方案 > 综合比较方案 > 排名比较方案

# 测试更复杂的情况
df_complex = pd.DataFrame({
      'A': [10, 8, 6, 4, 2],
      'B': [10, 8, 7, 3, 1],
      'C': [10, 8, 6, 5, 0]
}, index=['r1', 'r2', 'r3', 'r4', 'r5'])

print("\n复杂数据测试:")
print(df_complex)
print(f"复杂数据 - 综合比较方案: {find_max_column_comprehensive(df_complex)}")
print(f"复杂数据 - 详细比较方案: {find_max_column_with_detailed_comparison(df_complex)}")

# 测试完全相同的列
df_same = pd.DataFrame({
      'A': [1, 2, 3],
      'B': [1, 2, 3],
      'C': [1, 2, 3]
}, index=['r1', 'r2', 'r3'])

print("\n完全相同数据测试:")
print(df_same)
print(f"相同数据 - 综合比较方案: {find_max_column_comprehensive(df_same)}")
