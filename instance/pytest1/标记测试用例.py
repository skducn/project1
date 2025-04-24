# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-4-7
# Description: 标记测试用例
# https://www.bilibili.com/video/BV12f4y1d7c3?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372# pytest 文件名.py
# 场景：只执行符合要求的一部分用例，使用@pytest.mark.标签名，参数 -m

#  pytest 标记测试用例.py -vs -m "int"
#***************************************************************

import pytest

def double(a):
    return a*2

@pytest.mark.int
def test_double_int():
    print("test double int")
    assert 2 == double(1)

@pytest.mark.minus
def test_double_minus():
    print("test double minus")
    assert -2 == double(-1)

@pytest.mark.float
def test_double_float():
    print("test double float")
    assert -10.2 == double(-0.1)

@pytest.mark.float
def test_double1_float():
    print("test double float")
    assert -0.6 == double(-3)