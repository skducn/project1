# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description: BERT2
# 请使用NLP工具如BERT解析需求文档，设计一个实例。
# pip install transformers torch
# ********************************************************************************************************************
from transformers import (
    BertTokenizerFast,
    BertForTokenClassification,
    Trainer,
    TrainingArguments,
)
from datasets import Dataset
import torch

# 1. 加载预训练的分词器和模型
model_name = "bert-base-chinese"
tokenizer = BertTokenizerFast.from_pretrained(model_name)

# 假设我们有 5 个标签：O（非实体）, B-DATE, I-DATE, B-LOC, I-LOC, B-TASK, I-TASK
label_list = ["O", "B-DATE", "I-DATE", "B-LOC", "I-LOC", "B-TASK", "I-TASK"]
num_labels = len(label_list)
model = BertForTokenClassification.from_pretrained(model_name, num_labels=num_labels)

# 2. 准备数据集
# 假设我们有一个简单的数据集
data = {
    "tokens": [
        ["请", "在", "下", "周", "五", "之前", "完成", "项目", "报告", "，", "并", "在", "会议", "室", "A", "进行", "演示", "。"],
        ["明天", "下午", "3", "点", "在", "办公室", "开会", "。"],
    ],
    "labels": [
        [0, 0, 1, 2, 2, 0, 5, 6, 6, 0, 0, 0, 3, 4, 4, 0, 0, 0],
        [1, 2, 0, 0, 0, 3, 4, 0],
    ],
}

# 将数据转换为 Hugging Face Dataset 格式
dataset = Dataset.from_dict(data)

# 3. 数据预处理函数
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"],
        truncation=True,
        padding=True,
        is_split_into_words=True,  # 确保输入已经是分词的
    )

    labels = []
    for i, label in enumerate(examples["labels"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # 获取每个 token 对应的单词索引
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # 特殊 token（如 [CLS], [SEP]）的标签设为 -100
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])  # 新单词的第一个 token
            else:
                label_ids.append(label[word_idx])  # 同一个单词的其他 token
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# 对数据集进行预处理
tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)

# 4. 设置训练参数
training_args = TrainingArguments(
    output_dir="./results",          # 模型保存路径
    evaluation_strategy="epoch",     # 每个 epoch 评估一次
    learning_rate=2e-5,              # 学习率
    per_device_train_batch_size=8,   # 训练批次大小
    per_device_eval_batch_size=8,    # 评估批次大小
    num_train_epochs=3,              # 训练 epoch 数
    weight_decay=0.01,               # 权重衰减
    save_strategy="epoch",           # 每个 epoch 保存模型
    logging_dir="./logs",            # 日志目录
    logging_steps=10,                # 每 10 步记录一次日志
)

# 5. 定义 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,  # 实际使用时，建议使用单独的验证集
)

# 6. 训练模型
trainer.train()

# 7. 保存模型
model.save_pretrained("./ner_model")
tokenizer.save_pretrained("./ner_model")

# 8. 加载模型进行推理
model = BertForTokenClassification.from_pretrained("./ner_model")
tokenizer = BertTokenizerFast.from_pretrained("./ner_model")

# 9. 推理示例
text = "请在下周五之前完成项目报告，并在会议室A进行演示。"
inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
with torch.no_grad():
    logits = model(**inputs).logits
predictions = torch.argmax(logits, dim=-1).squeeze().tolist()

# 将预测的标签映射回实体
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze().tolist())
entities = []
current_entity = None
for token, label_id in zip(tokens, predictions):
    if label_id != -100:
        label = label_list[label_id]
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

# 打印结果
print("提取的实体：")
for entity in entities:
    print(f"文本: {entity['text']}, 标签: {entity['label']}")