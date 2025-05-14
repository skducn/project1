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


class BmiPO():


    def splitMode(self, condition):
        """
        拆分
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
        将形如 '18.5>BMI' 转换为 'BMI<18.5'
        :param condition: 条件字符串
        :return: 拆分或转换后的条件列表
        """
        cond = condition.strip().replace(" ", "")

        # 匹配类似 18.5>BMI 或 24<BMI 这样的逆序写法
        match = re.match(r'^(\d+(?:\.\d+)?)(>|>=|<|<=)(BMI)$', cond)

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

    # def split_compound_condition(self, condition):
    #     """
    #     将形如 '6<=年龄<6.5' 或 '14.7<BMI<18.8' 的复合条件拆分为两个标准条件
    #     :param condition: 条件字符串
    #     :return: 拆分后的简单条件列表
    #     """
    #
    #     cond = condition.strip().replace(" ", "")
    #
    #     # 匹配形如：6<=年龄<6.5 或 14.7<BMI<18.8
    #     match = re.match(r'^(\d+(?:\.\d+)?)(<=|<|>=|>)(年龄|BMI)(<=|<|>=|>)(\d+(?:\.\d+)?)$', cond)
    #
    #     if not match:
    #         return [condition]  # 不符合格式，返回原始条件
    #
    #     left_val, op1, field, op2, right_val = match.groups()
    #
    #     # 判断是否是合法组合（如：a < x < b）
    #     if (op1 in ('<', '<=') and op2 in ('<', '<=')) or (op1 in ('>', '>=') and op2 in ('>', '><')):
    #         # 如果是 a < x < b 类型，转换成 x > a 且 x < b
    #         cond1 = f"{field}{op1}{left_val}"
    #         cond2 = f"{field}{op2}{right_val}"
    #
    #         # 修复方向错误：例如 6<=年龄<6.5 → 年龄>=6 and 年龄<6.5
    #         if op1 == '<=' and op2 == '<':
    #             cond1 = f"{field}>={left_val}"
    #         elif op1 == '<' and op2 == '<=':
    #             cond1 = f"{field}>{left_val}"
    #             cond2 = f"{field}<={right_val}"
    #         elif op1 == '<' and op2 == '<':
    #             cond1 = f"{field}>{left_val}"
    #         elif op1 == '<=' and op2 == '<=':
    #             cond1 = f"{field}>={left_val}"
    #             cond2 = f"{field}<={right_val}"
    #
    #         return [cond1, cond2]
    #
    #     else:
    #         return [condition]


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
    #     # age_conditions = [c for c in conditions if '年龄' in c]
    #     # gender_conditions = [c for c in conditions if '性别' in c]
    #
    #     # 生成所有可能的条件组合
    #     cases = {}
    #
    #     # 生成所有8种可能的组合 (2^3 = 8)
    #     for bmi_satisfied in [True, False]:
    #
    #         case_name = self.get_case_name(bmi_satisfied)
    #         # print(case_name)
    #         if case_name == 'BMI满足且年龄满足且性别满足':
    #             case_name = 'satisfied'
    #         cases[case_name] = [
    #             self.generate_sample(bmi_conditions,
    #                             bmi_satisfied)
    #             for _ in range(num_samples)
    #         ]
    #     print(1212, cases)
    #     return cases

    def get_case_name(self, bmi_satisfied):
        """生成条件组合的名称"""
        parts = []
        if bmi_satisfied:
            parts.append("BMI满足")
        else:
            parts.append("BMI不满足")

        return "且".join(parts)


    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有4种可能的条件组合情况
    #
    #     参数:
    #     conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65']
    #     num_samples (int): 每种情况生成的样本数量
    #
    #     返回:
    #     dict: 包含4种情况的样本字典
    #     """
    #     # 分离BMI和年龄条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #     # bmi_conditions = [c for c in conditions if 'BMI' in c]
    #
    #
    #     # print("1212bmi_conditions", bmi_conditions)
    #     # bmi_conditions.append('24.0>BMI')
    #     # print(bmi_conditions)
    #     # # 然后在主流程中加入验证逻辑：
    #     # sample = self.generate_sample(bmi_conditions, age_conditions, False, True)
    #     # is_valid = self.is_bmi_satisfied(sample['BMI'], bmi_conditions)
    #     # print(f"生成的 BMI={sample['BMI']} 是否满足条件？{is_valid}")
    #
    #     # 生成每种情况的样本
    #     return {
    #         "satisfied": [self.generate_sample(bmi_conditions , True) for _ in range(num_samples)],
    #         "not1": [self.generate_sample(bmi_conditions, False) for _ in range(num_samples)]
    #     }

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     生成所有可能的条件组合情况
    #     参数:
    #     conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65']
    #     num_samples (int): 每种情况生成的样本数量
    #     返回:
    #     dict: 包含两种情况的样本字典
    #     """
    #     # 分离BMI条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #
    #     # 生成样本
    #     samples = {
    #         "satisfied": [self.generate_sample(bmi_conditions, True) for _ in range(num_samples)],
    #         "not1": [self.generate_sample(bmi_conditions, False) for _ in range(num_samples)]
    #     }
    #
    #     # 强制添加一个精确的边界值：BMI=18.5
    #     # 只有当条件包含 BMI>=18.5 时才添加
    #     if any("BMI>=" in cond and float(re.search(r'\d+', cond).group()) <= 18.5 for cond in bmi_conditions):
    #         samples["satisfied"].append({'BMI': 18.5})
    #
    #     return samples

    # def generate_all_cases(self, conditions, num_samples=1):
    #     """
    #     根据条件动态生成 satisfied 样本
    #     - >= 或 <=: 生成 2 个样本（包含边界值）
    #     - > 或 <: 生成 1 个样本
    #     """
    #
    #     # 提取 BMI 相关条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #
    #     satisfied_samples = []
    #     not1_samples = []
    #
    #     for cond in bmi_conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         operator, value_str = match.groups()
    #         value = float(value_str)
    #
    #         # 判断操作符类型
    #         if operator == '>=' or operator == '<=':
    #             # 对于 >= 或 <=，生成两个样本：边界值 + 随机值
    #             satisfied_samples.append({'BMI': value})
    #             satisfied_samples.append({'BMI': self._generate_valid_bmi(conditions)})
    #         elif operator == '>' or operator == '<':
    #             # 对于 > 或 <，只生成一个随机值
    #             satisfied_samples.append({'BMI': self._generate_valid_bmi(conditions)})
    #         else:
    #             not1_samples.append({'BMI': self._generate_invalid_bmi(conditions)})
    #
    #     return {
    #         "satisfied": satisfied_samples,
    #         "not1": not1_samples
    #     }

    # def generate_all_cases(self, conditions):
    #     """
    #     根据条件动态生成 satisfied 和 not1 的样本数据
    #     - 对于 >= 或 <=: 返回两个样本（边界值 + 随机值）
    #     - 对于 > 或 <: 返回一个样本（随机值）
    #     """
    #
    #     # 提取 BMI 相关条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #     satisfied_samples = []
    #     not1_samples = []
    #
    #     for cond in bmi_conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         op, val_str = match.groups()
    #         val = float(val_str)
    #
    #         # 判断操作符类型
    #         if op == '>=' or op == '<=':
    #             # 添加边界值 + 一个合法随机值
    #             satisfied_samples.append({'BMI': val})
    #             satisfied_samples.append({'BMI': self._generate_valid_bmi(bmi_conditions)})
    #         elif op == '>' or op == '<':
    #             # 只添加一个合法随机值
    #             satisfied_samples.append({'BMI': self._generate_valid_bmi(bmi_conditions)})
    #         else:
    #             # 不符合预期的操作符，跳过
    #             continue
    #
    #     # 去重并截取前两个
    #     unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())
    #     satisfied_samples = unique_satisfied[:2]
    #
    #     # 生成 not1（不满足条件的样本）
    #     if len(satisfied_samples) < 2:
    #         not1_samples.append({'BMI': self._generate_invalid_bmi(bmi_conditions)})
    #     else:
    #         # 如果已满足，可生成一个不满足任意条件的样本
    #         not1_samples.append({'BMI': self._generate_invalid_bmi(bmi_conditions)})
    #
    #     return {
    #         "satisfied": satisfied_samples,
    #         "not1": not1_samples
    #     }

    # def generate_all_cases(self, conditions):
    #     """
    #     根据条件动态生成 satisfied 和 not1 的样本数据
    #     - >= / <=: 返回两个样本（包含边界值）
    #     - > / <: 返回一个随机样本
    #     - not1 始终返回一个非法样本
    #     """
    #
    #     # 提取 BMI 相关条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #     satisfied_samples = []
    #     not1_samples = []
    #
    #     for cond in bmi_conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         op, val_str = match.groups()
    #         val = float(val_str)
    #
    #         # 判断操作符类型
    #         if op == '>=' or op == '<=':
    #             satisfied_samples.append({'BMI': val})  # 边界值
    #             satisfied_samples.append({'BMI': self._generate_valid_bmi(bmi_conditions)})  # 随机值
    #         elif op == '>' or op == '<':
    #             satisfied_samples.append({'BMI': self._generate_valid_bmi(bmi_conditions)})
    #
    #     # 去重并保留最多 2 个满足条件的样本
    #     unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())
    #
    #     # 如果是 > 和 < 组合，则只保留 1 个样本
    #     if all(re.search(r'(>|<)', c) for c in bmi_conditions):
    #         unique_satisfied = unique_satisfied[:1]
    #     else:
    #         unique_satisfied = unique_satisfied[:2]
    #
    #     # 生成不满足条件的样本
    #     not1_sample = self._generate_invalid_bmi(bmi_conditions)
    #     not1_samples.append(not1_sample)
    #
    #     return {
    #         "satisfied": unique_satisfied,
    #         "not1": not1_samples
    #     }

    # def generate_all_cases(self, conditions):
    #     """
    #     根据条件动态生成 satisfied 和 not1 的样本数据
    #     - >= / <=: 返回两个样本（包含边界值）
    #     - > / <: 返回一个样本（随机值）
    #     - not1 始终返回一个非法样本
    #     """
    #
    #     # 提取所有 BMI 条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #
    #     satisfied_samples = []
    #     not1_samples = []
    #
    #     # 遍历每个条件
    #     for cond in bmi_conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         op, val_str = match.groups()
    #         val = float(val_str)
    #
    #         # 判断操作符类型
    #         if op == '>=' or op == '<=':
    #             satisfied_samples.append({'BMI': val})  # 边界值
    #             satisfied_samples.append({'BMI': self._generate_valid_bmi(bmi_conditions)})  # 合法随机值
    #         elif op == '>' or op == '<':
    #             satisfied_samples.append({'BMI': self._generate_valid_bmi(bmi_conditions)})
    #
    #     # 去重 satisfied 并限制为最多 2 个样本
    #     unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())
    #
    #     # 如果是 > 和 < 组合，则只保留一个合法样本
    #     if all(re.search(r'(>|<)', c) for c in bmi_conditions):
    #         unique_satisfied = unique_satisfied[:1]
    #     else:
    #         unique_satisfied = unique_satisfied[:2]
    #
    #     # 生成不满足条件的样本
    #     not1_value = self._generate_invalid_bmi(bmi_conditions)
    #     not1_samples.append(not1_value)
    #
    #     return {
    #         "satisfied": unique_satisfied,
    #         "not1": not1_samples
    #     }

    # def generate_all_cases(self, conditions):
    #     """
    #     根据条件动态生成 satisfied 和 not1 的样本数据
    #     - >= / <=: 返回两个样本（包含边界值）
    #     - > / <: 返回一个随机样本
    #     - not1 始终返回一个非法样本
    #     """
    #
    #     # 提取所有 BMI 条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #
    #     satisfied_samples = []
    #     not1_samples = []
    #
    #     # 存储边界值和合法范围内的随机值
    #     lower_bounds = []
    #     upper_bounds = []
    #
    #     # 遍历每个条件，提取边界或生成随机值
    #     for cond in bmi_conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         op, val_str = match.groups()
    #         val = float(val_str)
    #
    #         # 收集合法范围
    #         if op == '>=':
    #             lower_bounds.append(val)
    #         elif op == '<=':
    #             upper_bounds.append(val)
    #         elif op == '>':
    #             lower_bounds.append(val + 0.1)
    #         elif op == '<':
    #             upper_bounds.append(val - 0.1)
    #
    #         # 添加满足条件的样本
    #         if op in ['>=', '<=']:
    #             satisfied_samples.append({'BMI': val})  # 边界值
    #
    #     # 计算合法区间
    #     bmi_min = max(lower_bounds) if lower_bounds else 10.0
    #     bmi_max = min(upper_bounds) if upper_bounds else 60.0
    #
    #     # 如果有多个边界值，再补充一个合法随机值
    #     if len(lower_bounds) > 0 and len(upper_bounds) > 0:
    #         random_value = round(random.uniform(bmi_min, bmi_max), 1)
    #         satisfied_samples.append({'BMI': random_value})
    #     elif len(lower_bounds) > 0:
    #         satisfied_samples.append({'BMI': round(random.uniform(bmi_min, 60.0), 1)})
    #     elif len(upper_bounds) > 0:
    #         satisfied_samples.append({'BMI': round(random.uniform(10.0, bmi_max), 1)})
    #     else:
    #         satisfied_samples.append({'BMI': round(random.uniform(bmi_min, bmi_max), 1)})
    #
    #     # 去重并限制为最多两个 satisfied 样本
    #     unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())
    #
    #     # 如果全是 > < 类型，则只保留一个样本
    #     if all(re.search(r'(>|<)', c) for c in bmi_conditions):
    #         unique_satisfied = unique_satisfied[:1]
    #     else:
    #         unique_satisfied = unique_satisfied[:2]
    #
    #     # 生成不满足条件的样本
    #     not1_value = self._generate_invalid_bmi(bmi_conditions)
    #     not1_samples.append(not1_value)
    #
    #     return {
    #         "satisfied": unique_satisfied,
    #         "not1": not1_samples
    #     }

    # def generate_all_cases(self, conditions):
    #     """
    #     根据条件动态生成 satisfied 和 not1 的样本数据
    #     - >= / <=: 返回两个样本（包含边界值）
    #     - > / <: 返回一个样本（随机值）
    #     - not1 始终返回一个非法样本
    #     """
    #
    #     # 提取所有 BMI 条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #
    #     satisfied_samples = []
    #     not1_samples = []
    #
    #     # 存储边界值和操作符类型
    #     lower_bounds = []
    #     upper_bounds = []
    #     boundary_values = []
    #
    #     # 第一遍：提取边界值
    #     for cond in bmi_conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         op, val_str = match.groups()
    #         val = float(val_str)
    #
    #         if op == '>=':
    #             lower_bounds.append(val)
    #             boundary_values.append({'BMI': val})
    #         elif op == '<=':
    #             upper_bounds.append(val)
    #             boundary_values.append({'BMI': val})
    #         elif op == '>':
    #             lower_bounds.append(val + 0.1)
    #         elif op == '<':
    #             upper_bounds.append(val - 0.1)
    #
    #     # 计算合法区间
    #     bmi_min = max(lower_bounds) if lower_bounds else 10.0
    #     bmi_max = min(upper_bounds) if upper_bounds else 60.0
    #
    #     # 第二遍：生成一个合法随机值
    #     valid_bmi = round(random.uniform(bmi_min, bmi_max), 1)
    #     satisfied_samples.extend(boundary_values)
    #     satisfied_samples.append({'BMI': valid_bmi})
    #
    #     # 去重并限制为最多两个样本
    #     unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())
    #
    #     # 如果全是 > < 类型，则只保留一个样本
    #     if all(re.search(r'(>|<)', c) for c in bmi_conditions):
    #         unique_satisfied = unique_satisfied[:1]
    #     else:
    #         unique_satisfied = unique_satisfied[:2]
    #
    #     # 生成不满足条件的样本
    #     not1_value = self._generate_invalid_bmi(bmi_conditions)
    #     not1_samples.append(not1_value)
    #
    #     return {
    #         "satisfied": unique_satisfied,
    #         "not1": not1_samples
    #     }

    # def generate_all_cases(self, conditions):
    #     """
    #     根据条件动态生成 satisfied 和 not1 的样本数据
    #     - >= / <=: 返回两个样本（包含边界值）
    #     - > / <: 返回一个样本（随机值）
    #     - not1 始终返回一个非法样本
    #     """
    #
    #     # 提取所有 BMI 条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #
    #     satisfied_samples = []
    #     not1_samples = []
    #
    #     # 收集上下限
    #     lower_bounds = []
    #     upper_bounds = []
    #     boundary_values = []
    #
    #     # 第一遍：提取操作符类型和边界值
    #     for cond in bmi_conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         op, val_str = match.groups()
    #         val = float(val_str)
    #
    #         if op == '>=':
    #             lower_bounds.append(val)
    #             boundary_values.append({'BMI': val})
    #         elif op == '<=':
    #             upper_bounds.append(val)
    #             boundary_values.append({'BMI': val})
    #         elif op == '>':
    #             lower_bounds.append(val + 0.1)
    #         elif op == '<':
    #             upper_bounds.append(val - 0.1)
    #
    #     # 计算合法区间
    #     bmi_min = max(lower_bounds) if lower_bounds else 10.0
    #     bmi_max = min(upper_bounds) if upper_bounds else 60.0
    #
    #     # 第二遍：生成满足条件的样本
    #     satisfied_samples.extend(boundary_values)  # 添加所有边界值
    #     satisfied_samples.append({'BMI': round(random.uniform(bmi_min, bmi_max), 1)})  # 添加一个合法随机值
    #
    #     # 去重并限制为最多两个样本
    #     unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())
    #
    #     # 如果全是 > < 类型，则只保留一个样本
    #     if all(re.search(r'(>|<)', c) for c in bmi_conditions):
    #         unique_satisfied = unique_satisfied[:1]
    #     else:
    #         unique_satisfied = unique_satisfied[:2]
    #
    #     # 生成不满足条件的样本
    #     not1_sample = self._generate_invalid_bmi(bmi_conditions)
    #     not1_samples.append(not1_sample)
    #
    #     return {
    #         "satisfied": unique_satisfied,
    #         "not1": not1_samples
    #     }

    # def generate_all_cases(self, conditions):
    #     """
    #     根据条件动态生成 satisfied 和 not1 的样本数据
    #     - >= / <=: 返回两个样本（包含边界值）
    #     - > / <: 返回一个样本（随机值）
    #     - not1 始终返回一个非法样本
    #     """
    #
    #     # 提取所有 BMI 条件
    #     bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    #
    #     satisfied_samples = []
    #     not1_samples = []
    #
    #     # 存储上下限和边界值
    #     lower_bounds = []
    #     upper_bounds = []
    #     boundary_values = set()  # 使用集合避免重复边界值
    #
    #     # 第一遍：提取操作符类型和边界值
    #     for cond in bmi_conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         op, val_str = match.groups()
    #         val = float(val_str)
    #
    #         if op == '>=':
    #             lower_bounds.append(val)
    #             boundary_values.add(val)
    #         elif op == '<=':
    #             upper_bounds.append(val)
    #             boundary_values.add(val)
    #         elif op == '>':
    #             lower_bounds.append(val + 0.1)
    #         elif op == '<':
    #             upper_bounds.append(val - 0.1)
    #
    #     # 计算合法区间
    #     bmi_min = max(lower_bounds) if lower_bounds else 10.0
    #     bmi_max = min(upper_bounds) if upper_bounds else 60.0
    #
    #     # 如果没有上限或下限，用默认范围
    #     if not upper_bounds:
    #         bmi_max = 60.0
    #     if not lower_bounds:
    #         bmi_min = 10.0
    #
    #     # 第二遍：添加边界值和随机值
    #     satisfied_samples.extend({'BMI': v} for v in sorted(boundary_values))
    #
    #     # 如果只有一个边界值，则再加一个随机值
    #     if len(boundary_values) < 2 and (bmi_min < bmi_max):
    #         random_value = round(random.uniform(bmi_min, bmi_max), 1)
    #         satisfied_samples.append({'BMI': random_value})
    #
    #     # 再次检查是否满足至少两个样本
    #     if len(satisfied_samples) < 2 and (bmi_min < bmi_max):
    #         while len(satisfied_samples) < 2:
    #             extra_value = round(random.uniform(bmi_min, bmi_max), 1)
    #             if not any(item['BMI'] == extra_value for item in satisfied_samples):
    #                 satisfied_samples.append({'BMI': extra_value})
    #
    #     # 去重并限制为最多两个样本
    #     unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())
    #     if all(re.search(r'(>|<)', c) for c in bmi_conditions):
    #         unique_satisfied = unique_satisfied[:1]
    #     else:
    #         unique_satisfied = unique_satisfied[:2]
    #
    #     # 生成不满足条件的样本
    #     not1_sample = self._generate_invalid_bmi(bmi_conditions)
    #     not1_samples.append(not1_sample)
    #
    #     return {
    #         "satisfied": unique_satisfied,
    #         "not1": not1_samples
    #     }

    def generate_all_cases(self, conditions):
        """
        根据条件动态生成 satisfied 和 not1 的样本数据
        - >= / <=: 返回两个样本（包含边界值）
        - > / <: 返回一个样本（随机值）
        - not1 始终返回一个非法样本
        """

        # 提取所有 BMI 条件
        bmi_conditions = [c for c in conditions if c.startswith('BMI')]

        satisfied_samples = []
        not1_samples = []

        # 存储上下限和边界值
        lower_bounds = []
        upper_bounds = []
        boundary_values = set()  # 使用集合避免重复边界值

        # 第一遍：提取操作符类型和边界值
        for cond in bmi_conditions:
            match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
            if not match:
                continue

            op, val_str = match.groups()
            val = float(val_str)

            if op == '>=':
                lower_bounds.append(val)
                boundary_values.add(val)
            elif op == '<=':
                upper_bounds.append(val)
                boundary_values.add(val)
            elif op == '>':
                lower_bounds.append(val + 0.1)
            elif op == '<':
                upper_bounds.append(val - 0.1)

        # 计算合法区间
        bmi_min = max(lower_bounds) if lower_bounds else 10.0
        bmi_max = min(upper_bounds) if upper_bounds else 60.0

        # 如果没有有效范围，设置默认值
        if not lower_bounds:
            bmi_min = 10.0
        if not upper_bounds:
            bmi_max = 60.0

        # 第二遍：生成满足条件的样本
        # 添加边界值
        satisfied_samples.extend({'BMI': v} for v in sorted(boundary_values))

        # 如果不足两个样本，则补充区间内的随机值
        while len(satisfied_samples) < 2:
            value = round(random.uniform(bmi_min, bmi_max), 1)
            if not any(item['BMI'] == value for item in satisfied_samples):  # 避免重复
                satisfied_samples.append({'BMI': value})

        # 去重并限制为最多两个样本
        unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())[:2]

        # 生成不满足条件的样本
        not1_sample = self._generate_invalid_bmi(bmi_conditions)
        not1_samples.append(not1_sample)

        return {
            "satisfied": unique_satisfied,
            "not1": not1_samples
        }

    def generate_sample(self, bmi_conditions, satisfy_bmi):
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

        # 返回字典格式
        return {'BMI': bmi}


    def generate_valid_bmi(self, conditions):
        """生成符合所有BMI条件的值"""
        bmi_min = 10.0
        bmi_max = 60.0
        # print(33, conditions)
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
        # print(44,round(random.uniform(bmi_min, bmi_max), 1))
        return round(random.uniform(bmi_min, bmi_max), 1)

    def _generate_valid_bmi(self, conditions):
        """根据所有条件计算合法 BMI 值"""
        bmi_min = 10.0
        bmi_max = 60.0

        for cond in conditions:
            match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
            if not match:
                continue
            op, value_str = match.groups()
            value = float(value_str)

            if op == '>':
                bmi_min = max(bmi_min, value + 0.1)
            elif op == '>=':
                bmi_min = max(bmi_min, value)
            elif op == '<':
                bmi_max = min(bmi_max, value - 0.1)
            elif op == '<=':
                bmi_max = min(bmi_max, value)

        return round(random.uniform(bmi_min, bmi_max), 1)

    def _generate_invalid_bmi(self, conditions):
        """
        生成一个不满足所有 BMI 条件的值
        :param conditions: 条件列表，例如 ['BMI<18.5']
        :return: {'BMI': value}
        """

        # 提取并解析所有有效条件
        valid_ranges = []

        for cond in conditions:
            match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
            if not match:
                continue

            op, value_str = match.groups()
            value = float(value_str)

            if op == '>':
                valid_ranges.append((value + 0.1, 60.0))
            elif op == '>=':
                valid_ranges.append((value, 60.0))
            elif op == '<':
                valid_ranges.append((0.0, value - 0.1))
            elif op == '<=':
                valid_ranges.append((0.0, value))

        # 计算合法区间
        satisfied_min = max(r[0] for r in valid_ranges) if valid_ranges else 0.0
        satisfied_max = min(r[1] for r in valid_ranges) if valid_ranges else 60.0

        # 在合法区间外生成一个无效值
        if satisfied_min <= satisfied_max:
            if random.random() < 0.5:
                invalid_value = round(random.uniform(0.0, satisfied_min - 0.1), 1)
            else:
                invalid_value = round(random.uniform(satisfied_max + 0.1, 60.0), 1)
        else:
            # 如果无合法区间（即条件冲突），随机生成一个值即可
            invalid_value = round(random.uniform(10.0, 60.0), 1)

        return {'BMI': invalid_value}


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
                if bmi_min > 10.0:
                    return round(random.uniform(10.0, bmi_min - 0.1), 1)
                else:
                    return round(random.uniform(bmi_max + 0.1, 60.0), 1)
            else:
                # 选择上界区间
                if bmi_max < 60.0:
                    return round(random.uniform(bmi_max + 0.1, 60.0), 1)
                else:
                    return round(random.uniform(10.0, bmi_min - 0.1), 1)
        else:
            # 条件矛盾，所有值都不符合条件
            return round(random.uniform(10.0, 60.0), 1)

    # def _generate_invalid_bmi(self, conditions):
    #     """生成不满足条件的 BMI 值"""
    #     valid_bmi_min = 10.0
    #     valid_bmi_max = 60.0
    #
    #     for cond in conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #         op, value_str = match.groups()
    #         value = float(value_str)
    #
    #         if op == '>':
    #             valid_bmi_min = max(valid_bmi_min, value + 0.1)
    #         elif op == '>=':
    #             valid_bmi_min = max(valid_bmi_min, value)
    #         elif op == '<':
    #             valid_bmi_max = min(valid_bmi_max, value - 0.1)
    #         elif op == '<=':
    #             valid_bmi_max = min(valid_bmi_max, value)
    #
    #     # 在有效范围外生成不满足条件的样本
    #     if random.random() < 0.5:
    #         invalid_value = round(random.uniform(10.0, valid_bmi_min - 0.1), 1)
    #     else:
    #         invalid_value = round(random.uniform(valid_bmi_max + 0.1, 60.0), 1)
    #
    #     return {'BMI': invalid_value}
    #



# 使用示例
if __name__ == "__main__":

    bmi_po = BmiPO()

    # 示例1：使用 >= 和 <
    # cases1 = bmi_po.generate_all_cases(['BMI>=18.5', 'BMI<24.0'])
    cases1 = bmi_po.generate_all_cases(['BMI＜18.5'])
    print(cases1)

    # # 示例2：使用 > 和 <
    # cases2 = bmi_po.generate_all_cases(['BMI>18.5', 'BMI<24.0'])
    # print("示例2:", cases2)

