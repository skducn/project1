# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-03-4
# Description: 豆包api 需求转测试用例
# 火山引擎 - 费用：https://console.volcengine.com/finance/fund/recharge
# 火山引擎 - api key：https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D
# 1，新增APIkey
# 2，开通管理 - Doubao-pro-32k
# 3，在线推理 - 传教推理接入点 - 生成接入点ID，如ep-20260304122201-mbd96
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
# 豆包
bytedance_API_KEY = os.getenv("bytedance_API_KEY")
if not bytedance_API_KEY:
    raise ValueError("请在.env文件中设置DASHSCOPE_API_KEY环境变量")


# -------------------------- 配置项 --------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORD_FILE_PATH = os.path.join(SCRIPT_DIR, "【专病库】需求规格说明书.docx")
EXCEL_SAVE_PATH = os.path.join(SCRIPT_DIR, "专病库测试用例_自动生成_豆包.xlsx") 
OVERWRITE_EXIST_FILE = True

# -------------------------- 读取Word --------------------------
def read_word_document(word_path):
    """
    读取本地.docx格式的需求文档，提取纯文本内容
    
    Args:
        word_path (str): Word文件本地路径
    
    Returns:
        str: 文档纯文本内容，按段落换行分隔
    
    Raises:
        FileNotFoundError: 当Word文件不存在时
        TypeError: 当文件格式不是.docx时
    """
    if not os.path.exists(word_path):
        raise FileNotFoundError(f"Word文件不存在：{word_path}")
    if not word_path.endswith(".docx"):
        raise TypeError("仅支持.docx格式")
    
    doc = Document(word_path)
    full_text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            full_text.append(paragraph.text.strip())
    return "\n".join(full_text)

# -------------------------- 修正后的豆包API调用函数 --------------------------
def call_doubao_api(prompt, api_key, model="ep-20260304122201-mbd96"):
    """
    适配新版仅API Key鉴权的豆包API调用
    
    Args:
        prompt (str): 测试用例生成提示词
        api_key (str): 火山引擎豆包API-KEY
        model (str, optional): 模型版本或接入点ID，默认为"ep-20260304122201-mbd96"
    
    Returns:
        str: 豆包API返回的测试用例纯文本
    
    Raises:
        Exception: 当API调用失败时
    """
    headers = {
        "Content-Type": "application/json",
        # 仅保留API Key，格式为 Bearer + 空格 + API Key
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 16384,
        "temperature": 0.01,
        "top_p": 0.1
    }
    try:
        # 确认接口地址与地域匹配（cn-beijing正确）
        response = requests.post(
            url="https://ark.cn-beijing.volces.com/api/v3/chat/completions",
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            # 新增：超时设置 + 关闭SSL验证（避免环境拦截）
            timeout=120,
            verify=False
        )
        # 打印详细响应（便于排查）
        print(f"API响应状态码：{response.status_code}")
        print(f"API响应内容：{response.text}")
        
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"API HTTP错误：{e}，响应内容：{response.text}")
    except Exception as e:
        raise Exception(f"调用豆包API失败：{str(e)}")

# -------------------------- 提示词构造/解析/保存逻辑不变 --------------------------
def build_prompt(requirement_text):
    """
    构造豆包API的测试用例生成提示词，明确所有约束规则
    
    Args:
        requirement_text (str): Word读取的需求文档纯文本
    
    Returns:
        str: 标准化提示词，包含测试用例生成的详细要求和约束
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

def parse_api_result(api_text):
    """
    解析API返回的|分隔用例文本，转为标准化pandas DataFrame，适配Excel保存
    
    Args:
        api_text (str): API返回的测试用例纯文本
    
    Returns:
        pandas.DataFrame: 测试用例DataFrame，包含用例ID、优先级、模块等字段
    
    Raises:
        Exception: 当解析后的测试用例为空时
    """
    lines = [line.strip() for line in api_text.split("\n") if line.strip() and "|" in line]
    columns = ["用例ID", "优先级", "模块", "子模块", "前置条件", "用例类型", "用例检查点", "操作步骤", "预期结果", "备注"]
    case_data = []
    for line_num, line in enumerate(lines, 1):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) == 10:
            case_data.append(parts)
        else:
            print(f"【警告】跳过第{line_num}行格式错误的用例：{line}")
    df = pd.DataFrame(case_data, columns=columns)
    df = df.drop_duplicates(subset=["用例ID"]).sort_values(by="用例ID").reset_index(drop=True)
    if len(df) == 0:
        raise Exception("API返回的测试用例解析后为空")
    return df

def save_to_excel(df, save_path, overwrite):
    """
    将测试用例DataFrame保存到本地Excel，无索引，支持中文sheet名
    
    Args:
        df (pandas.DataFrame): 测试用例DataFrame
        save_path (str): Excel保存路径
        overwrite (bool): 是否覆盖已存在文件
    
    Raises:
        FileExistsError: 当Excel文件已存在且overwrite为False时
        Exception: 当保存Excel失败时
    """
    if os.path.exists(save_path) and not overwrite:
        raise FileExistsError(f"Excel文件已存在：{save_path}")
    try:
        with pd.ExcelWriter(save_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="专病库功能测试用例", index=False)
        file_size = round(os.path.getsize(save_path) / 1024, 2)
        print(f"✅ Excel文件保存成功！")
        print(f"📁 保存绝对路径：{os.path.abspath(save_path)}")
        print(f"📊 生成测试用例总数：{len(df)} 条")
        print(f"📦 文件大小：{file_size} KB")
    except Exception as e:
        raise Exception(f"保存Excel失败：{str(e)}")

# -------------------------- 主函数 --------------------------
if __name__ == "__main__":
    try:
        print("="*60)
        print("📌 专病库测试用例自动生成脚本开始执行...")
        print("="*60)
        
        print(f"\n🔍 正在读取Word文档：{WORD_FILE_PATH}")
        req_text = read_word_document(WORD_FILE_PATH)
        print("✅ Word文档读取完成，共提取字符数：", len(req_text))
        
        print("\n📝 正在构造API生成提示词...")
        prompt = build_prompt(req_text)
        
        print("\n🚀 正在调用豆包API生成测试用例...")
        api_result = call_doubao_api(prompt, bytedance_API_KEY)
        print("✅ API调用完成，返回用例文本字符数：", len(api_result))
        
        print("\n📊 正在解析API返回的测试用例...")
        case_df = parse_api_result(api_result)
        
        print(f"\n💾 正在将测试用例保存到Excel：{EXCEL_SAVE_PATH}")
        save_to_excel(case_df, EXCEL_SAVE_PATH, OVERWRITE_EXIST_FILE)
        
        print("\n" + "="*60)
        print("🎉 专病库测试用例自动生成&保存完成！可直接打开Excel使用")
        print("="*60)
    except Exception as e:
        print(f"\n❌ 脚本执行失败：{str(e)}")
        exit(1)