from playwright.sync_api import Playwright, sync_playwright, expect


def run_playwright():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        test_data = {"role_name": "555", "remark": "1234"}

        page.goto("http://192.168.0.243:8083/login?redirect=/index")
        page.get_by_placeholder("请输入登录账号").click()
        page.get_by_placeholder("请输入登录账号").fill("admin")
        page.get_by_placeholder("请输入密码").click()
        page.get_by_placeholder("请输入密码").fill("Qa@123456")
        page.get_by_role("button", name="登 录").click()
        page.get_by_text("系统管理").click()
        page.get_by_role("link", name="角色管理").click()
        page.get_by_role("row", name="2025-08-06 16:40:18 编辑 删除").get_by_role("button").first.click()
        page.get_by_placeholder("请输入角色名称").click()
        page.get_by_placeholder("请输入角色名称").fill(test_data['role_name'])
        page.get_by_placeholder("请输入内容").click()
        page.get_by_placeholder("请输入内容").fill(test_data['remark'])
        page.get_by_role("button", name="保 存").click()

        # ---------------------
        context.close()
        browser.close()

    # 返回执行结果
    return test_data



# 如果直接运行此脚本
if __name__ == "__main__":
    result = run_playwright()
    print(f"执行结果: {result}")
