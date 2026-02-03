# 验证Playwright+Chromium是否安装成功
from playwright.sync_api import sync_playwright

def verify_chromium():
    with sync_playwright() as p:
        # 启动Chromium（无头模式）
        browser = p.chromium.launch(headless=True)
        # 新建页面
        page = browser.new_page()
        # 访问百度
        page.goto('https://www.baidu.com')
        # 打印页面标题
        print('页面标题：', page.title())
        # 关闭浏览器
        browser.close()
        print('✅ Chromium手动安装成功，可正常使用！')

if __name__ == '__main__':
    verify_chromium()