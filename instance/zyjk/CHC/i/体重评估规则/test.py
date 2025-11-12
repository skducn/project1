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


# 使用示例
condition_str = 'BMI>=24'
bmi_condition = parse_condition(condition_str)

# 测试生成的函数
print(bmi_condition(23))  # False
print(bmi_condition(24))  # True
print(bmi_condition(25))  # True