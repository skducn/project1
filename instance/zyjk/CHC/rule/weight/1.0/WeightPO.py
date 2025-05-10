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
Sqlserver_PO = SqlserverPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"))  # 测试环境

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

class WeightPO():


    def excel2db(self, varFile, varTable, varSheet="EFR"):

        # excel文件导入db

        # 1, db中删除已有的表
        Sqlserver_PO.execute("drop table if exists " + varTable)

        # 2, excel导入db
        Sqlserver_PO.xlsx2db(varFile, varTable, varSheet)

        # 3, 设置表注释
        Sqlserver_PO.setTableComment(varTable, '体重管理1.0评估因素判断规则自动化')

        # 4， 替换换行符为空格
        Sqlserver_PO.execute("UPDATE a_weight10 SET f_evaluationFactorJudgmentRules_N = REPLACE(REPLACE(f_evaluationFactorJudgmentRules_N, CHAR(10), ' '), CHAR(13), ' ');")

        # 5, 设置字段类型与描述
        Sqlserver_PO.setFieldTypeComment(varTable, 'f_result', 'varchar(50)', '结果')
        Sqlserver_PO.setFieldTypeComment(varTable, 'f_updateDate', 'varchar(50)', '更新日期')
        Sqlserver_PO.execute("ALTER TABLE %s ALTER COLUMN f_updateDate DATE;" % (varTable))
        Sqlserver_PO.setFieldTypeComment(varTable, 'f_type', 'varchar(50)', '分类')
        Sqlserver_PO.setFieldTypeComment(varTable, 'f_ruleName', 'varchar(100)', '规则名称')
        Sqlserver_PO.setFieldTypeComment(varTable, 'f_detailedDescription', 'varchar(999)', '评估规则详细描述')
        Sqlserver_PO.setFieldTypeComment(varTable, 'f_evaluationRuleCoding', 'varchar(50)', '评估规则编码')
        # # Sqlserver_PO.setFieldTypeComment(varTable, 'f_evaluationFactorJudgmentRules_O', 'varchar(999)', '评估因素判断规则_原始')  //不用，没处理。
        Sqlserver_PO.setFieldTypeComment(varTable, 'f_evaluationFactorJudgmentRules_N', 'varchar(8000)', '评估因素判断规则_自动化')

        # 6, 设置自增主键（最后）
        Sqlserver_PO.setIdentityPrimaryKey(varTable, "ID")

    def main(self, varTable, varRun='all'):

        if varRun != 'all':
            l_d_row = Sqlserver_PO.select("select * from %s where pResult != 'ok' or nResult != 'ok'" % (varTable))
            # print("l_d_row => ", l_d_row)

        else:
            l_d_row = Sqlserver_PO.select("select id,f_result,f_updateDate,f_ruleName,f_evaluationFactorJudgmentRules_N,f_evaluationRuleCoding from %s" % (varTable))
            # print("l_d_row => ", l_d_row)
            # [{'id': 1, 'f_result': None, 'f_updateDate': None, 'f_ruleName': '成人体重超重或肥胖',
            # 'f_evaluationFactorJudgmentRules_N': 'BMI>=24 and 年龄>=18 and 年龄<65', 'f_evaluationRuleCoding': 'TZ_STZB001'}, ...

        # 测试某条记录
        for i, index in enumerate(l_d_row):
            # i = 7
            id = l_d_row[i]['id']
            f_result = l_d_row[i]['f_result']
            f_updateDate = l_d_row[i]['f_updateDate']
            f_ruleName = l_d_row[i]['f_ruleName']
            f_evaluationFactorJudgmentRules_N = l_d_row[i]['f_evaluationFactorJudgmentRules_N']
            f_evaluationRuleCoding = l_d_row[i]['f_evaluationRuleCoding']

            # 获取原始数据
            Color_PO.outColor([{"34": "id:" + str(id) + ", f_evaluationFactorJudgmentRules_N:" + str(f_evaluationFactorJudgmentRules_N)}])
            # print("原始数据 >", f_evaluationFactorJudgmentRules_N)  # (14<= 年龄＜14.5 and 22.3<= BMI and 性别=男) or (14.5<= 年龄＜15 and 22.6<= BMI and 性别=男)

            # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
            f_evaluationFactorJudgmentRules_N = f_evaluationFactorJudgmentRules_N.replace("月", '')
            f_evaluationFactorJudgmentRules_N = f_evaluationFactorJudgmentRules_N.replace('＞', '>').replace('＜', '<').replace('＝', '=')
            f_evaluationFactorJudgmentRules_N = re.sub(r'\s*<=\s*', '<', f_evaluationFactorJudgmentRules_N)
            f_evaluationFactorJudgmentRules_N = re.sub(r'\s*<=\s*', '<=', f_evaluationFactorJudgmentRules_N)
            f_evaluationFactorJudgmentRules_N = re.sub(r'\s*<=\s*', '>', f_evaluationFactorJudgmentRules_N)
            f_evaluationFactorJudgmentRules_N = re.sub(r'\s*<=\s*', '>=', f_evaluationFactorJudgmentRules_N)
            f_evaluationFactorJudgmentRules_N = re.sub(r'\s*<=\s*', '=', f_evaluationFactorJudgmentRules_N)

            # 优先处理or，再处理and
            if "or" in f_evaluationFactorJudgmentRules_N:
                # print("[or]")

                # 结构化原始数据为列表，生成l_l_N
                l_N = f_evaluationFactorJudgmentRules_N.split("or")
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
                    varCount = self.checkRule3(d_cases['satisfied'][0], id, f_evaluationRuleCoding, varTable)
                    if varCount == 1:
                        print("ok > 条件：", lln, "，满足：", d_cases['satisfied'][0] , " > 命中。")

                        # 反向用例, 不满足条件的v[0]，预期不命中。
                        del d_cases['satisfied']
                        varCount = 2
                        for k, v in d_cases.items():
                            # print(v[0])
                            varCount = self.checkRule4(v[0], id, f_evaluationRuleCoding, varTable)
                            if varCount == 1:
                                # 反向如果命中就错，并且终止循环
                                print("error > 条件：", lln, "，不满足：", v[0], " > 命中！")
                                break
                            else:
                                print("ok > 条件：", lln, "，不满足：", v[0], " > 不命中。")
                                Ellipsis
                    else:
                        print("error > 条件：", lln, "，满足：", d_cases['satisfied'][0] , " > 不命中！")
                        Ellipsis
                        # Sqlserver_PO.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

                # 回写数据库f_resut, f_updateDate
                if varCount == 2:
                    print("ok")
                    Sqlserver_PO.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
                else:
                    print("error")
                    Sqlserver_PO.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

            elif "and" in f_evaluationFactorJudgmentRules_N:
                # print("[and]")
                l_N = f_evaluationFactorJudgmentRules_N.split("and")
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
                varCount = self.checkRule3(d_cases['satisfied'][0], id, f_evaluationRuleCoding, varTable)
                if varCount == 1:
                    print("ok > 条件：", l_N, "，满足：", d_cases['satisfied'][0], " > 命中。")

                    # 反向用例, 不满足条件的v[0]，预期不命中。
                    del d_cases['satisfied']
                    varCount = 2
                    for k, v in d_cases.items():
                        # print(v[0])
                        varCount = self.checkRule4(v[0], id, f_evaluationRuleCoding, varTable)
                        if varCount == 1:
                            # 反向如果命中就错，并且终止循环
                            print("error > 条件：", l_N, "，不满足：", v[0], " > 命中！")
                            break
                        else:
                            print("ok > 条件：", l_N, "，不满足：", v[0], " > 不命中。")
                            Ellipsis
                else:
                    print("error > 条件：", l_N, "，满足：", d_cases['satisfied'][0], " > 不命中！")
                    Ellipsis
                    # Sqlserver_PO.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

                # 回写数据库f_resut, f_updateDate
                if varCount == 2:
                    print("ok")
                    Sqlserver_PO.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
                else:
                    print("error")
                    Sqlserver_PO.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

            else:
                print("[not or & and ]")
            print("-".center(100, "-"))



    def checkRule2(self, d_cases, id, f_evaluationRuleCoding, varTable):
        # 不嵌套判断，2个字段（BMI和年龄）
        # 更新测试记录，确保满足
        Sqlserver_PO.execute("update %s set BMI = %s and '年龄' = %s where id = %s" % (varTable, d_cases['satisfied'][0]['BMI'], d_cases['satisfied'][0]['年龄'], id))   # 修改测试记录的BMI和年龄值

        # 跑接口

        # 查询是否命中 f_evaluationRuleCoding
        f_evaluationRuleCoding_actual = Sqlserver_PO.select("select f_evaluationRuleCoding from %s where id = %s" % (varTable, id))
        if f_evaluationRuleCoding == f_evaluationRuleCoding_actual:
            # 回写数据库f_resut, f_updateDate
            print("ok")
            Sqlserver_PO.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
        else:
            print("error")
            Sqlserver_PO.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

    def checkRule3(self, d_cases, id, f_evaluationRuleCoding, varTable):
        # 嵌套判断，3个字段（BMI，年龄，性别）
        # 更新测试记录，满足条件
        # d_cases = {'BMI': 41.0, '年龄': 14.4, '性别': '男'}
        # Sqlserver_PO.execute("update %s set BMI = %s and '年龄' = %s and '性别' = %s where id = %s" % (varTable, d_cases['BMI'], d_cases['年龄'], d_cases['性别'], id))   # 修改测试记录的BMI、年龄及性别值

        # 跑接口

        # 查询是否输出评估规则编码，输出则命中，查询是否命中 f_evaluationRuleCoding
        # f_evaluationRuleCoding_actual = Sqlserver_PO.select("select f_evaluationRuleCoding from %s where id = %s" % (varTable, id))
        # if f_evaluationRuleCoding == f_evaluationRuleCoding_actual:
        #     return 1
        # else:
        #     return 0

        return 1

    def checkRule4(self, d_cases, id, f_evaluationRuleCoding, varTable):
        # 嵌套判断，3个字段（BMI，年龄，性别）
        # 更新测试记录，不满足条件
        # d_cases = {'BMI': 41.0, '年龄': 14.4, '性别': '男'}
        # Sqlserver_PO.execute("update %s set BMI = %s and '年龄' = %s and '性别' = %s where id = %s" % (varTable, d_cases['BMI'], d_cases['年龄'], d_cases['性别'], id))   # 修改测试记录的BMI、年龄及性别值

        # 跑接口

        # 查询是否输出评估规则编码，输出则命中，查询是否命中 f_evaluationRuleCoding
        # f_evaluationRuleCoding_actual = Sqlserver_PO.select("select f_evaluationRuleCoding from %s where id = %s" % (varTable, id))
        # if f_evaluationRuleCoding == f_evaluationRuleCoding_actual:
        #     return 1
        # else:
        #     return 2
        return 2


