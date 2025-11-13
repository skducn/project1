import re
import itertools


class BmiAgeSexPO():
    def parse_condition(self, condition_str):
        """解析条件字符串为变量名、运算符和值"""
        # 处理复合条件，如 "18.0<=年龄<65.0"
        if '<=' in condition_str and '<' in condition_str:
            # 移除所有空格以简化解析
            clean_cond = condition_str.replace(' ', '')
            # 分割条件字符串
            parts = re.split(r'(<=|<)', clean_cond)

            # 提取变量名和上下限
            lower_part = parts[0]
            operator1 = parts[1]
            var_part = parts[2]
            operator2 = parts[3]
            upper_part = parts[4]

            var_name = var_part
            lower_bound = float(lower_part)
            upper_bound = float(upper_part)

            return var_name, lambda x: lower_bound <= x < upper_bound

        # 处理简单条件
        match = re.match(r'(\w+)\s*(!=|==|<=|>=|<|>|=)\s*([\d.]+|男|女)', condition_str)
        if not match:
            raise ValueError(f"无法解析条件: {condition_str}")

        var_name, operator, value_str = match.groups()

        # 判断是否为性别字段
        gender_map = {'男': 1, '女': 2}
        if value_str in gender_map:
            value = gender_map[value_str]
        else:
            value = float(value_str) if '.' in value_str else int(value_str)

        if operator == '>':
            return var_name, lambda x: x > value
        elif operator == '<':
            return var_name, lambda x: x < value
        elif operator == '>=':
            return var_name, lambda x: x >= value
        elif operator == '<=':
            return var_name, lambda x: x <= value
        elif operator == '==':
            return var_name, lambda x: x == value
        elif operator == '!=':
            return var_name, lambda x: x != value
        elif operator == '=':  # 支持单个等号
            return var_name, lambda x: x == value
        else:
            raise ValueError(f"不支持的运算符: {operator}")

    def generate_test_points(self, conditions):
        """为每个变量生成测试点"""
        test_points = {}
        var_conditions = {}

        # 按变量名组织条件
        for cond in conditions:
            var_name, _ = self.parse_condition(cond)
            var_conditions.setdefault(var_name, []).append(cond)

        for var_name, var_conds in var_conditions.items():
            if var_name == '性别':
                # 性别只取两个值：男/女 → 内部用 1 / 2 表示
                test_points[var_name] = [1, 2]
            elif var_name == '年龄':
                points = set()
                # 检查是否有复合条件（如 年龄>=18 和 年龄<65）
                if len(var_conds) > 1:
                    # 处理复合条件
                    lower_bound = None
                    upper_bound = None
                    has_lower = False
                    has_upper = False

                    for cond in var_conds:
                        threshold = float(re.search(r'([<>=!]+)\s*([\d.]+)', cond).group(2))
                        operator = re.search(r'([<>=!]+)', cond).group(1)

                        if operator == '>=':
                            if lower_bound is None or threshold > lower_bound:
                                lower_bound = threshold
                                has_lower = True
                        elif operator == '>':
                            if lower_bound is None or threshold >= lower_bound:
                                lower_bound = threshold
                                has_lower = True
                        elif operator == '<=':
                            if upper_bound is None or threshold < upper_bound:
                                upper_bound = threshold
                                has_upper = True
                        elif operator == '<':
                            if upper_bound is None or threshold <= upper_bound:
                                upper_bound = threshold
                                has_upper = True

                    # 生成复合条件的测试点
                    if has_lower:
                        points.add(int(lower_bound))      # 下界（有效）
                        points.add(int(lower_bound + 1))  # 下界后一个值（有效）
                    if has_upper:
                        points.add(int(upper_bound))      # 上界（无效）

                    # 添加边界外的无效值
                    if has_lower:
                        points.add(int(lower_bound - 1))  # 下界前一个值（无效）
                else:
                    # 处理单一条件
                    for cond in var_conds:
                        if '<=' in cond and '<' in cond:
                            # 处理复合条件如 "66<=年龄<69"
                            parts = re.split(r'(<=|<)', cond.replace(' ', ''))
                            lower_bound = int(float(parts[0]))
                            upper_bound = int(float(parts[-1]))

                            # 生成边界值（有效值和无效值）
                            points.add(lower_bound - 1)  # 下界前一个值（无效）
                            points.add(lower_bound)      # 下界（有效）
                            # 根据需求，对于66<=年龄<69只需要66和67，不需要68
                            if upper_bound - lower_bound > 1:
                                points.add(lower_bound + 1)  # 下界后一个值（有效）
                            points.add(upper_bound)      # 上界（无效）
                            # 移除了 upper_bound + 1，避免生成70这样的无效值
                        else:
                            # 处理简单条件
                            match = re.match(r'年龄\s*(!=|==|<=|>=|<|>|=)\s*([\d.]+)', cond)
                            if match:
                                operator, value_str = match.groups()
                                value = int(float(value_str))

                                if operator == '>':
                                    points.add(value)      # 无效（等于不满足大于）
                                    points.add(value + 1)  # 有效
                                    points.add(value + 2)  # 有效（确保有足够有效值）
                                elif operator == '<':
                                    points.add(value - 1)  # 有效
                                    points.add(value)      # 无效（等于不满足小于）
                                    points.add(value - 2)  # 有效（确保有足够有效值）
                                elif operator == '>=':
                                    points.add(value - 1)  # 无效
                                    points.add(value)      # 有效
                                    points.add(value + 1)  # 有效
                                elif operator == '<=':
                                    points.add(value)      # 有效
                                    points.add(value + 1)  # 无效
                                    points.add(value - 1)  # 有效
                                elif operator in ('==', '='):
                                    points.add(value)      # 有效
                                    points.add(value + 1)  # 无效（只添加一个无效值）
                                elif operator == '!=':
                                    points.add(value)      # 无效
                                    points.add(value + 1)  # 有效

                # 过滤掉负数年龄
                points = [p for p in points if p >= 0]
                test_points[var_name] = sorted(list(set(points)))
            else:  # BMI等其他变量
                points = set()
                # 检查是否有复合条件（如 BMI>=20 和 BMI<27）
                if len(var_conds) > 1:
                    # 处理复合条件
                    lower_bound = None
                    upper_bound = None
                    has_lower = False
                    has_upper = False

                    for cond in var_conds:
                        threshold = float(re.search(r'([<>=!]+)\s*([\d.]+)', cond).group(2))
                        operator = re.search(r'([<>=!]+)', cond).group(1)

                        if operator == '>=':
                            if lower_bound is None or threshold > lower_bound:
                                lower_bound = threshold
                                has_lower = True
                        elif operator == '>':
                            if lower_bound is None or threshold >= lower_bound:
                                lower_bound = threshold
                                has_lower = True
                        elif operator == '<=':
                            if upper_bound is None or threshold < upper_bound:
                                upper_bound = threshold
                                has_upper = True
                        elif operator == '<':
                            if upper_bound is None or threshold <= upper_bound:
                                upper_bound = threshold
                                has_upper = True

                    # 生成复合条件的测试点 - 简化测试点生成
                    if has_lower:
                        points.add(round(lower_bound, 10))      # 下界（有效）
                        points.add(round(lower_bound + 0.1, 10))  # 下界后一个值（有效）
                    if has_upper:
                        points.add(round(upper_bound, 10))        # 上界（无效）

                    # 添加边界外的无效值
                    if has_lower:
                        points.add(round(lower_bound - 0.1, 10))  # 下界前一个值（无效）
                else:
                    # 处理单一条件
                    for cond in var_conds:
                        if '<=' in cond and '<' in cond:
                            parts = re.split(r'(<=|<)', cond.replace(' ', ''))
                            lower_bound = float(parts[0])
                            upper_bound = float(parts[-1])

                            # 生成边界值（有效值和无效值）
                            points.add(round(lower_bound - 0.1, 10))  # 下界前一个值（无效）
                            points.add(round(lower_bound, 10))  # 下界（有效）
                            if upper_bound - lower_bound > 0.2:
                                points.add(round(lower_bound + 0.1, 10))  # 下界后一个值（有效）
                                points.add(round(upper_bound - 0.1, 10))  # 上界前一个值（有效）
                            points.add(round(upper_bound, 10))  # 上界（无效）
                            points.add(round(upper_bound + 0.1, 10))  # 上界后一个值（无效）
                        else:
                            threshold = float(re.search(r'([<>=!]+)\s*([\d.]+)', cond).group(2))
                            match = re.search(r'([<>=!]+)', cond)
                            if match:
                                operator = match.group(1)

                                if operator == '>':
                                    points.add(round(threshold, 10))  # 无效（等于不满足大于）
                                    points.add(round(threshold + 0.1, 10))  # 有效
                                elif operator == '<':
                                    points.add(round(threshold - 0.1, 10))  # 有效
                                    points.add(round(threshold, 10))  # 无效（等于不满足小于）
                                elif operator == '>=':
                                    points.add(round(threshold - 0.1, 10))  # 无效
                                    points.add(round(threshold, 10))  # 有效
                                    points.add(round(threshold + 0.1, 10))  # 有效
                                elif operator == '<=':
                                    points.add(round(threshold, 10))  # 有效
                                    points.add(round(threshold + 0.1, 10))  # 无效
                                elif operator in ('==', '='):
                                    points.add(round(threshold, 10))  # 有效
                                    points.add(round(threshold + 0.1, 10))  # 无效（只添加一个无效值）
                                elif operator == '!=':
                                    points.add(round(threshold, 10))  # 无效
                                    points.add(round(threshold + 0.1, 10))  # 有效

                test_points[var_name] = sorted(list(set(points)))

        return test_points

    def combinations(self, conditions, test_points):
        """测试所有组合并分类为有效和无效"""
        # 按变量名组织条件
        var_conditions = {}
        for cond in conditions:
            var_name, cond_func = self.parse_condition(cond)
            var_conditions.setdefault(var_name, []).append(cond_func)

        # 生成所有可能的组合
        variables = list(test_points.keys())
        value_combinations = itertools.product(*[test_points[var] for var in variables])

        valid = []
        invalid = []

        for values in value_combinations:
            value_dict = dict(zip(variables, values))
            is_valid = True

            # 检查所有条件
            for var, conds in var_conditions.items():
                if not all(cond(value_dict[var]) for cond in conds):
                    is_valid = False
                    break

            if is_valid:
                valid.append(value_dict)
            else:
                invalid.append(value_dict)

        return valid, invalid

    def format_output(self, data):
        """格式化输出结果"""
        result = []
        for item in data:
            formatted = {}
            for var, val in item.items():
                if var == '性别':
                    formatted[var] = '男' if val == 1 else '女'
                elif var == '年龄':
                    formatted[var] = int(val)
                else:
                    formatted[var] = round(float(val), 1)
            result.append(formatted)
        return result

    def main(self, conditions):
        """主函数，生成满足和不满足条件的组合"""
        # 生成测试点
        test_points = self.generate_test_points(conditions)

        # 测试所有组合
        valid, invalid = self.combinations(conditions, test_points)

        # 格式化输出
        return {
            'satisfied': self.format_output(valid),
            'notSatisfied': self.format_output(invalid)
        }


# 测试入口
if __name__ == "__main__":
    BmiAgeSex_PO = BmiAgeSexPO()

    # 测试示例
    print("测试条件: ['年龄=6', 'BMI>=19.5', '性别=男']")
    result1 = BmiAgeSex_PO.main(['年龄=6', 'BMI>=19.5', '性别=男'])
    print(result1)

    print("\n测试条件: ['66<=年龄<69', 'BMI<12', '性别=男']")
    result2 = BmiAgeSex_PO.main(['66<=年龄<69', 'BMI<12', '性别=男'])
    print(result2)

    print("\n测试条件: ['BMI<18.5', '年龄>=18', '年龄<65', '性别=女']")
    result3 = BmiAgeSex_PO.main(['BMI<18.5', '年龄>=18', '年龄<65', '性别=女'])
    print(result3)

    print("\n测试条件: ['BMI<27', 'BMI>=20', '年龄>=65', '性别=女']")
    print(BmiAgeSex_PO.main(['BMI<27', 'BMI>=20', '年龄>=65', '性别=女']))
