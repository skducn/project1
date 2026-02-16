# import pytest,os
#
# if __name__ == '__main__':
#     pytest.main(['-s', '-v', '--alluredir=allure-results'])
#     os.system(r'allure generate -c -o 测试报告')


# -*- coding: utf-8 -*-
import pytest
import os
import sys

if __name__ == '__main__':
    # 添加当前目录到Python路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # 运行pytest
    exit_code = pytest.main([
        '-s',  # 显示print输出
        '-v',  # 详细模式
        '--tb=short',  # 简洁的错误追踪
        '--alluredir=allure-results'  # 生成allure报告
    ])

    # 生成HTML测试报告
    if os.path.exists('allure-results'):
        os.system('allure generate -c -o 测试报告')
        print("\n📊 测试报告已生成到 '测试报告' 目录")

    # 退出程序
    sys.exit(exit_code)



# 结果：
# ============================= test session starts ==============================
# platform darwin -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0 -- /Users/linghuchong/miniconda3/envs/py311/bin/python
# cachedir: .pytest_cache
# rootdir: /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/CDRD/web/ai测试框架
# plugins: anyio-4.12.1, asyncio-1.3.0, langsmith-0.7.3, allure-pytest-2.15.3
# asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
# collecting ... 所有测试用例:  [{'用例标题': '首页搜索功能测试', '用例描述': '1，打开网页 http://novel.hctestedu.com/\n2，搜索框中输入文字“反派”，然后点击搜索按钮\n3，找到搜索结果列表序号1对应的小说名称\n结果：如果名称等于“我的123反派生涯”返回“测试通过”，否则返回测试失败'}]
# collected 2 items
#
# core.py::test_case_exec[case0]
# 🎯 执行测试用例: 首页搜索功能测试
# 📝 测试描述: 1，打开网页 http://novel.hctestedu.com/
# 2，搜索框中输入文字“反派”，然后点击搜索按钮
# 3，找到搜索结果列表序号1对应的小说名称
# 结果：如果名称等于“我的123反派生涯”返回“测试通过”，否则返回测试失败
# 执行AI测试: 1，打开网页 http://novel.hctestedu.com/
# 2，搜索框中输入文字“反派”，然后点击搜索按钮
# 3，找到搜索结果列表序号1对应的小说名称
# 结果：如果名称等于“我的123反派生涯”返回“测试通过”，否则返回测试失败
# ✅ 测试用例 '首页搜索功能测试' 执行成功
# PASSED
# core.py::test_simple_case 执行AI测试: 请验证基础功能
# 简单测试结果: {'status': 'success', 'message': '测试通过'}
# PASSED
#
# ============================== 2 passed in 2.93s ===============================
# Report successfully generated to 测试报告
#
# 📊 测试报告已生成到 '测试报告' 目录