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

from EfrbPO import *
Efrb_PO = EfrbPO()


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

    def str2dict_or(self, f_conditions):
        # 字符串转字典，将 （TZ_STZB042 = '是' and TZ_JWJB001 = '否' ） 转为字典{'TZ_STZB042': '是', 'TZ_JWJB001': '否'}
        pairs = [pair.strip() for pair in f_conditions.split('or')]
        d_conditions = {}
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=')
                d_conditions[key.strip()] = value.strip().replace("'", "")
        # print(d_conditions) # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
        return d_conditions



    # todo 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)
    def HIRB(self, varTestID, d_param={}):

        # 健康干预规则库（其他分类）Health Intervention Rule Base (Other Categories)
        # a_weight10_HIRB

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_code, f_conditions from %s" % (self.tableHI))
        # print("l_d_row => ", l_d_row)
        if varTestID == "all":
            self._HIRB(d_param)
        elif varTestID > len(l_d_row) or varTestID <= 0:
            print("[Error] 输入的ID超出" + str(len(l_d_row)) + "条范围")
            sys.exit(0)
        else:
            self._HIRB2(varTestID, d_param)

    def _HIRB(self, d_param):

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_code, f_conditions from %s" % (self.tableHI))
        # print("l_d_row => ", l_d_row)

        # d_['table'] = self.tableHI

        for i,index in enumerate(l_d_row):
            ID = l_d_row[i]['ID']
            f_code = l_d_row[i]['f_code']
            f_conditions = l_d_row[i]['f_conditions']

            # 测试项
            d_param['表'] = self.tableHI
            d_param['ID'] = ID
            # d_conditions = self.str2dict(f_conditions)
            # d_param['f_conditions'] = d_conditions
            d_param['f_conditions'] = f_conditions
            d_param['f_code'] = f_code
            d_param['表注释'] = '测试健康干预规则库'
            s = "测试项 => " + str(d_param)
            Color_PO.outColor([{"35": s}])
            Log_PO.logger.info(s)

            # todo TZ_STZB043='是' or TZ_STZB044='是' or TZ_STZB045='是'
            if "or" in f_conditions and "and" not in f_conditions:

                # 字符串转列表
                l_conditions = f_conditions.split("or")
                # print(l_conditions) # ["TZ_STZB043='是' ", " TZ_STZB044='是'  ", " TZ_STZB045='是'"]
                l_d_conditions = []
                for i in l_conditions:
                    l_d_conditions.append(self.str2dict(i))
                # print(1614, l_d_conditions)  # [{'TZ_STZB043': '是'}, {'TZ_STZB044': '是'}, {'TZ_STZB045': '是'}]
                d_param['l_d_conditions'] = l_d_conditions

                self.HIRB_case_or(d_param)


            # todo HIRB  (TZ_STZB002='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否') or (TZ_STZB005='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否')
            elif "or" in f_conditions and "and" in f_conditions:

                # 转换列表，结构化原始数据为列表，生成l_l_N
                l_conditions = f_conditions.split("or")
                # print(l_value)
                l_d_conditions = []
                for i in l_conditions:
                    i = i.replace("(",'').replace(")",'')
                    l_d_conditions.append(self.str2dict(i))

                d_param['l_d_conditions'] = l_d_conditions
                self.HIRB_case_or(d_param)



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

    def _HIRB2(self, varTestID, d_param):

        # 获取每行测试数据
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_code, f_conditions from %s" % (self.tableHI))
        # print("l_d_row => ", l_d_row)

        # d_['table'] = self.tableHI

        for i in enumerate(l_d_row):
            i = varTestID - 1
            ID = l_d_row[i]['ID']
            f_code = l_d_row[i]['f_code']
            f_conditions = l_d_row[i]['f_conditions']

            # 测试项
            d_param['表'] = self.tableHI
            d_param['ID'] = ID
            # d_conditions = self.str2dict(f_conditions)
            # d_param['f_conditions'] = d_conditions
            d_param['f_conditions'] = f_conditions
            d_param['f_code'] = f_code
            d_param['表注释'] = '测试健康干预规则库'
            s = "测试项 => " + str(d_param)
            Color_PO.outColor([{"35": s}])
            Log_PO.logger.info(s)

            # todo TZ_STZB043='是' or TZ_STZB044='是' or TZ_STZB045='是'
            if "or" in f_conditions and "and" not in f_conditions:

                # 字符串转列表
                l_conditions = f_conditions.split("or")
                # print(l_conditions) # ["TZ_STZB043='是' ", " TZ_STZB044='是'  ", " TZ_STZB045='是'"]
                l_d_conditions = []
                for i in l_conditions:
                    l_d_conditions.append(self.str2dict(i))
                # print(1614, l_d_conditions)  # [{'TZ_STZB043': '是'}, {'TZ_STZB044': '是'}, {'TZ_STZB045': '是'}]
                d_param['l_d_conditions'] = l_d_conditions
                # print(1624, d_param)

                self.HIRB_case_or(d_param)
                # self.HIRB_case_or(ID, f_code, l_d_conditions)


            # todo HIRB  (TZ_STZB002='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否') or (TZ_STZB005='是' and TZ_JWJB002='是' and TZ_RQFL005='否' and TZ_RQFL006='否')
            elif "or" in f_conditions and "and" in f_conditions:

                # 转换列表，结构化原始数据为列表，生成l_l_N
                l_conditions = f_conditions.split("or")
                # print(l_value)
                l_d_conditions = []
                for i in l_conditions:
                    i = i.replace("(",'').replace(")",'')
                    l_d_conditions.append(self.str2dict(i))

                d_param['l_d_conditions'] = l_d_conditions
                self.HIRB_case_or(d_param)


            # todo HIRB "TZ_RQFL001='是' and TZ_STZB001='是' and TZ_JB001='否' and TZ_JB002='否'"
            elif "and" in f_conditions:
                # 测试数据
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
        # print(d_param)
        # 生成EFRB参数 d_param_EFRB
        d_param_EFRB = {}

        # print(d_param['f_conditions'])
        if 'or' in d_param['f_conditions'] and 'and' not in d_param['f_conditions']:
            d_param['f_conditions'] = self.str2dict_or(d_param['f_conditions'])
            # print(d_param)
        elif 'and' not in d_param['f_conditions']:
            key, value = d_param['f_conditions'].split('=')
            result = {key: value.strip("'")}
            # print(result)  # 输出: {'TZ_RQFL005': '是'}
            d_param['f_conditions'] = result
            # 过滤评估因素规则（过滤掉TZ_STZB开头的key）
        elif 'and' in d_param['f_conditions']:
            d_param['f_conditions'] = self.str2dict(d_param['f_conditions'])

        d_filtered = {key: value for key, value in d_param['f_conditions'] .items() if 'TZ_STZB' not in key}
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
        # print(1800, l_matching_keys) # ['TZ_STZB001']
        if l_matching_keys != []:
            # print(l_1) # [{'ID': '3'}]
            # d_param['ID']
            d_1 = {}
            if len(l_matching_keys) == 1:
                l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[0]))
                d_1['table'] = self.tableEF
                d_1['ID'] = l_1[0]['ID']
                d_1.update(d_param_EFRB)
                # print(l_1[0]['ID'], d_param)
                # print(1714, l_1[0]['ID'])
                # print(1671)
                # d_param_EFRB['ID'] = l_1[0]['ID']
                # self.EFRB_1(d_1)
                Efrb_PO.EFRB(d_1['ID'], d_1)
            else:
                # for i in range(len(l_matching_keys)):
                #     l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[i]))
                #     d_param_EFRB['ID'] = l_1[0]['ID']
                #     self.EFRB_1(d_param_EFRB)
                # print(1816, i )

                print("warning, 匹配到多个值1：", l_matching_keys)
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
                    # self.EFRB_1(d_param_EFRB)
                    Efrb_PO.EFRB(d_param_EFRB['ID'], d_param_EFRB)

                else:
                    print("warning, 匹配到多个值2：", l_matching_keys)
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
                    # self.EFRB_1(d_param_EFRB)
                    Efrb_PO.EFRB(d_param_EFRB['ID'], d_param_EFRB)

                else:
                    print("warning, 匹配到多个值3：", l_matching_keys)
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

    def HIRB_case_or(self, d_param):

        # 执行ER中规则
        # ID, f_code, l_4

        # print("f_code", f_code)  # TZ_YS001
        # print("d_conditions", d_conditions)  # {'TZ_RQFL001': '是', 'TZ_STZB001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}

        d_tmp = {}

        # 遍历a_weight10_EFRB
        l_f_code = Sqlserver_PO_CHC5G.select("select ID, f_code from a_weight10_EFRB")
        # print(l_f_code)
        d_f_code = {item['ID']: item['f_code'] for item in l_f_code}
        # print(d_f_code)  # {1: 'TZ_STZB001', 2: 'TZ_STZB002', ...
        d_f_code = {v: k for k, v in d_f_code.items()}
        # print(d_f_code)  # {'TZ_STZB001': 1, 'TZ_STZB002': 2,

        sum = 0

        for d_ in d_param['l_d_conditions']:

            #  过滤掉TZ_STZB开头的key
            d_filtered = {key: value for key, value in d_.items() if 'TZ_STZB' not in key}
            # print("过滤掉TZ_STZB开头的key：", d_filtered) # {'TZ_RQFL001': '是', 'TZ_JWJB001': '否', 'TZ_JWJB002': '否'}
            # 先遍历否
            # 定义遍历顺序
            order = ['否', '是']

            # 按照定义的顺序遍历字典
            d_param_EFRB = {}
            for value in order:
                for key, val in d_filtered.items():
                    if val == value:
                        # print(f"键: {key}, 值: {val}")
                        l_ = Sqlserver_PO_CHC5G.select("select f_conditions from a_weight10_EFRB where f_code='%s'" % (key))
                        # print(l_) # [{'f_conditions': '3'}]
                        if val == "否" and "TZ_RQFL" in key:
                            d_param_EFRB['categoryCode'] = 100
                        if key == 'TZ_JB001' and val == "否":
                            d_param_EFRB['disease'] = "脑卒中"
                        if key == 'TZ_JB002' and val == "否":
                            d_param_EFRB['disease'] = "脑卒中"
                        if val == "是" and "TZ_RQFL" in key:
                            d_param_EFRB['categoryCode'] = int(l_[0]['f_conditions'])
                        if key == 'TZ_JB001' and val == "是":
                            d_param_EFRB['disease'] = l_[0]['f_conditions']
                        if key == 'TZ_JB002' and val == "是":
                            d_param_EFRB['disease'] = l_[0]['f_conditions']
                    if key == "性别":
                        d_param_EFRB['sex'] = val

            if "categoryCode" not in d_param_EFRB:
                d_param_EFRB['categoryCode'] = 100
            if "disease" not in d_param_EFRB:
                d_param_EFRB['disease'] = "脑卒中"
            if "sex" not in d_param_EFRB:
                d_param_EFRB['sex'] = "男"

            # print(d_param_EFRB)  # {'sex': '女', 'categoryCode': 3, 'disease': '脑卒中'}


            # 获取 TZ_STZB开头的key
            l_matching_keys = [key for key in d_ if 'TZ_STZB' in key]
            # print(l_matching_keys) # ['TZ_STZB001']
            if l_matching_keys != []:
                l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[0]))
                d_1 = {}
                d_1['table'] = 'a_weight10_EFRB'
                if len(l_matching_keys) == 1:
                    # print(l_1[0]['ID'], d_param)
                    d_1['ID'] = l_1[0]['ID']
                    d_1.update(d_param_EFRB)

                    # print(1958, d_1)  # {'table': 'a_weight10_EFRB', 'ID': 43, 'categoryCode': 100, 'disease': '脑卒中', 'sex': '男'}

                    Efrb_PO.EFRB(d_1['ID'], d_1)

                else:
                    print("warning, 匹配到多个值4：", l_matching_keys)
                    sys.exit(0)

            else:
                # # 匹配人群分类
                l_matching_keys = [key for key in d_ if 'TZ_RQFL' in key]
                if l_matching_keys != []:
                    l_1 = Sqlserver_PO_CHC5G.select("select ID from a_weight10_EFRB where f_code='%s'" % (l_matching_keys[0]))
                    d_1 = {}
                    d_1['table'] = 'a_weight10_EFRB'
                    if len(l_matching_keys) == 1:
                        # print(l_1[0]['ID'], d_param)
                        d_1['ID'] = l_1[0]['ID']
                        d_1.update(d_param_EFRB)

                        Efrb_PO.EFRB(d_1['ID'], d_1)
                    else:
                        print("warning, 匹配到多个值5：", l_matching_keys)
                        sys.exit(0)

            # 检查是否命中f_code
            sql = "select RULE_CODE from T_ASSESS_RULE_RECORD where WEIGHT_REPORT_ID = 2"
            l_d_RULE_CODE_actual = Sqlserver_PO_CHC.select(sql)
            l_d_RULE_CODE_actual = [item['RULE_CODE'] for item in l_d_RULE_CODE_actual]
            # print(l_d_RULE_CODE_actual) # ['TZ_STZB001', 'TZ_RQFL001', 'TZ_SRL001', 'TZ_MBTZ002', 'TZ_YD001', 'TZ_YS001']

            d_tmp['实际值'] = l_d_RULE_CODE_actual
            d_tmp['预期值'] = d_param['f_code']
            d_tmp['sql__T_ASSESS_RULE_RECORD'] = sql
            d_result = {}
            d_result['表'] = self.tableHI
            d_result['ID'] = d_param['ID']
            if d_tmp['预期值'] in l_d_RULE_CODE_actual:
                # s_print = "[正向ok], 既往疾病包含：" + str(varDisease)
                d_result['result'] = "ok"
                d_result.update(d_tmp)
                Color_PO.outColor([{"34": d_result}])
                Log_PO.logger.info(d_result)
                sum = sum + 1
            else:
                d_result['result'] = "error"
                Color_PO.outColor([{"31": d_result}])
                Log_PO.logger.info(d_result)
                s_tmp = str(d_tmp)
                s_tmp = s_tmp.replace("\\\\","\\")
                Color_PO.outColor([{"31": s_tmp}])
                sum = sum + 0

        d_1 = {}
        d_1['表'] = self.tableHI
        d_1['表注释'] = "健康干预规则库（其他分类）HIRB"
        d_1['ID'] = d_param['ID']
        if sum == len(d_param['l_d_conditions']):
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE()  where ID = %s" % (self.tableHI, d_param['ID']))
            d_1['result'] = "ok"
            d_1.update(d_tmp)
            Color_PO.outColor([{"32": "结果 => " + str(d_1)}])
        else:
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where ID = %s" % (self.tableHI, d_param['ID']))
            d_1['result'] = "error"
            d_1.update(d_tmp)
            Color_PO.outColor([{"31": "结果 => " + str(d_1)}])
        Log_PO.logger.info(d_1)




