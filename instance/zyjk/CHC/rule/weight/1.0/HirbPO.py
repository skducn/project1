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


class HirbPO():

    def __init__(self):
        self.tableEF = Configparser_PO.DB("tableEF")
        self.tableHI = Configparser_PO.DB("tableHI")

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

    def excel2db_HIRB(self):

        # excel文件导入db

        varTable = varSheet = "a_weight10_HIRB"

        # 1, db中删除已有的表
        Sqlserver_PO_CHC5G.execute("drop table if exists " + varTable)

        # 2, excel导入db
        Sqlserver_PO_CHC5G.xlsx2db(Configparser_PO.FILE("case"), varTable, varSheet)

        #  -- 修改表字符集
        # Sqlserver_PO_CHC5G.execute("ALTER TABLE %s CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" % (varTable))
                            # ALTER TABLE youCONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        #

        # 3, 设置表注释
        Sqlserver_PO_CHC5G.setTableComment(varTable, '体重管理1.0_健康干预规则库（其他分类)_自动化')

        # 4， 替换换行符为空格
        Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_conditions = REPLACE(REPLACE(f_conditions, CHAR(10), ' '), CHAR(13), ' ');" % (varTable))

        # # 5, 设置字段类型与描述
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_result', 'varchar(50)', '结果', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_updateDate', 'varchar(50)', '更新日期', "utf-8")
        Sqlserver_PO_CHC5G.execute("ALTER TABLE %s ALTER COLUMN f_updateDate DATE;" % (varTable))
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_type', 'varchar(50)', '分类', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_code', 'varchar(50)', '干预规则编码', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_conditions', 'varchar(8000)', '干预规则', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_detail', 'varchar(8000)', '干预规则描述', "utf-8")

        # 6, 设置自增主键（最后）
        Sqlserver_PO_CHC5G.setIdentityPrimaryKey(varTable, "ID")



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
    def EFRB_case_or(self, Numerator, d_param, d_cases):

        varTestcase = 0
        # count = self.EFRB_case_or(lln + 1, d_tmp, d_cases)
        # Denominator
        # print(d_param)
        # sys.exit(0)

        if len(d_cases['satisfied']) == 1:
            # 一条数据，正向用例
            l_count = []
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], d_param)
            if d_tmp['result'] == 1:
                s_print = str(Numerator) + "/" + str(d_param['f_conditions_total']) + ", {'正向': 'ok', '条件':" + str(d_param['f_conditions']) + ", '测试数据': " + str(d_cases['satisfied'][0]) + "}"
                Color_PO.outColor([{"34": s_print}])
                Log_PO.logger.info(s_print)
                l_count.append(1)
            else:
                s_print = "{'正向': 'error', '条件': " + str(d_param['f_conditions']) + ", '测试数据':" + str(d_cases['satisfied'][0]) + "}"
                Color_PO.outColor([{"31": s_print}])
                Log_PO.logger.info(s_print)
                Color_PO.outColor([{"33": d_param}])
                Log_PO.logger.info(d_param)
                l_count.append(0)
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
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], d_param)

                if d_tmp['result'] == 1:
                    s_print = str(Numerator) + "(" + str(i + 1) + ")/" + str(d_param['f_conditions_total']) + ", {'正向': 'ok', '条件': " + str(d_param['f_conditions']) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    Color_PO.outColor([{"34": s_print}])
                    # Log_PO.logger.info(s_print)
                    varTestcase = varTestcase + 1
                    l_count.append(1)
                else:
                    # s = "要求 => {'ID': " + str(id) + ", '正向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    # Color_PO.outColor([{"31": s}])
                    # Log_PO.logger.info(s)
                    d_1['表'] = 'a_weight10_EFRB'
                    d_1['ID'] = d_param['ID']
                    d_1['正向'] = 'error'
                    d_1['条件'] = d_param['f_conditions']
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1.update(d_param)
                    s_tmp= str(d_1)
                    s_tmp = s_tmp.replace("\\\\","\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    Log_PO.logger.info("---------------------------------------------------------------------")
                    varTestcase = varTestcase + 1
                    l_count.append(0)

            if 0 in l_count:
                s = "{'ID': " + str(id) + ", '合计数': " + str(l_count) + "}"
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                return varTestcase, 0
            else:
                return varTestcase, 1



    # 评估因素规则库 Evaluation Factor Rule Base
    def EFRB_1(self, d_param_EFRB):

        # EFRB(self, varTestID, varPN="p")
        # 评估因素规则库 Evaluation Factor Rule Base
        # a_weight10_EFRB
        # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
        # varPN = p 执行正向（默认值p），n 执行反向；
        # print(236, d_param_EFRB)  # {'disease': '脑卒中', 'categoryCode': 100, 'ID': 7}


        d_tmp = {}

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select f_conditions, f_code from %s where ID =%s" % (self.tableEF, d_param_EFRB['ID']))
        # print("1299l_d_row => ", l_d_row)
        # print(l_d_row[0]['f_conditions'])
        f_conditions = (l_d_row[0]['f_conditions'])
        # f_code = (l_d_row[0]['f_code'])
        d_tmp['表'] = self.tableEF
        # d_tmp['表注释'] = '评估因素规则库EFRB'
        d_tmp['f_code'] = l_d_row[0]['f_code']
        d_tmp['ID'] = d_param_EFRB['ID']
        d_tmp['所有条件'] = l_d_row[0]['f_conditions']

        d_tmp.update(d_param_EFRB)

        # 统计所有组合的数量
        varTestCount = f_conditions.count("or")
        # print(varTestCount)  # 输出or的数量: 2
        d_tmp['f_conditions_total'] = varTestCount + 1

        # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
        f_conditions = f_conditions.replace("月", '')
        f_conditions = f_conditions.replace('＞', '>').replace('＜', '<').replace('＝', '=')


        # todo EFRB_case for 只有年龄
        if "and" not in f_conditions and "年龄" in f_conditions:
            # 转换成列表
            l_ER = f_conditions.split("and")
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
            print("测试数据 =>", d_cases)

            # 测试数据
            # todo EFRB for and
            count = self.EFRB_case_1(d_cases, l_ER, d_tmp)
            # print("358count", count)
            return count


        # todo EFRB_case for 人群分类
        elif "and" not in f_conditions and "年龄" not in f_conditions:

            print("测试评估因素规则库 =>", d_tmp)
            self.EFRB_run_crowd_1(d_param_EFRB)


        # todo EFRB (14<= 年龄＜14.5 and 22.3<= BMI and 性别=男) or (14.5<= 年龄＜15 and 22.6<= BMI and 性别=男)
        elif "or" in f_conditions:
            # 转换列表，结构化原始数据为列表，生成l_l_N
            l_value = f_conditions.split("or")
            l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
            l_value = [i.split("and") for i in l_value]
            l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
            # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...

            l_result = []
            sum = 0
            print("测试评估因素规则库 =>", d_tmp)
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
                # print(419)
                # count = self.EFRB_case_or_1(d_cases, l_2_value, lln+1, varTestCount+1, d_tmp)
                # print(l_2_value)
                # print(lln+1)
                # print(varTestCount+1)
                # print(d_tmp)
                # sys.exit(0)
                d_tmp['f_conditions'] = l_2_value
                count = self.EFRB_case_or(lln+1, d_tmp, d_cases)
                # count = self.EFRB_case_or(d_cases, d_param_EFRB['ID'], l_2_value, lln+1, varTestCount+1, d_tmp)
                # print(382, count)
                # return count
                # varTestcase, varCount = self.EFRB_case_or(d_cases, id, l_2_value, lln+1, varTestCount+1)


        # todo EFRB BMI>=24 and 年龄>=18 and 年龄<65
        elif "and" in f_conditions:
            # print(432)
            # 转换成列表
            l_ER = f_conditions.split("and")
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
            # print(396, l_ER)
            # d_tmp['f_conditions'] = l_ER
            self.EFRB_case_1(d_cases, d_tmp)

            # print("459:", count)
            # return count

        # todo EFRB 无条件组合
        elif "and" not in f_conditions:

            l_2_value = []
            # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
            l_simple_conditions = Bmi_PO.splitMode(f_conditions)
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
        # a_weight10_EFRB
        # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
        # varPN = p 执行正向（默认值p），n 执行反向；

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_conditions, f_code from %s" % (self.tableEF))
        # print("l_d_row => ", l_d_row)
        if varTestID > len(l_d_row):
            print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
            sys.exit(0)

        for i in enumerate(l_d_row):
            i = varTestID - 1
            id = l_d_row[i]['ID']
            f_conditions = l_d_row[i]['f_conditions']

            # 获取原始数据
            print("评估因素规则库EFRB => {表: " + self.tableEF + ", ID: " + str(id) )
            # print("评估因素规则库EFRB => {表: " + self.tableEF + ", ID: " + str(id) + ", 条件: " + str(f_conditions) + "}")
            Log_PO.logger.info("评估因素规则库EFRB => {'表': '" + self.tableEF + "', 'ID': " + str(id) + "}")

            # 统计所有组合的数量
            varTestCount = f_conditions.count("or")
            # print(varTestCount)  # 输出or的数量: 2

            # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
            f_conditions = f_conditions.replace("月", '')
            f_conditions = f_conditions.replace('＞', '>').replace('＜', '<').replace('＝', '=')

            # todo EFRB_case for 高血压&糖尿病
            if f_conditions == "高血压" or f_conditions == "糖尿病":
                # 判断输出结果
                self.EFRB_run_disease(f_conditions, id)
                # if varPN == "n":
                #     self.EFRB_run_disease_n("脑卒中", id)
                # else:
                #     self.EFRB_run_disease(f_conditions, id)

            # todo EFRB_case for 人群分类
            elif f_conditions.isdigit() == True:
                # 判断输出结果
                self.EFRB_run_crowd(f_conditions, id)

            # todo EFRB_case for 只有年龄
            elif "and" not in f_conditions and "BMI" not in f_conditions:
                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                l_simple_conditions = Age_PO.splitMode(f_conditions)
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
            elif "or" in f_conditions:
                # 转换列表，结构化原始数据为列表，生成l_l_N
                l_value = f_conditions.split("or")
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
                    print(573)
                    l_result.append(varCount)
                    sum = sum + varTestcase

                # print(l_result)

                # 回写数据库f_resut, f_updateDate
                if 0 not in l_result:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => ok"}])
                    Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                        self.tableEF, sum, id))

                else:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                        self.tableEF, sum, id))

            # todo EFRB 简单条件组合
            elif "and" in f_conditions:

                # 转换成列表
                l_ER = f_conditions.split("and")
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
            elif "and" not in f_conditions:

                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                l_simple_conditions = Bmi_PO.splitMode(f_conditions)
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
    def EFRB_case_1(self, d_cases, d_param):

        # d_case : 测试数据
        # L_2_value： 条件
        # d_param：接口的参数

        varTestcase = 0
        # print(645)

        # 一条数据，正向用例
        l_count = []
        # todo EFRB_run_p_1
        d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], d_param)
        d_1 = {}
        if d_tmp['result'] == 1:
            d_1['正向'] = "ok"
            # d_1['条件'] = l_2_value
            d_1['测试数据'] = d_cases['satisfied'][0]
            d_param.update(d_1)
            print("测试评估因素规则库 =>", d_param)
            # Color_PO.outColor([{"34": d_param}])
            Log_PO.logger.info(d_param)
            return 1
        else:
            d_1['正向'] = "error"
            d_1['条件'] = d_param['f_conditions']
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
                Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableEF, varTestcase, ID))
            else:
                d_result['ID'] = ID
                d_result['result'] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableEF, varTestcase, ID))

        #         # 反向用例, 不满足条件的v[0]，预期不命中。
        #         del d_cases['satisfied']
        #         varCount = 2
        #         for k, v in d_cases.items():
        #             # print(v[0])
        #             # todo EFRB_run_n
        #             varCount = self.EFRB_run_n(v[0], id, self.tableEF)
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
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        #     else:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
        #         Log_PO.logger.info([{"31": "error, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        # else:
        #     for i in range(len(d_cases['satisfied'])):
        #         # print(d_cases)
        #         # todo EFRB_run_p_n
        #         result = self.EFRB_run_p(d_cases['satisfied'][i], id, self.tableEF)
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
        #         varCount = self.EFRB_run_n(v[0], id, self.tableEF)
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
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        #     else:
        #         s_print = "ID = " + str(id) + ", 结果：error"
        #         Color_PO.outColor([{"31": s_print}])
        #         Log_PO.logger.info([{"31": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
    def EFRB_run_disease(self, varDisease, ID):

        # 既往疾病
        # varDisease = 高血压
        # id = 46

        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_code from %s where ID= %s" % (self.tableEF, ID))
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']

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
            d_tmp['预期值'] = l_d_row[0]['f_code']
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
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result['result'], d_result['ID']))
            else:
                d_result['ID'] = ID
                d_result['result'] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result['result'],d_result['ID']))
        else:
            print("1750, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_disease_n(self, varDisease, ID):

        # 既往疾病(执行反向用例)
        # varDisease = 脑卒中
        # id = 46

        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_code from %s where ID= %s" % (self.tableEF, ID))
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']

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
            d_tmp['预期值'] = l_d_row[0]['f_code']
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
            #     Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, ID))
            # else:
            #     Color_PO.outColor([{"32": "[ID: " + str(ID) + "] => error"}])
            #     Log_PO.logger.info([{"31": "error, id=" + str(ID)}])
            #     Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, ID))
        else:
            print("1750, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_crowd(self, varCatatoryId, ID):

        # 人群分类
        # varDisease = 高血压
        # id = 46

        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_code from %s where ID= %s" % (self.tableEF, ID))
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']

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
            d_tmp['预期值'] = l_d_row[0]['f_code']
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
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result["result"], d_result["ID"]))
            else:
                d_result["ID"] = ID
                d_result["result"] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result["result"], d_result["ID"]))
        else:
            print("175110, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_crowd_1(self, d_param):

        # 人群分类
        # varDisease = 高血压
        # id = 46
        # print("1183", d_param)  # {'categoryCode': 6, 'disease': '脑卒中', 'ID': 52}
        if "sex" in d_param:
            if d_param['sex'] == "男":
                varSexCode = "1"
            elif d_param['sex'] == "女":
                varSexCode = "2"
        else:
            varSexCode = "1"

        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_categoryCode, f_conditions, f_code from %s where ID= %s" % (self.tableEF, d_param['ID']))
        # print(1196, l_d_row)
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']
        categoryCode = l_d_row[0]['f_categoryCode']

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
            d_tmp['预期值'] = l_d_row[0]['f_code']
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
            d_result["ID"] = d_param['ID']
            if 0 not in l_count:
                d_result["result"] = "ok"
                Color_PO.outColor([{"32": d_result}])
                Log_PO.logger.info(d_result)
            else:
                d_result["result"] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result["result"], d_result["ID"]))
        else:
            print("2333, error ", d_r['code'])
            sys.exit(0)
    def _EFRB_run(self, d_cases_satisfied, d_param):

        # 公共测试用例

        # d_cases_satisfied = {'BMI': 16.8}
        # id = 1
        # d_param = {'categoryCode': 1, 'disease': '脑卒中'}

        # print(d_cases_satisfied)
        # print(ID)
        # print(d_param)
        # sys.exit(0)

        d_tmp = {}
        # print("1332", ID)
        # 参数
        # 获取f_code,f_age
        l_d_row = Sqlserver_PO_CHC5G.select("select f_category, f_categoryCode, f_ageType, f_code from %s where ID= %s" % (self.tableEF, d_param['ID']))
        # print(l_d_row)  # [{'f_category': '学生', 'f_categoryCode': '2', 'f_ageType': 'float', 'f_code': 'TZ_STZB007'}]
        d_tmp['人群分类'] = l_d_row[0]['f_category']
        d_tmp['人群分类编码'] = l_d_row[0]['f_categoryCode']
        d_tmp['年龄类型'] = l_d_row[0]['f_ageType']
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']
        # d_tmp['条件'] = l_d_row[0]['f_conditions']

        if d_param == {}:
            d_param = {'categoryCode': d_tmp['人群分类编码'], 'disease': '脑卒中'}


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
            d_tmp['预期值'] = l_d_row[0]['f_code']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql

            return d_tmp

        else:
            print("4218, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_p(self, d_cases_satisfied, d_param):

        d_tmp = self._EFRB_run(d_cases_satisfied, d_param)
        # if d_tmp['实际值'] == d_tmp['预期值']:
        if d_tmp['预期值'] in d_tmp['实际值']:
            d_tmp['result'] = 1
        else:
            d_tmp['result'] = 0
        return d_tmp


    def str2dict(self, f_conditions):
        # 字符串转字典，将 （TZ_STZB042 = '是' and TZ_JWJB001 = '否' ） 转为字典{'TZ_STZB042': '是', 'TZ_JWJB001': '否'}
        pairs = [pair.strip() for pair in f_conditions.split('and')]
        d_conditions = {}
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=')
                d_conditions[key.strip()] = value.strip().replace("'", "")
        # print(d_conditions) # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        return d_conditions



    # todo 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)
    def HIRB(self, varTestID="all"):

        # 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)
        # a_weight10_HIRB

        d_param = {}
        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_code, f_conditions from %s" % (self.tableHI))
        # print("l_d_row => ", l_d_row)  # [{'ID': 1, 'f_code': 'TZ_YS001', 'f_conditions': "TZ_RQFL001='是' and TZ_STZB001='是' and TZ_JWJB001='否' and TZ_JWJB002='否'"},...
        # sys.exit(0)
        if varTestID > len(l_d_row):
            print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
            sys.exit(0)

        for i in enumerate(l_d_row):
            i = varTestID - 1
            ID = l_d_row[i]['ID']
            f_code = l_d_row[i]['f_code']
            f_conditions = l_d_row[i]['f_conditions']

            # 测试项
            d_param['表'] = self.tableHI
            d_param['ID'] = ID
            d_conditions = self.str2dict(f_conditions)
            d_param['f_conditions'] = d_conditions
            d_param['f_code'] = f_code
            s = "测试健康干预规则库 => " + str(d_param)
            print(s)
            Log_PO.logger.info(s)

            # todo TZ_STZB043='是' or TZ_STZB044='是' or TZ_STZB045='是'
            if "or" in f_conditions and "and" not in f_conditions:
                 
                l_value = f_conditions.split("or")
                # print(l_value)
                l_4 = []
                for i in l_value:
                    l_4.append(self.str2dict(i))
                # l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
                # l_value = [i.split("and") for i in l_value]
                # l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
                # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
                print(l_4)
                # sys.exit(0)
                # d_conditions = self.str2dict(f_conditions)
                self.HIRB_case_or(ID, f_code, l_4)


            # todo HIRB  (TZ_STZB002='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否') or (TZ_STZB005='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否')
            if "or" in f_conditions and "and" in f_conditions:
                

                # # 字符串转字典，{'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
                # pairs = [pair.strip() for pair in f_conditions.split('and')]
                # d_conditions = {}
                # for pair in pairs:
                #     if '=' in pair:
                #         key, value = pair.split('=')
                #         d_conditions[key.strip()] = value.strip().replace("'", "")
                # print(d_conditions) # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}

                # 转换列表，结构化原始数据为列表，生成l_l_N
                l_value = f_conditions.split("or")
                # print(l_value)
                l_4 = []
                for i in l_value:
                    i = i.replace("(",'').replace(")",'')
                    l_4.append(self.str2dict(i))
                # l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
                # l_value = [i.split("and") for i in l_value]
                # l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
                # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
                print(l_4)
                # sys.exit(0)
                # d_conditions = self.str2dict(f_conditions)
                self.HIRB_case_or(ID, f_code, l_4)
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
                    # self.HIRB_case(ID, f_code, d_conditions)
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
                            self.tableEF, sum, id))

                else:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                            self.tableEF, sum, id))


            # todo HIRB "TZ_RQFL001='是' and TZ_STZB001='是' and TZ_JB001='否' and TZ_JB002='否'"
            elif "and" in f_conditions:
                # 测试数据
                # print(1570, "HIRB_case")
                self.HIRB_case(d_param)


            # todo HIRB TZ_RQFL005='是'
            elif "and" not in f_conditions:
                self.HIRB_case(d_param)


            else:
                print("[not or & and ]")
            print("-".center(100, "-"))

            break
    def HIRB_case(self, d_param):

        # 执行ER中规则
        # print(ID)  # 7
        # print(f_code)  # TZ_YS001
        # print("d_conditions", d_conditions)  # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        # sys.exit(0)

        d_tmp = {}

        # 生成EFRB参数 d_param_EFRB
        d_param_EFRB = {}
        # 过滤评估因素规则（过滤掉TZ_STZB开头的key）
        d_filtered = {key: value for key, value in d_param['f_conditions'].items() if 'TZ_STZB' not in key}
        # print("过滤掉TZ_STZB开头的key：", d_filtered) # {'TZ_RQFL001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}

        # 先遍历否
        # 定义遍历顺序
        order = ['否', '是']

        # 按照定义的顺序遍历字典（写死了TZ_JB001、TZ_JB002）？？
        for value in order:
            for key, val in d_filtered.items():
                if val == value:
                    # print(f"键: {key}, 值: {val}")
                    l_ = Sqlserver_PO_CHC5G.select("select f_categoryCode, f_conditions from a_weight10_EFRB where f_code='%s'" % (key))
                    # print(l_) # [{'f_conditions': '3'}]
                    if val == "否" and "TZ_RQFL" in key:
                        d_param_EFRB['categoryCode'] = 100
                    if key == 'TZ_JB001' and val == "否":
                        d_param_EFRB['disease'] = "脑卒中"
                    if key == 'TZ_JB002' and val == "否":
                        d_param_EFRB['disease'] = "脑卒中"
                    if val == "是" and "TZ_RQFL" in key:
                        d_param_EFRB['categoryCode'] = int(l_[0]['f_categoryCode'])
                    if key == 'TZ_JB001' and val == "是":
                        d_param_EFRB['disease'] = l_[0]['f_conditions']
                    if key == 'TZ_JB002' and val == "是":
                        d_param_EFRB['disease'] = l_[0]['f_conditions']

        if "categoryCode" not in d_param_EFRB:
            d_param_EFRB['categoryCode'] = 100
        if "disease" not in d_param_EFRB:
            d_param_EFRB['disease'] = "脑卒中"

        # 获取 TZ_STZB开头的key
        l_matching_keys = [key for key in d_param['f_conditions'] if 'TZ_STZB' in key]
        # print(l_matching_keys) # ['TZ_STZB001']
        if l_matching_keys != []:
            l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[0]))
            # print(l_1) # [{'ID': '3'}]
            # d_param['ID']
            if len(l_matching_keys) == 1:
                # print(l_1[0]['ID'], d_param)
                # print(1714, l_1[0]['ID'])
                # print(1671)
                d_param_EFRB['ID'] = l_1[0]['ID']
                self.EFRB_1(d_param_EFRB)
            else:
                print("warning, 匹配到多个值：", l_matching_keys)
                sys.exit(0)

        else:
            # 匹配人群分类
            l_matching_keys = [key for key in d_param['f_conditions'] if 'TZ_RQFL' in key]
            if l_matching_keys != []:
                l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[0]))
                if len(l_matching_keys) == 1:
                    # print(l_1[0]['ID'], d_param)
                    # self.EFRB_1(l_1[0]['ID'], d_4)
                    d_param_EFRB['ID'] = l_1[0]['ID']
                    self.EFRB_1(d_param_EFRB)
                else:
                    print("warning, 匹配到多个值：", l_matching_keys)
                    sys.exit(0)

            # 匹配年龄
            l_matching_keys = [key for key in d_param['f_conditions'] if 'TZ_AGE' in key]
            # print(l_matching_keys)  # ['TZ_STZB001']
            if l_matching_keys != []:
                l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[0]))
                if len(l_matching_keys) == 1:
                    # print(l_1[0]['ID'], d_param)
                    # self.EFRB_1(l_1[0]['ID'], d_4)
                    d_param_EFRB['ID'] = l_1[0]['ID']
                    self.EFRB_1(d_param_EFRB)
                else:
                    print("warning, 匹配到多个值：", l_matching_keys)
                    sys.exit(0)

        # 检查是否命中f_code
        sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
        l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)

        l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
        # print(l_d_RULE_CODE_actual) # ['TZ_STZB001', 'TZ_RQFL001', 'TZ_SRL001', 'TZ_MBTZ002', 'TZ_YD001', 'TZ_YS001']

        d_tmp['实际值'] = l_d_RULE_CODE_actual
        d_tmp['预期值'] = d_param['f_code']
        d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
        l_count = []
        d_result = {}
        # print(d_tmp)
        d_1 = {}
        if d_tmp['预期值'] in d_tmp['实际值']:
            # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
            # Color_PO.outColor([{"34": d_tmp}])
            # Log_PO.logger.info(d_tmp)
            d_1['表'] = "a_weight10_HIRB"
            d_1['表注释'] = "健康干预规则库（其他分类）HIRB"
            d_1['ID'] = d_param['ID']
            d_1['result'] = "ok"
            d_1.update(d_tmp)
            Color_PO.outColor([{"32": "结果 => " + str(d_1)}])
            Log_PO.logger.info(d_1)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableHI, d_param['ID']))
        else:
            print("预期值:", d_tmp['预期值'] )
            print("实际值:", d_tmp['实际值'])
            Color_PO.outColor([{"32": "[ID: " + str(d_param['ID']) + "] => error"}])
            Log_PO.logger.info([{"31": "error, id=" + str(d_param['ID'])}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableHI, d_param['ID']))





        sys.exit(0)

        # 检查是否命中f_code
        sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
        l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
        l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
        d_tmp['f_code'] = f_code
        d_tmp['实际值'] = l_d_RULE_CODE_actual
        d_tmp['预期值'] = f_code
        d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
        l_count = []
        if d_tmp['预期值'] in l_d_RULE_CODE_actual:
            # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
            Color_PO.outColor([{"34": d_tmp}])
            Log_PO.logger.info(d_tmp)

            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => ok"}])
            Log_PO.logger.info([{"32": "ok, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableHI, id))

        else:
            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => error"}])
            Log_PO.logger.info([{"31": "error, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableHI, id))

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
                    self.tableEF, varTestcase, ID))
            else:
                s_print = "[ID: " + str(ID) + "] => ERROR"
                Color_PO.outColor([{"31": s_print}])
                Log_PO.logger.info(s_print)
                Sqlserver_PO_CHC5G.execute(
                    "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                    self.tableEF, varTestcase, ID))

        #         # 反向用例, 不满足条件的v[0]，预期不命中。
        #         del d_cases['satisfied']
        #         varCount = 2
        #         for k, v in d_cases.items():
        #             # print(v[0])
        #             # todo EFRB_run_n
        #             varCount = self.EFRB_run_n(v[0], id, self.tableEF)
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
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        #     else:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
        #         Log_PO.logger.info([{"31": "error, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        # else:
        #     for i in range(len(d_cases['satisfied'])):
        #         # print(d_cases)
        #         # todo EFRB_run_p_n
        #         result = self.EFRB_run_p(d_cases['satisfied'][i], id, self.tableEF)
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
        #         varCount = self.EFRB_run_n(v[0], id, self.tableEF)
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
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        #     else:
        #         s_print = "ID = " + str(id) + ", 结果：error"
        #         Color_PO.outColor([{"31": s_print}])
        #         Log_PO.logger.info([{"31": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
    def HIRB_case_or(self, ID, f_code, l_4):

        # 执行ER中规则
        # print("f_code", f_code)  # TZ_YS001
        # print("d_conditions", d_conditions)  # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        # sys.exit(0)

        d_tmp = {}

        # 遍历a_weight10_EFRB
        l_f_code = Sqlserver_PO_CHC5G.select("select ID, f_code from a_weight10_EFRB")
        # print(l_f_code)
        d_f_code = {item['ID']: item['f_code'] for item in l_f_code}
        # print(d_f_code)  # {1: 'TZ_STZB001', 2: 'TZ_STZB002', ...
        d_f_code = {v: k for k, v in d_f_code.items()}
        # print(d_f_code)  # {'TZ_STZB001': 1, 'TZ_STZB002': 2,

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
                        l_ = Sqlserver_PO_CHC5G.select("select f_conditions from a_weight10_EFRB where f_code='%s'" % (key))
                        # print(l_) # [{'f_conditions': '3'}]
                        if val == "否" and "TZ_RQFL" in key:
                            d_param['categoryCode'] = 100
                        if key == 'TZ_JWJB001' and val == "否":
                            d_param['disease'] = "脑卒中"
                        if key == 'TZ_JWJB002' and val == "否":
                            d_param['disease'] = "脑卒中"
                        if val == "是" and "TZ_RQFL" in key:
                            d_param['categoryCode'] = int(l_[0]['f_conditions'])
                        if key == 'TZ_JWJB001' and val == "是":
                            d_param['disease'] = l_[0]['f_conditions']
                        if key == 'TZ_JWJB002' and val == "是":
                            d_param['disease'] = l_[0]['f_conditions']
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
                l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[0]))
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
                    "select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[0]))
                if len(l_matching_keys) == 1:
                    # print(l_1[0]['ID'], d_param)
                    count = self.EFRB_1(l_1[0]['ID'], d_param)
                else:
                    print("warning, 匹配到多个值：", l_matching_keys)
                    sys.exit(0)

            # 检查是否命中f_code
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)

            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
            # print(l_d_RULE_CODE_actual) # ['TZ_STZB001', 'TZ_RQFL001', 'TZ_SRL001', 'TZ_MBTZ002', 'TZ_YD001', 'TZ_YS001']

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = f_code
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            l_count = []
            d_result = {}

            if d_tmp['预期值']  in l_d_RULE_CODE_actual:
                # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
                Color_PO.outColor([{"34": d_tmp}])
                Log_PO.logger.info(d_tmp)
                d_result['result'] = "ok"
                d_result['ID'] = ID
                Color_PO.outColor([{"32": d_result}])
                Log_PO.logger.info(d_result)
                sum = sum + 1
            else:
                d_result['result'] = "error"
                d_result['ID'] = ID
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                s_tmp = str(d_tmp)
                s_tmp = s_tmp.replace("\\\\","\\")
                Color_PO.outColor([{"31": s_tmp}])
                sum = sum + 0


        if sum == len(l_4):

            Sqlserver_PO_CHC5G.execute(
                "update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableHI, ID))
        else:

            Sqlserver_PO_CHC5G.execute(
                "update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableHI, ID))

        sys.exit(0)

        # 检查是否命中f_code
        sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
        l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
        l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
        d_tmp['f_code'] = f_code
        d_tmp['实际值'] = l_d_RULE_CODE_actual
        d_tmp['预期值'] = f_code
        d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
        l_count = []
        if d_tmp['预期值'] in l_d_RULE_CODE_actual:
            # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
            Color_PO.outColor([{"34": d_tmp}])
            Log_PO.logger.info(d_tmp)

            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => ok"}])
            Log_PO.logger.info([{"32": "ok, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableHI, id))

        else:
            Color_PO.outColor([{"32": "[ID: " + str(id) + "] => error"}])
            Log_PO.logger.info([{"31": "error, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableHI, id))

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
                    self.tableEF, varTestcase, ID))
            else:
                s_print = "[ID: " + str(ID) + "] => ERROR"
                Color_PO.outColor([{"31": s_print}])
                Log_PO.logger.info(s_print)
                Sqlserver_PO_CHC5G.execute(
                    "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                    self.tableEF, varTestcase, ID))

        #         # 反向用例, 不满足条件的v[0]，预期不命中。
        #         del d_cases['satisfied']
        #         varCount = 2
        #         for k, v in d_cases.items():
        #             # print(v[0])
        #             # todo EFRB_run_n
        #             varCount = self.EFRB_run_n(v[0], id, self.tableEF)
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
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        #     else:
        #         Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
        #         Log_PO.logger.info([{"31": "error, id=" + str(id)}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        # else:
        #     for i in range(len(d_cases['satisfied'])):
        #         # print(d_cases)
        #         # todo EFRB_run_p_n
        #         result = self.EFRB_run_p(d_cases['satisfied'][i], id, self.tableEF)
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
        #         varCount = self.EFRB_run_n(v[0], id, self.tableEF)
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
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))
        #     else:
        #         s_print = "ID = " + str(id) + ", 结果：error"
        #         Color_PO.outColor([{"31": s_print}])
        #         Log_PO.logger.info([{"31": s_print}])
        #         Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where id = %s" % (self.tableEF, varTestcase, id))


