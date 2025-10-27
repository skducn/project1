# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025-10-27
# Description: 阿里云百炼
# https://bailian.console.aliyun.com/#/home
# https://bailian.console.aliyun.com/&tab=doc?tab=model#/efm/model_experience_center/text
# 模型服务 - 密钥管理 - 创建api
# sk-fa71f3cbbd304313b4ba271981f65661

# 模型广场 - 选择 qwen3-vl-plus
# ********************************************************************************************************************
import os
from openai import OpenAI
from dotenv import load_dotenv





# text = input("提问: \n")
# print("正在AI思考中...")
#
# # client = OpenAI(api_key="mNF21RSnIIDP7lCzObF9w9JB", base_url="https://api.openai.com")
# client = OpenAI(api_key="sk-e2bf2354c1924fbeb55c41e4d7bd151d", base_url="https://api.deepseek.com")
#
# # 使用 stream=True 启用流式响应，默认情况下，返回的响应会被解析为一个 list，
# # https://api-docs.deepseek.com/zh-cn/
# # * ds-chat 模型已全面升级为 DeepSeek-V3，接口不变。 通过指定 model='ds-chat' 即可调用 DeepSeek-V3。
# # * ds-reasoner 是 DeepSeek 最新推出的推理模型 DeepSeek-R1。通过指定 model='ds-reasoner'，即可调用 DeepSeek-R1。
# response = client.chat.completions.create(
#     # model="ds-chat",
#     model="ds-reasoner",
#     messages=[
#         {"role": "system", "content": "you are a helpful assistant"},
#         {"role": "user", "content": text},
#     ],
#     stream=True  # 启用流式响应
# )
#
# print("AI 回答:")
# # 逐行显示响应内容
# for chunk in response:
#     if chunk.choices[0].delta.content:
#         # 检查是否有内容
#         print(chunk.choices[0].delta.content, end="", flush=True)
# print() # 换行
#
