# https://www.bilibili.com/video/BV1bt4y147M4?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372

# 参数化
# 定量信息变量化

import pytest

# todo 单参数
l_search1 = ['john', 'selenium', 'pytest']
@pytest.mark.parametrize('name', l_search1)
def test_search(name):
    assert name in l_search1


# todo 多参数
# l_search2 = [("3+5", 8), ("4*5", 20)]
l_search2 = [["3+5", 8], ["4*5", 20]]
@pytest.mark.parametrize('param1, expected', l_search2, ids=['add', 'mul'])
# ids 表示重命名
def test_search2(param1, expected):
    assert eval(param1) == expected


# todo 笛卡尔积
@pytest.mark.parametrize('wd', ['selenium', 'pytest', 'linux'])
@pytest.mark.parametrize('code', ['utf-8', 'gbk', 'gb2312'])
def test_dkej(wd, code):
    print(f"wd: {wd}, code:{code}")
