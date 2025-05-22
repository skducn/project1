import re
import random
from typing import List, Dict, Tuple, Set


class AgeConditionParser:

    def __init__(self, conditions: List[str]):
        """初始化条件解析器"""
        self.conditions = self._preprocess_conditions(conditions)  # 预处理条件
        self.min_age = 0  # 年龄最小值
        self.max_age = 120  # 年龄最大值
        self.parsed_conditions = self._parse_conditions()

    def _preprocess_conditions(self, conditions: List[str]) -> List[str]:
        """预处理条件列表，拆分复合条件（如 '年龄>=4 and 年龄<10'）"""
        processed = []
        for condition in conditions:
            # 按 'and' 拆分（忽略大小写，处理 'AND'、'and'、'And' 等）
            sub_conditions = re.split(r'\s+and\s+', condition, flags=re.IGNORECASE)
            for sub in sub_conditions:
                # 处理 '年龄=10' 这种情况
                sub = sub.strip()
                if re.match(r'^年龄\s*=\s*(\d+)$', sub):
                    value = re.match(r'^年龄\s*=\s*(\d+)$', sub).group(1)
                    processed.extend([f"年龄>={value}", f"年龄<={value}"])
                else:
                    processed.append(sub)
        return processed

    def _parse_conditions(self) -> Dict:
        """解析条件列表，提取最小值和最大值约束"""
        min_value = None
        max_value = None
        include_min = False
        include_max = False

        for condition in self.conditions:
            # 使用正则表达式匹配条件格式，支持 = 操作符
            match = re.match(r'^年龄\s*(>=|>|<=|<|=)\s*(\d+)$', condition)
            if not match:
                raise ValueError(f"条件格式不正确: {condition}")

            operator, value = match.groups()
            value = int(value)

            # 更新最小值约束
            if operator in ('>=', '>', '='):
                if operator == '>=':
                    if min_value is None or value > min_value or (value == min_value and not include_min):
                        min_value = value
                        include_min = True
                elif operator == '>':
                    adjusted_value = value + 1
                    if min_value is None or adjusted_value > min_value or (
                            adjusted_value == min_value and not include_min):
                        min_value = adjusted_value
                        include_min = True
                else:  # '='
                    if min_value is None or value > min_value or (value == min_value and not include_min):
                        min_value = value
                        include_min = True

            # 更新最大值约束
            if operator in ('<=', '<', '='):
                if operator == '<=':
                    if max_value is None or value < max_value or (value == max_value and not include_max):
                        max_value = value
                        include_max = True
                elif operator == '<':
                    adjusted_value = value - 1
                    if max_value is None or adjusted_value < max_value or (
                            adjusted_value == max_value and not include_max):
                        max_value = adjusted_value
                        include_max = True
                else:  # '='
                    if max_value is None or value < max_value or (value == max_value and not include_max):
                        max_value = value
                        include_max = True

        # 检查约束是否矛盾
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError("条件矛盾，没有有效解")

        return {
            'min_value': min_value,
            'max_value': max_value,
            'include_min': include_min,
            'include_max': include_max
        }

    def get_satisfied_values(self) -> List[int]:
        """生成满足所有条件的值，无等于号时只输出一个随机合法值"""
        values = []
        parsed = self.parsed_conditions
        min_val = parsed['min_value']
        max_val = parsed['max_value']
        include_min = parsed['include_min']
        include_max = parsed['include_max']

        # 检查所有条件是否都没有等于号
        all_without_equals = not any(
            '>=' in condition or '<=' in condition or '=' in condition
            for condition in self.conditions
        )

        # 确定有效范围
        if min_val is not None and max_val is not None:
            start = min_val if include_min else min_val + 1
            end = max_val if include_max else max_val - 1

            if start > end:
                return []  # 无有效范围

            valid_range = list(range(start, end + 1))
            if not valid_range:
                return []

            if all_without_equals:
                # 所有条件都没有等于号，只返回一个随机合法值
                values.append(random.choice(valid_range))
            else:
                # 添加闭区间边界值
                if include_min:
                    values.append(min_val)
                if include_max and max_val not in values:
                    values.append(max_val)

                # 如果只有一个边界值或无等于号条件，添加一个中间值
                if len(values) < 2 and len(valid_range) > 1:
                    mid_value = valid_range[len(valid_range) // 2]
                    if mid_value not in values:
                        values.append(mid_value)

        # 只有最小值约束
        elif min_val is not None:
            start = min_val if include_min else min_val + 1
            valid_range = list(range(start, self.max_age + 1))

            if all_without_equals:
                values.append(random.choice(valid_range))
            else:
                values.append(start)
                if len(valid_range) > 1:
                    next_value = valid_range[min(1, len(valid_range) - 1)]
                    if next_value not in values:
                        values.append(next_value)

        # 只有最大值约束
        elif max_val is not None:
            end = max_val if include_max else max_val - 1
            valid_range = list(range(self.min_age, end + 1))

            if all_without_equals:
                values.append(random.choice(valid_range))
            else:
                values.append(end)
                if len(valid_range) > 1:
                    prev_value = valid_range[max(0, len(valid_range) - 2)]
                    if prev_value not in values:
                        values.append(prev_value)

        # 无约束（所有年龄都有效）
        else:
            if all_without_equals:
                values.append(random.randint(self.min_age, self.max_age))
            else:
                values.append(self.min_age)
                if self.max_age > self.min_age:
                    values.append(self.max_age)

        # 过滤无效值
        values = [v for v in values if self.min_age <= v <= self.max_age]
        # 去重
        return list(dict.fromkeys(values))

    def get_not_satisfied_values(self) -> List[int]:
        """生成不满足条件的值，覆盖所有边界和超出范围的无效值"""
        values = []
        parsed = self.parsed_conditions
        min_val = parsed['min_value']
        max_val = parsed['max_value']
        include_min = parsed['include_min']
        include_max = parsed['include_max']

        # 检查条件中是否包含 >= 或 <= 或 =
        has_gte = any('>=' in cond or '=' in cond for cond in self.conditions)
        has_lte = any('<=' in cond or '=' in cond for cond in self.conditions)

        # 生成边界无效值
        lower_invalid = None  # 小于下界的无效值
        upper_invalid = None  # 大于上界的无效值

        # 处理下界
        if min_val is not None:
            if include_min or has_gte:  # 条件是 >= 或包含 >= 或 =
                # 添加刚好小于最小值的值
                if min_val > self.min_age:
                    lower_invalid = min_val - 1
            else:  # 条件是 >
                # 添加最小值本身
                lower_invalid = min_val

        # 处理上界
        if max_val is not None:
            if include_max or has_lte:  # 条件是 <= 或包含 <= 或 =
                # 添加刚好大于最大值的值
                if max_val < self.max_age:
                    upper_invalid = max_val + 1
            else:  # 条件是 <
                # 添加最大值本身
                upper_invalid = max_val

        # 添加生成的边界无效值
        if lower_invalid is not None:
            values.append(lower_invalid)
        if upper_invalid is not None:
            values.append(upper_invalid)

        # 确保至少有4个无效值（如果可能）
        if len(values) < 4:
            # 添加远离边界的值
            if min_val is not None:
                far_min = max(self.min_age, min_val - 10)
                if far_min not in values:
                    values.append(far_min)

            if max_val is not None:
                far_max = min(self.max_age, max_val + 10)
                if far_max not in values:
                    values.append(far_max)

        # 去重并过滤无效值
        values = [v for v in set(values) if self.min_age <= v <= self.max_age]
        # 限制为4个值
        return sorted(values)[:4]


class AgePO():

    def splitMode(self, condition):
        """
        拆分
        将形如 '6<=年龄<6.5' 或 '14.7<年龄<18.8' 的复合条件拆分为两个标准条件
        :param condition: 条件字符串
        :return: 拆分后的简单条件列表
        """

        cond = condition.strip().replace(" ", "")

        # 匹配形如：6<=年龄<6.5 或 14.7<年龄<18.8
        match = re.match(r'^(\d+(?:\.\d+)?)(<=|<|>=|>)(年龄|年龄)(<=|<|>=|>)(\d+(?:\.\d+)?)$', cond)

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
        将形如 '18.5>年龄' 转换为 '年龄<18.5'
        :param condition: 条件字符串
        :return: 拆分或转换后的条件列表
        """
        cond = condition.strip().replace(" ", "")

        # 匹配类似 18.5>年龄 或 24<年龄 这样的逆序写法
        match = re.match(r'^(\d+(?:\.\d+)?)(>|>=|<|<=)(年龄)$', cond)

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

    def generate_test_cases(self, conditions: List[str]) -> Dict:
        """生成测试用例"""
        test_cases = {}

        try:
            # 直接使用条件列表
            parser = AgeConditionParser(conditions)
            satisfied = parser.get_satisfied_values()
            not_satisfied = parser.get_not_satisfied_values()

            test_cases[f"条件"] = {
                "条件": conditions,
                "有效(satisfied)": satisfied,
                "无效(notSatisfied)": not_satisfied
            }
        except ValueError as e:
            test_cases[f"条件"] = {
                "条件": conditions,
                "错误": str(e)
            }

        return test_cases

    def generate_all_cases(self, conditions: List[str]) -> Dict:
        """生成所有测试用例"""
        test_cases = self.generate_test_cases(conditions)

        for key, value in test_cases.items():
            if "错误" in value:
                print(f"\n{key}: {value['条件']}")
                print(f"  错误: {value['错误']}")
            else:
                satisfied = [{'年龄': v} for v in value['有效(satisfied)']]
                not_satisfied = [{'年龄': v} for v in value['无效(notSatisfied)']]
                result = {'satisfied': satisfied, 'notSatisfied': not_satisfied}
                return result


if __name__ == "__main__":
    Age_PO = AgePO()


    print(Age_PO.generate_all_cases(['年龄>4', '年龄<10']))  # {'satisfied': [{'年龄': 5}], 'notSatisfied': [{'年龄': 0}, {'年龄': 4}, {'年龄': 10}, {'年龄': 19}]}

    print(Age_PO.generate_all_cases(['年龄>=4', '年龄<10']))  # {'satisfied': [{'年龄': 4}, {'年龄': 9}], 'notSatisfied': [{'年龄': 0}, {'年龄': 3}, {'年龄': 10}, {'年龄': 19}]}

    print(Age_PO.generate_all_cases(['年龄>4', '年龄<=10']))  # {'satisfied': [{'年龄': 5}, {'年龄': 10}], 'notSatisfied': [{'年龄': 0}, {'年龄': 4}, {'年龄': 11}, {'年龄': 20}]}


    print(Age_PO.generate_all_cases(['年龄<10']))  # {'satisfied': [{'年龄': 10}, {'年龄': 9}], 'notSatisfied': [{'年龄': 11}, {'年龄': 20}]}
    print(Age_PO.generate_all_cases(['年龄<=10']))  # {'satisfied': [{'年龄': 10}, {'年龄': 9}], 'notSatisfied': [{'年龄': 11}, {'年龄': 20}]}

    print(Age_PO.generate_all_cases(['年龄>24']))  # {'satisfied': [{'年龄': 25}], 'notSatisfied': [{'年龄': 15}, {'年龄': 24}]}
    print(Age_PO.generate_all_cases(['年龄>=24']))  # {'satisfied': [{'年龄': 24}, {'年龄': 25}], 'notSatisfied': [{'年龄': 14}, {'年龄': 23}]}

    print(Age_PO.generate_all_cases(['年龄=10']))  # {'satisfied': [{'年龄': 10}], 'notSatisfied': [{'年龄': 0}, {'年龄': 9}, {'年龄': 11}, {'年龄': 20}]}

