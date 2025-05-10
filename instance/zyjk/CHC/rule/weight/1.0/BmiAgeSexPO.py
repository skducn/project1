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


    def split_compound_condition(self, condition):
        """
        将类似 '14.7<BMI<18.8' 的复合条件拆分成两个简单条件
        :param condition: 复合条件字符串
        :return: 包含两个简单条件的列表
        """
        # 检查条件中是否包含 '<' 两次
        if condition.count('<') == 2 and condition.count('=') == 0:
            parts = condition.split('<')
            # 构建两个简单条件
            condition1 = f"{parts[0]}<{parts[1]}"
            condition2 = f"{parts[1]}<{parts[2]}"
            return [condition1, condition2]
        elif condition.count('>') == 2 and condition.count('=') == 0:
            parts = condition.split('>')
            # 构建两个简单条件
            condition1 = f"{parts[0]}>{parts[1]}"
            condition2 = f"{parts[1]}>{parts[2]}"
            return [condition1, condition2]
        elif condition.count('>=') == 2:
            parts = condition.split('>=')
            # 构建两个简单条件
            condition1 = f"{parts[0]}>={parts[1]}"
            condition2 = f"{parts[1]}>={parts[2]}"
            return [condition1, condition2]
        return [condition]

    def normalize_condition(self, condition):
        """将全角符号替换为半角符号"""
        return condition.replace('＞', '>').replace('＜', '<').replace('＝', '=').replace(" ", "")

    # condition = self.normalize_condition(condition)

    @staticmethod
    def normalize_condition(condition):
        return condition.replace('＞', '>').replace('＜', '<').replace('＝', '=').replace(" ", "")

    def generate_all_cases(self, conditions, num_samples=1):
        """
        生成所有可能的条件组合情况

        参数:
        conditions (list): 条件列表，例如 ['14<= 年龄＜14.5', '22.3<= BMI', '性别=男']
        num_samples (int): 每种情况生成的样本数量

        返回:
        dict: 包含所有情况的样本字典
        """
        # 分离BMI、年龄和性别条件
        bmi_conditions = [c for c in conditions if 'BMI' in c]
        age_conditions = [c for c in conditions if '年龄' in c]
        gender_conditions = [c for c in conditions if '性别' in c]

        # 生成所有可能的条件组合
        cases = {}

        # 生成所有8种可能的组合 (2^3 = 8)
        for bmi_satisfied in [True, False]:
            for age_satisfied in [True, False]:
                for gender_satisfied in [True, False]:
                    case_name = self.get_case_name(bmi_satisfied, age_satisfied, gender_satisfied)
                    # print(case_name)
                    if case_name == 'BMI满足且年龄满足且性别满足':
                        case_name = 'satisfied'
                    cases[case_name] = [
                        self.generate_sample(bmi_conditions, age_conditions, gender_conditions,
                                        bmi_satisfied, age_satisfied, gender_satisfied)
                        for _ in range(num_samples)
                    ]

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

    def generate_sample(self, bmi_conditions, age_conditions, gender_conditions,
                        satisfy_bmi, satisfy_age, satisfy_gender):
        """
        生成一个符合指定条件组合的样本

        参数:
        bmi_conditions (list): BMI相关条件
        age_conditions (list): 年龄相关条件
        gender_conditions (list): 性别相关条件
        satisfy_bmi (bool): 是否满足BMI条件
        satisfy_age (bool): 是否满足年龄条件
        satisfy_gender (bool): 是否满足性别条件

        返回:
        dict: 包含BMI、年龄和性别的字典
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

        # 生成性别值
        if satisfy_gender:
            gender = self.generate_valid_gender(gender_conditions)
        else:
            gender = self.generate_invalid_gender(gender_conditions)

        return {'BMI': bmi, '年龄': age, '性别': gender}


    def generate_valid_bmi(self, conditions):
        """生成符合所有BMI条件的值"""
        if not conditions:
            return round(random.uniform(10.0, 60.0), 1)

        # 初始化默认范围
        bmi_min = 10.0
        bmi_max = 60.0

        for condition in conditions:
            if '=' in condition and '<=' in condition:
                # 处理类似 "BMI<=24"
                parts = condition.split('<=')
                if 'BMI' in parts[0]:
                    bmi_max = min(bmi_max, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    bmi_min = max(bmi_min, float(parts[0].strip()))

            elif '=' in condition and '>=' in condition:
                # 处理类似 "BMI>=24"
                parts = condition.split('>=')
                if 'BMI' in parts[0]:
                    bmi_min = max(bmi_min, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    bmi_max = min(bmi_max, float(parts[0].strip()))

            elif '<' in condition:
                # 处理类似 "BMI<24" 或 "24>BMI"
                parts = condition.split('<')
                if 'BMI' in parts[0]:
                    # BMI < 24
                    bmi_max = min(bmi_max, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    # 24 < BMI
                    bmi_min = max(bmi_min, float(parts[0].strip()))

            elif '>' in condition:
                # 处理类似 "BMI>24" 或 "24>BMI"
                parts = condition.split('>')
                if 'BMI' in parts[0]:
                    # BMI > 24
                    bmi_min = max(bmi_min, float(parts[1].strip()))
                elif 'BMI' in parts[1]:
                    # 24 > BMI → BMI < 24
                    bmi_max = min(bmi_max, float(parts[0].strip()))

            elif '=' in condition:
                # 处理固定值，如 "BMI=24"
                parts = condition.split('=')
                if 'BMI' in parts[0]:
                    return float(parts[1].strip())
                elif 'BMI' in parts[1]:
                    return float(parts[0].strip())

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
    # 条件列表
    # l_conditions = ['14<年龄<14.5', '22.3<=BMI', '性别=男']
    # l_conditions = ['年龄=3', '14.3>BMI', '性别=女']
    # l_conditions = ['年龄=5', '14.7>BMI', '性别=女']
    l_conditions = ['年龄=5', '14.7<BMI<14.9', '性别=女']

    BmiAgeSex_PO = BmiAgeSexPO()
    l_1 = []
    for i in l_conditions:
        if "BMI" in i:
            l_simple_conditions = BmiAgeSex_PO.split_compound_condition(i)
            l_1.extend(l_simple_conditions)
        elif "年龄" in i:
            l_simple_conditions = BmiAgeSex_PO.split_compound_condition(i)
            l_1.extend(l_simple_conditions)
        else:
            l_1.append(i)
    print(l_1)


    try:
        # 生成每种情况的样本
        cases = BmiAgeSex_PO.generate_all_cases(l_1)
        print(cases)

        # # 打印结果
        # for case_name, samples in cases.items():
        #     print(f"\n情况: {case_name}")
        #     for i, sample in enumerate(samples, 1):
        #         print(f"样本 {i}: {sample}")

    except ValueError as e:
        print(f"错误: {e}")


