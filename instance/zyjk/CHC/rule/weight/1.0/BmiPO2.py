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
        satisfied_samples.extend({'BMI': v} for v in sorted(boundary_values))

        # 补充随机值以确保至少有一个样本
        while len(satisfied_samples) < 1:
            value = round(random.uniform(bmi_min, bmi_max), 1)
            if not any(item['BMI'] == value for item in satisfied_samples):  # 避免重复
                satisfied_samples.append({'BMI': value})

        # 去重并保留一个样本
        unique_satisfied = list({frozenset(item.items()): item for item in satisfied_samples}.values())[:1]

        # 生成不满足条件的样本（必须是非负数）
        not1_sample = self._generate_invalid_bmi(bmi_conditions)
        not1_samples.append(not1_sample)

        return {
            "satisfied": unique_satisfied,
            "not1": not1_samples
        }

    # def _generate_invalid_bmi(self, conditions):
    #     """
    #     生成一个不满足所有 BMI 条件的值，且不能为负数
    #     :param conditions: 条件列表，例如 ['BMI<18.5']
    #     :return: {'BMI': value}
    #     """
    #     valid_ranges = []
    #
    #     for cond in conditions:
    #         match = re.match(r'BMI([<>=]+)(\d+(?:\.\d+)?)', cond)
    #         if not match:
    #             continue
    #
    #         op, value_str = match.groups()
    #         value = float(value_str)
    #
    #         if op == '>':
    #             valid_ranges.append((value + 0.1, 60.0))
    #         elif op == '>=':
    #             valid_ranges.append((value, 60.0))
    #         elif op == '<':
    #             valid_ranges.append((0.0, value - 0.1))  # 允许下界为 0，但后续做非负处理
    #         elif op == '<=':
    #             valid_ranges.append((0.0, value))
    #
    #     # 计算合法区间
    #     satisfied_min = max(r[0] for r in valid_ranges) if valid_ranges else 10.0
    #     satisfied_max = min(r[1] for r in valid_ranges) if valid_ranges else 60.0
    #
    #     # 确保上界不超过最大值 60.0
    #     satisfied_max = min(satisfied_max, 60.0)
    #
    #     # 在合法区间外生成一个无效值，但不能为负数
    #     if satisfied_min <= satisfied_max:
    #         # 合法区间为 [satisfied_min, satisfied_max]
    #         # 所以非法值只能在 [10.0, satisfied_min - 0.1] 或 [satisfied_max + 0.1, 60.0] 区间中生成
    #         if random.random() < 0.5:
    #             # 下界区间
    #             invalid_value = round(random.uniform(10.0, max(10.0, satisfied_min - 0.1)), 1)
    #         else:
    #             # 上界区间
    #             invalid_value = round(random.uniform(min(60.0, satisfied_max + 0.1), 60.0), 1)
    #     else:
    #         # 条件冲突，所有值都是非法的，只生成 [10.0, 60.0] 内的随机值
    #         invalid_value = round(random.uniform(10.0, 60.0), 1)
    #
    #     return {'BMI': invalid_value}

    def _generate_invalid_bmi(self, conditions):
        """
        生成一个不满足所有 BMI 条件的值，且不能是合法值或负数
        :param conditions: 条件列表，例如 ['BMI<18.5']
        :return: {'BMI': value}
        """

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

        satisfied_min = max(r[0] for r in valid_ranges) if valid_ranges else 10.0
        satisfied_max = min(r[1] for r in valid_ranges) if valid_ranges else 60.0

        # 确保不在合法范围内，并且不能小于 10.0
        if satisfied_min <= satisfied_max:
            # 合法区间是 [satisfied_min, satisfied_max]，比如 [10.0, 18.4]
            # 所以非法值必须 >= 18.5
            invalid_value = round(random.uniform(satisfied_max + 0.1, 60.0), 1)
        else:
            # 条件冲突时，从 [10.0, 60.0] 随机选一个（虽然都非法）
            invalid_value = round(random.uniform(10.0, 60.0), 1)

        return {'BMI': invalid_value}


# 测试入口
if __name__ == "__main__":
    bmi_po = BmiPO()

    # 指定条件
    # cases = bmi_po.generate_all_cases(['BMI<18.5'])
    cases = bmi_po.generate_all_cases(['BMI<=18.5'])

    print(cases)

