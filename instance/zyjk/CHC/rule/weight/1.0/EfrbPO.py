# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0 - 评估因素规则库 Evaluation Factor Rule Base
# 需求：体重管理1.18
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r

# 数据源：weight10.xlsx - a_weight10_EFRB 导入数据库
# 测试数据库表：CHC-5G - a_weight10_EFRB
# 测试数据：CHC - WEIGHT_REPORT(体重报告记录表) - ID=2的记录
# 比对规则：CHC-5G - T_ASSESS_RULE_RECORD

# 警告如下：D:\dwp_backup\python study\GUI_wxpython\lib\site-packages\openpyxl\worksheet\_reader.py:312: UserWarning: Unknown extension is not supported and will be removed warn(msg)
# 解决方法：
import sys
import warnings
warnings.simplefilter("ignore")
# *****************************************************************


import subprocess

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
        self.tableEF = Configparser_PO.DB("tableEF")
        self.WEIGHT_REPORT__IDCARD = Configparser_PO.FILE("testIdcard")

        # 判断QYYH中是否存在此身份证
        isSFZH__QYYH = Sqlserver_PO_CHC.isRecord("QYYH", "SFZH", self.WEIGHT_REPORT__IDCARD)
        # 判断WEIGHT_REPORT中是否存在此身份证
        isID_CARD__WEIGHT_REPORT = Sqlserver_PO_CHC.isRecord("WEIGHT_REPORT", "ID_CARD", self.WEIGHT_REPORT__IDCARD)
        if isSFZH__QYYH != 1 or isID_CARD__WEIGHT_REPORT != 1:
            s = f'error, 身份证：{Configparser_PO.FILE("testIdcard")} 不存在!'
            Color_PO.outColor([{"35": s}])
            sys.exit(0)


        # 获取ID
        l_d_ID = Sqlserver_PO_CHC.select(
            "select ID from WEIGHT_REPORT where ID_CARD = '%s'" % (self.WEIGHT_REPORT__IDCARD))
        # print(l_d_ID[0]['ID'])  # 1644
        self.WEIGHT_REPORT__ID = l_d_ID[0]['ID']


    def convert_conditions(self, conditions):
        # 列表转字符串

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



    def EFRB(self, varTestID, d_param={}):

        # 主程序
        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select id, f_conditions, f_code from %s" % (self.tableEF))
        # print("l_d_row =>", l_d_row)  # [{'id': 1, 'f_conditions': 'BMI>=24 and 年龄>=18 and 年龄<65', 'f_code': 'TZ_STZB001'}, {'id': 2, 'f_conditions': 'BMI<24 and BMI>=18.5 and 年龄>=18 and 年龄<65', 'f_code': 'TZ_STZB002'},

        if varTestID == "all":
            # 测试所有规则
            self._EFRB_ALL()
        elif varTestID > len(l_d_row) or varTestID <= 0:
            # 异常退出
            print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
            sys.exit(0)
        else:
            # 测试一条规则
            self._EFRB_ID(varTestID, d_param)

    def _EFRB_main(self, d_param, f_conditions):

        # 统计所有组合的数量
        varTestCount = f_conditions.count("or")
        # print(varTestCount)  # 输出or的数量: 2

        # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
        f_conditions = f_conditions.replace("月", '')
        f_conditions = f_conditions.replace('＞', '>').replace('＜', '<').replace('＝', '=')

        # todo id 高血压&糖尿病
        if '疾病' in f_conditions:
            d_param['disease'] = f_conditions
            self.EFRB_run_disease(d_param)


        # todo id 人群分类
        elif '人群分类' in f_conditions:
        # elif f_conditions.isdigit() == True:
            d_param['categoryCode'] = f_conditions.split("=")[1]
            self.EFRB_run_crowd(d_param)


        # todo id 只有年龄
        elif "年龄" in f_conditions and "BMI" not in f_conditions:

            # 元素拆分，如 '6<=年龄<6.5'
            l_conditions = []
            l_simple_conditions = Age_PO.splitMode(f_conditions)
            l_conditions.extend(l_simple_conditions)
            # print(422, l_conditions)

            # 转换位置，如将 18.5>BMI 转换 BMI<18.5
            l_conditions_interconver = []
            for i in l_conditions:
                l_simple_conditions = Age_PO.interconvertMode(i)
                l_conditions_interconver.extend(l_simple_conditions)
            # print(429, l_conditions_interconver)

            # 生成随机数据d_cases
            d_cases = Age_PO.generate_all_cases(l_conditions_interconver)
            if Configparser_PO.SWITCH("testDataSet") == "on":
                print("测试数据集 =>", d_cases)  # {'satisfied': [{'年龄': 3.0}, {'年龄': 2.5}], 'not1': [{'年龄': 16.9}]}
            Log_PO.logger.info("测试数据集 => " + str(d_cases))

            # todo EFRB_case for 只有年龄
            self.EFRB_case(d_cases, d_param)


        # todo id 集合（(6<=年龄＜6.5 and 13.4＞BMI and 性别=男) or (6.5<=年龄＜7 and 13.8＞BMI and 性别=男)）
        elif "or" in f_conditions:

            # 格式化数据，结构化原始数据为列表，生成l_l_N
            l_value = f_conditions.split("or")
            l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
            l_value = [i.split("and") for i in l_value]
            l_l_value = [[item.strip() for item in sublist] for sublist in l_value]
            # print(l_l_value)  # [['14<= 年龄＜14.5', '22.3<= BMI', '性别=男'], ['14.5<= 年龄＜15', '22.6<= BMI', '性别=男'],...
            # print("--------------------")

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
            d_param['l_count'] = l_count
            d_param['caseTotal'] = sum
            # print(680, d_param)
            self._EFRB_result(d_param)


        # todo id 年龄和BMI
        elif "and" in f_conditions and "or" not in f_conditions and "BMI" in f_conditions and "年龄" in f_conditions:

            # 如：(BMI>=24 and 年龄>=18 and 年龄<65)
            # 字符串转换成列表
            l_conditions = f_conditions.split("and")
            l_conditions = [i.strip() for i in l_conditions]
            # print(517, l_conditions)  # ['18.5<BMI', 'BMI<24.0']

            # 元素拆分，如:'6<=年龄<6.5'
            l_conditions_split = []
            for i in l_conditions:
                l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                l_conditions_split.extend(l_simple_conditions)
            # print(524, l_conditions_split)  # ['年龄>=6', '年龄<6.5']

            # 转换位置，如:将 18.5>BMI 转换 BMI<18.5
            l_conditions_interconver = []
            for i in l_conditions_split:
                l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                l_conditions_interconver.extend(l_simple_conditions)
            # print(531, l_conditions_interconver)  # ['BMI>18.5', 'BMI<24.0']

            # 生成测试数据
            d_cases = BmiAge_PO.main(l_conditions_interconver)
            if Configparser_PO.SWITCH("testDataSet") == "on":
                print("测试数据集 =>", d_cases)
            Log_PO.logger.info("测试数据集 => " + str(d_cases))

            # 测试数据
            d_param['l_conditions'] = l_conditions
            self.EFRB_case(d_cases, d_param)


        # todo id 无条件组合，
        elif "and" not in f_conditions:

            l_conditions = []
            # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
            l_simple_conditions = Bmi_PO.splitMode(f_conditions)
            l_conditions.extend(l_simple_conditions)
            # print("611 分解参数 =", l_2_value)

            # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
            l_3_value = []
            for i in l_conditions:
                l_simple_conditions = Bmi_PO.interconvertMode(i)
                l_3_value.extend(l_simple_conditions)
            # print("680 结构化参数 =", l_3_value)  # ['BMI<18.5']

            # 读取BMI模块，生成随机数据d_cases
            d_cases = Age_PO.generate_all_cases(l_3_value)
            if Configparser_PO.SWITCH("testDataSet") == "on":
                print("测试数据集 =>", d_cases)
            Log_PO.logger.info("测试数据集 => " + str(d_cases))

            # todo EFRB_case for not and
            # 判断输出结果
            # self.EFRB_case(d_cases, id, l_2_value)
            d_param['l_conditions'] = l_conditions
            self.EFRB_case(d_cases, d_param)

        else:
            print("[not or & and ]")

    def _EFRB_ALL(self):

        # EFRB(self, varTestID, varPN="p")
        # 评估因素规则库 Evaluation Factor Rule Base
        # a_weight10_EFRB
        # varTestID = 1, 执行ID=1的测试数据 ； varTestID = 'all',执行所有的测试数据
        # varPN = p 执行正向（默认值p），n 执行反向；

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select id, f_conditions, f_code from %s" % (self.tableEF))
        # print("l_d_row => ", l_d_row)

        for i, index in enumerate(l_d_row):
            d_param = {}
            d_param['table'] = self.tableEF
            d_param['ID'] = l_d_row[i]['id']
            f_conditions = l_d_row[i]['f_conditions']
            d_param['f_conditions'] = f_conditions
            d_param['表注释'] = '评估因素规则库EFRB'
            d_param['WEIGHT_REPORT__IDCARD'] = self.WEIGHT_REPORT__IDCARD

            s = "测试 => " + str(d_param)
            Color_PO.outColor([{"35": s}])
            Log_PO.logger.info(s)

            self._EFRB_main(d_param, f_conditions)


    def _EFRB_ID(self, varTestID, d_param):

        # 评估因素规则库 Evaluation Factor Rule Base

        # 测试一条规则
        # varTestID = 1   //id=1

        d_ = {}

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select f_conditions, f_code from %s where id=%s" % (self.tableEF, varTestID))
        # print("l_d_row =>", l_d_row)  # [{'f_conditions': 'BMI>=24 and 年龄>=18 and 年龄<65', 'f_code': 'TZ_STZB001'}]
        f_conditions = l_d_row[0]['f_conditions']

        d_['table'] = self.tableEF
        d_['ID'] = varTestID
        d_['f_conditions'] = f_conditions
        d_['表注释'] = '评估因素规则库EFRB'
        d_['WEIGHT_REPORT__IDCARD'] = self.WEIGHT_REPORT__IDCARD
        d_.update(d_param)
        s = "测试 => " + str(d_)
        Color_PO.outColor([{"35": s}])
        Log_PO.logger.info(s)

        self._EFRB_main(d_, f_conditions)



    def EFRB_case(self, d_cases, d_param):

        # d_case : 测试数据
        # d_param：参数
        # print(579, d_param)  # {'table': 'a_weight10_EFRB', 'ID': 1, 'f_conditions': 'BMI>=24 and 年龄>=18 and 年龄<65', '表注释': '评估因素规则库EFRB', 'l_conditions': ['BMI>=24', '年龄>=18', '年龄<65']}

        caseTotal = 0

        if len(d_cases['satisfied']) == 1:
            # 正向用例, 一条数据
            l_count = []
            # todo EFRB_run_p_1
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], d_param)
            d_1 = {}
            if d_tmp['result'] == 1:
                d_1['正向'] = "ok"
                d_1['条件'] = d_param['f_conditions']
                d_1['测试数据'] = d_cases['satisfied'][0]
                if Configparser_PO.SWITCH("positiveResult") == "on":
                    Color_PO.outColor([{"34": d_1}])
                Log_PO.logger.info(d_1)
                l_count.append(1)
            else:
                d_1['正向'] = "error"
                d_1['条件'] = d_param['f_conditions']
                d_1['测试数据'] = d_cases['satisfied'][0]
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                # s_print = "[正向error], 条件：" + str(l_2_value) + "，测试数据：" + str(d_cases['satisfied'][0])
                if Configparser_PO.SWITCH("positiveResult") == "on":
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
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], d_param)
                d_1 = {}
                if d_tmp['result'] == 1:
                    d_1['正向'] = "ok"
                    d_1['条件'] = d_param['f_conditions']
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    if Configparser_PO.SWITCH("positiveResult") == "on":
                        Color_PO.outColor([{"34": d_1}])
                    Log_PO.logger.info(d_1)
                    caseTotal = caseTotal + 1
                    l_count.append(1)
                else:
                    d_1['正向'] = "error"
                    d_1['条件'] = d_param['f_conditions']
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1.update(d_tmp)
                    s_tmp = str(d_1)
                    s_tmp = s_tmp.replace("\\\\","\\")
                    if Configparser_PO.SWITCH("positiveResult") == "on":
                        Color_PO.outColor([{"31": s_tmp}])
                    Log_PO.logger.info(s_tmp)
                    caseTotal = caseTotal + 1
                    l_count.append(0)

        d_param['l_count'] = l_count
        d_param['caseTotal'] = caseTotal
        self._EFRB_result(d_param)

    def EFRB_case_or(self, d_cases, id, l_conditions, Numerator, Denominator, d_param):

        # 测试数据量
        caseTotal = 0
        d_result = {}

        if len(d_cases['satisfied']) == 1:
            # 正向用例, 一条数据
            l_count = []
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], d_param)
            d_1 = {}
            if d_tmp['result'] == 1:
                d_1['No.'] = str(Numerator) + "/" + str(Denominator)
                d_1['正向'] = 'ok'
                d_1['条件'] = l_conditions
                d_1['测试数据'] = d_cases['satisfied'][0]
                if Configparser_PO.SWITCH("positiveResult") == "on":
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
                f_conditions = (self.convert_conditions(l_conditions))  # 将列表转换字符串
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
                d_tmp = self.DRWS_run_n(d_cases['notSatisfied'][0], d_param)
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
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], d_param)
                if d_tmp['result'] == 1:
                    s_print = str(Numerator) + "(" + str(i + 1) + ")/" + str(Denominator) + ", {'正向': 'ok', '条件': " + str(l_conditions) + ", '测试数据': " + str(d_cases['satisfied'][i]) + "}"
                    if Configparser_PO.SWITCH("positiveResult") == "on":
                        Color_PO.outColor([{"34": s_print}])
                    Log_PO.logger.info(s_print)
                    caseTotal = caseTotal + 1
                    l_count.append(1)
                else:
                    d_1['表'] = 'a_weight10_EFRB'
                    d_1['ID'] = id
                    d_1['正向'] = 'error'
                    d_1['条件'] = l_conditions
                    d_1['测试数据'] = d_cases['satisfied'][i]
                    d_1.update(d_tmp)
                    s_tmp= str(d_1)
                    s_tmp = s_tmp.replace("\\\\","\\")
                    if Configparser_PO.SWITCH("positiveResult") == "on":
                        Color_PO.outColor([{"31": s_tmp}])
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    caseTotal = caseTotal + 1
                    l_count.append(0)

            # 反向用例, N个数据
            if Configparser_PO.SWITCH("testNegative") == "on":
                for i in range(len(d_cases['notSatisfied'])):
                    # d_tmp = self.EFRB_run_n(v[0], ID)
                    d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][i], d_param)
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

    def _EFRB_run(self, d_cases_satisfied, d_param):

        # 公共测试用例

        # print(d_cases_satisfied)  # {'BMI': 24.0, '年龄': 18.1}
        # print(d_param)  # {'table': 'a_weight10_EFRB', 'ID': 1, 'f_conditions': 'BMI>=24 and 年龄>=18 and 年龄<65', '表注释': '评估因素规则库EFRB', 'l_conditions': ['BMI>=24', '年龄>=18', '年龄<65'], 'disease': '', 'categoryCode': '3'}

        d_tmp = {}


        # 参数
        # 获取f_code,f_age
        l_d_row = Sqlserver_PO_CHC5G.select("select f_category, f_categoryCode, f_ageType, f_code from %s where id= %s" % (self.tableEF, d_param['ID']))
        # print(l_d_row)
        d_tmp['人群分类'] = l_d_row[0]['f_category']
        d_tmp['categoryCode'] = l_d_row[0]['f_categoryCode']
        d_tmp['年龄类型'] = l_d_row[0]['f_ageType']
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']
        # d_tmp['条件'] = l_d_row[0]['f_conditions']


        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = self.WEIGHT_REPORT__ID
        d_tmp['身份证'] = Configparser_PO.FILE("testIdcard")


        # BMI
        if 'BMI' in d_cases_satisfied:
            varBMI = d_cases_satisfied['BMI']
        else:
            varBMI = 0

        # 年龄
        # print(d_tmp['人群分类编码'])
        if d_tmp['年龄类型'] == "int":
            if d_tmp['categoryCode'] == '1':
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

        # print(1027,d_param)
        if 'categoryCode' not in d_param:
            categoryCode = ''
        else:
            categoryCode = d_param['categoryCode']
        if 'disease' not in d_param:
            disease = ''
        else:
            disease = d_param['disease']


        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":'+ str(varAge) +',\\"ageFloat\\":'+ str(varAgeFloat) +',\\"ageMonth\\":'+ str(varAgeMonth) +',\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":' + str(varBMI) + ',\\"categoryCode\\":\\"' + str(categoryCode) + '\\",\\"disease\\":\\"' + str(disease) + '\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\":\\"' + str(d_tmp['身份证']) + '\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"' + str(varSex) + '\\",\\"sexCode\\":\\"' + str(varSexCode) + '\\",\\"weight\\":55,\\"weightReportId\\":' + str(self.WEIGHT_REPORT__ID) + '}"'

        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command

        if d_r['code'] == 200:

            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = %s" % (self.WEIGHT_REPORT__ID)
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            # 可能命中多条
            # print(l_d_RULE_CODE_actual)  # [{'RULE_CODE': 'TZ_RQFL004'}, {'RULE_CODE': 'TZ_AGE001'}, {'RULE_CODE': 'TZ_JWJB001'}]
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['f_code']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            return d_tmp

        else:
            print("872, error ", d_r['code'])
            sys.exit(0)
    def EFRB_run_p(self, d_cases_satisfied, d_param):
        d_tmp = self._EFRB_run(d_cases_satisfied, d_param)
        # if d_tmp['实际值'] == d_tmp['预期值']:
        if d_tmp['预期值'] in d_tmp['实际值']:
            d_tmp['result'] = 1
        else:
            d_tmp['result'] = 0
        return d_tmp
    def EFRB_run_n(self, d_cases_satisfied, d_param):
        d_tmp = self._EFRB_run(d_cases_satisfied, d_param)
        # if d_tmp['实际值'] == d_tmp['预期值']:
        if d_tmp['预期值'] in d_tmp['实际值']:
            d_tmp['result'] = 0
        else:
            d_tmp['result'] = 1
        return d_tmp
    def EFRB_run_disease(self, d_param):

        # 既往疾病
        # varDisease = 高血压
        # id = 46
        d_tmp = {}

        # print(1077, d_param)
        # print(1079,d_param)
        # if 'disease' in d_param:
        #     d_param['disease'] = d_param['disease']
        # else:
        #     d_param['disease'] = d_param['f_conditions']


        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_code from %s where ID= %s" % (self.tableEF, d_param['ID']))
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']

        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = self.WEIGHT_REPORT__ID
        d_tmp['身份证'] = Configparser_PO.FILE("testIdcard")

        varAge = 0
        varAgeFloat = 0.0
        varAgeMonth = 0
        varBMI = 10.1

        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":'+ str(varAge) +',\\"ageFloat\\":'+ str(varAgeFloat) +',\\"ageMonth\\":'+ str(varAgeMonth) +',\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":'+str(varBMI)+',\\"categoryCode\\":1,\\"disease\\":\\"'+str(d_param['disease'])+'\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\\":\\"' + str(d_tmp['身份证']) + '\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"\\",\\"sexCode\\":\\"1\\",\\"weight\\":55,\\"weightReportId\\":' + str(self.WEIGHT_REPORT__ID) + '}"'

        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command

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
                d_1['既往疾病'] = d_param['f_conditions']
                # d_1.update(d_tmp)
                # s_tmp = str(d_1)
                # s_tmp = s_tmp.replace("\\\\","\\")
                if Configparser_PO.SWITCH("positiveResult") == "on":
                    Color_PO.outColor([{"34": d_1}])
                Log_PO.logger.info(d_1)
                l_count.append(1)
            else:
                d_1['正向'] = 'error'
                d_1['既往疾病包含'] = d_param['f_conditions']
                d_1.update(d_tmp)
                s_tmp= str(d_1)
                s_tmp = s_tmp.replace("\\\\","\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库f_resut, f_updateDate
            d_result = {}
            d_result['table'] = d_param['table']
            d_result['ID'] = d_param['ID']
            if 0 not in l_count:
                d_result['result'] = "ok"
                s = "结果 => " + str(d_result)
                Color_PO.outColor([{"32": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result['result'], d_result['ID']))
            else:
                d_result['result'] = "error"
                s = "结果 => " + str(d_result)
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result['result'],d_result['ID']))
        else:
            print("1750, error ", d_r['code'])
            sys.exit(0)

    def EFRB_run_crowd(self, d_param):

        # 人群分类
        # varDisease = 高血压
        # id = 46
        d_tmp = {}

        # 参数
        l_d_row = Sqlserver_PO_CHC5G.select("select f_code from %s where ID= %s" % (self.tableEF, d_param['ID']))
        d_tmp['评估因素编码'] = l_d_row[0]['f_code']

        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = self.WEIGHT_REPORT__ID
        d_tmp['身份证'] = Configparser_PO.FILE("testIdcard")

        varAge = 0
        varAgeFloat = 0.0
        varAgeMonth = 0
        varBMI = 10.1

        if "sex" in d_param:
            if d_param['sex'] == "女":
                varSex = '女'
                varSexCode = 2
            else:
                varSex = '男'
                varSexCode = 1
        else:
            varSex = '男'
            varSexCode = 1


        # 跑接口
        command = 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":'+ str(varAge) +',\\"ageFloat\\":'+ str(varAgeFloat) +',\\"ageMonth\\":'+ str(varAgeMonth) +',\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":'+str(varBMI)+',\\"categoryCode\\":'+str(d_param['categoryCode'])+',\\"disease\\":\\"\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\\":\\"' + str(d_tmp['身份证']) + '\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"' + str(varSex) + '\\",\\"sexCode\\":' + str(varSexCode) + ',\\"weight\\":55,\\"weightReportId\\":' + str(self.WEIGHT_REPORT__ID) + '}"'

        if Configparser_PO.SWITCH("curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command

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
                d_1['人群分类'] = d_param['f_conditions']
                if Configparser_PO.SWITCH("positiveResult") == "on":
                    Color_PO.outColor([{"34": d_1}])
                Log_PO.logger.info(d_1)
                l_count.append(1)
            else:
                d_1['正向'] = 'error'
                d_1['人群分类'] = d_param['f_conditions']
                d_1.update(d_tmp)
                s_tmp = str(d_1)
                s_tmp = s_tmp.replace("\\\\", "\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库f_resut, f_updateDate
            d_result = {}
            d_result["table"] = d_param['table']
            d_result["ID"] = d_param['ID']
            if 0 not in l_count:
                d_result["result"] = "ok"
                s = "结果 => " + str(d_result)
                Color_PO.outColor([{"32": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result["result"], d_result["ID"]))
            else:
                d_result["result"] = "error"
                s = "结果 => " + str(d_result)
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC5G.execute("update %s set f_result = '%s', f_updateDate = GETDATE() where ID = %s" % (self.tableEF, d_result["result"], d_result["ID"]))
        else:
            print("175110, error ", d_r['code'])
            sys.exit(0)


    def _EFRB_result(self, d_param):

        # print(783, d_param)  # {'table': 'a_weight10_EFRB', 'ID': 1, 'f_conditions': 'BMI>=24 and 年龄>=18 and 年龄<65', '表注释': '评估因素规则库EFRB', 'l_conditions': ['BMI>=24', '年龄>=18', '年龄<65'], 'disease': '', 'categoryCode': '3', 'l_count': [1, 1, 1, 1], 'caseTotal': 4}

        d_result = {}
        d_result['table'] = d_param['table']
        d_result['ID'] = d_param['ID']
        if 0 not in d_param['l_count']:
            d_result['result'] = 'ok'
            s = "结果 => " + str(d_result)
            Color_PO.outColor([{"32": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableEF, d_param['caseTotal'], d_param['ID']))
        else:
            d_result['result'] = 'error'
            s = "结果 => " + str(d_result)
            Color_PO.outColor([{"31": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_caseTotal=%s where ID = %s" % (self.tableEF, d_param['caseTotal'], d_param['ID']))

