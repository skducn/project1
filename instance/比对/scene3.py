# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-9-12
# Description   : 场景三：API 响应 JSON 深度结构比对
# 场景：接口回归测试中，JSON 响应往往嵌套多层，且包含时间戳、请求 ID 等动态字段。若采用全量断言，将导致用例频繁失败；若人工抽样，又可能遗漏关键业务差异。
# 步骤 1：解决思路深度遍历 JSON，忽略动态字段，只保留业务关键差异。
# 　　·遍历：递归比较嵌套结构。
# 　　· 忽略：用路径表达式排除 timestamp、request_id。
# 　　· 聚焦：自定义关键字段列表，差异一目了然。
# *********************************************************************

import json
from deepdiff import DeepDiff

def validate_api_response(actual, expected, ignore_fields=None):
    """
    API响应验证工具
    :param actual: 实际结构
    :param expected: 预期结构
    :param ignore_fields: 忽略的动态字段列表（默认忽略timestamp、request_id）
    """
    if ignore_fields is None:
        ignore_fields = ['timestamp', 'request_id']
    # 转换JSON字符串为dict（如果需要）
    if isinstance(actual, str):
        actual = json.loads(actual)
    if isinstance(expected, str):
        expected = json.loads(expected)
    # 深度比对（忽略动态字段、数组顺序）
    diff = DeepDiff(
        expected,
        actual,
        ignore_order=True,  # 忽略数组顺序
        exclude_paths=[f"root['{field}']" for field in ignore_fields]  # 忽略动态字段
    )
    # 返回所有差异
    return {
        "critical_diff": diff,  # 所有差异
        "full_diff": diff  # 完整差异（供调试）
    }

def validate_api_response_critical(actual, expected, critical_fields, ignore_fields=None):
    """
    API响应验证工具
    :param actual: 实际结构
    :param expected: 预期结构
    :param ignore_fields: 忽略的动态字段列表（默认忽略timestamp、request_id）
    """
    if ignore_fields is None:
        ignore_fields = ['timestamp', 'request_id']
    # 转换JSON字符串为dict（如果需要）
    if isinstance(actual, str):
        actual = json.loads(actual)
    if isinstance(expected, str):
        expected = json.loads(expected)
    # 深度比对（忽略动态字段、数组顺序）
    diff = DeepDiff(
        expected,
        actual,
        ignore_order=True,  # 忽略数组顺序
        exclude_paths=[f"root['{field}']" for field in ignore_fields]  # 忽略动态字段
    )
    # 提取关键差异（仅关注影响业务的字段）
    # critical_fields = ['status', 'name']  # 关键业务字段（可自定义）
    critical_diff = {}
    for change_type, changes in diff.items():
        if change_type in ['values_changed', 'dic_item_added', 'dic_item_removed']:
            for path, detail in changes.items():
                # 检查路径是否包含关键字段
                if any(key in path for key in critical_fields):
                    critical_diff[path] = detail
    return {
        "critical_diff": critical_diff,  # 关键差异（需关注）
        "full_diff": diff  # 完整差异（供调试）
    }


if __name__ == '__main__':
    with open('old.json') as f1, open('new.json') as f2:
        # result = validate_api_response(json.load(f2), json.load(f1))  # 比对所有key
        result = validate_api_response_critical(json.load(f2), json.load(f1), ['status', 'name'])  # 指定关键key字段, 只比对status和name关键字。
        # result = validate_api_response_critical(json.load(f2), json.load(f1), ['status', 'name'], ['timestamp', 'request_id'])  # 指定关键key字段, 只比对status和name关键字。
    print(json.dumps(result['critical_diff'], ensure_ascii=False, indent=2))