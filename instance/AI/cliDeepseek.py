# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025-1-25
# Description: deepseek cli模式
# https://platform.deepseek.com/usage  # 查看余款
# https://api-docs.deepseek.com/zh-cn/guides/reasoning_model  # 查看R1模型
# ********************************************************************************************************************

from openai import OpenAI
import sys, os
# text = input("提问: \n")
# print("正在AI思考中...")

api_key = os.getenv("sk-e2bf2354c1924fbeb55c41e4d7bd151d")
# client = OpenAI(api_key="mNF21RSnIIDP7lCzObF9w9JB", base_url="https://api.openai.com")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# 使用 stream=True 启用流式响应，默认情况下，返回的响应会被解析为一个 list，
# https://api-docs.deepseek.com/zh-cn/
# * deepseek-chat 模型已全面升级为 DeepSeek-V3，接口不变。 通过指定 model='deepseek-chat' 即可调用 DeepSeek-V3。
# * deepseek-reasoner 是 DeepSeek 最新推出的推理模型 DeepSeek-R1。通过指定 model='deepseek-reasoner'，即可调用 DeepSeek-R1。
response = client.chat.completions.create(
    # model="deepseek-chat",
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": sys.argv[1]},
    ],
    stream=True  # 启用流式响应
)

# print("AI 回答:")
# 逐行显示响应内容
for chunk in response:
    if chunk.choices[0].delta.content:
        # 检查是否有内容
        print(chunk.choices[0].delta.content, end="", flush=True)
print() # 换行

