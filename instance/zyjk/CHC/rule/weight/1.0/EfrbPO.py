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


class EfrbPO():

    def __init__(self):
        self.tableEF = Configparser_PO.DB("tableWS")
        self.tableEF = Configparser_PO.DB("tableEF")
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


    def excel2db_EFRB(self):

        try:
            # excel文件导入db
            varTable = varSheet = "a_weight10_EFRB"

            # 1, db中删除已有的表
            Sqlserver_PO_CHC5G.execute("drop table if exists " + varTable)

            # 读取 Excel 文件
            df = pd.read_excel(Configparser_PO.FILE("case"), sheet_name=varSheet)
            # pd.set_option('display.max_columns', None)  # 显示全部列
            # pd.set_option('display.max_rows', None)  # 显示全部行
            # pd.set_option('display.max_colwidth', None)  # 不限制列宽
            # pd.set_option('display.width', None)  # 不限制显示宽度


            # 手动设置字段类型
            df['f_conditions'] = df['f_conditions'].astype(str)  # 改为字符串类型

            # **新增：按Excel原始顺序排序（假设Excel有默认行索引）**
            df = df.sort_index()  # 按行索引排序，保持Excel原有顺序
            df = df.dropna(how="all")  # 移除全空行

            # **新增：添加自增顺序列**
            df.insert(0, 'id', range(1, len(df) + 1))  # 插入到第一列
            # 如果需要将 id 设置为索引
            # df.set_index('id', inplace=True)

            # 2, excel导入db
            Sqlserver_PO_CHC5G.df2db(df, varTable)

            # 3, 设置表注释
            Sqlserver_PO_CHC5G.setTableComment(varTable, '体重管理1.0_评估因素规则库_自动化1')

            # 4， 替换换行符为空格
            Sqlserver_PO_CHC5G.execute(
                "UPDATE %s SET f_conditions = REPLACE(REPLACE(f_conditions, CHAR(10), ' '), CHAR(13), ' ');" % (
                    varTable))

            # 5, 设置字段类型与描述
            # Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'id', 'varchar(50)', '结果')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_result', 'varchar(50)', '结果')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_updateDate', 'varchar(50)', '更新日期')
            Sqlserver_PO_CHC5G.execute("ALTER TABLE %s ALTER COLUMN f_updateDate DATE;" % (varTable))
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_log', 'varchar(8000)', '日志信息', "utf-8")
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_type', 'varchar(50)', '分类')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_category', 'varchar(50)', '人群分类')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_categoryCode', 'varchar(50)', '人群分类编码')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ageType', 'varchar(50)', '年龄类型')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ruleName', 'varchar(100)', '规则名称')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_detail', 'varchar(999)', '评估规则详细描述')
            # Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_conditions_o', 'varchar(8000)', '评估因素判断规则_原始')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_conditions', 'varchar(8000)', '评估因素判断规则', "utf-8")
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_code', 'varchar(50)', '评估规则编码')
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_testcase', 'varchar(100)', '测试用例', "utf-8")
            Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_caseTotal', 'varchar(10)', '测试数量', "utf-8")

            # 6, 设置自增主键（最后）
            # Sqlserver_PO_CHC5G.setIdentityPrimaryKey(varTable, "id")


        except Exception as e:
            raise e


    def EFRB_case_or_1(self, d_cases, l_2_value, Numerator, Denominator, d_param):

        caseTotal = 0


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
        caseTotal = caseTotal + 1

        if 0 in l_count:
            s = "{'ID': " + str(id) + ", '合计数': " + str(l_count) + "}"
            Color_PO.outColor([{"31": s}])
            Log_PO.logger.info(s)
            return 0
        else:
            return 1
    def EFRB_case_or(self, d_cases, id, l_conditions, Numerator, Denominator, d_param):

        # 测试数据量
        caseTotal = 0
        d_result = {}

        if len(d_cases['satisfied']) == 1:
            # 正向用例, 一条数据
            l_count = []
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], id, d_param)
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
                Sqlserver_PO_CHC5G.execute("UPDATE %s SET f_log = '%s' where ID=%s" % (self.tableEF, s_tmp, d_tmp['ID']))
            caseTotal = caseTotal + 1

            # 一条数据，反向用例
            if Configparser_PO.SWITCH("testNegative") == "on":
                d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], id, d_param)
                if d_tmp['result'] == 1:
                    s_print = "{'反向': 'error', '条件': " + str(f_conditions) + ", '测试数据': " + str(d_cases['notSatisfied'][0]) + "}"
                    Color_PO.outColor([{"31": s_print}])
                    Log_PO.logger.info(s_print)
                    Color_PO.outColor([{"33": d_tmp}])
                    Log_PO.logger.info(d_tmp)
                    l_count.append(0)
                else:
                    s_print = "{'反向': 'ok', '条件': " + str(f_conditions) + ", '测试数据': " + str(d_cases['notSatisfied'][0]) + "}"
                    Color_PO.outColor([{"36": s_print}])
                    Log_PO.logger.info(s_print)
                    l_count.append(1)
                caseTotal = caseTotal + 1

        else:
            # 正向用例, N个数据
            l_count = []
            d_1 = {}
            for i in range(len(d_cases['satisfied'])):
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], id, d_param)
                if d_tmp['result'] == 1:
                    s_print = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator) + ", {'正向': 'ok', '条件': " + str(l_conditions) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    Color_PO.outColor([{"34": s_print}])
                    # Log_PO.logger.info(s_print)
                    caseTotal = caseTotal + 1
                    l_count.append(1)
                else:
                    # s = "要求 => {'ID': " + str(id) + ", '正向': 'error', '条件': " + str(l_2_value) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    # Color_PO.outColor([{"31": s}])
                    # Log_PO.logger.info(s)
                    d_1['表'] = 'a_weight10_EFRB'
                    d_1['ID'] = id
                    d_1['正向'] = 'error'
                    d_1['条件'] = l_conditions
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1.update(d_tmp)
                    s_tmp= str(d_1)
                    s_tmp = s_tmp.replace("\\\\","\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])

                    Log_PO.logger.info("---------------------------------------------------------------------")
                    caseTotal = caseTotal + 1
                    l_count.append(0)

            # 反向用例, N个数据
            if Configparser_PO.SWITCH("testNegative") == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    # d_tmp = self.EFRB_run_n(v[0], ID)
                    d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][i], id)
                    if d_tmp['result'] == 1:
                        # 反向如果命中就错，并且终止循环
                        s = "要求 => {'ID': " + str(id) + ", '反向': 'error', '条件': " + str(l_conditions) + ", '测试数据': " + str(
                            d_cases['notSatisfied'][i]) + "}"
                        Color_PO.outColor([{"31": s}])
                        Log_PO.logger.info(s)
                        s_tmp = str(d_tmp)
                        s_tmp = s_tmp.replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])

                        Log_PO.logger.info("---------------------------------------------------------------------")
                        caseTotal = caseTotal + 1
                        l_count.append(0)

                        # 将列表转换字符串
                        f_2_value = (self.convert_conditions(l_conditions))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7
                        d_tmp['条件'] = str(f_2_value)
                        d_tmp['测试数据'] = str(d_cases['notSatisfied'][i])
                        d_tmp['用例类型'] = "反向满足"
                    else:
                        s_print = "{'反向': 'ok', '条件': " + str(l_conditions) + ", '测试数据': " + str(d_cases['notSatisfied'][i]) + "}"
                        Color_PO.outColor([{"36": s_print}])
                        caseTotal = caseTotal + 1
                        l_count.append(1)

        d_result['caseTotal'] = caseTotal
        if 0 in l_count:
            d_result['ID'] = id
            d_result['数据集合'] = l_count
            d_result['count'] = 0
            # Color_PO.outColor([{"31": d_result}])
            Log_PO.logger.info(d_result)
        else:
            d_result['count'] = 1
        return d_result

    # 评估因素规则库 Evaluation Factor Rule Base
    def EFRB_1(self, varTestID, d_param):

        # EFRB(self, varTestID, varPN="p")
        # 评估因素规则库 Evaluation Factor Rule Base
        # a_weight10_EFRB
        # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
        # varPN = p 执行正向（默认值p），n 执行反向；

        d_tmp = {}

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select f_conditions, f_code from %s where ID =%s" % (self.tableEF, varTestID))
        # print("1299l_d_row => ", l_d_row)
        # print(l_d_row[0]['f_conditions'])
        f_conditions = (l_d_row[0]['f_conditions'])
        # f_code = (l_d_row[0]['f_code'])
        d_tmp['规则库'] = '评估因素规则库EFRB'
        d_tmp['表'] = self.tableEF
        d_tmp['ID'] = varTestID
        d_tmp['f_conditions'] = l_d_row[0]['f_conditions']
        d_tmp['f_code'] = l_d_row[0]['f_code']
        d_tmp.update(d_param)

        # 统计所有组合的数量
        varTestCount = f_conditions.count("or")
        # print(varTestCount)  # 输出or的数量: 2

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
            print("测试数据集合 =>", d_cases)

            # 测试数据
            # todo EFRB for and
            count = self.EFRB_case_1(d_cases, l_ER, d_tmp)
            print("1474count", count)
            return count

        elif "and" not in f_conditions and "年龄" not in f_conditions:

            # todo EFRB_case for 人群分类

            print("varTestID：", varTestID)

            self.EFRB_run_crowd_1(varTestID, d_param)

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

                # print("--------------------")
                # print("测试数据集合 =>", d_cases)
                # sys.exit(0)

                # 判断输出结果
                # todo EFRB_case_or for or
                # self.EFRB_case_1(d_cases, l_ER, d_tmp)

                print("9999")
                count = self.EFRB_case_or_1(d_cases, l_2_value, lln+1, varTestCount+1, d_tmp)
                return count
                # caseTotal, varCount = self.EFRB_case_or(d_cases, id, l_2_value, lln+1, varTestCount+1)


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
            # print("测试数据集合 =>", d_cases)

            # 测试数据
            # todo EFRB for and
            count = self.EFRB_case_1(d_cases, l_ER, d_tmp)
            print("1474count", count)
            return count

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

    def _EFRB_result(self, count, caseTotal, ID):
        d_result = {}
        if 0 not in count:
            d_result['ID'] = ID
            d_result['结果'] = 'ok'
            Color_PO.outColor([{"32": "返回值 => " + str(d_result)}])
            Log_PO.logger.info("返回值 => " + str(d_result))
            Sqlserver_PO_CHC5G.execute(
                "update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                self.tableEF, caseTotal, ID))
        else:
            d_result['ID'] = ID
            d_result['结果'] = 'error'
            Color_PO.outColor([{"31": "返回值 => " + str(d_result)}])
            Log_PO.logger.info("返回值 => " + str(d_result))
            Sqlserver_PO_CHC5G.execute(
                "update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (
                self.tableEF, caseTotal, ID))
        Log_PO.logger.info("---------------------------------------------------------------------")

    def EFRB(self, varTestID, d_param={}):

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select id, f_conditions, f_code from %s" % (self.tableEF))
        # print("l_d_row => ", l_d_row)
        if varTestID == "all":
            self._EFRB(d_param)
        elif varTestID > len(l_d_row) or varTestID <= 0:
            print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
            sys.exit(0)
        else:
            self._EFRB2(varTestID, d_param)

    # def _EFRB(self, d_param):
    #
    #     # EFRB(self, varTestID, varPN="p")
    #     # 评估因素规则库 Evaluation Factor Rule Base
    #     # a_weight10_EFRB
    #     # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
    #     # varPN = p 执行正向（默认值p），n 执行反向；
    #
    #     d_ = {}
    #
    #     # 获取每行测试数据
    #     l_d_row = Sqlserver_PO_CHC5G.select("select id, f_conditions, f_code from %s" % (self.tableEF))
    #     # print("l_d_row => ", l_d_row)
    #
    #     d_['table'] = self.tableEF
    #     for i, index in enumerate(l_d_row):
    #         id = l_d_row[i]['id']
    #         f_conditions = l_d_row[i]['f_conditions']
    #         d_['ID'] = id
    #         d_['f_conditions'] = f_conditions
    #
    #         # 获取原始数据
    #         print("评估因素规则库EFRB =>", d_)
    #         Log_PO.logger.info("评估因素规则库EFRB =>" + str(d_))
    #
    #         # 统计所有组合的数量
    #         varTestCount = f_conditions.count("or")
    #         # print(varTestCount)  # 输出or的数量: 2
    #
    #         # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
    #         f_conditions = f_conditions.replace("月", '')
    #         f_conditions = f_conditions.replace('＞', '>').replace('＜', '<').replace('＝', '=')
    #
    #         # todo EFRB_case for 高血压&糖尿病
    #         if f_conditions == "高血压" or f_conditions == "糖尿病":
    #             # 判断输出结果
    #             self.EFRB_run_disease(f_conditions, id)
    #             # if varPN == "n":
    #             #     self.EFRB_run_disease_n("脑卒中", id)
    #             # else:
    #             #     self.EFRB_run_disease(f_conditions, id)
    #
    #         # todo EFRB_case for 人群分类
    #         elif f_conditions.isdigit() == True:
    #             # 判断输出结果
    #             self.EFRB_run_crowd(f_conditions, id)
    #
    #         # todo EFRB_case for 只有年龄
    #         elif "and" not in f_conditions and "BMI" not in f_conditions:
    #             l_2_value = []
    #             # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
    #             l_simple_conditions = Age_PO.splitMode(f_conditions)
    #             l_2_value.extend(l_simple_conditions)
    #             # print("611 分解参数 =", l_2_value)
    #
    #             # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
    #             l_3_value = []
    #             for i in l_2_value:
    #                 l_simple_conditions = Age_PO.interconvertMode(i)
    #                 l_3_value.extend(l_simple_conditions)
    #             print("680 结构化参数 =", l_3_value)  #680 结构化参数 = ['年龄<=3']
    #
    #             # 读取模块，生成随机数据d_cases
    #             d_cases = Age_PO.generate_all_cases(l_3_value)
    #             print("测试数据集合 =>", d_cases)  # {'satisfied': [{'年龄': 3.0}, {'年龄': 2.5}], 'not1': [{'年龄': 16.9}]}
    #
    #             # todo EFRB_case for 只有年龄
    #             # 判断输出结果
    #             self.EFRB_case(d_cases, id, l_2_value)
    #
    #         # todo 2 EFRB 集合（(6<=年龄＜6.5 and 13.4＞BMI and 性别=男) or (6.5<=年龄＜7 and 13.8＞BMI and 性别=男)）
    #         elif "or" in f_conditions:
    #
    #             # 格式化数据，结构化原始数据为列表，生成l_l_N
    #             l_value = f_conditions.split("or")
    #             l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
    #             l_value = [i.split("and") for i in l_value]
    #             l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
    #             # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
    #             print("--------------------")
    #
    #             l_count = []
    #             sum = 0
    #             for lln in range(len(l_l_value)):
    #
    #                 # Age、BMI、年龄 - 格式化条件
    #                 l_conditions = []
    #                 # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
    #                 # print(l_l_value(lln))
    #                 for i in l_l_value[lln]:
    #                     if "BMI" in i:
    #                         l_split_conditions = BmiAgeSex_PO.splitMode(i)
    #                         l_conditions.extend(l_split_conditions)
    #                     if "年龄" in i:
    #                         l_split_conditions = BmiAgeSex_PO.splitMode(i)
    #                         l_conditions.extend(l_split_conditions)
    #                     elif "性别" in i:
    #                         l_split_conditions = BmiAgeSex_PO.splitMode(i)
    #                         l_conditions.extend(l_split_conditions)
    #                 # print("611 分解参数 =", l_2_value)
    #
    #                 # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
    #                 l_interconvert_conditions = []
    #                 for i in l_conditions:
    #                     l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
    #                     l_interconvert_conditions.extend(l_simple_conditions)
    #
    #                 # 生成随机数据 d_cases
    #                 for i in l_interconvert_conditions:
    #                     if ('>=' or '<=') in i:
    #                         if '年龄' in i:
    #                             d_cases = BmiAgeSex_PO.main(l_interconvert_conditions)
    #                             break
    #                         if 'BMI' in i:
    #                             d_cases = BmiAgeSex_PO.main(l_interconvert_conditions)
    #                             break
    #                     else:
    #                         d_cases = BmiAgeSex_PO.main(l_interconvert_conditions)
    #
    #                 if Configparser_PO.SWITCH("testDataSet") == "on":
    #                     print("测试数据集合 =>", d_cases)
    #
    #                 # 判断输出结果
    #                 # todo DRWS_case_or for 集合
    #                 # 测试数据
    #                 Numerator = lln + 1
    #                 Denominator = varTestCount + 1
    #                 d_result = self.EFRB_case_or(d_cases, id, l_conditions, Numerator, Denominator, d_param)
    #                 # print(d_result)
    #                 l_count.append(d_result['count'])
    #                 sum = sum + d_result['caseTotal']
    #
    #                 # 更新记录
    #             self._EFRB_result(l_count, sum, id)
    #
    #
    #         # todo EFRB 简单条件组合
    #         elif "and" in f_conditions:
    #
    #             # 转换成列表
    #             l_ER = f_conditions.split("and")
    #             l_ER = [i.strip() for i in l_ER]
    #             # print("1039 实际参数 =", l_ER)  # ['18.5<BMI', 'BMI<24.0']
    #
    #             l_2_value = []
    #             # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
    #             for i in l_ER:
    #                 l_simple_conditions = BmiAgeSex_PO.splitMode(i)
    #                 l_2_value.extend(l_simple_conditions)
    #             # print("1046 分解参数 =", l_2_value)
    #
    #             # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
    #             l_3_value = []
    #             for i in l_2_value:
    #                 l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
    #                 l_3_value.extend(l_simple_conditions)
    #             # print("1053 结构化参数 =", l_3_value)  #  ['BMI>18.5', 'BMI<24.0']
    #
    #             # 读取BMI模块，生成随机数据d_cases
    #             d_cases = BmiAge_PO.main(l_3_value)
    #             print("测试数据集合 =>", d_cases)
    #
    #             # 测试数据
    #             # todo EFRB for and
    #             self.EFRB_case(d_cases, id, l_ER, d_param)
    #
    #         # todo EFRB 无条件组合
    #         elif "and" not in f_conditions:
    #
    #             l_2_value = []
    #             # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
    #             l_simple_conditions = Bmi_PO.splitMode(f_conditions)
    #             l_2_value.extend(l_simple_conditions)
    #             # print("611 分解参数 =", l_2_value)
    #
    #             # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
    #             l_3_value = []
    #             for i in l_2_value:
    #                 l_simple_conditions = Bmi_PO.interconvertMode(i)
    #                 l_3_value.extend(l_simple_conditions)
    #             # print("680 结构化参数 =", l_3_value)  # ['BMI<18.5']
    #
    #             # 读取BMI模块，生成随机数据d_cases
    #             d_cases = Age_PO.generate_all_cases(l_3_value)
    #             # d_cases = Bmi_PO.generate_all_cases(l_3_value)
    #             print(d_cases)  # {'satisfied': [{'BMI': 16.8}], 'not1': [{'BMI': 19.6}]}
    #
    #             # todo EFRB_case for not and
    #             # 判断输出结果
    #             self.EFRB_case(d_cases, id, l_2_value)
    #
    #         else:
    #             print("[not or & and ]")
    #         print("-".center(100, "-"))

    def _EFRB(self, d_param):

        # EFRB(self, varTestID, varPN="p")
        # 评估因素规则库 Evaluation Factor Rule Base
        # a_weight10_EFRB
        # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
        # varPN = p 执行正向（默认值p），n 执行反向；

        d_ = {}

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select id, f_conditions, f_code from %s" % (self.tableEF))
        # print("l_d_row => ", l_d_row)



        d_['table'] = self.tableEF
        for i, index in enumerate(l_d_row):
            # print(varTestID,l_d_row[i]['id'])

                id = l_d_row[i]['id']
                f_conditions = l_d_row[i]['f_conditions']
                d_['ID'] = id
                d_['f_conditions'] = f_conditions
                d_['表注释'] = '评估因素规则库EFRB'

                # 获取原始数据
                print("测试项 =>", d_)
                Log_PO.logger.info("测试项 => " + str(d_))

                # 统计所有组合的数量
                varTestCount = f_conditions.count("or")
                # print(varTestCount)  # 输出or的数量: 2

                # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
                f_conditions = f_conditions.replace("月", '')
                f_conditions = f_conditions.replace('＞', '>').replace('＜', '<').replace('＝', '=')

                # todo EFRB_case for 高血压&糖尿病
                if f_conditions == "高血压" or f_conditions == "糖尿病":
                    self.EFRB_run_disease(f_conditions, id)


                # todo EFRB_case for 人群分类
                elif f_conditions.isdigit() == True:
                    self.EFRB_run_crowd(f_conditions, id)


                # todo EFRB_case for 只有年龄
                elif "年龄" in f_conditions and "BMI" not in f_conditions:
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
                    # print("802 结构化参数 =", l_3_value)  #680 结构化参数 = ['年龄<=3']

                    # 读取模块，生成随机数据d_cases
                    d_cases = Age_PO.generate_all_cases(l_3_value)
                    print("测试数据 =>", d_cases)  # {'satisfied': [{'年龄': 3.0}, {'年龄': 2.5}], 'not1': [{'年龄': 16.9}]}
                    Log_PO.logger.info("测试数据 => " + str(d_cases))

                    # todo EFRB_case for 只有年龄
                    self.EFRB_case(d_cases, id, l_2_value,d_param)


                # todo 2 EFRB 集合（(6<=年龄＜6.5 and 13.4＞BMI and 性别=男) or (6.5<=年龄＜7 and 13.8＞BMI and 性别=男)）
                elif "or" in f_conditions:

                    # 格式化数据，结构化原始数据为列表，生成l_l_N
                    l_value = f_conditions.split("or")
                    l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
                    l_value = [i.split("and") for i in l_value]
                    l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
                    # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
                    print("--------------------")

                    l_count = []
                    sum = 0
                    for lln in range(len(l_l_value)):

                        # Age、BMI、年龄 - 格式化条件
                        l_conditions = []
                        # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                        # print(l_l_value(lln))
                        for i in l_l_value[lln]:
                            if "BMI" in i:
                                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                                l_conditions.extend(l_split_conditions)
                            if "年龄" in i:
                                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                                l_conditions.extend(l_split_conditions)
                            elif "性别" in i:
                                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                                l_conditions.extend(l_split_conditions)
                        # print("611 分解参数 =", l_2_value)

                        # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                        l_interconvert_conditions = []
                        for i in l_conditions:
                            l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                            l_interconvert_conditions.extend(l_simple_conditions)

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
                            print("测试数据 =>", d_cases)

                        # 判断输出结果
                        # todo DRWS_case_or for 集合
                        # 测试数据
                        Numerator = lln + 1
                        Denominator = varTestCount + 1
                        d_result = self.EFRB_case_or(d_cases, id, l_conditions, Numerator, Denominator, d_param)
                        # print(d_result)
                        l_count.append(d_result['count'])
                        sum = sum + d_result['caseTotal']

                        # 更新记录
                    self._EFRB_result(l_count, sum, id)

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

    def _EFRB2(self, varTestID, d_param):

        # EFRB(self, varTestID, varPN="p")
        # 评估因素规则库 Evaluation Factor Rule Base
        # a_weight10_EFRB
        # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
        # varPN = p 执行正向（默认值p），n 执行反向；

        d_ = {}

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select id, f_conditions, f_code from %s" % (self.tableEF))
        # print("l_d_row => ", l_d_row)

        d_['table'] = self.tableEF
        for i, index in enumerate(l_d_row):
            # print(varTestID,l_d_row[i]['id'])
            if l_d_row[i]['id'] == varTestID:
                id = l_d_row[i]['id']
                f_conditions = l_d_row[i]['f_conditions']
                d_['ID'] = id
                d_['f_conditions'] = f_conditions
                d_['表注释'] = '评估因素规则库EFRB'

                # 获取原始数据
                print("测试项 =>", d_)
                Log_PO.logger.info("测试项 => " + str(d_))

                # 统计所有组合的数量
                varTestCount = f_conditions.count("or")
                # print(varTestCount)  # 输出or的数量: 2

                # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
                f_conditions = f_conditions.replace("月", '')
                f_conditions = f_conditions.replace('＞', '>').replace('＜', '<').replace('＝', '=')

                # todo EFRB_case for 高血压&糖尿病
                if f_conditions == "高血压" or f_conditions == "糖尿病":
                    self.EFRB_run_disease(f_conditions, id)


                # todo EFRB_case for 人群分类
                elif f_conditions.isdigit() == True:
                    self.EFRB_run_crowd(f_conditions, id)


                # todo EFRB_case for 只有年龄
                elif "年龄" in f_conditions and "BMI" not in f_conditions:
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
                    # print("802 结构化参数 =", l_3_value)  #680 结构化参数 = ['年龄<=3']

                    # 读取模块，生成随机数据d_cases
                    d_cases = Age_PO.generate_all_cases(l_3_value)
                    print("测试数据 =>", d_cases)  # {'satisfied': [{'年龄': 3.0}, {'年龄': 2.5}], 'not1': [{'年龄': 16.9}]}
                    Log_PO.logger.info("测试数据 => " + str(d_cases))

                    # todo EFRB_case for 只有年龄
                    self.EFRB_case(d_cases, id, l_2_value,d_param)


                # todo 2 EFRB 集合（(6<=年龄＜6.5 and 13.4＞BMI and 性别=男) or (6.5<=年龄＜7 and 13.8＞BMI and 性别=男)）
                elif "or" in f_conditions:

                    # 格式化数据，结构化原始数据为列表，生成l_l_N
                    l_value = f_conditions.split("or")
                    l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
                    l_value = [i.split("and") for i in l_value]
                    l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
                    # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
                    print("--------------------")

                    l_count = []
                    sum = 0
                    for lln in range(len(l_l_value)):

                        # Age、BMI、年龄 - 格式化条件
                        l_conditions = []
                        # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                        # print(l_l_value(lln))
                        for i in l_l_value[lln]:
                            if "BMI" in i:
                                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                                l_conditions.extend(l_split_conditions)
                            if "年龄" in i:
                                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                                l_conditions.extend(l_split_conditions)
                            elif "性别" in i:
                                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                                l_conditions.extend(l_split_conditions)
                        # print("611 分解参数 =", l_2_value)

                        # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                        l_interconvert_conditions = []
                        for i in l_conditions:
                            l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                            l_interconvert_conditions.extend(l_simple_conditions)

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
                            print("测试数据 =>", d_cases)

                        # 判断输出结果
                        # todo DRWS_case_or for 集合
                        # 测试数据
                        Numerator = lln + 1
                        Denominator = varTestCount + 1
                        d_result = self.EFRB_case_or(d_cases, id, l_conditions, Numerator, Denominator, d_param)
                        # print(d_result)
                        l_count.append(d_result['count'])
                        sum = sum + d_result['caseTotal']

                        # 更新记录
                    self._EFRB_result(l_count, sum, id)

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

                if varTestID != "all":
                    break

    def EFRB_case_1(self, d_cases, l_2_value, d_param):

        # d_case : 测试数据
        # L_2_value： 条件
        # d_param：接口的参数

        caseTotal = 0

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

    def _EFRB_result(self, l_count, caseTotal, ID):
        d_result = {}
        if 0 not in l_count:
            d_result['ID'] = ID
            d_result['result'] = 'ok'
            s = "结果 => " + str(d_result)
            Color_PO.outColor([{"32": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableEF, caseTotal, ID))
        else:
            d_result['ID'] = ID
            d_result['result'] = 'error'
            s = "结果 => " + str(d_result)
            Color_PO.outColor([{"31": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableEF, caseTotal, ID))
        Log_PO.logger.info("---------------------------------------------------------------------")

    def _EFRB_print_ok(self,pORn, l_conditions, testData, d_tmp):
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

    def EFRB_case(self, d_cases, ID, l_2_value, d_param):

        # d_case : 测试数据
        # L_2_value： 条件
        # d_param：接口的参数

        caseTotal = 0

        if len(d_cases['satisfied']) == 1:
            # 正向用例, 一条数据
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
            caseTotal = caseTotal + 1

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
                    caseTotal = caseTotal + 1
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
                    caseTotal = caseTotal + 1
                    l_count.append(0)

        self._EFRB_result(l_count, caseTotal, ID)


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
        l_d_row = Sqlserver_PO_CHC5G.select("select f_conditions, f_code from %s where ID= %s" % (self.tableEF, ID))
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']
        categoryCode = l_d_row[0]['f_conditions']

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
        # 获取f_code,f_age
        l_d_row = Sqlserver_PO_CHC5G.select("select f_category, f_categoryCode, f_ageType, f_code from %s where id= %s" % (self.tableEF, ID))
        # print(l_d_row)
        d_tmp['人群分类'] = l_d_row[0]['f_category']
        d_tmp['人群分类编码'] = l_d_row[0]['f_categoryCode']
        d_tmp['年龄类型'] = l_d_row[0]['f_ageType']
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']
        # d_tmp['条件'] = l_d_row[0]['f_conditions']

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
        # print(d_tmp['人群分类编码'])
        if d_tmp['年龄类型'] == "int":
            if d_tmp['人群分类编码'] == '1':
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
            # l_count = []
            # if d_tmp['预期值'] in l_d_RULE_CODE_actual:


            # d_tmp['实际值'] = l_d_RULE_CODE_actual[0]['RULE_CODE']
            # d_tmp['预期值'] = l_d_row[0]['f_code']
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

