import re
import random


class BmiPO:
    def generate_all_cases(self, conditions):
        """
        根据条件动态生成 satisfied 和 not1 的样本数据
        """

        # 提取所有 BMI 条件
        bmi_conditions = [c for c in conditions if c.startswith('BMI')]

        satisfied_samples = []
        not1_samples = []

        # 存储上下限和边界值
        lower_bounds = []
        upper_bounds = []
        boundary_values = set()
        has_inequality = False  # 是否包含 <= 或 >=

        # 第一遍：提取操作符类型和边界值
        for cond in bmi_conditions:
            match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
            if not match:
                continue

            op, value_str = match.groups()
            val = float(value_str)

            if op == '>=':
                lower_bounds.append(val)
                boundary_values.add(val)
                has_inequality = True
            elif op == '<=':
                upper_bounds.append(val)
                boundary_values.add(val)
                has_inequality = True
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
        satisfied_samples.extend({'BMI': v} for v in sorted(boundary_values))

        # 如果条件中包含 <= 或 >=，则生成两个样本；否则只生成一个
        target_count = 2 if has_inequality else 1

        while len(satisfied_samples) < target_count:
            value = round(random.uniform(bmi_min, bmi_max), 1)
            if not any(item['BMI'] == value for item in satisfied_samples):  # 避免重复
                satisfied_samples.append({'BMI': value})

        # 去重并保留指定数量的样本
        unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())[:target_count]

        # # 生成不满足条件的样本
        # 替换原来的 not1 样本生成逻辑
        not1_samples = []

        # 如果有多个 BMI 条件，尝试从不同区间各取一个
        if len(bmi_conditions) > 1:
            # 第一次强制生成小于下限的值
            low_sample = self._generate_invalid_bmi([c for c in bmi_conditions if 'BMI<' in c or 'BMI<=' in c])
            not1_samples.append(low_sample)

            # 第二次强制生成大于等于上限的值
            high_sample = self._generate_invalid_bmi([c for c in bmi_conditions if 'BMI>' in c or 'BMI>=' in c])
            if low_sample['BMI'] != high_sample['BMI']:
                not1_samples.append(high_sample)
        else:
            # 单一条件只生成一个样本
            not1_sample = self._generate_invalid_bmi(bmi_conditions)
            not1_samples.append(not1_sample)


        return {
            "satisfied": unique_satisfied,
            "notSatisfied": not1_samples
        }

    def _generate_invalid_bmi(self, conditions):
        """
        生成一个不满足所有 BMI 条件的值，且在合理范围内 [10.0, 60.0]
        :param conditions: 条件列表，例如 ['BMI>=24']
        :return: {'BMI': value}
        """

        invalid_ranges = []

        for cond in conditions:
            match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
            if not match:
                continue

            op, value_str = match.groups()
            value = float(value_str)

            # 动态识别非法区间
            if op == '>':
                # 条件是 'BMI > x' → 不满足的区间是 'BMI <= x'
                invalid_ranges.append((10.0, value))
            elif op == '>=':
                # 条件是 'BMI >= x' → 不满足的区间是 'BMI < x'
                invalid_ranges.append((10.0, value - 0.1))
            elif op == '<':
                # 条件是 'BMI < x' → 不满足的区间是 'BMI >= x'
                invalid_ranges.append((value, 60.0))
            elif op == '<=':
                # 条件是 'BMI <= x' → 不满足的区间是 'BMI > x'
                invalid_ranges.append((value + 0.1, 60.0))

        # 如果有多个非法区间，取交集或并集（这里用并集更合适）
        if invalid_ranges:
            # 取所有非法区间的最小下界和最大上界
            invalid_min = max(r[0] for r in invalid_ranges)
            invalid_max = min(r[1] for r in invalid_ranges)

            if invalid_min <= invalid_max:
                # 在非法区间内生成一个随机值
                invalid_value = round(random.uniform(invalid_min, invalid_max), 1)
            else:
                # 区间无交集时，从 [10.0, 60.0] 中随机选一个不满足任意条件的值
                invalid_value = round(random.uniform(10.0, 60.0), 1)
        else:
            # 没有条件时，默认生成 [10.0, 60.0] 范围内的值
            invalid_value = round(random.uniform(10.0, 60.0), 1)

        return {'BMI': invalid_value}

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


# 测试入口
if __name__ == "__main__":
    Bmi_PO = BmiPO()

    # 18.5<=BMI<24.0
    # 24.0<=BMI<28.0
    # 18.5<=BMI<24.0
    # 24.0<=BMI<28.0
    print("\n测试条件: ['BMI>=18.5','BMI<24.0']")
    print(Bmi_PO.generate_all_cases(['BMI>=18.5','BMI<24.0']))

    print("\n测试条件: ['BMI<18.5']")
    print(Bmi_PO.generate_all_cases(['BMI<18.5']))

    print("\n测试条件: ['BMI<=18.5']")
    print(Bmi_PO.generate_all_cases(['BMI<=18.5']))

    print("\n测试条件: ['BMI>24']")
    print(Bmi_PO.generate_all_cases(['BMI>24']))

    print("\n测试条件: ['BMI>=24']")
    print(Bmi_PO.generate_all_cases(['BMI>=24']))
