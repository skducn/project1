# -*- coding: utf-8 -*-
import asyncio
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser

print("✓ Agent, Browser 导入成功")

# 创建浏览器实例
browser = Browser(
    headless=False,
    disable_security=True
)


# 创建兼容的LLM包装器类
class CompatibleLLM:
    def __init__(self, llm):
        self._llm = llm
        self.provider = "qwen"
        self.model = "qwen-plus"

    def __getattr__(self, name):
        return getattr(self._llm, name)

    def __call__(self, *args, **kwargs):
        return self._llm(*args, **kwargs)

    def invoke(self, *args, **kwargs):
        return self._llm.invoke(*args, **kwargs)

    def generate(self, *args, **kwargs):
        return self._llm.generate(*args, **kwargs)


# 创建LLM
llm = ChatOpenAI(
    api_key="sk-f3e3d8f64cab416fb028d582533c1e01",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus"
)

wrapped_llm = CompatibleLLM(llm)

print("检查包装后的LLM...")
print("Provider属性:", getattr(wrapped_llm, 'provider', '未找到'))
print("Model属性:", getattr(wrapped_llm, 'model', '未找到'))


async def process_by_ai(case_desc):
    try:
        print(f"\n🎯 开始执行任务: {case_desc}")

        agent = Agent(
            llm=wrapped_llm,
            browser=browser,
            message_context="你正在进行WEB软件自动化测试，请仔细执行用户的要求",
            task=case_desc
        )

        print("✅ Agent创建成功，开始运行...")
        print("🔄 AI正在思考和执行操作，请稍候...")

        # 修正：移除不支持的timeout参数，只保留max_steps
        history = await agent.run(max_steps=3)

        result = history.final_result()
        print("🎉 任务执行完成！")
        return result

    except asyncio.TimeoutError:
        print("⏰ 任务执行超时")
        return {"status": "timeout", "message": "任务执行时间过长"}
    except Exception as e:
        print(f"❌ Agent执行出错: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


# 异步Playwright测试版本
async def simple_test():
    """使用异步Playwright进行简单测试"""
    try:
        print("🧪 执行异步Playwright简单测试...")

        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser_instance = await p.chromium.launch(
                headless=False,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            page = await browser_instance.new_page()

            print("🌐 打开百度...")
            await page.goto("https://www.baidu.com", wait_until="networkidle")

            print("🔍 执行搜索...")
            await page.wait_for_selector("#chat-textarea", timeout=10000)
            search_box = page.locator("#chat-textarea")
            await search_box.fill("人工智能测试")

            search_button = page.locator("#chat-submit-button")
            await search_button.click()

            await page.wait_for_load_state("networkidle", timeout=30000)
            title = await page.title()

            print(f"✅ 搜索完成，页面标题: {title}")

            await page.screenshot(path="baidu_search_result.png", full_page=True)
            print("📸 结果已保存为 baidu_search_result.png")

            await browser_instance.close()

            return {
                "status": "success",
                "title": title,
                "screenshot": "baidu_search_result.png"
            }

    except Exception as e:
        print(f"❌ 异步Playwright测试失败: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


# 主程序
if __name__ == "__main__":
    async def main():
        try:
            print("=" * 60)
            print("🚀 Web自动化测试系统")
            print("=" * 60)

            # 运行异步Playwright测试
            print("\n📋 运行异步Playwright基础测试...")
            playwright_result = await simple_test()
            print(f"Playwright测试结果: {playwright_result}")

            # 如果基础测试成功，再尝试AI版本
            if playwright_result.get("status") == "success":
                print("\n🤖 现在尝试browser_use AI版本...")
                ai_result = await process_by_ai("请访问百度搜索人工智能")
                print("=" * 60)
                print("🤖 AI版本执行结果:")
                print(ai_result)
            else:
                print("\n⚠️  基础测试失败，建议检查环境配置")

        except KeyboardInterrupt:
            print("\n⚠️  用户中断了程序执行")
        except Exception as e:
            print(f"💥 主程序出错: {e}")
            import traceback
            traceback.print_exc()


    asyncio.run(main())
