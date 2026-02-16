# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2026-2-16
# Description: 使用playwright进行XPath定位
# 需求gitlab：http://192.168.0.241/cdrd_product_doc/product_doc
# *****************************************************************
from playwright.sync_api import sync_playwright

def xpath_locator_demo():
    with sync_playwright() as p:
        # 启动浏览器（适配 macOS 12）
        browser = p.chromium.launch(
            args=["--no-sandbox", "--disable-setuid-sandbox"],
            headless=False,
            slow_mo=800  # 慢动作，便于观察
        )
        page = browser.new_page()

        # 打开百度首页
        page.goto("http://192.168.0.243:8083/login?redirect=/index")
        # 等待页面加载完成
        page.wait_for_load_state("networkidle")

        # ========== 场景1：通过 XPath 定位搜索框并输入内容 ==========
        # 定位 id 为 kw 的输入框（百度搜索框）
        search_box = page.locator('xpath=//*[@placeholder="请输入登录账号"]')
        # 等待元素可见（避免定位到但不可操作）
        search_box.wait_for(state="visible")
        # 输入内容
        search_box.fill("admin")

        search_box = page.locator('xpath=//*[@placeholder="请输入密码"]')
        # 等待元素可见（避免定位到但不可操作）
        search_box.wait_for(state="visible")
        # 输入内容
        search_box.fill("Qa@123456")


        # ========== 场景2：通过 XPath 定位搜索按钮并点击 ==========
        # 定位 id 为 su 的按钮（百度搜索按钮）
        # search_btn = page.locator('xpath=//button[@class="el-button el-button--primary el-button--large is-disabled"]')
        search_btn = page.locator('xpath=//button[contains(@class, "el-button--primary") and contains(@class, "el-button--large")]')
        search_btn.click()

        # # ========== 场景3：通过文本内容定位元素（示例：定位"新闻"链接） ==========
        # # 先返回搜索页（方便演示）
        # page.goto("https://www.baidu.com")
        # # 定位文本为"新闻"的a标签
        # news_link = page.locator('xpath=//a[text()="新闻"]')
        # # 获取元素文本（验证定位成功）
        # print("定位到的链接文本：", news_link.text_content())
        # # 点击新闻链接
        # news_link.click()
        #
        # # ========== 场景4：通过包含文本定位元素 ==========
        # # 定位包含"百度"的span标签（示例）
        # baidu_span = page.locator('xpath=//span[contains(text(), "百度")]')
        # if baidu_span.is_visible():
        #     print("定位到包含'百度'的span元素")

        # ========== 备用写法：page.xpath()（返回元素列表） ==========
        # 注意：page.xpath() 返回元素列表，需遍历或取索引
        # input_elements = page.xpath('//input')
        # print(f"页面中找到 {len(input_elements)} 个input标签")

        # 关闭浏览器
        # browser.close()


if __name__ == "__main__":
    xpath_locator_demo()