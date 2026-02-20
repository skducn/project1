# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2026-2-20
# Description: 生成测试用例
# pip install python-docx openai pandas
# 一、整体流程
# 准备：安装依赖、获取 API Key
# 读取 docx 并提取需求文本
# 构造 Prompt（指定用例格式、字段）
# 调用大模型 API 生成用例
# 解析返回结果并导出（CSV/Excel）

#  其他大模型适配
# OpenAI：base_url="https://api.openai.com/v1"，model="gpt-3.5-turbo"
# 通义千问：base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"，model="qwen-turbo"
# 智谱 GLM：base_url="https://open.bigmodel.cn/api/paas/v4/"，model="glm-4"

# 进阶改进
# 按章节提取：只读取 “需求说明” 章节，避免无关内容
# 批量处理：遍历文件夹下所有 docx
# 导出 Excel：用 pandas 直接存 .xlsx
# 对接测试平台：生成后自动上传到禅道 / TestLink

# docx 读取不全
# 用 python-docx 遍历所有段落 + 表格
# 或改用 docx2txt 更鲁棒：pip install docx2txt

# Prompt 优化（最重要）
# 明确字段：序号、模块、标题、前置、步骤、预期、优先级
# 强制格式：只输出 CSV，不要解释
# 场景要求：正常 / 异常 / 边界
# 示例：可在 Prompt 里加 1–2 条示例用例，让模型更贴合你的规范
# ********************************************************************************************************************

import os
import pandas as pd
from docx import Document
from openai import OpenAI

# -------------------------- 配置区 --------------------------
# 1. 填入你的 API Key
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
BASE_URL = "https://api.deepseek.com/v1"

# 2. 你的 docx 路径
DOCX_PATH = "需求文档.docx"

# 3. 测试用例输出格式（可自定义）
CASE_TEMPLATE = """
请根据以下需求，生成结构化测试用例，严格按 CSV 格式输出，包含表头：
序号,模块,用例标题,前置条件,测试步骤,预期结果,优先级

需求内容：
{requirement_text}

要求：
- 覆盖正常、异常、边界场景
- 步骤清晰、结果明确
- 优先级：P0/P1/P2
- 不要额外解释，只输出 CSV 内容
"""


# ------------------------------------------------------------

def read_docx(file_path: str) -> str:
    """读取 docx 并返回纯文本"""
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())
    return "\n".join(full_text)


def generate_test_cases(requirement: str) -> str:
    """调用 API 生成测试用例"""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    prompt = CASE_TEMPLATE.format(requirement_text=requirement)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # 降低随机性，保证格式稳定
    )
    return response.choices[0].message.content.strip()


def save_to_csv(case_text: str, output_path: str = "测试用例.csv"):
    """将返回的 CSV 文本保存为文件"""
    lines = [line.strip() for line in case_text.split("\n") if line.strip()]
    # 简单处理：按逗号分割（复杂场景可加 csv 模块）
    data = [line.split(",") for line in lines]
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 测试用例已保存到：{output_path}")


if __name__ == "__main__":
    # 1. 读取需求
    req_text = read_docx(DOCX_PATH)
    print("📄 已读取需求文档，开始生成用例...")

    # 2. 生成用例
    case_result = generate_test_cases(req_text)
    print("\n📝 生成的测试用例：")
    print(case_result)

    # 3. 保存
    save_to_csv(case_result)