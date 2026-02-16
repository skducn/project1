from playwright.sync_api import sync_playwright
import time


def open_and_interact_webpage():
    with sync_playwright() as p:
        # 启动浏览器，添加更多参数确保兼容性
        browser = p.chromium.launch(
            args=[
                "--no-sandbox",  # 适配 macOS 12 权限
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ],
            headless=False,
            timeout=60000  # 增加启动超时时间
        )
        page = browser.new_page()

        # 设置页面加载超时时间
        page.set_default_timeout(30000)  # 30秒

        try:
            # 打开百度
            print("正在打开百度...")
            page.goto("https://www.baidu.com", wait_until="domcontentloaded")

            # 方法1：使用更宽松的等待条件
            print("等待搜索框加载...")
            search_box = page.wait_for_selector("#chat-textarea", state="attached", timeout=10000)

            if search_box:
                print("搜索框已找到，开始输入内容...")
                # 在搜索框输入内容
                search_box.fill("Playwright Python 使用教程")

                # 等待搜索按钮可点击
                search_button = page.wait_for_selector("#chat-submit-button", state="visible", timeout=5000)
                if search_button:
                    print("点击搜索按钮...")
                    search_button.click()
                else:
                    # 如果找不到按钮，直接按回车
                    print("按回车键搜索...")
                    search_box.press("Enter")

                # 等待搜索结果加载
                print("等待搜索结果加载...")
                page.wait_for_load_state("networkidle", timeout=30000)

                # 打印搜索结果标题
                title = page.title()
                print(f"搜索结果页标题：{title}")

                # 可选：截图保存
                page.screenshot(path="search_result.png")
                print("已保存搜索结果截图")
            else:
                print("警告：未能找到搜索框元素")
                # 尝试打印页面源码进行调试
                print("页面标题:", page.title())
                print("当前URL:", page.url())

        except Exception as e:
            print(f"发生错误: {e}")
            # 出错时截图以便调试
            page.screenshot(path="error_screenshot.png")
            print("错误截图已保存为 error_screenshot.png")

        finally:
            # 等待几秒让用户看到结果
            time.sleep(3)
            # 关闭浏览器
            browser.close()


if __name__ == "__main__":
    open_and_interact_webpage()
