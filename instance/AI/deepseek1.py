# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2025-1-25
# Description: deepseek
# https://platform.deepseek.com/usage  # 查看余款
# https://api-docs.deepseek.com/zh-cn/guides/reasoning_model  # 查看R1模型

# 要使用 `curl` 实现 DeepSeek API 的流式响应（Server-Sent Events, SSE），需确保 API 支持流式传输，并按照以下步骤操作：
#
# ---
#
# ### 1. **基础示例**
# ```bash
# curl https://api.deepseek.com/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
#   -d '{
#     "model": "deepseek-chat",
#     "messages": [{"role": "user", "content": "你的问题"}],
#     "stream": true  # 关键参数：启用流式
#   }' \
#   --no-buffer  # 禁用 curl 的缓冲，实时显示数据
# ```
#
# ---
#
# ### 2. **解析流式响应**
# 响应数据通常是多个 `data:` 开头的 JSON 块，需逐行解析：
#
# ```bash
# curl ... | while IFS= read -r line; do
#   if [[ $line == data:* ]]; then
#     content=$(echo "$line" | sed 's/^data: //' | jq -r '.choices[0].delta.content // empty')
#     printf "%s" "$content"
#   fi
# done
# ```
# ********************************************************************************************************************

from openai import OpenAI

text = input("提问: \n")
print("正在AI思考中...")

# client = OpenAI(api_key="mNF21RSnIIDP7lCzObF9w9JB", base_url="https://api.openai.com")
client = OpenAI(api_key="sk-e2bf2354c1924fbeb55c41e4d7bd151d", base_url="https://api.deepseek.com")

# 使用 stream=True 启用流式响应，默认情况下，返回的响应会被解析为一个 list，
# https://api-docs.deepseek.com/zh-cn/
# * deepseek-chat 模型已全面升级为 DeepSeek-V3，接口不变。 通过指定 model='deepseek-chat' 即可调用 DeepSeek-V3。
# * deepseek-reasoner 是 DeepSeek 最新推出的推理模型 DeepSeek-R1。通过指定 model='deepseek-reasoner'，即可调用 DeepSeek-R1。
response = client.chat.completions.create(
    # model="deepseek-chat",
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": text},
    ],
    stream=True  # 启用流式响应
)

print("AI 回答:")
# 逐行显示响应内容
for chunk in response:
    if chunk.choices[0].delta.content:
        # 检查是否有内容
        print(chunk.choices[0].delta.content, end="", flush=True)
print() # 换行

