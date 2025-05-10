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

from ThreeFieldPO import *
ThreeField_PO = ThreeFieldPO()

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

        # 测试第一条记录
        i = 6
        id = l_d_row[i]['id']
        f_result = l_d_row[i]['f_result']
        f_updateDate = l_d_row[i]['f_updateDate']
        f_ruleName = l_d_row[i]['f_ruleName']
        f_evaluationFactorJudgmentRules_N = l_d_row[i]['f_evaluationFactorJudgmentRules_N']
        f_evaluationRuleCoding = l_d_row[i]['f_evaluationRuleCoding']

        # 获取条件
        print(f_evaluationFactorJudgmentRules_N)  # BMI>=24 and 年龄>=18 and 年龄<65

        # 优先处理or，再处理and
        print("----------------------------------------")
        if "or" in f_evaluationFactorJudgmentRules_N:
            ...
            print("orororor")
            l_N = f_evaluationFactorJudgmentRules_N.split("or")
            l_N = [i.replace("(",'').replace(")",'').strip() for i in l_N]
            l_N = [i.split("and") for i in l_N]
            l_l_N = [[item.strip() for item in sublist] for sublist in l_N]
            # print(l_l_N)
            print(len(l_l_N))  # 16 ， 16个组合条件
            varCount = sum = 0
            l_1 = []
            for k in l_l_N:
                d_cases = ThreeField_PO.generate_all_cases(k)
                # print(d_cases)
                # print(len(d_cases))
                print(d_cases['satisfied'][0])  # {'BMI': 44.5, '年龄': 14.4, '性别': '男'}

                (varCount, d_caseConditionName) = self.checkRule3(d_cases['satisfied'][0], id, f_evaluationRuleCoding, varTable)
                sum = sum + varCount
                l_1.append(d_caseConditionName)
            if sum == len(l_l_N):
                print("ok > ", len(l_l_N), "个组合条件全部命中")

                # 反向用例，不符合条件的其他都没有命中
                l_2 = list(d_cases.keys())
                print(l_2)
                l_2.remove('satisfied')
                print(l_2) # ['BMI满足且年龄满足且性别不满足', 'BMI满足且年龄不满足且性别满足', 'BMI满足且年龄不满足且性别不满足', 'BMI不满足且年龄满足且性别满足', 'BMI不满足且年龄满足且性别不满足', 'BMI不满足且年龄不满足且性别满足', 'BMI不满足且年龄不满足且性别不满足']
                varCount = 0
                for j in l_2:
                    print(d_cases[j][0])
                    (varCount, d_caseConditionName) = self.checkRule3(d_cases[j][0], id, f_evaluationRuleCoding, varTable)
                    if varCount == 1:
                        # 反向如果命中就错，并且终止循环
                        print("error > ", d_cases[j][0], "组合条件命中！")
                        break
                if varCount == 0:
                    # 回写数据库f_resut, f_updateDate
                    print("ok")
                    Sqlserver_PO.execute("update %s set f_result = 'ok', f_updateDate = GETDATE() where id = %s" % (varTable, id))
                else:
                    print("error")
                    Sqlserver_PO.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

            else:
                print("error > ", len(l_l_N), "个组合条件中, 只命中", sum, "个！未命中的组合为：", l_1)
                Sqlserver_PO.execute("update %s set f_result = 'error', f_updateDate = GETDATE() where id = %s" % (varTable, id))

            sys.exit(0)

        elif "and" in f_evaluationFactorJudgmentRules_N:
            l_N = f_evaluationFactorJudgmentRules_N.split("and")
            l_N = [i.strip() for i in l_N]
            print(l_N)  # ['BMI>=24', '年龄>=18', '年龄<65']

            cases = ThreeField_PO.generate_all_cases(l_N)
            print(cases)
            sys.exit(0)
        else:
            print("没有or和and")
            sys.exit(0)

        # 生成每种情况的样本数据，1个满足，3个不满足
        d_cases = self.generate_all_cases(l_N)
        print(d_cases)  # {'satisfied': [{'BMI': 26.9, '年龄': 26}], 'not1': [{'BMI': 41.8, '年龄': 7}], 'not2': [{'BMI': 21.9, '年龄': 33}], 'not3': [{'BMI': 19.0, '年龄': 14}]}
        # print(cases['satisfied'][0]['BMI'])  #  26.9

        sys.exit(0)

        # # 遍历每条记录
        # for i, index in enumerate(l_d_row):
        #     id = l_d_row[i]['id']
        #     f_result = l_d_row[i]['f_result']
        #     f_updateDate = l_d_row[i]['f_updateDate']
        #     f_ruleName = l_d_row[i]['f_ruleName']
        #     f_evaluationFactorJudgmentRules_N = l_d_row[i]['f_evaluationFactorJudgmentRules_N']
        #     f_evaluationRuleCoding = l_d_row[i]['f_evaluationRuleCoding']
        #     print(id)

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
        # 更新测试记录，确保满足
        # d_cases = {'BMI': 41.0, '年龄': 14.4, '性别': '男'}
        # Sqlserver_PO.execute("update %s set BMI = %s and '年龄' = %s and '性别' = %s where id = %s" % (varTable, d_cases['BMI'], d_cases['年龄'], d_cases['性别'], id))   # 修改测试记录的BMI、年龄及性别值

        # 跑接口

        # 查询是否输出评估规则编码，输出则命中，查询是否命中 f_evaluationRuleCoding
        # f_evaluationRuleCoding_actual = Sqlserver_PO.select("select f_evaluationRuleCoding from %s where id = %s" % (varTable, id))
        # if f_evaluationRuleCoding == f_evaluationRuleCoding_actual:
        #     return (1, d_cases['satisfied'][0])
        # else:
        #     return (0, d_cases['satisfied'][0])

        return (1, d_cases)




    def generate_all_cases(self, conditions, num_samples=1):
        """
        生成所有4种可能的条件组合情况

        参数:
        conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65']
        num_samples (int): 每种情况生成的样本数量

        返回:
        dict: 包含4种情况的样本字典
        """
        # 分离BMI和年龄条件
        bmi_conditions = [c for c in conditions if c.startswith('BMI')]
        age_conditions = [c for c in conditions if c.startswith('年龄')]

        # 生成每种情况的样本
        return {
            "satisfied": [self.generate_sample(bmi_conditions, age_conditions, True, True) for _ in range(num_samples)],
            "not1": [self.generate_sample(bmi_conditions, age_conditions, True, False) for _ in range(num_samples)],
            "not2": [self.generate_sample(bmi_conditions, age_conditions, False, True) for _ in range(num_samples)],
            "not3": [self.generate_sample(bmi_conditions, age_conditions, False, False) for _ in range(num_samples)]
        }

    def generate_sample(self, bmi_conditions, age_conditions, satisfy_bmi, satisfy_age):
        """
        生成一个符合指定条件组合的样本

        参数:
        bmi_conditions (list): BMI相关条件
        age_conditions (list): 年龄相关条件
        satisfy_bmi (bool): 是否满足BMI条件
        satisfy_age (bool): 是否满足年龄条件

        返回:
        dict: 包含BMI和年龄的字典
        """
        # 生成BMI值
        if satisfy_bmi:
            bmi = self.generate_valid_bmi(bmi_conditions)
        else:
            bmi = self.generate_invalid_bmi(bmi_conditions)

        # 生成年龄值
        if satisfy_age:
            age = self.generate_valid_age(age_conditions)
        else:
            age = self.generate_invalid_age(age_conditions)

        # 返回字典格式
        return {'BMI': bmi, '年龄': age}

    def generate_valid_bmi(self, conditions):
        """生成符合所有BMI条件的值"""
        bmi_min = 10.0
        bmi_max = 60.0

        for condition in conditions:
            match = re.match(r'BMI([<>=]+)(\d+)', condition)
            if not match:
                continue

            operator, value = match.groups()
            value = float(value)

            if operator == '>':
                bmi_min = max(bmi_min, value + 0.1)
            elif operator == '>=':
                bmi_min = max(bmi_min, value)
            elif operator == '<':
                bmi_max = min(bmi_max, value - 0.1)
            elif operator == '<=':
                bmi_max = min(bmi_max, value)

        return round(random.uniform(bmi_min, bmi_max), 1)

    def generate_invalid_bmi(self, conditions):
        """生成不符合所有BMI条件的值"""
        if not conditions:
            return round(random.uniform(10.0, 60.0), 1)

        # 计算所有BMI条件的有效范围
        bmi_min = 10.0
        bmi_max = 60.0

        for condition in conditions:
            match = re.match(r'BMI([<>=]+)(\d+)', condition)
            if not match:
                continue

            operator, value = match.groups()
            value = float(value)

            if operator == '>':
                bmi_min = max(bmi_min, value + 0.1)
            elif operator == '>=':
                bmi_min = max(bmi_min, value)
            elif operator == '<':
                bmi_max = min(bmi_max, value - 0.1)
            elif operator == '<=':
                bmi_max = min(bmi_max, value)

        # 如果有效范围存在，生成范围外的值
        if bmi_min <= bmi_max:
            # 有效范围外有两个区间：[10.0, bmi_min) 和 (bmi_max, 60.0]
            if random.random() < 0.5:
                # 选择下界区间
                return round(random.uniform(10.0, bmi_min - 0.1), 1)
            else:
                # 选择上界区间
                return round(random.uniform(bmi_max + 0.1, 60.0), 1)
        else:
            # 条件矛盾，所有值都不符合条件
            return round(random.uniform(10.0, 60.0), 1)

    def generate_valid_age(self, conditions):
        """生成符合所有年龄条件的值"""
        age_min = 0
        age_max = 120

        for condition in conditions:
            match = re.match(r'年龄([<>=]+)(\d+)', condition)
            if not match:
                continue

            operator, value = match.groups()
            value = float(value)

            if operator == '>':
                age_min = max(age_min, value + 1)
            elif operator == '>=':
                age_min = max(age_min, value)
            elif operator == '<':
                age_max = min(age_max, value - 1)
            elif operator == '<=':
                age_max = min(age_max, value)

        return random.randint(int(age_min), int(age_max))

    def generate_invalid_age(self, conditions):
        """生成不符合所有年龄条件的值"""
        if not conditions:
            return random.randint(0, 120)

        # 计算所有年龄条件的有效范围
        age_min = 0
        age_max = 120

        for condition in conditions:
            match = re.match(r'年龄([<>=]+)(\d+)', condition)
            if not match:
                continue

            operator, value = match.groups()
            value = float(value)

            if operator == '>':
                age_min = max(age_min, value + 1)
            elif operator == '>=':
                age_min = max(age_min, value)
            elif operator == '<':
                age_max = min(age_max, value - 1)
            elif operator == '<=':
                age_max = min(age_max, value)

        # 如果有效范围存在，生成范围外的值
        if age_min <= age_max:
            # 有效范围外有两个区间：[0, age_min) 和 (age_max, 120]
            if random.random() < 0.5:
                # 选择下界区间
                if age_min > 0:
                    return random.randint(0, int(age_min - 1))
                else:
                    # 如果 age_min 是 0，无法再生成更小的数，就返回一个固定值
                    return random.randint(0, 120)
            else:
                # 选择上界区间
                if age_max < 120:
                    return random.randint(int(age_max + 1), 120)
                else:
                    # 如果 age_max 是 120，无法再生成更大的数，就返回一个固定值
                    return random.randint(0, 120)
        else:
            # 条件矛盾，所有值都不符合条件
            return random.randint(0, 120)

        # if age_min <= age_max:
        #     # 有效范围外有两个区间：[0, age_min) 和 (age_max, 120]
        #     if random.random() < 0.5:
        #         # 选择下界区间
        #         return random.randint(0, int(age_min - 1))
        #     else:
        #         # 选择上界区间
        #         return random.randint(int(age_max + 1), 120)
        # else:
        #     # 条件矛盾，所有值都不符合条件
        #     return random.randint(0, 120)

    # 使用示例
    if __name__ == "__main__":
        # 条件列表
        conditions = ['BMI>=24', '年龄>=18', '年龄<65']

        try:
            # 生成每种情况的样本
            cases = generate_all_cases(conditions)

            # 打印结果
            for case_name, samples in cases.items():
                print(f"\n情况: {case_name}")
                for i, (bmi, age) in enumerate(samples, 1):
                    print(f"样本 {i}: BMI = {bmi}, 年龄 = {age}")

        except ValueError as e:
            print(f"错误: {e}")



