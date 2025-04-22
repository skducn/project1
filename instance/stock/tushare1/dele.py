# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 删除all。xlsx shsz表中name字段中包含ST的行
# *****************************************************************
import pandas as pd

# 读取 Excel 文件
file_path = 'all.xlsx'
excel_file = pd.ExcelFile(file_path)

# 获取指定工作表中的数据
df = excel_file.parse('shsz')

# 删除 name 字段包含 ST 字符的行
df = df[~df['name'].str.contains('ST', na=False)]

# 保存处理后的数据到新文件
new_file_path = 'all_without_st.xlsx'
df.to_excel(new_file_path, index=False)
