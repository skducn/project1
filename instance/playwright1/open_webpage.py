# 导入 Playwright 同步 API
from playwright.sync_api import sync_playwright


def open_basic_webpage():
    # 启动 Playwright 上下文
    with sync_playwright() as p:
        # 启动 Chromium 浏览器（适配 macOS 12 的参数）
        browser = p.chromium.launch(
            args=["--no-sandbox", "--disable-setuid-sandbox"],
            headless=False,  # 显示浏览器窗口（方便查看）
            slow_mo=500  # 慢动作（延迟 500ms，便于观察操作）
        )
        # 创建新的浏览器页面
        page = browser.new_page()

        # 打开指定网页（比如百度）
        page.goto("https://www.baidu.com")

        # 等待页面完全加载（可选，确保内容加载完成）
        page.wait_for_load_state("networkidle")  # 等待网络请求完成

        # 打印网页标题
        print("网页标题：", page.title())

        # 可选：截图保存（验证页面是否正确打开）
        page.screenshot(path="baidu_screenshot.png")

        # 关闭浏览器
        browser.close()


if __name__ == "__main__":
    open_basic_webpage()