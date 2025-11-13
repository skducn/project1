# coding=utf-8
# ***************************************************************
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
import subprocess
import json
warnings.simplefilter("ignore")
# *****************************************************************
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO_CHC = SqlserverPO(
    Configparser_PO.DB("host"),
    Configparser_PO.DB("user"),
    Configparser_PO.DB("password"),
    Configparser_PO.DB("database2")
)

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
        self.tableEFRB = Configparser_PO.DB("tableEFRB")

        # 检查身份证是否存在, WEIGHT_REPORT(体重报告记录表)
        # 和QYYH中都必须要有此身份证，且在WEIGHT_REPORT表中获取ID
        self.IDCARD, self.WEIGHT_REPORT__ID = self.getIdcard()


    def getIdcard(self):
        # 自动获取身份证号，从QYYH和WEIGHT_REPORT中匹配相同身份证，同时获取WEIGHT_REPORT（ID）

        l_d_1 = Sqlserver_PO_CHC.select("select SFZH from QYYH ")
        l_d_2 = Sqlserver_PO_CHC.select("select ID_CARD from WEIGHT_REPORT ")
        set_QYYH = {item['SFZH'] for item in l_d_1 if item['SFZH'] not in ('', None, 0)}
        set_WEIGHT_REPORT = {item['ID_CARD'] for item in l_d_2 if item['ID_CARD'] not in ('', None, 0)}
        set_ = set_QYYH & set_WEIGHT_REPORT
        if set_:  # 如果交集非空
            IDCARD = list(set_)[0]
            l_d_2 = Sqlserver_PO_CHC.select("select ID from WEIGHT_REPORT where ID_CARD='%s'" % (IDCARD))
            ID = l_d_2[0]['ID']
            return IDCARD, ID
        else:  # 如果交集为空（即 set()）
            print("error, QYYH(SFZH字段) 与 WEIGHT_REPORT(ID_CARD字段)中没有相同的身份证号!")
            sys.exit(0)

    def convert_conditions(self, conditions):
        """列表转字符串"""
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
        """excel文件导入db"""
        try:
            varSheet = "EFRB"
            varTable = self.tableEFRB

            # 1, db中删除已有的表
            Sqlserver_PO_CHC.execute("drop table if exists " + varTable)

            # 读取 Excel 文件
            df = pd.read_excel(Configparser_PO.FILE("case"), sheet_name=varSheet)
            df = df.sort_index()  # 按行索引排序，保持Excel原有顺序
            df = df.dropna(how="all")  # 移除全空行

            # 手动设置字段类型
            # df['conditions'] = df['conditions'].astype(str)  # 改为字符串类型

            # 2, excel导入db
            Sqlserver_PO_CHC.df2db(df, varTable)

            # 3, 设置表注释
            Sqlserver_PO_CHC.setTableComment(varTable, '体重管理1.0_评估因素规则库_自动化测试')

            # 4， 替换换行符为空格
            Sqlserver_PO_CHC.execute(
                "UPDATE %s SET conditions = REPLACE(REPLACE(conditions, CHAR(10), ' '), CHAR(13), ' ');" % (
                    varTable)
            )

            # 5, 设置字段类型与描述
            field_definitions = [
                ('result', 'nvarchar(10)', '测试结果'),
                ('updateDate', 'nvarchar(50)', '更新日期'),
                ('log', 'varchar(max)', '日志信息'),
                ('f_type', 'nvarchar(20)', '分类'),
                ('category', 'nvarchar(20)', '人群分类'),
                ('categoryCode', 'varchar(3)', '人群分类编码'),
                # ('categoryType', 'nvarchar(10)', '年龄类型'),
                ('ruleName', 'nvarchar(100)', '规则名称'),
                ('detail', 'nvarchar(999)', '评估规则详细描述'),
                ('conditions_original', 'nvarchar(max)', '评估因素判断规则_原始'),
                ('conditions', 'nvarchar(max)', '评估因素判断规则'),
                ('ER_code', 'varchar(50)', '评估规则编码'),
                ('ER_result', 'varchar(50)', '评估规则结果'),
                ('testCase', 'nvarchar(100)', '测试用例'),
                ('totalCase', 'int', '用例合计数'),
                ('errId', 'int', '错误id')
            ]

            for field_name, field_type, comment in field_definitions:
                Sqlserver_PO_CHC.setFieldTypeComment(varTable, field_name, field_type, comment)

            Sqlserver_PO_CHC.execute("ALTER TABLE %s ALTER COLUMN updateDate DATE;" % (varTable))

            # 6, 设置自增主键（最后）
            Sqlserver_PO_CHC.setIdentityPrimaryKey(varTable, "id")

        except Exception as e:
            raise e

    def EFRB(self, object=None, d_param={}):
        # 入口

        if object == None:
            # 执行所有规则
            self._EFRB_ALL()
        elif isinstance(object, list):
            # 执行连续规则, [起始，步长]
            self._EFRB_area(object, d_param)
        elif isinstance(object, dict):
            if 'id' in object:
                # 执行多条
                if isinstance(object['id'], list):
                    self._EFRB_multiple(object, d_param)
                else:
                    # 执行一条
                    # 判断id是否溢出
                    l_d_row = Sqlserver_PO_CHC.select("select * from %s" % (self.tableEFRB))
                    i_records = len(l_d_row)
                    if object['id'] > i_records or object['id'] <= 0:
                        # 异常退出
                        print("[Error] 输入的ID超出" + str(i_records) + "条范围！")
                        sys.exit(0)
                    else:
                        self._EFRB_one(object, d_param)
            elif 'ER_code' in object:
                # 执行多条
                if isinstance(object['ER_code'], list):
                    self._EFRB_multiple(object, d_param)
                else:
                    # 执行一条
                    self._EFRB_one(object, d_param)
            else:
                print("[Error] 参数中没有id或ER_code！")
                sys.exit(0)

        return self.WEIGHT_REPORT__ID

    def _EFRB_main(self, d_param):

        # 清洗清洗条件字符串,如去掉月，将大写>=替换为<=，将大写<=替换为<=，将大写>替换为<，将大写<替换为<，将大写<=替换为<=，将大写>=替换为>=，将大写<>替换为<>，
        conditions = self._clean_conditions(d_param['conditions'])
        # print(207, conditions) # (73<=年龄<79 and 17.1<=BMI and 性别=男) or (79<=年龄<84 and 17.2<=BMI and 性别=男)

        # 根据条件类型分发处理
        if '疾病' in conditions:
            self._handle_disease_condition(d_param, conditions)
        elif '人群分类' in conditions:
            self._handle_crowd_condition(d_param, conditions)
        elif "年龄" in conditions and "BMI" not in conditions:
            self._handle_age_only_condition(d_param, conditions)
        elif "or" in conditions:
            # (14≤年龄<14.5 and 22.3≤BMI and 性别=男) or (14.5≤年龄<15 and 22.6≤BMI and 性别=男)
            self._handle_or_condition(d_param, conditions)
        elif "and" in conditions and "or" not in conditions and "BMI" in conditions and "年龄" in conditions:
            # 'BMI>=24 and 年龄>=18 and 年龄<65'
            self._handle_age_bmi_condition(d_param, conditions)
        elif "and" not in conditions:
            self._handle_simple_condition(d_param, conditions)
        else:
            print("[not or & and ]")

    def _format_bmi_age_gender(self, l_one_rule):
        """格式化BMI，年龄，性别"""
        # l_value = ['7<=年龄<8', '13.9>BMI', '性别=男']

        # 拆分年龄
        l_one_rule_split = []
        for i in l_one_rule:
            if "BMI" in i or "年龄" in i:
                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                l_one_rule_split.extend(l_split_conditions)
            elif "性别" in i:
                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                l_one_rule_split.extend(l_split_conditions)
        # l_one_rule_split = ['年龄>=7', '年龄<8', '13.9>BMI', '性别=男']

        # 置换位置 -（左边指标，右边数据）
        l_one_rule_split_interconvert = []
        for i in l_one_rule_split:
            l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
            l_one_rule_split_interconvert.extend(l_simple_conditions)
        # print(l_one_rule_split_interconvert)  # ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']
        return l_one_rule_split_interconvert

    def _s_rule2l_rule(self, f_rule):
        # 将字符串转列表，解析包含or的规则
        # 如：(7<=年龄<8 and 13.9>BMI and 性别=男) or (8<=年龄<9 and 14.0>BMI and 性别=男)

        l_value = f_rule.split("or")
        l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
        l_value = [i.split("and") for i in l_value]
        l_l_rule = [[item.strip() for item in sublist] for sublist in l_value]
        return l_l_rule

    def _clean_conditions(self, conditions):
        """清洗条件字符串"""
        conditions = conditions.replace("月", '')
        conditions = conditions.replace('＞', '>').replace('＜', '<').replace('＝', '=')
        return conditions

    def _handle_disease_condition(self, d_param, conditions):
        """处理疾病条件"""
        d_param['disease'] = conditions
        self.EFRB_run_disease(d_param)

    def _handle_crowd_condition(self, d_param, conditions):
        """处理人群分类条件"""
        d_param['categoryCode'] = conditions.split("=")[1]
        self.EFRB_run_crowd(d_param)

    def _generate_matched_data(self, l_interconvert_conditions, type):
        # 生成测试数据
        # l_interconvert_conditions = ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']
        if type == "int":
            for i in l_interconvert_conditions:
                if ('>=' in i or '<=' in i or '=' in i) and ('年龄' in i or 'BMI' in i or '性别' in i):
                    return BmiAgeSex_PO.int(l_interconvert_conditions)
            return BmiAgeSex_PO.int(l_interconvert_conditions)
        else:
            for i in l_interconvert_conditions:
                if ('>=' in i or '<=' in i or '=' in i) and ('年龄' in i or 'BMI' in i or '性别' in i):
                    return BmiAgeSex_PO.float(l_interconvert_conditions)
            return BmiAgeSex_PO.float(l_interconvert_conditions)

    def _handle_age_only_condition(self, d_param, conditions):
        """处理只有年龄的条件"""
        # 元素拆分
        l_conditions = []
        l_simple_conditions = Age_PO.splitMode(conditions)
        l_conditions.extend(l_simple_conditions)

        # 转换位置
        l_conditions_interconver = []
        for i in l_conditions:
            l_simple_conditions = Age_PO.interconvertMode(i)
            l_conditions_interconver.extend(l_simple_conditions)

        # 生成随机数据
        d_cases = Age_PO.generate_all_cases(l_conditions_interconver)
        if Configparser_PO.SWITCH("print_testData") == "on":
            print("生成测试数据集 =>", d_cases)
        Log_PO.logger.info("生成测试数据集 => " + str(d_cases))

        # 执行
        self.EFRB_case(d_cases, d_param)

    def _handle_or_condition(self, d_param, conditions):
        # print(333, d_param)  # 333 {'id': 28, 'ER_code': 'TZ_STZB017', 'conditions':'(60月<= 年龄<63月 and 13.2<= BMI<16.7 and 性别=男) or (63月<= 年龄<66月 and 13.1<= BMI<16.7 and 性别=男)
        # 包含or的复合条件
        # 如：(73月<=年龄<79月 and 17.1<=BMI and 性别=男) or (79月<=年龄＜84月 and 17.2<=BMI and 性别=男) or (73月<=年龄＜79月 and 16.6<=BMI and 性别=女) or (79月<=年龄＜84月 and 16.7<=BMI and 性别=女)
        # print(278)
        l_d_ = Sqlserver_PO_CHC.select("select category, categoryCode, conditions from %s where id=%s" % (self.tableEFRB, d_param['id']))
        category = l_d_[0]['category']
        categoryCode = int(l_d_[0]['categoryCode'])
        s_rule = l_d_[0]['conditions']
        # print("原始 =>", s_rule)

        # 格式化数据1, 将 f_value 转列表
        l_l_rule = self._s_rule2l_rule(s_rule)
        # print("格式化1 =>",  l_l_rule)  #  [['7<=年龄<8', '13.9>BMI', '性别=男'], ['8<=年龄<9', '14.0>BMI', '性别=男']。。。
        # 格式化数据2, 最终
        l_l_rule2 = []
        for lln, l_value in enumerate(l_l_rule):
            # 格式化BMI，年龄，性别
            l_one_rule_split_interconvert = self._format_bmi_age_gender(l_value)
            # print(l_one_rule_split_interconvert)  # ['年龄>=7', '年龄<8', '13.9>BMI', '性别=男']
            l_l_rule2.append(l_one_rule_split_interconvert)
        # print("格式化2 =>",  l_l_rule2)  # [['年龄>=7', '年龄<8', 'BMI<13.9', '性别=男'], ['年龄>=8', '年龄<9', 'BMI<14.0', '性别=男'], ...

        l_log = []
        l_count = []
        sum = 0

        # todo 正向p（单组）
        # 如：(7<= 年龄 < 8 and 13.9>BMI and 性别 = 男)
        if Configparser_PO.SWITCH("run_p") == "on":
            qty_l_l_rule2 = len(l_l_rule2)
            # print(l_l_rule2)  # [['年龄>=60', '年龄<63', 'BMI>=13.2', 'BMI<16.7', '性别=男'], ['年龄>=63', '年龄<66', 'BMI>=13.1', 'BMI<16.7', '性别=男'],

            # 对单组条件（['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']）生成正向测试数据
            for index, l_rule in enumerate(l_l_rule2):
                if Configparser_PO.SWITCH("only_print_error") == "off":
                    print("单组" + str(index + 1) + "/" + str(qty_l_l_rule2) + " => " + str(l_rule))

                # 儿童
                if categoryCode == 1:
                    d_satisfied = self._generate_matched_data(l_rule, "int")  # 生成正向有效数据
                else:
                    d_satisfied = self._generate_matched_data(l_rule, "float")  # 生成正向有效数据
                if Configparser_PO.SWITCH("print_testData") == "on":
                    # l_d_case = d_satisfied
                    print("生成正向有效数据 =>", d_satisfied)  # {'年龄': 6.5, 'BMI': 15.0, '性别': '男'},

                # 跑正向
                Numerator = index + 1
                d_result = self.EFRB_case_or("p", d_satisfied, l_rule, Numerator, d_param)
                # print(36888, d_satisfied)  # {'satisfied': [{'年龄': 60, 'BMI': 16.6, '性别': '男'}, {'年龄': 60, 'BMI': 13.2, '性别': '男'},
                # print(36889, l_rule)  # ['年龄>=60', '年龄<63', 'BMI>=13.2', 'BMI<16.7', '性别=男']
                # print(4545, d_param) # {'id': 28, 'ER_code': 'TZ_STZB017', 'conditions': '(60月<= 年龄<63月 and 13.2<= BMI<16.7 and 性别=男) or (63月<= 年龄<66月 and 13.1<= BMI<16.7 and 性别=男) or (66月<= 年龄<69月 and 13.1<= BMI<16.8 and 性别=男) or (69月<= 年龄<72月 and 13.1<= BMI<16.9 and 性别=男) or (年龄=72月 and 13.1<= BMI<16.9 and 性别=男) or (60月<= 年龄<63月 and 12.9<= BMI<16.4 and 性别=女) or (63月<= 年龄<66月 and 12.8<= BMI<16.4 and 性别=女) or (66月<= 年龄<69月 and 12.8<= BMI<16.5 and 性别=女) or (69月<= 年龄<72月 and 12.8<= BMI<16.5 and 性别=女) or (年龄= 72月 and 12.8<= BMI<16.5 and 性别=女)', 'IDCARD': '310101193012210813'}


                # print(325, d_result)  # 325 {'caseTotal': 4, 'count': 1}
                l_count.append(d_result['count'])
                sum = sum + d_result['caseTotal']



        # todo 反向n（所有条件）
        if Configparser_PO.SWITCH("run_n") == "on":
            d_cases_n = {}
            if categoryCode == 3 or categoryCode == 4:
                # 普通人群和老年人，只需要处理bmi
                d_cases_n = Bmi_PO.generate_all_cases(l_l_rule2[0])  # {'satisfied': [{'BMI': 14.1}], 'notSatisfied': [{'BMI': 42.1}]}
                l_d_case = d_cases_n['notSatisfied']
            else:
                # 儿童和学生，需要处理年龄和bmi
                if categoryCode == 1:
                    # 儿童
                    d_cases_n = self._generate_unmatched_data_children(l_l_rule2)  # 生成反向不匹配数据
                    l_d_case = d_cases_n['notSatisfied']
                    # # 特殊处理，如果儿童且肥胖，不生成等于0或大于84的值。
                    # if weightStatusCode == 4:
                    #     l_d_case = [d for d in l_d_case if d['年龄'] >= 1 and d['年龄'] < 85]
                elif categoryCode == 2:
                    # 学生
                    d_cases_n = self._generate_unmatched_data_student(l_l_rule2)  # 生成反向不匹配数据
                    l_d_case = d_cases_n['notSatisfied']
                    # # 特殊处理，如果是学生且肥胖，不生成小于7的值。
                    # if weightStatusCode == 4:
                    #     l_d_case = [d for d in l_d_case if d['年龄'] >= 7]

            if Configparser_PO.SWITCH("only_print_error") == "off":
                print("条件 => " + str(l_l_rule2))
                print("反向无效数据 =>", l_d_case)  # [{'年龄': 6.5, 'BMI': 15.0, '性别': '男'}, {'年龄': 6.5, 'BMI': 15.0, '性别': '女'},

            d_result = self.EFRB_case_or("n", d_cases_n,  l_l_rule2, 1, d_param)
            # d_cases = {'notSatisfied': [{'年龄': 73.0, 'BMI': 17.1, '性别': '男'}, {'年龄': 73.0, 'BMI': 27.2, '性别': '男'}...
            # l_interconvert_conditions = ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']
            # d_param = {'id': 59, 'ER_code': 'TZ_STZB046',
            # 'conditions': '(73月<=年龄<79月 and 17.1<=BMI and 性别=男) or (79月<=年龄＜84月 and 17.2<=BMI and 性别=男) or (73月<=年龄＜79月 and 16.6<=BMI and 性别=女) or (79月<=年龄＜84月 and 16.7<=BMI and 性别=女)',
            # 'IDCARD': '310101193012210813'}

            # print(325, d_result)  # 325 {'caseTotal': 4, 'count': 1}
            l_count.append(d_result['count'])
            sum = sum + d_result['caseTotal']

        # 更新记录
        d_param['l_count'] = l_count
        d_param['caseTotal'] = sum
        self._EFRB_result(d_param)


    def _parse_or_conditions(self, conditions):
        """解析包含or的条件"""
        l_value = conditions.split("or")
        l_value = [i.replace("(", '').replace(")", '').strip() for i in l_value]
        l_value = [i.split("and") for i in l_value]
        return [[item.strip() for item in sublist] for sublist in l_value]

    def _format_conditions(self, l_value):
        """格式化条件"""
        l_conditions = []
        for i in l_value:
            if "BMI" in i or "年龄" in i:
                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                l_conditions.extend(l_split_conditions)
            elif "性别" in i:
                l_split_conditions = BmiAgeSex_PO.splitMode(i)
                l_conditions.extend(l_split_conditions)
        return l_conditions

    def generate_unmatched_cases(self, conditions):
        """
        生成不满足指定条件的年龄、BMI、性别组合示例（年龄取整数，BMI保留1位小数）

        参数:
            conditions: 条件列表，每个元素为一个条件子列表
                        格式如: [['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男'], ...]

        返回:
            list: 不满足条件的组合示例列表
        """
        # 解析条件中的关键参数
        age_ranges = set()
        bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

        for cond in conditions:
            age_min = None
            age_max = None
            bmi_min = None
            gender = None

            for c in cond:
                if c.startswith('年龄>='):
                    age_min = float(c.split('>=')[1])
                elif c.startswith('年龄<'):
                    age_max = float(c.split('<')[1])
                elif c.startswith('BMI>='):
                    bmi_min = float(c.split('>=')[1])
                elif c.startswith('性别='):
                    gender = c.split('=')[1]

            if all([age_min, age_max, bmi_min, gender]):
                age_range = (age_min, age_max)
                age_ranges.add(age_range)
                bmi_thresholds[gender][age_range] = bmi_min

        # 生成不满足条件的示例组合
        unmatched = []

        # 1. 年龄低于最小范围（取整数）
        min_age = min(r[0] for r in age_ranges)
        test_age = int(min_age - 1)  # 年龄取整数且低于最小范围
        sample_bmi = 18.5  # 代表性BMI值
        unmatched.append({
            '年龄': test_age,
            'BMI': round(sample_bmi, 1),
            '性别': '男'
        })
        unmatched.append({
            '年龄': test_age,
            'BMI': round(sample_bmi, 1),
            '性别': '女'
        })

        # 2. 年龄高于最大范围（取整数）
        max_age = max(r[1] for r in age_ranges)
        test_age = int(max_age)  # 年龄取整数且高于最大范围
        unmatched.append({
            '年龄': test_age,
            'BMI': round(sample_bmi, 1),
            '性别': '男'
        })
        unmatched.append({
            '年龄': test_age,
            'BMI': round(sample_bmi, 1),
            '性别': '女'
        })

        # 3. 年龄在范围内但男性BMI不达标（年龄取整数中间值）
        for (age_min, age_max), bmi_min in bmi_thresholds['男'].items():
            # 取年龄区间内的整数中间值
            test_age = int((age_min + age_max) // 2)
            # BMI值设为阈值减0.1（确保不满足条件且保留1位小数）
            test_bmi = round(bmi_min - 0.1, 1)
            unmatched.append({
                '年龄': test_age,
                'BMI': test_bmi,
                '性别': '男'
            })

        # 4. 年龄在范围内但女性BMI不达标（年龄取整数中间值）
        for (age_min, age_max), bmi_min in bmi_thresholds['女'].items():
            # 取年龄区间内的整数中间值
            test_age = int((age_min + age_max) // 2)
            # BMI值设为阈值减0.1（确保不满足条件且保留1位小数）
            test_bmi = round(bmi_min - 0.1, 1)
            unmatched.append({
                '年龄': test_age,
                'BMI': test_bmi,
                '性别': '女'
            })

        return unmatched

    def _generate_unmatched_data_children(self, l_l_rule2):
        """
        生成不满足指定条件的年龄、BMI、性别组合示例（针对儿童，年龄使用整数）

        参数:
            l_l_rule2: 条件列表，每个元素为一个条件子列表
                        格式如: [['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ...]

        返回:
            dict: 包含满足和不满足条件的组合示例字典
        """
        d_cases_n = {}

        # 解析条件中的关键参数
        age_values = set()  # 存储具体的年龄值
        age_ranges = set()  # 存储年龄范围
        bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

        for cond in l_l_rule2:
            age_value = None
            age_min = None
            age_max = None
            bmi_min = None
            bmi_max = None
            gender = None

            for c in cond:
                c = c.replace("月", "")
                if c.startswith('年龄='):
                    age_value = int(float(c.split('=')[1]))  # 转换为整数
                    age_values.add(age_value)
                elif c.startswith('年龄>='):
                    age_min = int(float(c.split('>=')[1]))  # 转换为整数
                elif c.startswith('年龄<'):
                    age_max = int(float(c.split('<')[1]))  # 转换为整数
                elif c.startswith('BMI>='):
                    bmi_min = float(c.split('>=')[1])
                elif c.startswith('BMI<='):
                    bmi_max = float(c.split('<=')[1])
                elif c.startswith('BMI<'):
                    bmi_max = float(c.split('<')[1])
                elif c.startswith('性别='):
                    gender = c.split('=')[1]

            # 处理具体年龄值的情况
            if age_value is not None and gender is not None:
                bmi_range = {}
                if bmi_min is not None:
                    bmi_range['min'] = bmi_min
                if bmi_max is not None:
                    bmi_range['max'] = bmi_max
                if bmi_range:
                    bmi_thresholds[gender][age_value] = bmi_range
                    age_ranges.add((age_value, age_value))  # 将具体值转换为范围

            # 处理年龄范围的情况
            elif all(x is not None for x in [age_min, age_max, gender]):
                age_range = (age_min, age_max)
                age_ranges.add(age_range)
                bmi_range = {}
                if bmi_min is not None:
                    bmi_range['min'] = bmi_min
                if bmi_max is not None:
                    bmi_range['max'] = bmi_max
                if bmi_range:
                    bmi_thresholds[gender][age_range] = bmi_range

        # 如果没有解析到有效的条件，则返回空列表
        if not age_ranges:
            return []

        # 生成不满足条件的示例组合
        unmatched = []

        # 1. 年龄不在任何有效范围内（使用整数）
        if age_ranges:
            min_age = min(r[0] for r in age_ranges)
            max_age = max(r[1] for r in age_ranges)

            # 年龄低于最小范围（使用整数）
            test_age = min_age - 1
            sample_bmi = 15.0
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '男'
            })
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '女'
            })

            # 年龄高于最大范围（使用整数）
            test_age = max_age + 1
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '男'
            })
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '女'
            })

        # 2. 年龄在范围内但BMI不满足条件
        for gender in ['男', '女']:
            for age_key, bmi_range in bmi_thresholds[gender].items():
                # 确定测试年龄（使用整数）
                if isinstance(age_key, tuple):  # 年龄范围
                    test_age = int((age_key[0] + age_key[1]) // 2)  # 使用整数
                else:  # 具体年龄值
                    test_age = int(age_key)  # 使用整数

                # 生成不满足BMI条件的值
                if 'min' in bmi_range and 'max' in bmi_range:
                    # 既有最小值又有最大值，生成范围外的值
                    test_bmi_below = round(bmi_range['min'] - 0.1, 1)
                    test_bmi_above = round(bmi_range['max'], 1)  # 等于最大值时不满足条件
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi_below,
                        '性别': gender
                    })
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi_above,
                        '性别': gender
                    })
                elif 'min' in bmi_range:
                    # 只有最小值，生成小于最小值的BMI
                    test_bmi = round(bmi_range['min'] - 0.1, 1)
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi,
                        '性别': gender
                    })
                elif 'max' in bmi_range:
                    # 只有最大值，生成大于等于最大值的BMI
                    test_bmi = round(bmi_range['max'], 1)
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi,
                        '性别': gender
                    })

        d_cases_n['satisfied'] = []
        d_cases_n['notSatisfied'] = unmatched
        return d_cases_n
    def _generate_unmatched_data_student(self, l_l_rule2):
        """
        生成不满足指定条件的年龄、BMI、性别组合示例（年龄保留1位小数，BMI保留1位小数）

        参数:
            l_l_rule2: 条件列表，每个元素为一个条件子列表
                        格式如: [['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ...]

        返回:
            list: 不满足条件的组合示例列表
        """
        d_cases_n = {}

        # 解析条件中的关键参数
        age_values = set()  # 存储具体的年龄值
        age_ranges = set()  # 存储年龄范围
        bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

        for cond in l_l_rule2:
            age_value = None
            age_min = None
            age_max = None
            bmi_min = None
            bmi_max = None
            gender = None

            for c in cond:
                c = c.replace("月", "")
                if c.startswith('年龄='):
                    age_value = float(c.split('=')[1])
                    age_values.add(age_value)
                elif c.startswith('年龄>='):
                    age_min = float(c.split('>=')[1])
                elif c.startswith('年龄<'):
                    age_max = float(c.split('<')[1])
                elif c.startswith('BMI>='):
                    bmi_min = float(c.split('>=')[1])
                elif c.startswith('BMI<='):
                    bmi_max = float(c.split('<=')[1])
                elif c.startswith('BMI<'):
                    bmi_max = float(c.split('<')[1])
                elif c.startswith('性别='):
                    gender = c.split('=')[1]

            # 处理具体年龄值的情况
            if age_value is not None and gender is not None:
                bmi_range = {}
                if bmi_min is not None:
                    bmi_range['min'] = bmi_min
                if bmi_max is not None:
                    bmi_range['max'] = bmi_max
                if bmi_range:
                    bmi_thresholds[gender][age_value] = bmi_range
                    age_ranges.add((age_value, age_value))  # 将具体值转换为范围

            # 处理年龄范围的情况
            elif all(x is not None for x in [age_min, age_max, gender]):
                age_range = (age_min, age_max)
                age_ranges.add(age_range)
                bmi_range = {}
                if bmi_min is not None:
                    bmi_range['min'] = bmi_min
                if bmi_max is not None:
                    bmi_range['max'] = bmi_max
                if bmi_range:
                    bmi_thresholds[gender][age_range] = bmi_range

        # 如果没有解析到有效的条件，则返回空列表
        if not age_ranges:
            return []

        # 生成不满足条件的示例组合
        unmatched = []

        # 1. 年龄不在任何有效范围内
        if age_ranges:
            min_age = min(r[0] for r in age_ranges)
            max_age = max(r[1] for r in age_ranges)

            # 年龄低于最小范围
            test_age = round(min_age - 0.5, 1)
            sample_bmi = 15.0
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '男'
            })
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '女'
            })

            # 年龄高于最大范围
            test_age = round(max_age + 0.5, 1)
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '男'
            })
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '女'
            })

        # 2. 年龄在范围内但BMI不满足条件
        for gender in ['男', '女']:
            for age_key, bmi_range in bmi_thresholds[gender].items():
                # 确定测试年龄
                if isinstance(age_key, tuple):  # 年龄范围
                    test_age = round((age_key[0] + age_key[1]) / 2, 1)
                else:  # 具体年龄值
                    test_age = round(age_key, 1)

                # 生成不满足BMI条件的值
                if 'min' in bmi_range and 'max' in bmi_range:
                    # 既有最小值又有最大值，生成范围外的值
                    test_bmi_below = round(bmi_range['min'] - 0.1, 1)
                    test_bmi_above = round(bmi_range['max'], 1)  # 等于最大值时不满足条件
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi_below,
                        '性别': gender
                    })
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi_above,
                        '性别': gender
                    })
                elif 'min' in bmi_range:
                    # 只有最小值，生成小于最小值的BMI
                    test_bmi = round(bmi_range['min'] - 0.1, 1)
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi,
                        '性别': gender
                    })
                elif 'max' in bmi_range:
                    # 只有最大值，生成大于等于最大值的BMI
                    test_bmi = round(bmi_range['max'], 1)
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi,
                        '性别': gender
                    })

        d_cases_n['satisfied'] = []
        d_cases_n['notSatisfied'] = unmatched
        return d_cases_n
    def generate_unmatched_cases2(self, conditions):
        """
        生成不满足指定条件的年龄、BMI、性别组合示例（年龄保留1位小数，BMI保留1位小数）

        参数:
            conditions: 条件列表，每个元素为一个条件子列表
                        格式如: [['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ...]

        返回:
            list: 不满足条件的组合示例列表
        """
        # 解析条件中的关键参数
        age_values = set()  # 存储具体的年龄值
        age_ranges = set()  # 存储年龄范围
        bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

        for cond in conditions:
            age_value = None
            age_min = None
            age_max = None
            bmi_min = None
            bmi_max = None
            gender = None

            for c in cond:
                if c.startswith('年龄='):
                    age_value = float(c.split('=')[1])
                    age_values.add(age_value)
                elif c.startswith('年龄>='):
                    age_min = float(c.split('>=')[1])
                elif c.startswith('年龄<'):
                    age_max = float(c.split('<')[1])
                elif c.startswith('BMI>='):
                    bmi_min = float(c.split('>=')[1])
                elif c.startswith('BMI<='):
                    bmi_max = float(c.split('<=')[1])
                elif c.startswith('BMI<'):
                    bmi_max = float(c.split('<')[1])
                elif c.startswith('性别='):
                    gender = c.split('=')[1]

            # 处理具体年龄值的情况
            if age_value is not None and gender is not None:
                bmi_range = {}
                if bmi_min is not None:
                    bmi_range['min'] = bmi_min
                if bmi_max is not None:
                    bmi_range['max'] = bmi_max
                if bmi_range:
                    bmi_thresholds[gender][age_value] = bmi_range
                    age_ranges.add((age_value, age_value))  # 将具体值转换为范围

            # 处理年龄范围的情况
            elif all(x is not None for x in [age_min, age_max, gender]):
                age_range = (age_min, age_max)
                age_ranges.add(age_range)
                bmi_range = {}
                if bmi_min is not None:
                    bmi_range['min'] = bmi_min
                if bmi_max is not None:
                    bmi_range['max'] = bmi_max
                if bmi_range:
                    bmi_thresholds[gender][age_range] = bmi_range

        # 如果没有解析到有效的条件，则返回空列表
        if not age_ranges:
            return []

        # 生成不满足条件的示例组合
        unmatched = []

        # 1. 年龄不在任何有效范围内
        if age_ranges:
            min_age = min(r[0] for r in age_ranges)
            max_age = max(r[1] for r in age_ranges)

            # 年龄低于最小范围
            test_age = round(min_age - 0.5, 1)
            sample_bmi = 15.0
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '男'
            })
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '女'
            })

            # 年龄高于最大范围
            test_age = round(max_age + 0.5, 1)
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '男'
            })
            unmatched.append({
                '年龄': test_age,
                'BMI': round(sample_bmi, 1),
                '性别': '女'
            })

        # 2. 年龄在范围内但BMI不满足条件
        for gender in ['男', '女']:
            for age_key, bmi_range in bmi_thresholds[gender].items():
                # 确定测试年龄
                if isinstance(age_key, tuple):  # 年龄范围
                    test_age = round((age_key[0] + age_key[1]) / 2, 1)
                else:  # 具体年龄值
                    test_age = round(age_key, 1)

                # 生成不满足BMI条件的值
                if 'min' in bmi_range and 'max' in bmi_range:
                    # 既有最小值又有最大值，生成范围外的值
                    test_bmi_below = round(bmi_range['min'] - 0.1, 1)
                    test_bmi_above = round(bmi_range['max'], 1)  # 等于最大值时不满足条件
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi_below,
                        '性别': gender
                    })
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi_above,
                        '性别': gender
                    })
                elif 'min' in bmi_range:
                    # 只有最小值，生成小于最小值的BMI
                    test_bmi = round(bmi_range['min'] - 0.1, 1)
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi,
                        '性别': gender
                    })
                elif 'max' in bmi_range:
                    # 只有最大值，生成大于等于最大值的BMI
                    test_bmi = round(bmi_range['max'], 1)
                    unmatched.append({
                        '年龄': test_age,
                        'BMI': test_bmi,
                        '性别': gender
                    })

        # # 3. 性别不匹配的情况
        # if age_values:
        #     sample_age = list(age_values)[0]
        #     sample_bmi = 15.0
        #     unmatched.append({
        #         '年龄': round(sample_age, 1),
        #         'BMI': round(sample_bmi, 1),
        #         '性别': '未知'
        #     })

        return unmatched



    def _generate_test_data(self, l_interconvert_conditions):
        """生成测试数据"""
        # l_interconvert_conditions = ['年龄>=73', '年龄<79', 'BMI>=17.1', '性别=男']
        for i in l_interconvert_conditions:
            # if ('>=' in i or '<=' in i) and ('年龄' in i or 'BMI' in i):
            if ('>=' in i or '<=' in i or '=' in i) and ('年龄' in i or 'BMI' in i or '性别' in i):
                return BmiAgeSex_PO.main(l_interconvert_conditions)
        return BmiAgeSex_PO.main(l_interconvert_conditions)

    def _handle_age_bmi_condition(self, d_param, conditions):
        # 年龄,BMI组合条件
        # 'BMI>=24 and 年龄>=18 and 年龄<65'

        # 字符串转换成列表
        l_conditions = conditions.split("and")
        l_conditions = [i.strip() for i in l_conditions]

        # 元素拆分
        l_conditions_split = []
        for i in l_conditions:
            l_simple_conditions = BmiAgeSex_PO.splitMode(i)
            l_conditions_split.extend(l_simple_conditions)

        # 转换位置
        l_conditions_interconver = []
        for i in l_conditions_split:
            l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
            l_conditions_interconver.extend(l_simple_conditions)

        # 生成测试数据
        d_cases = BmiAge_PO.main(l_conditions_interconver)
        if Configparser_PO.SWITCH("print_testData") == "on":
            print("生成测试数据集 =>", d_cases)
        Log_PO.logger.info("生成测试数据集 => " + str(d_cases))

        # 测试数据
        d_param['l_conditions'] = l_conditions
        self.EFRB_case(d_cases, d_param)

    def _handle_simple_condition(self, d_param, conditions):
        """处理简单条件"""
        l_conditions = []
        # 拆分
        l_simple_conditions = Bmi_PO.splitMode(conditions)
        l_conditions.extend(l_simple_conditions)

        # 转换位置
        l_3_value = []
        for i in l_conditions:
            l_simple_conditions = Bmi_PO.interconvertMode(i)
            l_3_value.extend(l_simple_conditions)

        # 生成随机数据
        d_cases = Age_PO.generate_all_cases(l_3_value)
        if Configparser_PO.SWITCH("print_testData") == "on":
            print("生成测试数据集 =>", d_cases)
        Log_PO.logger.info("生成测试数据集 => " + str(d_cases))

        # 处理测试用例
        d_param['l_conditions'] = l_conditions
        self.EFRB_case(d_cases, d_param)

    def _EFRB_ALL(self):
        """测试所有规则"""
        l_d_row = Sqlserver_PO_CHC.select("select id, category, conditions, ER_code from %s" % (self.tableEFRB))

        for row in l_d_row:
            d_param = {
                'ER_code': row['ER_code'],
                'id': row['id'],
                'category': row['category'],
                'conditions': row['conditions'],
                'IDCARD': self.IDCARD
            }

            s = "评估因素规则库_EFRB(" + self.tableEFRB + ") => " + str(d_param)
            Color_PO.outColor([{"35": s}])
            Log_PO.logger.info(s)

            self._EFRB_main(d_param)


    def _EFRB_area(self, l_, d_param):
        # l_= [起始，步长]
        # 执行多条(区间id)，如：{'id': [1, 3]} ,表示执行1，2，3 三条记录
        # 执行多条(区间ER_code)，如：{'ER_code': ['TZ_STZB046', 'TZ_STZB047']}

        # if 'ER_code' in d_:
        #     # # 匹配字母部分（非数字）和数字部分
        #     # match = re.match(r'([^\d]+)(\d+)', d_['ER_code'][0])
        #     # if match:
        #     #     prefix = match.group(1)  # 字母部分
        #     #     ER_code0 = int(match.group(2))  # 数字部分
        #     #
        #     # match = re.match(r'([^\d]+)(\d+)', d_['ER_code'][1])
        #     # if match:
        #     #     prefix = match.group(1)  # 字母部分
        #     #     ER_code1 = int(match.group(2))  # 数字部分
        #     #
        #     # if int(ER_code0) < 1 or int(ER_code0) > int(ER_code1) :
        #     #     print("[Error] 请输入正确的ER_code区间!")
        #     #     sys.exit(0)
        #     #
        #     # for ER_code in list(range(int(ER_code0), int(ER_code1) + 1)):
        #     #     if ER_code < 10:
        #     #         ER_code = prefix + "00" + str(ER_code)
        #     #     elif ER_code < 100:
        #     #         ER_code = prefix + "0" + str(ER_code)
        #     #     else:
        #     #         ER_code = prefix + str(ER_code)
        #
        #     # 获取每行测试数据
        #     for ER_code in d_['ER_code']:
        #         l_d_row = Sqlserver_PO_CHC.select("select id, category, conditions, ER_code from %s where ER_code='%s'" % (self.tableEFRB, ER_code))
        #         self.__EFRB_one(l_d_row, d_param)

        # 执行多条(区间id)，如：{'id': [1, 3]} ,表示执行1，2，3 三条记录
        id1 = l_[0]
        step = l_[1]
        id2 = id1 + step

        l_d_row = Sqlserver_PO_CHC.select("select count(*) as qty from %s where id=%s" % (self.tableEFRB, id2))
        if l_d_row[0]['qty'] != 0:
            for id in list(range(id1, id2)):
                l_d_row = Sqlserver_PO_CHC.select(
                    "select id, category, conditions, ER_code from %s where id=%s" % (self.tableEFRB, id))
                self.__EFRB_one(l_d_row, d_param)
        else:
            Color_PO.outColor([{"31": "[Error] 参数：[id起始，步长]，id起始 + 步长溢出!"}])
            sys.exit(0)





    def _EFRB_multiple(self, d_, d_param):
        # 执行多条id 或 ER_code

        if 'ER_code' in d_:
            for ER_code in d_['ER_code']:
                l_d_row = Sqlserver_PO_CHC.select("select id, category, conditions, ER_code from %s where ER_code='%s'" % (self.tableEFRB, ER_code))
                self.__EFRB_one(l_d_row, d_param)
        if 'id' in d_:
            # 判断id是否溢出
            if d_['id'][0] < 1 or d_['id'][0] > d_['id'][1] :
                print("[Error] 请输入正确的id区间!")
                sys.exit(0)

            for id in d_['id']:
                l_d_row = Sqlserver_PO_CHC.select("select id, category, conditions, ER_code from %s where id=%s" % (self.tableEFRB, id))
                self.__EFRB_one(l_d_row, d_param)




    def __EFRB_one(self, l_d_row, d_param):
        # _EFRB_one内部调用

        # 输出测试概要
        d_tmp = {
            'ER_code': l_d_row[0]['ER_code'],
            'id': l_d_row[0]['id'],
            'category': l_d_row[0]['category'],
            'conditions': l_d_row[0]['conditions'],
            'IDCARD': self.IDCARD
        }
        d_tmp.update(d_param)
        # d_tmp = {'id': 59, 'ER_code': 'TZ_STZB046', 'conditions': '(73月<=年龄<79月 and 17.1<=BMI and 性别=男) or (79月<=年龄＜84月 and 17.2<=BMI and 性别=男) or (73月<=年龄＜79月 and 16.6<=BMI and 性别=女) or (79月<=年龄＜84月 and 16.7<=BMI and 性别=女)', 'IDCARD': '310101193012210813'}
        s = "评估因素规则库EFRB(" + self.tableEFRB + ") => " + str(d_tmp)
        Color_PO.outColor([{"35": s}])

        # 写入日志
        Log_PO.logger.info(s)

        # 执行main
        self._EFRB_main(d_tmp)
    def _EFRB_one(self, d_, d_param):
        # 执行一条(id)
        # d_ = {'id': 56}
        # d_ = {'ER_code': 'TZ_STZB047'}
        # d_ = {'id': 59, 'ER_code': 'TZ_STZB047'}

        if "id" in d_:
            # 获取数据
            l_d_row = Sqlserver_PO_CHC.select("select id, category, conditions, ER_code from %s where id=%s" % (self.tableEFRB, d_['id']))
            self.__EFRB_one(l_d_row, d_param)
        if 'ER_code' in d_:
            # 获取数据
            l_d_row = Sqlserver_PO_CHC.select("select id, category, conditions, ER_code from %s where ER_code='%s'" % (self.tableEFRB, d_['ER_code']))
            self.__EFRB_one(l_d_row, d_param)


    def EFRB_case(self, d_cases, d_param):
        """处理测试用例"""
        caseTotal = 0
        l_count = []

        # print(d_param) # {'id': 1, 'ER_code': 'TZ_STZB001', 'conditions': 'BMI>=24 and 年龄>=18 and 年龄<65', 'IDCARD': '310101193012210813', 'l_conditions': ['BMI>=24', '年龄>=18', '年龄<65']}

        if Configparser_PO.SWITCH("run_p") == "on":
            # 正向
            for case in d_cases['satisfied']:
                d_tmp = self.EFRB_run_p(case, d_param)
                # print(d_tmp)  # {'预期值': 'TZ_STZB001', '实际值': ['TZ_STZB001', 'TZ_MBTZ002'], 'sql__T_ASSESS_RULE_RECORD': 'select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 1952', 'i': 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":18.0,\\"ageFloat\\":0.0,\\"ageMonth\\":0,\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":24.0,\\"categoryCode\\":\\"\\",\\"disease\\":\\"\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\":\\"310101193012210813\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"男\\",\\"sexCode\\":\\"1\\",\\"weight\\":55,\\"weightReportId\\":1952}"'}
                # 命中
                if d_tmp['result'] == 1:
                    d_data_result = {
                        '正向': "ok",
                        '验证': case
                    }
                    if Configparser_PO.SWITCH("only_print_error") == "off":
                        Color_PO.outColor([{"34": d_data_result}])
                    Log_PO.logger.info(d_data_result)
                    l_count.append(1)
                else:
                    # 未命中
                    d_data_result = {
                        '正向': "error",
                        '验证': case
                    }
                    d_data_result.update(d_tmp)
                    s_tmp = str(d_data_result).replace("\\\\", "\\")
                    Color_PO.outColor([{"31": d_data_result}])
                    Log_PO.logger.info(s_tmp)
                    l_count.append(0)
                caseTotal += 1


        if Configparser_PO.SWITCH("run_n") == "on":
            # 反向
            for case in d_cases['notSatisfied']:
                d_tmp = self.EFRB_run_n(case, d_param)

                if d_tmp['result'] == 1:
                    d_data_result = {
                        '反向': "ok",
                        '验证': case
                    }
                    if Configparser_PO.SWITCH("only_print_error") == "off":
                        Color_PO.outColor([{"36": d_data_result}])
                    Log_PO.logger.info(d_data_result)
                    l_count.append(1)
                else:
                    d_data_result = {
                        '反向': "error",
                        '验证': case
                    }
                    d_data_result.update(d_tmp)
                    s_tmp = str(d_data_result).replace("\\\\", "\\")
                    Color_PO.outColor([{"31": s_tmp}])
                    Log_PO.logger.info(s_tmp)
                    l_count.append(0)
                caseTotal += 1

        # 结果
        d_param['l_count'] = l_count
        d_param['caseTotal'] = caseTotal
        self._EFRB_result(d_param)

    def EFRB_case_or(self, caseType, d_cases, l_interconvert_conditions, Numerator, d_param):
        # 执行包含or条件的数据

        caseTotal = 0
        d_result = {}
        l_count = []

        if caseType == "p":
            # 正向
            if len(d_cases['satisfied']) == 1:
                # 正向, one条数据
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], d_param)
                if d_tmp['result'] == 1:
                    d_1 = {
                        '正向': 'ok',
                        '验证': d_cases['satisfied'][0]
                    }
                    s_print = f"{Numerator}-1, " + str(d_1)
                    if Configparser_PO.SWITCH("only_print_error") == "off":
                        Color_PO.outColor([{"34": s_print}])
                    d_1.update(d_tmp)
                    s_tmp = str(d_1).replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    # if Configparser_PO.SWITCH("curl_p") == "on":
                    #     Color_PO.outColor([{"34": s_tmp}])
                    l_count.append(1)
                else:
                    d_1 = {
                        '正向': 'error',
                        '验证': d_cases['satisfied'][0]
                    }
                    d_1.update(d_tmp)
                    s_tmp = str(d_1).replace("\\\\", "\\")
                    s_print = f"{Numerator}-1, " + s_tmp
                    Color_PO.outColor([{"31": s_print}])
                    Log_PO.logger.info(s_print)
                    # Color_PO.outColor([{"31": d_1}])
                    l_count.append(0)

                    # 将错误写入数据库log
                    conditions = self.convert_conditions(l_interconvert_conditions)  # 将列表转换字符串
                    d_tmp['条件'] = str(conditions)
                    d_tmp['测试数据'] = str(d_cases['satisfied'][0])
                    d_tmp['用例类型'] = "正向不满足"
                    s_tmp = str(d_tmp).replace("'", "''").replace("\\\\", "\\")
                    Sqlserver_PO_CHC.execute(
                        "UPDATE %s SET log = '%s' where id=%s" % (self.tableEFRB, s_tmp, d_param['id'])
                    )
                caseTotal += 1
            elif len(d_cases['satisfied']) > 1:
                # 正向, Multiple条数据

                for i in range(len(d_cases['satisfied'])):
                    d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], d_param)  # 正向 d_tmp['result']返回1
                    # print(444, d_tmp)

                    if d_tmp['result'] == 1:
                        s_print = f"{Numerator}-({i + 1}/{len(d_cases['satisfied'])}), {{'正向': 'ok', '验证': {str(d_cases['satisfied'][i])}}}"
                        if Configparser_PO.SWITCH("only_print_error") == "off":
                            Color_PO.outColor([{"34": s_print}])
                        Log_PO.logger.info(s_print)
                        caseTotal += 1
                        l_count.append(1)
                    else:
                        d_1 = {
                            '正向': 'error',
                            '验证': d_cases['satisfied'][i]
                        }
                        d_1.update(d_tmp)
                        s_tmp = str(d_1).replace("\\\\", "\\")
                        s_print = f"{Numerator}-({i + 1}/{len(d_cases['satisfied'])}), {s_tmp}"
                        Log_PO.logger.info(s_print)
                        Color_PO.outColor([{"31": s_print}])
                        caseTotal += 1
                        l_count.append(0)

        if caseType == "n":
            # 反向
            if len(d_cases['notSatisfied']) == 1:
                # 反向, 一条数据
                d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][0], d_param)
                # print(323,d_tmp)

                if d_tmp['result'] == 1:
                    d_1 = {
                        'No.': f"{Numerator}/{len(d_cases['notSatisfied'])}",
                        '反向': 'ok',
                        # '条件': l_interconvert_conditions,
                        '验证': d_cases['notSatisfied'][0]
                    }
                    if Configparser_PO.SWITCH("only_print_error") == "off":
                        Color_PO.outColor([{"34": d_1}])
                    d_1.update(d_tmp)
                    s_tmp = str(d_1).replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    # if Configparser_PO.SWITCH("curl_p") == "on":
                    #     Color_PO.outColor([{"34": s_tmp}])
                    l_count.append(1)
                else:
                    d_1 = {
                        'No.': f"{Numerator}/{len(d_cases['notSatisfied'])}",
                        '反向': 'error',
                        '验证': d_cases['notSatisfied'][0]
                    }
                    d_1.update(d_tmp)
                    s_tmp = str(d_1).replace("\\\\", "\\")
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": d_tmp}])
                    l_count.append(0)

                    # 将错误写入数据库log
                    conditions = self.convert_conditions(l_interconvert_conditions)  # 将列表转换字符串
                    # d_tmp['条件'] = str(conditions)
                    d_tmp['验证'] = str(d_cases['notSatisfied'][0])
                    d_tmp['用例类型'] = "正向不满足"
                    s_tmp = str(d_tmp).replace("'", "''").replace("\\\\", "\\")
                    Sqlserver_PO_CHC.execute(
                        "UPDATE %s SET log = '%s' where id=%s" % (self.tableEFRB, s_tmp, d_tmp['id'])
                    )
                caseTotal += 1

            elif len(d_cases['notSatisfied']) > 1:
                # 反向, N个数据
                # print(d_cases['notSatisfied'])
                for i in range(len(d_cases['notSatisfied'])):
                    d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][i], d_param)  # 正向 d_tmp['result']返回1
                    # print(444, d_tmp)  # 444 {'人群分类': '学生', 'categoryCode': '2', '年龄类型': 'float', '评估因素编码': 'TZ_STZB007', 'WEIGHT_REPORT__ID': 1952, '身份证': '310101193012210813', 'i': 'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" -H  "Request-Origion:SwaggerBootstrapUi" -H  "accept:*/*" -H "Authorization:" -H  "Content-Type:application/json" -d "{\\"age\\":0,\\"ageFloat\\":13,\\"ageMonth\\":0,\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],\\"bmi\\":18.5,\\"categoryCode\\":\\"\\",\\"disease\\":\\"\\",\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],\\"height\\":175,\\"idCard\\":\\"310101193012210813\\",\\"orgCode\\":\\"\\",\\"orgName\\":\\"\\",\\"sex\\":\\"男\\",\\"sexCode\\":\\"1\\",\\"weight\\":55,\\"weightReportId\\":1952}"', '实际值': ['TZ_AGE001', 'TZ_STZB011', 'TZ_SRL003', 'TZ_YD011', 'TZ_YS011', 'TZ_MBTZ001'], '预期值': 'TZ_STZB007', 'sql__T_ASSESS_RULE_RECORD': 'select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 1952', 'result': 1}

                    if d_tmp['result'] == 1:
                        s_print = f"{i + 1}/{len(d_cases['notSatisfied'])}, {{'反向': 'ok', '验证': {str(d_cases['notSatisfied'][i])}}}"
                        # s_print = f"{Numerator}-({i + 1}/{len(d_cases['notSatisfied'])}), {{'反向': 'ok', '验证': {str(d_cases['notSatisfied'][i])}}}"
                        if Configparser_PO.SWITCH("only_print_error") == "off":
                            Color_PO.outColor([{"36": s_print}])
                        Log_PO.logger.info(s_print)
                        caseTotal += 1
                        l_count.append(1)
                    else:
                        d_1 = {
                            '反向': 'error',
                            '验证': d_cases['notSatisfied'][i]
                        }
                        d_1.update(d_tmp)
                        s_tmp = str(d_1).replace("\\\\", "\\")
                        Log_PO.logger.info(s_tmp)
                        Color_PO.outColor([{"31": s_tmp}])
                        caseTotal += 1
                        l_count.append(0)

        # 结果
        d_result['caseTotal'] = caseTotal
        if 0 in l_count:
            d_result['id'] = id
            d_result['数据集合'] = l_count
            d_result['count'] = 0
            Log_PO.logger.info(d_result)
        else:
            d_result['count'] = 1
        # print(677,d_result)  # 677 {'caseTotal': 4, 'count': 1}

        return d_result

    def _EFRB_run(self, d_cases_satisfied, d_param):
        """公共测试用例执行"""
        d_tmp = {}

        # print(1408, d_param)

        # 获取规则信息
        l_d_row = Sqlserver_PO_CHC.select("select categoryCode, ER_code from %s where id= %s" %(self.tableEFRB, d_param['id']))

        # d_tmp['ER_code'] = l_d_row[0]['ER_code']
        # d_tmp['身份证'] = Configparser_PO.FILE("testIdcard")
        # d_tmp['category'] = l_d_row[0]['category']
        d_tmp['categoryCode'] = l_d_row[0]['categoryCode']
        # d_tmp['categoryType'] = l_d_row[0]['categoryType']

        # categoryCode = d_param.get('categoryCode', '')

        # 疾病
        disease = d_param.get('disease', '')

        # BMI
        varBMI = d_cases_satisfied.get('BMI', 0)

        # 年龄
        # 儿童 0-6岁（0-72月龄），ageMonth ， categoryCode=1
        # 学生 7-18岁，ageFloat, categoryCode=2
        # 普通人群，孕妇，产妇，老年人，age
        if l_d_row[0]['categoryCode'] == '1':
            varAgeMonth = d_cases_satisfied.get('年龄', 0)
            varAgeFloat = 0.0
            varAge = 0
        elif l_d_row[0]['categoryCode'] == '2':
            varAgeMonth = 0
            varAgeFloat = d_cases_satisfied.get('年龄', 0.0)
            varAge = 0
        else:
            varAgeMonth = 0
            varAgeFloat = 0.0
            varAge = d_cases_satisfied.get('年龄', 0)

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


        # 跑接口
        command = (
                'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" '
                '-H  "Request-Origion:SwaggerBootstrapUi" '
                '-H  "accept:*/*" '
                '-H "Authorization:" '
                '-H  "Content-Type:application/json" '
                '-d "{\\"age\\":' + str(varAge) + ','
                '\\"ageFloat\\":' + str(varAgeFloat) + ','
                '\\"ageMonth\\":' + str(
                varAgeMonth) + ','
                '\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],'
                '\\"bmi\\":' + str(varBMI) + ','
                '\\"categoryCode\\":\\"' + str(d_tmp['categoryCode']) + '\\",'
                '\\"disease\\":\\"' + str(disease) + '\\",'
                '\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],'
                '\\"height\\":175,'
                '\\"idCard\\":\\"' + str(self.IDCARD) + '\\",'
                '\\"orgCode\\":\\"\\",'
                '\\"orgName\\":\\"\\",'
                '\\"sex\\":\\"' + str(varSex) + '\\",'
                '\\"sexCode\\":\\"' + str(
                varSexCode) + '\\",'
                '\\"weight\\":55,'
                '\\"weightReportId\\":' + str(self.WEIGHT_REPORT__ID) + '}"'
                )

        if Configparser_PO.SWITCH("print_curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # d_tmp["i"] = command

        if d_r['code'] == 200:
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = %s" % (self.WEIGHT_REPORT__ID)
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['预期值'] = l_d_row[0]['ER_code']
            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            d_tmp["i"] = command
            return d_tmp
        else:
            print("error ", d_r['code'])
            sys.exit(0)

    def EFRB_run_p(self, d_cases_satisfied, d_param):
        """正向测试"""
        d_1 = {}
        d_tmp = self._EFRB_run(d_cases_satisfied, d_param)
        d_1['result'] = 1 if d_tmp['预期值'] in d_tmp['实际值'] else 0
        d_1.update(d_tmp)
        return d_1

    def EFRB_run_n(self, d_cases_notSatisfied, d_param):
        """反向测试"""
        d_1 = {}
        d_tmp = self._EFRB_run(d_cases_notSatisfied, d_param)
        d_1['result'] = 0 if d_tmp['预期值'] in d_tmp['实际值'] else 1
        d_1.update(d_tmp)
        return d_1

    def EFRB_run_disease(self, d_param):
        """处理疾病测试"""
        d_tmp = {}

        # 获取规则信息
        l_d_row = Sqlserver_PO_CHC.select(
            "select ER_code from %s where id= %s" % (self.tableEFRB, d_param['id'])
        )
        d_tmp['评估因素编码'] = l_d_row[0]['ER_code']

        # 参数化
        # d_tmp['WEIGHT_REPORT__ID'] = self.WEIGHT_REPORT__ID
        # d_tmp['身份证'] = Configparser_PO.FILE("testIdcard")

        varAge = 0
        varAgeFloat = 0.0
        varAgeMonth = 0
        varBMI = 10.1

        # 跑接口
        command = (
                'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" '
                '-H  "Request-Origion:SwaggerBootstrapUi" '
                '-H  "accept:*/*" '
                '-H "Authorization:" '
                '-H  "Content-Type:application/json" '
                '-d "{\\"age\\":' + str(varAge) + ','
                '\\"ageFloat\\":' + str(varAgeFloat) + ','
                '\\"ageMonth\\":' + str(varAgeMonth) + ','
                '\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],'
                '\\"bmi\\":' + str(varBMI) + ','
                '\\"categoryCode\\":1,'
                '\\"disease\\":\\"' + str(d_param['disease']) + '\\",'
                '\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],'
                '\\"height\\":175,'
                '\\"idCard\\":\\"' + str(self.IDCARD) + '\\",'
                '\\"orgCode\\":\\"\\",'
                '\\"orgName\\":\\"\\",'
                '\\"sex\\":\\"\\",'
                '\\"sexCode\\":\\"1\\",'
                '\\"weight\\":55,'
                '\\"weightReportId\\":' + str(self.WEIGHT_REPORT__ID) + '}"'
                )

        if Configparser_PO.SWITCH("print_curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command

        if d_r['code'] == 200:
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = %s" % (self.WEIGHT_REPORT__ID)
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['ER_code']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql

            l_count = []
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                result_data = {
                    '正向': "ok",
                    '既往疾病': d_param['conditions']
                }
                if Configparser_PO.SWITCH("only_print_error") == "off":
                    Color_PO.outColor([{"34": result_data}])
                Log_PO.logger.info(result_data)
                l_count.append(1)
            else:
                result_data = {
                    '正向': 'error',
                    '既往疾病包含': d_param['conditions']
                }
                result_data.update(d_tmp)
                s_tmp = str(result_data).replace("\\\\", "\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库result, updateDate
            if 0 not in l_count:
                d_result = {'result': 'ok', 'id': d_param['id'], 'ER_code': d_param['ER_code']}
                s = "评估因素规则库EFRB => " + str(d_result)
                Color_PO.outColor([{"32": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC.execute(
                    "update %s set result = '%s', updateDate = GETDATE() where id = %s" %
                    (self.tableEFRB, 'ok', d_result['id'])
                )
            else:
                d_result = {'result': 'error', 'id': d_param['id'], 'ER_code': d_param['ER_code']}
                s = "评估因素规则库EFRB => " + str(d_result)
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC.execute(
                    "update %s set result = '%s', updateDate = GETDATE() where id = %s" %
                    (self.tableEFRB, 'error', d_result['id'])
                )
        else:
            print("error ", d_r['code'])
            sys.exit(0)

    def EFRB_run_crowd(self, d_param):
        """处理人群分类测试"""

        print(1629, d_param)
        d_tmp = {}

        # 获取规则信息
        l_d_row = Sqlserver_PO_CHC.select("select ER_code from %s where id= %s" % (self.tableEFRB, d_param['id']))
        d_tmp['评估因素编码'] = l_d_row[0]['ER_code']

        # 参数化
        # d_tmp['WEIGHT_REPORT__ID'] = self.WEIGHT_REPORT__ID
        # d_tmp['身份证'] = self.IDCARD

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
        command = (
                'curl -X POST "http://192.168.0.243:8016/tAssessRuleRecord/executeWeightRule" '
                '-H  "Request-Origion:SwaggerBootstrapUi" '
                '-H  "accept:*/*" '
                '-H "Authorization:" '
                '-H  "Content-Type:application/json" '
                '-d "{\\"age\\":' + str(varAge) + ','
                '\\"ageFloat\\":' + str(varAgeFloat) + ','
                '\\"ageMonth\\":' + str(varAgeMonth) + ','
                '\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],'
                '\\"bmi\\":' + str(varBMI) + ','
                '\\"categoryCode\\":' + str(d_param['categoryCode']) + ','
                '\\"disease\\":\\"\\",'
                '\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],'
                '\\"height\\":175,'
                '\\"idCard\\":\\"' + str(self.IDCARD) + '\\",'
                '\\"orgCode\\":\\"\\", \\"orgName\\":\\"\\",'
                '\\"sex\\":\\"' + str(varSex) + '\\",'
                '\\"sexCode\\":' + str(varSexCode) + ','
                '\\"weight\\":55,'
                '\\"weightReportId\\":' + str(self.WEIGHT_REPORT__ID) + '}"')

        if Configparser_PO.SWITCH("print_curl") == "on":
            print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        d_tmp["i"] = command

        if d_r['code'] == 200:
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = %s" % (self.WEIGHT_REPORT__ID)
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['ER_code']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql

            l_count = []
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                result_data = {
                    '正向': 'ok',
                    '条件': d_param['conditions']
                }
                if Configparser_PO.SWITCH("only_print_error") == "off":
                    Color_PO.outColor([{"34": result_data}])
                Log_PO.logger.info(result_data)
                l_count.append(1)
            else:
                result_data = {
                    '正向': 'error',
                    '条件': d_param['conditions']
                }
                result_data.update(d_tmp)
                s_tmp = str(result_data).replace("\\\\", "\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库result, updateDate
            if 0 not in l_count:
                d_result = {"result": "ok", "id": d_param['id'], "ER_code": d_param['ER_code']}
                s = "评估因素规则库EFRB => " + str(d_result)
                Color_PO.outColor([{"32": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC.execute(
                    "update %s set result = '%s', updateDate = GETDATE() where id = %s" %
                    (self.tableEFRB, "ok", d_result["id"])
                )
            else:
                d_result = {"result": "error", "id": d_param['id'], "ER_code": d_param['ER_code']}
                s = "评估因素规则库EFRB => " + str(d_result)
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC.execute(
                    "update %s set result = '%s', updateDate = GETDATE() where id = %s" %
                    (self.tableEFRB, "error", d_result["id"])
                )
        else:
            print("error ", d_r['code'])
            sys.exit(0)

    def _EFRB_result(self, d_param):
        # 测试结果
        if 0 not in d_param['l_count']:
            d_result = {'result': 'ok', 'id': d_param['id'], 'ER_code': d_param['ER_code']}
            s = "评估因素规则库EFRB => " + str(d_result)
            Color_PO.outColor([{"32": s}])
            print("".center(100, "-"))
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC.execute(
                "update %s set result = 'ok', updateDate = GETDATE(), totalCase=%s where id = %s" %
                (self.tableEFRB, d_param['caseTotal'], d_param['id'])
            )
        else:
            d_result = {'result': 'error', 'id': d_param['id'], 'ER_code': d_param['ER_code']}
            s = "评估因素规则库EFRB => " + str(d_result)
            Color_PO.outColor([{"31": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC.execute(
                "update %s set result = 'error', updateDate = GETDATE(), totalCase=%s where id = %s" %
                (self.tableEFRB, d_param['caseTotal'], d_param['id'])
            )
