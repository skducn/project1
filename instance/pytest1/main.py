# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-4-7
# Description: pytest
# https://zhuanlan.zhihu.com/p/697749358
# 学习视频：https://www.bilibili.com/video/BV1aN4y1u7MB?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372

# todo 执行具体的测试用例
# pytest 文件名.py
# pytest 文件名.py::类名
# pytest 文件名.py::类名::方法名
# pytest run.py::TestPytest::test_one - v

# todo 调用次数
# 模块级（setup_module/teardown_module）在模块始末调用
# 函数级（setup_function/teardown_function）在函数始末调用(在类外部）
# 类级（setup_class/teardown_class）在类始末调用（在类中）
# 方法级（setup_method/teardown_methond）在方法始末调用（在类中）
# 方法级（setup/teardown）在方法始末调用（在类中）
# 调用顺序：
# setup_module > setup_class >setup_method > setup > teardown > teardown_method > teardown_class > teardown_module

# todo 按照order顺序执行
# pytest-order 插件，指定用例的执行顺序只需要在测试用例的方法前面加上装饰器 @pytest.mark.run(order=[num]) 设置order的对应的num值，它就可以按照 num 的大小顺序来执行。
# pip install pytest-ordering

# todo 执行错误用例
# pytest --lf (只重现运行错误的用例，如果上一次没有错误用例，则执行所有用例)
# pytest --ff (先运行错误用例，在运行其他用例，如果上一次没有错误用例，则执行所有用例)
#***************************************************************

import pytest

class TestPytest(object):

    @pytest.mark.run(order=-1)
    def test_two(self):
        print("test_two，测试用例")

    @pytest.mark.run(order=3)
    def test_one(self):
        print("test_one，测试用例")

    @pytest.mark.run(order=1)
    def test_three(self):
        print("\ntest_three，测试用例")