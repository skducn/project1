# coding: utf-8
# ********************************************************
# Author     : John
# Date       : 2025.3.12
# Description: spacy
# ********************************************************
import spacy
from spacy.matcher import Matcher

# 加载SpaCy的预训练模型
nlp = spacy.load("zh_core_web_sm")  # 使用中文模型

# 需求文档内容
requirement_text = """
需求文档：
1. 用户登录功能：
   - 用户输入正确的用户名和密码后，点击“登录”按钮，应跳转到主页。
   - 用户名为空时，点击“登录”按钮，应提示“用户名不能为空”。
   - 密码为空时，点击“登录”按钮，应提示“密码不能为空”。
2. 订单支付功能：
   - 用户选择支付方式为“信用卡”，输入正确的信用卡信息后，点击“支付”按钮，应显示“支付成功”。
   - 用户未选择支付方式时，点击“支付”按钮，应提示“请选择支付方式”。
"""

# 创建一个Matcher对象用于匹配功能模块
# matcher = Matcher(nlp.vocab)
# pattern = [{"TEXT": {"REGEX": r"^\d+\.\s*"}}]  # 匹配以数字开头的功能模块
# matcher.add("MODULE_PATTERN", [pattern])

# 解析需求文档
doc = nlp(requirement_text)

# 提取功能模块
module_spans = matcher(doc)
modules = []
for match_id, start, end in module_spans:
    span = doc[start:end]
    modules.append(span.text.strip())

# 初始化变量
test_cases = []
current_module = None


# 定义一个函数来提取输入条件和预期结果
def extract_input_and_output(sentence):
    if "应" in sentence:
        parts = sentence.split("应")
        input_condition = parts[0].strip()
        expected_result = parts[1].strip()
    elif "时" in sentence:
        parts = sentence.split("时")
        input_condition = parts[0].strip() + "时"
        expected_result = parts[1].strip()
    else:
        input_condition = sentence
        expected_result = "无明确预期结果"
    return input_condition, expected_result


# 遍历每个句子，提取关键信息
for sent in doc.sents:
    text = sent.text.strip()

    print("text >", text)
    print("modules >", modules)
    # 判断是否是新的功能模块
    for module in modules:
        if module in text:
            current_module = module.split("。")[0].strip()
            break

    # 提取用户场景、输入条件和预期结果
    if "用户" in text or "点击" in text:
        scenario = text
        input_condition, expected_result = extract_input_and_output(scenario)

        # 添加到测试用例列表
        if current_module and input_condition and expected_result:
            test_cases.append({
                "功能模块": current_module,
                "用户场景": scenario,
                "输入条件": input_condition,
                "预期结果": expected_result
            })

# 打印解析结果
# print(test_cases)
for case in test_cases:
    print(f"功能模块: {case['功能模块']}")
    print(f"用户场景: {case['用户场景']}")
    print(f"输入条件: {case['输入条件']}")
    print(f"预期结果: {case['预期结果']}")
    print("-" * 40)