from playwright.sync_api import Playwright, sync_playwright, expect
import re

# from PO.FakerPO import *
#
# Fake_PO = FakePO()
#
# # 生成测试数据
# r = Fake_PO.genTest(['genName', 'genPhone', 'genEmail', 'genPostcode', 'genPostcode'], 1)
# print(r)


def run_playwright(test_data=None):
    """执行 playwright 自动化流程"""
    # if test_data is None:
    #     test_data = r  # 使用默认生成的数据

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto("http://192.168.0.243:8083/login?redirect=/index")
            page.get_by_placeholder("请输入登录账号").fill("admin")
            page.get_by_placeholder("请输入密码").fill("Qa@123456")
            page.get_by_role("button", name="登 录").click()
            page.locator("div").filter(has_text=re.compile(r"^系统管理$")).click()
            page.get_by_role("link", name="用户管理").click()
            page.get_by_role("button", name="新增用户").click()

            # 使用传入的测试数据
            page.get_by_label("姓名", exact=True).fill(test_data[0][0])
            page.locator(
                ".el-col > .el-form-item > .el-form-item__content > .el-select > .el-select__wrapper > .el-select__selection > div:nth-child(2)").first.click()
            page.get_by_role("option", name="眼科(0023)").locator("span").click()
            page.get_by_label("手机号").fill(test_data[0][1])
            page.get_by_label("邮箱").fill(test_data[0][2])
            page.get_by_label("账号（保存成功后不可修改）").fill(test_data[0][3])
            page.get_by_label("工号").fill(test_data[0][4])
            page.locator(
                "div:nth-child(4) > div > .el-form-item > .el-form-item__content > .el-select > .el-select__wrapper > .el-select__selection > div:nth-child(2)").first.click()
            page.get_by_role("option", name="主治医生", exact=True).locator("span").click()
            page.locator("div").filter(has_text=re.compile(r"^请选择$")).nth(4).click()
            page.get_by_role("option", name="女").click()
            page.get_by_label("备注").fill("自动化测试用户")

            # 保存操作（取消注释以执行）
            # page.get_by_role("button", name="保 存").click()

            # 记录成功结果
            results.append({
                "status": "success",
                "name": test_data[0][0],
                "phone": test_data[0][1],
                "email": test_data[0][2],
                "account": test_data[0][3],
                "work_id": test_data[0][4]
            })

        except Exception as e:
            results.append({
                "status": "failed",
                "error": str(e)
            })
        finally:
            context.close()
            browser.close()

    return results


# 如果直接运行此脚本
if __name__ == "__main__":
    result = run_playwright()
    print(f"执行结果: {result}")

    # 设置返回值供外部调用
    PLAYWRIGHT_RESULT = result
