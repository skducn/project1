import sys
import os

# 这是一个用于测试路径的工具脚本
# 打印当前文件路径
print(f"当前文件路径: {os.path.abspath(__file__)}")

# 尝试计算到project目录的路径
dir1 = os.path.dirname(os.path.abspath(__file__))  # 造数据
dir2 = os.path.dirname(dir1)  # CDRD
dir3 = os.path.dirname(dir2)  # zyjk
dir4 = os.path.dirname(dir3)  # instance
dir5 = os.path.dirname(dir4)  # project

print(f"project目录路径: {dir5}")

# 添加project目录到路径
sys.path.append(dir5)
print(f"Python路径已添加: {dir5}")

# 尝试导入PO模块
try:
    from PO.SqlserverPO import *
    print("成功导入PO.SqlserverPO模块!")
except ImportError as e:
    print(f"导入失败: {e}")
    # 打印完整的Python路径，用于调试
    print("当前Python路径:")
    for path in sys.path:
        print(f"- {path}")