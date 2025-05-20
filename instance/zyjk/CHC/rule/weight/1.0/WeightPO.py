# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0 评估因素判断规则自动化,
# 需求：体重管理1.18
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r
#***************************************************************
# 警告如下：D:\dwp_backup\python study\GUI_wxpython\lib\site-packages\openpyxl\worksheet\_reader.py:312: UserWarning: Unknown extension is not supported and will be removed warn(msg)
# 解决方法：
import sys
import warnings
warnings.simplefilter("ignore")
# *****************************************************************
# 要切换到 $ cd /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/EHR/rule 下执行 python p_main.py
# sys.path.append("../../../../")
# sys.path.append("/Users/linghuchong/Downloads/51/Python/project")

import random, re
import subprocess, json

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO_CHC5G = SqlserverPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"))  # 测试环境
Sqlserver_PO_CHC = SqlserverPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database2"))  # 测试环境

from AgePO import *
Age_PO = AgePO()

from BmiPO import *
Bmi_PO = BmiPO()

from BmiAgePO import *
BmiAge_PO = BmiAgePO()

from BmiAgeSexPO import *
BmiAgeSex_PO = BmiAgeSexPO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.LogPO import *
Log_PO = LogPO(filename='log.log', level="info")


class WeightPO():

    def __init__(self):
        self.tableWS = Configparser_PO.DB("tableWS")
        self.tableER = Configparser_PO.DB("tableER")
        self.tableIR = Configparser_PO.DB("tableIR")

    def convert_conditions(self, conditions):
        valid_operators = ['=', '>', '<', '>=', '<=']
        result = []

        for condition in conditions:
            operator_pos = -1
            current_op = None
            for op in sorted(valid_operators, key=len, reverse=True):
                pos = condition.find(op)
                if pos != -1:
                    operator_pos = pos
                    current_op = op
                    break

            if operator_pos == -1:
                continue  # 忽略无法解析的条件

            left = condition[:operator_pos].strip()
            right = condition[operator_pos + len(current_op):].strip()

            if left and right:
                result.append(f"{left}{current_op}{right}")

        return " and ".join(result)

    def excel2db_ER(self, varFile, varSheet, varTable):

        # excel文件导入db

        # 1, db中删除已有的表
        Sqlserver_PO_CHC5G.execute("drop table if exists " + varTable)

        # 2, excel导入db
        Sqlserver_PO_CHC5G.xlsx2db(varFile, varTable, varSheet)

        # 3, 设置表注释
        Sqlserver_PO_CHC5G.setTableComment(varTable, '体重管理1.0_评估因素规则库_自动化')

        # 4， 替换换行符为空格
        Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_ER = REPLACE(REPLACE(f_ER, CHAR(10), ' '), CHAR(13), ' ');" % (varTable))

        # 5, 设置字段类型与描述
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_result', 'varchar(50)', '结果')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_updateDate', 'varchar(50)', '更新日期')
        Sqlserver_PO_CHC5G.execute("ALTER TABLE %s ALTER COLUMN f_updateDate DATE;" % (varTable))
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_type', 'varchar(50)', '分类')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_crowd', 'varchar(50)', '人群分类')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_crowdCode', 'varchar(50)', '人群分类编码')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ageType', 'varchar(50)', '年龄类型')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ruleName', 'varchar(100)', '规则名称')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_detail', 'varchar(999)', '评估规则详细描述')
        # # Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ER_O', 'varchar(999)', '评估因素判断规则_原始')  //不用，没处理。
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ER', 'varchar(8000)', '评估因素判断规则')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ERcode', 'varchar(50)', '评估规则编码')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_testcase', 'varchar(100)', '测试用例', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_caseTotal', 'varchar(10)', '测试数量', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_errInfo', 'varchar(8000)', '错误信息', "utf-8")

        # 6, 设置自增主键（最后）
        Sqlserver_PO_CHC5G.setIdentityPrimaryKey(varTable, "ID")

    def excel2db_HIRB(self, varFile, varSheet, varTable):

        # excel文件导入db

        # 1, db中删除已有的表
        Sqlserver_PO_CHC5G.execute("drop table if exists " + varTable)

        # 2, excel导入db
        Sqlserver_PO_CHC5G.xlsx2db(varFile, varTable, varSheet)

        #  -- 修改表字符集
        # Sqlserver_PO_CHC5G.execute("ALTER TABLE %s CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" % (varTable))
                            # ALTER TABLE youCONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        #

        # 3, 设置表注释
        Sqlserver_PO_CHC5G.setTableComment(varTable, '体重管理1.0_健康干预规则库（其他分类)_自动化')

        # 4， 替换换行符为空格
        Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_IR = REPLACE(REPLACE(f_IR, CHAR(10), ' '), CHAR(13), ' ');" % (varTable))

        # # 5, 设置字段类型与描述
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_result', 'varchar(50)', '结果', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_updateDate', 'varchar(50)', '更新日期', "utf-8")
        Sqlserver_PO_CHC5G.execute("ALTER TABLE %s ALTER COLUMN f_updateDate DATE;" % (varTable))
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_type', 'varchar(50)', '分类', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_IRcode', 'varchar(50)', '干预规则编码', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_IR', 'varchar(8000)', '干预规则', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_detail', 'varchar(8000)', '干预规则描述', "utf-8")

        # 6, 设置自增主键（最后）
        Sqlserver_PO_CHC5G.setIdentityPrimaryKey(varTable, "ID")

    def excel2db_WS(self, varFile, varSheet, varTable):

        # excel文件导入db

        # 1, db中删除已有的表
        Sqlserver_PO_CHC5G.execute("drop table if exists " + varTable)

        # 2, excel导入db
        Sqlserver_PO_CHC5G.xlsx2db(varFile, varTable, varSheet)

        # 3, 设置表注释
        Sqlserver_PO_CHC5G.setTableComment(varTable, '体重管理1.0_体重状态_自动化')

        # 4， 替换换行符为空格
        Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_value = REPLACE(REPLACE(f_value, CHAR(10), ' '), CHAR(13), ' ');" % (varTable))

        # # 5, 设置字段类型与描述
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_result', 'varchar(50)', '结果', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_updateDate', 'varchar(50)', '更新日期', "utf-8")
        Sqlserver_PO_CHC5G.execute("ALTER TABLE %s ALTER COLUMN f_updateDate DATE;" % (varTable))
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_type', 'varchar(50)', '人群分类', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_typeCode', 'varchar(50)', '人群分类编码', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_weightStatus', 'varchar(50)', '体重状态', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_weightStatusCode', 'varchar(50)', '体重状态编码', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_value', 'varchar(8000)', '取值', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_testcase', 'varchar(100)', '测试用例', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_caseTotal', 'varchar(10)', '测试数量', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_errInfo', 'varchar(8000)', '错误信息', "utf-8")

        # 6, 设置自增主键（最后）
        Sqlserver_PO_CHC5G.setIdentityPrimaryKey(varTable, "ID")

    def main(self, varTable, varRun='all'):

        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_result, f_updateDate, f_ruleName, f_ER, f_ERcode from %s" % (varTable))
        # print("l_d_row => ", l_d_row)
        # [{'id': 1, 'f_result': None, 'f_updateDate': None, 'f_ruleName': '成人体重超重或肥胖',
        # 'f_evaluationFactorJudgmentRules_N': 'BMI>=24 and 年龄>=18 and 年龄<65', 'f_evaluationRuleCoding': 'TZ_STZB001'}, ...

        # 测试某条记录
        for i, index in enumerate(l_d_row):
            # i = 7
            id = l_d_row[i]['ID']
            f_result = l_d_row[i]['f_result']
            f_updateDate = l_d_row[i]['f_updateDate']
            f_ruleName = l_d_row[i]['f_ruleName']
            f_ER = l_d_row[i]['f_ER']
            f_ERcode = l_d_row[i]['f_ERcode']

            # 获取原始数据
            Color_PO.outColor([{"34": "id:" + str(id) + ", f_ER: " + str(f_ER)}])
            # print("原始数据 >", f_ER)  # (14<= 年龄＜14.5 and 22.3<= BMI and 性别=男) or (14.5<= 年龄＜15 and 22.6<= BMI and 性别=男)

            # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
            f_ER = f_ER.replace("月", '')
            f_ER = f_ER.replace('＞', '>').replace('＜', '<').replace('＝', '=')
            f_ER = re.sub(r'\s*<=\s*', '<', f_ER)
            f_ER = re.sub(r'\s*<=\s*', '<=', f_ER)
            f_ER = re.sub(r'\s*<=\s*', '>', f_ER)
            f_ER = re.sub(r'\s*<=\s*', '>=', f_ER)
            f_ER = re.sub(r'\s*<=\s*', '=', f_ER)

            # 优先处理or，再处理and
            if "or" in f_ER:
                # print("[or]")

                # 结构化原始数据为列表，生成l_l_N
                l_N = f_ER.split("or")
                l_N = [i.replace("(",'').replace(")",'').strip() for i in l_N]
                l_N = [i.split("and") for i in l_N]
                l_l_N = [[item.strip() for item in sublist] for sublist in l_N]
                # print(l_l_N)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
                # print(len(l_l_N))  # 16 ， 16个组合条件

                varCount = 0
                l_1 = []
                # 遍历所有条件，生成满足的数据和不满足的数据，生成d_cases，（3个条件，就是2的3次方，8条数据，以此类推）
                for lln in l_l_N:

                    l_1 = []
                    for i in lln:
                        if "BMI" in i:
                            l_simple_conditions = BmiAgeSex_PO.split_compound_condition(i)
                            l_1.extend(l_simple_conditions)
                        elif "年龄" in i:
                            l_simple_conditions = BmiAgeSex_PO.split_compound_condition(i)
                            l_1.extend(l_simple_conditions)
                        else:
                            l_1.append(i)
                    print(l_1)

                    d_cases = BmiAgeSex_PO.generate_all_cases(l_1)
                    # print(d_cases)  # {'satisfied': [{'BMI': 47.2, '年龄': 14.0, '性别': '男'}], 'BMI满足且年龄满足且性别不满足': [{'BMI': 47.2, '年龄': 14.4, '性别': '女'}],...
                    # print(len(d_cases))  # 8

                    # 正向用例，满足条件的d_cases['satisfied'][0]，预期要命中
                    varCount = self.checkRule3(d_cases['satisfied'][0], id, f_ERcode, varTable)
                    if varCount == 1:
                        print("ok > 条件：", lln, "，测试数据：", d_cases['satisfied'][0] , " > 命中。")

                        # 反向用例, 不满足条件的v[0]，预期不命中。
                        del d_cases['satisfied']
                        varCount = 2
                        for k, v in d_cases.items():
                            # print(v[0])
                            varCount = self.checkRule4(v[0], id, f_ERcode, varTable)
                            if varCount == 1:
                                # 反向如果命中就错，并且终止循环
                                print("error > 条件：", lln, "，测试数据：", v[0], " > 命中！")
                                break
                            else:
                                print("ok > 条件：", lln, "，测试数据：", v[0], " > 不命中。")
                                Ellipsis
                    else:
                        print("error > 条件：", lln, "，测试数据：", d_cases['satisfied'][0] , " > 不命中！")
                        Ellipsis
                        # Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

                # 回写数据库f_resut, f_updateDate
                if varCount == 2:
                    print("ok")
                    Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
                else:
                    print("error")
                    Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

            elif "and" in f_ER:
                # print("[and]")
                l_N = f_ER.split("and")
                l_N = [i.strip() for i in l_N]
                # print(l_N)  # ['BMI>=24', '年龄>=18', '年龄<65']

                # 判断条件中有哪些字段，如 年龄、BMI
                bmi_conditions = [c for c in l_N if c.startswith('BMI')]
                # print("bmi_conditions", bmi_conditions)
                age_conditions = [c for c in l_N if c.startswith('年龄')]
                # print("age_conditions", age_conditions)

                # 只读取年龄
                if len(bmi_conditions) == 0 and len(age_conditions) != 0:
                    d_cases = Age_PO.generate_all_cases(l_N)
                # 只读取BMI
                elif len(bmi_conditions) != 0 and len(age_conditions) == 0:
                    d_cases = Bmi_PO.generate_all_cases(l_N)
                # 读取年龄和BMI
                elif len(bmi_conditions) != 0 and len(age_conditions) != 0:
                    d_cases = BmiAge_PO.generate_all_cases(l_N)
                # print(d_cases)

                # 正向用例，满足条件的d_cases['satisfied'][0]，预期要命中
                varCount = self.checkRule3(d_cases['satisfied'][0], id, f_ERcode, varTable)
                if varCount == 1:
                    print("ok > 条件：", l_N, "，测试数据：", d_cases['satisfied'][0], " > 命中。")

                    # 反向用例, 不满足条件的v[0]，预期不命中。
                    del d_cases['satisfied']
                    varCount = 2
                    for k, v in d_cases.items():
                        # print(v[0])
                        varCount = self.checkRule4(v[0], id, f_ERcode, varTable)
                        if varCount == 1:
                            # 反向如果命中就错，并且终止循环
                            print("error > 条件：", l_N, "，测试数据：", v[0], " > 命中！")
                            break
                        else:
                            print("ok > 条件：", l_N, "，测试数据：", v[0], " > 不命中。")
                            Ellipsis
                else:
                    print("error > 条件：", l_N, "，测试数据：", d_cases['satisfied'][0], " > 不命中！")
                    Ellipsis
                    # Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

                # 回写数据库f_resut, f_updateDate
                if varCount == 2:
                    print("ok")
                    Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
                else:
                    print("error")
                    Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

            elif ("<" in f_ER or ">" in f_ER or "<=" in f_ER or ">=" in f_ER):
                ...
                # l_N = [i.strip() for i in l_N]
                # print(f_ER)
                l_N= []
                l_N.append(f_ER)
                # print(l_N)  # ['BMI>=24', '年龄>=18', '年龄<65']
                # 判断条件中有哪些字段，如 年龄、BMI
                bmi_conditions = [c for c in l_N if c.startswith('BMI')]
                # print("bmi_conditions", bmi_conditions)
                age_conditions = [c for c in l_N if c.startswith('年龄')]
                # print("age_conditions", age_conditions)

                # 只读取年龄
                if len(bmi_conditions) == 0 and len(age_conditions) != 0:
                    d_cases = Age_PO.generate_all_cases(l_N)
                # 只读取BMI
                elif len(bmi_conditions) != 0 and len(age_conditions) == 0:
                    d_cases = Bmi_PO.generate_all_cases(l_N)

                # 正向用例，满足条件的d_cases['satisfied'][0]，预期要命中
                varCount = self.checkRule3(d_cases['satisfied'][0], id, f_ERcode, varTable)
                if varCount == 1:
                    print("ok > 条件：", l_N, "，测试数据：", d_cases['satisfied'][0], " > 命中。")

                    # 反向用例, 不满足条件的v[0]，预期不命中。
                    del d_cases['satisfied']
                    varCount = 2
                    for k, v in d_cases.items():
                        # print(v[0])
                        varCount = self.checkRule4(v[0], id, f_ERcode, varTable)
                        if varCount == 1:
                            # 反向如果命中就错，并且终止循环
                            print("error > 条件：", l_N, "，测试数据：", v[0], " > 命中！")
                            break
                        else:
                            print("ok > 条件：", l_N, "，测试数据：", v[0], " > 不命中。")
                            Ellipsis
                else:
                    print("error > 条件：", l_N, "，测试数据：", d_cases['satisfied'][0], " > 不命中！")
                    Ellipsis
                    # Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

                # 回写数据库f_resut, f_updateDate
                if varCount == 2:
                    print("ok")
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
                else:
                    print("error")
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

            else:
                print("[not or & and ]")
            print("-".center(100, "-"))




    # 判定居民体重状态 Determine Residents' Weight Status
    def DRWS(self, varTestID="all"):

        # 判定居民体重状态 Determine Residents' Weight Status
        # a_weight10_WS

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_value from %s" % (self.tableWS))
        # print("l_d_row =>", l_d_row)  # [{'ID': 1, 'f_value': 'BMI＜18.5'}, ...
        if varTestID > len(l_d_row):
            print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围" )
            sys.exit(0)

        for i in enumerate(l_d_row):
            i = varTestID - 1
            ID = l_d_row[i]['ID']
            f_value = l_d_row[i]['f_value']

            # 获取原始数据
            print("判定居民体重状态DRWS => {表: " + self.tableWS + ", ID: " + str(ID) + ", 条件: " + str(f_value) + "}")
            Log_PO.logger.info("判定居民体重状态DRWS => {'表': '" + self.tableWS + "', 'ID': " + str(ID) + "}")

            # 统计所有组合的数量
            varTestCount = f_value.count("or")
            # print(varTestCount)  # 输出or的数量: 2

            # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
            f_value = f_value.replace("月", '')
            f_value = f_value.replace('＞', '>').replace('＜', '<').replace('＝', '=')

            # todo DRWS 复杂条件组合
            if "or" in f_value:
                # 转换列表，结构化原始数据为列表，生成l_l_N
                l_value = f_value.split("or")
                l_value = [i.replace("(",'').replace(")",'').strip() for i in l_value]
                l_value = [i.split("and") for i in l_value]
                l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
                # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...

                l_result = []
                sum = 0
                for lln in range(len(l_l_value)):
                    l_2_value = []
                    # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                    # print(l_l_value(lln))
                    for i in l_l_value[lln]:
                        if "BMI" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                        if "年龄" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                        elif "性别" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                    # print("611 分解参数 =", l_2_value)

                    # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                    l_3_value = []
                    for i in l_2_value:
                        l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                        l_3_value.extend(l_simple_conditions)
                    # print("618 结构化参数 =", l_3_value)

                    # 读取BmiAgeSex模块，生成随机数据d_cases
                    # d_cases = BmiAgeSex_PO.generate_all_cases(l_3_value)

                    for i in l_3_value:
                        if ('>=' or '<=') in i:
                            if '年龄' in i:
                                d_cases = BmiAgeSex_PO.main(l_3_value)
                                break
                            if 'BMI' in i:
                                d_cases = BmiAgeSex_PO.main(l_3_value)
                                break
                        else:
                            d_cases = BmiAgeSex_PO.main(l_3_value)

                    print("--------------------")
                    if Configparser_PO.SWITCH("testDataSet") == "on":
                        print("测试数据集合 =>", d_cases)

                    # 判断输出结果
                    # todo DRWS_case_or for or
                    varTestcase, varCount = self.DRWS_case_or(d_cases, ID, l_2_value, lln+1, varTestCount+1)
                    l_result.append(varCount)
                    sum = sum + varTestcase

                # print(l_result)

                # 回写数据库f_resut, f_updateDate
                if 0 not in l_result:
                    Color_PO.outColor([{"32": "ID = " + str(ID) + ", => ok"}])
                    Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, sum, ID))

                else:
                    Color_PO.outColor([{"32": "ID = " + str(ID) + ", => error"}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, sum, ID))

            # todo DRWS 简单条件组合
            elif "and" in f_value:

                # 转换成列表
                l_value = f_value.split("and")
                l_value = [i.strip() for i in l_value]
                print("730 实际参数 =>", l_value)  # ['18.5<BMI', 'BMI<24.0']

                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                for i in l_value:
                    l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                    l_2_value.extend(l_simple_conditions)
                print("737 分解参数 =>", l_2_value)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                l_3_value = []
                for i in l_2_value:
                    l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                    l_3_value.extend(l_simple_conditions)
                print("744 结构化参数 =>", l_3_value)  #  ['BMI>18.5', 'BMI<24.0']

                # 读取BMI模块，生成随机数据d_cases
                d_cases = BmiAgeSex_PO.generate_all_cases(l_3_value)

                # 测试数据
                # todo DRWS_case for and
                self.DRWS_case(d_cases, ID, l_value)

            # todo DRWS 无条件组合
            elif "and" not in f_value:

                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                l_simple_conditions = Bmi_PO.splitMode(f_value)
                l_2_value.extend(l_simple_conditions)
                # print("517 分解条件 =>", l_2_value)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                l_3_value = []
                for i in l_2_value:
                    l_simple_conditions = Bmi_PO.interconvertMode(i)
                    l_3_value.extend(l_simple_conditions)
                # print("548 结构化参数 =", l_3_value)  # ['BMI<18.5']

                # 读取BMI模块，生成随机数据d_cases
                d_cases = Bmi_PO.generate_all_cases(l_3_value)
                if Configparser_PO.SWITCH("testDataSet") == "on":
                    print("测试数据集合 =>", d_cases)  # {'satisfied': [{'BMI': 16.8}], 'not1': [{'BMI': 19.6}]}
                    Log_PO.logger.info("测试数据集合 => " + str(d_cases))

                # todo DRWS_case for not and
                # 测试数据
                self.DRWS_case(d_cases, ID, l_2_value)

            else:
                print("[not or & and ]")
            print("-".center(100, "-"))

            break
    def DRWS_case(self, d_cases, ID, l_2_value):

        # d_cases = {'satisfied': [{'BMI': 14.2}], 'not1': [{'BMI': 53.4}]}
        # ID = 1
        # l_2_value = ['BMI<18.5']

        varTestcase = 0

        if len(d_cases['satisfied']) == 1:
            # 一条数据，正向用例
            l_count = []
            # todo DRWS_run_p_1
            d_tmp = self.DRWS_run_p(d_cases['satisfied'][0], ID)
            d_1 = {}
            if d_tmp['result'] == 1:
                d_1['正向'] = 'ok'
                d_1['条件'] = l_2_value
                d_1['测试数据'] = d_cases['satisfied'][0]
                Color_PO.outColor([{"34": d_1}])
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\","\\")
                Log_PO.logger.info(s_tmp)
                l_count.append(1)
            else:
                d_1['正向'] = 'error'
                d_1['条件'] = l_2_value
                d_1['测试数据'] = d_cases['satisfied'][0]
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Log_PO.logger.info(s_tmp)
                Color_PO.outColor([{"31": s_tmp}])
                l_count.append(0)
            varTestcase = varTestcase + 1

            # 一条数据，反向用例
            # todo DRWS_run_n
            if Configparser_PO.SWITCH('testNegative') == "on":
                d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], ID)
                d_2 = {}
                if d_tmp['result'] == 1:
                    d_2['反向'] = 'error'
                    d_2['条件'] = l_2_value
                    d_2['测试数据'] = d_cases['notSatisfied'][0]
                    d_2.update(d_tmp)
                    s_tmp = str(d_2)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    l_count.append(0)
                else:
                    d_2['反向'] = 'ok'
                    d_2['条件'] = l_2_value
                    d_2['测试数据'] = d_cases['notSatisfied'][0]
                    Color_PO.outColor([{"36": d_2}])
                    d_2.update(d_tmp)
                    s_tmp = str(d_2)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    l_count.append(1)
                varTestcase = varTestcase + 1

            # 回写数据库f_resut, f_updateDate
            if 0 not in l_count:
                s = "{ID: " + str(ID) + "} => ok"
                Color_PO.outColor([{"32": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, varTestcase, ID))
            else:
                s = "{ID: " + str(ID) + "} => error"
                Color_PO.outColor([{"32": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, varTestcase, ID))
            Log_PO.logger.info("---------------------------------------------------------------------")

        else:
            # 正向用例, N个数据
            l_count = []
            for i in range(len(d_cases['satisfied'])):
                # print(d_cases)
                # todo DRWS_run_p_n
                d_tmp = self.DRWS_run_p(d_cases['satisfied'][i], ID)
                d_1 = {}
                if d_tmp['result'] == 1:
                    # s_print = "{'正向': 'ok', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    # Color_PO.outColor([{"34": s_print}])
                    # Log_PO.logger.info(s_print)
                    # l_count.append(1)
                    d_1['正向'] = 'ok'
                    d_1['条件'] = l_2_value
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    Color_PO.outColor([{"34": d_1}])
                    d_1.update(d_tmp)
                    s_tmp = str(d_1)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    l_count.append(1)
                    varTestcase = varTestcase + 1
                else:
                    d_1['正向'] = 'error'
                    d_1['条件'] = l_2_value
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1.update(d_tmp)
                    s_tmp = str(d_1)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    l_count.append(0)
                    varTestcase = varTestcase + 1

            # 反向用例, N个数据
            if Configparser_PO.SWITCH('testNegative') == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    # todo DRWS_run_n_n
                    d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][i], ID)
                    d_2 = {}
                    if d_tmp['result'] == 1:
                        # 反向如果命中就错，并且终止循环
                        d_2['反向'] = 'error'
                        d_2['条件'] = l_2_value
                        d_2['测试数据'] = d_cases['notSatisfied'][i]
                        d_2.update(d_tmp)
                        s_tmp = str(d_2)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])
                        l_count.append(0)
                        varTestcase = varTestcase + 1
                    else:
                        d_2['反向'] = 'ok'
                        d_2['条件'] = l_2_value
                        d_2['测试数据'] = d_cases['notSatisfied'][i]
                        Color_PO.outColor([{"36": d_2}])
                        d_2.update(d_tmp)
                        s_tmp = str(d_2)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        l_count.append(1)
                        varTestcase = varTestcase + 1

            # 回写数据库f_resut, f_updateDate
            if 0 not in l_count:
                s_print = "{'ID': " + str(ID) + "} => ok"
                Color_PO.outColor([{"32": s_print}])
                Log_PO.logger.info([{"32": s_print}])
                Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, varTestcase, ID))
            else:
                s_print = "{'ID': " + str(ID) + "} => error"
                Color_PO.outColor([{"31": s_print}])
                Log_PO.logger.info([{"31": s_print}])
                Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, varTestcase, ID))
    def DRWS_case_or(self, d_cases, id, l_2_value, Numerator, Denominator):

        varTestcase = 0

        if len(d_cases['satisfied']) == 1:
            # 一条数据，正向用例
            l_count = []
            d_tmp = self.DRWS_run_p(d_cases['satisfied'][0], id)
            d_1 = {}
            if d_tmp['result'] == 1:
                d_1['No.'] = str(Numerator) + "/" + str(Denominator)
                d_1['正向'] = 'ok'
                d_1['条件'] = l_2_value
                d_1['测试数据'] = d_cases['satisfied'][0]
                Color_PO.outColor([{"34": d_1}])
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Log_PO.logger.info(s_tmp)

                # s_print = str(Numerator) + "/" + str(Denominator) + ", {'正向': 'ok', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][0]) + "}"
                # Color_PO.outColor([{"34": s_print}])
                # Log_PO.logger.info(s_print)
                l_count.append(1)
            else:
                d_1['No.'] = str(Numerator) + "/" + str(Denominator)
                d_1['正向'] = 'error'
                d_1['条件'] = l_2_value
                d_1['测试数据'] = d_cases['satisfied'][0]
                # Color_PO.outColor([{"34": d_1}])
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Log_PO.logger.info(s_tmp)
                Color_PO.outColor([{"31": d_tmp}])
                l_count.append(0)
                # s_print = "{'正向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][0]) + "}"
                # Color_PO.outColor([{"31": s_print}])
                # Log_PO.logger.info(s_print)
                # Color_PO.outColor([{"33": d_tmp}])
                # Log_PO.logger.info(d_tmp)

                # Color_PO.outColor([{"31": "ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(d_cases['satisfied'][0])}])
                # Color_PO.outColor([{"31":"run接口：", "33": d_tmp["i"].replace("\\\\", "\\")}])
                # Color_PO.outColor([{"31":"查询1：", "33": d_tmp['WEIGHT_REPORT_WEIGHT_STATUS']}])
                # Color_PO.outColor([{"31":"查询2：", "33": d_tmp['QYYH_WEIGHT_STATUS']}])
                # Color_PO.outColor([{"31":"f_weightStatusCode预期值：", "33": d_tmp['f_weightStatusCode预期值']}])
                # Color_PO.outColor([{"31":"WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])
                # Color_PO.outColor([{"31":"WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])

                # # 将错误条件写入数据库，以备复测。
                # l_d_row = Sqlserver_PO_CHC5G.select(
                #     "select f_type, f_typeCode,f_weightStatus,f_weightStatusCode from %s where ID=%s" % (
                #     self.tableWS, id))
                # # print(l_d_row)
                # f_type1 = l_d_row[0]['f_type']
                # f_typeCode1 = l_d_row[0]['f_typeCode']
                # f_weightStatus1 = l_d_row[0]['f_weightStatus']
                # f_weightStatusCode1 = l_d_row[0]['f_weightStatusCode']
                # f_errInfo1 = d_tmp
                # 将列表转换字符串
                # f_2_value = (self.convert_conditions(l_2_value))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                # Sqlserver_PO_CHC5G.execute("insert into %s (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID) values (%s,%s,%s,%s,'%s',%s) "
                #                            % (varTable, f_type1, f_typeCode1, f_weightStatus1, f_weightStatusCode1, str(l_2_value), int(id)))
                # sql = """
                #       INSERT INTO [%s]
                #       (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID, f_errInfo)
                #       VALUES ('%s', '%s', '%s', '%s', '%s', %d, '%s')
                #   """ % (
                #     self.tableWS,
                #     f_type1,
                #     f_typeCode1,
                #     f_weightStatus1,
                #     f_weightStatusCode1,
                #     str(f_2_value).replace("'", "''"),  # 防止内部有单引号导致 SQL 错误
                #     int(id),
                #     f_errInfo1
                # )
                # Sqlserver_PO_CHC5G.execute(sql)

                # 将错误条件写入数据库，以备复测。
                # 将列表转换字符串
                f_2_value = (self.convert_conditions(l_2_value))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                d_tmp['条件'] = str(f_2_value)
                d_tmp['测试数据'] = str(d_cases['notSatisfied'][0])
                d_tmp['用例类型'] = "正向不满足"
                s_tmp = str(d_tmp)
                s_tmp = s_tmp.replace("'", "''")
                s_tmp = s_tmp.replace("\\\\", "\\")
                # print(d_tmp)
                Sqlserver_PO_CHC5G.execute(
                    "insert into %s (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID, f_errInfo) values ('%s','%s','%s','%s','%s',%s,'%s') "
                    % (self.tableWS, d_tmp['人群分类'], d_tmp['人群分类编码'], d_tmp['体重状态'], d_tmp['体重状态编码'], d_tmp['条件'], id, s_tmp))
            varTestcase = varTestcase + 1

            # 一条数据，反向用例
            if Configparser_PO.SWITCH("testNegative") == "on":
                d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], id)
                d_2 = {}
                if d_tmp['result'] == 1:
                    d_2['No.'] = str(Numerator) + "/" + str(Denominator)
                    d_2['反向'] = 'error'
                    d_2['条件'] = l_2_value
                    d_2['测试数据'] = d_cases['notSatisfied'][0]
                    d_2.update(d_tmp)
                    s_tmp = str(d_2)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    l_count.append(0)

                    # s_print = "{'反向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['notSatisfied'][0]) + "}"
                    # Color_PO.outColor([{"31": s_print}])
                    # Log_PO.logger.info(s_print)
                    # Color_PO.outColor([{"33": d_tmp}])
                    # Log_PO.logger.info(d_tmp)
                    # l_count.append(0)

                    # 将错误条件写入数据库，以备复测。
                    # 将列表转换字符串
                    f_2_value = (self.convert_conditions(l_2_value))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                    d_tmp['条件'] = str(f_2_value)
                    d_tmp['测试数据'] = str(d_cases['notSatisfied'][0])
                    d_tmp['用例类型'] = "反向满足"
                    s_tmp = str(d_tmp)
                    s_tmp = s_tmp.replace("'", "''")
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    # print(d_tmp)
                    Sqlserver_PO_CHC5G.execute(
                        "insert into %s (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID, f_errInfo) values ('%s','%s','%s','%s','%s',%s,'%s') "
                        % (self.tableWS, d_tmp['人群分类'], d_tmp['人群分类编码'], d_tmp['体重状态'], d_tmp['体重状态编码'], d_tmp['条件'], id, s_tmp))
                else:
                    d_2['No.'] = str(Numerator) + "/" + str(Denominator)
                    d_2['反向'] = 'ok'
                    d_2['条件'] = l_2_value
                    d_2['测试数据'] = d_cases['notSatisfied'][0]
                    Color_PO.outColor([{"31": d_2}])
                    d_2.update(d_tmp)
                    s_tmp = str(d_2)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    l_count.append(1)
                    # s_print = "{'反向': 'ok', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['notSatisfied'][0]) + "}"
                    # Color_PO.outColor([{"36": s_print}])
                    # Log_PO.logger.info(s_print)
                    # l_count.append(1)
                varTestcase = varTestcase + 1

            if 0 in l_count:
                s = "{'ID': " + str(id) + ", '合计数': " + str(l_count) + "}"
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                return varTestcase, 0
            else:
                return varTestcase, 1
        else:
            # 正向用例, N个数据
            l_count = []
            for i in range(len(d_cases['satisfied'])):
                d_tmp = self.DRWS_run_p(d_cases['satisfied'][i], id)
                d_1 = {}
                if d_tmp['result'] == 1:
                    d_1['No.'] = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator)
                    d_1['正向'] = 'ok'
                    d_1['条件'] = l_2_value
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    Color_PO.outColor([{"34": d_1}])
                    d_1.update(d_tmp)
                    s_tmp = str(d_1)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    l_count.append(1)
                    varTestcase = varTestcase + 1
                else:
                    Log_PO.logger.info("判定居民体重状态DRWS => {'表': '" + self.tableWS + "', 'ID': " + str(id) + "}")
                    d_1['No.'] = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator)
                    d_1['正向'] = 'error'
                    d_1['条件'] = l_2_value
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1['结果'] = '正向不满足'
                    d_1.update(d_tmp)
                    s_tmp = str(d_1)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    l_count.append(0)
                    varTestcase = varTestcase + 1

                    # s = "要求 => {'正向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    # Color_PO.outColor([{"31": s}])
                    # Log_PO.logger.info(s)
                    # s = "步骤1 => " + str(d_tmp["i"])
                    # print(s)
                    # Log_PO.logger.info(s)
                    # s = "步骤2 => " + "{'sql': " + str(d_tmp['sql__WEIGHT_REPORT']) + ", 'WEIGHT_STATUS': " + str(
                    #     d_tmp['WEIGHT_REPORT__WEIGHT_STATUS']) + "}"
                    # print(s)
                    # Log_PO.logger.info(s)
                    # s = "步骤3 => " + "{'sql': " + str(d_tmp['sql__QYYH']) + ", 'WEIGHT_STATUS': " + str(
                    #     d_tmp['QYYH__WEIGHT_STATUS']) + "}"
                    # print(s)
                    # Log_PO.logger.info(s)
                    # s = "返回值 => " + "{'结果': '正向不满足', '" + d_tmp['人群分类'] + "(人群分类：" + str(d_tmp['人群分类编码']) + ")': '" + \
                    #     d_tmp['体重状态'] + "', '预期值': " + str(d_tmp['体重状态编码']) + ", '实际值': " + str(
                    #     d_tmp['WEIGHT_REPORT__WEIGHT_STATUS']) + "}"
                    # print(s)
                    # Log_PO.logger.info(s)
                    Log_PO.logger.info("---------------------------------------------------------------------")
                    # varTestcase = varTestcase + 1
                    # l_count.append(0)

                    # 将错误条件写入数据库，以备复测。
                    # 将列表转换字符串
                    f_2_value = (self.convert_conditions(l_2_value))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                    d_tmp['条件'] = str(f_2_value)
                    d_tmp['测试数据'] = str(d_cases['satisfied'][i])
                    d_tmp['用例类型'] = '正向不满足'
                    s_tmp = str(d_tmp)
                    s_tmp = s_tmp.replace("'", "''")
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Sqlserver_PO_CHC5G.execute(
                        "insert into %s (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID, f_errInfo) values ('%s','%s','%s','%s','%s',%s,'%s') "
                        % (self.tableWS, d_tmp['人群分类'], d_tmp['人群分类编码'], d_tmp['体重状态'], d_tmp['体重状态编码'], d_tmp['条件'], id, s_tmp))

            # 反向用例, N个数据
            if Configparser_PO.SWITCH("testNegative") == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][i], id)
                    d_2 = {}
                    if d_tmp['result'] == 1:
                        # 反向如果命中就错，并且终止循环
                        Log_PO.logger.info("判定居民体重状态DRWS => {'表': '" + self.tableWS + "', 'ID': " + str(id) + "}")
                        d_2['No.'] = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator)
                        d_2['反向'] = 'error'
                        d_2['条件'] = l_2_value
                        d_2['测试数据'] = d_cases['notSatisfied'][i]
                        d_2['结果'] = '反向满足'
                        d_2.update(d_tmp)
                        s_tmp = str(d_2)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])
                        l_count.append(0)
                        varTestcase = varTestcase + 1


                        # Log_PO.logger.info("判定居民体重状态DRWS => {'表': '" + self.tableWS + "', 'ID': " + str(id) + "}")
                        # s = "要求 => {'反向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['notSatisfied'][i]) + "}"
                        # Color_PO.outColor([{"31": s}])
                        # Log_PO.logger.info(s)
                        # s = "步骤1 => " + str(d_tmp["i"])
                        # print(s)
                        # Log_PO.logger.info(s)
                        # s = "步骤2 => " + "{'sql': " + str(d_tmp['sql__WEIGHT_REPORT']) + ", 'WEIGHT_STATUS': " + str(
                        #     d_tmp['WEIGHT_REPORT__WEIGHT_STATUS']) + "}"
                        # print(s)
                        # Log_PO.logger.info(s)
                        # s = "步骤3 => " + "{'sql': " + str(d_tmp['sql__QYYH']) + ", 'WEIGHT_STATUS': " + str(
                        #     d_tmp['QYYH__WEIGHT_STATUS']) + "}"
                        # print(s)
                        # Log_PO.logger.info(s)
                        # s = "返回值 => " + "{'结果': '反向满足', '" + d_tmp['人群分类'] + "(人群分类：" + str(d_tmp['人群分类编码']) + ")': '" + \
                        #     d_tmp['体重状态'] + "', '预期值': " + str(d_tmp['体重状态编码']) + ", '实际值': " + str(
                        #     d_tmp['WEIGHT_REPORT__WEIGHT_STATUS']) + "}"
                        # print(s)
                        # Log_PO.logger.info(s)
                        Log_PO.logger.info("---------------------------------------------------------------------")
                        # varTestcase = varTestcase + 1
                        # l_count.append(0)

                        # 将错误条件写入数据库，以备复测。
                        # 将列表转换字符串
                        f_2_value = (self.convert_conditions(l_2_value))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                        d_tmp['条件'] = str(f_2_value)
                        d_tmp['测试数据'] = str(d_cases['notSatisfied'][i])
                        d_tmp['用例类型'] = "反向满足"
                        s_tmp = str(d_tmp)
                        s_tmp = s_tmp.replace("'", "''")
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        # print(d_tmp)
                        Sqlserver_PO_CHC5G.execute(
                            "insert into %s (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID, f_errInfo) values ('%s','%s','%s','%s','%s',%s,'%s') "
                            % (self.tableWS, d_tmp['人群分类'], d_tmp['人群分类编码'], d_tmp['体重状态'], d_tmp['体重状态编码'], d_tmp['条件'], id, s_tmp))
                    else:
                        d_2['No.'] = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator)
                        d_2['反向'] = 'ok'
                        d_2['条件'] = l_2_value
                        d_2['测试数据'] = d_cases['notSatisfied'][i]
                        Color_PO.outColor([{"36": d_2}])
                        d_2.update(d_tmp)
                        s_tmp = str(d_2)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)

                        # s_print = "{'反向': 'ok', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['notSatisfied'][i]) + "}"
                        # Color_PO.outColor([{"36": s_print}])

                        l_count.append(1)
                        varTestcase = varTestcase + 1

            if 0 in l_count:
                s = "{'ID': " + str(id) + ", '合计数': " + str(l_count) + "}"
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                return varTestcase, 0
            else:
                return varTestcase, 1
    def check_number_type(self, num):
        """判断输入的数字是整数还是浮点数"""
        if isinstance(num, int):
            return "整数"
        elif isinstance(num, float):
            # 检查是否为整数形式的浮点数，如 3.0
            if num.is_integer():
                return "整数（浮点形式）"
            else:
                return "浮点数"
        else:
            return "不是数字类型"
    def _DRWS_run(self, d_cases_satisfied, ID):

        # 公共测试用例

        # d_cases_satisfied = {'BMI': 16.8}
        # ID = 1

        d_tmp = {}

        # 参数
        # 获取f_type, f_typeCode, f_weightStatus, f_weightStatusCode
        l_d_row = Sqlserver_PO_CHC5G.select(
            "select f_type, f_typeCode, f_weightStatus, f_weightStatusCode from %s where ID= %s" % (self.tableWS, ID))
        # print(l_d_row)  # [{'f_type': '普通人群', 'f_typeCode': '3', 'f_weightStatus': '体重偏低', 'f_weightStatusCode': '1'}]
        f_type = l_d_row[0]['f_type']  # 普通人群
        f_typeCode = l_d_row[0]['f_typeCode']  # 3
        f_weightStatus = l_d_row[0]['f_weightStatus']  # 1
        f_weightStatusCode = l_d_row[0]['f_weightStatusCode']  # 1
        d_tmp['人群分类'] = f_type
        d_tmp['人群分类编码'] = f_typeCode
        d_tmp['体重状态'] = f_weightStatus
        d_tmp['体重状态编码'] = f_weightStatusCode

        # 参数化
        WEIGHT_REPORT__ID = 2  # //测试id，位于WEIGHT_REPORT表
        d_tmp['WEIGHT_REPORT__ID'] = 2
        d_tmp['身份证'] = '420204202201011268'

        # BMI
        varBMI = d_cases_satisfied['BMI']

        # 年龄
        if '年龄' in d_cases_satisfied:
            if isinstance(d_cases_satisfied['年龄'], int):
                varAge = d_cases_satisfied['年龄']
                varAgeFloat = 0.0
            elif isinstance(d_cases_satisfied['年龄'], float):
                # 检查是否为整数形式的浮点数，如 3.0
                # if d_cases_satisfied['年龄'].is_integer():
                #     varAge = int(d_cases_satisfied['年龄'])
                #     varAgeFloat = 0.0
                # else:
                varAgeFloat = d_cases_satisfied['年龄']
                varAge = 0
        else:
            varAge = 0
            varAgeFloat = 0.0

        # 性别
        if '性别' in d_cases_satisfied:
            if d_cases_satisfied['性别'] == "女":
                varSexCode = '2'
                varSex = "女"
            else:
                varSexCode = '1'
                varSex = '男'
        else:
            varSexCode = '1'
            varSex = '男'

        # 儿童使用月龄
        if f_type == '儿童':
            varAgeMonth = d_cases_satisfied['年龄']
        else:
            varAgeMonth = 0

        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8014/weight/saveOrUpdateWeightManage" -H "Request-Origion:SwaggerBootstrapUi" -H "accept:*/*" -H "Authorization:" -H "Content-Type:application/json" -d "{\\"age\\":' + str(
            varAge) + ',\\"ageFloat\\":' + str(varAgeFloat) + ',\\"ageMonth\\":' + str(
            varAgeMonth) + ',\\"basicIntake\\":100,\\"bmi\\":' + str(
            varBMI) + ',\\"categoryCode\\":\\"' + str(d_tmp[
                                                          '人群分类编码']) + '\\",\\"disease\\":\\"无\\",\\"foodAdvice\\":\\"建议饮食\\",\\"height\\":175,\\"hipline\\":33,\\"id\\":' + str(
            d_tmp['WEIGHT_REPORT__ID']) + ',\\"idCard\\":\\"' + str(
            d_tmp['身份证']) + '\\",\\"orgCode\\":\\"0000001\\",\\"orgName\\":\\"静安精神病院\\",\\"sex\\":\\"' + str(
            varSex) + '\\",\\"sexCode\\":\\"' + str(
            varSexCode) + '\\",\\"sportAdvice\\":\\"建议运动\\",\\"targetWeight\\":50,\\"waistHip\\":0.9,\\"waistline\\":33,\\"weight\\":55,\\"weightRecordId\\":0}"'
        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        # curl -X POST "http://192.168.0.243:8014/weight/saveOrUpdateWeightManage" -H "Request-Origion:SwaggerBootstrapUi" -H "accept:*/*" -H "Authorization:" -H "Content-Type:application/json" -d "{\"age\":12,\"ageFloat\":6.0,\"ageMonth\":0,\"basicIntake\":100,\"bmi\":13.3,\"categoryCode\":\"2\",\"disease\":\"无\",\"foodAdvice\":\"建议饮食\",\"height\":175,\"hipline\":33,\"id\":2,\"idCard\":\"420204202201011268\",\"orgCode\":\"0000001\",\"orgName\":\"静安精神病院\",\"sex\":\"男\",\"sexCode\":\"1\",\"sportAdvice\":\"建议运动\",\"targetWeight\":50,\"waistHip\":0.9,\"waistline\":33,\"weight\":55,\"weightRecordId\":0}"
        # sys.exit(0)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # command = command.replace("'", "''")
        # command = command.replace("\\\\","\\")
        d_tmp["i"] = command
        # print(d_r)

        if d_r['code'] == 200:
            l_d_1 = Sqlserver_PO_CHC.select(
                "select WEIGHT_STATUS from WEIGHT_REPORT where ID = %s" % (WEIGHT_REPORT__ID))
            l_d_2 = Sqlserver_PO_CHC.select("select WEIGHT_STATUS from QYYH where SFZH = '%s'" % (str(d_tmp['身份证'])))
            d_tmp['sql__WEIGHT_REPORT'] = "select WEIGHT_STATUS from WEIGHT_REPORT where ID = " + str(WEIGHT_REPORT__ID)
            d_tmp['sql__QYYH'] = "select WEIGHT_STATUS from QYYH where SFZH = '" + str(d_tmp['身份证']) + "'"
            # print("l_d_1", l_d_1)
            # print("l_d_2", l_d_2)
            # print("l_d_1[0]['WEIGHT_STATUS']", l_d_2[0]['WEIGHT_STATUS'])
            # print("f_weightStatusCode", f_weightStatusCode)
            d_tmp['WEIGHT_REPORT__WEIGHT_STATUS'] = l_d_1[0]['WEIGHT_STATUS']
            d_tmp['QYYH__WEIGHT_STATUS'] = l_d_2[0]['WEIGHT_STATUS']
            d_tmp['l_d_1'] = l_d_1
            d_tmp['l_d_2'] = l_d_2
            d_tmp['WEIGHT_STATUS'] = l_d_1[0]['WEIGHT_STATUS']
            return d_tmp

        else:
            print("638, error ", d_r['code'])
            sys.exit(0)
    def DRWS_run_p(self, d_cases_satisfied, ID):

        d_tmp = self._DRWS_run(d_cases_satisfied, ID)
        # print(d_tmp)
        if d_tmp['l_d_1'] == d_tmp['l_d_2'] and d_tmp['WEIGHT_STATUS'] == int(d_tmp['体重状态编码']):
            d_tmp['result'] = 1
        else:
            d_tmp['result'] = 0
        return d_tmp
    def DRWS_run_n(self, d_cases_satisfied, ID):

        d_tmp = self._DRWS_run(d_cases_satisfied, ID)
        # print(d_tmp)
        if d_tmp['l_d_1'] == d_tmp['l_d_2'] and d_tmp['WEIGHT_STATUS'] != int(d_tmp['体重状态编码']):
            d_tmp['result'] = 0
        else:
            d_tmp['result'] = 1
        return d_tmp




    def EFRB_case_or_1(self, d_cases, l_2_value, Numerator, Denominator, d_param):

        varTestcase = 0


        # 一条数据，正向用例
        l_count = []
        d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], d_param['ID'], d_param)
        if d_tmp['result'] == 1:
            s_print = str(Numerator) + "/" + str(Denominator) + ", {'正向': 'ok', '条件':" + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][0]) + "}"
            Color_PO.outColor([{"34": s_print}])
            Log_PO.logger.info(s_print)
            l_count.append(1)
        else:
            s_print = "{'正向': 'error', '条件': " + str(l_2_value) + ", '测试数据':" + str(d_cases['satisfied'][0]) + "}"
            Color_PO.outColor([{"31": s_print}])
            Log_PO.logger.info(s_print)
            s_tmp = str(d_tmp)
            s_tmp =s_tmp.replace("\\\\","\\")
            Color_PO.outColor([{"31": s_tmp}])
            Log_PO.logger.info(s_tmp)
            l_count.append(0)
        varTestcase = varTestcase + 1

        if 0 in l_count:
            s = "{'ID': " + str(id) + ", '合计数': " + str(l_count) + "}"
            Color_PO.outColor([{"31": s}])
            Log_PO.logger.info(s)
            return 0
        else:
            return 1
    def EFRB_case_or(self, d_cases, id, l_2_value, Numerator, Denominator,d_param):

        varTestcase = 0

        if len(d_cases['satisfied']) == 1:
            # 一条数据，正向用例
            l_count = []
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], id, d_param)
            if d_tmp['result'] == 1:
                s_print = str(Numerator) + "/" + str(Denominator) + ", {'正向': 'ok', '条件':" + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][0]) + "}"
                Color_PO.outColor([{"34": s_print}])
                Log_PO.logger.info(s_print)
                l_count.append(1)
            else:
                s_print = "{'正向': 'error', '条件': " + str(l_2_value) + ", '测试数据':" + str(d_cases['satisfied'][0]) + "}"
                Color_PO.outColor([{"31": s_print}])
                Log_PO.logger.info(s_print)
                Color_PO.outColor([{"33": d_tmp}])
                Log_PO.logger.info(d_tmp)
                l_count.append(0)
            varTestcase = varTestcase + 1

            # 一条数据，反向用例
            if Configparser_PO.SWITCH("testNegative") == "on":

                d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], id, d_param)
                if d_tmp['result'] == 1:
                    s_print = "{'反向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['notSatisfied'][0]) + "}"
                    Color_PO.outColor([{"31": s_print}])
                    Log_PO.logger.info(s_print)
                    Color_PO.outColor([{"33": d_tmp}])
                    Log_PO.logger.info(d_tmp)
                    l_count.append(0)
                else:
                    s_print = "{'反向': 'ok', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['notSatisfied'][0]) + "}"
                    Color_PO.outColor([{"36": s_print}])
                    Log_PO.logger.info(s_print)
                    l_count.append(1)
                varTestcase = varTestcase + 1

            if 0 in l_count:
                s = "{'ID': " + str(id) + ", '合计数': " + str(l_count) + "}"
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                return varTestcase, 0
            else:
                return varTestcase, 1

        else:
            # 正向用例, N个数据
            l_count = []
            d_1 = {}
            for i in range(len(d_cases['satisfied'])):
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], id, d_param)
                if d_tmp['result'] == 1:
                    s_print = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator) + ", {'正向': 'ok', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    Color_PO.outColor([{"34": s_print}])
                    # Log_PO.logger.info(s_print)
                    varTestcase = varTestcase + 1
                    l_count.append(1)
                else:
                    # s = "要求 => {'ID': " + str(id) + ", '正向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    # Color_PO.outColor([{"31": s}])
                    # Log_PO.logger.info(s)
                    d_1['表'] = 'a_weight10_ER'
                    d_1['ID'] = id
                    d_1['正向'] = 'error'
                    d_1['条件'] = l_2_value
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1.update(d_tmp)
                    s_tmp= str(d_1)
                    s_tmp = s_tmp.replace("\\\\","\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])


                    # s = "步骤1 => " + str(d_tmp["i"])
                    # print(s)
                    # Log_PO.logger.info(s)
                    # # print(d_tmp)
                    # s = "步骤2 => " + "{'sql': " + str(d_tmp['sql__T_ASSESS_RULE_RECORD']) + ", 'RULE_CODE': " + str(
                    #     d_tmp['T_ASSESS_RULE_RECORD__RULE_CODE']) + "}"
                    # print(s)
                    # Log_PO.logger.info(s)
                    # s = "返回值 => " + "{'结果': '正向不满足', '" + d_tmp['人群分类'] + "(人群分类：" + str(d_tmp['人群分类编码']) + ")': '" + "', '预期值': " + str(d_tmp['RULE_CODE']) + ", '实际值': " + str(
                    #     d_tmp['T_ASSESS_RULE_RECORD__RULE_CODE']) + "}"
                    # print(s)
                    # Log_PO.logger.info(s)
                    Log_PO.logger.info("---------------------------------------------------------------------")
                    varTestcase = varTestcase + 1
                    l_count.append(0)

            # 反向用例, N个数据
            if Configparser_PO.SWITCH("testNegative") == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    # d_tmp = self.EFRB_run_n(v[0], ID)
                    d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][i], id)
                    if d_tmp['result'] == 1:
                        # 反向如果命中就错，并且终止循环
                        s = "要求 => {'ID': " + str(id) + ", '反向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(
                            d_cases['notSatisfied'][i]) + "}"
                        Color_PO.outColor([{"31": s}])
                        Log_PO.logger.info(s)
                        s_tmp = str(d_tmp)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])

                        # s = "步骤1 => " + str(d_tmp["i"])
                        # print(s)
                        # Log_PO.logger.info(s)
                        # s = "步骤2 => " + "{'sql': " + str(d_tmp['sql__T_ASSESS_RULE_RECORD']) + ", 'RULE_CODE': " + str(
                        #     d_tmp['T_ASSESS_RULE_RECORD__RULE_CODE']) + "}"
                        # print(s)
                        # Log_PO.logger.info(s)
                        # s = "返回值 => " + "{'结果': '反向满足', '" + d_tmp['人群分类'] + "(人群分类：" + str(
                        #     d_tmp['人群分类编码']) + ")': '" + "', '预期值': " + str(d_tmp['RULE_CODE']) + ", '实际值': " + str(
                        #     d_tmp['T_ASSESS_RULE_RECORD__RULE_CODE']) + "}"
                        # print(s)
                        # Log_PO.logger.info(s)
                        Log_PO.logger.info("---------------------------------------------------------------------")
                        varTestcase = varTestcase + 1
                        l_count.append(0)

                        # 将列表转换字符串
                        f_2_value = (self.convert_conditions(l_2_value))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                        d_tmp['条件'] = str(f_2_value)
                        d_tmp['测试数据'] = str(d_cases['notSatisfied'][i])
                        d_tmp['用例类型'] = "反向满足"
                    else:
                        s_print = "{'反向': 'ok', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['notSatisfied'][i]) + "}"
                        Color_PO.outColor([{"36": s_print}])
                        varTestcase = varTestcase + 1
                        l_count.append(1)

            if 0 in l_count:
                s = "{'ID': " + str(id) + ", '合计数': " + str(l_count) + "}"
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                return varTestcase, 0
            else:
                return varTestcase, 1




    # 评估因素规则库 Evaluation Factor Rule Base
    def EFRB_1(self, varTestID, d_param):

        # EFRB(self, varTestID, varPN="p")
        # 评估因素规则库 Evaluation Factor Rule Base
        # a_weight10_ER
        # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
        # varPN = p 执行正向（默认值p），n 执行反向；

        d_tmp = {}

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select f_ER, f_ERcode from %s where ID =%s" % (self.tableER, varTestID))
        # print("1299l_d_row => ", l_d_row)
        # print(l_d_row[0]['f_ER'])
        f_ER = (l_d_row[0]['f_ER'])
        # f_ERcode = (l_d_row[0]['f_ERcode'])
        d_tmp['规则库'] = '评估因素规则库EFRB'
        d_tmp['表'] = self.tableER
        d_tmp['ID'] = varTestID
        d_tmp['f_ER'] = l_d_row[0]['f_ER']
        d_tmp['f_ERcode'] = l_d_row[0]['f_ERcode']
        d_tmp.update(d_param)

        # 统计所有组合的数量
        varTestCount = f_ER.count("or")
        # print(varTestCount)  # 输出or的数量: 2

        # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
        f_ER = f_ER.replace("月", '')
        f_ER = f_ER.replace('＞', '>').replace('＜', '<').replace('＝', '=')

        # todo EFRB_case for 只有年龄
        if "and" not in f_ER and "年龄" in f_ER:
            # 转换成列表
            l_ER = f_ER.split("and")
            l_ER = [i.strip() for i in l_ER]
            # print("1039 实际参数 =", l_ER)  # ['18.5<BMI', 'BMI<24.0']

            l_2_value = []
            # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
            for i in l_ER:
                l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                l_2_value.extend(l_simple_conditions)
            # print("1046 分解参数 =", l_2_value)

            # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
            l_3_value = []
            for i in l_2_value:
                l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                l_3_value.extend(l_simple_conditions)
            # print("1053 结构化参数 =", l_3_value)  #  ['BMI>18.5', 'BMI<24.0']

            # 读取BMI模块，生成随机数据d_cases
            d_cases = Age_PO.generate_all_cases(l_3_value)
            print("测试数据集合 =>", d_cases)

            # 测试数据
            # todo EFRB for and
            count = self.EFRB_case_1(d_cases, l_ER, d_tmp)
            print("1474count", count)
            return count

        elif "and" not in f_ER and "年龄" not in f_ER:

            # todo EFRB_case for 人群分类

            print("varTestID：", varTestID)

            self.EFRB_run_crowd_1(varTestID, d_param)

        # todo EFRB 复杂条件组合
        elif "or" in f_ER:
            # 转换列表，结构化原始数据为列表，生成l_l_N
            l_value = f_ER.split("or")
            l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
            l_value = [i.split("and") for i in l_value]
            l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
            # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...

            l_result = []
            sum = 0
            for lln in range(len(l_l_value)):
                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                # print(l_l_value(lln))
                for i in l_l_value[lln]:
                    if "BMI" in i:
                        l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                        l_2_value.extend(l_simple_conditions)
                    if "年龄" in i:
                        l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                        l_2_value.extend(l_simple_conditions)
                    elif "性别" in i:
                        l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                        l_2_value.extend(l_simple_conditions)
                # print("611 分解参数 =", l_2_value)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                l_3_value = []
                for i in l_2_value:
                    l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                    l_3_value.extend(l_simple_conditions)
                # print("618 结构化参数 =", l_3_value)

                # 读取BmiAgeSex模块，生成随机数据d_cases
                # d_cases = BmiAgeSex_PO.generate_all_cases(l_3_value)

                for i in l_3_value:
                    if ('>=' or '<=') in i:
                        if '年龄' in i:
                            d_cases = BmiAgeSex_PO.main(l_3_value)
                            break
                        if 'BMI' in i:
                            d_cases = BmiAgeSex_PO.main(l_3_value)
                            break
                    else:
                        d_cases = BmiAgeSex_PO.main(l_3_value)

                # print("--------------------")
                # print("测试数据集合 =>", d_cases)
                # sys.exit(0)

                # 判断输出结果
                # todo EFRB_case_or for or
                # self.EFRB_case_1(d_cases, l_ER, d_tmp)

                print("9999")
                count = self.EFRB_case_or_1(d_cases, l_2_value, lln+1, varTestCount+1, d_tmp)
                return count
                # varTestcase, varCount = self.EFRB_case_or(d_cases, id, l_2_value, lln+1, varTestCount+1)


        # todo EFRB 简单条件组合
        elif "and" in f_ER:

            # 转换成列表
            l_ER = f_ER.split("and")
            l_ER = [i.strip() for i in l_ER]
            # print("1039 实际参数 =", l_ER)  # ['18.5<BMI', 'BMI<24.0']

            l_2_value = []
            # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
            for i in l_ER:
                l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                l_2_value.extend(l_simple_conditions)
            # print("1046 分解参数 =", l_2_value)

            # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
            l_3_value = []
            for i in l_2_value:
                l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                l_3_value.extend(l_simple_conditions)
            # print("1053 结构化参数 =", l_3_value)  #  ['BMI>18.5', 'BMI<24.0']

            # 读取BMI模块，生成随机数据d_cases
            d_cases = BmiAge_PO.main(l_3_value)
            # print("测试数据集合 =>", d_cases)

            # 测试数据
            # todo EFRB for and
            count = self.EFRB_case_1(d_cases, l_ER, d_tmp)
            print("1474count", count)
            return count

        # todo EFRB 无条件组合
        elif "and" not in f_ER:

            l_2_value = []
            # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
            l_simple_conditions = Bmi_PO.splitMode(f_ER)
            l_2_value.extend(l_simple_conditions)
            # print("611 分解参数 =", l_2_value)

            # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
            l_3_value = []
            for i in l_2_value:
                l_simple_conditions = Bmi_PO.interconvertMode(i)
                l_3_value.extend(l_simple_conditions)
            # print("680 结构化参数 =", l_3_value)  # ['BMI<18.5']

            # 读取BMI模块，生成随机数据d_cases
            d_cases = Age_PO.generate_all_cases(l_3_value)
            # d_cases = Bmi_PO.generate_all_cases(l_3_value)
            print(d_cases)  # {'satisfied': [{'BMI': 16.8}], 'not1': [{'BMI': 19.6}]}

            sys.exit(0)

            # todo EFRB_case for not and
            # 判断输出结果
            self.EFRB_case(d_cases, id, l_2_value)

        else:
            print("[not or & and ]")
        print("-".center(100, "-"))
    def EFRB(self, varTestID, d_param={}):

        # EFRB(self, varTestID, varPN="p")
        # 评估因素规则库 Evaluation Factor Rule Base
        # a_weight10_ER
        # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
        # varPN = p 执行正向（默认值p），n 执行反向；

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_ER, f_ERcode from %s" % (self.tableER))
        # print("l_d_row => ", l_d_row)
        if varTestID > len(l_d_row):
            print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
            sys.exit(0)

        for i in enumerate(l_d_row):
            i = varTestID - 1
            id = l_d_row[i]['ID']
            f_ER = l_d_row[i]['f_ER']

            # 获取原始数据
            print("评估因素规则库EFRB => {表: " + self.tableER + ", ID: " + str(id) )
            # print("评估因素规则库EFRB => {表: " + self.tableER + ", ID: " + str(id) + ", 条件: " + str(f_ER) + "}")
            Log_PO.logger.info("评估因素规则库EFRB => {'表': '" + self.tableER + "', 'ID': " + str(id) + "}")

            # 统计所有组合的数量
            varTestCount = f_ER.count("or")
            # print(varTestCount)  # 输出or的数量: 2

            # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
            f_ER = f_ER.replace("月", '')
            f_ER = f_ER.replace('＞', '>').replace('＜', '<').replace('＝', '=')

            # todo EFRB_case for 高血压&糖尿病
            if f_ER == "高血压" or f_ER == "糖尿病":
                # 判断输出结果
                self.EFRB_run_disease(f_ER, id)
                # if varPN == "n":
                #     self.EFRB_run_disease_n("脑卒中", id)
                # else:
                #     self.EFRB_run_disease(f_ER, id)

            # todo EFRB_case for 人群分类
            elif f_ER.isdigit() == True:
                # 判断输出结果
                self.EFRB_run_crowd(f_ER, id)

            # todo EFRB_case for 只有年龄
            elif "and" not in f_ER and "BMI" not in f_ER:
                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                l_simple_conditions = Age_PO.splitMode(f_ER)
                l_2_value.extend(l_simple_conditions)
                # print("611 分解参数 =", l_2_value)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                l_3_value = []
                for i in l_2_value:
                    l_simple_conditions = Age_PO.interconvertMode(i)
                    l_3_value.extend(l_simple_conditions)
                print("680 结构化参数 =", l_3_value)  #680 结构化参数 = ['年龄<=3']

                # 读取模块，生成随机数据d_cases
                d_cases = Age_PO.generate_all_cases(l_3_value)
                print("测试数据集合 =>", d_cases)  # {'satisfied': [{'年龄': 3.0}, {'年龄': 2.5}], 'not1': [{'年龄': 16.9}]}

                # todo EFRB_case for 只有年龄
                # 判断输出结果
                self.EFRB_case(d_cases, id, l_2_value)

            # todo EFRB 复杂条件组合
            elif "or" in f_ER:
                # 转换列表，结构化原始数据为列表，生成l_l_N
                l_value = f_ER.split("or")
                l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
                l_value = [i.split("and") for i in l_value]
                l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
                # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...

                l_result = []
                sum = 0
                for lln in range(len(l_l_value)):
                    l_2_value = []
                    # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                    # print(l_l_value(lln))
                    for i in l_l_value[lln]:
                        if "BMI" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                        if "年龄" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                        elif "性别" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                    # print("611 分解参数 =", l_2_value)

                    # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                    l_3_value = []
                    for i in l_2_value:
                        l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                        l_3_value.extend(l_simple_conditions)
                    # print("618 结构化参数 =", l_3_value)

                    # 读取BmiAgeSex模块，生成随机数据d_cases
                    # d_cases = BmiAgeSex_PO.generate_all_cases(l_3_value)

                    for i in l_3_value:
                        if ('>=' or '<=') in i:
                            if '年龄' in i:
                                d_cases = BmiAgeSex_PO.main(l_3_value)
                                break
                            if 'BMI' in i:
                                d_cases = BmiAgeSex_PO.main(l_3_value)
                                break
                        else:
                            d_cases = BmiAgeSex_PO.main(l_3_value)

                    print("--------------------")
                    print("测试数据集合 =>", d_cases)
                    # sys.exit(0)

                    # 判断输出结果
                    # todo EFRB_case_or for or
                    varTestcase, varCount = self.EFRB_case_or(d_cases, id, l_2_value, lln+1, varTestCount+1, d_param)
                    l_result.append(varCount)
                    sum = sum + varTestcase

                # print(l_result)

                # 回写数据库f_resut, f_updateDate
                if 0 not in l_result:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => ok"}])
                    Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                        self.tableER, sum, id))

                else:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                        self.tableER, sum, id))

            # todo EFRB 简单条件组合
            elif "and" in f_ER:

                # 转换成列表
                l_ER = f_ER.split("and")
                l_ER = [i.strip() for i in l_ER]
                # print("1039 实际参数 =", l_ER)  # ['18.5<BMI', 'BMI<24.0']

                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                for i in l_ER:
                    l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                    l_2_value.extend(l_simple_conditions)
                # print("1046 分解参数 =", l_2_value)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                l_3_value = []
                for i in l_2_value:
                    l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                    l_3_value.extend(l_simple_conditions)
                # print("1053 结构化参数 =", l_3_value)  #  ['BMI>18.5', 'BMI<24.0']

                # 读取BMI模块，生成随机数据d_cases
                d_cases = BmiAge_PO.main(l_3_value)
                print("测试数据集合 =>", d_cases)

                # 测试数据
                # todo EFRB for and
                self.EFRB_case(d_cases, id, l_ER, d_param)

            # todo EFRB 无条件组合
            elif "and" not in f_ER:

                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                l_simple_conditions = Bmi_PO.splitMode(f_ER)
                l_2_value.extend(l_simple_conditions)
                # print("611 分解参数 =", l_2_value)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                l_3_value = []
                for i in l_2_value:
                    l_simple_conditions = Bmi_PO.interconvertMode(i)
                    l_3_value.extend(l_simple_conditions)
                # print("680 结构化参数 =", l_3_value)  # ['BMI<18.5']

                # 读取BMI模块，生成随机数据d_cases
                d_cases = Age_PO.generate_all_cases(l_3_value)
                # d_cases = Bmi_PO.generate_all_cases(l_3_value)
                print(d_cases)  # {'satisfied': [{'BMI': 16.8}], 'not1': [{'BMI': 19.6}]}

                # todo EFRB_case for not and
                # 判断输出结果
                self.EFRB_case(d_cases, id, l_2_value)



            else:
                print("[not or & and ]")
            print("-".center(100, "-"))

            break
    def EFRB_case_1(self, d_cases, l_2_value, d_param):

        # d_case : 测试数据
        # L_2_value： 条件
        # d_param：接口的参数

        varTestcase = 0

        # 一条数据，正向用例
        l_count = []
        # todo EFRB_run_p_1
        d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], d_param['ID'], d_param)
        d_1 = {}
        if d_tmp['result'] == 1:
            d_1['正向'] = "ok"
            # d_1['条件'] = l_2_value
            d_1['测试数据'] = d_cases['satisfied'][0]
            d_param.update(d_1)
            Color_PO.outColor([{"34": d_param}])
            Log_PO.logger.info(d_param)
            return 1
        else:
            d_1['正向'] = "error"
            d_1['条件'] = l_2_value
            d_1['测试数据'] = d_cases['satisfied'][0]
            d_1.update(d_tmp)
            s_tmp = str(d_1)
            s_tmp = s_tmp.replace("\\\\", "\\")
            # s_print = "[正向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][0])
            Color_PO.outColor([{"31": s_tmp}])
            Log_PO.logger.info(s_tmp)
            return 0
    def EFRB_case(self, d_cases, ID, l_2_value, d_param):

        # d_case : 测试数据
        # L_2_value： 条件
        # d_param：接口的参数

        varTestcase = 0

        if len(d_cases['satisfied']) == 1:
            # 一条数据，正向用例
            l_count = []
            # todo EFRB_run_p_1
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], ID, d_param)
            d_1 = {}
            if d_tmp['result'] == 1:
                d_1['正向'] = "ok"
                d_1['条件'] = l_2_value
                d_1['测试数据'] = d_cases['satisfied'][0]
                Color_PO.outColor([{"34": d_1}])
                Log_PO.logger.info(d_1)
                l_count.append(1)
            else:
                d_1['正向'] = "error"
                d_1['条件'] = l_2_value
                d_1['测试数据'] = d_cases['satisfied'][0]
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                # s_print = "[正向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][0])
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)
            varTestcase = varTestcase + 1

            # 一条数据，反向用例
            # todo EFRB_run_n
            if Configparser_PO.SWITCH("testNegative") == "on":

                if Configparser_PO.SWITCH("testNegative") == "on":
                    d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], ID)
                    if d_tmp['result'] == 1:
                        s_print = "[反向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][0])
                        Color_PO.outColor([{"31": s_print}])
                        Log_PO.logger.info(s_print)
                        Color_PO.outColor([{"33": d_tmp}])
                        Log_PO.logger.info(d_tmp)
                        l_count.append(0)
                    else:
                        s_print = "[反向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][0])
                        Color_PO.outColor([{"36": s_print}])
                        Log_PO.logger.info(s_print)
                        l_count.append(1)
                    varTestcase = varTestcase + 1

            # 回写数据库f_resut, f_updateDate
            d_result = {}
            if 0 not in l_count:
                d_result['ID'] = ID
                d_result['result'] = 'ok'
                Color_PO.outColor([{"32": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, varTestcase, d_result['result'] ,d_result['ID'] ))
            else:
                d_result['ID'] = ID
                d_result['result'] = 'error'
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, varTestcase, d_result['result'], d_result['ID']))
        else:
            # 正向用例, N个数据
            l_count = []
            for i in range(len(d_cases['satisfied'])):
                # print(d_cases)
                # todo EFRB_run_p
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], ID, d_param)
                d_1 = {}
                if d_tmp['result'] == 1:
                    d_1['正向'] = "ok"
                    d_1['条件'] = l_2_value
                    d_1['测试数据'] = d_cases['satisfied'][i]

                    # s_print = "[正向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][i])
                    Color_PO.outColor([{"34": d_1}])
                    # s_tmp = str(d_tmp)
                    # s_tmp = s_tmp.replace("\\\\","\\")
                    # Color_PO.outColor([{"34": s_tmp}])
                    Log_PO.logger.info(d_1)
                    varTestcase = varTestcase + 1
                    l_count.append(1)
                else:
                    d_1['正向'] = "error"
                    d_1['条件'] = l_2_value
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1.update(d_tmp)
                    s_tmp = str(d_1)
                    s_tmp = s_tmp.replace("\\\\","\\")

                    # s_print = "[正向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][i])
                    Color_PO.outColor([{"31": s_tmp}])
                    Log_PO.logger.info(s_tmp)
                    # Color_PO.outColor([{"33": d_tmp}])
                    # Log_PO.logger.info(d_tmp['i'])
                    # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                    # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                    varTestcase = varTestcase + 1
                    l_count.append(0)

            # 反向用例, N个数据
            if Configparser_PO.SWITCH("testNegative") == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    # todo DRWS_run_n_n
                    d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][i], ID)
                    if d_tmp['result'] == 1:
                        # 反向如果命中就错，并且终止循环
                        s_print = "[反向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][i])
                        Color_PO.outColor([{"31": s_print}])
                        Log_PO.logger.info(s_print)
                        s_tmp = str(d_tmp)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])

                        # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                        # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                        varTestcase = varTestcase + 1
                        l_count.append(0)
                    else:
                        s_print = "[反向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][i])
                        Color_PO.outColor([{"36": s_print}])
                        Log_PO.logger.info(s_print)
                        varTestcase = varTestcase + 1
                        l_count.append(1)

            # 回写数据库f_resut, f_updateDate
            d_result = {}
            if 0 not in l_count:
                d_result['ID'] = ID
                d_result['result'] = "ok"
                Color_PO.outColor([{"32": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableER, varTestcase, ID))
            else:
                d_result['ID'] = ID
                d_result['result'] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableER, varTestcase, ID))

        #         # 反向用例, 不满足条件的v[0]，预期不命中。
        #         del d_cases['satisfied']
        #         varCount = 2
        #         for k, v in d_cases.items():
        #             # print(v[0])
        #             # todo EFRB_run_n
        #             varCount = self.EFRB_run_n(v[0], id, self.tableER)
        #             if varCount == 1:
        #                 # 反向如果命中就错，并且终止循环
        #                 Color_PO.outColor([{"31": "p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
        #                 # Log_PO.logger.info("p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
        #                 # varTestcase = varTestcase + 1
        #                 # Color_PO.outColor([{"33": d_tmp}])
        #
        #                 # print("步骤1 => ", d_tmp["i"])
        #                 # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #                 # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #                 Log_PO.logger.info("ID = " + str(id) + ", p3, 反向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #                     str(v[0])))
        #                 # Log_PO.logger.info(d_tmp['i'])
        #                 # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #                 # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #                 varTestcase = varTestcase + 1
        #
        #                 # print("p3, 反向error, 条件：", l_N, "，不满足：", v[0])
        #                 break
        #             else:
        #                 Color_PO.outColor([{"34": "p4, 反向ok, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
        #                 Log_PO.logger.info("p4, 反向ok, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
        #                 varTestcase = varTestcase + 1
        #                 # print("p4, 反向ok, 条件：", l_N, "，不满足：", v[0], " > 不命中")
        #                 # Ellipsis
        #     else:
        #         Color_PO.outColor([{"31": "ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #             d_cases['satisfied'][0])}])
        #         # Color_PO.outColor([{"33": d_tmp}])
        #
        #         # print("步骤1 => ", d_tmp["i"])
        #         # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #         # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #         Log_PO.logger.info("ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #             d_cases['satisfied'][0]))
        #         # Log_PO.logger.info(d_tmp['i'])
        #         # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #         # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #         varTestcase = varTestcase + 1
        #
        #         # Color_PO.outColor([{"31": "p2, 正向error, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0])}])
        #         # Log_PO.logger.info("p2, 正向error, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0]))
        #         # varTestcase = varTestcase + 1
        #         # print("p2, 正向error, 条件：", l_N, "，满足：", d_cases['satisfied'][0], varCount)
        #         # Ellipsis
        #
        #     # 回写数据库f_resut, f_updateDate
        #     if varCount == 2:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => ok"}])
        #         Log_PO.logger.info([{"32": "ok, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        #     else:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
        #         Log_PO.logger.info([{"31": "error, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        # else:
        #     for i in range(len(d_cases['satisfied'])):
        #         # print(d_cases)
        #         # todo EFRB_run_p_n
        #         result = self.EFRB_run_p(d_cases['satisfied'][i], id, self.tableER)
        #         if result == 1:
        #             s_print = "[正向ok], 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][i])
        #             Color_PO.outColor([{"34": s_print}])
        #             Log_PO.logger.info(s_print)
        #             varTestcase = varTestcase + 1
        #         else:
        #             s_print = "[正向error], 条件：" + str(l_2_value) + "，不满足：" + str(d_cases['satisfied'][i])
        #             Color_PO.outColor([{"31": s_print}])
        #             Log_PO.logger.info(s_print)
        #             # Color_PO.outColor([{"33": d_tmp}])
        #             # Log_PO.logger.info(d_tmp['i'])
        #             # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #             varTestcase = varTestcase + 1
        #
        #
        #     # 反向用例, 不满足条件的v[0]，预期不命中。
        #     del d_cases['satisfied']
        #     varCount = 2
        #     for k, v in d_cases.items():
        #         # todo EFRB_run_n_n
        #         varCount = self.EFRB_run_n(v[0], id, self.tableER)
        #         if varCount == 1:
        #             # 反向如果命中就错，并且终止循环
        #             s_print = "[反向error], 条件：" + str(l_2_value) + "，不满足：" + str(v[0])
        #             Color_PO.outColor([{"31": s_print}])
        #             Log_PO.logger.info(s_print)
        #             # varTestcase = varTestcase + 1
        #             # Color_PO.outColor([{"33": d_tmp}])
        #
        #             # print("步骤1 => ", d_tmp["i"])
        #             # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['i'])
        #             # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #             varTestcase = varTestcase + 1
        #         else:
        #             s_print = "[反向ok], 条件：" + str(l_2_value) + "，不满足：" + str(v[0])
        #             Color_PO.outColor([{"34": s_print}])
        #             Log_PO.logger.info(s_print)
        #             varTestcase = varTestcase + 1
        #
        #         # 回写数据库f_resut, f_updateDate
        #     if varCount == 2:
        #         s_print = "ID = " + str(id) + ", 结果：ok"
        #         Color_PO.outColor([{"32": s_print}])
        #         Log_PO.logger.info([{"32": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        #     else:
        #         s_print = "ID = " + str(id) + ", 结果：error"
        #         Color_PO.outColor([{"31": s_print}])
        #         Log_PO.logger.info([{"31": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
    def EFRB_run_disease(self, varDisease, ID):

        # 既往疾病
        # varDisease = 高血压
        # id = 46

        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_ERcode from %s where ID= %s" % (self.tableER, ID))
        d_tmp['评估因素编码'] = l_d_row[0]['f_ERcode']

        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = 2  # //测试id，位于WEIGHT_REPORT表
        d_tmp['身份证'] = '420204202201011268'

        varAge = 0
        varAgeFloat = 0.0
        varAgeMonth = 0
        varBMI = 10.1

        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":'+ str(varAge) +',\\"ageFloat\\":'+ str(varAgeFloat) +',\\"ageMonth\\":'+ str(varAgeMonth) +',\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":'+str(varBMI)+',\\"categoryCode\\":1,\\"disease\\":\\"'+str(varDisease)+'\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\\":\\"' + str(d_tmp['身份证']) + '\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"\\",\\"sexCode\\":\\"1\\",\\"weight\\":55,\\"weightReportId\\":' + str(d_tmp['WEIGHT_REPORT__ID']) + '}"'

        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command
        # print(d_r)

        if d_r['code'] == 200:

            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            # 可能命中多条
            # print(l_d_RULE_CODE_actual)  # [{'RULE_CODE': 'TZ_RQFL004'}, {'RULE_CODE': 'TZ_AGE001'}, {'RULE_CODE': 'TZ_JWJB001'}]
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['f_ERcode']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            l_count = []
            d_1 = {}
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                d_1['正向'] = "ok"
                d_1['既往疾病'] = varDisease
                # d_1.update(d_tmp)
                # s_tmp = str(d_1)
                # s_tmp = s_tmp.replace("\\\\","\\")
                Color_PO.outColor([{"34": d_1}])
                Log_PO.logger.info(d_1)
                l_count.append(1)
            else:
                d_1['正向'] = 'error'
                d_1['既往疾病包含'] = varDisease
                d_1.update(d_tmp)
                s_tmp= str(d_1)
                s_tmp = s_tmp.replace("\\\\","\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库f_resut, f_updateDate
            d_result = {}
            if 0 not in l_count:
                d_result['ID'] = ID
                d_result['result'] = "ok"
                Color_PO.outColor([{"32": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableER, d_result['result'], d_result['ID']))
            else:
                d_result['ID'] = ID
                d_result['result'] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableER, d_result['result'],d_result['ID']))
        else:
            print("1750, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_disease_n(self, varDisease, ID):

        # 既往疾病(执行反向用例)
        # varDisease = 脑卒中
        # id = 46

        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_ERcode from %s where ID= %s" % (self.tableER, ID))
        d_tmp['评估因素编码'] = l_d_row[0]['f_ERcode']

        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = 2  # //测试id，位于WEIGHT_REPORT表
        d_tmp['身份证'] = '420204202201011268'

        varAge = 0
        varAgeFloat = 0.0
        varAgeMonth = 0
        varBMI = 10.1

        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":'+ str(varAge) +',\\"ageFloat\\":'+ str(varAgeFloat) +',\\"ageMonth\\":'+ str(varAgeMonth) +',\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":'+str(varBMI)+',\\"categoryCode\\":1,\\"disease\\":\\"'+str(varDisease)+'\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\\":\\"' + str(d_tmp['身份证']) + '\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"\\",\\"sexCode\\":\\"1\\",\\"weight\\":55,\\"weightReportId\\":' + str(d_tmp['WEIGHT_REPORT__ID']) + '}"'

        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command
        # print(d_r)

        if d_r['code'] == 200:
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            # 可能命中多条
            # print(l_d_RULE_CODE_actual)  # [{'RULE_CODE': 'TZ_RQFL004'}, {'RULE_CODE': 'TZ_AGE001'}, {'RULE_CODE': 'TZ_JWJB001'}]
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['f_ERcode']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            l_count = []
            d_2 = {}
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                d_2['反向'] = 'error'
                d_2['既往疾病'] = varDisease
                s_tmp = str(d_2)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
            else:
                d_2['反向'] = "ok"
                d_2['既往疾病'] = varDisease
                Color_PO.outColor([{"36": d_2}])
                Log_PO.logger.info(d_2)



            # # 回写数据库f_resut, f_updateDate
            # if 0 not in l_count:
            #     Color_PO.outColor([{"32": "[ID: " + str(ID) + "] => ok"}])
            #     Log_PO.logger.info([{"32": "ok, id=" + str(ID)}])
            #     Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where ID = %s" % (self.tableER, ID))
            # else:
            #     Color_PO.outColor([{"32": "[ID: " + str(ID) + "] => error"}])
            #     Log_PO.logger.info([{"31": "error, id=" + str(ID)}])
            #     Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableER, ID))
        else:
            print("1750, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_crowd(self, varCatatoryId, ID):

        # 人群分类
        # varDisease = 高血压
        # id = 46

        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_ERcode from %s where ID= %s" % (self.tableER, ID))
        d_tmp['评估因素编码'] = l_d_row[0]['f_ERcode']

        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = 2  # //测试id，位于WEIGHT_REPORT表
        d_tmp['身份证'] = '420204202201011268'

        varAge = 0
        varAgeFloat = 0.0
        varAgeMonth = 0
        varBMI = 10.1

        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":'+ str(varAge) +',\\"ageFloat\\":'+ str(varAgeFloat) +',\\"ageMonth\\":'+ str(varAgeMonth) +',\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":'+str(varBMI)+',\\"categoryCode\\":'+str(varCatatoryId)+',\\"disease\\":\\"\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\\":\\"' + str(d_tmp['身份证']) + '\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"\\",\\"sexCode\\":\\"1\\",\\"weight\\":55,\\"weightReportId\\":' + str(d_tmp['WEIGHT_REPORT__ID']) + '}"'

        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command
        # print(d_r)

        if d_r['code'] == 200:
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            # 可能命中多条
            # print(l_d_RULE_CODE_actual)  # [{'RULE_CODE': 'TZ_RQFL004'}, {'RULE_CODE': 'TZ_AGE001'}, {'RULE_CODE': 'TZ_JWJB001'}]
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['f_ERcode']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            l_count = []
            d_1 = {}
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                d_1['正向'] = 'ok'
                d_1['人群分类'] = varCatatoryId
                Color_PO.outColor([{"34": d_1}])
                Log_PO.logger.info(d_1)
                l_count.append(1)
            else:
                d_1['正向'] = 'error'
                d_1['人群分类'] = varCatatoryId
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库f_resut, f_updateDate
            d_result = {}
            if 0 not in l_count:
                d_result["ID"] = ID
                d_result["result"] = "ok"
                Color_PO.outColor([{"32": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableER, d_result["result"], d_result["ID"]))
            else:
                d_result["ID"] = ID
                d_result["result"] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableER, d_result["result"], d_result["ID"]))
        else:
            print("175110, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_crowd_1(self, ID, d_param):

        # 人群分类
        # varDisease = 高血压
        # id = 46
        print("d_param", d_param)
        if "sex" in d_param:
            if d_param['sex'] == "男":
                varSexCode = "1"
            elif d_param['sex'] == "女":
                varSexCode = "2"
        else:
            varSexCode = "1"

        # sys.exit(0)
        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_ER, f_ERcode from %s where ID= %s" % (self.tableER, ID))
        d_tmp['评估因素编码'] = l_d_row[0]['f_ERcode']
        categoryCode = l_d_row[0]['f_ER']

        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = 2  # //测试id，位于WEIGHT_REPORT表
        d_tmp['身份证'] = '420204202201011268'

        varAge = 0
        varAgeFloat = 0.0
        varAgeMonth = 0
        varBMI = 10.1

        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":'+ str(varAge) +',\\"ageFloat\\":'+ str(varAgeFloat) +',\\"ageMonth\\":'+ str(varAgeMonth) +',\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":'+str(varBMI)+',\\"categoryCode\\":'+str(categoryCode)+',\\"disease\\":\\"\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\\":\\"' + str(d_tmp['身份证']) + '\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"\\",\\"sexCode\\":\\"' + str(varSexCode) + '\\",\\"weight\\":55,\\"weightReportId\\":' + str(d_tmp['WEIGHT_REPORT__ID']) + '}"'

        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command
        # print(d_r)
        # print(command)

        if d_r['code'] == 200:
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            # 可能命中多条
            # print(l_d_RULE_CODE_actual)  # [{'RULE_CODE': 'TZ_RQFL004'}, {'RULE_CODE': 'TZ_AGE001'}, {'RULE_CODE': 'TZ_JWJB001'}]
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['f_ERcode']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            l_count = []
            d_1 = {}
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                d_1['正向'] = 'ok'
                d_1['人群分类'] = categoryCode
                Color_PO.outColor([{"34": d_1}])
                Log_PO.logger.info(d_1)
                l_count.append(1)
            else:
                d_1['正向'] = 'error'
                d_1['人群分类'] = categoryCode
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库f_resut, f_updateDate
            d_result = {}
            if 0 not in l_count:
                d_result["ID"] = ID
                d_result["result"] = "ok"
                Color_PO.outColor([{"32": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableER, d_result["result"], d_result["ID"]))
            else:
                d_result["ID"] = ID
                d_result["result"] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableER, d_result["result"], d_result["ID"]))
        else:
            print("2333, error ", d_r['code'])
            sys.exit(0)
    def _EFRB_run(self, d_cases_satisfied, ID, d_param):

        # 公共测试用例

        # d_cases_satisfied = {'BMI': 16.8}
        # id = 1
        # d_param = {'categoryCode': 1, 'disease': '脑卒中'}

        # print(d_cases_satisfied)
        # print(ID)
        # print(d_param)
        # sys.exit(0)

        d_tmp = {}

        # 参数
        # 获取f_ERcode,f_age
        l_d_row = Sqlserver_PO_CHC5G.select("select f_crowd, f_crowdCode, f_ageType, f_ERcode from %s where ID= %s" % (self.tableER, ID))
        # print(l_d_row)
        d_tmp['人群分类'] = l_d_row[0]['f_crowd']
        d_tmp['人群分类编码'] = l_d_row[0]['f_crowdCode']
        d_tmp['年龄类型'] = l_d_row[0]['f_ageType']
        d_tmp['评估因素编码'] = l_d_row[0]['f_ERcode']
        # d_tmp['条件'] = l_d_row[0]['f_ER']

        if d_param == {}:
            d_param = {'categoryCode': d_tmp['人群分类编码'], 'disease': '脑卒中'}

        # print(d_tmp)
        # sys.exit(0)

        # 参数化
        WEIGHT_REPORT__ID = 2  # //测试id，位于WEIGHT_REPORT表
        d_tmp['WEIGHT_REPORT__ID'] = 2
        d_tmp['身份证'] = '420204202201011268'

        # BMI
        if 'BMI' in d_cases_satisfied:
            varBMI = d_cases_satisfied['BMI']
        else:
            varBMI = 0

        # 年龄
        if d_tmp['年龄类型'] == "int":
            if d_tmp['人群分类'] == "儿童":
                varAgeMonth = d_cases_satisfied['年龄']
                varAge = 0
                varAgeFloat = 0.0
            else:
                varAgeMonth = 0
                varAge = d_cases_satisfied['年龄']
                varAgeFloat = 0.0
        elif d_tmp['年龄类型'] == "float":
            varAgeFloat = d_cases_satisfied['年龄']
            varAge = 0
            varAgeMonth = 0

        # 性别
        if '性别' in d_cases_satisfied:
            if d_cases_satisfied['性别'] == "女":
                varSexCode = '2'
                varSex = "女"
            else:
                varSexCode = '1'
                varSex = '男'
        else:
            varSexCode = '1'
            varSex = '男'

        # print("d_cases_satisfied:", d_cases_satisfied)
        # print("d_param: ", d_param)

        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":'+ str(varAge) +',\\"ageFloat\\":'+ str(varAgeFloat) +',\\"ageMonth\\":'+ str(varAgeMonth) +',\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":' + str(varBMI) + ',\\"categoryCode\\":' + str(d_param['categoryCode']) + ',\\"disease\\":\\"' + str(d_param['disease']) + '\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\\":\\"' + str(d_tmp['身份证']) + '\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"' + str(varSex) + '\\",\\"sexCode\\":\\"' + str(varSexCode) + '\\",\\"weight\\":55,\\"weightReportId\\":' + str(d_tmp['WEIGHT_REPORT__ID']) + '}"'

        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command

        # print(command)
        # print(d_r)

        if d_r['code'] == 200:

            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            # 可能命中多条
            # print(l_d_RULE_CODE_actual)  # [{'RULE_CODE': 'TZ_RQFL004'}, {'RULE_CODE': 'TZ_AGE001'}, {'RULE_CODE': 'TZ_JWJB001'}]
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['f_ERcode']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            # l_count = []
            # if d_tmp['预期值'] in l_d_RULE_CODE_actual:


            # d_tmp['实际值'] = l_d_RULE_CODE_actual[0]['RULE_CODE']
            # d_tmp['预期值'] = l_d_row[0]['f_ERcode']
            # d_tmp['sql__T_ASSESS_RULE_RECORD'] = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2 and RULE_GROUP='weight'"

            return d_tmp

        else:
            print("4218, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_p(self, d_cases_satisfied, ID, d_param):

        d_tmp = self._EFRB_run(d_cases_satisfied, ID, d_param)
        # if d_tmp['实际值'] == d_tmp['预期值']:
        if d_tmp['预期值'] in d_tmp['实际值']:
            d_tmp['result'] = 1
        else:
            d_tmp['result'] = 0
        return d_tmp
    def EFRB_run_n(self, d_cases_satisfied, ID, d_param):

        d_tmp = self._EFRB_run(d_cases_satisfied, ID, d_param)
        # if d_tmp['实际值'] == d_tmp['预期值']:
        if d_tmp['预期值'] in d_tmp['实际值']:
            d_tmp['result'] = 0
        else:
            d_tmp['result'] = 1
        return d_tmp


    def ss(self, f_IR):
        # 字符串转字典，将 （TZ_STZB042 = '是' and TZ_JWJB001 = '否' ） 转为字典{'TZ_STZB042': '是', 'TZ_JWJB001': '否'}
        pairs = [pair.strip() for pair in f_IR.split('and')]
        d_IR = {}
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=')
                d_IR[key.strip()] = value.strip().replace("'", "")
        # print(d_IR) # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        return d_IR

    # 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)
    def HIRB(self, varTestID="all"):

        # 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)
        # a_weight10_HIRB

        d_tmp = {}
        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_IRcode, f_IR from %s" % (self.tableIR))
        # print("l_d_row => ", l_d_row)  # [{'ID': 1, 'f_IRcode': 'TZ_YS001', 'f_IR': "TZ_RQFL001='是' and TZ_STZB001='是' and TZ_JWJB001='否' and TZ_JWJB002='否'"},...
        # sys.exit(0)
        if varTestID > len(l_d_row):
            print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
            sys.exit(0)

        for i in enumerate(l_d_row):
            i = varTestID - 1
            IR_ID = l_d_row[i]['ID']
            f_IRcode = l_d_row[i]['f_IRcode']
            f_IR = l_d_row[i]['f_IR']

            # 获取原始数据
            d_tmp['表'] = self.tableIR
            d_tmp['ID'] = IR_ID
            d_tmp['干预规则f_IR'] = f_IR
            s = "健康干预规则库（其他分类）HIRB => " + str(d_tmp)
            print(s)
            Log_PO.logger.info(s)

            # # 字符串转字典，{'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
            # pairs = [pair.strip() for pair in f_IR.split('and')]
            # d_IR = {}
            # for pair in pairs:
            #     if '=' in pair:
            #         key, value = pair.split('=')
            #         d_IR[key.strip()] = value.strip().replace("'", "")
            # # print(d_IR) # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}


            if "or" in f_IR and "and" not in f_IR:
                ...
                # TZ_STZB043='是' or TZ_STZB044='是' or TZ_STZB045='是'
                l_value = f_IR.split("or")
                # print(l_value)
                l_4 = []
                for i in l_value:
                    l_4.append(self.ss(i))
                # l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
                # l_value = [i.split("and") for i in l_value]
                # l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
                # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
                print(l_4)
                # sys.exit(0)
                # d_IR = self.ss(f_IR)
                self.HIRB_case_or(IR_ID, f_IRcode, l_4)

            # todo HIRB 复杂条件组合
            if "or" in f_IR and "and" in f_IR:
                # (TZ_STZB002='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否') or (TZ_STZB005='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否')

                # # 字符串转字典，{'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
                # pairs = [pair.strip() for pair in f_IR.split('and')]
                # d_IR = {}
                # for pair in pairs:
                #     if '=' in pair:
                #         key, value = pair.split('=')
                #         d_IR[key.strip()] = value.strip().replace("'", "")
                # print(d_IR) # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}

                # 转换列表，结构化原始数据为列表，生成l_l_N
                l_value = f_IR.split("or")
                # print(l_value)
                l_4 = []
                for i in l_value:
                    i = i.replace("(",'').replace(")",'')
                    l_4.append(self.ss(i))
                # l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
                # l_value = [i.split("and") for i in l_value]
                # l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
                # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
                print(l_4)
                # sys.exit(0)
                # d_IR = self.ss(f_IR)
                self.HIRB_case_or(IR_ID, f_IRcode, l_4)
                sys.exit(0)

                l_result = []
                sum = 0
                for lln in range(len(l_l_value)):
                    l_2_value = []
                    # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                    # print(l_l_value(lln))
                    for i in l_l_value[lln]:
                        if "BMI" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                        if "年龄" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                        elif "性别" in i:
                            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                            l_2_value.extend(l_simple_conditions)
                    # print("611 分解参数 =", l_2_value)

                    # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                    l_3_value = []
                    for i in l_2_value:
                        l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                        l_3_value.extend(l_simple_conditions)
                    # print("618 结构化参数 =", l_3_value)

                    # 读取BmiAgeSex模块，生成随机数据d_cases
                    # d_cases = BmiAgeSex_PO.generate_all_cases(l_3_value)

                    for i in l_3_value:
                        if ('>=' or '<=') in i:
                            if '年龄' in i:
                                d_cases = BmiAgeSex_PO.main(l_3_value)
                                break
                            if 'BMI' in i:
                                d_cases = BmiAgeSex_PO.main(l_3_value)
                                break
                        else:
                            d_cases = BmiAgeSex_PO.main(l_3_value)

                    print("--------------------")
                    print("测试数据集合 =>", d_cases)
                    sys.exit(0)

                    # 判断输出结果
                    # todo HIRB_case for or
                    # self.HIRB_case(IR_ID, f_IRcode, d_IR)
                    varTestCount = 0
                    varTestcase, varCount = self.HIRB_case_or(d_cases, id, l_2_value, lln + 1, varTestCount + 1)
                    # varTestcase, varCount = self.EFRB_case_or(d_cases, id, l_2_value, lln + 1, varTestCount + 1)
                    l_result.append(varCount)
                    sum = sum + varTestcase

                # print(l_result)

                # 回写数据库f_resut, f_updateDate
                if 0 not in l_result:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => ok"}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                            self.tableER, sum, id))

                else:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                            self.tableER, sum, id))

            # todo HIRB 简单条件组合
            elif "and" in f_IR:
                # 测试数据
                # todo HIRB for and

                d_IR = self.ss(f_IR)
                self.HIRB_case(IR_ID, f_IRcode, d_IR)

            # todo HIRB 无条件组合
            elif "and" not in f_IR:

                # l_2_value = []
                # # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                # l_simple_conditions = Bmi_PO.splitMode(f_IR)
                # l_2_value.extend(l_simple_conditions)
                # # print("611 分解参数 =", l_2_value)
                #
                # # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                # l_3_value = []
                # for i in l_2_value:
                #     l_simple_conditions = Bmi_PO.interconvertMode(i)
                #     l_3_value.extend(l_simple_conditions)
                # # print("680 结构化参数 =", l_3_value)  # ['BMI<18.5']
                #
                # # 读取BMI模块，生成随机数据d_cases
                # d_cases = Age_PO.generate_all_cases(l_3_value)
                # # d_cases = Bmi_PO.generate_all_cases(l_3_value)
                # print(d_cases)  # {'satisfied': [{'BMI': 16.8}], 'not1': [{'BMI': 19.6}]}

                # todo EFRB_case for not and
                # 判断输出结果
                d_IR = self.ss(f_IR)
                print(d_IR)
                self.HIRB_case(IR_ID, f_IRcode, d_IR)

            else:
                print("[not or & and ]")
            print("-".center(100, "-"))

            break
    def HIRB_case(self, IR_ID, f_IRcode, d_IR):

        # 执行ER中规则
        # print("f_IRcode", f_IRcode)  # TZ_YS001
        # print("d_IR", d_IR)  # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        # sys.exit(0)

        d_tmp = {}

        # 遍历a_weight10_ER
        l_f_ERcode = Sqlserver_PO_CHC5G.select("select ID, f_ERcode from a_weight10_ER")
        # print(l_f_ERcode)
        d_f_ERcode = {item['ID']: item['f_ERcode'] for item in l_f_ERcode}
        # print(d_f_ERcode)  # {1: 'TZ_STZB001', 2: 'TZ_STZB002', ...
        d_f_ERcode = {v: k for k, v in d_f_ERcode.items()}
        # print(d_f_ERcode)  # {'TZ_STZB001': 1, 'TZ_STZB002': 2,

        #  过滤掉TZ_STZB开头的key
        d_filtered = {key: value for key, value in d_IR.items() if 'TZ_STZB' not in key}
        print("过滤掉TZ_STZB开头的key：", d_filtered) # {'TZ_RQFL001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}

        # 先遍历否
        # 定义遍历顺序
        order = ['否', '是']

        # 按照定义的顺序遍历字典
        d_4 = {}
        for value in order:
            for key, val in d_filtered.items():
                if val == value:
                    # print(f"键: {key}, 值: {val}")
                    l_ = Sqlserver_PO_CHC5G.select("select f_ER from a_weight10_ER where f_ERcode='%s'" % (key))
                    # print(l_) # [{'f_ER': '3'}]
                    if val == "否" and "TZ_RQFL" in key:
                        d_4['categoryCode'] = 100
                    if key == 'TZ_JWJB001' and val == "否":
                        d_4['disease'] = "脑卒中"
                    if key == 'TZ_JWJB002' and val == "否":
                        d_4['disease'] = "脑卒中"
                    if val == "是" and "TZ_RQFL" in key:
                        d_4['categoryCode'] = int(l_[0]['f_ER'])
                    if key == 'TZ_JWJB001' and val == "是":
                        d_4['disease'] = l_[0]['f_ER']
                    if key == 'TZ_JWJB002' and val == "是":
                        d_4['disease'] = l_[0]['f_ER']
        # print(d_4)
        d_param = d_4
        if "categoryCode" not in d_param:
            d_param['categoryCode'] = 100
        if "disease" not in d_param:
            d_param['disease'] = "脑卒中"
        # sys.exit(0)


        # 获取 TZ_STZB开头的key
        l_matching_keys = [key for key in d_IR if 'TZ_STZB' in key]
        print(l_matching_keys) # ['TZ_STZB001']
        if l_matching_keys != []:
            l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_ER where f_ERcode='%s'" % (l_matching_keys[0]))
            # print(l_1) # [{'ID': '3'}]
            # d_param['ID']

            if len(l_matching_keys) == 1:
                # print(l_1[0]['ID'], d_param)
                self.EFRB_1(l_1[0]['ID'], d_param)
            else:
                print("warning, 匹配到多个值：",l_matching_keys)
                sys.exit(0)

        l_matching_keys = [key for key in d_IR if 'TZ_RQFL' in key]
        print(l_matching_keys)  # ['TZ_STZB001']
        if l_matching_keys != []:
            l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_ER where f_ERcode='%s'" % (l_matching_keys[0]))
            if len(l_matching_keys) == 1:
                # print(l_1[0]['ID'], d_param)
                self.EFRB_1(l_1[0]['ID'], d_param)
            else:
                print("warning, 匹配到多个值：",l_matching_keys)
                sys.exit(0)

        l_matching_keys = [key for key in d_IR if 'TZ_AGE' in key]
        print(l_matching_keys)  # ['TZ_STZB001']
        if l_matching_keys != []:
            l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_ER where f_ERcode='%s'" % (l_matching_keys[0]))
            if len(l_matching_keys) == 1:
                # print(l_1[0]['ID'], d_param)
                self.EFRB_1(l_1[0]['ID'], d_param)
            else:
                print("warning, 匹配到多个值：", l_matching_keys)
                sys.exit(0)

        # 检查是否命中f_IRcode
        sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
        l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)

        l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
        # print(l_d_RULE_CODE_actual) # ['TZ_STZB001', 'TZ_RQFL001', 'TZ_SRL001', 'TZ_MBTZ002', 'TZ_YD001', 'TZ_YS001']

        d_tmp['实际值'] = l_d_RULE_CODE_actual
        d_tmp['预期值'] = f_IRcode
        d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
        l_count = []
        d_result = {}
        if d_tmp['预期值']  in l_d_RULE_CODE_actual:
            # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
            Color_PO.outColor([{"34": d_tmp}])
            Log_PO.logger.info(d_tmp)
            d_result['result'] = "ok"
            d_result['ID'] = IR_ID
            Color_PO.outColor([{"32": d_result}])
            Log_PO.logger.info(d_result)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableIR, IR_ID))

        else:
            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => error"}])
            Log_PO.logger.info([{"31": "error, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableIR, IR_ID))





        sys.exit(0)

        # 检查是否命中f_IRcode
        sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
        l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
        l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
        d_tmp['f_IRcode'] = f_IRcode
        d_tmp['实际值'] = l_d_RULE_CODE_actual
        d_tmp['预期值'] = f_IRcode
        d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
        l_count = []
        if d_tmp['预期值'] in l_d_RULE_CODE_actual:
            # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
            Color_PO.outColor([{"34": d_tmp}])
            Log_PO.logger.info(d_tmp)

            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => ok"}])
            Log_PO.logger.info([{"32": "ok, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableIR, id))

        else:
            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => error"}])
            Log_PO.logger.info([{"31": "error, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableIR, id))

        sys.exit(0)

        if len(d_cases['satisfied']) == 1:
            # 一条数据，正向用例
            l_count = []
            # todo EFRB_run_p_1
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], ID)
            if d_tmp['result'] == 1:
                if d_tmp['result'] == 1:
                    s_print = "[正向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][0])
                    Color_PO.outColor([{"34": s_print}])
                    Color_PO.outColor([{"34": d_tmp}])
                    Log_PO.logger.info(s_print)
                    l_count.append(1)
                else:
                    s_print = "[正向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][0])
                    Color_PO.outColor([{"31": s_print}])
                    Log_PO.logger.info(s_print)
                    Color_PO.outColor([{"33": d_tmp}])
                    Log_PO.logger.info(d_tmp)
                    l_count.append(0)
                varTestcase = varTestcase + 1

                # 一条数据，反向用例
                # todo EFRB_run_n
                if Configparser_PO.SWITCH("testNegative") == "on":

                    if Configparser_PO.SWITCH("testNegative") == "on":
                        d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], ID)
                        if d_tmp['result'] == 1:
                            s_print = "[反向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][0])
                            Color_PO.outColor([{"31": s_print}])
                            Log_PO.logger.info(s_print)
                            Color_PO.outColor([{"33": d_tmp}])
                            Log_PO.logger.info(d_tmp)
                            l_count.append(0)
                        else:
                            s_print = "[反向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][0])
                            Color_PO.outColor([{"36": s_print}])
                            Log_PO.logger.info(s_print)
                            l_count.append(1)
                        varTestcase = varTestcase + 1

                # 回写数据库f_resut, f_updateDate
                if 0 not in l_count:
                    Color_PO.outColor([{"32": "[ID: " + str(ID) + "] => ok"}])
                    Log_PO.logger.info([{"32": "ok, id=" + str(ID)}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                        self.tableWS, varTestcase, ID))
                else:
                    Color_PO.outColor([{"32": "[ID: " + str(ID) + "] => error"}])
                    Log_PO.logger.info([{"31": "error, id=" + str(ID)}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                        self.tableWS, varTestcase, ID))
        else:
            # 正向用例, N个数据
            l_count = []
            for i in range(len(d_cases['satisfied'])):
                # print(d_cases)
                # todo EFRB_run_p_n
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], ID)
                if d_tmp['result'] == 1:
                    s_print = "[正向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][i])
                    Color_PO.outColor([{"34": s_print}])
                    s_tmp = str(d_tmp)
                    s_tmp = s_tmp.replace("\\\\","\\")
                    Color_PO.outColor([{"34": s_tmp}])
                    Log_PO.logger.info(s_print)
                    varTestcase = varTestcase + 1
                    l_count.append(1)
                else:
                    s_print = "[正向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][i])
                    Color_PO.outColor([{"31": s_print}])
                    Log_PO.logger.info(s_print)
                    Color_PO.outColor([{"33": d_tmp}])
                    Log_PO.logger.info(d_tmp['i'])
                    # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                    # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                    varTestcase = varTestcase + 1
                    l_count.append(0)

            # 反向用例, N个数据
            if Configparser_PO.SWITCH("testNegative") == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    # todo DRWS_run_n_n
                    d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][i], ID)
                    if d_tmp['result'] == 1:
                        # 反向如果命中就错，并且终止循环
                        s_print = "[反向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][i])
                        Color_PO.outColor([{"31": s_print}])
                        Log_PO.logger.info(s_print)
                        s_tmp = str(d_tmp)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])

                        # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                        # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                        varTestcase = varTestcase + 1
                        l_count.append(0)
                    else:
                        s_print = "[反向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][i])
                        Color_PO.outColor([{"36": s_print}])
                        Log_PO.logger.info(s_print)
                        varTestcase = varTestcase + 1
                        l_count.append(1)

            # 回写数据库f_resut, f_updateDate
            if 0 not in l_count:
                s_print = "[ID: " + str(ID) + "] => OK"
                Color_PO.outColor([{"32": s_print}])
                Log_PO.logger.info(s_print)
                Sqlserver_PO_CHC5G.execute(
                    "update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                    self.tableER, varTestcase, ID))
            else:
                s_print = "[ID: " + str(ID) + "] => ERROR"
                Color_PO.outColor([{"31": s_print}])
                Log_PO.logger.info(s_print)
                Sqlserver_PO_CHC5G.execute(
                    "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                    self.tableER, varTestcase, ID))

        #         # 反向用例, 不满足条件的v[0]，预期不命中。
        #         del d_cases['satisfied']
        #         varCount = 2
        #         for k, v in d_cases.items():
        #             # print(v[0])
        #             # todo EFRB_run_n
        #             varCount = self.EFRB_run_n(v[0], id, self.tableER)
        #             if varCount == 1:
        #                 # 反向如果命中就错，并且终止循环
        #                 Color_PO.outColor([{"31": "p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
        #                 # Log_PO.logger.info("p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
        #                 # varTestcase = varTestcase + 1
        #                 # Color_PO.outColor([{"33": d_tmp}])
        #
        #                 # print("步骤1 => ", d_tmp["i"])
        #                 # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #                 # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #                 Log_PO.logger.info("ID = " + str(id) + ", p3, 反向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #                     str(v[0])))
        #                 # Log_PO.logger.info(d_tmp['i'])
        #                 # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #                 # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #                 varTestcase = varTestcase + 1
        #
        #                 # print("p3, 反向error, 条件：", l_N, "，不满足：", v[0])
        #                 break
        #             else:
        #                 Color_PO.outColor([{"34": "p4, 反向ok, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
        #                 Log_PO.logger.info("p4, 反向ok, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
        #                 varTestcase = varTestcase + 1
        #                 # print("p4, 反向ok, 条件：", l_N, "，不满足：", v[0], " > 不命中")
        #                 # Ellipsis
        #     else:
        #         Color_PO.outColor([{"31": "ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #             d_cases['satisfied'][0])}])
        #         # Color_PO.outColor([{"33": d_tmp}])
        #
        #         # print("步骤1 => ", d_tmp["i"])
        #         # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #         # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #         Log_PO.logger.info("ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #             d_cases['satisfied'][0]))
        #         # Log_PO.logger.info(d_tmp['i'])
        #         # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #         # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #         varTestcase = varTestcase + 1
        #
        #         # Color_PO.outColor([{"31": "p2, 正向error, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0])}])
        #         # Log_PO.logger.info("p2, 正向error, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0]))
        #         # varTestcase = varTestcase + 1
        #         # print("p2, 正向error, 条件：", l_N, "，满足：", d_cases['satisfied'][0], varCount)
        #         # Ellipsis
        #
        #     # 回写数据库f_resut, f_updateDate
        #     if varCount == 2:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => ok"}])
        #         Log_PO.logger.info([{"32": "ok, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        #     else:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
        #         Log_PO.logger.info([{"31": "error, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        # else:
        #     for i in range(len(d_cases['satisfied'])):
        #         # print(d_cases)
        #         # todo EFRB_run_p_n
        #         result = self.EFRB_run_p(d_cases['satisfied'][i], id, self.tableER)
        #         if result == 1:
        #             s_print = "[正向ok], 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][i])
        #             Color_PO.outColor([{"34": s_print}])
        #             Log_PO.logger.info(s_print)
        #             varTestcase = varTestcase + 1
        #         else:
        #             s_print = "[正向error], 条件：" + str(l_2_value) + "，不满足：" + str(d_cases['satisfied'][i])
        #             Color_PO.outColor([{"31": s_print}])
        #             Log_PO.logger.info(s_print)
        #             # Color_PO.outColor([{"33": d_tmp}])
        #             # Log_PO.logger.info(d_tmp['i'])
        #             # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #             varTestcase = varTestcase + 1
        #
        #
        #     # 反向用例, 不满足条件的v[0]，预期不命中。
        #     del d_cases['satisfied']
        #     varCount = 2
        #     for k, v in d_cases.items():
        #         # todo EFRB_run_n_n
        #         varCount = self.EFRB_run_n(v[0], id, self.tableER)
        #         if varCount == 1:
        #             # 反向如果命中就错，并且终止循环
        #             s_print = "[反向error], 条件：" + str(l_2_value) + "，不满足：" + str(v[0])
        #             Color_PO.outColor([{"31": s_print}])
        #             Log_PO.logger.info(s_print)
        #             # varTestcase = varTestcase + 1
        #             # Color_PO.outColor([{"33": d_tmp}])
        #
        #             # print("步骤1 => ", d_tmp["i"])
        #             # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['i'])
        #             # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #             varTestcase = varTestcase + 1
        #         else:
        #             s_print = "[反向ok], 条件：" + str(l_2_value) + "，不满足：" + str(v[0])
        #             Color_PO.outColor([{"34": s_print}])
        #             Log_PO.logger.info(s_print)
        #             varTestcase = varTestcase + 1
        #
        #         # 回写数据库f_resut, f_updateDate
        #     if varCount == 2:
        #         s_print = "ID = " + str(id) + ", 结果：ok"
        #         Color_PO.outColor([{"32": s_print}])
        #         Log_PO.logger.info([{"32": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        #     else:
        #         s_print = "ID = " + str(id) + ", 结果：error"
        #         Color_PO.outColor([{"31": s_print}])
        #         Log_PO.logger.info([{"31": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
    def HIRB_case_or(self, IR_ID, f_IRcode, l_4):

        # 执行ER中规则
        # print("f_IRcode", f_IRcode)  # TZ_YS001
        # print("d_IR", d_IR)  # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        # sys.exit(0)

        d_tmp = {}

        # 遍历a_weight10_ER
        l_f_ERcode = Sqlserver_PO_CHC5G.select("select ID, f_ERcode from a_weight10_ER")
        # print(l_f_ERcode)
        d_f_ERcode = {item['ID']: item['f_ERcode'] for item in l_f_ERcode}
        # print(d_f_ERcode)  # {1: 'TZ_STZB001', 2: 'TZ_STZB002', ...
        d_f_ERcode = {v: k for k, v in d_f_ERcode.items()}
        # print(d_f_ERcode)  # {'TZ_STZB001': 1, 'TZ_STZB002': 2,

        sum = 0
        print("l_4", l_4)

        for d_ in l_4:

            #  过滤掉TZ_STZB开头的key
            d_filtered = {key: value for key, value in d_.items() if 'TZ_STZB' not in key}
            # print("过滤掉TZ_STZB开头的key：", d_filtered) # {'TZ_RQFL001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}

            # 先遍历否
            # 定义遍历顺序
            order = ['否', '是']

            # 按照定义的顺序遍历字典
            d_param = {}
            for value in order:
                for key, val in d_filtered.items():
                    if val == value:
                        # print(f"键: {key}, 值: {val}")
                        l_ = Sqlserver_PO_CHC5G.select("select f_ER from a_weight10_ER where f_ERcode='%s'" % (key))
                        # print(l_) # [{'f_ER': '3'}]
                        if val == "否" and "TZ_RQFL" in key:
                            d_param['categoryCode'] = 100
                        if key == 'TZ_JWJB001' and val == "否":
                            d_param['disease'] = "脑卒中"
                        if key == 'TZ_JWJB002' and val == "否":
                            d_param['disease'] = "脑卒中"
                        if val == "是" and "TZ_RQFL" in key:
                            d_param['categoryCode'] = int(l_[0]['f_ER'])
                        if key == 'TZ_JWJB001' and val == "是":
                            d_param['disease'] = l_[0]['f_ER']
                        if key == 'TZ_JWJB002' and val == "是":
                            d_param['disease'] = l_[0]['f_ER']
                    if key == "性别":
                        d_param['sex'] = val

            if "categoryCode" not in d_param:
                d_param['categoryCode'] = 100
            if "disease" not in d_param:
                d_param['disease'] = "脑卒中"
            if "sex" not in d_param:
                d_param['sex'] = "男"
            print(d_param)



            # 获取 TZ_STZB开头的key
            l_matching_keys = [key for key in d_ if 'TZ_STZB' in key]
            # print(l_matching_keys) # ['TZ_STZB001']
            if l_matching_keys != []:
                l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_ER where f_ERcode='%s'" % (l_matching_keys[0]))
                if len(l_matching_keys) == 1:
                    # print(l_1[0]['ID'], d_param)
                    count = self.EFRB_1(l_1[0]['ID'], d_param)
                    # print(count)
                    # sum = sum + int(count)
                else:
                    print("warning, 匹配到多个值：",l_matching_keys)
                    sys.exit(0)

            l_matching_keys = [key for key in d_ if 'TZ_RQFL' in key]
            # print(l_matching_keys) # ['TZ_STZB001']
            if l_matching_keys != []:
                l_1 = Sqlserver_PO_CHC5G.select(
                    "select ID from a_weight10_ER where f_ERcode='%s'" % (l_matching_keys[0]))
                if len(l_matching_keys) == 1:
                    # print(l_1[0]['ID'], d_param)
                    count = self.EFRB_1(l_1[0]['ID'], d_param)
                else:
                    print("warning, 匹配到多个值：", l_matching_keys)
                    sys.exit(0)

            # 检查是否命中f_IRcode
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)

            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
            # print(l_d_RULE_CODE_actual) # ['TZ_STZB001', 'TZ_RQFL001', 'TZ_SRL001', 'TZ_MBTZ002', 'TZ_YD001', 'TZ_YS001']

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = f_IRcode
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            l_count = []
            d_result = {}

            if d_tmp['预期值']  in l_d_RULE_CODE_actual:
                # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
                Color_PO.outColor([{"34": d_tmp}])
                Log_PO.logger.info(d_tmp)
                d_result['result'] = "ok"
                d_result['ID'] = IR_ID
                Color_PO.outColor([{"32": d_result}])
                Log_PO.logger.info(d_result)
                sum = sum + 1
            else:
                d_result['result'] = "error"
                d_result['ID'] = IR_ID
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                s_tmp = str(d_tmp)
                s_tmp = s_tmp.replace("\\\\","\\")
                Color_PO.outColor([{"31": s_tmp}])
                sum = sum + 0


        if sum == len(l_4):

            Sqlserver_PO_CHC5G.execute(
                "update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableIR, IR_ID))
        else:

            Sqlserver_PO_CHC5G.execute(
                "update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableIR, IR_ID))

        sys.exit(0)

        # 检查是否命中f_IRcode
        sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
        l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
        l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
        d_tmp['f_IRcode'] = f_IRcode
        d_tmp['实际值'] = l_d_RULE_CODE_actual
        d_tmp['预期值'] = f_IRcode
        d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
        l_count = []
        if d_tmp['预期值'] in l_d_RULE_CODE_actual:
            # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
            Color_PO.outColor([{"34": d_tmp}])
            Log_PO.logger.info(d_tmp)

            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => ok"}])
            Log_PO.logger.info([{"32": "ok, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableIR, id))

        else:
            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => error"}])
            Log_PO.logger.info([{"31": "error, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableIR, id))

        sys.exit(0)

        if len(d_cases['satisfied']) == 1:
            # 一条数据，正向用例
            l_count = []
            # todo EFRB_run_p_1
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], ID)
            if d_tmp['result'] == 1:
                if d_tmp['result'] == 1:
                    s_print = "[正向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][0])
                    Color_PO.outColor([{"34": s_print}])
                    Color_PO.outColor([{"34": d_tmp}])
                    Log_PO.logger.info(s_print)
                    l_count.append(1)
                else:
                    s_print = "[正向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][0])
                    Color_PO.outColor([{"31": s_print}])
                    Log_PO.logger.info(s_print)
                    Color_PO.outColor([{"33": d_tmp}])
                    Log_PO.logger.info(d_tmp)
                    l_count.append(0)
                varTestcase = varTestcase + 1

                # 一条数据，反向用例
                # todo EFRB_run_n
                if Configparser_PO.SWITCH("testNegative") == "on":

                    if Configparser_PO.SWITCH("testNegative") == "on":
                        d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], ID)
                        if d_tmp['result'] == 1:
                            s_print = "[反向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][0])
                            Color_PO.outColor([{"31": s_print}])
                            Log_PO.logger.info(s_print)
                            Color_PO.outColor([{"33": d_tmp}])
                            Log_PO.logger.info(d_tmp)
                            l_count.append(0)
                        else:
                            s_print = "[反向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][0])
                            Color_PO.outColor([{"36": s_print}])
                            Log_PO.logger.info(s_print)
                            l_count.append(1)
                        varTestcase = varTestcase + 1

                # 回写数据库f_resut, f_updateDate
                if 0 not in l_count:
                    Color_PO.outColor([{"32": "[ID: " + str(ID) + "] => ok"}])
                    Log_PO.logger.info([{"32": "ok, id=" + str(ID)}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                        self.tableWS, varTestcase, ID))
                else:
                    Color_PO.outColor([{"32": "[ID: " + str(ID) + "] => error"}])
                    Log_PO.logger.info([{"31": "error, id=" + str(ID)}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                        self.tableWS, varTestcase, ID))
        else:
            # 正向用例, N个数据
            l_count = []
            for i in range(len(d_cases['satisfied'])):
                # print(d_cases)
                # todo EFRB_run_p_n
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], ID)
                if d_tmp['result'] == 1:
                    s_print = "[正向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][i])
                    Color_PO.outColor([{"34": s_print}])
                    s_tmp = str(d_tmp)
                    s_tmp = s_tmp.replace("\\\\","\\")
                    Color_PO.outColor([{"34": s_tmp}])
                    Log_PO.logger.info(s_print)
                    varTestcase = varTestcase + 1
                    l_count.append(1)
                else:
                    s_print = "[正向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][i])
                    Color_PO.outColor([{"31": s_print}])
                    Log_PO.logger.info(s_print)
                    Color_PO.outColor([{"33": d_tmp}])
                    Log_PO.logger.info(d_tmp['i'])
                    # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                    # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                    varTestcase = varTestcase + 1
                    l_count.append(0)

            # 反向用例, N个数据
            if Configparser_PO.SWITCH("testNegative") == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    # todo DRWS_run_n_n
                    d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][i], ID)
                    if d_tmp['result'] == 1:
                        # 反向如果命中就错，并且终止循环
                        s_print = "[反向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][i])
                        Color_PO.outColor([{"31": s_print}])
                        Log_PO.logger.info(s_print)
                        s_tmp = str(d_tmp)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])

                        # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                        # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                        varTestcase = varTestcase + 1
                        l_count.append(0)
                    else:
                        s_print = "[反向ok], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['notSatisfied'][i])
                        Color_PO.outColor([{"36": s_print}])
                        Log_PO.logger.info(s_print)
                        varTestcase = varTestcase + 1
                        l_count.append(1)

            # 回写数据库f_resut, f_updateDate
            if 0 not in l_count:
                s_print = "[ID: " + str(ID) + "] => OK"
                Color_PO.outColor([{"32": s_print}])
                Log_PO.logger.info(s_print)
                Sqlserver_PO_CHC5G.execute(
                    "update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                    self.tableER, varTestcase, ID))
            else:
                s_print = "[ID: " + str(ID) + "] => ERROR"
                Color_PO.outColor([{"31": s_print}])
                Log_PO.logger.info(s_print)
                Sqlserver_PO_CHC5G.execute(
                    "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                    self.tableER, varTestcase, ID))

        #         # 反向用例, 不满足条件的v[0]，预期不命中。
        #         del d_cases['satisfied']
        #         varCount = 2
        #         for k, v in d_cases.items():
        #             # print(v[0])
        #             # todo EFRB_run_n
        #             varCount = self.EFRB_run_n(v[0], id, self.tableER)
        #             if varCount == 1:
        #                 # 反向如果命中就错，并且终止循环
        #                 Color_PO.outColor([{"31": "p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
        #                 # Log_PO.logger.info("p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
        #                 # varTestcase = varTestcase + 1
        #                 # Color_PO.outColor([{"33": d_tmp}])
        #
        #                 # print("步骤1 => ", d_tmp["i"])
        #                 # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #                 # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #                 Log_PO.logger.info("ID = " + str(id) + ", p3, 反向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #                     str(v[0])))
        #                 # Log_PO.logger.info(d_tmp['i'])
        #                 # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #                 # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #                 varTestcase = varTestcase + 1
        #
        #                 # print("p3, 反向error, 条件：", l_N, "，不满足：", v[0])
        #                 break
        #             else:
        #                 Color_PO.outColor([{"34": "p4, 反向ok, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
        #                 Log_PO.logger.info("p4, 反向ok, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
        #                 varTestcase = varTestcase + 1
        #                 # print("p4, 反向ok, 条件：", l_N, "，不满足：", v[0], " > 不命中")
        #                 # Ellipsis
        #     else:
        #         Color_PO.outColor([{"31": "ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #             d_cases['satisfied'][0])}])
        #         # Color_PO.outColor([{"33": d_tmp}])
        #
        #         # print("步骤1 => ", d_tmp["i"])
        #         # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #         # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #         Log_PO.logger.info("ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
        #             d_cases['satisfied'][0]))
        #         # Log_PO.logger.info(d_tmp['i'])
        #         # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #         # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #         varTestcase = varTestcase + 1
        #
        #         # Color_PO.outColor([{"31": "p2, 正向error, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0])}])
        #         # Log_PO.logger.info("p2, 正向error, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0]))
        #         # varTestcase = varTestcase + 1
        #         # print("p2, 正向error, 条件：", l_N, "，满足：", d_cases['satisfied'][0], varCount)
        #         # Ellipsis
        #
        #     # 回写数据库f_resut, f_updateDate
        #     if varCount == 2:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => ok"}])
        #         Log_PO.logger.info([{"32": "ok, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        #     else:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
        #         Log_PO.logger.info([{"31": "error, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        # else:
        #     for i in range(len(d_cases['satisfied'])):
        #         # print(d_cases)
        #         # todo EFRB_run_p_n
        #         result = self.EFRB_run_p(d_cases['satisfied'][i], id, self.tableER)
        #         if result == 1:
        #             s_print = "[正向ok], 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][i])
        #             Color_PO.outColor([{"34": s_print}])
        #             Log_PO.logger.info(s_print)
        #             varTestcase = varTestcase + 1
        #         else:
        #             s_print = "[正向error], 条件：" + str(l_2_value) + "，不满足：" + str(d_cases['satisfied'][i])
        #             Color_PO.outColor([{"31": s_print}])
        #             Log_PO.logger.info(s_print)
        #             # Color_PO.outColor([{"33": d_tmp}])
        #             # Log_PO.logger.info(d_tmp['i'])
        #             # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #             varTestcase = varTestcase + 1
        #
        #
        #     # 反向用例, 不满足条件的v[0]，预期不命中。
        #     del d_cases['satisfied']
        #     varCount = 2
        #     for k, v in d_cases.items():
        #         # todo EFRB_run_n_n
        #         varCount = self.EFRB_run_n(v[0], id, self.tableER)
        #         if varCount == 1:
        #             # 反向如果命中就错，并且终止循环
        #             s_print = "[反向error], 条件：" + str(l_2_value) + "，不满足：" + str(v[0])
        #             Color_PO.outColor([{"31": s_print}])
        #             Log_PO.logger.info(s_print)
        #             # varTestcase = varTestcase + 1
        #             # Color_PO.outColor([{"33": d_tmp}])
        #
        #             # print("步骤1 => ", d_tmp["i"])
        #             # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['i'])
        #             # Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
        #             # Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
        #             varTestcase = varTestcase + 1
        #         else:
        #             s_print = "[反向ok], 条件：" + str(l_2_value) + "，不满足：" + str(v[0])
        #             Color_PO.outColor([{"34": s_print}])
        #             Log_PO.logger.info(s_print)
        #             varTestcase = varTestcase + 1
        #
        #         # 回写数据库f_resut, f_updateDate
        #     if varCount == 2:
        #         s_print = "ID = " + str(id) + ", 结果：ok"
        #         Color_PO.outColor([{"32": s_print}])
        #         Log_PO.logger.info([{"32": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))
        #     else:
        #         s_print = "ID = " + str(id) + ", 结果：error"
        #         Color_PO.outColor([{"31": s_print}])
        #         Log_PO.logger.info([{"31": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableER, varTestcase, id))




    def checkRule2(self, d_cases, id, f_evaluationRuleCoding, varTable):
        # 不嵌套判断，2个字段（BMI和年龄）
        # 更新测试记录，确保满足
        Sqlserver_PO_CHC5G.execute("update %s set BMI = %s and '年龄' = %s where id = %s" % (varTable, d_cases['satisfied'][0]['BMI'], d_cases['satisfied'][0]['年龄'], id))   # 修改测试记录的BMI和年龄值

        # 跑接口

        # 查询是否命中 f_evaluationRuleCoding
        f_evaluationRuleCoding_actual = Sqlserver_PO_CHC5G.select("select f_evaluationRuleCoding from %s where id = %s" % (varTable, id))
        if f_evaluationRuleCoding == f_evaluationRuleCoding_actual:
            # 回写数据库f_resut, f_updateDate
            print("ok")
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
        else:
            print("error")
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))
    def checkRule3(self, d_cases, id, f_evaluationRuleCoding, varTable):
        # 嵌套判断，3个字段（BMI，年龄，性别）
        # 更新测试记录，满足条件
        # d_cases = {'BMI': 41.0, '年龄': 14.4, '性别': '男'}
        # Sqlserver_PO_CHC5G.execute("update %s set BMI = %s and '年龄' = %s and '性别' = %s where id = %s" % (varTable, d_cases['BMI'], d_cases['年龄'], d_cases['性别'], id))   # 修改测试记录的BMI、年龄及性别值

        # 跑接口

        # 查询是否输出评估规则编码，输出则命中，查询是否命中 f_evaluationRuleCoding
        # f_evaluationRuleCoding_actual = Sqlserver_PO_CHC5G.select("select f_evaluationRuleCoding from %s where id = %s" % (varTable, id))
        # if f_evaluationRuleCoding == f_evaluationRuleCoding_actual:
        #     return 1
        # else:
        #     return 0

        return 1
    def checkRule4(self, d_cases, id, f_evaluationRuleCoding, varTable):
        # 嵌套判断，3个字段（BMI，年龄，性别）
        # 更新测试记录，不满足条件
        # d_cases = {'BMI': 41.0, '年龄': 14.4, '性别': '男'}
        # Sqlserver_PO_CHC5G.execute("update %s set BMI = %s and '年龄' = %s and '性别' = %s where id = %s" % (varTable, d_cases['BMI'], d_cases['年龄'], d_cases['性别'], id))   # 修改测试记录的BMI、年龄及性别值

        # 跑接口

        # 查询是否输出评估规则编码，输出则命中，查询是否命中 f_evaluationRuleCoding
        # f_evaluationRuleCoding_actual = Sqlserver_PO_CHC5G.select("select f_evaluationRuleCoding from %s where id = %s" % (varTable, id))
        # if f_evaluationRuleCoding == f_evaluationRuleCoding_actual:
        #     return 1
        # else:
        #     return 2
        return 2
