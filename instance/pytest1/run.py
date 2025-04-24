# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-4-7
# Description: pytest
# https://zhuanlan.zhihu.com/p/697749358
# pytest-order 插件，指定用例的执行顺序只需要在测试用例的方法前面加上装饰器 @pytest.mark.run(order=[num]) 设置order的对应的num值，它就可以按照 num 的大小顺序来执行。
# pip install pytest-ordering
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