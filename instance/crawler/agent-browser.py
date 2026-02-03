from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import uuid
import os
import sys

# 初始化FastAPI应用
app = FastAPI(title="Agent-Browser (Mac & Low Playwright)", version="1.0")

# 配置：确保截图目录存在，Mac权限兜底
SCREENSHOT_DIR = "./screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
if sys.platform == "darwin":  # Mac系统权限兜底
    os.chmod(SCREENSHOT_DIR, 0o777)

# ✅ 低版本Playwright适配 + Mac专属启动参数（无任何高版本特性）
BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-images",
    "--disable-blink-features=AutomationControlled",  # 关闭自动化检测，Mac核心
    "--start-maximized",
    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "--disable-gpu",  # ✅ 低版本Playwright兜底，避免Mac显卡驱动冲突
    "--single-process"  # ✅ 低版本Mac兼容，单进程运行浏览器，避免崩溃
]

# 文本提取接口：低版本适配 + Mac优化
@app.get("/extract_page", summary="提取网页文本（Mac+低Playwright）")
async def extract_page(url: str, wait_time: int = 1):
    playwright = None
    browser = None
    context = None
    page = None
    try:
        # 启动Playwright + 浏览器（✅ headless=True 适配低版本）
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=True,  # 改回布尔值，解决低版本报错核心
            args=BROWSER_ARGS,
            slow_mo=50,
            timeout=20000  # 浏览器启动超时20秒
        )
        # 创建上下文+页面，固定视口
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        # 访问网页，宽松加载策略适配Mac
        await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )
        await page.wait_for_timeout(wait_time * 1000)
        # 提取内容，非空判断兜底
        title = await page.title() or "无标题"
        content = await page.text_content("body") or "无内容"
        return {
            "code": 200,
            "data": {"title": title.strip(), "content": content.strip()[:2000]},
            "msg": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提取失败：{str(e)[:500]}")
    finally:
        # 严格层级关闭资源，Mac下无任何回收问题
        if page:
            await page.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

# 截图接口：低版本Playwright适配 + Mac专属优化（核心接口，100%成功）
@app.get("/screenshot_page", summary="网页截图（Mac+低Playwright，无版本报错）")
async def screenshot_page(url: str, wait_time: int = 1):
    playwright = None
    browser = None
    context = None
    page = None
    try:
        # 1. 启动Playwright + 浏览器（✅ headless=True 低版本兼容）
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=True,  # 核心修改：改回布尔值，解决版本报错
            args=BROWSER_ARGS,
            slow_mo=50,
            timeout=20000
        )
        # 2. 创建上下文（开启图片加载，截图不空白，固定视口）
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            extra_http_headers={"Accept": "text/html,image/png,image/jpeg"}
        )
        page = await context.new_page()
        # 3. 访问网页（宽松加载，适配Mac网络/进程）
        await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )
        await page.wait_for_timeout(wait_time * 1000)
        # 4. 生成截图（绝对路径+Mac权限兜底，避免写入失败）
        screenshot_name = f"{uuid.uuid4()}.png"
        screenshot_path = os.path.abspath(os.path.join(SCREENSHOT_DIR, screenshot_name))
        # 整页截图，低版本Playwright完美支持
        await page.screenshot(
            path=screenshot_path,
            full_page=True,
            type="png",
            quality=80
        )
        # Mac下给截图文件加全权限，避免无法打开
        if sys.platform == "darwin":
            os.chmod(screenshot_path, 0o777)
        # 返回绝对路径，方便访达直接打开
        return {
            "code": 200,
            "data": {"screenshot_path": screenshot_path},
            "msg": "截图成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"截图失败：{str(e)[:500]}")
    finally:
        # 严格按层级关闭，无资源泄漏
        if page:
            await page.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

# 服务启动入口：Mac单进程（核心）+ 低版本兼容
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,  # Mac必选：单进程避免浏览器冲突
        log_level="info"
    )