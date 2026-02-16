# 验证 Python 版本
import sys
print("Python 版本：", sys.version)

# 验证 Playwright
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(
        args=["--no-sandbox", "--disable-setuid-sandbox"],
        headless=False
    )
    print("Playwright Chromium 启动成功！")
    browser.close()

# 验证 fake-useragent
from fake_useragent import UserAgent
ua = UserAgent()
print("随机生成的 User-Agent：", ua.chrome)