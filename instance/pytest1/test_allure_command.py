# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-4-7
# Description: allure
# https://www.bilibili.com/video/BV1kd4y1D7BD?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372
# 官网源码：https://allurereport.org/docs/#_pytest
# 源码example：https://github.com/allure-examples/allure-examples
# https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/
# 官网：https://allurereport.org/docs/install-for-macos/
# vi ~/.bash_profile
# export PATH=$PATH:/Users/linghuchong/Downloads/51/Python/allure/allure-2.32.2/bin
# Source ~/.bash_profile
# Allure --version

# 执行步骤：
# pip3 install allure-pytest
# pytest --alluredir ./result -vs
# pytest --alluredir ./result -vs --clean-alluredir
# pytest serve ./result
# allure generate ./result
# allure open -h 127.0.0.1 -p 8883 ./allure-report
# allure open -h 192.168.1.105 -p 8883 ./allure-report

#
# @allure.epic()
# 参数值：epic 描述。
# 参数说明：用于定义项目，当存在多个项目时使用，是一种高层次的分类，在它之下是 Feature 。
# @allure.feature()
# 参数值：模块名称。
# 参数说明：按照模块区分用例，为不同功能模块命名，方便对测试用例进行归类管理 。
# @allure.story()
# 参数值：用例名称。
# 参数说明：对具体测试用例的描述，突出用例的业务场景或功能点 。
# @allure.title
# 参数值：用例标题。
# 参数说明：测试用例的标题，简洁明了地概括用例核心内容 。
# @allure.testcase()
# 参数值：用例相关链接。
# 参数说明：指向自动化用例对应的功能用例存放系统的地址，方便关联查看详细功能用例 。
# @allure.issue()
# 参数值：缺陷地址。
# 参数说明：对应缺陷管理系统里的缺陷地址，方便在测试报告中快速定位缺陷 。
# @allure.description()
# 参数值：用例描述。
# 参数说明：对测试用例进行详细说明，涵盖用例的前置条件、预期结果等信息 。
# @allure.step()
# 参数值：操作步骤。
# 参数说明：记录测试用例的具体操作步骤，便于复现和理解测试过程 。
# @allure.severity()
# 参数值：用例等级，取值包括 blocker 、critical 、normal 、minor 、trivial 。
# 参数说明：定义测试用例的严重程度，帮助团队评估用例失败时对系统的影响程度 。
# @allure.link()
# 参数值：定义连接。
# 参数说明：用于在测试报告中展示需要关联的链接，如需求文档链接等 。
# @allure.attachment()
# 参数值：附件。
# 参数说明：向测试报告中添加附件，如日志文件、截图等，辅助理解测试结果 。
#***************************************************************

import pytest

def test_success():
    assert True

def test_failure():
    assert False

def test_skip():
    pytest.skip('forr a reason!')

def test_broken():
    raise Exception('oops')