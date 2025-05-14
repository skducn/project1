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

import re
import random


class BmiAgeSexPO():
    import re

    def is_match(self, value, conds):
        """
        判断某个值是否满足一组条件
        :param value: 待判断的值（float 或 str）
        :param conds: 条件列表，例如 ['BMI<13.4', 'BMI>13.0']
        :return: True / False
        """
        if not conds or conds == ["always_true"]:
            return True

        for cond in conds:
            if cond == "always_true":
                continue
            field, op, val = self.parse_condition(cond)
            val = float(val) if field != "性别" else val.strip()

            if field == "性别":
                if op == '=' and value != val:
                    return False
            elif field in ["BMI", "年龄"]:
                if op == '>' and not (value > val):
                    return False
                elif op == '>=' and not (value >= val):
                    return False
                elif op == '<' and not (value < val):
                    return False
                elif op == '<=' and not (value <= val):
                    return False
                elif op == '=' and not (value == val):
                    return False

        return True

    def parse_condition(self, condition):
        """
        将形如 'BMI<13.4' 的条件解析成 (字段名, 操作符, 值)
        """
        # 先标准化
        cond = condition.replace('>', '').replace('<', '').replace('=', '')
        match = re.match(r'^(BMI|年龄|性别)([><]=?|=)([^=]+)$', condition.strip())
        if not match:
            raise ValueError(f"无法解析条件: {condition}")
        return match.groups()

    def splitMode(self, condition):
        """
        将形如 '6<=年龄<6.5' 或 '14.7<BMI<18.8' 的复合条件拆分为两个标准条件
        :param condition: 条件字符串
        :return: 拆分后的简单条件列表
        """

        cond = condition.strip().replace(" ", "")

        # 匹配形如：6<=年龄<6.5 或 14.7<BMI<18.8
        match = re.match(r'^(\d+(?:\.\d+)?)(<=|<|>=|>)(年龄|BMI)(<=|<|>=|>)(\d+(?:\.\d+)?)$', cond)

        if not match:
            return [condition]  # 不符合格式，返回原始条件

        left_val, op1, field, op2, right_val = match.groups()

        # 判断是否是合法组合（如：a < x < b）
        if (op1 in ('<', '<=') and op2 in ('<', '<=')) or (op1 in ('>', '>=') and op2 in ('>', '><')):
            # 如果是 a < x < b 类型，转换成 x > a 且 x < b
            cond1 = f"{field}{op1}{left_val}"
            cond2 = f"{field}{op2}{right_val}"

            # 修复方向错误：例如 6<=年龄<6.5 → 年龄>=6 and 年龄<6.5
            if op1 == '<=' and op2 == '<':
                cond1 = f"{field}>={left_val}"
            elif op1 == '<' and op2 == '<=':
                cond1 = f"{field}>{left_val}"
                cond2 = f"{field}<={right_val}"
            elif op1 == '<' and op2 == '<':
                cond1 = f"{field}>{left_val}"
            elif op1 == '<=' and op2 == '<=':
                cond1 = f"{field}>={left_val}"
                cond2 = f"{field}<={right_val}"

            return [cond1, cond2]

        else:
            return [condition]

    def interconvertMode(self, condition):
        """
        互换
        将形如 '18.5>BMI' 转换为 'BMI<18.5'
        :param condition: 条件字符串
        :return: 拆分或转换后的条件列表
        """
        cond = condition.strip().replace(" ", "")

        # 匹配类似 18.5>BMI 或 24<BMI 这样的逆序写法
        match = re.match(r'^(\d+(?:\.\d+)?)(>|>=|<|<=)(BMI|年龄)$', cond)

        if match:
            value, op, field = match.groups()

            # 反转操作符方向
            if op == '>':
                return [f"{field}<{value}"]
            elif op == '>=':
                return [f"{field}<={value}"]
            elif op == '<':
                return [f"{field}>{value}"]
            elif op == '<=':
                return [f"{field}>={value}"]

        # 默认返回原条件
        return [condition]


    # def split_compound_condition22(self, condition):
    #     """
    #     将类似 '14.7<BMI<18.8' 的复合条件拆分成两个简单条件
    #     :param condition: 复合条件字符串
    #     :return: 包含两个简单条件的列表
    #     """
    #     # 检查条件中是否包含 '<' 两次
    #     if condition.count('<') == 2 and condition.count('=') == 0:
    #         parts = condition.split('<')
    #         # 构建两个简单条件
    #         condition1 = f"{parts[0]}<{parts[1]}"
    #         condition2 = f"{parts[1]}<{parts[2]}"
    #         return [condition1, condition2]
    #     elif condition.count('>') == 2 and condition.count('=') == 0:
    #         parts = condition.split('>')
    #         # 构建两个简单条件
    #         condition1 = f"{parts[0]}>{parts[1]}"
    #         condition2 = f"{parts[1]}>{parts[2]}"
    #         return [condition1, condition2]
    #     elif condition.count('>=') == 2:
    #         parts = condition.split('>=')
    #         # 构建两个简单条件
    #         condition1 = f"{parts[0]}>={parts[1]}"
    #         condition2 = f"{parts[1]}>={parts[2]}"
    #         return [condition1, condition2]
    #     return [condition]

    def normalize_condition(self, condition):
        """将全角符号替换为半角符号"""
        return condition.replace('＞', '>').replace('＜', '<').replace('＝', '=').replace(" ", "")

    # condition = self.normalize_condition(condition)

    @staticmethod
    def normalize_condition(condition):
        return condition.replace('＞', '>').replace('＜', '<').replace('＝', '=').replace(" ", "")

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有可能的条件组合情况
    #
    #     参数:
    #     conditions (list): 条件列表，例如 ['14<= 年龄＜14.5', '22.3<= BMI', '性别=男']
    #     num_samples (int): 每种情况生成的样本数量
    #
    #     返回:
    #     dict: 包含所有情况的样本字典
    #     """
    #     # 分离BMI、年龄和性别条件
    #     bmi_conditions = [c for c in conditions if 'BMI' in c]
    #     age_conditions = [c for c in conditions if '年龄' in c]
    #     gender_conditions = [c for c in conditions if '性别' in c]
    #
    #     # 生成所有可能的条件组合
    #     cases = {}
    #
    #     # 生成所有8种可能的组合 (2^3 = 8)
    #     for bmi_satisfied in [True, False]:
    #         for age_satisfied in [True, False]:
    #             for gender_satisfied in [True, False]:
    #                 case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
    #                 # print(case_name)
    #                 if case_name == 'BMI满足且年龄满足且性别满足':
    #                     case_name = 'satisfied'
    #                 cases[case_name] = [
    #                     self.generate_sample(bmi_conditions, age_conditions, gender_conditions,
    #                                     bmi_satisfied, age_satisfied, gender_satisfied)
    #                     for _ in range(num_samples)
    #                 ]
    #
    #     return cases

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有可能的条件组合情况（支持多个同字段条件）
    #
    #     参数:
    #         conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65', '性别=男']
    #         num_samples (int): 每种情况生成的样本数量
    #
    #     返回:
    #         dict: 包含各种情况的样本字典
    #     """
    #
    #     # 解析条件
    #     parsed_conditions = {
    #         "BMI": [],
    #         "年龄": [],
    #         "性别": []
    #     }
    #
    #     for cond in conditions:
    #         field = None
    #         if cond.startswith("BMI"):
    #             field = "BMI"
    #         elif cond.startswith("年龄"):
    #             field = "年龄"
    #         elif cond.startswith("性别"):
    #             field = "性别"
    #
    #         if field:
    #             parsed_conditions[field].append(cond)
    #
    #     # 如果没有某个字段的条件，则默认该字段总是满足
    #     for field in ["BMI", "年龄", "性别"]:
    #         if not parsed_conditions[field]:
    #             parsed_conditions[field] = ["always_true"]
    #
    #     # 生成所有组合
    #     cases = {}
    #
    #     # 生成所有8种可能的组合 (2^3 = 8)
    #     from itertools import product
    #     for bmi_satisfied, age_satisfied, gender_satisfied in product([True, False], repeat=3):
    #
    #         case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
    #
    #         # 将主满足条件命名为 'satisfied'
    #         if case_name == 'BMI满足且年龄满足且性别满足':
    #             case_name = 'satisfied'
    #
    #         samples = []
    #         for _ in range(num_samples):
    #             sample = {}
    #             try:
    #                 if bmi_satisfied:
    #                     sample["BMI"] = self.generate_valid_bmi(parsed_conditions["BMI"])
    #                 else:
    #                     sample["BMI"] = self.generate_invalid_bmi(parsed_conditions["BMI"])
    #
    #                 if age_satisfied:
    #                     sample["年龄"] = self.generate_valid_age(parsed_conditions["年龄"])
    #                 else:
    #                     sample["年龄"] = self.generate_invalid_age(parsed_conditions["年龄"])
    #
    #                 if gender_satisfied:
    #                     sample["性别"] = self.generate_valid_gender(parsed_conditions["性别"])
    #                 else:
    #                     sample["性别"] = self.generate_invalid_gender(parsed_conditions["性别"])
    #
    #                 samples.append(sample)
    #
    #             except Exception as e:
    #                 continue  # 跳过无效组合
    #
    #         if samples:
    #             cases[case_name] = samples
    #
    #     return cases

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有可能的条件组合情况（支持多个同字段条件）
    #
    #     参数:
    #         conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65', '性别=男']
    #         num_samples (int): 每种情况生成的样本数量
    #
    #     返回:
    #         dict: 包含各种情况的样本字典
    #     """
    #
    #     # 解析条件
    #     parsed_conditions = {
    #         "BMI": [],
    #         "年龄": [],
    #         "性别": []
    #     }
    #
    #     for cond in conditions:
    #         field = None
    #         if cond.startswith("BMI"):
    #             field = "BMI"
    #         elif cond.startswith("年龄"):
    #             field = "年龄"
    #         elif cond.startswith("性别"):
    #             field = "性别"
    #
    #         if field:
    #             parsed_conditions[field].append(cond)
    #
    #     for field in ["BMI", "年龄", "性别"]:
    #         if not parsed_conditions[field]:
    #             parsed_conditions[field] = ["always_true"]
    #
    #     # 生成所有组合
    #     cases = {}
    #     from itertools import product
    #
    #     for bmi_satisfied, age_satisfied, gender_satisfied in product([True, False], repeat=3):
    #
    #         case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
    #         if case_name == 'BMI满足且年龄满足且性别满足':
    #             case_name = 'satisfied'
    #
    #         samples = []
    #
    #         # 手动添加一个固定值样本
    #         if bmi_satisfied and any('=' in c for c in bmi_conditions):
    #             fixed_bmi = None
    #             for cond in bmi_conditions:
    #                 if '=' in cond:
    #                     parts = cond.split('=')
    #                     if 'BMI' in parts[0]:
    #                         fixed_bmi = float(parts[1].strip())
    #                     elif 'BMI' in parts[1]:
    #                         fixed_bmi = float(parts[0].strip())
    #             if fixed_bmi is not None:
    #                 sample_fixed = {
    #                     "BMI": fixed_bmi,
    #                     "年龄": self.generate_valid_age(age_conditions) if age_satisfied else self.generate_invalid_age(
    #                         age_conditions),
    #                     "性别": self.generate_valid_gender(
    #                         gender_conditions) if gender_satisfied else self.generate_invalid_gender(gender_conditions)
    #                 }
    #                 if self.is_match(sample_fixed["BMI"], bmi_conditions) and \
    #                         self.is_match(sample_fixed["年龄"], age_conditions) and \
    #                         self.is_match(sample_fixed["性别"], gender_conditions):
    #                     samples.append(sample_fixed)
    #
    #         # 再生成其他随机样本
    #         while len(samples) < num_samples:
    #             sample = {}
    #             try:
    #                 if bmi_satisfied:
    #                     sample["BMI"] = self.generate_valid_bmi(bmi_conditions)
    #                 else:
    #                     sample["BMI"] = self.generate_invalid_bmi(bmi_conditions)
    #
    #                 if age_satisfied:
    #                     sample["年龄"] = self.generate_valid_age(age_conditions)
    #                 else:
    #                     sample["年龄"] = self.generate_invalid_age(age_conditions)
    #
    #                 if gender_satisfied:
    #                     sample["性别"] = self.generate_valid_gender(gender_conditions)
    #                 else:
    #                     sample["性别"] = self.generate_invalid_gender(gender_conditions)
    #
    #                 # 校验是否满足组合条件
    #                 if (
    #                         self.is_match(sample["BMI"], bmi_conditions if satisfy_bmi else []) and
    #                         self.is_match(sample["年龄"], age_conditions if satisfy_age else []) and
    #                         self.is_match(sample["性别"], gender_conditions if satisfy_gender else [])
    #                 ):
    #                     samples.append(sample)
    #             except Exception as e:
    #                 continue
    #
    #         if samples:
    #             cases[case_name] = samples
    #
    #     return cases

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有可能的条件组合情况（支持多个同字段条件）
    #
    #     参数:
    #         conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65', '性别=男']
    #         num_samples (int): 每种情况生成的样本数量
    #
    #     返回:
    #         dict: 包含各种情况的样本字典
    #     """
    #
    #     # 解析条件
    #     parsed_conditions = {
    #         "BMI": [],
    #         "年龄": [],
    #         "性别": []
    #     }
    #
    #     for cond in conditions:
    #         field = None
    #         if cond.startswith("BMI"):
    #             field = "BMI"
    #         elif cond.startswith("年龄"):
    #             field = "年龄"
    #         elif cond.startswith("性别"):
    #             field = "性别"
    #
    #         if field:
    #             parsed_conditions[field].append(cond)
    #
    #     for field in ["BMI", "年龄", "性别"]:
    #         if not parsed_conditions[field]:
    #             parsed_conditions[field] = ["always_true"]
    #
    #     # 生成所有组合
    #     cases = {}
    #     from itertools import product
    #
    #     for bmi_satisfied, age_satisfied, gender_satisfied in product([True, False], repeat=3):
    #
    #         case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
    #         if case_name == 'BMI满足且年龄满足且性别满足':
    #             case_name = 'satisfied'
    #
    #         samples = []
    #
    #         # 如果有等值匹配，优先插入固定值样本
    #         bmi_conds = parsed_conditions["BMI"]
    #         age_conds = parsed_conditions["年龄"]
    #         gender_conds = parsed_conditions["性别"]
    #
    #         # 手动插入一个固定值样本
    #         if bmi_satisfied and any('=' in c for c in bmi_conds) and not any('<' in c or '>' in c for c in bmi_conds):
    #             fixed_bmi = None
    #             for cond in bmi_conds:
    #                 if '=' in cond:
    #                     parts = cond.split('=')
    #                     if 'BMI' in parts[0]:
    #                         fixed_bmi = float(parts[1].strip())
    #                     elif 'BMI' in parts[1]:
    #                         fixed_bmi = float(parts[0].strip())
    #             if fixed_bmi is not None:
    #                 sample_fixed = {
    #                     "BMI": fixed_bmi,
    #                     "年龄": self.generate_valid_age(age_conds) if age_satisfied else self.generate_invalid_age(
    #                         age_conds),
    #                     "性别": self.generate_valid_gender(
    #                         gender_conds) if gender_satisfied else self.generate_invalid_gender(gender_conds)
    #                 }
    #                 if self.is_match(sample_fixed["BMI"], bmi_conds) and \
    #                         self.is_match(sample_fixed["年龄"], age_conds) and \
    #                         self.is_match(sample_fixed["性别"], gender_conds):
    #                     samples.append(sample_fixed)
    #
    #         # 再生成其他随机样本
    #         while len(samples) < num_samples:
    #             sample = {}
    #             try:
    #                 if bmi_satisfied:
    #                     sample["BMI"] = self.generate_valid_bmi(bmi_conds)
    #                 else:
    #                     sample["BMI"] = self.generate_invalid_bmi(bmi_conds)
    #
    #                 if age_satisfied:
    #                     sample["年龄"] = self.generate_valid_age(age_conds)
    #                 else:
    #                     sample["年龄"] = self.generate_invalid_age(age_conds)
    #
    #                 if gender_satisfied:
    #                     sample["性别"] = self.generate_valid_gender(gender_conds)
    #                 else:
    #                     sample["性别"] = self.generate_invalid_gender(gender_conds)
    #
    #                 # 校验是否满足组合条件
    #                 if (
    #                         self.is_match(sample["BMI"], bmi_conds if bmi_satisfied else []) and
    #                         self.is_match(sample["年龄"], age_conds if age_satisfied else []) and
    #                         self.is_match(sample["性别"], gender_conds if gender_satisfied else [])
    #                 ):
    #                     samples.append(sample)
    #             except Exception as e:
    #                 continue
    #
    #         if samples:
    #             cases[case_name] = samples
    #
    #     return cases

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有可能的条件组合情况（支持多个同字段条件）
    #
    #     参数:
    #         conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65', '性别=男']
    #         num_samples (int): 每种情况生成的样本数量
    #
    #     返回:
    #         dict: 包含各种情况的样本字典
    #     """
    #
    #     # 解析条件
    #     parsed_conditions = {
    #         "BMI": [],
    #         "年龄": [],
    #         "性别": []
    #     }
    #
    #     for cond in conditions:
    #         field = None
    #         if cond.startswith("BMI"):
    #             field = "BMI"
    #         elif cond.startswith("年龄"):
    #             field = "年龄"
    #         elif cond.startswith("性别"):
    #             field = "性别"
    #
    #         if field:
    #             parsed_conditions[field].append(cond)
    #
    #     for field in ["BMI", "年龄", "性别"]:
    #         if not parsed_conditions[field]:
    #             parsed_conditions[field] = ["always_true"]
    #
    #     # 生成所有组合
    #     cases = {}
    #     from itertools import product
    #
    #     for bmi_satisfied, age_satisfied, gender_satisfied in product([True, False], repeat=3):
    #
    #         case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
    #         if case_name == 'BMI满足且年龄满足且性别满足':
    #             case_name = 'satisfied'
    #
    #         samples = []
    #
    #         # 获取当前组合的字段条件
    #         bmi_conds = parsed_conditions["BMI"]
    #         age_conds = parsed_conditions["年龄"]
    #         gender_conds = parsed_conditions["性别"]
    #
    #         # 强制插入一个固定值样本（比如 BMI=16.4）
    #         if bmi_satisfied and not any('=' in c for c in bmi_conds):
    #             fixed_bmi = None
    #             for cond in bmi_conds:
    #                 if '>=' in cond:
    #                     parts = cond.split('>=')
    #                     if 'BMI' in parts[0]:
    #                         fixed_bmi = float(parts[1].strip())
    #                         break
    #
    #             if fixed_bmi is not None:
    #                 sample_fixed = {
    #                     "BMI": fixed_bmi,
    #                     "年龄": self.generate_valid_age(age_conds),
    #                     "性别": self.generate_valid_gender(gender_conds)
    #                 }
    #                 if self.is_match(sample_fixed["BMI"], bmi_conds):
    #                     samples.append(sample_fixed)
    #
    #         # 再生成其他随机样本
    #         while len(samples) < num_samples:
    #             sample = {}
    #             try:
    #                 if bmi_satisfied:
    #                     sample["BMI"] = self.generate_valid_bmi(bmi_conds)
    #                 else:
    #                     sample["BMI"] = self.generate_invalid_bmi(bmi_conds)
    #
    #                 if age_satisfied:
    #                     sample["年龄"] = self.generate_valid_age(age_conds)
    #                 else:
    #                     sample["年龄"] = self.generate_invalid_age(age_conds)
    #
    #                 if gender_satisfied:
    #                     sample["性别"] = self.generate_valid_gender(gender_conds)
    #                 else:
    #                     sample["性别"] = self.generate_invalid_gender(gender_conds)
    #
    #                 # 校验是否满足组合条件
    #                 if (
    #                         self.is_match(sample["BMI"], bmi_conds if bmi_satisfied else []) and
    #                         self.is_match(sample["年龄"], age_conds if age_satisfied else []) and
    #                         self.is_match(sample["性别"], gender_conds if gender_satisfied else [])
    #                 ):
    #                     samples.append(sample)
    #             except Exception as e:
    #                 continue
    #
    #         if samples:
    #             cases[case_name] = samples
    #
    #     return cases

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有可能的条件组合情况（支持多个同字段条件）
    #
    #     参数:
    #         conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65', '性别=男']
    #         num_samples (int): 每种情况生成的样本数量
    #
    #     返回:
    #         dict: 包含各种情况的样本字典
    #     """
    #
    #     # 解析条件
    #     parsed_conditions = {
    #         "BMI": [],
    #         "年龄": [],
    #         "性别": []
    #     }
    #
    #     for cond in conditions:
    #         field = None
    #         if cond.startswith("BMI"):
    #             field = "BMI"
    #         elif cond.startswith("年龄"):
    #             field = "年龄"
    #         elif cond.startswith("性别"):
    #             field = "性别"
    #
    #         if field:
    #             parsed_conditions[field].append(cond)
    #
    #     for field in ["BMI", "年龄", "性别"]:
    #         if not parsed_conditions[field]:
    #             parsed_conditions[field] = ["always_true"]
    #
    #     # 生成所有组合
    #     cases = {}
    #     from itertools import product
    #
    #     for bmi_satisfied, age_satisfied, gender_satisfied in product([True, False], repeat=3):
    #
    #         case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
    #         if case_name == 'BMI满足且年龄满足且性别满足':
    #             case_name = 'satisfied'
    #
    #         samples = []
    #
    #         while len(samples) < num_samples:
    #             sample = {}
    #
    #             # 强制生成一个固定值样本
    #             if bmi_satisfied:
    #                 sample["BMI"] = self.generate_valid_bmi(parsed_conditions["BMI"])
    #             else:
    #                 sample["BMI"] = self.generate_invalid_bmi(parsed_conditions["BMI"])
    #
    #             if age_satisfied:
    #                 sample["年龄"] = self.generate_valid_age(parsed_conditions["年龄"])
    #             else:
    #                 sample["年龄"] = self.generate_invalid_age(parsed_conditions["年龄"])
    #
    #             if gender_satisfied:
    #                 sample["性别"] = self.generate_valid_gender(parsed_conditions["性别"])
    #             else:
    #                 sample["性别"] = self.generate_invalid_gender(parsed_conditions["性别"])
    #
    #             # 校验是否满足组合条件
    #             if (
    #                     self.is_match(sample["BMI"], parsed_conditions["BMI"] if bmi_satisfied else []) and
    #                     self.is_match(sample["年龄"], parsed_conditions["年龄"] if age_satisfied else []) and
    #                     self.is_match(sample["性别"], parsed_conditions["性别"] if gender_satisfied else [])
    #             ):
    #                 samples.append(sample)
    #
    #         if samples:
    #             cases[case_name] = samples
    #
    #     return cases

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有可能的条件组合情况（支持多个同字段条件）
    #
    #     参数:
    #         conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65', '性别=男']
    #         num_samples (int): 每种情况生成的样本数量
    #
    #     返回:
    #         dict: 包含各种情况的样本字典
    #     """
    #
    #     # 解析条件
    #     parsed_conditions = {
    #         "BMI": [],
    #         "年龄": [],
    #         "性别": []
    #     }
    #
    #     for cond in conditions:
    #         field = None
    #         if cond.startswith("BMI"):
    #             field = "BMI"
    #         elif cond.startswith("年龄"):
    #             field = "年龄"
    #         elif cond.startswith("性别"):
    #             field = "性别"
    #
    #         if field:
    #             parsed_conditions[field].append(cond)
    #
    #     for field in ["BMI", "年龄", "性别"]:
    #         if not parsed_conditions[field]:
    #             parsed_conditions[field] = ["always_true"]
    #
    #     # 生成所有组合
    #     cases = {}
    #     from itertools import product
    #
    #     for bmi_satisfied, age_satisfied, gender_satisfied in product([True, False], repeat=3):
    #
    #         case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
    #         if case_name == 'BMI满足且年龄满足且性别满足':
    #             case_name = 'satisfied'
    #
    #         samples = []
    #
    #         while len(samples) < num_samples:
    #             sample = {}
    #
    #             # 强制生成一个固定值样本（比如 BMI=16.4）
    #             if bmi_satisfied and len(samples) == 0:
    #                 # 获取最小边界值
    #                 min_val = None
    #                 for cond in parsed_conditions["BMI"]:
    #                     if '>=' in cond:
    #                         parts = cond.split('>=')
    #                         if 'BMI' in parts[0]:
    #                             min_val = float(parts[1].strip())
    #
    #                 if min_val is not None:
    #                     sample["BMI"] = round(min_val, 1)
    #                 else:
    #                     sample["BMI"] = self.generate_valid_bmi(parsed_conditions["BMI"])
    #             else:
    #                 sample["BMI"] = self.generate_valid_bmi(parsed_conditions["BMI"])
    #
    #             # 生成其他字段
    #             if age_satisfied:
    #                 sample["年龄"] = self.generate_valid_age(parsed_conditions["年龄"])
    #             else:
    #                 sample["年龄"] = self.generate_invalid_age(parsed_conditions["年龄"])
    #
    #             if gender_satisfied:
    #                 sample["性别"] = self.generate_valid_gender(parsed_conditions["性别"])
    #             else:
    #                 sample["性别"] = self.generate_invalid_gender(parsed_conditions["性别"])
    #
    #             # 校验是否满足组合条件
    #             if (
    #                     self.is_match(sample["BMI"], parsed_conditions["BMI"] if bmi_satisfied else []) and
    #                     self.is_match(sample["年龄"], parsed_conditions["年龄"] if age_satisfied else []) and
    #                     self.is_match(sample["性别"], parsed_conditions["性别"] if gender_satisfied else [])
    #             ):
    #                 samples.append(sample)
    #
    #         if samples:
    #             cases[case_name] = samples
    #
    #     return cases

    def generate_all_cases(self, conditions, num_samples=None):
        """
        生成所有可能的条件组合情况（支持多个同字段条件）

        参数:
            conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '性别=男']
            num_samples (int): 每种情况生成的样本数量（默认根据条件自动判断）

        返回:
            dict: 包含各种情况的样本字典
        """

        # 自动判断样本数
        if num_samples is None:
            has_gte_or_lte = any(
                '>=' in cond or '<=' in cond for cond in conditions if cond.startswith('BMI')
            )
            num_samples = 2 if has_gte_or_lte else 1

        # 解析条件
        parsed_conditions = {
            "BMI": [],
            "年龄": [],
            "性别": []
        }

        for cond in conditions:
            field = None
            if cond.startswith("BMI"):
                field = "BMI"
            elif cond.startswith("年龄"):
                field = "年龄"
            elif cond.startswith("性别"):
                field = "性别"

            if field:
                parsed_conditions[field].append(cond)

        for field in ["BMI", "年龄", "性别"]:
            if not parsed_conditions[field]:
                parsed_conditions[field] = ["always_true"]

        # 生成所有组合
        cases = {}
        from itertools import product

        for bmi_satisfied, age_satisfied, gender_satisfied in product([True, False], repeat=3):

            case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
            if case_name == 'BMI满足且年龄满足且性别满足':
                case_name = 'satisfied'

            samples = []

            while len(samples) < num_samples:
                sample = {}

                # 强制插入第一个样本为边界值
                if bmi_satisfied and len(samples) == 0:
                    min_val = None
                    for cond in parsed_conditions["BMI"]:
                        if '>=' in cond:
                            parts = cond.split('>=')
                            if 'BMI' in parts[0]:
                                min_val = float(parts[1].strip())
                        elif '<=' in cond:
                            parts = cond.split('<=')
                            if 'BMI' in parts[0]:
                                min_val = float(parts[1].strip())

                    if min_val is not None:
                        sample["BMI"] = round(min_val, 1)
                    else:
                        sample["BMI"] = self.generate_valid_bmi(parsed_conditions["BMI"])
                else:
                    sample["BMI"] = self.generate_valid_bmi(parsed_conditions["BMI"])

                # 生成其他字段
                if age_satisfied:
                    sample["年龄"] = self.generate_valid_age(parsed_conditions["年龄"])
                else:
                    sample["年龄"] = self.generate_invalid_age(parsed_conditions["年龄"])

                if gender_satisfied:
                    sample["性别"] = self.generate_valid_gender(parsed_conditions["性别"])
                else:
                    sample["性别"] = self.generate_invalid_gender(parsed_conditions["性别"])

                # 校验是否满足组合条件
                if (
                        self.is_match(sample["BMI"], parsed_conditions["BMI"] if bmi_satisfied else []) and
                        self.is_match(sample["年龄"], parsed_conditions["年龄"] if age_satisfied else []) and
                        self.is_match(sample["性别"], parsed_conditions["性别"] if gender_satisfied else [])
                ):
                    samples.append(sample)

            if samples:
                cases[case_name] = samples

        return cases

    def get_case_name(self, bmi_satisfied, age_satisfied, gender_satisfied):
        """生成条件组合的名称"""
        parts = []
        if bmi_satisfied:
            parts.append("BMI满足")
        else:
            parts.append("BMI不满足")

        if age_satisfied:
            parts.append("年龄满足")
        else:
            parts.append("年龄不满足")

        if gender_satisfied:
            parts.append("性别满足")
        else:
            parts.append("性别不满足")

        return "且".join(parts)

    # def generate_sample(self, bmi_conditions, age_conditions, gender_conditions,
    #                     satisfy_bmi, satisfy_age, satisfy_gender):
    #     """
    #     生成一个符合指定条件组合的样本
    #
    #     参数:
    #     bmi_conditions (list): BMI相关条件
    #     age_conditions (list): 年龄相关条件
    #     gender_conditions (list): 性别相关条件
    #     satisfy_bmi (bool): 是否满足BMI条件
    #     satisfy_age (bool): 是否满足年龄条件
    #     satisfy_gender (bool): 是否满足性别条件
    #
    #     返回:
    #     dict: 包含BMI、年龄和性别的字典
    #     """
    #     # 生成BMI值
    #     if satisfy_bmi:
    #         bmi = self.generate_valid_bmi(bmi_conditions)
    #     else:
    #         bmi = self.generate_invalid_bmi(bmi_conditions)
    #
    #     # 生成年龄值
    #     if satisfy_age:
    #         age = self.generate_valid_age(age_conditions)
    #     else:
    #         age = self.generate_invalid_age(age_conditions)
    #
    #     # 生成性别值
    #     if satisfy_gender:
    #         gender = self.generate_valid_gender(gender_conditions)
    #     else:
    #         gender = self.generate_invalid_gender(gender_conditions)
    #
    #     return {'BMI': bmi, '年龄': age, '性别': gender}

    # def generate_sample(self, bmi_conditions, age_conditions, gender_conditions, satisfy_bmi, satisfy_age, satisfy_gender):
    #     attempts = 0
    #     while attempts < 100:  # 防止死循环
    #         sample = {}
    #
    #         if satisfy_bmi:
    #             sample["BMI"] = self.generate_valid_bmi(bmi_conditions)
    #         else:
    #             sample["BMI"] = self.generate_invalid_bmi(bmi_conditions)
    #
    #         if satisfy_age:
    #             sample["年龄"] = self.generate_valid_age(age_conditions)
    #         else:
    #             sample["年龄"] = self.generate_invalid_age(age_conditions)
    #
    #         if satisfy_gender:
    #             sample["性别"] = self.generate_valid_gender(gender_conditions)
    #         else:
    #             sample["性别"] = self.generate_invalid_gender(gender_conditions)
    #
    #         # 校验是否满足指定组合
    #         if (
    #                 self.is_match(sample["BMI"], bmi_conditions if satisfy_bmi else []) and
    #                 self.is_match(sample["年龄"], age_conditions if satisfy_age else []) and
    #                 self.is_match(sample["性别"], gender_conditions if satisfy_gender else [])
    #         ):
    #             return sample
    #
    #         attempts += 1
    #
    #     raise ValueError("无法生成符合要求的样本，请检查条件是否有冲突")

    def generate_sample(self, bmi_conditions, age_conditions, gender_conditions,
                        satisfy_bmi, satisfy_age, satisfy_gender):
        attempts = 0
        while attempts < 100:  # 防止死循环
            sample = {}

            if satisfy_bmi:
                if any('=' in cond and '>=' not in cond and '<=' not in cond for cond in bmi_conditions):
                    # 如果有等值匹配条件（如 BMI=16.4），优先使用该值
                    for cond in bmi_conditions:
                        if '=' in cond:
                            parts = cond.split('=')
                            if 'BMI' in parts[0]:
                                sample["BMI"] = float(parts[1].strip())
                            elif 'BMI' in parts[1]:
                                sample["BMI"] = float(parts[0].strip())
                else:
                    sample["BMI"] = self.generate_valid_bmi(bmi_conditions)
            else:
                sample["BMI"] = self.generate_invalid_bmi(bmi_conditions)

            if satisfy_age:
                sample["年龄"] = self.generate_valid_age(age_conditions)
            else:
                sample["年龄"] = self.generate_invalid_age(age_conditions)

            if satisfy_gender:
                sample["性别"] = self.generate_valid_gender(gender_conditions)
            else:
                sample["性别"] = self.generate_invalid_gender(gender_conditions)

            # 校验是否满足组合条件
            if (
                    self.is_match(sample["BMI"], bmi_conditions if satisfy_bmi else []) and
                    self.is_match(sample["年龄"], age_conditions if satisfy_age else []) and
                    self.is_match(sample["性别"], gender_conditions if satisfy_gender else [])
            ):
                return sample

            attempts += 1

        raise ValueError("无法生成符合要求的样本，请检查条件是否有冲突")

    # def generate_valid_bmi(self, conditions):
    #     """生成符合所有BMI条件的值"""
    #     if not conditions:
    #         return round(random.uniform(10.0, 60.0), 1)
    #
    #     # 初始化默认范围
    #     bmi_min = 10.0
    #     bmi_max = 60.0
    #
    #     for condition in conditions:
    #         if '=' in condition and '<=' in condition:
    #             # 处理类似 "BMI<=24"
    #             parts = condition.split('<=')
    #             if 'BMI' in parts[0]:
    #                 bmi_max = min(bmi_max, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 bmi_min = max(bmi_min, float(parts[0].strip()))
    #
    #         elif '=' in condition and '>=' in condition:
    #             # 处理类似 "BMI>=24"
    #             parts = condition.split('>=')
    #             if 'BMI' in parts[0]:
    #                 bmi_min = max(bmi_min, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 bmi_max = min(bmi_max, float(parts[0].strip()))
    #
    #         elif '<' in condition:
    #             # 处理类似 "BMI<24" 或 "24>BMI"
    #             parts = condition.split('<')
    #             if 'BMI' in parts[0]:
    #                 # BMI < 24
    #                 bmi_max = min(bmi_max, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 # 24 < BMI
    #                 bmi_min = max(bmi_min, float(parts[0].strip()))
    #
    #         elif '>' in condition:
    #             # 处理类似 "BMI>24" 或 "24>BMI"
    #             parts = condition.split('>')
    #             if 'BMI' in parts[0]:
    #                 # BMI > 24
    #                 bmi_min = max(bmi_min, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 # 24 > BMI → BMI < 24
    #                 bmi_max = min(bmi_max, float(parts[0].strip()))
    #
    #         elif '=' in condition:
    #             # 处理固定值，如 "BMI=24"
    #             parts = condition.split('=')
    #             if 'BMI' in parts[0]:
    #                 return float(parts[1].strip())
    #             elif 'BMI' in parts[1]:
    #                 return float(parts[0].strip())
    #
    #     return round(random.uniform(bmi_min, bmi_max), 1)

    # def generate_valid_bmi(self, conditions):
    #     """生成符合所有BMI条件的值"""
    #     if not conditions:
    #         return round(random.uniform(10.0, 60.0), 1)
    #
    #     # 初始化默认范围
    #     bmi_min = 10.0
    #     bmi_max = 60.0
    #
    #     fixed_value = None
    #     for condition in conditions:
    #         if '=' in condition and '>=' not in condition and '<=' not in condition:
    #             parts = condition.split('=')
    #             if 'BMI' in parts[0] or 'BMI' in parts[1]:
    #                 fixed_value = float(parts[1].strip()) if 'BMI' in parts[0] else float(parts[0].strip())
    #
    #     if fixed_value is not None:
    #         return fixed_value
    #
    #     for condition in conditions:
    #         if '=' in condition and '<=' in condition:
    #             parts = condition.split('<=')
    #             if 'BMI' in parts[0]:
    #                 bmi_max = min(bmi_max, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 bmi_min = max(bmi_min, float(parts[0].strip()))
    #
    #         elif '=' in condition and '>=' in condition:
    #             parts = condition.split('>=')
    #             if 'BMI' in parts[0]:
    #                 bmi_min = max(bmi_min, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 bmi_max = min(bmi_max, float(parts[0].strip()))
    #
    #         elif '<' in condition:
    #             parts = condition.split('<')
    #             if 'BMI' in parts[0]:
    #                 bmi_max = min(bmi_max, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 bmi_min = max(bmi_min, float(parts[0].strip()))
    #
    #         elif '>' in condition:
    #             parts = condition.split('>')
    #             if 'BMI' in parts[0]:
    #                 bmi_min = max(bmi_min, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 bmi_max = min(bmi_max, float(parts[0].strip()))
    #
    #     return round(random.uniform(bmi_min, bmi_max), 1)

    def generate_valid_bmi(self, conditions):
        """生成符合所有BMI条件的值"""
        if not conditions:
            return round(random.uniform(10.0, 60.0), 1)

        # 初始化默认范围
        bmi_min = 10.0
        bmi_max = 60.0

        fixed_value = None
        for condition in conditions:
            if '=' in condition and '>=' not in condition and '<=' not in condition:
                parts = condition.split('=')
                if 'BMI' in parts[0]:
                    fixed_value = float(parts[1].strip())
                elif 'BMI' in parts[1]:
                    fixed_value = float(parts[0].strip())

        if fixed_value is not None:
            return fixed_value

        for condition in conditions:
            if '=' in condition and '<=' in condition:
                parts = condition.split('<=')
                if 'BMI' in parts[0]:
                    bmi_max = min(bmi_max, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    bmi_min = max(bmi_min, float(parts[0].strip()))

            elif '=' in condition and '>=' in condition:
                parts = condition.split('>=')
                if 'BMI' in parts[0]:
                    bmi_min = max(bmi_min, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    bmi_max = min(bmi_max, float(parts[0].strip()))

            elif '<' in condition:
                parts = condition.split('<')
                if 'BMI' in parts[0]:
                    bmi_max = min(bmi_max, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    bmi_min = max(bmi_min, float(parts[0].strip()))

            elif '>' in condition:
                parts = condition.split('>')
                if 'BMI' in parts[0]:
                    bmi_min = max(bmi_min, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    bmi_max = min(bmi_max, float(parts[0].strip()))

        return round(random.uniform(bmi_min, bmi_max), 1)

    def generate_invalid_bmi(self, conditions):
        if not conditions:
            return round(random.uniform(10.0, 60.0), 1)

        bmi_min = 10.0
        bmi_max = 60.0

        for condition in conditions:
            if '=' in condition and '<=' in condition:
                parts = condition.split('<=')
                if 'BMI' in parts[0]:
                    bmi_max = min(bmi_max, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    bmi_min = max(bmi_min, float(parts[0].strip()))
            elif '=' in condition and '>=' in condition:
                parts = condition.split('>=')
                if 'BMI' in parts[0]:
                    bmi_min = max(bmi_min, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    bmi_max = min(bmi_max, float(parts[0].strip()))
            elif '<' in condition:
                parts = condition.split('<')
                if 'BMI' in parts[0]:
                    # BMI < X → 不满足时要 > X
                    bmi_min = max(bmi_min, float(parts[1].strip()) + 0.1)
                elif 'BMI' in parts[1]:
                    # X < BMI → 不满足时要 < X
                    bmi_max = min(bmi_max, float(parts[0].strip()) - 0.1)
            elif '>' in condition:
                parts = condition.split('>')
                if 'BMI' in parts[0]:
                    # BMI > X → 不满足时要 <= X
                    bmi_max = min(bmi_max, float(parts[1].strip()) - 0.1)
                elif 'BMI' in parts[1]:
                    # X > BMI → 不满足时要 >= X
                    bmi_min = max(bmi_min, float(parts[0].strip()) + 0.1)
            elif '=' in condition:
                parts = condition.split('=')
                if 'BMI' in parts[0] or 'BMI' in parts[1]:
                    fixed_value = float(parts[1].strip() if 'BMI' in parts[0] else parts[0].strip())
                    while True:
                        value = round(random.uniform(10.0, 60.0), 1)
                        if value != fixed_value:
                            return value

        if random.random() < 0.5:
            return round(random.uniform(10.0, bmi_min - 0.1), 1)
        else:
            return round(random.uniform(bmi_max + 0.1, 60.0), 1)

    # def generate_invalid_bmi(self, conditions):
    #     """生成不符合所有BMI条件的值"""
    #     if not conditions:
    #         return round(random.uniform(10.0, 60.0), 1)
    #
    #     # 解析条件中的BMI有效范围
    #     bmi_min = 10.0
    #     bmi_max = 60.0
    #
    #     # for condition in conditions:
    #     #     if '<=' in condition:
    #     #         parts = condition.split('<=')
    #     #         if 'BMI' in parts[1]:
    #     #             bmi_min = max(bmi_min, float(parts[0].strip()))
    #     #     elif '>=' in condition:
    #     #         parts = condition.split('>=')
    #     #         if 'BMI' in parts[0]:
    #     #             bmi_min = max(bmi_min, float(parts[1].strip()))
    #     #     elif '<' in condition:
    #     #         parts = condition.split('<')
    #     #         if 'BMI' in parts[0]:
    #     #             bmi_max = min(bmi_max, float(parts[1].strip()))
    #     #     elif '>' in condition:
    #     #         parts = condition.split('>')
    #     #         if 'BMI' in parts[0]:
    #     #             bmi_max = min(bmi_max, float(parts[1].strip()))
    #     for condition in conditions:
    #         if '<=' in condition:
    #             parts = condition.split('<=')
    #             if 'BMI' in parts[1]:
    #                 bmi_min = max(bmi_min, float(parts[0].strip()))
    #         elif '>=' in condition:
    #             parts = condition.split('>=')
    #             if 'BMI' in parts[0]:
    #                 bmi_min = max(bmi_min, float(parts[1].strip()))
    #         elif '<' in condition:
    #             parts = condition.split('<')
    #             if 'BMI' in parts[0]:
    #                 bmi_max = min(bmi_max, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 bmi_max = min(bmi_max, float(parts[0].strip()))
    #         elif '>' in condition:
    #             parts = condition.split('>')
    #             if 'BMI' in parts[0]:
    #                 bmi_min = max(bmi_min, float(parts[1].strip()))
    #             elif 'BMI' in parts[1]:
    #                 bmi_min = max(bmi_min, float(parts[0].strip()))
    #
    #
    #     # 生成范围外的值
    #     if random.random() < 0.5:
    #         return round(random.uniform(10.0, bmi_min - 0.1), 1)
    #     else:
    #         return round(random.uniform(bmi_max + 0.1, 60.0), 1)

    # def generate_valid_age(self, conditions):
    #     """生成符合所有年龄条件的整数值"""
    #     if not conditions:
    #         return random.randint(0, 120)
    #
    #     age_min = 0
    #     age_max = 120
    #     fixed_value = None
    #
    #     for condition in conditions:
    #         if '=' in condition:
    #             parts = condition.split('=')
    #             if '年龄' in parts[0]:
    #                 fixed_value = int(parts[1].strip())
    #         elif '<=' in condition and '＜' in condition:
    #             parts = condition.split('＜')
    #             lower_part = parts[0].split('<=')
    #             age_min = max(age_min, int(lower_part[0].strip()))
    #             age_max = min(age_max, int(parts[1].strip()))
    #         elif '<=' in condition:
    #             parts = condition.split('<=')
    #             if '年龄' in parts[1]:
    #                 age_min = max(age_min, int(parts[0].strip()))
    #         elif '>=' in condition:
    #             parts = condition.split('>=')
    #             if '年龄' in parts[0]:
    #                 age_min = max(age_min, int(parts[1].strip()))
    #         elif '<' in condition:
    #             parts = condition.split('<')
    #             if '年龄' in parts[0]:
    #                 age_max = min(age_max, int(parts[1].strip()) - 1)
    #             elif '年龄' in parts[1]:
    #                 age_max = min(age_max, int(parts[0].strip()) - 1)
    #         elif '>' in condition:
    #             parts = condition.split('>')
    #             if '年龄' in parts[0]:
    #                 age_min = max(age_min, int(parts[1].strip()) + 1)
    #             elif '年龄' in parts[1]:
    #                 age_min = max(age_min, int(parts[0].strip()) + 1)
    #
    #     # 如果有固定值，返回该值
    #     if fixed_value is not None:
    #         return fixed_value
    #
    #     # 确保范围有效
    #     if age_min > age_max:
    #         raise ValueError(f"年龄条件冲突，无法生成合法值：{conditions}")
    #
    #     return random.randint(age_min, age_max)



    def generate_valid_age(self, conditions):
        """生成符合所有年龄条件的值"""
        if not conditions:
            return random.randint(0, 120)

        # 解析条件中的年龄范围
        age_min = 0
        age_max = 120

        for condition in conditions:
            if '=' in condition and '<=' in condition:
                parts = condition.split('<=')
                if '年龄' in parts[0]:
                    age_max = min(age_max, float(parts[1].strip()))
                elif '年龄' in parts[1]:
                    age_min = max(age_min, float(parts[0].strip()))
            elif '=' in condition and '>=' in condition:
                parts = condition.split('>=')
                if '年龄' in parts[0]:
                    age_min = max(age_min, float(parts[1].strip()))
                elif '年龄' in parts[1]:
                    age_max = min(age_max, float(parts[0].strip()))
            elif '<' in condition:
                parts = condition.split('<')
                if '年龄' in parts[0]:
                    age_max = min(age_max, float(parts[1].strip()))
                elif '年龄' in parts[1]:
                    age_min = max(age_min, float(parts[0].strip()))
            elif '>' in condition:
                parts = condition.split('>')
                if '年龄' in parts[0]:
                    age_min = max(age_min, float(parts[1].strip()))
                elif '年龄' in parts[1]:
                    age_max = min(age_max, float(parts[0].strip()))
            elif '=' in condition:
                parts = condition.split('=')
                if '年龄' in parts[0]:
                    return float(parts[1].strip())
                elif '年龄' in parts[1]:
                    return float(parts[0].strip())

        # 生成范围内的随机年龄（保留一位小数）
        return round(random.uniform(age_min, age_max), 1)




    # def generate_invalid_age(self, conditions):
    #     """生成不符合所有年龄条件的整数值"""
    #     if not conditions:
    #         return random.randint(0, 120)
    #
    #     age_min = 0
    #     age_max = 120
    #     fixed_value = None
    #
    #     for condition in conditions:
    #         if '=' in condition:
    #             parts = condition.split('=')
    #             if '年龄' in parts[0]:
    #                 fixed_value = int(parts[1].strip())
    #         elif '<=' in condition and '＜' in condition:
    #             parts = condition.split('＜')
    #             lower_part = parts[0].split('<=')
    #             age_min = max(age_min, int(lower_part[0].strip()))
    #             age_max = min(age_max, int(parts[1].strip()))
    #         elif '<=' in condition:
    #             parts = condition.split('<=')
    #             if '年龄' in parts[1]:
    #                 age_min = max(age_min, int(parts[0].strip()))
    #         elif '>=' in condition:
    #             parts = condition.split('>=')
    #             if '年龄' in parts[0]:
    #                 age_min = max(age_min, int(parts[1].strip()))
    #         elif '<' in condition:
    #             parts = condition.split('<')
    #             if '年龄' in parts[0]:
    #                 age_max = min(age_max, int(parts[1].strip()) - 1)
    #             elif '年龄' in parts[1]:
    #                 age_max = min(age_max, int(parts[0].strip()) - 1)
    #         elif '>' in condition:
    #             parts = condition.split('>')
    #             if '年龄' in parts[0]:
    #                 age_min = max(age_min, int(parts[1].strip()) + 1)
    #             elif '年龄' in parts[1]:
    #                 age_min = max(age_min, int(parts[0].strip()) + 1)
    #
    #     # 如果有固定值，则返回非该值
    #     if fixed_value is not None:
    #         while True:
    #             value = random.randint(0, 120)
    #             if value != fixed_value:
    #                 return value
    #
    #     # 否则按范围外取值
    #     if age_min <= age_max:
    #         if random.random() < 0.5:
    #             if age_min > 0:
    #                 return random.randint(0, age_min - 1)
    #             else:
    #                 return random.randint(0, 120)
    #         else:
    #             if age_max < 120:
    #                 return random.randint(age_max + 1, 120)
    #             else:
    #                 return random.randint(0, 120)
    #     else:
    #         return random.randint(0, 120)

    def generate_invalid_age(self, conditions):
        """生成不符合所有年龄条件的值"""
        if not conditions:
            return round(random.uniform(0, 120), 1)

        age_min = 0
        age_max = 120
        fixed_value = None

        for condition in conditions:
            if '=' in condition:
                parts = condition.split('=')
                if '年龄' in parts[0]:
                    fixed_value = float(parts[1].strip())
            elif '<=' in condition and '＜' in condition:
                parts = condition.split('＜')
                lower_part = parts[0].split('<=')
                age_min = max(age_min, float(lower_part[0].strip()))
                age_max = min(age_max, float(parts[1].strip()))
            elif '<=' in condition:
                parts = condition.split('<=')
                if '年龄' in parts[1]:
                    age_min = max(age_min, float(parts[0].strip()))
            elif '>=' in condition:
                parts = condition.split('>=')
                if '年龄' in parts[0]:
                    age_min = max(age_min, float(parts[1].strip()))
            elif '<' in condition:
                parts = condition.split('<')
                if '年龄' in parts[0]:
                    age_max = min(age_max, float(parts[1].strip()))
                elif '年龄' in parts[1]:
                    age_max = min(age_max, float(parts[0].strip()))
            elif '>' in condition:
                parts = condition.split('>')
                if '年龄' in parts[0]:
                    age_min = max(age_min, float(parts[1].strip()))
                elif '年龄' in parts[1]:
                    age_min = max(age_min, float(parts[0].strip()))

        # 如果有固定值，则返回非该值
        if fixed_value is not None:
            while True:
                value = round(random.uniform(0, 120), 1)
                if value != fixed_value:
                    return value

        # 否则按范围外取值
        if random.random() < 0.5:
            return round(random.uniform(0, age_min - 0.1), 1)
        else:
            return round(random.uniform(age_max + 0.1, 120), 1)

    # def generate_invalid_age(self, conditions):
    #     """生成不符合所有年龄条件的值"""
    #     if not conditions:
    #         return random.randint(0, 120)
    #
    #     # 解析条件中的年龄有效范围
    #     age_min = 0
    #     age_max = 120
    #
    #     for condition in conditions:
    #         if '<=' in condition and '＜' in condition:
    #             parts = condition.split('＜')
    #             lower_part = parts[0].split('<=')
    #             age_min = max(age_min, float(lower_part[0].strip()))
    #             age_max = min(age_max, float(parts[1].strip()))
    #         elif '<=' in condition:
    #             parts = condition.split('<=')
    #             if '年龄' in parts[1]:
    #                 age_min = max(age_min, float(parts[0].strip()))
    #         elif '>=' in condition:
    #             parts = condition.split('>=')
    #             if '年龄' in parts[0]:
    #                 age_min = max(age_min, float(parts[1].strip()))
    #         elif '<' in condition:
    #             parts = condition.split('<')
    #             if '年龄' in parts[0]:
    #                 age_max = min(age_max, float(parts[1].strip()))
    #         elif '>' in condition:
    #             parts = condition.split('>')
    #             if '年龄' in parts[0]:
    #                 age_max = min(age_max, float(parts[1].strip()))
    #
    #     # 生成范围外的值
    #     if random.random() < 0.5:
    #         return round(random.uniform(0, age_min - 0.1), 1)
    #     else:
    #         return round(random.uniform(age_max + 0.1, 120), 1)

    def generate_valid_gender(self, conditions):
        """生成符合所有性别条件的值"""
        if not conditions:
            return random.choice(['男', '女'])

        # 提取性别条件中的值
        valid_genders = set()
        for condition in conditions:
            if '=' in condition:
                parts = condition.split('=')
                if '性别' in parts[0]:
                    valid_genders.add(parts[1].strip())

        if valid_genders:
            return random.choice(list(valid_genders))
        else:
            return random.choice(['男', '女'])

    def generate_invalid_gender(self, conditions):
        """生成不符合所有性别条件的值"""
        if not conditions:
            return random.choice(['男', '女'])

        # 提取性别条件中的值
        invalid_genders = {'男', '女'}
        for condition in conditions:
            if '=' in condition:
                parts = condition.split('=')
                if '性别' in parts[0]:
                    invalid_genders.discard(parts[1].strip())

        if invalid_genders:
            return random.choice(list(invalid_genders))
        else:
            return random.choice(['其他'])

# 使用示例
if __name__ == "__main__":

    po = BmiAgeSexPO()

    # 示例 1: 包含 >= 和 <=，应输出 2 个样本
    # conditions1 = ['BMI>=16.4', 'BMI<17.7', '年龄=1', '性别=男']
    conditions1 = ['年龄>=6', '年龄<6.5', 'BMI<13.4', '性别=男']
    print("Condition 1:", conditions1)
    d_cases1 = po.generate_all_cases(conditions1)
    print(d_cases1)
    for idx, sample in enumerate(d_cases1.get('satisfied', []), 1):
        print(f"✅ 第{idx}个样本: {sample}")

    # 示例 2: 只包含 > 和 <，应输出 1 个样本
    conditions2 = ['BMI>16.4', 'BMI<17.7', '年龄=1', '性别=男']
    print("\nCondition 2:")
    d_cases2 = po.generate_all_cases(conditions2)
    print(d_cases2)

    for idx, sample in enumerate(d_cases2.get('satisfied', []), 1):
        print(f"✅ 第{idx}个样本: {sample}")

    sys.exit(0)
    po = BmiAgeSexPO()
    conditions = ['年龄=1', 'BMI>16.4', 'BMI<17.7', '性别=男']

    l_3_value = []
    for cond in conditions:
        if "BMI" in cond:
            l_3_value.extend(po.splitMode(cond))
        elif "年龄" in cond:
            l_3_value.extend(po.splitMode(cond))
        else:
            l_3_value.append(cond)

    print("解析后的条件:", l_3_value)

    d_cases = po.generate_all_cases(l_3_value, num_samples=2)
    print(d_cases)

    if 'satisfied' in d_cases:
        for idx, sample in enumerate(d_cases['satisfied'], 1):
            print(f"✅ 第{idx}个样本: {sample}")
    else:
        print("❌ 未生成满足条件的样本，请检查逻辑或范围")

    # po = BmiAgeSexPO()
    # conditions = ['年龄>6', '年龄<6.5', 'BMI<13.4', '性别=男']
    #
    # l_1 = []
    # for i in conditions:
    #     if "BMI" in i:
    #         l_simple_conditions = po.splitMode(i)
    #         l_1.extend(l_simple_conditions)
    #     elif "年龄" in i:
    #         l_simple_conditions = po.splitMode(i)
    #         l_1.extend(l_simple_conditions)
    #     else:
    #         l_1.append(i)
    #
    # print("解析后的条件:", l_1)
    #
    # cases = po.generate_all_cases(l_1)
    # print(cases)
    #
    # # 查看 satisfied 是否包含符合条件的数据
    # if 'satisfied' in cases:
    #     for sample in cases['satisfied']:
    #         print("✅ 满足条件的样本:", sample)
    # else:
    #     print("❌ 未生成满足条件的数据，请检查条件范围或逻辑")


    # # 条件列表
    # # l_conditions = ['14<年龄<14.5', '22.3<=BMI', '性别=男']
    # # l_conditions = ['年龄=3', '14.3>BMI', '性别=女']
    # # l_conditions = ['年龄=5', '14.7>BMI', '性别=女']
    # l_conditions = ['年龄=5', '14.7<BMI<14.9', '性别=女']
    #
    # BmiAgeSex_PO = BmiAgeSexPO()
    # l_1 = []
    # for i in l_conditions:
    #     if "BMI" in i:
    #         l_simple_conditions = BmiAgeSex_PO.split_compound_condition(i)
    #         l_1.extend(l_simple_conditions)
    #     elif "年龄" in i:
    #         l_simple_conditions = BmiAgeSex_PO.split_compound_condition(i)
    #         l_1.extend(l_simple_conditions)
    #     else:
    #         l_1.append(i)
    # print(l_1)
    #
    #
    # try:
    #     # 生成每种情况的样本
    #     cases = BmiAgeSex_PO.generate_all_cases(l_1)
    #     print(cases)
    #
    #     # # 打印结果
    #     # for case_name, samples in cases.items():
    #     #     print(f"\n情况: {case_name}")
    #     #     for i, sample in enumerate(samples, 1):
    #     #         print(f"样本 {i}: {sample}")
    #
    # except ValueError as e:
    #     print(f"错误: {e}")
    #
    #
