import subprocess

# 执行自动化测试并生成报告
result = subprocess.run(
    ["pytest", "/Users/linghuchong/Downloads/51/Python/project/instance/pytest1/test_2.py", "-v",
     "--html=/tmp/test_report.html"],
    capture_output=True, text=True
)
print(result)


#
# import pdfplumber
# import pandas as pd
#
# p = pdfplumber.open("//Users/linghuchong/Desktop/ProC迁移指南.pdf")
# print(len(p.pages))
#
# page = p.pages[4]
# # print(page.extract_tables())
# # tables = page.extract_tables()
# # print(pd.DataFrame(tables[0]))
#
# for i in range(len(p.pages)):
#     tables = p.pages[i].extract_tables()
#     if len(tables) > 0:
#         print(f'第{i + 1}页，有{len(tables)}表')
#         for j in range(len(tables)):
#             df = (pd.DataFrame(tables[j]))
#             # 获取 df 的第一行数据作为表头（列名）
#             df_header = df.loc[0,:]
#             # 将之前保存的第一行数据设置为新的列名
#             df.columns = df_header
#             # 从第二行开始截取数据，去掉原来的第一行（表头行）
#             df = df.loc[1:,]
#             # print(df)
#             df.to_excel(f'//Users/linghuchong/Desktop/ProC迁移指南_第{i + 1}页第{j + 1}张表.xlsx', index=False)
#         print("-".center(100, "-"))
#
#
