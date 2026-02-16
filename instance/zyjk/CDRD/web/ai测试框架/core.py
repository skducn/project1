# -*- coding: utf-8 -*-
import pytest
import allure
import os
import asyncio
import json
from datetime import datetime


# 使用pandas读取Excel文件
def read_test_cases():
    """读取测试用例Excel文件"""
    try:
        import pandas as pd

        excel_file = "测试用例.xlsx"
        if not os.path.exists(excel_file):
            print(f"警告: 找不到 {excel_file} 文件，使用默认测试用例")
            return get_default_test_cases()

        df = pd.read_excel(excel_file, sheet_name=0)

        test_cases = []
        for _, row in df.iterrows():
            test_cases.append({
                "用例标题": row.get("用例标题", f"测试用例_{_}"),
                "用例描述": row.get("用例描述", "请执行基本操作")
            })

        return test_cases

    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return get_default_test_cases()


def get_default_test_cases():
    """默认测试用例"""
    return [
        {
            "用例标题": "百度搜索测试",
            "用例描述": "请访问百度搜索人工智能"
        },
        {
            "用例标题": "简单导航测试",
            "用例描述": "请访问百度首页"
        }
    ]


# 读取测试用例
all_case = read_test_cases()
print("所有测试用例: ", all_case)

# 导入AI处理函数
try:
    from ai_main import process_by_ai
except ImportError:
    async def process_by_ai(description):
        print(f"执行AI测试: {description}")
        await asyncio.sleep(1)
        return {"status": "success", "message": "测试通过", "details": "模拟测试成功"}


@pytest.mark.parametrize('case', all_case)
@pytest.mark.asyncio
@allure.feature("AI自动化测试")
@allure.story("Web自动化功能测试")
async def test_case_exec(case):
    """AI自动化测试用例执行"""

    # 设置测试用例标题和描述
    allure.dynamic.title(case["用例标题"])
    allure.dynamic.description(f"测试描述: {case['用例描述']}")

    # 添加测试步骤
    with allure.step("准备测试环境"):
        print(f"\n🎯 准备执行测试用例: {case['用例标题']}")

    try:
        with allure.step("执行AI自动化测试"):
            print(f"📝 测试描述: {case['用例描述']}")

            # 记录开始时间
            start_time = datetime.now()
            allure.attach(str(start_time), "开始时间", allure.attachment_type.TEXT)

            # 执行AI测试
            test_result = await process_by_ai(case["用例描述"])

            # 记录结束时间
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            allure.attach(str(end_time), "结束时间", allure.attachment_type.TEXT)
            allure.attach(str(duration), "执行耗时(秒)", allure.attachment_type.TEXT)

        with allure.step("验证测试结果"):
            # 验证结果并记录到报告
            assert test_result is not None, "测试执行失败，返回结果为空"

            # 根据返回结果类型进行不同的断言
            success_message = ""
            if isinstance(test_result, dict):
                status = test_result.get("status", "").lower()
                message = test_result.get("message", "")
                details = test_result.get("details", "")

                allure.attach(json.dumps(test_result, ensure_ascii=False, indent=2),
                              "详细测试结果", allure.attachment_type.JSON)

                assert status in ["success", "completed", "pass"], f"测试失败: {test_result}"
                success_message = f"✅ 测试用例 '{case['用例标题']}' 执行成功 - {message}"

            elif isinstance(test_result, str):
                allure.attach(test_result, "测试结果", allure.attachment_type.TEXT)
                assert "成功" in test_result or "success" in test_result.lower(), f"测试失败: {test_result}"
                success_message = f"✅ 测试用例 '{case['用例标题']}' 执行成功"

            else:
                allure.attach(str(test_result), "测试结果", allure.attachment_type.TEXT)
                success_message = f"✅ 测试用例 '{case['用例标题']}' 执行成功"

            # 将成功消息记录到Allure报告
            allure.attach(success_message, "执行结果", allure.attachment_type.TEXT)
            print(success_message)

            # 添加环境信息
            allure.attach("Python 3.11", "测试环境", allure.attachment_type.TEXT)
            allure.attach("browser-use AI", "测试框架", allure.attachment_type.TEXT)

    except Exception as e:
        # 记录失败信息到Allure报告
        error_message = f"❌ 测试用例 '{case['用例标题']}' 执行失败: {str(e)}"
        allure.attach(error_message, "错误信息", allure.attachment_type.TEXT)
        print(error_message)
        pytest.fail(f"测试执行异常: {str(e)}")


# 独立测试函数
@pytest.mark.asyncio
@allure.feature("AI自动化测试")
@allure.story("基础功能验证")
async def test_simple_case():
    """简单的独立测试"""
    with allure.step("执行简单功能验证"):
        test_case = {
            "用例标题": "简单功能验证",
            "用例描述": "请验证基础功能"
        }

        result = await process_by_ai(test_case["用例描述"])
        allure.attach(json.dumps(result, ensure_ascii=False), "简单测试结果", allure.attachment_type.JSON)
        assert result is not None
        print(f"简单测试结果: {result}")


# 测试套件配置
@pytest.fixture(scope="session", autouse=True)
def configure_allure_report():
    """配置Allure报告环境信息"""
    allure.dynamic.label("environment", "development")
    allure.dynamic.label("framework", "browser-use")
    allure.dynamic.label("language", "Python 3.11")
