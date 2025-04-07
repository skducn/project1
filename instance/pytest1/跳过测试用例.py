# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-4-7
# Description: 跳过及预期失败
# https://www.bilibili.com/video/BV12G411H7Ws?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372
# skip 始终跳过该测试用例
# skipif 遇到特定情况跳过该测试用例
# xfail 遇到特定情况，产生一个"期望失败"输出

# @pytest.mark.skip
# @pytest.mark.skipif
# pytest.skip(reason)
# pytest.xfail(reason)
#***************************************************************

import pytest

# todo skip用法1
@pytest.mark.skip
def test_aaa():
    assert True

@pytest.mark.skip(reason='代码没有实现')
def test_bbb():
    assert False


# todo skip用法2
def is_login():
    return False

# 函数中依赖前置条件，如果登录失败，则跳过该测试用例
def test_function():
    print("start")
    # 如果未登录，则跳过后续步骤，不打印end
    if not is_login():
        pytest.skip("登录失败，不执行此函数")
    print("end")


# todo skipif用法
import sys
@pytest.mark.skipif(sys.platform =='darwin', reason='does not run on mac')
def test_case1():
    assert True

@pytest.mark.skipif(sys.platform =='win', reason='does not run on windows')
def test_case2():
    assert True

@pytest.mark.skipif(sys.version_info < (3,6), reason='requires python3.6 or higher')
def test_case3():
    assert True



# todo xfail用法

# 结果：XPASS
@pytest.mark.xfail
def test_case4():
    print("test_xfail1 方法执行")
    assert 2 == 2

# 结果：XFAIL (bug 110)
xfail = pytest.mark.xfail
@xfail(reason='bug 110')
def test_case5():
    assert 0


# 结果：XFAIL (该功能尚未完成)                       [100%]开始测试
def test_xfail():
    print('开始测试')
    pytest.xfail(reason='该功能尚未完成')
    # 后面的都不被执行
    print('测试过程')
    assert 1==1