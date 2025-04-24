# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025.3.12
# Description: BERT
# 请使用NLP工具如BERT解析需求文档，设计一个实例。
# pip install transformers torch

# 报错：OSError: We couldn't connect to 'https://huggingface.co' to load this file, couldn't find it in the cached files and it looks like facebook/bart-large-mnli is not the path to a directory containing a file named config.json.
# Checkout your internet connection or see how to run the library in offline mode at 'https://huggingface.co/docs/transformers/installation#offline-mode'.
# https://blog.csdn.net/weixin_48321427/article/details/145042238
# 二、我的解决办法
# 用的镜像：https://hf-mirror.com/
# 点进去这个镜像网站，里面有四种解决办法，我相信总有一种适合你嘞
# HF_ENDPOINT=https://hf-mirror.com python your_script.py

# https://hf-mirror.com/

# RuntimeError: Failed to import transformers.models.bart.modeling_tf_bart because of the following error (look up to see its traceback):
# Your currently installed version of Keras is Keras 3, but this is not yet supported in Transformers. Please install the backwards-compatible tf-keras package with `pip install tf-keras`.
# ********************************************************************************************************************

### **步骤2：加载预训练模型**
# 使用Hugging Face的`pipeline`加载零样本分类模型（底层基于BERT架构）：

from transformers import pipeline

# 加载零样本分类模型（使用NLI训练的BERT变体）
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


### **步骤3：定义需求文档示例**
# 假设需求文档包含以下内容：
requirements = [
    "系统应允许用户通过指纹登录。",
    "系统应在0.5秒内响应请求。",
    "用户最多可同时上传10个文件。",
    "界面需符合WCAG 2.0无障碍标准。"
]


### **步骤4：定义候选标签**
# 设定需求类型分类的候选标签：
candidate_labels = ["功能需求", "非功能需求"]

### **步骤5：执行分类并输出结果**
for req in requirements:
    result = classifier(req, candidate_labels, multi_label=False)
    print(f"需求：'{req}'\n分类结果：{result['labels'][0]}（置信度：{result['scores'][0]:.2f}）\n")