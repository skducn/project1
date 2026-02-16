# -*- coding: utf-8 -*-
# ConversationBufferMemory.py (完整修正版)

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

load_dotenv()


# 自定义简单的对话记忆类（替代ConversationBufferMemory）
class SimpleConversationMemory:
    def __init__(self, memory_key="history", return_messages=True):
        self.memory_key = memory_key
        self.return_messages = return_messages
        self.history = []

    def save_context(self, inputs, outputs):
        """保存对话上下文"""
        # 保存用户输入
        if "input" in inputs:
            self.history.append(HumanMessage(content=inputs["input"]))
        # 保存AI输出
        if "text" in outputs:
            self.history.append(AIMessage(content=outputs["text"]))

    def load_memory_variables(self, inputs):
        """加载记忆变量"""
        if self.return_messages:
            return {self.memory_key: self.history}
        else:
            # 将消息转换为字符串格式
            history_str = ""
            for msg in self.history:
                if isinstance(msg, HumanMessage):
                    history_str += f"Human: {msg.content}\n"
                else:
                    history_str += f"AI: {msg.content}\n"
            return {self.memory_key: history_str}


# 初始化Qwen模型
llm = ChatTongyi(
    model_name="qwen-turbo",
    dashscope_api_key="sk-f3e3d8f64cab416fb028d582533c1e01"
)

# 定义Prompt模板
prompt = ChatPromptTemplate.from_template("""
你是一位贴心的AI助手，现在和用户聊天。
请根据对话历史和最新提问，给出自然、有帮助的回答。

对话历史：
{history}

用户提问：
{input}

请回答：
""")

# 初始化自定义记忆模块
memory = SimpleConversationMemory(memory_key="history", return_messages=False)


# 手动实现类似LLMChain的功能
def chat_with_memory(user_input):
    """带记忆的聊天函数"""
    # 获取历史
    memory_vars = memory.load_memory_variables({})
    history = memory_vars["history"]

    # 构造prompt
    formatted_prompt = prompt.format(history=history, input=user_input)

    # 调用模型
    response = llm.invoke(formatted_prompt)

    # 保存到记忆
    memory.save_context(
        {"input": user_input},
        {"text": response.content}
    )

    return response.content


# 多轮对话测试
def run_multi_turn_conversation():
    print("🚀 带记忆的多轮对话测试")
    print("=" * 40)

    test_inputs = [
        "你好，你是谁？",
        "你能帮我写一个Python Hello World程序吗？",
        "再帮我写一个Java版本的吧！",
        "比较一下这两种语言的特点"
    ]

    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n--- 第{i}轮对话 ---")
        print(f"👤 用户: {user_input}")

        try:
            response = chat_with_memory(user_input)
            print(f"🤖 助手: {response}")

            # 显示当前记忆状态
            memory_vars = memory.load_memory_variables({})
            history_length = len(memory_vars["history"].split('\n')) if memory_vars["history"] else 0
            print(f"📊 历史记录条数: {history_length}")

        except Exception as e:
            print(f"❌ 出错: {e}")
            import traceback
            traceback.print_exc()
            break


if __name__ == "__main__":
    run_multi_turn_conversation()


# /Users/linghuchong/miniconda3/envs/py311/bin/python /Users/linghuchong/Downloads/51/Python/project/instance/AI/Langchain/ConversationBufferMemory2.py
# 🚀 带记忆的多轮对话测试
# ========================================
#
# --- 第1轮对话 ---
# 👤 用户: 你好，你是谁？
# 🤖 助手: 你好！我是Qwen，是阿里巴巴集团旗下的通义实验室自主研发的超大规模语言模型。我可以帮助你解答问题、创作文字、进行多轮对话等等。有什么我可以帮你的吗？😊
# 📊 历史记录条数: 3
#
# --- 第2轮对话 ---
# 👤 用户: 你能帮我写一个Python Hello World程序吗？
# 🤖 助手: 当然可以！下面是一个简单的 Python "Hello, World!" 程序：
#
# ```python
# print("Hello, World!")
# ```
#
# 当你运行这段代码时，它会在屏幕上输出 `Hello, World!`。如果你需要更复杂的例子或者有其他问题，随时告诉我！😊
# 📊 历史记录条数: 11
#
# --- 第3轮对话 ---
# 👤 用户: 再帮我写一个Java版本的吧！
# 🤖 助手: 当然可以！下面是一个简单的 Java "Hello, World!" 程序：
#
# ```java
# public class HelloWorld {
#     public static void main(String[] args) {
#         System.out.println("Hello, World!");
#     }
# }
# ```
#
# 这段代码定义了一个名为 `HelloWorld` 的类，其中包含一个 `main` 方法。当程序运行时，它会输出 `Hello, World!`。如果你需要更复杂的例子或者有其他问题，随时告诉我！😊
# 📊 历史记录条数: 23
#
# --- 第4轮对话 ---
# 👤 用户: 比较一下这两种语言的特点
# 🤖 助手: Python 和 Java 是两种非常流行的编程语言，它们各有特点，适用于不同的场景。以下是它们的一些主要区别和特点：
#
# ### **Python 的特点：**
# 1. **简洁易读**：Python 的语法简洁明了，接近自然语言，使得代码更易于阅读和编写。
# 2. **动态类型**：Python 是动态类型的，变量不需要显式声明类型，这使得开发更加灵活。
# 3. **丰富的库和框架**：Python 有大量现成的库和框架，适合快速开发，比如数据分析（Pandas、NumPy）、人工智能（TensorFlow、PyTorch）等。
# 4. **解释型语言**：Python 是解释型语言，代码可以直接运行，无需编译，调试更方便。
# 5. **跨平台**：Python 可以在多种操作系统上运行，如 Windows、Linux 和 macOS。
#
# ### **Java 的特点：**
# 1. **静态类型**：Java 是静态类型的，变量需要显式声明类型，这有助于在编译时发现错误。
# 2. **面向对象**：Java 是完全面向对象的语言，支持封装、继承和多态等特性。
# 3. **强类型和安全性**：Java 的类型系统更严格，运行时安全性更高，适合大型企业级应用。
# 4. **编译型语言**：Java 需要先编译成字节码，然后在 Java 虚拟机（JVM）上运行，性能较好。
# 5. **跨平台**：Java 通过“一次编写，到处运行”的理念实现跨平台，但需要 JVM 支持。
#
# ### **适用场景：**
# - **Python** 更适合快速开发、脚本编写、数据科学、机器学习等领域。
# - **Java** 更适合大型企业级应用、安卓开发、后端服务等对性能和安全性要求较高的场景。
#
# 如果你有具体的需求或想了解某个方面的细节，可以告诉我，我会进一步帮你分析！😊
# 📊 历史记录条数: 45
#
# Process finished with exit code 0