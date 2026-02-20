import docx
import openpyxl
import requests, os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


# 从环境变量获取API密钥
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("请在.env文件中设置DASHSCOPE_API_KEY环境变量")


# -------------------------- 第一步：解析Doc需求文档 --------------------------
def read_doc_requirement(doc_path):
    """读取doc/docx需求文档，提取文本内容"""
    doc = docx.Document(doc_path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())
    # 合并文本，只保留核心需求（过滤空行、无关内容）
    requirement_text = "\n".join(full_text)
    print(f"解析到需求文本：\n{requirement_text[:500]}...")
    return requirement_text


# -------------------------- 第二步：调用免费LLM生成测试用例 --------------------------
def generate_test_cases_with_llm(requirement_text):
    """调用通义千问免费API生成结构化测试用例"""
    # 1. 替换为你的通义千问API Key（免费获取：https://dashscope.aliyun.com/）
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    # 2. 标准化Prompt（全球最优的测试用例生成Prompt）
    prompt = f"""
    你是资深Web测试工程师，现在需要根据以下需求文档生成测试用例，要求：
    1. 仅针对Web项目，覆盖功能、边界、异常场景；
    2. 用例格式：序号|用例名称|前置条件|测试步骤|预期结果|优先级（P1/P2/P3）；
    3. 每个核心功能至少生成5条用例，优先级合理分配；
    4. 只输出用例内容，不要多余解释；
    5. 需求文档内容：
    {requirement_text}
    6. 额外输出每个用例对应的Playwright自动化脚本（Python），格式：用例名称|脚本代码；
    """

    # 3. 调用API生成用例
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-turbo",  # 通义千问免费版模型
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {"result_format": "text"}
    }

    # try:
    #     response = requests.post(url, json=data, headers=headers)
    #     response.raise_for_status()
    #     # 提取生成的用例文本
    #     test_cases_text = response.json()["output"]["choices"][0]["message"]["content"]
    #     print(f"生成的测试用例：\n{test_cases_text}")
    #     return test_cases_text
    # except Exception as e:
    #     print(f"LLM调用失败：{e}")
    #     return ""

        # ... existing code ...
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        # 调试：打印完整的响应内容
        print(f"API响应状态码: {response.status_code}")
        print(f"API响应内容: {response.text}")

        response_json = response.json()

        # 检查响应结构并提取内容
        test_cases_text = ""

        # 方法1：尝试标准的choices格式
        if "output" in response_json and "choices" in response_json["output"]:
            test_cases_text = response_json["output"]["choices"][0]["message"]["content"]
        # 方法2：尝试直接的text格式
        elif "output" in response_json and "text" in response_json["output"]:
            test_cases_text = response_json["output"]["text"]
        # 方法3：尝试其他可能的格式
        else:
            # 打印响应结构帮助调试
            print(f"响应结构: {list(response_json.keys())}")
            if "output" in response_json:
                print(f"output结构: {list(response_json['output'].keys())}")
            raise KeyError("无法找到期望的响应格式（choices或text）")

        print(f"生成的测试用例：\n{test_cases_text}")
        return test_cases_text
    except KeyError as e:
        print(f"响应格式错误：{e}")
        print(f"完整响应: {response.text}")
        return ""
    except Exception as e:
        print(f"LLM调用失败：{e}")
        return ""
    # ... existing code ...


# -------------------------- 第三步：用例写入Excel（可导入禅道） --------------------------
def write_cases_to_excel(test_cases_text, excel_path="test_cases.xlsx"):
    """将生成的用例写入Excel，适配禅道导入格式"""
    wb = openpyxl.Workbook()
    ws = wb.active
    # 禅道通用用例表头（可直接导入）
    ws.append(["序号", "用例名称", "前置条件", "测试步骤", "预期结果", "优先级"])

    # 解析LLM生成的用例文本，按行写入
    lines = test_cases_text.strip().split("\n")
    for line in lines:
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 6:
                ws.append([
                    parts[0].strip(),  # 序号
                    parts[1].strip(),  # 用例名称
                    parts[2].strip(),  # 前置条件
                    parts[3].strip(),  # 测试步骤
                    parts[4].strip(),  # 预期结果
                    parts[5].strip()  # 优先级
                ])

    wb.save(excel_path)
    print(f"测试用例已写入Excel：{excel_path}")


# -------------------------- 主流程：Doc→用例→Excel --------------------------
if __name__ == "__main__":
    # 替换为你的需求文档路径
    doc_path = "专病库需求文档.docx"
    # 1. 解析Doc
    requirement = read_doc_requirement(doc_path)
    # 2. 生成用例
    test_cases = generate_test_cases_with_llm(requirement)
    # 3. 写入Excel
    if test_cases:
        write_cases_to_excel(test_cases)


# 结果：
# /Users/linghuchong/miniconda3/envs/py311/bin/python /Users/linghuchong/Downloads/51/Python/project/instance/AI/测试用例/gen_test_cases1.py
# 解析到需求文本：
# 专病库需求文档
# 核心原则：结构化分区、语义清晰、字段标准化、无冗余信息，贴合通义千问对“明确指令+固定格式”的识别偏好，让大模型快速提取“模块-功能-规则-约束”，生成规范测试用例（适配通义千问API调用，无需额外优化Prompt）。
# 说明：本格式可直接在Word（docx）中编辑，所有标题层级、字段名称严格沿用，避免自定义修改；内容填写时，按“示例”规范表述，减少模糊化、口语化描述，确保测试用例覆盖正常/异常/边界场景。
# 一、文档封面（必选，统一格式）
# （居中对齐，字体加粗，无需多余装饰，核心信息明确，便于大模型快速识别文档主体）
# 标题：【专病库】需求规格说明书（测试用例生成专用）
# 副标题：适配通义千问API，结构化需求提取
# 补充信息（左对齐，下一行）：版本号：V1.0 | 编制人：金浩| 编制日期：2026-2-20
# 二、文档目录（必选，自动生成）
# 操作方式：Word中“引用”→“目录”→“自动目录1”，确保所有一级/二级/三级标题自动收录，便于大模型定位各模块需求，避免遗漏。
# 三、核心需求总览（必选，全局说明）
# （简洁概括项目核心目标、测试范围，避免冗余，让大模型快速明确整体需求...
# API响应状态码: 200
# API响应内容: {"output":{"finish_reason":"stop","text":"1|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入有效用户名、手机号、密码、确认密码；3. 点击“注册”按钮|注册成功，跳转至登录页面，数据库新增用户信息|P1  \n2|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入无效用户名（小于4个字符）；3. 点击“注册”按钮|提示“用户名长度不足，至少4个字符”，不跳转，不新增数据|P2  \n3|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入已存在的用户名；3. 点击“注册”按钮|提示“该用户名已存在，请更换”，不跳转，不新增数据|P1  \n4|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入手机号格式错误（如：1234567890）；3. 点击“注册”按钮|提示“请输入正确的11位手机号”，不跳转，不新增数据|P2  \n5|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入密码与确认密码不一致；3. 点击“注册”按钮|提示“两次密码输入不一致，请重新输入”，不跳转，不新增数据|P2  \n专病库-用户注册功能|async def test_register_valid_user(page):  \n    await page.goto(\"https://example.com/register\")  \n    await page.fill(\"#username\", \"testuser\")  \n    await page.fill(\"#phone\", \"13800138000\")  \n    await page.fill(\"#password\", \"Test123@\")  \n    await page.fill(\"#confirm_password\", \"Test123@\")  \n    await page.click(\"#submit\")  \n    assert await page.url() == \"https://example.com/login\"  \n\n6|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入正确用户名和密码；3. 点击“登录”按钮|登录成功，跳转至首页，显示用户信息|P1  \n7|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入错误用户名或密码；3. 点击“登录”按钮|提示“用户名或密码错误，请重新输入”，不跳转|P2  \n8|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入空用户名；3. 点击“登录”按钮|提示“请填写用户名”，不跳转|P2  \n9|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入空密码；3. 点击“登录”按钮|提示“请填写密码”，不跳转|P2  \n10|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入手机号代替用户名；3. 点击“登录”按钮|提示“用户名格式错误”，不跳转|P2  \n专病库-用户登录功能|async def test_login_valid_user(page):  \n    await page.goto(\"https://example.com/login\")  \n    await page.fill(\"#username\", \"testuser\")  \n    await page.fill(\"#password\", \"Test123@\")  \n    await page.click(\"#submit\")  \n    assert await page.url() == \"https://example.com/home\"  \n\n11|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 填写完整病历信息；3. 点击“提交”按钮|病历信息保存成功，提示“提交成功”，刷新页面显示最新数据|P1  \n12|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 不填写必填项（如患者姓名）；3. 点击“提交”按钮|提示“请填写必填项”，不提交数据|P2  \n13|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 输入超长文本（如超过200字符）；3. 点击“提交”按钮|提示“输入内容过长，最多200字符”，不提交数据|P2  \n14|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 选择非法日期格式（如“2026/02/30”）；3. 点击“提交”按钮|提示“日期格式错误”，不提交数据|P2  \n15|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 输入非数字字符到数字字段（如年龄）；3. 点击“提交”按钮|提示“请输入数字”，不提交数据|P2  \n专病库-病历录入功能|async def test_add_medical_record_valid(page):  \n    await page.goto(\"https://example.com/medical-record\")  \n    await page.fill(\"#patient_name\", \"张三\")  \n    await page.fill(\"#age\", \"30\")  \n    await page.fill(\"#diagnosis\", \"高血压\")  \n    await page.fill(\"#date\", \"2026-02-20\")  \n    await page.click(\"#submit\")  \n    assert \"提交成功\" in await page.text_content(\"#message\")  \n\n16|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 输入合法患者姓名；3. 点击“查询”按钮|显示匹配的病历列表，包含患者信息、诊断结果等|P1  \n17|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 输入无效患者姓名（不存在）；3. 点击“查询”按钮|提示“未找到相关病历记录”|P2  \n18|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 输入超长患者姓名（超过50字符）；3. 点击“查询”按钮|提示“输入内容过长，最多50字符”，不执行查询|P2  \n19|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 不输入任何查询条件；3. 点击“查询”按钮|提示“请输入查询条件”，不执行查询|P2  \n20|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 输入特殊字符（如“<script>”）作为查询条件；3. 点击“查询”按钮|提示“输入内容包含非法字符”，不执行查询|P2  \n专病库-病历查询功能|async def test_search_medical_records(page):  \n    await page.goto(\"https://example.com/medical-record/search\")  \n    await page.fill(\"#search_input\", \"张三\")  \n    await page.click(\"#search_button\")  \n    assert \"张三\" in await page.text_content(\"#results\")  \n\n21|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 修改部分信息；5. 点击“保存”按钮|病历信息更新成功，提示“保存成功”|P1  \n22|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 不修改任何信息；5. 点击“保存”按钮|提示“无修改内容，无需保存”|P2  \n23|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 输入非法字符（如“<script>”）；5. 点击“保存”按钮|提示“输入内容包含非法字符”，不保存数据|P2  \n24|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 输入超长文本（超过200字符）；5. 点击“保存”按钮|提示“输入内容过长，最多200字符”，不保存数据|P2  \n25|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 选择非法日期格式；5. 点击“保存”按钮|提示“日期格式错误”，不保存数据|P2  \n专病库-病历修改功能|async def test_edit_medical_record(page):  \n    await page.goto(\"https://example.com/medical-record/edit\")  \n    await page.fill(\"#diagnosis\", \"糖尿病\")  \n    await page.click(\"#save_button\")  \n    assert \"保存成功\" in await page.text_content(\"#message\")  \n\n26|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 确认删除|病历信息被删除，提示“删除成功”|P1  \n27|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 取消删除操作|不执行删除操作，返回病历页面|P2  \n28|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 输入非法字符在确认框中|提示“请输入有效确认信息”，不执行删除|P2  \n29|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 不输入任何确认信息；5. 点击“确定”|提示“请输入确认信息”，不执行删除|P2  \n30|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 选择非当前用户创建的病历|提示“您无权删除此病历”，不执行删除|P2  \n专病库-病历删除功能|async def test_delete_medical_record(page):  \n    await page.goto(\"https://example.com/medical-record/delete\")  \n    await page.click(\"#delete_button\")  \n    await page.fill(\"#confirmation\", \"确认\")  \n    await page.click(\"#confirm\")  \n    assert \"删除成功\" in await page.text_content(\"#message\")  \n\n31|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 添加新角色；3. 分配权限；4. 点击“保存”按钮|角色添加成功，权限分配生效|P1  \n32|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 不填写角色名称；3. 点击“保存”按钮|提示“请填写角色名称”，不保存|P2  \n33|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 输入非法角色名称（如“<script>”）；3. 点击“保存”按钮|提示“角色名称包含非法字符”，不保存|P2  \n34|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 输入超长角色名称（超过50字符）；3. 点击“保存”按钮|提示“角色名称过长，最多50字符”，不保存|P2  \n35|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 未选择任何权限；3. 点击“保存”按钮|提示“请选择至少一个权限”，不保存|P2  \n专病库-权限管理功能|async def test_add_role_with_permissions(page):  \n    await page.goto(\"https://example.com/roles\")  \n    await page.fill(\"#role_name\", \"医生\")  \n    await page.check(\"#permission_1\")  \n    await page.check(\"#permission_2\")  \n    await page.click(\"#save_button\")  \n    assert \"角色添加成功\" in await page.text_content(\"#message\")  \n\n36|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 选择导出范围（如全部）；3. 点击“导出”按钮|生成CSV文件，提示“导出成功”，可下载|P1  \n37|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 未选择导出范围；3. 点击“导出”按钮|提示“请选择导出范围”，不执行导出|P2  \n38|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 选择非法时间范围（如未来日期）；3. 点击“导出”按钮|提示“时间范围无效”，不执行导出|P2  \n39|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 选择导出范围后，点击“取消”按钮|不执行导出操作，返回上一页|P2  \n40|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 选择导出范围后，网络中断；3. 点击“导出”按钮|提示“网络异常，请检查网络连接后重试”，不执行导出|P2  \n专病库-数据导出功能|async def test_export_data(page):  \n    await page.goto(\"https://example.com/export\")  \n    await page.select(\"#export_range\", \"all\")  \n    await page.click(\"#export_button\")  \n    assert \"导出成功\" in await page.text_content(\"#message\")"},"usage":{"input_tokens":2005,"output_tokens":3269,"prompt_tokens_details":{"cached_tokens":0},"total_tokens":5274},"request_id":"dedc44f4-2e21-4f52-8c25-b819d2c75581"}
# 生成的测试用例：
# 1|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入有效用户名、手机号、密码、确认密码；3. 点击“注册”按钮|注册成功，跳转至登录页面，数据库新增用户信息|P1
# 2|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入无效用户名（小于4个字符）；3. 点击“注册”按钮|提示“用户名长度不足，至少4个字符”，不跳转，不新增数据|P2
# 3|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入已存在的用户名；3. 点击“注册”按钮|提示“该用户名已存在，请更换”，不跳转，不新增数据|P1
# 4|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入手机号格式错误（如：1234567890）；3. 点击“注册”按钮|提示“请输入正确的11位手机号”，不跳转，不新增数据|P2
# 5|专病库-用户注册功能|用户未登录|1. 打开注册页面；2. 输入密码与确认密码不一致；3. 点击“注册”按钮|提示“两次密码输入不一致，请重新输入”，不跳转，不新增数据|P2
# 专病库-用户注册功能|async def test_register_valid_user(page):
#     await page.goto("https://example.com/register")
#     await page.fill("#username", "testuser")
#     await page.fill("#phone", "13800138000")
#     await page.fill("#password", "Test123@")
#     await page.fill("#confirm_password", "Test123@")
#     await page.click("#submit")
#     assert await page.url() == "https://example.com/login"
#
# 6|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入正确用户名和密码；3. 点击“登录”按钮|登录成功，跳转至首页，显示用户信息|P1
# 7|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入错误用户名或密码；3. 点击“登录”按钮|提示“用户名或密码错误，请重新输入”，不跳转|P2
# 8|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入空用户名；3. 点击“登录”按钮|提示“请填写用户名”，不跳转|P2
# 9|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入空密码；3. 点击“登录”按钮|提示“请填写密码”，不跳转|P2
# 10|专病库-用户登录功能|用户未登录|1. 打开登录页面；2. 输入手机号代替用户名；3. 点击“登录”按钮|提示“用户名格式错误”，不跳转|P2
# 专病库-用户登录功能|async def test_login_valid_user(page):
#     await page.goto("https://example.com/login")
#     await page.fill("#username", "testuser")
#     await page.fill("#password", "Test123@")
#     await page.click("#submit")
#     assert await page.url() == "https://example.com/home"
#
# 11|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 填写完整病历信息；3. 点击“提交”按钮|病历信息保存成功，提示“提交成功”，刷新页面显示最新数据|P1
# 12|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 不填写必填项（如患者姓名）；3. 点击“提交”按钮|提示“请填写必填项”，不提交数据|P2
# 13|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 输入超长文本（如超过200字符）；3. 点击“提交”按钮|提示“输入内容过长，最多200字符”，不提交数据|P2
# 14|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 选择非法日期格式（如“2026/02/30”）；3. 点击“提交”按钮|提示“日期格式错误”，不提交数据|P2
# 15|专病库-病历录入功能|用户已登录|1. 进入病历录入页面；2. 输入非数字字符到数字字段（如年龄）；3. 点击“提交”按钮|提示“请输入数字”，不提交数据|P2
# 专病库-病历录入功能|async def test_add_medical_record_valid(page):
#     await page.goto("https://example.com/medical-record")
#     await page.fill("#patient_name", "张三")
#     await page.fill("#age", "30")
#     await page.fill("#diagnosis", "高血压")
#     await page.fill("#date", "2026-02-20")
#     await page.click("#submit")
#     assert "提交成功" in await page.text_content("#message")
#
# 16|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 输入合法患者姓名；3. 点击“查询”按钮|显示匹配的病历列表，包含患者信息、诊断结果等|P1
# 17|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 输入无效患者姓名（不存在）；3. 点击“查询”按钮|提示“未找到相关病历记录”|P2
# 18|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 输入超长患者姓名（超过50字符）；3. 点击“查询”按钮|提示“输入内容过长，最多50字符”，不执行查询|P2
# 19|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 不输入任何查询条件；3. 点击“查询”按钮|提示“请输入查询条件”，不执行查询|P2
# 20|专病库-病历查询功能|用户已登录|1. 进入病历查询页面；2. 输入特殊字符（如“<script>”）作为查询条件；3. 点击“查询”按钮|提示“输入内容包含非法字符”，不执行查询|P2
# 专病库-病历查询功能|async def test_search_medical_records(page):
#     await page.goto("https://example.com/medical-record/search")
#     await page.fill("#search_input", "张三")
#     await page.click("#search_button")
#     assert "张三" in await page.text_content("#results")
#
# 21|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 修改部分信息；5. 点击“保存”按钮|病历信息更新成功，提示“保存成功”|P1
# 22|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 不修改任何信息；5. 点击“保存”按钮|提示“无修改内容，无需保存”|P2
# 23|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 输入非法字符（如“<script>”）；5. 点击“保存”按钮|提示“输入内容包含非法字符”，不保存数据|P2
# 24|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 输入超长文本（超过200字符）；5. 点击“保存”按钮|提示“输入内容过长，最多200字符”，不保存数据|P2
# 25|专病库-病历修改功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“编辑”按钮；4. 选择非法日期格式；5. 点击“保存”按钮|提示“日期格式错误”，不保存数据|P2
# 专病库-病历修改功能|async def test_edit_medical_record(page):
#     await page.goto("https://example.com/medical-record/edit")
#     await page.fill("#diagnosis", "糖尿病")
#     await page.click("#save_button")
#     assert "保存成功" in await page.text_content("#message")
#
# 26|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 确认删除|病历信息被删除，提示“删除成功”|P1
# 27|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 取消删除操作|不执行删除操作，返回病历页面|P2
# 28|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 输入非法字符在确认框中|提示“请输入有效确认信息”，不执行删除|P2
# 29|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 不输入任何确认信息；5. 点击“确定”|提示“请输入确认信息”，不执行删除|P2
# 30|专病库-病历删除功能|用户已登录|1. 进入病历查询页面；2. 查找已有病历；3. 点击“删除”按钮；4. 选择非当前用户创建的病历|提示“您无权删除此病历”，不执行删除|P2
# 专病库-病历删除功能|async def test_delete_medical_record(page):
#     await page.goto("https://example.com/medical-record/delete")
#     await page.click("#delete_button")
#     await page.fill("#confirmation", "确认")
#     await page.click("#confirm")
#     assert "删除成功" in await page.text_content("#message")
#
# 31|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 添加新角色；3. 分配权限；4. 点击“保存”按钮|角色添加成功，权限分配生效|P1
# 32|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 不填写角色名称；3. 点击“保存”按钮|提示“请填写角色名称”，不保存|P2
# 33|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 输入非法角色名称（如“<script>”）；3. 点击“保存”按钮|提示“角色名称包含非法字符”，不保存|P2
# 34|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 输入超长角色名称（超过50字符）；3. 点击“保存”按钮|提示“角色名称过长，最多50字符”，不保存|P2
# 35|专病库-权限管理功能|管理员已登录|1. 进入权限管理页面；2. 未选择任何权限；3. 点击“保存”按钮|提示“请选择至少一个权限”，不保存|P2
# 专病库-权限管理功能|async def test_add_role_with_permissions(page):
#     await page.goto("https://example.com/roles")
#     await page.fill("#role_name", "医生")
#     await page.check("#permission_1")
#     await page.check("#permission_2")
#     await page.click("#save_button")
#     assert "角色添加成功" in await page.text_content("#message")
#
# 36|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 选择导出范围（如全部）；3. 点击“导出”按钮|生成CSV文件，提示“导出成功”，可下载|P1
# 37|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 未选择导出范围；3. 点击“导出”按钮|提示“请选择导出范围”，不执行导出|P2
# 38|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 选择非法时间范围（如未来日期）；3. 点击“导出”按钮|提示“时间范围无效”，不执行导出|P2
# 39|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 选择导出范围后，点击“取消”按钮|不执行导出操作，返回上一页|P2
# 40|专病库-数据导出功能|用户已登录|1. 进入数据导出页面；2. 选择导出范围后，网络中断；3. 点击“导出”按钮|提示“网络异常，请检查网络连接后重试”，不执行导出|P2
# 专病库-数据导出功能|async def test_export_data(page):
#     await page.goto("https://example.com/export")
#     await page.select("#export_range", "all")
#     await page.click("#export_button")
#     assert "导出成功" in await page.text_content("#message")
# 测试用例已写入Excel：test_cases.xlsx
#
# Process finished with exit code 0