# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0 - 健康干预 Health Intervention  Rule Base
# 需求：体重管理1.18
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r

# 数据源：weight10.xlsx - a_weight10_HIRB 导入数据库
# 测试数据库表：CHC-5G - a_weight10_HIRB
# 测试数据：CHC - WEIGHT_REPORT(体重报告记录表) - ID=2的记录
# 比对规则：CHC-5G - T_ASSESS_RULE_RECORD

# 警告如下：D:\dwp_backup\python study\GUI_wxpython\lib\site-packages\openpyxl\worksheet\_reader.py:312: UserWarning: Unknown extension is not supported and will be removed warn(msg)
# 解决方法：
import warnings
warnings.simplefilter("ignore")
#***************************************************************
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO_CHC = SqlserverPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database2"))

from AgePO import *
Age_PO = AgePO()

from BmiPO import *
Bmi_PO = BmiPO()

from BmiAgePO import *
BmiAge_PO = BmiAgePO()

from AgeBmiSexPO import *
AgeBmiSex_PO = AgeBmiSexPO()

from PO.ColorPO import *
Color_PO = ColorPO()

from EfrbPO import *
Efrb_PO = EfrbPO()



class HirbPO():

    def __init__(self):
        self.tableEFRB = Configparser_PO.DB("tableEFRB")
        self.tableHIRB = Configparser_PO.DB("tableHIRB")
        self.tableCommon = '健康干预HIRB => '
        self.testData = '正反测试数据 => '

        # 检查身份证是否存在, WEIGHT_REPORT(体重报告记录表)
        # 和QYYH中都必须要有此身份证，且在WEIGHT_REPORT表中获取ID
        self.IDCARD, self.WEIGHT_REPORT__ID = Efrb_PO.getIdcard()
        Color_PO.outColor([{"30": "QYYH__SFZH =>"}, {"35": self.IDCARD}, {"30": ", WEIGHT_REPORT__ID =>"}, {"35": self.WEIGHT_REPORT__ID}, ])

    def excel2db_HIRB(self):

        # excel文件导入db

        # 1，db中删除已有的表
        Sqlserver_PO_CHC.execute("drop table if exists " + self.tableHIRB)

        # 2，读取 Excel 文件
        df = pd.read_excel(Configparser_PO.FILE("case"), sheet_name=Configparser_PO.FILE("sheetHIRB"))
        df = df.sort_index()  # 按行索引排序，保持Excel原有顺序
        df = df.dropna(how="all")  # 移除全空行
        # 手动设置字段类型
        # df['conditions'] = df['conditions'].astype(str)  # 改为字符串类型

        # 3，Excel导入db
        Sqlserver_PO_CHC.df2db(df, self.tableHIRB)

        # 4, 设置表注释
        Sqlserver_PO_CHC.setTableComment(self.tableHIRB, '体重管理_健康干预规则库(测试)')

        # 5，将conditions字段替换换行符为空格
        Sqlserver_PO_CHC.execute("UPDATE %s SET conditions = REPLACE(REPLACE(conditions, CHAR(10), ' '), CHAR(13), ' ');" % (self.tableHIRB))

        # 6，设置字段类型与备注
        field_definitions = [
            ('f_type', 'nvarchar(50)', '干预项目分类'),
            ('IR_code', 'nvarchar(20)', '干预规则编码'),
            ('conditions', 'nvarchar(max)', '干预规则'),
            ('IR_detail', 'nvarchar(500)', '干预规则描述'),
            ('totalCase', 'int', '用例合计数'),
            ('log', 'varchar(max)', '日志信息'),
            ('updateDate', 'nvarchar(50)', '更新日期'),
            ('result', 'nvarchar(10)', '测试结果')
        ]
        for field_name, field_type, comment in field_definitions:
            Sqlserver_PO_CHC.setFieldTypeComment(self.tableHIRB, field_name, field_type, comment)

        # 7，修改字段类型为日期类型
        Sqlserver_PO_CHC.execute("ALTER TABLE %s ALTER COLUMN updateDate DATE;" % (self.tableHIRB))

        # 8，设置id自增主键（放在最后）
        Sqlserver_PO_CHC.setIdentityPrimaryKey(self.tableHIRB, "id")


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


    def str2dict(self, conditions):
        # 字符串转字典，将 （TZ_STZB042 = '是' and TZ_JWJB001 = '否' ） 转为字典{'TZ_STZB042': '是', 'TZ_JWJB001': '否'}
        pairs = [pair.strip() for pair in conditions.split('and')]
        d_conditions = {}
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=')
                d_conditions[key.strip()] = value.strip().replace("'", "")
        # print(d_conditions) # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        return d_conditions
    def str2dict_or(self, conditions):
        # 字符串转字典，将 （TZ_STZB042 = '是' and TZ_JWJB001 = '否' ） 转为字典{'TZ_STZB042': '是', 'TZ_JWJB001': '否'}
        pairs = [pair.strip() for pair in conditions.split('or')]
        d_conditions = {}
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=')
                d_conditions[key.strip()] = value.strip().replace("'", "")
        # print(d_conditions) # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        return d_conditions


    def HIRB(self, object=None, d_param={}):
        # 入口

        if object == None:
            # todo 执行所有
            self.HIRB_all()
        elif isinstance(object, list):
            # todo 执行连续 [起始，步长]
            self.HIRB_area(object, d_param)
        elif isinstance(object, dict):
            if 'id' in object:
                # 执行多条
                if isinstance(object['id'], list):
                    # todo 执行多条
                    self.HIRB_multiple(object, d_param)
                else:
                    # 执行一条
                    # 判断id是否溢出
                    l_d_row = Sqlserver_PO_CHC.select("select * from %s" % (self.tableHIRB))
                    i_records = len(l_d_row)
                    if object['id'] > i_records or object['id'] <= 0:
                        # 异常退出
                        print("[Error] 输入的ID超出" + str(i_records) + "条范围！")
                        sys.exit(0)
                    else:
                        # todo 执行一条
                        self.HIRB_one(object, d_param)
            elif 'IR_code' in object:
                # 执行多条
                if isinstance(object['IR_code'], list):
                    self.HIRB_multiple(object, d_param)
                else:
                    # 执行一条
                    self.HIRB_one(object, d_param)
            else:
                print("[Error] 参数中没有id或IR_code！")
                sys.exit(0)

        # 由于健康干预模块，需要返回结果
        return self.WEIGHT_REPORT__ID

    def _HIRB_one(self, l_d_row):
        # _HIRB_one内部调用

        d_tmp = {
            'IR_code': l_d_row[0]['IR_code'],
            'id': l_d_row[0]['id'],
            'conditions': l_d_row[0]['conditions']
        }
        # 健康干预HIRB =>
        # d_tmp = {'IR_code': 'TZ_STZB046', 'id': 59, 'conditions': '(73月<=年龄<79月 and 17.1<=BMI and 性别=男) or (79月<=年龄＜84月 and 17.2<=BMI and 性别=男) or (73月<=年龄＜79月 and 16.6<=BMI and 性别=女) or (79月<=年龄＜84月 and 16.7<=BMI and 性别=女)', 'IDCARD': '310101193012210813'}
        s = self.tableCommon + str(d_tmp)
        Color_PO.outColor([{"30": s}])

        # 写入日志
        Log_PO.logger.info(s)

        # self.HIRB_conditions(d_tmp)
        # todo 执行一条
        self._HIRB_main(d_tmp)
    def HIRB_one(self, d_, d_param):
        # 执行一条
        # d_ = {'id': 56}
        # d_ = {'IR_code': 'TZ_STZB047'}
        # d_ = {'id': 59, 'ER_code': 'TZ_STZB047'}

        if "id" in d_:
            # 获取数据
            l_d_row = Sqlserver_PO_CHC.select(
                "select id, conditions, IR_code from %s where id=%s" % (self.tableHIRB, d_['id']))
            self._HIRB_one(l_d_row)
        if 'IR_code' in d_:
            # 获取数据
            l_d_row = Sqlserver_PO_CHC.select(
                "select id, conditions, IR_code from %s where IR_code='%s'" % (self.tableHIRB, d_['IR_code']))
            self._HIRB_one(l_d_row)
    def HIRB_area(self, l_, d_param):
        # l_= [起始，步长]
        # 执行多条(区间id)，如：{'id': [1, 3]} ,表示执行1，2，3 三条记录
        # 执行多条(区间ER_code)，如：{'ER_code': ['TZ_STZB046', 'TZ_STZB047']}

        # 执行多条(区间id)，如：{'id': [1, 3]} ,表示执行1，2，3 三条记录
        id1 = l_[0]
        step = l_[1]
        id2 = id1 + step

        l_d_row = Sqlserver_PO_CHC.select("select count(*) as qty from %s where id=%s" % (self.tableHIRB, id2))
        if l_d_row[0]['qty'] != 0:
            for id in list(range(id1, id2)):
                l_d_row = Sqlserver_PO_CHC.select(
                    "select id, conditions, IR_code from %s where id=%s" % (self.tableHIRB, id))
                self._HIRB_one(l_d_row)
        else:
            Color_PO.outColor([{"31": "[Error] 参数：[id起始，步长]，id起始 + 步长溢出!"}])
            sys.exit(0)
    def HIRB_multiple(self, d_, d_param):
        # 执行多条id 或 IR_code

        if 'IR_code' in d_:
            for IR_code in d_['IR_code']:
                l_d_row = Sqlserver_PO_CHC.select(
                    "select id, conditions, IR_code from %s where IR_code='%s'" % (self.tableHIRB, IR_code))
                self._HIRB_one(l_d_row)
        if 'id' in d_:
            # 判断id是否溢出
            if d_['id'][0] < 1 or d_['id'][0] > d_['id'][1]:
                print("[Error] 请输入正确的id区间!")
                sys.exit(0)

            for id in d_['id']:
                l_d_row = Sqlserver_PO_CHC.select(
                    "select id, conditions, IR_code from %s where id=%s" % (self.tableHIRB, id))
                self._HIRB_one(l_d_row)

    def HIRB_all(self):
        # 执行所有
        l_d_row = Sqlserver_PO_CHC.select("select IR_code, id, conditions from %s" % (self.tableHIRB))

        for row in l_d_row:
            d_param = {
                'IR_code': row['ER_code'],
                'id': row['id'],
                'conditions': row['conditions'],
            }

            s = self.tableCommon + str(d_param)
            Color_PO.outColor([{"35": s}])
            Log_PO.logger.info(s)

            # self.HIRB_conditions(d_param)
            self._HIRB_main(d_param)


    # def HIRB(self, varTestID):
    #     # 入口
    #
    #     # 获取每行测试数据
    #     l_d_row = Sqlserver_PO_CHC.select("select id, IR_code, conditions from %s" % (self.tableHIRB))
    #     # print("l_d_row => ", l_d_row)
    #     if varTestID == "all":
    #         self._HIRB_All()
    #     elif varTestID > len(l_d_row) or varTestID <= 0:
    #         print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
    #         sys.exit(0)
    #     else:
    #         self._HIRB_ID(varTestID)

    # def _HIRB_All(self):
    #     # 执行所有
    #     d_param = {}
    #     l_d_row = Sqlserver_PO_CHC.select("select id, IR_code, conditions from %s" % (self.tableHIRB))
    #     for i, index in enumerate(l_d_row):
    #         d_param['IR_code'] = l_d_row[i]['IR_code']
    #         d_param['id'] = l_d_row[i]['id']
    #         d_param['conditions'] = l_d_row[i]['conditions']
    #         s = self.tableCommon + str(d_param)
    #         Color_PO.outColor([{"35": s}])
    #         Log_PO.logger.info(s)
    #
    #         # todo 执行所有
    #         self._HIRB_main(d_param)

    def _HIRB_ID(self, varTestID):
        # 执行一条
        d_param = {}
        l_d_row = Sqlserver_PO_CHC.select("select IR_code, conditions from %s where id =%s" % (self.tableHIRB, varTestID))
        d_param['IR_code'] = l_d_row[0]['IR_code']
        d_param['id'] = varTestID
        d_param['conditions'] = l_d_row[0]['conditions']
        s = self.tableCommon + str(d_param)
        Color_PO.outColor([{"35": s}])
        Log_PO.logger.info(s)

        # todo 执行一条
        self._HIRB_main(d_param)

    def _HIRB_main(self, d_param):
        # todo 无组有or TZ_STZB043='是' or TZ_STZB044='是' or TZ_STZB045='是'
        if "or" in d_param['conditions'] and "and" not in d_param['conditions']:

            # 字符串转列表
            l_conditions = d_param['conditions'].split("or")
            # print(l_conditions) # ["TZ_STZB043='是' ", " TZ_STZB044='是'  ", " TZ_STZB045='是'"]
            l_d_conditions = []
            for i in l_conditions:
                l_d_conditions.append(self.str2dict(i))
            # print(1614, l_d_conditions)  # [{'TZ_STZB043': '是'}, {'TZ_STZB044': '是'}, {'TZ_STZB045': '是'}]
            d_param['l_d_conditions'] = l_d_conditions
            # print(1624, d_param)

            self.HIRB_case_or(d_param)
            # self.HIRB_case_or(ID, IR_code, l_d_conditions)

        # todo 多组有or  (TZ_STZB002='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否') or (TZ_STZB005='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否')
        elif "or" in d_param['conditions'] and "and" in d_param['conditions']:
            self.HIRB_case_or(d_param)

        # todo 一组无or "TZ_RQFL001='是' and TZ_STZB001='是' and TZ_JB001='否' and TZ_JB002='否'"
        elif "and" in d_param['conditions']:
            # 测试数据
            self.HIRB_case(d_param)

        # todo 无组无or 年龄，人群分类，疾病， TZ_RQFL005='是'
        elif "and" not in d_param['conditions']:
            self.HIRB_case(d_param)


    def HIRB_case(self, d_param):

        # 执行ER中规则

        d_tmp = {}
        d_param_EFRB = {}

        # 格式化干预规则（conditions）
        # 字符串转字典
        if 'or' in d_param['conditions'] and 'and' not in d_param['conditions']:
            d_param['conditions'] = self.str2dict_or(d_param['conditions'])
        elif 'and' not in d_param['conditions']:
            key, value = d_param['conditions'].split('=')
            result = {key: value.strip("'")}
            # print(result)  # 输出: {'TZ_RQFL005': '是'}
            d_param['conditions'] = result
        elif 'and' in d_param['conditions']:
            d_param['conditions'] = self.str2dict(d_param['conditions'])

        # print(304,d_param)  # {'IR_code': 'TZ_YS001', 'id': 1, 'conditions': {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JB001': '否', 'TZ_JB002': '否'}}

        # （写死TZ_JB001=高血压、TZ_JB002=糖尿病）
        gxy = d_param['conditions']['TZ_JB001']
        tnb = d_param['conditions']['TZ_JB002']
        if gxy == '否' and tnb == '否':
            # 不是高血压也不是糖尿病
            d_param_EFRB['disease'] = "无"
        elif gxy == '是' and tnb == '是':
            # 如果既是高血压也是糖尿病，则取糖尿病
            d_param_EFRB['disease'] = "糖尿病"
        elif gxy == '是' and tnb == '否':
            # 如果是高血压，不是糖尿病
            d_param_EFRB['disease'] = "高血压"
        elif gxy == '否' and tnb == '是':
            # 如果是糖尿病，不是高血压
            d_param_EFRB['disease'] = "糖尿病"

        # print(323, d_param_EFRB)  # 339 {'disease': '高血压' }


        # 获取 TZ_STZB 开头的评估规则编码，如：ER_code = TZ_STZB001
        # 通过TZ_STZB001 获取评估因素规则库EFRB中id
        l_matching_keys = [key for key in d_param['conditions'] if 'TZ_STZB' in key]
        # print(1800, l_matching_keys) # ['TZ_STZB001']
        if l_matching_keys != []:
            # print(l_1) # [{'ID': '3'}]
            # d_param['id'] 
            d_1 = {}
            if len(l_matching_keys) == 1:
                l_1 = Sqlserver_PO_CHC.select("select id from %s where ER_code='%s'" % (self.tableEFRB, l_matching_keys[0]))
                # d_1['table'] = self.tableEFRB
                d_1['id'] = l_1[0]['id']
                d_1.update(d_param_EFRB)
                # print(339, 'a_weightAssessmentRule_EFRB =>', d_1)  # {'id': 1, 'disease': '无'}

                # 跑评估因素规则库
                WEIGHT_REPORT__ID = Efrb_PO.EFRB({'id': d_1['id']}, d_1)

            else:
                print("warning, 匹配到多个值1：", l_matching_keys)
                sys.exit(0)
        else:
            # 匹配人群分类
            l_matching_keys = [key for key in d_param['conditions'] if 'TZ_RQFL' in key]
            if l_matching_keys != []:
                l_1 = Sqlserver_PO_CHC.select("select id from %s where ER_code='%s'" % (self.tableEFRB, l_matching_keys[0]))
                if len(l_matching_keys) == 1:
                    # print(l_1[0]['ID'], d_param)
                    # self.EFRB_1(l_1[0]['ID'], d_4)
                    d_param_EFRB['id'] = l_1[0]['id']
                    # self.EFRB_1(d_param_EFRB)
                    Efrb_PO.EFRB(d_param_EFRB['id'], d_param_EFRB)

                else:
                    print("warning, 匹配到多个值2：", l_matching_keys)
                    sys.exit(0)

            # 匹配年龄
            l_matching_keys = [key for key in d_param['conditions'] if 'TZ_AGE' in key]
            # print(l_matching_keys)  # ['TZ_STZB001']
            if l_matching_keys != []:
                l_1 = Sqlserver_PO_CHC.select("select id from %s where ER_code='%s'" % (self.tableEFRB, l_matching_keys[0]))
                if len(l_matching_keys) == 1:
                    # print(l_1[0]['ID'], d_param)
                    # self.EFRB_1(l_1[0]['ID'], d_4)
                    d_param_EFRB['id'] = l_1[0]['id']
                    # self.EFRB_1(d_param_EFRB)
                    # print(382, d_param_EFRB)
                    Efrb_PO.EFRB(d_param_EFRB['id'], d_param_EFRB)

                else:
                    print("warning, 匹配到多个值3：", l_matching_keys)
                    sys.exit(0)

        # 检查是否命中IR_code
        sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = %s" % (WEIGHT_REPORT__ID)
        l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)

        l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
        # print(l_d_RULE_CODE_actual)  # ['TZ_STZB001', 'TZ_RQFL001', 'TZ_SRL001', 'TZ_MBTZ002', 'TZ_YD001', 'TZ_YS001']
        d_tmp['预期值'] = d_param['IR_code']
        d_tmp['实际值'] = l_d_RULE_CODE_actual
        d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
        l_count = []
        d_result = {}
        # print(d_tmp)
        d_1 = {}
        # d_1['表'] = self.tableHIRB

        if d_tmp['预期值'] in d_tmp['实际值']:
            # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
            # Color_PO.outColor([{"34": d_tmp}])
            # Log_PO.logger.info(d_tmp)
            d_1['result'] = "ok"
            d_1['IR_code'] = d_param['IR_code']
            d_1['id'] = d_param['id']
            # d_1.update(d_tmp)
            s = self.tableCommon + str(d_1)
            Color_PO.outColor([{"32": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC.execute("update %s set result = 'ok', updateDate = GETDATE()  where id = %s" % (self.tableHIRB, d_param['id'] ))
        else:
            d_1['result'] = "error"
            d_1['IR_code'] = d_param['IR_code']
            d_1['id'] = d_param['id']
            d_1['IDCARD'] = self.IDCARD
            d_1.update(d_tmp)
            s = self.tableCommon + str(d_1)
            Color_PO.outColor([{"31": s}])
            Log_PO.logger.info(s)
            Sqlserver_PO_CHC.execute("update %s set result = 'error', updateDate = GETDATE() where id = %s" % (self.tableHIRB, d_param['id'] ))
        print("-".center(100, "-"))

    def HIRB_case_or(self, d_param):

        # 执行ER中规则

        # print("IR_code", IR_code)  # TZ_YS001
        # print("d_conditions", d_conditions)  # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}

        # 格式化干预规则（conditions）
        # 字符串转列表
        l_conditions = d_param['conditions'].split("or")
        l_d_conditions = []
        for i in l_conditions:
            i = i.replace("(", '').replace(")", '')
            l_d_conditions.append(self.str2dict(i))

        print(435, l_d_conditions)  # [{'TZ_STZB002': '是', 'TZ_JB002': '是', 'TZ_RQFL005': '否', 'TZ_RQFL006': '否'}, {'TZ_STZB005': '是', 'TZ_JB002': '是', 'TZ_RQFL005': '否', 'TZ_RQFL006': '否'}]
                                    # [{'TZ_STZB043': '是'}, {'TZ_STZB044': '是'}, {'TZ_STZB045': '是'}]

        d_tmp = {}

        # # 遍历获取EFRB的字典映射{id：ER_code}
        # l_IR_code = Sqlserver_PO_CHC.select("select id, ER_code from %s" % (self.tableEFRB))
        # print(473, l_IR_code)
        # d_IR_code = {item['id']: item['ER_code'] for item in l_IR_code}
        # # print(d_IR_code)  # {1: 'TZ_STZB001', 2: 'TZ_STZB002', ...
        # d_IR_code = {v: k for k, v in d_IR_code.items()}
        # # print(d_IR_code)  # {'TZ_STZB001': 1, 'TZ_STZB002': 2,

        sum = 0
        d_param_EFRB = {}

        # （写死TZ_JB001=高血压、TZ_JB002=糖尿病）成堆出现
        if any('TZ_JB001' in item for item in l_d_conditions):
            gxy = l_d_conditions[0]['TZ_JB001']
            tnb = l_d_conditions[0]['TZ_JB002']
            if gxy == '否' and tnb == '否':
                # 不是高血压也不是糖尿病
                d_param_EFRB['disease'] = "无"
            elif gxy == '是' and tnb == '是':
                # 如果既是高血压也是糖尿病，则取糖尿病
                d_param_EFRB['disease'] = "糖尿病"
            elif gxy == '是' and tnb == '否':
                # 如果是高血压，不是糖尿病
                d_param_EFRB['disease'] = "高血压"
            elif gxy == '否' and tnb == '是':
                # 如果是糖尿病，不是高血压
                d_param_EFRB['disease'] = "糖尿病"

        # if '性别' in l_d_conditions:
        #     d_param_EFRB['sexCode'] =

        # print(323, d_param_EFRB)  # 339 {'disease': '高血压' }

        # # 遍历评估因素规则库编码，如 [{'TZ_STZB043': '是'}, {'TZ_STZB044': '是'}, {'TZ_STZB045': '是'}]
        # for d_ in l_d_conditions:
        #
        #     #  过滤掉TZ_STZB开头的key
        #     d_filtered = {key: value for key, value in d_.items() if 'TZ_STZB' not in key}
        #     print("过滤掉TZ_STZB开头的key：", d_filtered) # {'TZ_RQFL001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        #     # 先遍历否
        #     # 定义遍历顺序
        #     order = ['否', '是']
        #
        #     # 按照定义的顺序遍历字典
        #     d_param_EFRB = {}
        #     for value in order:
        #         for key, val in d_filtered.items():
        #             if val == value:
        #                 # print(f"键: {key}, 值: {val}")
        #                 l_ = Sqlserver_PO_CHC.select("select conditions from %s where ER_code='%s'" % (self.tableEFRB, key))
        #                 # print(l_) # [{'conditions': '3'}]
        #                 if val == "否" and "TZ_RQFL" in key:
        #                     d_param_EFRB['categoryCode'] = 100
        #                 if key == 'TZ_JB001' and val == "否":
        #                     d_param_EFRB['disease'] = "脑卒中"
        #                 if key == 'TZ_JB002' and val == "否":
        #                     d_param_EFRB['disease'] = "脑卒中"
        #                 if val == "是" and "TZ_RQFL" in key:
        #                     d_param_EFRB['categoryCode'] = int(l_[0]['conditions'].split("=")[1])
        #                 if key == 'TZ_JB001' and val == "是":
        #                     d_param_EFRB['disease'] = l_[0]['conditions']
        #                 if key == 'TZ_JB002' and val == "是":
        #                     d_param_EFRB['disease'] = l_[0]['conditions']
        #             if key == "性别":
        #                 d_param_EFRB['sex'] = val
        #
        #     if "categoryCode" not in d_param_EFRB:
        #         d_param_EFRB['categoryCode'] = 100
        #     if "disease" not in d_param_EFRB:
        #         d_param_EFRB['disease'] = "脑卒中"
        #     if "sex" not in d_param_EFRB:
        #         d_param_EFRB['sex'] = "男"

        print(521, d_param_EFRB)  # {'sex': '女', 'categoryCode': 3, 'disease': '脑卒中'}

        # 遍历l_conditions   jinhao
        # ？？？
        # ???
        # 如果TZ_STZB开头，如果有TZ_RQFL001，如果有

        # 获取 TZ_STZB开头的key
        # l_d_conditions
        # l_matching_keys = [key for key in l_d_conditions[0] if 'TZ_STZB' in key]
        l_matching_keys = [key for item in l_d_conditions for key in item.keys() if key.startswith('TZ_STZB')]

        print(515, l_matching_keys) # ['TZ_STZB001']
        if l_matching_keys != []:
            l_1 = Sqlserver_PO_CHC.select("select id from %s where ER_code='%s'" % (self.tableEFRB, l_matching_keys[0]))
            # print(222,l_1)
            d_1 = {}
            d_1['table'] = self.tableEFRB
            if len(l_matching_keys) == 1:
                # print(l_1[0]['id'], d_param)
                d_1['id'] = l_1[0]['id']
                d_1.update(d_param_EFRB)

                print(529, d_1)  # {'table': self.tableEFRB, 'ID': 43, 'categoryCode': 100, 'disease': '脑卒中', 'sex': '男'}

                # 跑评估因素规则库
                WEIGHT_REPORT__ID = Efrb_PO.EFRB({'id': d_1['id']}, d_1)
            else:
                for ER_code in l_matching_keys:
                    l_1 = Sqlserver_PO_CHC.select("select id from %s where ER_code='%s'" % (self.tableEFRB, ER_code))
                    d_1 = {}
                    d_1['table'] = self.tableEFRB
                    d_1['id'] = l_1[0]['id']
                    d_1.update(d_param_EFRB)
                    # print(542, d_1)  # {'table': 'a_weightAssessmentRule_EFRB', 'id': 3}
                    # 跑评估因素规则库
                    WEIGHT_REPORT__ID = Efrb_PO.EFRB({'id': d_1['id']}, d_1)



        # 获取 TZ_RQFL开头的key,匹配人群分类

        # l_matching_keys = [key for key in l_d_conditions[0] if 'TZ_STZB' in key]
        l_matching_keys = [key for item in l_d_conditions for key in item.keys() if key.startswith('TZ_RQFL')]
        # #
        # l_matching_keys = [key for key in d_ if 'TZ_RQFL' in key]
        if l_matching_keys != []:
            l_1 = Sqlserver_PO_CHC.select("select id from %s where ER_code='%s'" % (self.tableEFRB, l_matching_keys[0]))
            d_1 = {}
            d_1['table'] = self.tableEFRB
            if len(l_matching_keys) == 1:
                # print(l_1[0]['ID'], d_param)
                d_1['id'] = l_1[0]['id']
                d_1.update(d_param_EFRB)

                # Efrb_PO.EFRB(d_1['id'],d_1)
                WEIGHT_REPORT__ID = Efrb_PO.EFRB({'id': d_1['id']}, d_1)

            else:
                for ER_code in l_matching_keys:
                    l_1 = Sqlserver_PO_CHC.select("select id from %s where ER_code='%s'" % (self.tableEFRB, ER_code))
                    d_1 = {}
                    d_1['table'] = self.tableEFRB
                    d_1['id'] = l_1[0]['id']
                    d_1.update(d_param_EFRB)
                    # print(542, d_1)  # {'table': 'a_weightAssessmentRule_EFRB', 'id': 3}
                    # 跑评估因素规则库
                    WEIGHT_REPORT__ID = Efrb_PO.EFRB({'id': d_1['id']}, d_1)

        # 检查是否命中IR_code
        sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = %s" % (WEIGHT_REPORT__ID)
        l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
        l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
        # print(l_d_RULE_CODE_actual) # ['TZ_STZB001', 'TZ_RQFL001', 'TZ_SRL001', 'TZ_MBTZ002', 'TZ_YD001', 'TZ_YS001']

        d_tmp['预期值'] = d_param['IR_code']
        d_tmp['实际值'] = l_d_RULE_CODE_actual
        d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
        d_result = {}
        # d_result['表'] = self.tableHIRB
        # d_result['id'] = d_param['id']
        # d_result['IR_code'] = d_param['IR_code']
        if d_tmp['预期值'] in l_d_RULE_CODE_actual:
            # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
            d_result['result'] = 'ok'
            d_result['IR_code'] = d_param['IR_code']
            d_result['id'] = d_param['id']
            d_result.update(d_tmp)
            Color_PO.outColor([{"34": d_result}])
            Log_PO.logger.info(d_result)
            sum = sum + 1
        else:
            d_result['result'] = 'error'
            d_result['IR_code'] = d_param['IR_code']
            d_result['id'] = d_param['id']
            d_result.update(d_tmp)
            # Color_PO.outColor([{"31": d_result}])
            Log_PO.logger.info(d_result)
            s_tmp = str(d_result)
            s_tmp = s_tmp.replace("\\\\","\\")
            Color_PO.outColor([{"31": s_tmp}])
            sum = sum + 0

        d_1 = {}
        # d_1['表'] = self.tableHIRB
        # d_1['表注释'] = self.tableCommon
        # print(678, sum,len(l_d_conditions))
        # if sum == len(l_d_conditions):
        # if sum == len(d_param['l_d_conditions']):
        if d_result['result'] =='ok':
            Sqlserver_PO_CHC.execute("update %s set result = 'ok', updateDate = GETDATE()  where id = %s" % (self.tableHIRB, d_param['id'] ))
            d_1['result'] = 'ok'
            d_1['IR_code'] = d_param['IR_code']
            d_1['id'] = d_param['id']
            d_1.update(d_tmp)
            Color_PO.outColor([{"32": self.tableCommon + str(d_1)}])
        else:
            Sqlserver_PO_CHC.execute("update %s set result = 'error', updateDate = GETDATE() where id = %s" % (self.tableHIRB, d_param['id'] ))
            d_1['result'] = 'error'
            d_1['IR_code'] = d_param['IR_code']
            d_1['id'] = d_param['id']
            d_1['IDCARD'] = self.IDCARD
            d_1.update(d_tmp)
            Color_PO.outColor([{"31": self.tableCommon + str(d_1)}])
        Log_PO.logger.info(d_1)




