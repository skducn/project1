# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2026-2-3
# Description   :
# python agent_browser.py
# 自动文档测试：访问http://localhost:8000/docs，FastAPI 内置 Swagger 文档，可直接点击 “Try it out” 调用接口；
# curl 命令测试（终端执行）：
# bash
# 运行
# # 提取百度首页文本
# curl "http://localhost:8000/extract_page?url=https://www.baidu.com"
# # 百度首页截图
# curl "http://localhost:8000/screenshot_page?url=https://www.baidu.com"
# *********************************************************************

from fastapi import FastAPI, HTTPException
from playwright.sync_api import sync_playwright, Page
import uuid
import os

# 初始化FastAPI应用
app = FastAPI(title="Agent-Browser Service", version="1.0")

# 配置：截图保存路径、浏览器启动参数
SCREENSHOT_DIR = "./screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
# 浏览器启动参数：禁用图片加载（提速）、模拟人类UA、无沙箱（服务端部署必需）
BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-images",
    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def get_browser_page() -> Page:
    """获取Playwright浏览器页面（同步模式，适合简单服务）"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(
        headless=True,  # 无头模式（无图形界面），测试时可设为False看浏览器界面
        args=BROWSER_ARGS,
        slow_mo=100  # 模拟人类操作速度，每步延迟100ms，规避反爬
    )
    context = browser.new_context()  # 新建浏览器上下文（独立会话）
    page = context.new_page()
    return page

@app.get("/extract_page", summary="提取网页文本内容")
def extract_page(url: str, wait_time: int = 2):
    """
    提取指定URL的网页文本内容（自动等待JS渲染）
    :param url: 目标网页URL（如https://www.baidu.com）
    :param wait_time: 页面加载后等待时间（秒），确保JS渲染完成
    :return: 网页标题、文本内容
    """
    try:
        page = get_browser_page()
        page.goto(url, wait_until="networkidle")  # 网络空闲时判定为加载完成
        page.wait_for_timeout(wait_time * 1000)   # 额外等待，适配慢渲染页面
        title = page.title()
        content = page.text_content("body")  # 提取body标签下所有文本
        # 关闭浏览器资源，避免内存泄漏
        page.context().browser().close()
        page.context().close()
        return {"code": 200, "data": {"title": title, "content": content}, "msg": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提取失败：{str(e)}")

@app.get("/screenshot_page", summary="网页整页截图")
def screenshot_page(url: str, wait_time: int = 2):
    """
    对指定URL整页截图，返回截图保存路径
    :param url: 目标网页URL
    :param wait_time: 页面加载后等待时间
    :return: 截图文件路径
    """
    try:
        page = get_browser_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(wait_time * 1000)
        # 生成唯一截图文件名
        screenshot_name = f"{uuid.uuid4()}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
        # 整页截图（full_page=True）
        page.screenshot(path=screenshot_path, full_page=True)
        # 关闭资源
        page.context().browser().close()
        page.context().close()
        return {"code": 200, "data": {"screenshot_path": screenshot_path}, "msg": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"截图失败：{str(e)}")

# 服务运行入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)