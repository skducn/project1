def generate_unmatched_cases2(conditions):
    """
    生成不满足指定条件的年龄、BMI、性别组合示例（年龄保留1位小数，BMI保留1位小数）

    参数:
        conditions: 条件列表，每个元素为一个条件子列表
                    格式如: [['年龄>=14', '年龄<14.5', 'BMI>=22.3', '性别=男'], ...]

    返回:
        list: 不满足条件的组合示例列表
    """
    # 解析条件中的关键参数
    age_values = set()  # 存储具体的年龄值
    age_ranges = set()  # 存储年龄范围
    bmi_thresholds = {'男': {}, '女': {}}  # 按性别存储不同年龄区间的BMI阈值

    for cond in conditions:
        age_value = None
        age_min = None
        age_max = None
        bmi_min = None
        bmi_max = None
        gender = None

        for c in cond:
            if c.startswith('年龄='):
                age_value = float(c.split('=')[1])
                age_values.add(age_value)
            elif c.startswith('年龄>='):
                age_min = float(c.split('>=')[1])
            elif c.startswith('年龄<'):
                age_max = float(c.split('<')[1])
            elif c.startswith('BMI>='):
                bmi_min = float(c.split('>=')[1])
            elif c.startswith('BMI<='):
                bmi_max = float(c.split('<=')[1])
            elif c.startswith('BMI<'):
                bmi_max = float(c.split('<')[1])
            elif c.startswith('性别='):
                gender = c.split('=')[1]

        # 处理具体年龄值的情况
        if age_value is not None and gender is not None:
            bmi_range = {}
            if bmi_min is not None:
                bmi_range['min'] = bmi_min
            if bmi_max is not None:
                bmi_range['max'] = bmi_max
            if bmi_range:
                bmi_thresholds[gender][age_value] = bmi_range
                age_ranges.add((age_value, age_value))  # 将具体值转换为范围

        # 处理年龄范围的情况
        elif all(x is not None for x in [age_min, age_max, gender]):
            age_range = (age_min, age_max)
            age_ranges.add(age_range)
            bmi_range = {}
            if bmi_min is not None:
                bmi_range['min'] = bmi_min
            if bmi_max is not None:
                bmi_range['max'] = bmi_max
            if bmi_range:
                bmi_thresholds[gender][age_range] = bmi_range

    # 如果没有解析到有效的条件，则返回空列表
    if not age_ranges:
        return []

    # 生成不满足条件的示例组合
    unmatched = []

    # 1. 年龄不在任何有效范围内
    if age_ranges:
        min_age = min(r[0] for r in age_ranges)
        max_age = max(r[1] for r in age_ranges)

        # 年龄低于最小范围
        test_age = round(min_age - 0.5, 1)
        sample_bmi = 15.0
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

        # 年龄高于最大范围
        test_age = round(max_age + 0.5, 1)
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

    # 2. 年龄在范围内但BMI不满足条件
    for gender in ['男', '女']:
        for age_key, bmi_range in bmi_thresholds[gender].items():
            # 确定测试年龄
            if isinstance(age_key, tuple):  # 年龄范围
                test_age = round((age_key[0] + age_key[1]) / 2, 1)
            else:  # 具体年龄值
                test_age = round(age_key, 1)

            # 生成不满足BMI条件的值
            if 'min' in bmi_range and 'max' in bmi_range:
                # 既有最小值又有最大值，生成范围外的值
                test_bmi_below = round(bmi_range['min'] - 0.1, 1)
                test_bmi_above = round(bmi_range['max'], 1)  # 等于最大值时不满足条件
                unmatched.append({
                    '年龄': test_age,
                    'BMI': test_bmi_below,
                    '性别': gender
                })
                unmatched.append({
                    '年龄': test_age,
                    'BMI': test_bmi_above,
                    '性别': gender
                })
            elif 'min' in bmi_range:
                # 只有最小值，生成小于最小值的BMI
                test_bmi = round(bmi_range['min'] - 0.1, 1)
                unmatched.append({
                    '年龄': test_age,
                    'BMI': test_bmi,
                    '性别': gender
                })
            elif 'max' in bmi_range:
                # 只有最大值，生成大于等于最大值的BMI
                test_bmi = round(bmi_range['max'], 1)
                unmatched.append({
                    '年龄': test_age,
                    'BMI': test_bmi,
                    '性别': gender
                })

    # 3. 性别不匹配的情况
    if age_values:
        sample_age = list(age_values)[0]
        sample_bmi = 15.0
        unmatched.append({
            '年龄': round(sample_age, 1),
            'BMI': round(sample_bmi, 1),
            '性别': '未知'
        })

    return unmatched


# # 测试示例（使用新条件）
# if __name__ == "__main__":
#     conditions = [['年龄>=73', '年龄<79', 'BMI<13.4', '性别=男'], ['年龄>=79', '年龄<84', 'BMI<13.8', '性别=男'], ['年龄>=73', '年龄<79', 'BMI<13.1', '性别=女'], ['年龄>=79', '年龄<84', 'BMI<13.3', '性别=女']]
#
#     result = generate_unmatched_cases2(conditions)
#     # 格式化输出
#     import pprint
#
#     pprint.pprint(result, indent=4)


print(generate_unmatched_cases2([['年龄>=73', '年龄<79', 'BMI<13.4', '性别=男'], ['年龄>=79', '年龄<84', 'BMI<13.8', '性别=男'], ['年龄>=73', '年龄<79', 'BMI<13.1', '性别=女'], ['年龄>=79', '年龄<84', 'BMI<13.3', '性别=女']]))
# print(generate_unmatched_cases2([['年龄=1', 'BMI>=12.9', 'BMI<16.4', '性别=男'], ['年龄=2', 'BMI>=14.2', 'BMI<18.1', '性别=男'], ['年龄=3', 'BMI>=14.8', 'BMI<19', '性别=男'], ['年龄=4', 'BMI>=15', 'BMI<19.4', '性别=男'], ['年龄=5', 'BMI>=15.1', 'BMI<19.5', '性别=男'], ['年龄=1', 'BMI>=12.6', 'BMI<15.9', '性别=女'], ['年龄=2', 'BMI>=13.7', 'BMI<17.5', '性别=女'], ['年龄=3', 'BMI>=14.3', 'BMI<18.3', '性别=女'], ['年龄=4', 'BMI>=14.6', 'BMI<18.6', '性别=女'], ['年龄=5', 'BMI>=14.7', 'BMI<18.8', '性别=女']]))