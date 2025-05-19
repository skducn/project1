def check_number_type(num):
    """判断输入的数字是整数还是浮点数"""
    if isinstance(num, int):
        return "整数"
    elif isinstance(num, float):
        # 检查是否为整数形式的浮点数，如 3.0
        if num.is_integer():
            print(int(num))
        else:
            return "浮点数"
    else:
        return "不是数字类型"


# 测试示例
if __name__ == "__main__":
    test_values = [5, 3.14, 2.0, -7, -4.5, "hello", [1, 2]]

    for value in test_values:
        result = check_number_type(value)
        print(f"{value} 的类型是：{result}")