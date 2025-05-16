import itertools
import random

import re


def parse_condition(condition_str):
    # 提取变量名、运算符和值
    match = re.match(r'(\w+)\s*([<>=!]+)\s*([\d.]+)', condition_str)
    if not match:
        raise ValueError(f"无法解析条件: {condition_str}")

    var_name, operator, value_str = match.groups()
    value = float(value_str)

    # 根据运算符生成对应的函数
    if operator == '>':
        return lambda x: x > value
    elif operator == '<':
        return lambda x: x < value
    elif operator == '>=':
        return lambda x: x >= value
    elif operator == '<=':
        return lambda x: x <= value
    elif operator == '==':
        return lambda x: x == value
    elif operator == '!=':
        return lambda x: x != value
    else:
        raise ValueError(f"不支持的运算符: {operator}")




# 定义条件函数
def bmi_condition(bmi):
    return bmi >= 24


def age_lt65_condition(age):
    return age < 65


def age_gte18_condition(age):
    return age >= 18


# 生成测试数据点
def generate_test_points():
    # 边界值和随机值
    bmi_points = [23.9, 24, 24.1]
    age_points = [17, 18, 18.1, 65.1]
    return bmi_points, age_points


# 主函数
def main():

    # # 使用示例
    # condition_str = 'BMI>=24'
    # bmi_condition = parse_condition(condition_str)
    # condition_str = 'age < 65'
    # age_lt65_condition = parse_condition(condition_str)
    # condition_str = 'age >= 65'
    # age_gte18_condition = parse_condition(condition_str)
    #
    # # 测试生成的函数
    # print(bmi_condition(23))  # False
    # print(bmi_condition(24))  # True
    # print(bmi_condition(25))  # True

    a = 'BMI>=24 and 年龄>=18 and 年龄<65'
    l = ['BMI>=24', '年龄>=18', '年龄<65']

    bmi_points, age_points = generate_test_points()

    # 生成所有组合
    all_combinations = list(itertools.product(bmi_points, age_points))
    print(all_combinations) # [(23.9, 17), (23.9, 18), (23.9, 18.1), (23.9, 65.1), (24, 17), (24, 18), (24, 18.1), (24, 65.1), (24.1, 17), (24.1, 18), (24.1, 18.1), (24.1, 65.1)]


    # 条件列表
    conditions = [bmi_condition, age_lt65_condition, age_gte18_condition]

    # 遍历所有组合并分类
    valid_combinations = []
    invalid_combinations = []

    for bmi, age in all_combinations:
        # 检查所有条件是否满足
        results = [cond(bmi if i == 0 else age) for i, cond in enumerate(conditions)]
        is_valid = all(results)

        if is_valid:
            valid_combinations.append((bmi, age, results))
        else:
            invalid_combinations.append((bmi, age, results))

    # 输出结果
    print("有效组合 (BMI, 年龄):")
    for bmi, age, results in valid_combinations:
        print(f"BMI={bmi:.1f}, 年龄={age:.1f}")

    print("\n无效组合 (BMI, 年龄):")
    for bmi, age, results in invalid_combinations:
        print(f"BMI={bmi:.1f}, 年龄={age:.1f}, 条件结果: {results}")


if __name__ == "__main__":
    main()