import docx
import openpyxl
import requests
import json
from datetime import datetime

# ===================== 配置项 =====================
# 替换为你的通义千问API-KEY（阿里云获取）
DASHSCOPE_API_KEY = "your-dashscope-api-key-here"
# 通义千问API地址（固定）
DASHSCOPE_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# 需求文档路径（Word文件）
WORD_FILE_PATH = "需求文档_登录功能.docx"
# 测试用例Excel保存路径
EXCEL_SAVE_PATH = "测试用例_登录功能_通义千问.xlsx"


# ===================== 核心函数 =====================
def read_word_document(file_path):
    """读取Word文档内容"""
    try:
        doc = docx.Document(file_path)
        full_text = []
        # 读取文档中所有段落
        for para in doc.paragraphs:
            if para.text.strip():  # 跳过空行
                full_text.append(para.text.strip())
        # 拼接所有内容
        requirement_text = "\n".join(full_text)
        if not requirement_text:
            print("Word文档内容为空")
            return None
        return requirement_text
    except FileNotFoundError:
        print(f"未找到Word文件：{file_path}")
        return None
    except Exception as e:
        print(f"读取Word文档失败：{str(e)}")
        return None


def call_qianfan_api(requirement_text):
    """调用通义千问API，将需求文档转换为测试用例"""
    # 构造精准的提示词，确保返回结构化JSON
    prompt = f"""
    请严格按照以下要求将需求文档转换为测试用例：
    1. 测试用例必须包含字段：用例ID、模块、用例名称、前置条件、操作步骤、预期结果、优先级；
    2. 仅返回JSON格式结果，外层为列表，每个元素是测试用例字典，不要额外解释；
    3. 优先级分为：高、中、低；
    4. 用例ID格式：TC_模块名_3位序号（如TC_登录功能_001）；
    5. 操作步骤和预期结果需具体、可执行，符合软件测试规范；
    6. 不要返回任何markdown格式、代码块标识，仅返回纯JSON字符串。

    需求文档内容：
    {requirement_text}
    """

    # 构造通义千问API请求参数
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-turbo",  # 通义千问轻量版，也可换qwen-plus/qwen-max
        "input": {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        "parameters": {
            "result_format": "text",  # 返回文本格式
            "temperature": 0.1,  # 低随机性，保证结果稳定
            "max_tokens": 2000  # 最大返回字符数
        }
    }

    try:
        # 发送请求
        response = requests.post(DASHSCOPE_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()  # 抛出HTTP错误
        result = response.json()

        # 提取AI返回的测试用例JSON
        ai_content = result["output"]["text"].strip()
        # 兼容可能的格式问题（如多余空格、换行）
        ai_content = ai_content.replace("\n", "").replace("\r", "").strip()

        # 解析JSON为测试用例列表
        test_cases = json.loads(ai_content)
        return test_cases

    except json.JSONDecodeError:
        print(f"AI返回的内容不是合法JSON：{ai_content}")
        return None
    except Exception as e:
        print(f"调用通义千问API失败：{str(e)}")
        return None


def save_test_cases_to_excel(test_cases, save_path):
    """将测试用例写入Excel，带格式优化"""
    if not test_cases:
        print("无测试用例数据可保存")
        return

    # 创建工作簿
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "功能测试用例"

    # 定义表头
    headers = ["用例ID", "模块", "用例名称", "前置条件", "操作步骤", "预期结果", "优先级", "创建时间"]
    ws.append(headers)

    # 设置表头样式（加粗、居中、浅灰色背景）
    header_style = openpyxl.styles.Font(bold=True)
    header_alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")
    header_fill = openpyxl.styles.PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")
    for cell in ws[1]:
        cell.font = header_style
        cell.alignment = header_alignment
        cell.fill = header_fill

    # 写入测试用例数据
    create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for case in test_cases:
        row_data = [
            case.get("用例ID", ""),
            case.get("模块", ""),
            case.get("用例名称", ""),
            case.get("前置条件", ""),
            case.get("操作步骤", ""),
            case.get("预期结果", ""),
            case.get("优先级", ""),
            create_time
        ]
        ws.append(row_data)

    # 调整列宽（适配内容长度）
    column_widths = [18, 15, 35, 25, 45, 35, 8, 20]
    for col_idx, width in enumerate(column_widths, 1):
        col_letter = openpyxl.utils.get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width

    # 自动换行（操作步骤/预期结果字段）
    wrap_alignment = openpyxl.styles.Alignment(wrap_text=True, vertical="top")
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        # 操作步骤（第5列）、预期结果（第6列）开启自动换行
        row[4].alignment = wrap_alignment
        row[5].alignment = wrap_alignment

    # 保存Excel
    try:
        wb.save(save_path)
        print(f"✅ 测试用例已成功保存至：{save_path}")
    except PermissionError:
        print(f"❌ 保存失败：{save_path} 文件已被打开，请关闭后重试")
    except Exception as e:
        print(f"❌ 保存Excel失败：{str(e)}")


# ===================== 主程序 =====================
if __name__ == "__main__":
    # 1. 读取Word需求文档
    print("📄 正在读取Word需求文档...")
    requirement_text = read_word_document(WORD_FILE_PATH)
    if not requirement_text:
        exit(1)

    # 2. 调用通义千问API生成测试用例
    print("🤖 正在调用通义千问API生成测试用例...")
    test_cases = call_qianfan_api(requirement_text)
    if not test_cases:
        exit(1)

    # 3. 保存到Excel
    print("💾 正在将测试用例写入Excel...")
    save_test_cases_to_excel(test_cases, EXCEL_SAVE_PATH)