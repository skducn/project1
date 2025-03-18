# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description: BERT2
# 请使用NLP工具如BERT解析需求文档，设计一个实例。
# pip install transformers torch
# ********************************************************************************************************************
from transformers import BertTokenizer, BertForTokenClassification
import torch

from transformers import logging

logging.set_verbosity_warning()

# 加载预训练的BERT模型和分词器
model_name = "bert-base-chinese"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForTokenClassification.from_pretrained(model_name)
# model = BertForTokenClassification.from_pretrained("bert-base-chinese", num_labels=num_labels)



# 将模型移动到 GPU（如果有）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 定义标签
labels = ["O", "B-FUNC", "I-FUNC", "B-SCEN", "I-SCEN", "B-INPUT", "I-INPUT", "B-OUTPUT", "I-OUTPUT"]

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

# 检查文本长度
if len(tokenizer.tokenize(requirement_text)) > 512:
    print("输入文本过长，请截断或拆分文本！")
    exit()

# 分词并转换为模型输入
inputs = tokenizer(requirement_text, return_tensors="pt", truncation=True, padding=True)
inputs = {k: v.to(device) for k, v in inputs.items()}  # 移动到 GPU

# 使用BERT模型进行预测
with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)

# 打印模型输出形状
print("模型输出形状:", outputs.logits.shape)

# 将预测结果转换为标签
predicted_labels = [labels[i] if i < len(labels) else "O" for i in predictions[0].tolist()]

# 提取关键信息
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
extracted_info = {"功能模块": [], "用户场景": [], "输入条件": [], "预期结果": []}

current_label = None
current_phrase = []

for token, label in zip(tokens, predicted_labels):
    if token in ["[CLS]", "[SEP]", "[PAD]"]:
        continue
    if label.startswith("B-"):
        if current_label and current_phrase:
            extracted_info[current_label].append("".join(current_phrase))
        current_label = label[2:]
        current_phrase = [token]
    elif label.startswith("I-"):
        current_phrase.append(token)
    else:
        if current_label and current_phrase:
            extracted_info[current_label].append("".join(current_phrase))
        current_label = None
        current_phrase = []

# 打印解析结果
for key, values in extracted_info.items():
    print(f"{key}:")
    for value in values:
        print(f"  - {value}")
