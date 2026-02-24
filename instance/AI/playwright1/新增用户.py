from playwright.sync_api import Playwright, sync_playwright, expect
import re

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://192.168.0.243:8083/login?redirect=/index")
    page.get_by_placeholder("请输入登录账号").fill("admin")
    page.get_by_placeholder("请输入密码").fill("Qa@123456")
    page.get_by_role("button", name="登 录").click()
    page.locator("div").filter(has_text=re.compile(r"^系统管理$")).click()
    page.get_by_role("link", name="用户管理").click()
    page.get_by_role("button", name="新增用户").click()
    page.get_by_label("姓名", exact=True).fill("test444")
    page.locator(".el-col > .el-form-item > .el-form-item__content > .el-select > .el-select__wrapper > .el-select__selection > div:nth-child(2)").first.click()
    page.get_by_role("option", name="眼科(0023)").locator("span").click()
    page.get_by_label("手机号").fill("13816109088")
    page.get_by_label("邮箱").fill("sk@1235678.com")
    page.get_by_label("账号（保存成功后不可修改）").fill("tester66")
    page.get_by_label("工号").fill("009")
    page.locator("div:nth-child(4) > div > .el-form-item > .el-form-item__content > .el-select > .el-select__wrapper > .el-select__selection > div:nth-child(2)").first.click()
    page.get_by_role("option", name="主治医生", exact=True).locator("span").click()
    page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(4).click()
    page.get_by_role("option", name="女").click()
    page.get_by_label("备注").fill("哈哈哈")
    page.get_by_role("button", name="保 存").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
