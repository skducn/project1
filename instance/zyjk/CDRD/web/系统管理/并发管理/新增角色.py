# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2026-2-26
# Description: 专病库 - 新增角色
# 路径：系统管理 - 角色管理
# 自动录制脚本：playwright codegen http://192.168.0.243:8083/login?redirect=/index
# *****************************************************************

from playwright.sync_api import Playwright, sync_playwright, expect
import re, os, sys
import time


# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# 重新计算项目根目录路径
project_root = os.path.normpath(os.path.join(current_dir, "../../../../../.."))
print(f"Calculated project root: {project_root}")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to sys.path")

# 验证PO模块路径
po_path = os.path.join(project_root, 'PO')
print(f"PO module path: {po_path}")
print(f"PO module exists: {os.path.exists(po_path)}")

from PO.FakerPO import *
Fake_PO = FakePO()
test_data = Fake_PO.genTest(['genName', 'genPostcode', 'genAddress'], 1)
print(f"随机生成测试数据: {test_data}")



def run_playwright():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://192.168.0.243:8083/login?redirect=/index")

        # # 等待5秒，让用户看到页面加载
        # print("等待5秒...")
        # time.sleep(5)

        page.get_by_placeholder("请输入登录账号").click()
        page.get_by_placeholder("请输入登录账号").fill("syy")
        page.get_by_placeholder("请输入密码").click()
        page.get_by_placeholder("请输入密码").fill("Qa@1234567")
        page.get_by_role("button", name="登 录").click()
        page.locator("div").filter(has_text=re.compile(r"^系统管理$")).click()
        page.get_by_role("link", name="角色管理").click()
        page.get_by_role("button", name="新增角色").click()
        page.get_by_placeholder("请输入角色名称").click()
        page.get_by_placeholder("请输入角色名称").fill(test_data[0][0])
        page.get_by_placeholder("请输入权限字符").click()
        page.get_by_placeholder("请输入权限字符").fill("44")
        page.get_by_label("角色顺序").click()
        page.get_by_label("角色顺序").fill(test_data[0][1])
        page.get_by_role("treeitem", name="基础配置").locator("span").nth(1).click()
        page.get_by_role("treeitem", name="系统日志").locator("span").nth(1).click()
        page.get_by_role("treeitem", name="系统管理").locator("span").nth(1).click()
        page.get_by_placeholder("请输入内容").click()
        page.get_by_placeholder("请输入内容").fill(test_data[0][2])
        # page.get_by_role("button", name="保 存").click()
        page.get_by_role("button", name="取 消").click()

        # ---------------------
        context.close()
        browser.close()

    # 返回执行结果, key使用对应数据库表字段
    return {
        "role_name": test_data[0][0],
        "role_sort": test_data[0][1],
        "remark": test_data[0][2]
    }



# 如果直接运行此脚本
if __name__ == "__main__":
    result = run_playwright()
    print(f"执行结果: {result}")