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

    # def __init__(self):
    #     self.Log_PO = LogPO(filename='log.log', level="info")

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
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ruleName', 'varchar(100)', '规则名称')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_detail', 'varchar(999)', '评估规则详细描述')
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ERcode', 'varchar(50)', '评估规则编码')
        # # Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_evaluationFactorJudgmentRules_O', 'varchar(999)', '评估因素判断规则_原始')  //不用，没处理。
        Sqlserver_PO_CHC5G.setFieldTypeComment(varTable, 'f_ER', 'varchar(8000)', '评估因素判断规则')

        # 6, 设置自增主键（最后）
        Sqlserver_PO_CHC5G.setIdentityPrimaryKey(varTable, "ID")

    def excel2db_IR(self, varFile, varSheet, varTable):

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
                        print("ok > 条件：", lln, "，满足：", d_cases['satisfied'][0] , " > 命中。")

                        # 反向用例, 不满足条件的v[0]，预期不命中。
                        del d_cases['satisfied']
                        varCount = 2
                        for k, v in d_cases.items():
                            # print(v[0])
                            varCount = self.checkRule4(v[0], id, f_ERcode, varTable)
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
                    print("ok > 条件：", l_N, "，满足：", d_cases['satisfied'][0], " > 命中。")

                    # 反向用例, 不满足条件的v[0]，预期不命中。
                    del d_cases['satisfied']
                    varCount = 2
                    for k, v in d_cases.items():
                        # print(v[0])
                        varCount = self.checkRule4(v[0], id, f_ERcode, varTable)
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
                    print("ok > 条件：", l_N, "，满足：", d_cases['satisfied'][0], " > 命中。")

                    # 反向用例, 不满足条件的v[0]，预期不命中。
                    del d_cases['satisfied']
                    varCount = 2
                    for k, v in d_cases.items():
                        # print(v[0])
                        varCount = self.checkRule4(v[0], id, f_ERcode, varTable)
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

    def checkWS_ok(self, d_cases_satisfied, ID, varTable):

        # d_cases_satisfied = {'BMI': 16.8}
        # id = 1
        # varTable = a_weight10_WA

        l_d_row = Sqlserver_PO_CHC5G.select("select f_type, f_typeCode, f_weightStatusCode from %s where ID= %s" % (varTable, ID))
        # print("id, l_d_row", ID, l_d_row)
        # print(l_d_row)  # [{'f_typeCode': '3', 'f_weightStatusCode': '1'}]

        # 参数

        # print("p2, d_cases_satisfied:", d_cases_satisfied)  # {'BMI': 16.8}
        f_type = l_d_row[0]['f_type']  # 儿童
        f_typeCode = l_d_row[0]['f_typeCode']  # 3
        f_weightStatusCode = l_d_row[0]['f_weightStatusCode']  # 1


        # 跑接口
        if '年龄' in d_cases_satisfied:
            varAge = d_cases_satisfied['年龄']
        else:
            varAge = 18

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

        if f_type == '儿童':
            varAgeMonth = d_cases_satisfied['年龄']
        else:
            varAgeMonth = 0


        d_tmp = {}
        d_tmp['f_weightStatusCode预期值'] = f_weightStatusCode  # 预期值

        command = 'curl -X POST "http://192.168.0.243:8014/weight/saveOrUpdateWeightManage" -H "Request-Origion:SwaggerBootstrapUi" -H "accept:*/*" -H "Authorization:" -H "Content-Type:application/json" -d "{\\"age\\":12,\\"ageFloat\\":' + str(varAge) + ',\\"ageMonth\\":' + str(varAgeMonth) + ',\\"basicIntake\\":100,\\"bmi\\":' + str(
            d_cases_satisfied['BMI']) + ',\\"categoryCode\\":\\"' + str(
            f_typeCode) + '\\",\\"disease\\":\\"无\\",\\"foodAdvice\\":\\"建议饮食\\",\\"height\\":175,\\"hipline\\":33,\\"id\\":2,\\"idCard\\":\\"420204202201011268\\",\\"orgCode\\":\\"0000001\\",\\"orgName\\":\\"静安精神病院\\",\\"sex\\":\\"' + str(varSex) +'\\",\\"sexCode\\":\\"' + str(varSexCode) +'\\",\\"sportAdvice\\":\\"建议运动\\",\\"targetWeight\\":50,\\"waistHip\\":0.9,\\"waistline\\":33,\\"weight\\":55,\\"weightRecordId\\":0}"'
        # print(command)

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # command = command.replace("\\\\", "\\")
        # print(command)
        d_tmp["i"] = command
        # print(d_r)
        if d_r['code'] == 200:
            # 断言
            l_d_1 = Sqlserver_PO_CHC.select("select WEIGHT_STATUS from WEIGHT_REPORT where ID = 2")
            l_d_2 = Sqlserver_PO_CHC.select("select WEIGHT_STATUS from QYYH where SFZH = '420204202201011268'")
            d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'] = "select WEIGHT_STATUS from WEIGHT_REPORT where ID = 2"
            d_tmp['QYYH_WEIGHT_STATUS'] = "select WEIGHT_STATUS from QYYH where SFZH = '420204202201011268'"
            # print("l_d_1", l_d_1)
            # print("l_d_2", l_d_2)
            # print("l_d_1[0]['WEIGHT_STATUS']", l_d_2[0]['WEIGHT_STATUS'])
            # print("f_weightStatusCode", f_weightStatusCode)
            d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值'] = l_d_1[0]['WEIGHT_STATUS']  # 预期值
            d_tmp['QYYH__WEIGHT_STATUS实际值'] = l_d_2[0]['WEIGHT_STATUS'] # 预期值

            if l_d_1 == l_d_2 and str(l_d_1[0]['WEIGHT_STATUS']) == str(f_weightStatusCode):
                d_tmp['result'] = 1
                return d_tmp
            else:
                d_tmp['result'] = 0
                return d_tmp
        else:
            print("428, error ", d_r['code'])
            sys.exit(0)

    def checkWS_error(self, d_cases_satisfied, ID, varTable):

        # d_cases_satisfied = {'BMI': 16.8}
        # id = 1
        # varTable = a_weight10_WA

        sleep(1)

        l_d_row = Sqlserver_PO_CHC5G.select(
            "select f_typeCode, f_weightStatusCode from %s where ID= %s" % (varTable, ID))
        # print("id, l_d_row", ID, l_d_row)
        # print(l_d_row)  # [{'f_typeCode': '3', 'f_weightStatusCode': '1'}]

        # 参数

        # print("p2, d_cases_satisfied:", d_cases_satisfied)  # {'BMI': 16.8}
        f_typeCode = l_d_row[0]['f_typeCode']  # 3
        f_weightStatusCode = l_d_row[0]['f_weightStatusCode']  # 1

        # 跑接口
        if '年龄' in d_cases_satisfied:
            varAge = d_cases_satisfied['年龄']
        else:
            varAge = 18
        if '性别' in d_cases_satisfied:
            varSex = d_cases_satisfied['性别']
        else:
            varSex = '男'

        # print(varAge, varSex)
        # d_cases_satisfied['年龄']
        # d_cases_satisfied['性别']

        # d_cases_satisfied['BMI']
        # f_typeCode

        command = 'curl -X POST "http://192.168.0.243:8014/weight/saveOrUpdateWeightManage" -H "Request-Origion:SwaggerBootstrapUi" -H "accept:*/*" -H "Authorization:" -H "Content-Type:application/json" -d "{\\"age\\":12,\\"ageFloat\\":' + str(
            varAge) + ',\\"ageMonth\\":40,\\"basicIntake\\":100,\\"bmi\\":' + str(
            d_cases_satisfied['BMI']) + ',\\"categoryCode\\":\\"' + str(
            f_typeCode) + '\\",\\"disease\\":\\"无\\",\\"foodAdvice\\":\\"建议饮食\\",\\"height\\":175,\\"hipline\\":33,\\"id\\":2,\\"idCard\\":\\"420204202201011268\\",\\"orgCode\\":\\"0000001\\",\\"orgName\\":\\"静安精神病院\\",\\"sex\\":\\"' + str(
            varSex) + '\\",\\"sexCode\\":\\"1\\",\\"sportAdvice\\":\\"建议运动\\",\\"targetWeight\\":50,\\"waistHip\\":0.9,\\"waistline\\":33,\\"weight\\":55,\\"weightRecordId\\":0}"'
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)
        if d_r['code'] == 200:
            # 断言
            l_d_1 = Sqlserver_PO_CHC.select("select WEIGHT_STATUS from WEIGHT_REPORT where ID = 2")
            l_d_2 = Sqlserver_PO_CHC.select("select WEIGHT_STATUS from QYYH where SFZH = '420204202201011268'")
            # print("l_d_1", l_d_1)
            # print("l_d_2", l_d_2)
            # print("l_d_1[0]['WEIGHT_STATUS']", l_d_1[0]['WEIGHT_STATUS'])
            # print("f_weightStatusCode", f_weightStatusCode)
            if l_d_1 == l_d_2 and str(l_d_1[0]['WEIGHT_STATUS']) != str(f_weightStatusCode):
                return 2
            else:
                return 0

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



    def resultOR(self, d_cases, id, l_2_value, varTable, lln, varTestCount):

        varTestcase = 0

        l_result = []
        # 正向用例，满足条件的d_cases['satisfied'][0]，预期要命中
        # print(len(d_cases['satisfied']))
        if len(d_cases['satisfied']) == 1:
            d_tmp = self.checkWS_ok(d_cases['satisfied'][0], id, varTable)
            if d_tmp['result'] == 1:
                Color_PO.outColor([{"34": str(lln) + "/" + str(varTestCount) + ",[正向ok], 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0])}])

                # Color_PO.outColor([{"34": "p1, 正向ok, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0])}])
                # Color_PO.outColor([{"34": "run接口：", "33": d_tmp["i"].replace("\\\\", "\\")}])
                # Color_PO.outColor([{"34": "查询1：", "33": d_tmp['WEIGHT_REPORT_WEIGHT_STATUS']}])
                # Color_PO.outColor([{"34": "查询2：", "33": d_tmp['QYYH_WEIGHT_STATUS']}])
                # Color_PO.outColor([{"34": "f_weightStatusCode预期值：", "33": d_tmp['f_weightStatusCode预期值']}])
                # Color_PO.outColor([{"34": "WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])
                # Color_PO.outColor([{"34": "WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])
                # # print("p1, 正向ok, 条件：", l_N, "，满足：", d_cases['satisfied'][0])
                l_result.append(1)
                varTestcase = varTestcase + 1
            else:
                Color_PO.outColor([{"31": "ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(d_cases['satisfied'][0])}])
                # print(d_tmp["i"].replace("\\\\","\\"))
                Color_PO.outColor([{"31":"run接口：", "33": d_tmp["i"].replace("\\\\", "\\")}])
                Color_PO.outColor([{"31":"查询1：", "33": d_tmp['WEIGHT_REPORT_WEIGHT_STATUS']}])
                Color_PO.outColor([{"31":"查询2：", "33": d_tmp['QYYH_WEIGHT_STATUS']}])
                Color_PO.outColor([{"31":"f_weightStatusCode预期值：", "33": d_tmp['f_weightStatusCode预期值']}])
                Color_PO.outColor([{"31":"WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])
                Color_PO.outColor([{"31":"WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])


                # print("f_weightStatusCode预期值", d_tmp['f_weightStatusCode预期值'])
                # print("WEIGHT_REPORT_WEIGHT_STATUS", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                # print("QYYH_WEIGHT_STATUS", d_tmp['QYYH_WEIGHT_STATUS'])
                # print("WEIGHT_REPORT__WEIGHT_STATUS实际值", d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值'])
                # print("QYYH__WEIGHT_STATUS实际值", d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值'])
                # Color_PO.outColor([{"33": d_tmp}])


                # print("步骤1 => ", d_tmp["i"])
                # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
                Log_PO.logger.info("ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(d_cases['satisfied'][0]))
                Log_PO.logger.info(d_tmp['i'])
                Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                varTestcase = varTestcase + 1
                # 将错误条件写入数据库，以备复测。
                l_d_row = Sqlserver_PO_CHC5G.select("select f_type, f_typeCode,f_weightStatus,f_weightStatusCode from %s where ID=%s" % (varTable,id))
                # print(l_d_row)
                f_type1 = l_d_row[0]['f_type']
                f_typeCode1 = l_d_row[0]['f_typeCode']
                f_weightStatus1 = l_d_row[0]['f_weightStatus']
                f_weightStatusCode1 = l_d_row[0]['f_weightStatusCode']
                # 将列表转换字符串
                f_2_value = (self.convert_conditions(l_2_value))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7

                # Sqlserver_PO_CHC5G.execute("insert into %s (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID) values (%s,%s,%s,%s,'%s',%s) "
                #                            % (varTable, f_type1, f_typeCode1, f_weightStatus1, f_weightStatusCode1, str(l_2_value), int(id)))
                sql = """
                    INSERT INTO [%s] 
                    (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID) 
                    VALUES ('%s', '%s', '%s', '%s', '%s', %d)
                """ % (
                    varTable,
                    f_type1,
                    f_typeCode1,
                    f_weightStatus1,
                    f_weightStatusCode1,
                    str(f_2_value).replace("'", "''"),  # 防止内部有单引号导致 SQL 错误
                    int(id)
                )
                Sqlserver_PO_CHC5G.execute(sql)

                # print("p2, 正向error, 条件：", l_N, "，满足：", d_cases['satisfied'][0], varCount)
                # Ellipsis
                l_result.append(0)
        else:
            for i in range(len(d_cases['satisfied'])):
                d_tmp = self.checkWS_ok(d_cases['satisfied'][i], id, varTable)
                if d_tmp['result'] == 1:
                    Color_PO.outColor([{"34": str(lln) + "(" + str(i+1) + ")/" + str(varTestCount) + ",[正向ok], 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][i])}])
                    # Color_PO.outColor([{"34": "run接口：", "33": d_tmp["i"].replace("\\\\", "\\")}])
                    # Color_PO.outColor([{"34": "查询1：", "33": d_tmp['WEIGHT_REPORT_WEIGHT_STATUS']}])
                    # Color_PO.outColor([{"34": "查询2：", "33": d_tmp['QYYH_WEIGHT_STATUS']}])
                    # Color_PO.outColor([{"34": "f_weightStatusCode预期值：", "33": d_tmp['f_weightStatusCode预期值']}])
                    # Color_PO.outColor([{"34": "WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])
                    # Color_PO.outColor([{"34": "WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])
                    # # print("p1, 正向ok, 条件：", l_N, "，满足：", d_cases['satisfied'][0])
                    l_result.append(1)
                    varTestcase = varTestcase + 1
                else:
                    Color_PO.outColor([{"31": "ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
                        d_cases['satisfied'][i])}])
                    # print(d_tmp["i"].replace("\\\\","\\"))
                    Color_PO.outColor([{"31": "run接口：", "33": d_tmp["i"].replace("\\\\", "\\")}])
                    Color_PO.outColor([{"31": "查询1：", "33": d_tmp['WEIGHT_REPORT_WEIGHT_STATUS']}])
                    Color_PO.outColor([{"31": "查询2：", "33": d_tmp['QYYH_WEIGHT_STATUS']}])
                    Color_PO.outColor([{"31": "f_weightStatusCode预期值：", "33": d_tmp['f_weightStatusCode预期值']}])
                    Color_PO.outColor(
                        [{"31": "WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])
                    Color_PO.outColor(
                        [{"31": "WEIGHT_REPORT__WEIGHT_STATUS实际值：", "33": d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值']}])

                    # print("f_weightStatusCode预期值", d_tmp['f_weightStatusCode预期值'])
                    # print("WEIGHT_REPORT_WEIGHT_STATUS", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                    # print("QYYH_WEIGHT_STATUS", d_tmp['QYYH_WEIGHT_STATUS'])
                    # print("WEIGHT_REPORT__WEIGHT_STATUS实际值", d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值'])
                    # print("QYYH__WEIGHT_STATUS实际值", d_tmp['WEIGHT_REPORT__WEIGHT_STATUS实际值'])
                    # Color_PO.outColor([{"33": d_tmp}])

                    # print("步骤1 => ", d_tmp["i"])
                    # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                    # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
                    Log_PO.logger.info("ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
                        d_cases['satisfied'][i]))
                    Log_PO.logger.info(d_tmp['i'])
                    Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                    Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                    varTestcase = varTestcase + 1
                    # 将错误条件写入数据库，以备复测。
                    l_d_row = Sqlserver_PO_CHC5G.select(
                        "select f_type, f_typeCode,f_weightStatus,f_weightStatusCode from %s where ID=%s" % (
                        varTable, id))
                    # print(l_d_row)
                    f_type1 = l_d_row[0]['f_type']
                    f_typeCode1 = l_d_row[0]['f_typeCode']
                    f_weightStatus1 = l_d_row[0]['f_weightStatus']
                    f_weightStatusCode1 = l_d_row[0]['f_weightStatusCode']
                    # 将列表转换字符串
                    f_2_value = (self.convert_conditions(l_2_value))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7

                    # Sqlserver_PO_CHC5G.execute("insert into %s (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID) values (%s,%s,%s,%s,'%s',%s) "
                    #                            % (varTable, f_type1, f_typeCode1, f_weightStatus1, f_weightStatusCode1, str(l_2_value), int(id)))
                    sql = """
                                    INSERT INTO [%s] 
                                    (f_type, f_typeCode, f_weightStatus, f_weightStatusCode, f_value, f_errID) 
                                    VALUES ('%s', '%s', '%s', '%s', '%s', %d)
                                """ % (
                        varTable,
                        f_type1,
                        f_typeCode1,
                        f_weightStatus1,
                        f_weightStatusCode1,
                        str(f_2_value).replace("'", "''"),  # 防止内部有单引号导致 SQL 错误
                        int(id)
                    )
                    Sqlserver_PO_CHC5G.execute(sql)

                    # print("p2, 正向error, 条件：", l_N, "，满足：", d_cases['satisfied'][0], varCount)
                    # Ellipsis
                    l_result.append(0)

        # 反向用例, 不满足条件的v[0]，预期不命中。
        del d_cases['satisfied']
        for k, v in d_cases.items():
            # print(v[0])
            varCount = self.checkWS_error(v[0], id, varTable)
            if varCount == 1:
                # 反向如果命中就错，并且终止循环
                Color_PO.outColor([{"31": "ID = " + str(id) + ", p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
                # Log_PO.logger.info("ID = " + str(id) + ", p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
                # varTestcase = varTestcase + 1
                Color_PO.outColor([{"33": d_tmp}])


                # print("步骤1 => ", d_tmp["i"])
                # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
                Log_PO.logger.info("ID = " + str(id) + ", p3, 反向error, 条件：" + str(l_2_value) + "，不满足：" + str(v[0]))
                Log_PO.logger.info(d_tmp['i'])
                Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                varTestcase = varTestcase + 1

                # print("p3, 反向error, 条件：", l_N, "，不满足：", v[0])
                l_result.append(0)
                # break
            else:
                # Color_PO.outColor([{"33": "p4, 反向ok, 条件：" + str(l_2_value) + "，不满足：" + str(v[0])}])
                # print("p4, 反向ok, 条件：", l_N, "，不满足：", v[0], " > 不命中")
                # Ellipsis
                l_result.append(1)
                varTestcase = varTestcase + 1

        if 0 in l_result:
            Color_PO.outColor([{"31": "ID = " + str(id) + ", " + str(l_result)}])
            Log_PO.logger.info("ID = " + str(id) + ", " + str(l_result))
            return varTestcase,0
        else:
            return varTestcase,1

        # 回写数据库f_resut, f_updateDate
        # if varCount == 2:
        #     Color_PO.outColor([{"32": "ok, id=" + str(id)}])
        #     Sqlserver_PO_CHC5G.execute(
        #         "update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
        # else:
        #     Color_PO.outColor([{"31": "error, id=" + str(id)}])
        #     Sqlserver_PO_CHC5G.execute(
        #         "update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

    def result(self, d_cases, id, l_2_value, varTable):

        varTestcase = 0

        # 正向用例，满足条件的d_cases['satisfied'][0]，预期要命中
        d_tmp = self.checkWS_ok(d_cases['satisfied'][0], id, varTable)
        if d_tmp['result'] == 1:
            Color_PO.outColor([{"34": "p1, 正向ok, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0])}])
            Log_PO.logger.info("p1, 正向ok, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0]))
            varTestcase = varTestcase + 1
            # print("p1, 正向ok, 条件：", l_N, "，满足：", d_cases['satisfied'][0])

            # 反向用例, 不满足条件的v[0]，预期不命中。
            del d_cases['satisfied']
            varCount = 2
            for k, v in d_cases.items():
                # print(v[0])
                varCount = self.checkWS_error(v[0], id, varTable)
                if varCount == 1:
                    # 反向如果命中就错，并且终止循环
                    Color_PO.outColor([{"31": "p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
                    # Log_PO.logger.info("p3, 反向error, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
                    # varTestcase = varTestcase + 1
                    Color_PO.outColor([{"33": d_tmp}])

                    # print("步骤1 => ", d_tmp["i"])
                    # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                    # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
                    Log_PO.logger.info("ID = " + str(id) + ", p3, 反向error, 条件：" + str(l_2_value) + "，不满足：" + str(
                        str(v[0])))
                    Log_PO.logger.info(d_tmp['i'])
                    Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
                    Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
                    varTestcase = varTestcase + 1

                    # print("p3, 反向error, 条件：", l_N, "，不满足：", v[0])
                    break
                else:
                    Color_PO.outColor([{"34": "p4, 反向ok, 条件：" + str(l_2_value) + "，满足：" + str(v[0])}])
                    Log_PO.logger.info("p4, 反向ok, 条件：" + str(l_2_value) + "，满足：" + str(v[0]))
                    varTestcase = varTestcase + 1
                    # print("p4, 反向ok, 条件：", l_N, "，不满足：", v[0], " > 不命中")
                    # Ellipsis
        else:
            Color_PO.outColor([{"31": "ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
                d_cases['satisfied'][0])}])
            Color_PO.outColor([{"33": d_tmp}])

            # print("步骤1 => ", d_tmp["i"])
            # print("步骤2 => ", d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
            # print("步骤3 => ", d_tmp['QYYH_WEIGHT_STATUS'])
            Log_PO.logger.info("ID = " + str(id) + ", p2, 正向error, 条件：" + str(l_2_value) + "，不满足：" + str(
                d_cases['satisfied'][0]))
            Log_PO.logger.info(d_tmp['i'])
            Log_PO.logger.info(d_tmp['WEIGHT_REPORT_WEIGHT_STATUS'])
            Log_PO.logger.info(d_tmp['QYYH_WEIGHT_STATUS'])
            varTestcase = varTestcase + 1

            # Color_PO.outColor([{"31": "p2, 正向error, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0])}])
            # Log_PO.logger.info("p2, 正向error, 条件：" + str(l_2_value) + "，满足：" + str(d_cases['satisfied'][0]))
            # varTestcase = varTestcase + 1
            # print("p2, 正向error, 条件：", l_N, "，满足：", d_cases['satisfied'][0], varCount)
            # Ellipsis

        # 回写数据库f_resut, f_updateDate
        if varCount == 2:
            Color_PO.outColor([{"32": "ID = " + str(id) + ", => ok"}])
            Log_PO.logger.info([{"32": "ok, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_testcase=%s where id = %s" % (varTable, varTestcase, id))
        else:
            Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
            Log_PO.logger.info([{"31": "error, id=" + str(id)}])
            Sqlserver_PO_CHC5G.execute("update %s set f_result = 'error', f_updateDate = GETDATE(), f_testcase=%s where id = %s" % (varTable, varTestcase, id))


    def WS(self, varTable):

        # 体重状态

        # 获取每行数据
        # l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_type, f_typeCode, f_weightStatus, f_weightStatusCode,f_value from %s" % (varTable))
        l_d_row = Sqlserver_PO_CHC5G.select("select ID, f_type, f_value from %s" % (varTable))
        # print("l_d_row => ", l_d_row)  [{'f_type': '普通人群', 'f_weightStatus': '体重偏低', 'f_value': 'BMI＜18.5'},

        # 测试某条记录
        # todo debug
        for i, index in enumerate(l_d_row):
            i = 1
            id = l_d_row[i]['ID']
            f_value = l_d_row[i]['f_value']

            # 获取原始数据
            # todo p1
            print("ID = " + str(id) + ", f_value = " + str(f_value))
            varTestCount = f_value.count("or")
            # print(varTestCount)  # 输出or的数量: 2
            # Color_PO.outColor([{"32": "p1, id = " + str(id) + ", f_value = " + str(f_value)}])
            Log_PO.logger.info("p1, id = " + str(id) + ", f_value = " + str(f_value))

            # 清洗不规则数据，包括 清除运算符左右的空格、换行符、括号、等
            f_value = f_value.replace("月", '')
            f_value = f_value.replace('＞', '>').replace('＜', '<').replace('＝', '=')
            # f_value = re.sub(r'\s*<=\s*', '<', f_value)
            # f_value = re.sub(r'\s*>=\s*', '>', f_value)
            # f_ER = re.sub(r'\s*<=\s*', '>', f_ER)
            # f_ER = re.sub(r'\s*<=\s*', '>=', f_ER)
            # f_ER = re.sub(r'\s*<=\s*', '=', f_ER)

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
                    d_cases = BmiAgeSex_PO.generate_all_cases(l_3_value)

                    # d_cases = po.generate_all_cases(l_3_value, num_samples=2)

                    # print("--------------------")
                    # print("d_case", d_cases)
                    # sys.exit(0)

                    # 判断输出结果
                    varTestcase, varCount = self.resultOR(d_cases, id, l_2_value, varTable, lln+1, varTestCount)
                    l_result.append(varCount)
                    sum = sum + varTestcase

                # print(l_result)

                # 回写数据库f_resut, f_updateDate
                if 0 not in l_result:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => ok"}])
                    Sqlserver_PO_CHC5G.execute("update %s set f_result = 'ok', f_updateDate = GETDATE(), f_testcase=%s where id = %s" % (
                        varTable, sum, id))

                else:
                    Color_PO.outColor([{"32": "ID = " + str(id) + ", => error"}])
                    Sqlserver_PO_CHC5G.execute(
                        "update %s set f_result = 'error', f_updateDate = GETDATE(), f_testcase=%s where id = %s" % (
                        varTable, sum, id))

            elif "and" in f_value:

                # 转换成列表
                l_value = f_value.split("and")
                l_value = [i.strip() for i in l_value]
                print("730 实际参数 =", l_value)  # ['18.5<BMI', 'BMI<24.0']

                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                for i in l_value:
                    l_simple_conditions = BmiAgeSex_PO.splitMode(i)
                    l_2_value.extend(l_simple_conditions)
                print("737 分解参数 =", l_2_value)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                l_3_value = []
                for i in l_2_value:
                    l_simple_conditions = BmiAgeSex_PO.interconvertMode(i)
                    l_3_value.extend(l_simple_conditions)
                print("744 结构化参数 =", l_3_value)  #  ['BMI>18.5', 'BMI<24.0']

                # 读取BMI模块，生成随机数据d_cases
                d_cases = BmiAgeSex_PO.generate_all_cases(l_3_value)

                # 判断输出结果
                self.result(d_cases, id, l_value, varTable)

            elif "and" not in f_value:
                # todo 适配一个条件，如 18.5>BMI 和 BMI<18.5

                l_2_value = []
                # 拆分，如 '6<=年龄<6.5' 拆分为 或 6<=年龄'and 年龄<6.5'
                l_simple_conditions = Bmi_PO.splitMode(f_value)
                l_2_value.extend(l_simple_conditions)
                # print("611 分解参数 =", l_2_value)

                # 转换位置（要求前面是左边是关键字，右边是值），如将 18.5>BMI 转换 BMI<18.5
                l_3_value = []
                for i in l_2_value:
                    l_simple_conditions = Bmi_PO.interconvertMode(i)
                    l_3_value.extend(l_simple_conditions)
                # print("680 结构化参数 =", l_3_value)  # ['BMI<18.5']

                # 读取BMI模块，生成随机数据d_cases
                d_cases = Bmi_PO.generate_all_cases(l_3_value)
                # print(d_cases)  # {'satisfied': [{'BMI': 16.8}], 'not1': [{'BMI': 19.6}]}

                # 判断输出结果
                self.result(d_cases, id, l_2_value, varTable)

            else:
                print("[not or & and ]")
            print("-".center(100, "-"))

            break

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

