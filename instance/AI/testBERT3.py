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

# 1. 加载预训练的分词器和模型
model_name = "bert-base-chinese"
tokenizer = BertTokenizer.from_pretrained(model_name)

# 假设我们有 5 个标签：O（非实体）, B-DATE, I-DATE, B-LOC, I-LOC, B-TASK, I-TASK
num_labels = 7
model = BertForTokenClassification.from_pretrained(model_name, num_labels=num_labels)

# 2. 准备输入文本
text = "请在下周五之前完成项目报告，并在会议室A进行演示。"

# 3. 将文本转换为模型输入格式
inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
input_ids = inputs["input_ids"]
attention_mask = inputs["attention_mask"]

# 4. 模型推理
model.eval()
with torch.no_grad():
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    logits = outputs.logits

# 5. 获取预测的标签
predictions = torch.argmax(logits, dim=-1).squeeze().tolist()

# 6. 将预测的标签映射回实体
# 假设标签映射如下：
# 0: O, 1: B-DATE, 2: I-DATE, 3: B-LOC, 4: I-LOC, 5: B-TASK, 6: I-TASK
id2label = {
    0: "O",
    1: "B-DATE",
    2: "I-DATE",
    3: "B-LOC",
    4: "I-LOC",
    5: "B-TASK",
    6: "I-TASK",
}

# 7. 将 token IDs 转换回文本
tokens = tokenizer.convert_ids_to_tokens(input_ids.squeeze().tolist())

# 8. 提取实体
entities = []
current_entity = None
for token, label_id in zip(tokens, predictions):
    label = id2label[label_id]
    if label != "O":
        if label.startswith("B-"):
            if current_entity:
                entities.append(current_entity)
            current_entity = {"text": token, "label": label[2:]}
        elif label.startswith("I-"):
            if current_entity:
                current_entity["text"] += token.replace("##", "")
    else:
        if current_entity:
            entities.append(current_entity)
            current_entity = None

# 9. 打印结果
print("提取的实体：")
for entity in entities:
    print(f"文本: {entity['text']}, 标签: {entity['label']}")