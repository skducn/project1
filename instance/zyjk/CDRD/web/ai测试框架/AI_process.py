# -*- coding: utf-8 -*-
import asyncio
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser

print("✓ Agent, Browser 导入成功")


# 浏览器配置管理器
class BrowserManager:
    def __init__(self):
        self.browser = None
        self.is_initialized = False

    async def initialize_browser(self):
        """初始化浏览器"""
        if not self.is_initialized:
            try:
                print("🚀 正在启动可视化浏览器...")
                self.browser = Browser(
                    headless=False,  # 显示浏览器窗口
                    disable_security=True
                )
                self.is_initialized = True
                print("✅ 浏览器启动成功")
                return self.browser
            except Exception as e:
                print(f"❌ 浏览器启动失败: {e}")
                # 降级到Playwright
                return await self._fallback_to_playwright()
        return self.browser

    async def _fallback_to_playwright(self):
        """降级到Playwright方案"""
        print("⚠️  降级到Playwright方案...")
        try:
            from playwright.async_api import async_playwright

            self.p = await async_playwright().start()
            self.browser = await self.p.chromium.launch(
                headless=False,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            print("✅ Playwright浏览器启动成功")
            return self.browser
        except Exception as e:
            print(f"❌ Playwright启动失败: {e}")
            return None

    async def close_browser(self):
        """关闭浏览器"""
        try:
            if self.browser:
                if hasattr(self.browser, 'close'):
                    await self.browser.close()
                print("🔚 浏览器已关闭")
            if hasattr(self, 'p') and self.p:
                await self.p.stop()
        except Exception as e:
            print(f"关闭浏览器时出错: {e}")
        finally:
            self.browser = None
            self.is_initialized = False


# 全局浏览器管理器
browser_manager = BrowserManager()


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
    """增强版AI处理函数 - 确保浏览器打开"""
    try:
        print(f"\n🎯 开始执行任务: {case_desc}")

        # 获取浏览器实例
        browser = await browser_manager.initialize_browser()
        if not browser:
            return {"status": "error", "message": "浏览器启动失败"}

        print("🖥️  浏览器窗口已打开，请观察操作步骤...")
        print("=" * 50)

        # 创建Agent
        agent = Agent(
            llm=wrapped_llm,
            browser=browser,
            message_context="""你正在进行WEB软件自动化测试，请：
            1. 仔细分析测试需求
            2. 逐步执行每个操作步骤
            3. 在每步操作后给出清晰的说明
            4. 最终返回明确的测试结果（通过/不通过）""",
            task=case_desc
        )

        print("✅ Agent创建成功，开始运行...")
        print("🔄 AI正在思考和执行操作...")
        print("=" * 50)

        # 执行任务（添加超时保护）
        try:
            history = await asyncio.wait_for(agent.run(max_steps=20), timeout=600)  # 10分钟超时
        except asyncio.TimeoutError:
            print("⏰ 任务执行超时")
            return {"status": "timeout", "message": "任务执行时间过长"}
        except Exception as e:
            print(f"❌ Agent执行异常: {e}")
            return {"status": "error", "message": f"执行异常: {str(e)}"}

        # 获取详细的执行历史
        steps = history.steps if hasattr(history, 'steps') else []
        print("\n📋 执行步骤详情:")
        print("-" * 30)
        for i, step in enumerate(steps, 1):
            action = getattr(step, 'action', '未知操作') if hasattr(step, 'action') else "未知操作"
            result = getattr(step, 'result', '无结果') if hasattr(step, 'result') else "无结果"
            print(f"步骤 {i}: {action}")
            if result and result != "None":
                print(f"  结果: {result}")
            print()

        result = history.final_result()
        print("=" * 50)
        print("🎉 任务执行完成！")

        # 智能结果解析
        if isinstance(result, str):
            # 关键：根据内容判断测试结果
            if any(keyword in result for keyword in ['失败', '错误', 'fail', 'error']):
                return {
                    "status": "failed",
                    "message": result,
                    "details": "测试执行失败",
                    "steps_count": len(steps),
                    "execution_time": "completed"
                }
            else:
                return {
                    "status": "success",
                    "message": result,
                    "details": "测试执行成功",
                    "steps_count": len(steps),
                    "execution_time": "completed"
                }
        else:
            return {
                "status": "success",
                "message": str(result),
                "details": "测试完成",
                "steps_count": len(steps),
                "execution_time": "completed"
            }

    except Exception as e:
        print(f"❌ 处理函数执行出错: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


# 简单的浏览器演示函数
async def browser_demo():
    """浏览器功能演示"""
    try:
        print("🧪 执行浏览器功能演示...")

        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            page = await browser.new_page()

            print("🌐 打开百度首页...")
            await page.goto("https://www.baidu.com", wait_until="networkidle")

            print("🔍 执行简单搜索...")
            await page.wait_for_selector("#kw", timeout=10000)
            search_box = page.locator("#kw")
            await search_box.fill("AI自动化测试")

            search_button = page.locator("#su")
            await search_button.click()

            await page.wait_for_load_state("networkidle", timeout=30000)
            title = await page.title()

            print(f"✅ 搜索完成，页面标题: {title}")

            await page.screenshot(path="demo_result.png", full_page=True)
            print("📸 演示结果已保存为 demo_result.png")

            # 保持浏览器打开10秒以便观察
            print("⏳ 保持浏览器打开10秒以便观察...")
            await asyncio.sleep(10)
            await browser.close()

            return {
                "status": "success",
                "title": title,
                "screenshot": "demo_result.png"
            }

    except Exception as e:
        print(f"❌ 浏览器演示失败: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}


# 主函数
async def main():
    print("=" * 60)
    print("🚀 AI自动化测试系统 - 带浏览器可视化")
    print("=" * 60)

    # 首先验证浏览器功能
    print("\n第一步：验证浏览器基础功能...")
    demo_result = await browser_demo()
    print(f"浏览器演示结果: {demo_result}")

    if demo_result.get("status") == "success":
        print("\n第二步：运行AI自动化测试...")
        test_cases = [
            "请访问百度搜索'人工智能'，然后告诉我搜索结果页面的标题",
            "请访问GitHub官网，然后截图保存"
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- 测试用例 {i} ---")
            result = await process_by_ai(test_case)
            print(f"结果: {result}")
            await asyncio.sleep(2)  # 间隔时间
    else:
        print("\n⚠️  浏览器基础功能验证失败")

    # 清理资源
    await browser_manager.close_browser()
    print("\n🔚 程序执行完毕")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  用户中断程序执行")
        asyncio.run(browser_manager.close_browser())
    except Exception as e:
        print(f"💥 程序执行出错: {e}")
        asyncio.run(browser_manager.close_browser())
