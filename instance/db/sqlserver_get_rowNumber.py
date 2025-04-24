# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : 使用ROW_NUMBER()，定位行号
# 使用ROW_NUMBER()，获取某列中为Null值的行号集合，如获取body列中为空值的行号集合
# 使用ROW_NUMBER()，更改第N行的字段值，如修改第三行的query和body值
# 需求，获取两个字段都为Null的行号集合，即先获取两个字段都为Null的行号集合，再提取出交集。
# 处理字典中有多个键值对的通用情况

# *********************************************************************
from PO.SqlserverPO import *
# 公卫
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS", "GBK")


# todo 获取某列中为Null值的行号集合，如获取body列中为空值的行号集合
def get_row_number_with_null(tableName, colName):
    # 获取某字段为Null值的集结行号
    # 执行 SQL 查询，使用 ROW_NUMBER() 函数为结果集添加行号
    query = f"""
        SELECT _{colName}
        FROM (
            SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS _{colName}, {colName}
            FROM {tableName}
        ) subquery
        WHERE {colName} IS NULL
    """
    l_d_rows = Sqlserver_PO.select(query)
    # print(l_d_rows) # [{'_body': 3}, {'_body': 4}, {'_body': 5}]

    l_1 = [v for d in l_d_rows for k, v in d.items()]
    return {colName: l_1}


# print(get_row_number_with_null('a_phs_auth_app', 'body'))  # {'body': [3, 4, 5]}
# print(get_row_number_with_null('a_phs_auth_app', 'query'))  # {'query': [1, 2, 3, 5]}


# todo 需求，获取两个字段都为Null的行号集合，即先获取两个字段都为Null的行号集合，再提取出交集。
dict1 = {'body': [3, 4, 5]}
dict2 = {'query': [1, 2, 3, 5]}
# 提取字典中的值并转换为集合
set1 = set(next(iter(dict1.values())))
set2 = set(next(iter(dict2.values())))

# 计算集合的交集
intersection = set1.intersection(set2)

print("每个字典只有一个键值对时的交集:", intersection)  # {3, 5}
intersection = list(intersection)
print(intersection[0])  # 3
print(intersection[1])  # 5


# todo 处理字典中有多个键值对的通用情况
dict1 = {'body': [3, 4, 5], 'another_key': [6, 7]}
dict2 = {'query': [1, 2, 3, 5], 'yet_another_key': [5, 8]}

# 提取所有值并转换为集合
values1 = [set(v) for v in dict1.values()]
values2 = [set(v) for v in dict2.values()]

# 初始化交集结果
all_intersections = []

# 计算所有可能的交集
for set1 in values1:
    for set2 in values2:
        intersection = set1.intersection(set2)
        if intersection:
            all_intersections.append(intersection)

print("字典中有多个键值对时的所有交集:", all_intersections)  # 字典中有多个键值对时的所有交集: [{3, 5}, {5}]




# todo 更改第N行的字段值，如修改第三行的query和body值
def setValue_with_row_number(tableName, row_number, d_value, valid_field):
    # valid_field 是一个有效的列名，用于连接，必须要有值。如果表中没有唯一标识列，需要根据实际表结构选择合适的列进行连接
    # 构造 SET 子句
    set_clause = ', '.join([f"{column} = '{value}'" for column, value in d_value.items()])
    print(set_clause)  # query = 'test', body = 'hello'
    # 执行更新操作
    update_query = f"""
        UPDATE {tableName}
        SET {set_clause}
        FROM {tableName} t
        JOIN (
            SELECT ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS rn, *
            FROM {tableName}
        ) subquery ON t.[{valid_field}] = subquery.[{valid_field}]
        WHERE subquery.rn = {row_number}
    """
    Sqlserver_PO.execute(update_query)

# 修改第三行的query和body值，前置条件是url有值。
# setValue_with_row_number('a_phs_auth_app', 3, {'query': 'peter', 'body':'2010-12-12'}, 'url')
# setValue_with_row_number('a_phs_auth_app', 4, {'updateDate':'2020-12-22','body': 'hello', 'query': 'test'})
# setValue_with_row_number('a_phs_auth_app', 3, {'updateDate':'2030-12-22'})
