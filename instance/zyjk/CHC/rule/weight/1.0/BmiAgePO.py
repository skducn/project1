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


class BmiAgePO():

    def is_bmi_satisfied(self, bmi, conditions):
        """检查给定的 BMI 是否满足所有条件"""
        for condition in conditions:
            match = re.match(r'BMI([<>=]+)(\d+)', condition)
            if not match:
                continue
            operator, value = match.groups()
            value = float(value)
            if operator == '>' and not (bmi > value):
                return False
            elif operator == '>=' and not (bmi >= value):
                return False
            elif operator == '<' and not (bmi < value):
                return False
            elif operator == '<=' and not (bmi <= value):
                return False
        return True

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
        # print("bmi_conditions", bmi_conditions)
        age_conditions = [c for c in conditions if c.startswith('年龄')]

        # # 然后在主流程中加入验证逻辑：
        # sample = self.generate_sample(bmi_conditions, age_conditions, False, True)
        # is_valid = self.is_bmi_satisfied(sample['BMI'], bmi_conditions)
        # print(f"生成的 BMI={sample['BMI']} 是否满足条件？{is_valid}")

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



        # if bmi_min <= bmi_max:
        #     # 有效范围外有两个区间：[10.0, bmi_min) 和 (bmi_max, 60.0]
        #     if random.random() < 0.5:
        #         # 选择下界区间
        #         return round(random.uniform(10.0, bmi_min - 0.1), 1)
        #     else:
        #         # 选择上界区间
        #         return round(random.uniform(bmi_max + 0.1, 60.0), 1)
        # else:
        #     # 条件矛盾，所有值都不符合条件
        #     return round(random.uniform(10.0, 60.0), 1)

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
    conditions =['BMI>=24', '年龄>=18', '年龄<65']
    BmiAge_PO = BmiAgePO()

    try:
        # 生成每种情况的样本
        cases = BmiAge_PO.generate_all_cases(conditions)
        print(cases)

        # # 打印结果
        # for case_name, samples in cases.items():
        #     print(f"\n情况: {case_name}")
        #     for i, sample in enumerate(samples, 1):
        #         print(f"样本 {i}: {sample}")

    except ValueError as e:
        print(f"错误: {e}")


