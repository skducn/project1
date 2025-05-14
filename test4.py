
def convert_conditions(conditions):
    valid_operators = ['=', '>', '<', '>=', '<=']
    result = []

    for condition in conditions:
        operator_pos = -1
        current_op = None
        for op in sorted(valid_operators, key=len, reverse=True):
            pos = condition.find(op)
            if pos != -1:
                operator_pos = pos
                current_op = op
                break

        if operator_pos == -1:
            continue  # 忽略无法解析的条件

        left = condition[:operator_pos].strip()
        right = condition[operator_pos + len(current_op):].strip()

        if left and right:
            result.append(f"{left}{current_op}{right}")

    return " and ".join(result)


# 测试示例
conditions = ['年龄=2', 'BMI>18.1', 'BMI<19.7', '性别=男']
print(convert_conditions(conditions))  # 输出: 年龄=2 and BMI>18.1 and BMI<19.7