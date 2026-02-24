from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://192.168.0.243:8083/login?redirect=/index")
    page.get_by_placeholder("请输入登录账号").click()
    page.get_by_placeholder("请输入登录账号").fill("admin")
    page.get_by_placeholder("请输入密码").click()
    page.get_by_placeholder("请输入密码").fill("Qa@123456")
    page.get_by_role("button", name="登 录").click()
    page.get_by_text("系统管理").click()
    page.get_by_role("link", name="角色管理").click()
    page.get_by_role("row", name="1 4 2025-08-06 16:40:18 编辑 删除").get_by_role("button").first.click()
    page.get_by_placeholder("请输入角色名称").click()
    page.get_by_placeholder("请输入角色名称").fill("777")
    page.get_by_placeholder("请输入权限字符").click()
    page.get_by_placeholder("请输入权限字符").click()
    page.get_by_placeholder("请输入内容").click()
    page.get_by_placeholder("请输入内容").fill("888")
    page.get_by_role("button", name="保 存").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
