def generate_unmatched_cases(conditions):
    """
    生成不满足指定条件的年龄、BMI、性别组合示例（年龄保留1位小数，BMI保留1位小数）

    参数:
        conditions: 条件列表，每个元素为一个条件子列表
                    格式如: [['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ...]

    返回:
        list: 不满足条件的组合示例列表
    """
    # 解析条件中的关键参数
    age_ranges = set()
    bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

    for cond in conditions:
        age_min = None
        age_max = None
        bmi_min = None
        gender = None

        for c in cond:
            if c.startswith('年龄>='):
                age_min = float(c.split('>=')[1])
            elif c.startswith('年龄<'):
                age_max = float(c.split('<')[1])
            elif c.startswith('BMI>='):
                bmi_min = float(c.split('>=')[1])
            elif c.startswith('性别='):
                gender = c.split('=')[1]

        if all([age_min, age_max, bmi_min, gender]):
            age_range = (age_min, age_max)
            age_ranges.add(age_range)
            bmi_thresholds[gender][age_range] = bmi_min

    # 生成不满足条件的示例组合
    unmatched = []

    # 1. 年龄低于最小范围（取最小年龄阈值-0.5）
    min_age = min(r[0] for r in age_ranges)
    test_age = round(min_age - 0.5, 1)  # 确保低于最小年龄范围
    sample_bmi = 22.0  # 代表性BMI值（低于多数阈值）
    unmatched.append({
        '年龄': test_age,
        'BMI': round(sample_bmi, 1),
        '性别': '男'
    })
    unmatched.append({
        '年龄': test_age,
        'BMI': round(sample_bmi, 1),
        '性别': '女'
    })

    # 2. 年龄高于最大范围（取最大年龄阈值+0.5）
    max_age = max(r[1] for r in age_ranges)
    test_age = round(max_age + 0.5, 1)  # 确保高于最大年龄范围
    unmatched.append({
        '年龄': test_age,
        'BMI': round(sample_bmi, 1),
        '性别': '男'
    })
    unmatched.append({
        '年龄': test_age,
        'BMI': round(sample_bmi, 1),
        '性别': '女'
    })

    # 3. 年龄在范围内但男性BMI不达标（取区间中间值）
    for (age_min, age_max), bmi_min in bmi_thresholds['男'].items():
        test_age = round((age_min + age_max) / 2, 1)  # 区间中间值
        test_bmi = round(bmi_min - 0.1, 1)  # 低于阈值0.1确保不满足
        unmatched.append({
            '年龄': test_age,
            'BMI': test_bmi,
            '性别': '男'
        })

    # 4. 年龄在范围内但女性BMI不达标（取区间中间值）
    for (age_min, age_max), bmi_min in bmi_thresholds['女'].items():
        test_age = round((age_min + age_max) / 2, 1)  # 区间中间值
        test_bmi = round(bmi_min - 0.1, 1)  # 低于阈值0.1确保不满足
        unmatched.append({
            '年龄': test_age,
            'BMI': test_bmi,
            '性别': '女'
        })

    return unmatched


# 测试示例（使用新条件）
if __name__ == "__main__":
    conditions = [
        ['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'],
        ['年龄>=14.5', '年龄<15', 'BMI>=22.6', '性别=男'],
        ['年龄>=15', '年龄<15.5', 'BMI>=22.9', '性别=男'],
        ['年龄>=15.5', '年龄<16', 'BMI>=23.1', '性别=男'],
        ['年龄>=16', '年龄<16.5', 'BMI>=23.3', '性别=男'],
        ['年龄>=16.5', '年龄<17', 'BMI>=23.5', '性别=男'],
        ['年龄>=17', '年龄<17.5', 'BMI>=23.7', '性别=男'],
        ['年龄>=17.5', '年龄<18', 'BMI>=23.8', '性别=男'],
        ['年龄>=14', '年龄<14.5', 'BMI>=22.8', '性别=女'],
        ['年龄>=14.5', '年龄<15', 'BMI>=23.0', '性别=女'],
        ['年龄>=15', '年龄<15.5', 'BMI>=23.2', '性别=女'],
        ['年龄>=15.5', '年龄<16', 'BMI>=23.4', '性别=女'],
        ['年龄>=16', '年龄<16.5', 'BMI>=23.6', '性别=女'],
        ['年龄>=16.5', '年龄<17', 'BMI>=23.7', '性别=女'],
        ['年龄>=17', '年龄<17.5', 'BMI>=23.8', '性别=女'],
        ['年龄>=17.5', '年龄<18', 'BMI>=23.9', '性别=女']
    ]

    result = generate_unmatched_cases(conditions)
    # 格式化输出
    import pprint

    pprint.pprint(result, indent=4)


print(generate_unmatched_cases([['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ['年龄>=14.5', '年龄<15', 'BMI>=22.6', '性别=男'], ['年龄>=15', '年龄<15.5', 'BMI>=22.9', '性别=男'], ['年龄>=15.5', '年龄<16', 'BMI>=23.1', '性别=男'], ['年龄>=16', '年龄<16.5', 'BMI>=23.3', '性别=男'], ['年龄>=16.5', '年龄<17', 'BMI>=23.5', '性别=男'], ['年龄>=17', '年龄<17.5', 'BMI>=23.7', '性别=男'], ['年龄>=17.5', '年龄<18', 'BMI>=23.8', '性别=男'], ['年龄>=14', '年龄<14.5', 'BMI>=22.8', '性别=女'], ['年龄>=14.5', '年龄<15', 'BMI>=23.0', '性别=女'], ['年龄>=15', '年龄<15.5', 'BMI>=23.2', '性别=女'], ['年龄>=15.5', '年龄<16', 'BMI>=23.4', '性别=女'], ['年龄>=16', '年龄<16.5', 'BMI>=23.6', '性别=女'], ['年龄>=16.5', '年龄<17', 'BMI>=23.7', '性别=女'], ['年龄>=17', '年龄<17.5', 'BMI>=23.8', '性别=女'], ['年龄>=17.5', '年龄<18', 'BMI>=23.9', '性别=女']]))