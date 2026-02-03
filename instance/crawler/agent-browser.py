# {"code":200,"data":{"screenshot_path":"/Users/linghuchong/Downloads/51/Python/project/instance/crawler/screenshots/eb951099-4173-487b-acf9-67d780475a5c.png"},"msg":"截图成功！可通过访达Shift+Command+G打开路径"}localhost-2:ms-playwright linghuchong$


from fastapi import FastAPI, HTTPException
from playwright.async_api import async_playwright
import uuid
import os
import sys

app = FastAPI(title="Agent-Browser (Mac 本地Chrome最终版)", version="1.0")

# 截图目录配置+Mac权限兜底
SCREENSHOT_DIR = "./screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
if sys.platform == "darwin":
    os.chmod(SCREENSHOT_DIR, 0o777)

# 本地Chrome适配参数（精简无冲突）
BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--start-maximized",
    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

# 文本提取接口（本地Chrome版）
@app.get("/extract_page", summary="提取网页文本（本地Chrome，无报错）")
async def extract_page(url: str, wait_time: int = 1):
    playwright = None
    browser = None
    context = None
    page = None
    try:
        playwright = await async_playwright().start()
        # 调用Mac本地Chrome，无内置内核兼容问题
        browser = await playwright.chromium.launch(
            headless=False,
            args=BROWSER_ARGS,
            slow_mo=50,
            timeout=30000,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(wait_time * 1000)
        title = await page.title() or "无标题"
        content = await page.text_content("body") or "无内容"
        return {
            "code": 200,
            "data": {"title": title.strip(), "content": content.strip()[:2000]},
            "msg": "文本提取成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提取失败：{str(e)[:500]}")
    finally:
        # 严格按层级关闭资源
        if page:
            await page.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

# 截图接口（✅ 核心修复：删除quality参数，解决PNG不兼容）
@app.get("/screenshot_page", summary="网页截图（本地Chrome最终版，100%成功）")
async def screenshot_page(url: str, wait_time: int = 1):
    playwright = None
    browser = None
    context = None
    page = None
    try:
        playwright = await async_playwright().start()
        # 调用Mac本地Chrome
        browser = await playwright.chromium.launch(
            headless=False,
            args=BROWSER_ARGS,
            slow_mo=50,
            timeout=30000,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
        # 开启图片加载，保证截图不空白
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            extra_http_headers={"Accept": "text/html,image/png,image/jpeg"}
        )
        page = await context.new_page()
        # 访问目标网页
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(wait_time * 1000)
        # 生成唯一截图名+绝对路径
        screenshot_name = f"{uuid.uuid4()}.png"
        screenshot_path = os.path.abspath(os.path.join(SCREENSHOT_DIR, screenshot_name))
        # ✅ 核心修复：删除quality=80，PNG格式无需质量参数
        await page.screenshot(
            path=screenshot_path,
            full_page=True,
            type="png"
        )
        # Mac截图文件权限兜底
        if sys.platform == "darwin":
            os.chmod(screenshot_path, 0o777)
        return {
            "code": 200,
            "data": {"screenshot_path": screenshot_path},
            "msg": "截图成功！可通过访达Shift+Command+G打开路径"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"截图失败：{str(e)[:500]}")
    finally:
        # 关闭所有资源，避免内存占用
        if page:
            await page.close()
        if context:
            await context.close()
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()

# Mac单进程启动（必选，避免浏览器冲突）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
        log_level="info"
    )