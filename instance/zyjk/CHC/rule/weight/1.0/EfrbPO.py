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
        self.WEIGHT_REPORT__ID = l_d_ID[0]['ID']

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
            varTable = varSheet = "a_weight10_EFRB"

            # 1, db中删除已有的表
            Sqlserver_PO_CHC.execute("drop table if exists " + varTable)

            # 读取 Excel 文件
            df = pd.read_excel(Configparser_PO.FILE("case"), sheet_name=varSheet)
            df = df.sort_index()  # 按行索引排序，保持Excel原有顺序
            df = df.dropna(how="all")  # 移除全空行

            # 手动设置字段类型
            df['conditions_nvc'] = df['conditions_nvc'].astype(str)  # 改为字符串类型

            # 2, excel导入db
            Sqlserver_PO_CHC.df2db(df, varTable)

            # 3, 设置表注释
            Sqlserver_PO_CHC.setTableComment(varTable, '体重管理1.0_评估因素规则库_自动化测试')

            # 4， 替换换行符为空格
            Sqlserver_PO_CHC.execute(
                "UPDATE %s SET conditions_nvc = REPLACE(REPLACE(conditions_nvc, CHAR(10), ' '), CHAR(13), ' ');" % (
                    varTable)
            )

            # 5, 设置字段类型与描述
            field_definitions = [
                ('result_nvc', 'nvarchar(10)', '测试结果'),
                ('testDate_date', 'nvarchar(50)', '更新日期'),
                ('log_nvc', 'varchar(max)', '日志信息'),
                ('type_nvc', 'nvarchar(20)', '分类'),
                ('category_nvc', 'nvarchar(20)', '人群分类'),
                ('categoryCode_vc', 'varchar(3)', '人群分类编码'),
                ('ageType_nvc', 'nvarchar(50)', '年龄类型'),
                ('ruleName_nvc', 'nvarchar(100)', '规则名称'),
                ('detail_nvc', 'nvarchar(999)', '评估规则详细描述'),
                ('conditions_old_nvc', 'nvarchar(max)', '评估因素判断规则_原始'),
                ('conditions_nvc', 'nvarchar(max)', '评估因素判断规则'),
                ('code_vc', 'varchar(50)', '评估规则编码'),
                ('testCase_nvc', 'nvarchar(100)', '测试用例'),
                ('caseTotal_i', 'int', '测试数量'),
                ('errID_i', 'int', '错误id')
            ]

            for field_name, field_type, comment in field_definitions:
                Sqlserver_PO_CHC.setFieldTypeComment(varTable, field_name, field_type, comment)

            Sqlserver_PO_CHC.execute("ALTER TABLE %s ALTER COLUMN testDate_date DATE;" % (varTable))

            # 6, 设置自增主键（最后）
            Sqlserver_PO_CHC.setIdentityPrimaryKey(varTable, "id_pk")

        except Exception as e:
            raise e

    def EFRB(self, varTestID, d_param={}):
        """主程序"""
        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC.select("select id_pk, conditions_nvc, code_vc from %s" % (self.tableEF))

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

    def _EFRB_main(self, d_param, conditions_nvc):
        """主处理逻辑"""
        # 清洗不规则数据
        conditions_nvc = self._clean_conditions(conditions_nvc)

        # 根据条件类型分发处理
        if '疾病' in conditions_nvc:
            self._handle_disease_condition(d_param, conditions_nvc)
        elif '人群分类' in conditions_nvc:
            self._handle_crowd_condition(d_param, conditions_nvc)
        elif "年龄" in conditions_nvc and "BMI" not in conditions_nvc:
            self._handle_age_only_condition(d_param, conditions_nvc)
        elif "or" in conditions_nvc:
            self._handle_or_condition(d_param, conditions_nvc)
        elif "and" in conditions_nvc and "or" not in conditions_nvc and "BMI" in conditions_nvc and "年龄" in conditions_nvc:
            self._handle_age_bmi_condition(d_param, conditions_nvc)
        elif "and" not in conditions_nvc:
            self._handle_simple_condition(d_param, conditions_nvc)
        else:
            print("[not or & and ]")

    def _clean_conditions(self, conditions_nvc):
        """清洗条件字符串"""
        conditions_nvc = conditions_nvc.replace("月", '')
        conditions_nvc = conditions_nvc.replace('＞', '>').replace('＜', '<').replace('＝', '=')
        return conditions_nvc

    def _handle_disease_condition(self, d_param, conditions_nvc):
        """处理疾病条件"""
        d_param['disease'] = conditions_nvc
        self.EFRB_run_disease(d_param)

    def _handle_crowd_condition(self, d_param, conditions_nvc):
        """处理人群分类条件"""
        d_param['categoryCode'] = conditions_nvc.split("=")[1]
        self.EFRB_run_crowd(d_param)

    def _handle_age_only_condition(self, d_param, conditions_nvc):
        """处理只有年龄的条件"""
        # 元素拆分
        l_conditions = []
        l_simple_conditions = Age_PO.splitMode(conditions_nvc)
        l_conditions.extend(l_simple_conditions)

        # 转换位置
        l_conditions_interconver = []
        for i in l_conditions:
            l_simple_conditions = Age_PO.interconvertMode(i)
            l_conditions_interconver.extend(l_simple_conditions)

        # 生成随机数据
        d_cases = Age_PO.generate_all_cases(l_conditions_interconver)
        if Configparser_PO.SWITCH("testDataSet") == "on":
            print("测试数据集 =>", d_cases)
        Log_PO.logger.info("测试数据集 => " + str(d_cases))

        # 处理测试用例
        self.EFRB_case(d_cases, d_param)

    def _handle_or_condition(self, d_param, conditions_nvc):
        """处理包含or的复合条件"""
        # 格式化数据
        l_l_value = self._parse_or_conditions(conditions_nvc)

        l_count = []
        sum = 0
        varTestCount = conditions_nvc.count("or")

        for lln, l_value in enumerate(l_l_value):
            # 格式化条件
            l_conditions = self._format_conditions(l_value)

            # 转换位置
            l_interconvert_conditions = []
            for i in l_conditions:
                l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                l_interconvert_conditions.extend(l_simple_conditions)

            # 生成随机数据
            d_cases = self._generate_test_data(l_interconvert_conditions)

            if Configparser_PO.SWITCH("testDataSet") == "on":
                print("测试数据 =>", d_cases)

            # 测试数据
            Numerator = lln + 1
            Denominator = varTestCount + 1
            d_result = self.EFRB_case_or(d_cases, d_param['id_pk'], l_conditions, Numerator, Denominator, d_param)
            l_count.append(d_result['count'])
            sum = sum + d_result['caseTotal']

        # 更新记录
        d_param['l_count'] = l_count
        d_param['caseTotal'] = sum
        self._EFRB_result(d_param)

    def _parse_or_conditions(self, conditions_nvc):
        """解析包含or的条件"""
        l_value = conditions_nvc.split("or")
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

    def _generate_test_data(self, l_interconvert_conditions):
        """生成测试数据"""
        for i in l_interconvert_conditions:
            if ('>=' in i or '<=' in i) and ('年龄' in i or 'BMI' in i):
                return BmiAgeSex_PO.main(l_interconvert_conditions)
        return BmiAgeSex_PO.main(l_interconvert_conditions)

    def _handle_age_bmi_condition(self, d_param, conditions_nvc):
        """处理年龄和BMI组合条件"""
        # 字符串转换成列表
        l_conditions = conditions_nvc.split("and")
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
        if Configparser_PO.SWITCH("testDataSet") == "on":
            print("测试数据集 =>", d_cases)
        Log_PO.logger.info("测试数据集 => " + str(d_cases))

        # 测试数据
        d_param['l_conditions'] = l_conditions
        self.EFRB_case(d_cases, d_param)

    def _handle_simple_condition(self, d_param, conditions_nvc):
        """处理简单条件"""
        l_conditions = []
        # 拆分
        l_simple_conditions = Bmi_PO.splitMode(conditions_nvc)
        l_conditions.extend(l_simple_conditions)

        # 转换位置
        l_3_value = []
        for i in l_conditions:
            l_simple_conditions = Bmi_PO.interconvertMode(i)
            l_3_value.extend(l_simple_conditions)

        # 生成随机数据
        d_cases = Age_PO.generate_all_cases(l_3_value)
        if Configparser_PO.SWITCH("testDataSet") == "on":
            print("测试数据集 =>", d_cases)
        Log_PO.logger.info("测试数据集 => " + str(d_cases))

        # 处理测试用例
        d_param['l_conditions'] = l_conditions
        self.EFRB_case(d_cases, d_param)

    def _EFRB_ALL(self):
        """测试所有规则"""
        l_d_row = Sqlserver_PO_CHC.select("select id_pk, conditions_nvc, code_vc from %s" % (self.tableEF))

        for row in l_d_row:
            d_param = {
                '表': self.tableEF,
                'id_pk': row['id_pk'],
                'conditions_nvc': row['conditions_nvc'],
                '表注释': '评估因素规则库EFRB',
                'WEIGHT_REPORT__IDCARD': self.WEIGHT_REPORT__IDCARD
            }

            s = "测试 => " + str(d_param)
            Color_PO.outColor([{"35": s}])
            Log_PO.logger.info(s)

            self._EFRB_main(d_param, row['conditions_nvc'])

    def _EFRB_ID(self, varTestID, d_param):
        """测试单条规则"""
        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC.select(
            "select conditions_nvc, code_vc from %s where id_pk=%s" % (self.tableEF, varTestID)
        )
        conditions_nvc = l_d_row[0]['conditions_nvc']

        d_ = {
            '表': self.tableEF,
            '表注释': '评估因素规则库EFRB',
            'id_pk': varTestID,
            'conditions_nvc': conditions_nvc,
            'WEIGHT_REPORT__IDCARD': self.WEIGHT_REPORT__IDCARD
        }
        d_.update(d_param)

        s = "测试 => " + str(d_)
        Color_PO.outColor([{"35": s}])
        Log_PO.logger.info(s)

        self._EFRB_main(d_, conditions_nvc)

    def EFRB_case(self, d_cases, d_param):
        """处理测试用例"""
        caseTotal = 0
        l_count = []

        for case in d_cases['satisfied']:
            d_tmp = self.EFRB_run_p(case, d_param)

            if d_tmp['result'] == 1:
                result_data = {
                    '正向': "ok",
                    '条件': d_param['conditions_nvc'],
                    '测试数据': case
                }
                if Configparser_PO.SWITCH("positiveResult") == "on":
                    Color_PO.outColor([{"34": result_data}])
                Log_PO.logger.info(result_data)
                l_count.append(1)
            else:
                result_data = {
                    '正向': "error",
                    '条件': d_param['conditions_nvc'],
                    '测试数据': case
                }
                result_data.update(d_tmp)
                s_tmp = str(result_data).replace("\\\\", "\\")
                if Configparser_PO.SWITCH("positiveResult") == "on":
                    Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)
            caseTotal += 1

        d_param['l_count'] = l_count
        d_param['caseTotal'] = caseTotal
        self._EFRB_result(d_param)

    def EFRB_case_or(self, d_cases, id, l_conditions, Numerator, Denominator, d_param):
        """处理包含or条件的测试用例"""
        caseTotal = 0
        d_result = {}

        if len(d_cases['satisfied']) == 1:
            # 正向用例, 一条数据
            l_count = []
            d_tmp = self.EFRB_run_p(d_cases['satisfied'][0], d_param)

            if d_tmp['result'] == 1:
                d_1 = {
                    'No.': f"{Numerator}/{Denominator}",
                    '正向': 'ok',
                    '条件': l_conditions,
                    '测试数据': d_cases['satisfied'][0]
                }
                if Configparser_PO.SWITCH("positiveResult") == "on":
                    Color_PO.outColor([{"34": d_1}])
                d_1.update(d_tmp)
                s_tmp = str(d_1).replace("\\\\", "\\")
                Log_PO.logger.info(s_tmp)
                if Configparser_PO.SWITCH("curl_p") == "on":
                    Color_PO.outColor([{"34": s_tmp}])
                l_count.append(1)
            else:
                d_1 = {
                    'No.': f"{Numerator}/{Denominator}",
                    '正向': 'error',
                    '条件': l_conditions,
                    '测试数据': d_cases['satisfied'][0]
                }
                d_1.update(d_tmp)
                s_tmp = str(d_1).replace("\\\\", "\\")
                Log_PO.logger.info(s_tmp)
                Color_PO.outColor([{"31": d_tmp}])
                l_count.append(0)

                # 将错误写入数据库log
                conditions_nvc = self.convert_conditions(l_conditions)  # 将列表转换字符串
                d_tmp['条件'] = str(conditions_nvc)
                d_tmp['测试数据'] = str(d_cases['satisfied'][0])
                d_tmp['用例类型'] = "正向不满足"
                s_tmp = str(d_tmp).replace("'", "''").replace("\\\\", "\\")
                Sqlserver_PO_CHC.execute(
                    "UPDATE %s SET log_nvc = '%s' where id_pk=%s" % (self.tableEF, s_tmp, d_tmp['id_pk'])
                )
            caseTotal += 1

            # 一条数据，反向用例
            if Configparser_PO.SWITCH("testNegative") == "on":
                d_tmp = self.EFRB_run_n(d_cases['notSatisfied'][0], d_param)
                conditions_nvc = self.convert_conditions(l_conditions)
                if d_tmp['result'] == 1:
                    s_print = "{'反向': 'error', '条件': " + str(conditions_nvc) + ", '测试数据': " + str(
                        d_cases['notSatisfied'][0]) + "}"
                    Color_PO.outColor([{"31": s_print}])
                    Log_PO.logger.info(s_print)
                    Color_PO.outColor([{"33": d_tmp}])
                    Log_PO.logger.info(d_tmp)
                    l_count.append(0)
                else:
                    s_print = "{'反向': 'ok', '条件': " + str(conditions_nvc) + ", '测试数据': " + str(
                        d_cases['notSatisfied'][0]) + "}"
                    Color_PO.outColor([{"36": s_print}])
                    Log_PO.logger.info(s_print)
                    l_count.append(1)
                caseTotal += 1

        else:
            # 正向用例, N个数据
            l_count = []
            for i in range(len(d_cases['satisfied'])):
                d_tmp = self.EFRB_run_p(d_cases['satisfied'][i], d_param)
                if d_tmp['result'] == 1:
                    s_print = f"{Numerator}({i + 1})/{Denominator}, {{'正向': 'ok', '条件': {str(l_conditions)}, '测试数据': {str(d_cases['satisfied'][i])}}}"
                    if Configparser_PO.SWITCH("positiveResult") == "on":
                        Color_PO.outColor([{"34": s_print}])
                    Log_PO.logger.info(s_print)
                    caseTotal += 1
                    l_count.append(1)
                else:
                    d_1 = {
                        '表': 'a_weight10_EFRB',
                        'id_pk': id,
                        '正向': 'error',
                        '条件': l_conditions,
                        '测试数据': d_cases['satisfied'][i]
                    }
                    d_1.update(d_tmp)
                    s_tmp = str(d_1).replace("\\\\", "\\")
                    if Configparser_PO.SWITCH("positiveResult") == "on":
                        Color_PO.outColor([{"31": s_tmp}])
                    Log_PO.logger.info(s_tmp)
                    Color_PO.outColor([{"31": s_tmp}])
                    caseTotal += 1
                    l_count.append(0)

        d_result['caseTotal'] = caseTotal
        if 0 in l_count:
            d_result['id_pk'] = id
            d_result['数据集合'] = l_count
            d_result['count'] = 0
            Log_PO.logger.info(d_result)
        else:
            d_result['count'] = 1
        return d_result

    def _EFRB_run(self, d_cases_satisfied, d_param):
        """公共测试用例执行"""
        d_tmp = {}

        # 获取规则信息
        l_d_row = Sqlserver_PO_CHC.select(
            "select category_nvc, categoryCode_vc, ageType_nvc, code_vc from %s where id_pk= %s" %
            (self.tableEF, d_param['id_pk'])
        )

        d_tmp['人群分类'] = l_d_row[0]['category_nvc']
        d_tmp['categoryCode'] = l_d_row[0]['categoryCode_vc']
        d_tmp['年龄类型'] = l_d_row[0]['ageType_nvc']
        d_tmp['评估因素编码'] = l_d_row[0]['code_vc']

        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = self.WEIGHT_REPORT__ID
        d_tmp['身份证'] = Configparser_PO.FILE("testIdcard")

        # BMI
        varBMI = d_cases_satisfied.get('BMI', 0)

        # 年龄
        if d_tmp['年龄类型'] == "int":
            if d_tmp['categoryCode'] == '1':
                varAgeMonth = d_cases_satisfied.get('年龄', 0)
                varAge = 0
                varAgeFloat = 0.0
            else:
                varAgeMonth = 0
                varAge = d_cases_satisfied.get('年龄', 0)
                varAgeFloat = 0.0
        elif d_tmp['年龄类型'] == "float":
            varAgeFloat = d_cases_satisfied.get('年龄', 0.0)
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

        categoryCode = d_param.get('categoryCode', '')
        disease = d_param.get('disease', '')

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
                                                        '\\"categoryCode\\":\\"' + str(categoryCode) + '\\",'
                                                                                                       '\\"disease\\":\\"' + str(
            disease) + '\\",'
                       '\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],'
                       '\\"height\\":175,'
                       '\\"idCard\\":\\"' + str(d_tmp['身份证']) + '\\",'
                                                                '\\"orgCode\\":\\"\\",'
                                                                '\\"orgName\\":\\"\\",'
                                                                '\\"sex\\":\\"' + str(varSex) + '\\",'
                                                                                                '\\"sexCode\\":\\"' + str(
            varSexCode) + '\\",'
                          '\\"weight\\":55,'
                          '\\"weightReportId\\":' + str(self.WEIGHT_REPORT__ID) + '}"'
        )

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
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['code_vc']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            return d_tmp
        else:
            print("error ", d_r['code'])
            sys.exit(0)

    def EFRB_run_p(self, d_cases_satisfied, d_param):
        """正向测试"""
        d_tmp = self._EFRB_run(d_cases_satisfied, d_param)
        d_tmp['result'] = 1 if d_tmp['预期值'] in d_tmp['实际值'] else 0
        return d_tmp

    def EFRB_run_n(self, d_cases_satisfied, d_param):
        """反向测试"""
        d_tmp = self._EFRB_run(d_cases_satisfied, d_param)
        d_tmp['result'] = 0 if d_tmp['预期值'] in d_tmp['实际值'] else 1
        return d_tmp

    def EFRB_run_disease(self, d_param):
        """处理疾病测试"""
        d_tmp = {}

        # 获取规则信息
        l_d_row = Sqlserver_PO_CHC.select(
            "select code_vc from %s where id_pk= %s" % (self.tableEF, d_param['id_pk'])
        )
        d_tmp['评估因素编码'] = l_d_row[0]['code_vc']

        # 参数化
        d_tmp['WEIGHT_REPORT__ID'] = self.WEIGHT_REPORT__ID
        d_tmp['身份证'] = Configparser_PO.FILE("testIdcard")

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
                                                                                         '\\"ageMonth\\":' + str(
            varAgeMonth) + ','
                           '\\"assessRuleRecord\\":[{\\"assessId\\":0,\\"createDate\\":\\"\\",\\"id\\":0,\\"riskFactor\\":\\"\\",\\"riskFactorRuleCodes\\":[],\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"suggestedValue\\":\\"\\",\\"weightReportId\\":0}],'
                           '\\"bmi\\":' + str(varBMI) + ','
                                                        '\\"categoryCode\\":1,'
                                                        '\\"disease\\":\\"' + str(d_param['disease']) + '\\",'
                                                                                                        '\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],'
                                                                                                        '\\"height\\":175,'
                                                                                                        '\\"idCard\\":\\"' + str(
            d_tmp['身份证']) + '\\",'
                            '\\"orgCode\\":\\"\\",'
                            '\\"orgName\\":\\"\\",'
                            '\\"sex\\":\\"\\",'
                            '\\"sexCode\\":\\"1\\",'
                            '\\"weight\\":55,'
                            '\\"weightReportId\\":' + str(self.WEIGHT_REPORT__ID) + '}"'
        )

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
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['code_vc']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql

            l_count = []
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                result_data = {
                    '正向': "ok",
                    '既往疾病': d_param['conditions_nvc']
                }
                if Configparser_PO.SWITCH("positiveResult") == "on":
                    Color_PO.outColor([{"34": result_data}])
                Log_PO.logger.info(result_data)
                l_count.append(1)
            else:
                result_data = {
                    '正向': 'error',
                    '既往疾病包含': d_param['conditions_nvc']
                }
                result_data.update(d_tmp)
                s_tmp = str(result_data).replace("\\\\", "\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库result, testDate_date
            d_result = {
                '表': d_param.get('表', ''),
                'id_pk': d_param['id_pk']
            }

            if 0 not in l_count:
                d_result['测试结果'] = "ok"
                s = "结果 => " + str(d_result)
                Color_PO.outColor([{"32": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC.execute(
                    "update %s set result_nvc = '%s', testDate_date = GETDATE() where id_pk = %s" %
                    (self.tableEF, d_result['测试结果'], d_result['id_pk'])
                )
            else:
                d_result['测试结果'] = "error"
                s = "结果 => " + str(d_result)
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC.execute(
                    "update %s set result_nvc = '%s', testDate_date = GETDATE() where id_pk = %s" %
                    (self.tableEF, d_result['测试结果'], d_result['id_pk'])
                )
        else:
            print("error ", d_r['code'])
            sys.exit(0)

    def EFRB_run_crowd(self, d_param):
        """处理人群分类测试"""
        d_tmp = {}

        # 获取规则信息
        l_d_row = Sqlserver_PO_CHC.select(
            "select code_vc from %s where id_pk= %s" % (self.tableEF, d_param['id_pk'])
        )
        d_tmp['评估因素编码'] = l_d_row[0]['code_vc']

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
                                                        '\\"categoryCode\\":' + str(d_param['categoryCode']) + ','
                                                                                                               '\\"disease\\":\\"\\",'
                                                                                                               '\\"enableRule\\":[{\\"description\\":\\"\\",\\"diseaseCode\\":\\"\\",\\"diseaseName\\":\\"\\",\\"enable\\":0,\\"id\\":0,\\"interveneType\\":0,\\"judgment\\":\\"\\",\\"orgCode\\":\\"\\",\\"ruleCode\\":\\"\\",\\"ruleGroup\\":\\"\\",\\"ruleName\\":\\"\\",\\"serialNumber\\":0}],'
                                                                                                               '\\"height\\":175,'
                                                                                                               '\\"idCard\\":\\"' + str(
            d_tmp['身份证']) + '\\",'
                            '\\"orgCode\\":\\"\\",'
                            '\\"orgName\\":\\"\\",'
                            '\\"sex\\":\\"' + str(varSex) + '\\",'
                                                            '\\"sexCode\\":' + str(varSexCode) + ','
                                                                                                 '\\"weight\\":55,'
                                                                                                 '\\"weightReportId\\":' + str(
            self.WEIGHT_REPORT__ID) + '}"'
        )

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
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = l_d_row[0]['code_vc']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql

            l_count = []
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                result_data = {
                    '正向': 'ok',
                    '人群分类': d_param['conditions_nvc']
                }
                if Configparser_PO.SWITCH("positiveResult") == "on":
                    Color_PO.outColor([{"34": result_data}])
                Log_PO.logger.info(result_data)
                l_count.append(1)
            else:
                result_data = {
                    '正向': 'error',
                    '人群分类': d_param['conditions_nvc']
                }
                result_data.update(d_tmp)
                s_tmp = str(result_data).replace("\\\\", "\\")
                Color_PO.outColor([{"31": s_tmp}])
                Log_PO.logger.info(s_tmp)
                l_count.append(0)

            # 回写数据库result, testDate_date
            d_result = {
                "表": d_param.get('表', ''),
                "id_pk": d_param['id_pk']
            }

            if 0 not in l_count:
                d_result["测试结果"] = "ok"
                s = "结果 => " + str(d_result)
                Color_PO.outColor([{"32": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC.execute(
                    "update %s set result_nvc = '%s', testDate_date = GETDATE() where id_pk = %s" %
                    (self.tableEF, d_result["测试结果"], d_result["id_pk"])
                )
            else:
                d_result["测试结果"] = "error"
                s = "结果 => " + str(d_result)
                Color_PO.outColor([{"31": s}])
                Log_PO.logger.info(s)
                Sqlserver_PO_CHC.execute(
                    "update %s set result_nvc = '%s', testDate_date = GETDATE() where id_pk = %s" %
                    (self.tableEF, d_result["测试结果"], d_result["id_pk"])
                )
        else:
            print("error ", d_r['code'])
            sys.exit(0)

    def _EFRB_result(self, d_param):
        """处理测试结果"""
        d_result = {'id_pk': d_param['id_pk']}

        if 0 not in d_param['l_count']:
            d_result['测试结果'] = 'ok'
            s = "结果 => " + str(d_result)
            Color_PO.outColor([{"32": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC.execute(
                "update %s set result_nvc = 'ok', testDate_date = GETDATE(), caseTotal_i=%s where id_pk = %s" %
                (self.tableEF, d_param['caseTotal'], d_param['id_pk'])
            )
        else:
            d_result['测试结果'] = 'error'
            s = "结果 => " + str(d_result)
            Color_PO.outColor([{"31": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC.execute(
                "update %s set result_nvc = 'error', testDate_date = GETDATE(), caseTotal_i=%s where id_pk = %s" %
                (self.tableEF, d_param['caseTotal'], d_param['id_pk'])
            )
