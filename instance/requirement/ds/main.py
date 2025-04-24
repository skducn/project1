# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-4-2
# Description: # DeepSeek + Python 提效测试用例生成落地
# http://www.51testing.com/html/98/n-7804598.html
# ***************************************************************u**
# 档中的重要信息。
# 步骤1：获取临时授权码（联系客服获取）
# import requests
# requests.get("https://pypi.deepseek.com", verify=True)  # 无异常则证书可信

# import deepseek
# print(deepseek.__file__)
import deepseek_coder
print(deepseek_coder.__version__)  # 应输出版本号（如0.3.2）


# from deepseek import DeepSeek
from deepseek.api import DeepSeek
# 初始化 DeepSeek
deepseek = DeepSeek(config_path="config.yaml")
# 解析需求文档
def parse_requirements(requirement_text):
    """
    使用 DeepSeek 分析需求文档并提取关键点
    """
    parsed_results = deepseek.query(requirement_text)
    return parsed_results

# 示例需求文档
requirement_text = """
用户输入正确的用户名和密码后，系统应成功登录。
超过 3 次登录失败，系统应锁定账户。
"""

parsed_results = parse_requirements(requirement_text)
# 输出解析结果
print("需求解析结果：")
for result in parsed_results:
    print(f"关键点：{result['title']}")