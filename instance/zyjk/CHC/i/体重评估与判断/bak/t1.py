import re
import random
import itertools


def parse_condition(condition_str):
    """解析条件字符串为变量名、运算符和值"""
    match = re.match(r'(\w+)\s*([<>=!]+)\s*([\d.]+)', condition_str)
    if not match:
        raise ValueError(f"无法解析条件: {condition_str}")

    var_name, operator, value_str = match.groups()
    value = float(value_str)

    # 生成对应的判断函数
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
    else:
        raise ValueError(f"不支持的运算符: {operator}")


def generate_test_points(conditions, num_random=1):
    """根据条件动态生成测试点"""
    test_points = {}

    for cond in conditions:
        var_name, cond_func = parse_condition(cond)

        # 从条件中提取阈值
        threshold = float(re.search(r'([<>=!]+)\s*([\d.]+)', cond).group(2))

        # 为每个变量创建测试点
        if var_name not in test_points:
            # 边界值
            points = [threshold - 0.1, threshold, threshold + 0.1]

            # 添加随机值
            if '>=' in cond or '>' in cond:
                points.extend([random.uniform(threshold + 0.2, threshold + 10) for _ in range(num_random)])
                points.extend([random.uniform(threshold - 10, threshold - 0.2) for _ in range(num_random)])
            elif '<=' in cond or '<' in cond:
                points.extend([random.uniform(threshold - 10, threshold - 0.2) for _ in range(num_random)])
                points.extend([random.uniform(threshold + 0.2, threshold + 10) for _ in range(num_random)])

            test_points[var_name] = points

    return test_points


def combinations(conditions, test_points):
    """测试所有组合并分类为有效和无效"""
    # 按变量名组织条件
    var_conditions = {}
    for cond in conditions:
        var_name, cond_func = parse_condition(cond)
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


def main():
    # 可配置的条件列表
    conditions = ['BMI>=24', '年龄>=18', '年龄<65']

    # 生成测试点
    test_points = generate_test_points(conditions)

    # 测试所有组合
    valid, invalid = combinations(conditions, test_points)

    # 输出结果
    print(f"有效组合 ({len(valid)}):")
    for case in valid:
        print(', '.join([f"{var}={val:.2f}" for var, val in case.items()]))

    print(f"\n无效组合 ({len(invalid)}):")
    for case in invalid:
        print(', '.join([f"{var}={val:.2f}" for var, val in case.items()]))


if __name__ == "__main__":
    main()