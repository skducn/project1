# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-4-7
# Description: 数据驱动 yaml
# https://www.bilibili.com/video/BV1B94y197vo?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372
#***************************************************************

import pytest
import yaml


class TestDemo:
    @pytest.mark.parametrize("env", yaml.safe_load(open("./env.yml")))
    def test_demo(self, env):
        if "test" in env:
            print("测试环境的ip是：", env['test'])

            print("开发环境的ip是：", env['dev'])
