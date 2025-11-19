def parse_condition(condition):
    """解析单个条件字符串为函数"""
    condition = condition.strip()

    # 处理复合条件: 18.0<=年龄<65.0
    if '<=' in condition and '<' in condition:
        parts = condition.split('<=')
        left_value = float(parts[0].strip())
        right_part = parts[1].split('<')
        mid_var = right_part[0].strip()
        right_value = float(right_part[1].strip())
        return lambda x: left_value <= x[mid_var] < right_value

    # 处理其他条件
    elif '>=' in condition:
        var, value = condition.split('>=')
        return lambda x: x[var.strip()] >= float(value.strip())
    elif '<=' in condition:
        var, value = condition.split('<=')
        return lambda x: x[var.strip()] <= float(value.strip())
    elif '>' in condition:
        var, value = condition.split('>')
        return lambda x: x[var.strip()] > float(value.strip())
    elif '<' in condition:
        var, value = condition.split('<')
        return lambda x: x[var.strip()] < float(value.strip())
    else:
        raise ValueError(f"无法解析条件: {condition}")

def filter_samples(samples, conditions):
    """
    根据条件筛选样本

    参数:
    samples (list): 样本列表，每个样本是一个字典
    conditions (list): 条件列表，每个条件是一个字符串

    返回:
    tuple: 包含两个列表的元组，第一个是符合条件的样本，第二个是不符合条件的样本
    """
    parsed_conditions = [parse_condition(cond) for cond in conditions]

    valid_samples = []
    invalid_samples = []

    for sample in samples:
        is_valid = True
        for condition_func in parsed_conditions:
            if not condition_func(sample):
                is_valid = False
                break
        if is_valid:
            valid_samples.append(sample)
        else:
            invalid_samples.append(sample)

    return valid_samples, invalid_samples


# 示例用法
if __name__ == "__main__":
    # 示例样本数据
    samples = [
        {"BMI": 25.5, "年龄": 35.0},
        {"BMI": 22.0, "年龄": 45.0},
        {"BMI": 26.0, "年龄": 17.5},
        {"BMI": 24.0, "年龄": 60.0},
        {"BMI": 23.5, "年龄": 65.5}
    ]

    # 条件列表
    conditions = ['BMI>=24', '18.0<=年龄<65.0']

    # 筛选样本
    valid, invalid = filter_samples(samples, conditions)

    print("符合条件的样本:")
    for sample in valid:
        print(sample)

    print("\n不符合条件的样本:")
    for sample in invalid:
        print(sample)    