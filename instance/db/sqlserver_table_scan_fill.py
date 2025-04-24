# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : 数据清洗，扫描表中空缺项，并用0填补
# *********************************************************************
from PO.SqlserverPO import *

# 公卫
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")

table_name = 'a_phs_auth_app'

# 获取表的列名
columns = Sqlserver_PO.select(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
columns_info = {row['COLUMN_NAME']: row['DATA_TYPE'] for row in columns}
# print(columns_info)  # {'status': 'varchar', 'tags': 'varchar', 'summary': 'varchar', 'path': 'varchar', 'method': 'varchar', 'consumes': 'varchar', 'query': 'varchar', 'body': 'varchar', 'case': 'varchar', 'approach': 'varchar', 'rpsStatus': 'float', 'rpsDetail': 'real', 'sql': 'varchar', 'tester': 'varchar', 'updateDate': 'date', 'memo': 'varchar', 'url': 'varchar'}


# 遍历每一列
for column, data_type in columns_info.items():
    if data_type in ['int', 'smallint', 'bigint', 'tinyint', 'decimal', 'numeric', 'float', 'real']:
        # 对于数值类型的列，用 0 填补空缺项
        sql = f"UPDATE {table_name} SET [{column}] = 0 WHERE [{column}] IS NULL"
        # print(f"Executing: {sql}")
        Sqlserver_PO.execute(sql)
    elif data_type in ['varchar', 'char', 'nvarchar', 'nchar', 'text', 'ntext']:
        # 对于字符串类型的列，用空字符串填补空缺项
        sql = f"UPDATE {table_name} SET [{column}] = '' WHERE [{column}] IS NULL"
        # print(f"Executing: {sql}")
        Sqlserver_PO.execute(sql)
    elif data_type in ['date']:
        # 对于日期类型的列，用1900-01-01填补空缺项
        sql = f"UPDATE {table_name} SET [{column}] = '1900-01-01' WHERE [{column}] IS NULL"
        # print(f"Executing: {sql}")
        Sqlserver_PO.execute(sql)
    else:
        print(f"Skipping column {column} with data type {data_type}")


print("空缺项填补完成。")
