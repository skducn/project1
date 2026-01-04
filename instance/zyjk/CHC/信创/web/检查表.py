# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-12-22
# Description: 社区健康5G 信创1.0 - 检查表
# 需求：/Users/linghuchong/Desktop/智赢健康/信创/社区健康管理中心系统信创版本V1.0.docx
# 5G项目三个数据库，CHC、CHCCONFIG、CHC_JOB
# 要求：检查三个数据库中的表，并检查表是否存在，比对需初始数据输出有差异的记录。
# c1, 检查要求初始化数据的表
# c2, 检查要求去掉的表

#***************************************************************
from PO.SqlserverPO import *

from PO.OpenpyxlPO import *
Openpyxl_PO = OpenpyxlPO("./5G.xlsx")

def delField(varTable, l_row_title, l_varField, Sqlserver_PO):
    # 删除某些字段，如动态的值或无用的ID值（手工删除excel中无用字段，如ID， 去掉数据库表无用字段，如CREATE_DATE）
    # 确保excel表格字段与数据库表字段可比较。
    # l_d_ = delField(check, l_row_title, ["CREATE_DATE"], Sqlserver_PO)

    # exclude_fields = varField  # 需要排除的字段列表
    all_fields = [field for field in l_row_title if field not in l_varField]
    print(25,all_fields)
    fields_str = ', '.join(all_fields)
    l_d_ = Sqlserver_PO.select("SELECT %s FROM %s" % (fields_str, varTable))
    return l_d_


def main(db, excel, check_type="init"):
    Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", db, "utf8")
    d_table_comment = Sqlserver_PO.getTableComment(format=False)
    # print(d_table_comment) # {'a_autoIdcard': None, 'a_ceshiguize': '(测试用)测试规则',...
    rows1 = Openpyxl_PO.getTotalRowCol(db)[0]
    if check_type == "init":
        Color_PO.outColor([{"36": db + "，检查初始化数据的表，输出有差异的记录"}])
        for i in range(1, rows1):
            l_tmp = Openpyxl_PO.getOneRow(i+1, db)
            # 是否初始数据
            if l_tmp[3] == "是":
                Color_PO.outColor([{"30": db + " - " + l_tmp[0] + "（" + l_tmp[1] + "）"}])
                varTable = l_tmp[0]
                Openpyxl_PO2 = OpenpyxlPO(excel, varTable)
                l_row_title = Openpyxl_PO2.getOneRow(1, varTable)
                # print(l_row_title) # ['ID', 'SYSTEM_ID', 'NAME', 'PARENT_ID', 'URL', 'COMPONENT', 'ICON', 'HIDDEN', 'AFFIX', 'ABI_ID', 'IS_SCREEN']
                rows2 = Openpyxl_PO2.getTotalRowCol(varTable)[0]
                # 部分表，需去掉无用字段
                if varTable == 'T_INTERVENE_CONFIG':
                    l_d_ = delField(varTable, l_row_title, ["CREATE_DATE"], Sqlserver_PO)
                else:
                    l_d_ = Sqlserver_PO.select("SELECT * FROM %s" % (varTable))
                result_list = [[item[field] for field in l_row_title] for item in l_d_]
                # 过滤掉字段内容中换行符
                result_list = [
                    [str(field).replace('\r\n', '').replace('\n', '').replace('\r', '') if field is not None else '' for
                     field in item] for item in result_list]

                # 比对表格与数据库表字段值是否相同，输出有差异的记录。
                for j in range(1, rows2):
                    l_row = Openpyxl_PO2.getOneRow(j+1, varTable)
                    target_list = [str(item).replace('\r\n', '').replace('\n', '').replace('\r', '') if item is not None else '' for item in l_row]
                    if target_list != result_list[j-1]:
                        Color_PO.outColor([{"30": j}, {"31": '文档 => ' + str(target_list)}])
                        Color_PO.outColor([{"30": j}, {"34": '库表 => ' + str(result_list[j-1]) + "\n"}])

    elif check_type == "remove":
        Color_PO.outColor([{"35": db + ", 要求去掉的表:"}])
        for i in range(1, rows1):
            l_tmp = Openpyxl_PO.getOneRow(i+1, db)
            if l_tmp[2] == "不要":
                if l_tmp[0] in d_table_comment:
                    Color_PO.outColor([{"30": l_tmp[0]}, {"31": l_tmp[1]}])
    else:
        Color_PO.outColor([{"36": db + ", 要求初始化数据的表:"}])
        for i in range(1, rows1):
            l_tmp = Openpyxl_PO.getOneRow(i + 1, db)
            if l_tmp[3] == "是":
                Color_PO.outColor([{"30": l_tmp[0]}, {"31": l_tmp[1]}])
        print("----------------------------------------------")
        Color_PO.outColor([{"35": db + ", 要求去掉的表:"}])
        for i in range(1, rows1):
            l_tmp = Openpyxl_PO.getOneRow(i + 1, db)
            if l_tmp[2] == "不要":
                if l_tmp[0] in d_table_comment:
                    Color_PO.outColor([{"30": l_tmp[0]}, {"31": l_tmp[1]}])
    print("----------------------------------------------")



# main("CHC", "./CHC.xlsx", check_type="init")
main("CHCCONFIG", "./CHCCONFIG.xlsx", check_type="init")
# main("CHC_JOB", check_type="init")






