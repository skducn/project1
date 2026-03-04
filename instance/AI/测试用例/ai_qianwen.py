# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-03-4
# Description: 阿里云白练 千问 需求转测试用例
# 火山引擎 - api和费用：https://bailian.console.aliyun.com/cn-beijing/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.afe7133cCn3wfo&tab=demohouse#/api-key
# *****************************************************************

import requests
import json
import pandas as pd
import os
from docx import Document
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

# 从环境变量获取API密钥
# qianwen
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("请在.env文件中设置DASHSCOPE_API_KEY环境变量")


# -------------------------- 配置项（需手动修改，仅3处） --------------------------
# 1. 通义千问API配置（阿里云获取：https://dashscope.aliyun.com/）

# 2. 本地Word需求文档路径（专病库需求规格说明书.docx）
# 获取脚本所在目录的绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 使用相对于脚本所在目录的路径
WORD_FILE_PATH = os.path.join(SCRIPT_DIR, "【专病库】需求规格说明书.docx")  # 替换为实际Word文件路径
# 3. Excel测试用例保存路径
EXCEL_SAVE_PATH = os.path.join(SCRIPT_DIR, "专病库测试用例_自动生成_千问.xlsx") 

OVERWRITE_EXIST_FILE = True  # 是否覆盖已存在的Excel文件

# -------------------------- 读取本地Word文档内容 --------------------------
def read_word_document(word_path):
    """
    读取本地.docx格式的需求文档，提取纯文本内容
    :param word_path: Word文件本地路径
    :return: 文档纯文本内容
    """
    if not os.path.exists(word_path):
        raise FileNotFoundError(f"Word文件不存在：{word_path}，请检查路径是否正确")
    if not word_path.endswith(".docx"):
        raise TypeError("仅支持.docx格式的Word文件，不支持.doc格式")
    
    doc = Document(word_path)
    full_text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():  # 过滤空行
            full_text.append(paragraph.text.strip())
    # 拼接为完整文本，换行分隔
    return "\n".join(full_text)

# -------------------------- 通义千问API调用函数 --------------------------
def call_qianwen_api(prompt, api_key, model="qwen-plus"):
    """
    调用通义千问API生成标准化测试用例
    :param prompt: 生成用例的提示词
    :param api_key: 通义千问API_KEY
    :param model: 模型版本，qwen-plus/qwen-turbo均可
    :return: API返回的测试用例纯文本
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model,
        "input": {"prompt": prompt},
        "parameters": {
            "max_tokens": 20000,  # 足够容纳所有测试用例
            "temperature": 0.01,   # 低温度保证结果精准、结构化
            "top_p": 0.9,  # # 缩小采样范围，避免内容简化
            "result_format": "text",
            "stop": None
        }
    }
    try:
        response = requests.post(
            url="https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8")
        )
        response.raise_for_status()  # 抛出HTTP请求异常
        result = response.json()
        if "output" in result and "text" in result["output"]:
            return result["output"]["text"].strip()
        else:
            raise Exception(f"API返回格式异常，无有效内容：{json.dumps(result, ensure_ascii=False)}")
    except Exception as e:
        raise Exception(f"调用通义千问API失败：{str(e)}")

# -------------------------- 构造API提示词（严格匹配需求） --------------------------
def build_prompt(requirement_text):
    """
    构造通义千问的测试用例生成提示词，明确所有约束规则
    :param requirement_text: Word读取的需求文档纯文本
    :return: 标准化提示词
    """
    prompt = f"""
你是10年经验的医疗软件测试工程师，精通医疗系统功能测试用例设计，现在请严格解析这份专病库管理系统的需求文档，生成符合行业标准的功能测试用例，**仅返回测试用例数据，无任何多余解释、前言、后语**。

### 第一步：先提取核心信息
从需求文档中提取：
1. 所有功能模块、子模块；
2. 每个功能的所有字段/参数名称；
3. 字段数据类型；
4. 全量约束规则（必填/非必填、长度、取值范围、枚举值、格式要求、唯一性等）。

### 第二步：生成测试用例要求（全覆盖，无遗漏）
为每个字段/功能生成**三类测试用例**，必须覆盖所有反向、边界场景：
1. 正向用例：符合所有约束规则的正常、合法、有效数据；
2. 反向用例：必须包含「必填字段空值、非法字符、格式错误、长度越界（过长/过短）、数据类型错误」所有子场景；
3. 边界用例：必须包含「最小长度/最小值、最大长度/最大值、枚举边界（第一个/最后一个值）、临界值」所有子场景。

### 第三步：输出格式强制要求（严格遵守，否则无效）
1. 列固定（顺序不可变）：用例ID|优先级|模块|子模块|前置条件|用例类型|用例检查点|操作步骤|预期结果|备注；
2. 用例ID：从UC001开始自动递增，纯大写+数字，无其他字符；
3. 优先级：仅允许「高」「中」，核心功能（录入/编辑/查询）为高，全局异常场景为中；
4. 用例类型：仅允许「正向用例」「反向用例」「边界用例」；
5. 每行1条测试用例，列之间用「|」分隔，无markdown表格、无缩进、无空行；
6. 用例顺序：专病信息录入功能→专病信息编辑功能→专病精准查询功能→全局异常场景；
7. 语言：纯中文，操作步骤/预期结果贴合系统实际操作，备注简洁明了；
8. 覆盖需求文档中**所有约束规则、异常场景、特殊规则**，无遗漏。

### 需求文档原始内容
{requirement_text}
"""
    return prompt.strip()

# -------------------------- 解析API返回结果为DataFrame --------------------------
def parse_api_result(api_text):
    """
    解析API返回的|分隔用例文本，转为标准化pandas DataFrame，适配Excel保存
    :param api_text: API返回的测试用例纯文本
    :return: 测试用例DataFrame
    """
    # 按行分割，过滤空行和格式错误行
    lines = [line.strip() for line in api_text.split("\n") if line.strip() and "|" in line]
    # 定义固定列名（与要求完全一致）
    columns = ["用例ID", "优先级", "模块", "子模块", "前置条件", "用例类型", "用例检查点", "操作步骤", "预期结果", "备注"]
    # 解析每行数据，清洗空格
    case_data = []
    for line_num, line in enumerate(lines, 1):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) == 10:  # 确保列数正确
            case_data.append(parts)
        else:
            print(f"【警告】跳过第{line_num}行格式错误的用例：{line}")
    # 转为DataFrame并去重、排序
    df = pd.DataFrame(case_data, columns=columns)
    df = df.drop_duplicates(subset=["用例ID"]).sort_values(by="用例ID").reset_index(drop=True)
    if len(df) == 0:
        raise Exception("API返回的测试用例解析后为空，可能是格式错误")
    return df

# -------------------------- 保存测试用例到本地Excel --------------------------
def save_to_excel(df, save_path, overwrite):
    """
    将测试用例DataFrame保存到本地Excel，无索引，支持中文sheet名
    :param df: 测试用例DataFrame
    :param save_path: Excel保存路径
    :param overwrite: 是否覆盖已存在文件
    """
    # 检查文件存在性
    if os.path.exists(save_path) and not overwrite:
        raise FileExistsError(f"Excel文件已存在：{save_path}，请修改路径或设置OVERWRITE_EXIST_FILE=True")
    # 保存Excel（使用openpyxl引擎，支持.xlsx）
    try:
        with pd.ExcelWriter(save_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="专病库功能测试用例", index=False)
        # 验证保存结果并输出信息
        file_size = round(os.path.getsize(save_path) / 1024, 2)
        print(f"✅ Excel文件保存成功！")
        print(f"📁 保存绝对路径：{os.path.abspath(save_path)}")
        print(f"📊 生成测试用例总数：{len(df)} 条")
        print(f"📦 文件大小：{file_size} KB")
    except Exception as e:
        raise Exception(f"保存Excel失败：{str(e)}")

# -------------------------- 主函数：一键执行（读Word→调API→解析→存Excel） --------------------------
if __name__ == "__main__":
    try:
        print("="*60)
        print("📌 专病库测试用例自动生成脚本开始执行...")
        print("="*60)
        # 1. 读取本地Word需求文档
        print(f"\n🔍 正在读取Word文档：{WORD_FILE_PATH}")
        req_text = read_word_document(WORD_FILE_PATH)
        print("✅ Word文档读取完成，共提取字符数：", len(req_text))
        
        # 2. 构造通义千问API提示词
        print("\n📝 正在构造API生成提示词...")
        prompt = build_prompt(req_text)
        
        # 3. 调用通义千问API生成测试用例
        print("\n🚀 正在调用通义千问API生成测试用例...")
        api_result = call_qianwen_api(prompt, DASHSCOPE_API_KEY)
        print("✅ API调用完成，返回用例文本字符数：", len(api_result))
        
        # 4. 解析API返回结果为结构化数据
        print("\n📊 正在解析API返回的测试用例...")
        case_df = parse_api_result(api_result)
        
        # 5. 保存到本地Excel文件
        print(f"\n💾 正在将测试用例保存到Excel：{EXCEL_SAVE_PATH}")
        save_to_excel(case_df, EXCEL_SAVE_PATH, OVERWRITE_EXIST_FILE)
        
        print("\n" + "="*60)
        print("🎉 专病库测试用例自动生成&保存完成！可直接打开Excel使用")
        print("="*60)
    except Exception as e:
        print(f"\n❌ 脚本执行失败：{str(e)}")
        exit(1)