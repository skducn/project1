# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2026-2-26
# Description: 专病库 - 编辑角色
# 路径：系统管理 - 角色管理
# 自动录制脚本：playwright codegen http://192.168.0.243:8083/login?redirect=/index
# # 等待networkidle，超时时间设为10秒
# page.wait_for_load_state("networkidle", timeout=10000)
# # 等待DOM加载完成
# page.wait_for_load_state("domcontentloaded")
# # 等待页面完全加载（对应浏览器load事件）
# page.wait_for_load_state("load")
# step_screenshot(page, "结果加载完成")
# *****************************************************************

from playwright.sync_api import Playwright, sync_playwright, expect
import re, os, sys
from pathlib import Path

# 更可靠的方式获取上级目录路径
current_file = Path(__file__).resolve()
web_dir = current_file.parents[2]  # 获取web目录（上三级）
config_dir = web_dir / "config"
config_file_path = config_dir / "config.ini"
# print(f"当前文件: {current_file}")
# print(f"Config目录: {config_dir}")
# print(f"Config文件: {config_file_path}")

# 将web目录添加到Python路径
# print(f"Web目录: {web_dir}")
sys.path.insert(0, str(web_dir))

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# print(f"Current directory: {current_dir}")
project_root = os.path.normpath(os.path.join(current_dir, "../../../../../.."))
# print(f"Calculated project root: {project_root}")
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    # print(f"Added {project_root} to sys.path")
# 验证PO模块路径
po_path = os.path.join(project_root, 'PO')
# print(f"PO module path: {po_path}")
# print(f"PO module exists: {os.path.exists(po_path)}")

from config.ConfigparserPO import ConfigparserPO
Configparser_PO = ConfigparserPO(str(config_file_path))

from PO.FakerPO import *
Fake_PO = FakePO()

# 提取无扩展名的文件名（新增用户）
full_path = __file__  # 获取完整路径（如：/Users/xxx/新增用户.py）
file_name = os.path.basename(full_path)  # 提取纯文件名（新增用户.py）
file_name_no_ext = os.path.splitext(file_name)[0]  # 提取无扩展名的文件名（新增用户）


# 数据
test_data = {"role_name": "7566", "remark": "today"}
print(f"编辑角色，生成指定数据: {test_data}")



def step_screenshot(page, step_name):
    """步骤化截图函数"""
    if Configparser_PO.角色管理("screenshots") == "on":
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        # 使用相对路径并确保目录存在
        screenshots_dir = f"{current_dir}/screenshots/{file_name_no_ext}"
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = f"{screenshots_dir}/{timestamp}_{step_name}.png"
        page.screenshot(path=screenshot_path)
        print(f"步骤[{step_name}]截图已保存：{screenshot_path}")

def run_playwright():
    # 1. 定义基础配置
    video_dir = f"{current_dir}/videos/{file_name_no_ext}"
    os.makedirs(video_dir, exist_ok=True)  # 确保目录存在
    # 自定义文件名（比如：操作名称_时间戳.webm）
    custom_video_name = f"{file_name_no_ext}_{time.strftime('%Y%m%d_%H%M%S')}.webm"
    custom_video_path = os.path.join(video_dir, custom_video_name)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        if Configparser_PO.角色管理("videos") == "on":
            # 开启录屏
            context = browser.new_context(record_video_dir=video_dir, record_video_size={"width": 1280, "height": 720})
        else:
            context = browser.new_context()
        page = context.new_page()

        page.goto(Configparser_PO.HTTP("url"))
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

        step_screenshot(page, "编辑角色")  # 截图

        # 保存
        if Configparser_PO.角色管理("isSave") == "on":
            page.get_by_role("button", name="保 存").click()
        else:
            page.get_by_role("button", name="取 消").click()

        if Configparser_PO.角色管理("videos") == "on":
            # 获取自动生成的视频路径
            original_video_path = page.video.path()

        # 5. 关闭上下文（必须先关闭，否则视频文件未生成，重命名会失败）
        context.close()
        browser.close()

        if Configparser_PO.角色管理("videos") == "on":
            # 重命名视频文件
            os.rename(original_video_path, custom_video_path)
            print(f"录屏文件已重命名为: {custom_video_path}")

        # ---------------------
        context.close()
        browser.close()

    # 返回执行结果, key使用对应数据库表字段
    return test_data



# 如果直接运行此脚本
if __name__ == "__main__":
    result = run_playwright()
    print(f"返回结果: {result}")

