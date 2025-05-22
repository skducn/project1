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


class DrwsPO():

    def __init__(self):
        self.tableWS = Configparser_PO.DB("tableWS")

    def convert_conditions(self, conditions):

        # 将列表转换字符串
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

    def excel2db_DRWS(self):

        # excel文件导入db
        # Configparser_PO.FILE("case"), "WEIGHT_STATUS", "a_weight10_WS"
        varTable = varSheet = "a_weight10_DRWS"

        # 1, db中删除已有的表
        Sqlserver_PO_CHC5G.execute("drop table if exists " + varTable)

        # 2, excel导入db
        Sqlserver_PO_CHC5G.xlsx2db(Configparser_PO.FILE("case"), varTable, varSheet)

        # 3, 设置表注释
        Sqlserver_PO_CHC5G.setTableComment(varTable, '体重管理1.0_判定居民体重状态_自动化')

        # 4， 替换换行符为空格
        Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_conditions = REPLACE(REPLACE(f_conditions, CHAR(10), ' '), CHAR(13), ' ');" % (varTable))

        # # 5, 设置字段类型与描述
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_result', 'varchar(50)', '测试结果', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_updateDate', 'varchar(50)', '更新日期', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_log', 'varchar(8000)', '日志信息', "utf-8")
        Sqlserver_PO_CHC5G.execute("ALTER TABLE %s ALTER COLUMN f_updateDate DATE;" % (varTable))
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_category', 'varchar(50)', '人群分类', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_categoryCode', 'varchar(50)', '人群分类编码', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_weightStatus', 'varchar(50)', '体重状态', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_weightStatusCode', 'varchar(50)', '体重状态编码', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_conditions', 'varchar(8000)', '取值条件', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_testcase', 'varchar(100)', '测试检查点', "utf-8")
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_caseTotal', 'varchar(10)', '用例数量', "utf-8")

        # 6, 设置自增主键（最后）
        Sqlserver_PO_CHC5G.setIdentityPrimaryKey(varTable, "ID")


    # todo 1 判定居民体重状态 Determine Residents' Weight Status
    def DRWS(self, varTestID="all"):

        # 判定居民体重状态 Determine Residents' Weight Status
        # a_weight10_DRWS

        d_ = {}

        # 获取表每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_conditions from %s" % (self.tableWS))
        # print("l_d_row =>", l_d_row)  # [{'ID': 1, 'f_conditions': 'BMI＜18.5'}, ...

        d_['table'] = self.tableWS
        for i, index in enumerate(l_d_row):
            # print(l_d_row[i], i)
            if varTestID == "all":
                ...
            elif varTestID > len(l_d_row) or varTestID <= 0:
                print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
                sys.exit(0)
            else:
                i = varTestID - 1
            ID = l_d_row[i]['ID']
            f_conditions = l_d_row[i]['f_conditions']
            d_['ID'] = ID
            d_['f_conditions'] = f_conditions

            # 获取原始数据
            print("判定居民体重状态DRWS =>", d_)
            Log_PO.logger.info("判定居民体重状态DRWS =>" + str(d_))

            # 统计所有组合的数量
            varTestCount = f_conditions.count("or")
            # print(varTestCount)  # 输出or的数量: 2

            # 格式化数据，清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
            f_conditions = f_conditions.replace("月", '').replace('＞', '>').replace('＜', '<').replace('＝', '=')

            # todo 2 DRWS 集合（(6<=年龄＜6.5 and 13.4＞BMI and 性别=男) or (6.5<=年龄＜7 and 13.8＞BMI and 性别=男)）
            if "or" in f_conditions:

                # 格式化数据，字符串转列表，生成l_l_N
                l_conditions = f_conditions.split("or")
                l_conditions = [i.replace("(", '').replace(")", '').strip() for i in l_conditions]
                l_conditions = [i.split("and") for i in l_conditions]
                l_l_conditions = [[item.strip() for item in sublist] for sublist in l_conditions]
                # print(l_l_conditions)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
                print("--------------------")

                l_count = []
                sum = 0
                for lln in range(len(l_l_conditions)):
                    # Age、BMI、年龄 - 格式化条件
                    l_conditions = []

                    # 拆分条件，如 '6<=年龄<6.5' 拆分为 或 6<=年龄' and 年龄<6.5'
                    for i in l_l_conditions[lln]:
                        if "BMI" in i:
                            l_split_conditions = BmiAgeSex_PO.splitMode(i)
                            l_conditions.extend(l_split_conditions)
                        if "年龄" in i:
                            l_split_conditions = BmiAgeSex_PO.splitMode(i)
                            l_conditions.extend(l_split_conditions)
                        elif "性别" in i:
                            l_split_conditions = BmiAgeSex_PO.splitMode(i)
                            l_conditions.extend(l_split_conditions)
                    # print("244 拆分条件 =", l_conditions)

                    # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                    l_interconvert_conditions = []
                    for i in l_conditions:
                        l_split_conditions = BmiAgeSex_PO.interconvertMode(i)
                        l_interconvert_conditions.extend(l_split_conditions)

                    # 生成随机数据 d_cases
                    for i in l_interconvert_conditions:
                        if ('>=' or '<=') in i:
                            if '年龄' in i:
                                d_cases = BmiAgeSex_PO.main(l_interconvert_conditions)
                                break
                            if 'BMI' in i:
                                d_cases = BmiAgeSex_PO.main(l_interconvert_conditions)
                                break
                        else:
                            d_cases = BmiAgeSex_PO.main(l_interconvert_conditions)

                    if Configparser_PO.SWITCH("testDataSet") == "on":
                        print("测试数据集合 =>", d_cases)

                    # 判断输出结果
                    # todo DRWS_case_or for 集合
                    # 测试数据
                    Numerator = lln + 1
                    Denominator = varTestCount + 1
                    d_result = self.DRWS_case_or(d_cases, ID, l_conditions, Numerator, Denominator)
                    l_count.append(d_result['count'])
                    sum = sum + d_result['caseTotal']

                # 更新记录
                self._DRWS_result(l_count, sum, ID)

            # # todo 3 DRWS 多个条件（年龄=2月 and 14.2≤BMI＜18.1 and 性别=男）
            # elif "and" in f_conditions:
            #
            #     # 格式化数据，字符串转列表，生成l_conditions
            #     l_conditions = f_conditions.split("and")
            #     l_conditions = [i.strip() for i in l_conditions]
            #     # print("730 实际参数 =>", l_conditions)  # ['18.5<BMI', 'BMI<24.0']
            #
            #     l_2_value = []
            #     # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄' and 年龄<6.5'
            #     for i in l_conditions:
            #         l_simple_conditions = BmiAgeSex_PO.splitMode(i)
            #         l_2_value.extend(l_simple_conditions)
            #     print("737 分解参数 =>", l_2_value)
            #
            #     # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
            #     l_3_value = []
            #     for i in l_2_value:
            #         l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
            #         l_3_value.extend(l_simple_conditions)
            #     print("744 结构化参数 =>", l_3_value)  #  ['BMI>18.5', 'BMI<24.0']
            #
            #     # 读取BMI模块，生成随机数据d_cases
            #     d_cases = BmiAgeSex_PO.main(l_3_value)
            #     # d_cases = BmiAgeSex_PO.generate_all_cases(l_3_value)
            #
            #     # 测试数据
            #     # todo DRWS_case for and
            #     self.DRWS_case(ID, l_conditions, d_cases)

            # todo 4 DRWS 单个条件（BMI＜18.5）
            elif "and" not in f_conditions:
                # BMI - 格式化条件
                l_conditions = []

                # 拆分条件，如 '6<=年龄<6.5' 拆分为 6<=年龄' and 年龄<6.5'
                l_split_conditions = Bmi_PO.splitMode(f_conditions)
                l_conditions.extend(l_split_conditions)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 ['18.5>BMI' 转换 ['BMI<18.5']
                l_interconvert_conditions = []
                for i in l_conditions:
                    l_split_conditions = Bmi_PO.interconvertMode(i)
                    l_interconvert_conditions.extend(l_split_conditions)

                # 生成随机数据 d_cases
                d_cases = Bmi_PO.generate_all_cases(l_interconvert_conditions)

                if Configparser_PO.SWITCH("testDataSet") == "on":
                    print("测试数据集合 =>", d_cases)  # {'satisfied': [{'BMI': 16.8}], 'not1': [{'BMI': 19.6}]}
                Log_PO.logger.info("测试数据集合 => " + str(d_cases))

                # todo 5 DRWS_case for 单个条件
                # 测试数据
                self.DRWS_case(ID, l_conditions, d_cases)

            else:
                print("[not or & and ]")
            print("-".center(100, "-"))

            if varTestID != "all":
                break

    def _DRWS_print_ok(self,pORn, l_conditions, testData, d_tmp):
        l_count = []
        d_1 = {}
        d_1[pORn] = 'ok'
        d_1['条件'] = l_conditions
        # d_1['测试数据'] = d_cases['satisfied'][0]
        d_1['测试数据'] = testData
        Color_PO.outColor([{"34": d_1}])
        d_1.update(d_tmp)
        s_tmp = str(d_1)
        s_tmp = s_tmp.replace("\\\\", "\\")
        Log_PO.logger.info(s_tmp)
        if Configparser_PO.SWITCH("curl_p") == "on":
            Color_PO.outColor([{"34": s_tmp}])
        l_count.append(1)
        return l_count
    def _DRWS_print_error(self,pORn, l_conditions, testData, d_tmp):
        l_count = []
        d_1 = {}
        d_1[pORn] = 'error'
        d_1['条件'] = l_conditions
        d_1['测试数据'] = testData
        d_1.update(d_tmp)
        s_tmp = str(d_1)
        s_tmp = s_tmp.replace("\\\\", "\\")
        Log_PO.logger.info(s_tmp)
        Color_PO.outColor([{"31": s_tmp}])
        l_count.append(0)
        return l_count

    def _DRWS_result(self, count, caseTotal, ID):
        d_result = {}
        if 0 not in count:
            d_result['ID'] = ID
            d_result['result'] = 'ok'
            s = "结果 => " + str(d_result)
            Color_PO.outColor([{"32": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, caseTotal, ID))
        else:
            d_result['ID'] = ID
            d_result['result'] = 'error'
            s = "结果 => " + str(d_result)
            Color_PO.outColor([{"31": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableWS, caseTotal, ID))
        Log_PO.logger.info("---------------------------------------------------------------------")

    def DRWS_case(self, ID, l_conditions, d_cases):

        # ID = 1
        # l_conditions = ['BMI<18.5']
        # d_cases = {'satisfied': [{'BMI': 14.2}], 'not1': [{'BMI': 53.4}]}

        # 测试数据量
        caseTotal = 0

        if len(d_cases['satisfied']) == 1:
            # 正向用例, 一条数据
            # todo DRWS_run_p1
            d_tmp = self.DRWS_run_p(d_cases['satisfied'][0], ID)
            if d_tmp['result'] == 1:
                l_count = self._DRWS_print_ok("正向", l_conditions, d_cases['satisfied'][0], d_tmp)
            else:
                l_count = self._DRWS_print_error("正向", l_conditions, d_cases['satisfied'][0], d_tmp)
            caseTotal = caseTotal + 1

            # 反向用例, 一条数据
            # todo DRWS_run_n1
            if Configparser_PO.SWITCH('testNegative') == "on":
                d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], ID)
                if d_tmp['result'] == 1:
                    l_count = self._DRWS_print_ok("反向", l_conditions, d_cases['notSatisfied'][0], d_tmp)
                else:
                    l_count = self._DRWS_print_error("反向", l_conditions, d_cases['notSatisfied'][0], d_tmp)
                caseTotal = caseTotal + 1
        else:
            # 正向用例, N个数据
            for i in range(len(d_cases['satisfied'])):
                # todo DRWS_run_pn
                d_tmp = self.DRWS_run_p(d_cases['satisfied'][i], ID)
                if d_tmp['result'] == 1:
                    l_count = self._DRWS_print_ok("正向", l_conditions, d_cases['satisfied'][i], d_tmp)
                else:
                    l_count = self._DRWS_print_error("正向", l_conditions, d_cases['satisfied'][i], d_tmp)
                caseTotal = caseTotal + 1

            # 反向用例, N个数据
            if Configparser_PO.SWITCH('testNegative') == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    # todo DRWS_run_nn
                    d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][i], ID)
                    if d_tmp['result'] == 1:
                        l_count = self._DRWS_print_ok("反向", l_conditions, d_cases['satisfied'][i], d_tmp)
                    else:
                        l_count = self._DRWS_print_error("反向", l_conditions, d_cases['satisfied'][i], d_tmp)
                    caseTotal = caseTotal + 1
        # 更新记录
        self._DRWS_result(l_count, caseTotal, ID)
    def DRWS_case_or(self, d_cases, id, l_conditions, Numerator, Denominator):

        # 测试数据量
        caseTotal = 0
        d_result = {}
        if len(d_cases['satisfied']) == 1:
            # 正向用例, 一条数据
            l_count = []
            d_tmp = self.DRWS_run_p(d_cases['satisfied'][0], id)
            d_1 = {}
            if d_tmp['result'] == 1:
                d_1['No.'] = str(Numerator) + "/" + str(Denominator)
                d_1['正向'] = 'ok'
                d_1['条件'] = l_conditions
                d_1['测试数据'] = d_cases['satisfied'][0]
                Color_PO.outColor([{"34": d_1}])
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Log_PO.logger.info(s_tmp)
                if Configparser_PO.SWITCH("curl_p") == "on":
                    Color_PO.outColor([{"34": s_tmp}])
                l_count.append(1)
            else:
                d_1['No.'] = str(Numerator) + "/" + str(Denominator)
                d_1['正向'] = 'error'
                d_1['条件'] = l_conditions
                d_1['测试数据'] = d_cases['satisfied'][0]
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Log_PO.logger.info(s_tmp)
                Color_PO.outColor([{"31": d_tmp}])
                l_count.append(0)

                # 将错误写入数据库log
                f_conditions = (self.convert_conditions(l_conditions))  # # 将列表转换字符串
                d_tmp['条件'] = str(f_conditions)
                d_tmp['测试数据'] = str(d_cases['satisfied'][0])
                d_tmp['用例类型'] = "正向不满足"
                s_tmp = str(d_tmp)
                s_tmp = s_tmp.replace("'", "''")
                s_tmp = s_tmp.replace("\\\\", "\\")
                Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_log = '%s' where ID=%s" % (self.tableWS, s_tmp, d_tmp['ID']))

            caseTotal = caseTotal + 1

            # 反向用例，一条数据
            if Configparser_PO.SWITCH("testNegative") == "on":
                d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], id)
                d_2 = {}
                if d_tmp['result'] == 1:
                    d_2['No.'] = str(Numerator) + "/" + str(Denominator)
                    d_2['反向'] = 'error'
                    d_2['条件'] = l_conditions
                    d_2['测试数据'] = d_cases['notSatisfied'][0]
                    d_2.update(d_tmp)
                    s_tmp = str(d_2)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    l_count.append(0)

                    # 将错误条件写入数据库，以备复测。
                    # 将列表转换字符串
                    f_conditions = (self.convert_conditions(l_conditions))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                    d_tmp['条件'] = str(f_conditions)
                    d_tmp['测试数据'] = str(d_cases['notSatisfied'][0])
                    d_tmp['用例类型'] = "反向满足"
                    s_tmp = str(d_tmp)
                    s_tmp = s_tmp.replace("'", "''")
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    # print(d_tmp)
                    Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_log = '%s' where ID=%s" % (self.tableWS, s_tmp, d_tmp['ID']))
                else:
                    d_2['No.'] = str(Numerator) + "/" + str(Denominator)
                    d_2['反向'] = 'ok'
                    d_2['条件'] = l_conditions
                    d_2['测试数据'] = d_cases['notSatisfied'][0]
                    Color_PO.outColor([{"31": d_2}])
                    d_2.update(d_tmp)
                    s_tmp = str(d_2)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    l_count.append(1)
                caseTotal = caseTotal + 1

        else:
            # 正向用例, N个数据
            l_count = []
            for i in range(len(d_cases['satisfied'])):
                d_tmp = self.DRWS_run_p(d_cases['satisfied'][i], id)
                d_1 = {}
                if d_tmp['result'] == 1:
                    d_1['No.'] = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator)
                    d_1['正向'] = 'ok'
                    d_1['条件'] = l_conditions
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    Color_PO.outColor([{"34": d_1}])
                    d_1.update(d_tmp)
                    s_tmp = str(d_1)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    l_count.append(1)
                else:
                    Log_PO.logger.info("判定居民体重状态DRWS => {'表': '" + self.tableWS + "', 'ID': " + str(id) + "}")
                    d_1['No.'] = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator)
                    d_1['正向'] = 'error'
                    d_1['条件'] = l_conditions
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1['结果'] = '正向不满足'
                    d_1.update(d_tmp)
                    s_tmp = str(d_1)
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    l_count.append(0)

                    # 将错误条件写入数据库，以备复测。
                    # 将列表转换字符串
                    f_2_value = (self.convert_conditions(l_conditions))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                    d_tmp['条件'] = str(f_2_value)
                    d_tmp['测试数据'] = str(d_cases['satisfied'][i])
                    d_tmp['用例类型'] = '正向不满足'
                    s_tmp = str(d_tmp)
                    s_tmp = s_tmp.replace("'", "''")
                    s_tmp = s_tmp.replace("\\\\", "\\")
                    Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_log = '%s' where ID=%s" % (self.tableWS, s_tmp, d_tmp['ID']))
                caseTotal = caseTotal + 1
                Log_PO.logger.info("---------------------------------------------------------------------")

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
                        d_2['条件'] = l_conditions
                        d_2['测试数据'] = d_cases['notSatisfied'][i]
                        d_2['结果'] = '反向满足'
                        d_2.update(d_tmp)
                        s_tmp = str(d_2)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])
                        l_count.append(0)

                        # 将错误条件写入数据库，以备复测。
                        # 将列表转换字符串
                        f_conditions = (self.convert_conditions(l_conditions))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                        d_tmp['条件'] = str(f_conditions)
                        d_tmp['测试数据'] = str(d_cases['notSatisfied'][i])
                        d_tmp['用例类型'] = "反向满足"
                        s_tmp = str(d_tmp)
                        s_tmp = s_tmp.replace("'", "''")
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        # print(d_tmp)
                        Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_log = '%s' where ID=%s" % (self.tableWS, s_tmp, d_tmp['ID']))

                    else:
                        d_2['No.'] = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator)
                        d_2['反向'] = 'ok'
                        d_2['条件'] = l_conditions
                        d_2['测试数据'] = d_cases['notSatisfied'][i]
                        Color_PO.outColor([{"36": d_2}])
                        d_2.update(d_tmp)
                        s_tmp = str(d_2)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        l_count.append(1)
                    caseTotal = caseTotal + 1
                    Log_PO.logger.info("---------------------------------------------------------------------")

        d_result['caseTotal'] = caseTotal
        if 0 in l_count:
            d_result['ID'] = id
            d_result['数据集合'] = l_count
            d_result['count'] = 0
            Color_PO.outColor([{"31": d_result}])
            Log_PO.logger.info(d_result)
        else:
            d_result['count'] = 1
        return d_result

    def _DRWS_run(self, d_cases_satisfied, ID):

        # 公共测试用例

        # d_cases_satisfied = {'BMI': 16.8}
        # ID = 1

        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select(
            "select f_category, f_categoryCode, f_weightStatus, f_weightStatusCode from %s where ID= %s" % (self.tableWS, ID))
        # print(l_d_row)  # [{'f_category': '普通人群', 'f_categoryCode': '3', 'f_weightStatus': '体重偏低', 'f_weightStatusCode': '1'}]
        d_tmp['人群分类'] = l_d_row[0]['f_category']  # 普通人群
        d_tmp['人群分类编码'] = l_d_row[0]['f_categoryCode']  # 3
        d_tmp['体重状态'] = l_d_row[0]['f_weightStatus']  # 1
        d_tmp['体重状态编码'] = l_d_row[0]['f_weightStatusCode']  # 1

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
        if d_tmp['人群分类'] == '儿童':
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

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # command = command.replace("'", "''")
        # command = command.replace("\\\\","\\")
        d_tmp["i"] = command

        if d_r['code'] == 200:
            l_d_1 = Sqlserver_PO_CHC.select(
                "select WEIGHT_STATUS from WEIGHT_REPORT where ID = %s" % (WEIGHT_REPORT__ID))
            l_d_2 = Sqlserver_PO_CHC.select("select WEIGHT_STATUS from QYYH where SFZH = '%s'" % (str(d_tmp['身份证'])))
            d_tmp['sql__WEIGHT_REPORT'] = "select WEIGHT_STATUS from WEIGHT_REPORT where ID = " + str(WEIGHT_REPORT__ID)
            d_tmp['sql__QYYH'] = "select WEIGHT_STATUS from QYYH where SFZH = '" + str(d_tmp['身份证']) + "'"
            d_tmp['WEIGHT_REPORT__WEIGHT_STATUS'] = l_d_1[0]['WEIGHT_STATUS']
            d_tmp['QYYH__WEIGHT_STATUS'] = l_d_2[0]['WEIGHT_STATUS']
            d_tmp['l_d_1'] = l_d_1
            d_tmp['l_d_2'] = l_d_2
            d_tmp['WEIGHT_STATUS'] = l_d_1[0]['WEIGHT_STATUS']
            return d_tmp
        else:
            print("682, error ", d_r['code'])
            sys.exit(0)
    def DRWS_run_p(self, d_cases_satisfied, ID):

        d_tmp = self._DRWS_run(d_cases_satisfied, ID)
        if d_tmp['l_d_1'] == d_tmp['l_d_2'] and d_tmp['WEIGHT_STATUS'] == int(d_tmp['体重状态编码']):
            d_tmp['result'] = 1
        else:
            d_tmp['result'] = 0
        return d_tmp
    def DRWS_run_n(self, d_cases_satisfied, ID):

        d_tmp = self._DRWS_run(d_cases_satisfied, ID)
        if d_tmp['l_d_1'] == d_tmp['l_d_2'] and d_tmp['WEIGHT_STATUS'] != int(d_tmp['体重状态编码']):
            d_tmp['result'] = 0
        else:
            d_tmp['result'] = 1
        return d_tmp



