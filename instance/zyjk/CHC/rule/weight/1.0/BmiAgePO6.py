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
import re
import random


class BmiAgePO():

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


    # def generate_all_cases(self, conditions):
    #     """
    #     动态生成所有可能的条件组合情况（仅支持 BMI 和 年龄）
    #     - 如果条件包含 >= 或 <=，则插入边界值 + 随机值
    #     - 否则只生成一个随机值
    #     """
    #
    #     # 解析条件
    #     parsed_conditions = {
    #         "BMI": [],
    #         "年龄": []
    #     }
    #
    #     for cond in conditions:
    #         field = None
    #         if cond.startswith("BMI"):
    #             field = "BMI"
    #         elif cond.startswith("年龄"):
    #             field = "年龄"
    #
    #         if field:
    #             parsed_conditions[field].append(cond)
    #
    #     for field in ["BMI", "年龄"]:
    #         if not parsed_conditions[field]:
    #             parsed_conditions[field] = ["always_true"]
    #
    #     cases = {}
    #     from itertools import product
    #
    #     # 四种组合情况
    #     combinations = list(product([True, False], repeat=2))
    #
    #     target_names = {
    #         (True, True): "satisfied",
    #         (False, True): "BMI不满足且年龄满足",
    #         (True, False): "BMI满足且年龄不满足",
    #         (False, False): "BMI不满足且年龄不满足"
    #     }
    #
    #     for bmi_satisfied, age_satisfied in combinations:
    #
    #         case_name = target_names[(bmi_satisfied, age_satisfied)]
    #         samples = []
    #
    #         sample_count = 2 if case_name == "satisfied" and any(
    #             '>=' in cond or '<=' in cond for cond in parsed_conditions["BMI"] + parsed_conditions["年龄"]
    #         ) else 1
    #
    #         attempts = 0
    #         while len(samples) < sample_count and attempts < 100:
    #             sample = {}
    #
    #             if bmi_satisfied:
    #                 if case_name == "satisfied" and len(samples) == 0:
    #                     boundary_bmi = self._get_min_valid_bmi(parsed_conditions["BMI"])
    #                     sample["BMI"] = round(boundary_bmi, 1)
    #                 else:
    #                     sample["BMI"] = self.generate_valid_bmi(parsed_conditions["BMI"])
    #             else:
    #                 sample["BMI"] = self.generate_invalid_bmi(parsed_conditions["BMI"])
    #
    #             if age_satisfied:
    #                 if case_name == "satisfied" and len(samples) == 0:
    #                     boundary_age = self._get_min_valid_age(parsed_conditions["年龄"])
    #                     sample["年龄"] = round(boundary_age, 1)
    #                 else:
    #                     sample["年龄"] = self.generate_valid_age(parsed_conditions["年龄"])
    #             else:
    #                 sample["年龄"] = self.generate_invalid_age(parsed_conditions["年龄"])
    #
    #             # 校验是否满足组合条件
    #             valid_bmi = self.is_match(sample["BMI"],
    #                                       parsed_conditions["BMI"]) if bmi_satisfied else not self.is_match(
    #                 sample["BMI"], parsed_conditions["BMI"])
    #             valid_age = self.is_match(sample["年龄"],
    #                                       parsed_conditions["年龄"]) if age_satisfied else not self.is_match(sample["年龄"],
    #                                                                                                        parsed_conditions[
    #                                                                                                            "年龄"])
    #
    #             if valid_bmi and valid_age:
    #                 samples.append(sample)
    #
    #             attempts += 1
    #
    #         if samples:
    #             cases[case_name] = samples
    #
    #     return cases

    def generate_all_cases(self, conditions):
        """
        动态生成所有可能的条件组合情况（仅支持 BMI 和 年龄）
        - 如果条件包含 >= 或 <=，则插入边界值 + 随机值
        - 否则只生成一个随机值
        """

        # 解析条件
        parsed_conditions = {
            "BMI": [],
            "年龄": []
        }

        for cond in conditions:
            field = None
            if cond.startswith("BMI"):
                field = "BMI"
            elif cond.startswith("年龄"):
                field = "年龄"

            if field:
                parsed_conditions[field].append(cond)

        for field in ["BMI", "年龄"]:
            if not parsed_conditions[field]:
                parsed_conditions[field] = ["always_true"]

        cases = {}
        from itertools import product

        combinations = list(product([True, False], repeat=2))

        target_names = {
            (True, True): "satisfied",
            (False, True): "BMI不满足且年龄满足",
            (True, False): "BMI满足且年龄不满足",
            (False, False): "BMI不满足且年龄不满足"
        }

        for bmi_satisfied, age_satisfied in combinations:

            case_name = target_names[(bmi_satisfied, age_satisfied)]
            samples = []

            # 判断是否为 satisfied 情况
            is_satisfied = case_name == "satisfied"

            # 自动判断样本数
            sample_count = 1
            has_gte_or_lte = any(
                '>=' in cond or '<=' in cond for cond in parsed_conditions["BMI"] + parsed_conditions["年龄"]
            )

            if is_satisfied and has_gte_or_lte:
                sample_count = 2  # 包含 >= 或 <=，生成边界值 + 随机值
            elif is_satisfied:
                sample_count = 1  # 只有一个等值匹配，只需输出一个样本

            attempts = 0
            while len(samples) < sample_count and attempts < 100:
                sample = {}

                if bmi_satisfied:
                    # 生成符合 BMI 条件的值
                    if is_satisfied and len(samples) == 0:
                        boundary_bmi = self._get_min_valid_bmi(parsed_conditions["BMI"])
                        sample["BMI"] = round(boundary_bmi, 1)
                    else:
                        sample["BMI"] = self.generate_valid_bmi(parsed_conditions["BMI"])
                else:
                    sample["BMI"] = self.generate_invalid_bmi(parsed_conditions["BMI"])

                if age_satisfied:
                    # 生成符合 年龄 条件的值
                    if is_satisfied and len(samples) == 0:
                        boundary_age = self._get_min_valid_age(parsed_conditions["年龄"])
                        sample["年龄"] = round(boundary_age, 1)
                    else:
                        sample["年龄"] = self.generate_valid_age(parsed_conditions["年龄"])
                else:
                    sample["年龄"] = self.generate_invalid_age(parsed_conditions["年龄"])

                # 校验是否满足组合条件
                valid_bmi = self.is_match(sample["BMI"],
                                          parsed_conditions["BMI"]) if bmi_satisfied else not self.is_match(
                    sample["BMI"], parsed_conditions["BMI"])
                valid_age = self.is_match(sample["年龄"],
                                          parsed_conditions["年龄"]) if age_satisfied else not self.is_match(
                    sample["年龄"], parsed_conditions["年龄"])

                if valid_bmi and valid_age:
                    samples.append(sample)

                attempts += 1

            if samples:
                cases[case_name] = samples

        return cases


    def get_case_name(self, bmi_satisfied, age_satisfied):
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

        return "且".join(parts)

    def generate_sample(self, bmi_conditions, age_conditions, satisfy_bmi, satisfy_age):
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


            # 校验是否满足组合条件
            if (
                    self.is_match(sample["BMI"], bmi_conditions if satisfy_bmi else []) and
                    self.is_match(sample["年龄"], age_conditions if satisfy_age else [])
            ):
                return sample

            attempts += 1

        raise ValueError("无法生成符合要求的样本，请检查条件是否有冲突")

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
        """
        生成不符合所有BMI条件的值，并确保数值有效
        """

        if not conditions:
            return round(random.uniform(10.0, 60.0), 1)

        bmi_min = 10.0
        bmi_max = 60.0
        fixed_value = None

        for condition in conditions:
            if '=' in condition:
                parts = condition.split('=')
                if 'BMI' in parts[0]:
                    fixed_value = float(parts[1].strip())
                elif 'BMI' in parts[1]:
                    fixed_value = float(parts[0].strip())

            elif '>' in condition:
                parts = condition.split('>')
                if 'BMI' in parts[0]:
                    # BMI > x → 不满足时要 <= x
                    bmi_max = min(bmi_max, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    # x > BMI → 不满足时要 >= x
                    bmi_min = max(bmi_min, float(parts[0].strip()))

            elif '>=' in condition:
                parts = condition.split('>=')
                if 'BMI' in parts[0]:
                    # BMI >= x → 不满足时要 < x
                    bmi_max = min(bmi_max, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    # x >= BMI → 不满足时要 > x
                    bmi_min = max(bmi_min, float(parts[0].strip()) + 0.1)

            elif '<' in condition:
                parts = condition.split('<')
                if 'BMI' in parts[0]:
                    # BMI < x → 不满足时要 >= x
                    bmi_min = max(bmi_min, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    # x < BMI → 不满足时要 <= x
                    bmi_max = min(bmi_max, float(parts[0].strip()))

            elif '<=' in condition:
                parts = condition.split('<=')
                if 'BMI' in parts[0]:
                    # BMI <= x → 不满足时要 > x
                    bmi_min = max(bmi_min, float(parts[1].strip()) + 0.1)
                elif 'BMI' in parts[1]:
                    # x <= BMI → 不满足时要 < x
                    bmi_max = min(bmi_max, float(parts[0].strip()) - 0.1)

        # 如果有固定值，则跳过该值
        if fixed_value is not None:
            while True:
                value = round(random.uniform(10.0, 60.0), 1)
                if value != fixed_value:
                    return value

        # 最终生成不满足条件的非法值
        if random.random() < 0.5:
            return round(random.uniform(10.0, bmi_min - 0.1), 1)
        else:
            return round(random.uniform(bmi_max + 0.1, 60.0), 1)
    # def _get_min_valid_bmi(self, conditions):
    #     """获取符合BMI条件的最小合法值"""
    #     bmi_min = 10.0
    #
    #     for cond in conditions:
    #         if '>=' in cond:
    #             parts = cond.split('>=')
    #             if 'BMI' in parts[0]:
    #                 val = float(parts[1].strip())
    #                 bmi_min = max(bmi_min, val)
    #         elif '>' in cond:
    #             parts = cond.split('>')
    #             if 'BMI' in parts[0]:
    #                 val = float(parts[1].strip()) + 0.1
    #                 bmi_min = max(bmi_min, val)
    #
    #     return round(bmi_min, 1)

    def _get_min_valid_bmi(self, conditions):
        """获取符合BMI条件的最小合法值"""
        bmi_min = 10.0

        for cond in conditions:
            if '>=' in cond:
                parts = cond.split('>=')
                if 'BMI' in parts[0]:
                    val = float(parts[1].strip())
                    bmi_min = max(bmi_min, val)
            elif '>' in cond:
                parts = cond.split('>')
                if 'BMI' in parts[0]:
                    val = float(parts[1].strip()) + 0.1
                    bmi_min = max(bmi_min, val)

        return round(bmi_min, 1)

    def _get_max_valid_bmi(self, conditions):
        """获取符合BMI条件的最大合法值（用于 <= 或 < 类型）"""
        max_val = 60.0  # 最大限制

        for cond in conditions:
            if '<=' in cond:
                parts = cond.split('<=')
                if 'BMI' in parts[0]:
                    val = float(parts[1].strip())
                    max_val = min(max_val, val)
            elif '<' in cond:
                parts = cond.split('<')
                if 'BMI' in parts[0]:
                    val = float(parts[1].strip())
                    max_val = min(max_val, val)

        return round(max_val, 1)


    def generate_valid_age(self, conditions):
        """生成符合所有年龄条件的值，并确保动态范围"""
        if not conditions:
            return round(random.uniform(0, 120), 1)

        age_min = 0.0
        age_max = 65.0  # 因为条件是 年龄<65

        for condition in conditions:
            if '<' in condition:
                parts = condition.split('<')
                if '年龄' in parts[0]:
                    age_max = min(age_max, float(parts[1].strip()))
                elif '年龄' in parts[1]:
                    age_min = max(age_min, float(parts[0].strip()))

        return round(random.uniform(age_min, age_max), 1)
    def generate_invalid_age(self, conditions):
        """生成不符合所有年龄条件的值，并确保年龄 >= 0"""
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
                elif '年龄' in parts[1]:
                    fixed_value = float(parts[0].strip())

            elif '<=' in condition and '＜' in condition:
                # 处理 a <= 年龄 < b 类型
                parts = condition.split('＜')
                lower_part = parts[0].split('<=')
                age_min = max(age_min, float(lower_part[1].strip()))
                age_max = min(age_max, float(parts[1].strip()))

            elif '<=' in condition:
                # 处理 年龄 <= x
                parts = condition.split('<=')
                if '年龄' in parts[1]:
                    age_min = max(age_min, float(parts[0].strip()))

            elif '>=' in condition:
                # 处理 年龄 >= x
                parts = condition.split('>=')
                if '年龄' in parts[0]:
                    age_min = max(age_min, float(parts[1].strip()))

            elif '<' in condition:
                # 处理 年龄 < x 或 x < 年龄
                parts = condition.split('<')
                if '年龄' in parts[0]:
                    age_max = min(age_max, float(parts[1].strip()))
                elif '年龄' in parts[1]:
                    age_max = min(age_max, float(parts[0].strip()))

            elif '>' in condition:
                # 处理 年龄 > x 或 x > 年龄
                parts = condition.split('>')
                if '年龄' in parts[0]:
                    age_min = max(age_min, float(parts[1].strip()) + 0.1)
                elif '年龄' in parts[1]:
                    age_min = max(age_min, float(parts[0].strip()) + 0.1)

        # 如果有固定值，则返回非该值
        if fixed_value is not None:
            while True:
                value = round(random.uniform(0, 120), 1)
                if value != fixed_value:
                    return value

        # 防止边界溢出为负数
        from math import floor, ceil

        if random.random() < 0.5:
            low_bound = max(0.0, age_min - 0.1 - 1)  # 下限不能低于0
            up_bound = max(0.0, age_min - 0.1)  # 上限也不能低于0
            if low_bound >= up_bound:
                low_bound = max(0.0, floor(up_bound - 1))
            invalid_age = round(random.uniform(low_bound, up_bound), 1)
        else:
            low_bound = max(0.0, age_max + 0.1)
            up_bound = 120
            if low_bound >= up_bound:
                low_bound = max(0.0, age_max + 0.1)
            invalid_age = round(random.uniform(low_bound, up_bound), 1)

        return invalid_age
    # def _get_min_valid_age(self, conditions):
    #     """获取符合年龄条件的最小合法值"""
    #     age_min = 0.0
    #     has_boundary = False
    #
    #     for cond in conditions:
    #         if '>=' in cond:
    #             parts = cond.split('>=')
    #             if '年龄' in parts[0]:
    #                 val = float(parts[1].strip())
    #                 age_min = max(age_min, val)
    #                 has_boundary = True
    #         elif '>' in cond:
    #             parts = cond.split('>')
    #             if '年龄' in parts[0]:
    #                 val = float(parts[1].strip()) + 0.1
    #                 age_min = max(age_min, val)
    #                 has_boundary = True
    #
    #     # 如果没有 >= 或 > 条件，则随机生成一个合理起始值
    #     if not has_boundary:
    #         age_min = random.uniform(0.0, 65.0)
    #
    #     return round(age_min, 1)

    def _get_min_valid_age(self, conditions):
        """获取符合年龄条件的最小合法值"""
        age_min = 0.0

        for cond in conditions:
            if '>=' in cond:
                parts = cond.split('>=')
                if '年龄' in parts[0]:
                    val = float(parts[1].strip())
                    age_min = max(age_min, val)
            elif '>' in cond:
                parts = cond.split('>')
                if '年龄' in parts[0]:
                    val = float(parts[1].strip()) + 0.1
                    age_min = max(age_min, val)

        return round(age_min, 1)


# 使用示例
if __name__ == "__main__":

    po = BmiAgePO()

    # 示例 1: 包含 >= 和 <=，应输出 2 个样>
    # conditions1 = ['BMI<26', '年龄<65']
    # conditions1 = ['BMI>=24', 'BMI<26','年龄<65']
    # conditions1 = ['BMI>=27' ,'年龄>=65']
    # conditions1 =  ['BMI<24', 'BMI>=18.5', '年龄>=18', '年龄<65']
    # conditions1 = ['BMI>=11', 'BMI<16.5', '年龄>=13.4', '年龄<15']
    # conditions1 = ['BMI>16.4', 'BMI<=17.7', '年龄>1']

    BMI >= 24 and 年龄 >= 18 and 年龄 < 65
    BMI < 24 and BMI >= 18.5 and 年龄 >= 18 and 年龄 < 65
    BMI < 18.5 and 年龄 >= 18 and 年龄 < 65
    BMI >= 27 and 年龄 >= 65
    BMI < 27 and BMI >= 20 and 年龄 >= 65
    BMI < 20 and 年龄 >= 65

    print("Condition 1:", conditions1)
    d_cases1 = po.generate_all_cases(conditions1)
    print(d_cases1)
    for idx, sample in enumerate(d_cases1.get('satisfied', []), 1):
        print(f"✅ 第{idx}个样本: {sample}")

    print("\n测试条件: ['BMI>=24','年龄<65','年龄>=18']")
    print(po.generate_all_cases(['BMI>=27', '年龄>=65']))



    print("\n测试条件: ['BMI<20','年龄<=65']")
    print(po.generate_all_cases(['BMI<20', '年龄<=65']))

    print("\n测试条件: ['BMI>=24','年龄>=18','年龄<65']")
    print(po.generate_all_cases(['BMI>=24', '年龄>=18', '年龄<65']))

    print("\n测试条件: ['BMI<18.5','年龄>18','年龄<=65']")
    print(po.generate_all_cases(['BMI<18.5', '年龄>18', '年龄<=65']))

    print("\n测试条件: ['BMI<27','BMI>18','年龄<=65']")
    print(po.generate_all_cases(['BMI<27', 'BMI>18', '年龄<=65']))

    print("\n测试条件: ['BMI<27','BMI>18','年龄<=65']")
    print(po.generate_all_cases(['BMI<=27', 'BMI>18', '年龄>=65']))

    print("\n测试条件: ['BMI<24','BMI>18.5','年龄>=18','年龄<65']")
    print(po.generate_all_cases(['BMI<24', 'BMI>18.5', '年龄>=18', '年龄<65']))



    # # 示例 2: 只包含 > 和 <，应输出 1 个样本
    # conditions2 = ['BMI>16.4', 'BMI<17.7', '年龄=1', '性别=男']
    # print("\nCondition 2:")
    # d_cases2 = po.generate_all_cases(conditions2)
    # print(d_cases2)
    #
    # for idx, sample in enumerate(d_cases2.get('satisfied', []), 1):
    #     print(f"✅ 第{idx}个样本: {sample}")
