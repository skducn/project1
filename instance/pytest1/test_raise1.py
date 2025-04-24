# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-4-7
# Description: pytest.raise() 异常处理
# https://www.bilibili.com/video/BV1GG411p7Nt?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372

#***************************************************************

import pytest

def test_raise():
    with pytest.raises((ZeroDivisionError, ValueError)):
        raise ZeroDivisionError('除数为0')

def test_raise1():
    with pytest.raises(ValueError) as exc_info:
        raise ValueError('value must be 43')
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == 'value must be 43'