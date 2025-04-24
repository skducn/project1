# *****************************************************************
# Author     : John
# Date       : 2025-4-198
# Description: 使用 xlwings 库定义可在 Excel 中调用的函数，并启动通信服务器
# 说明：
# - @xw.func：xlwings 装饰器，将普通 Python 函数转换为可在 Excel 中调用的函数
# - xw.serve()：启动服务器，实现 Excel 与 Python 的通信
# - xlwings 版本: 0.31.0
# 安装命令: (py310) localhost-2:i linghuchong$ xlwings addin install
# 安装完成后需重启 Excel (通过 Cmd-Q 退出，然后重新启动)
# *****************************************************************

import xlwings as xw

@xw.func
def add_numbers(a: float, b: float) -> float:
    """
    将两个数相加

    参数:
    a (float): 第一个数
    b (float): 第二个数

    返回:
    float: 两个数相加的结果
    """
    try:
        return float(a) + float(b)
    except ValueError:
        print("输入不是有效的数字，请检查输入。")
        return None

@xw.func
def multiply_numbers(a: float, b: float) -> float:
    """
    将两个数相乘

    参数:
    a (float): 第一个数
    b (float): 第二个数

    返回:
    float: 两个数相乘的结果
    """
    try:
        return float(a) * float(b)
    except ValueError:
        print("输入不是有效的数字，请检查输入。")
        return None

if __name__ == '__main__':
    try:
        xw.serve()
    except Exception as e:
        print(f"启动服务器时出现错误: {e}")