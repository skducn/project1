# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-06-15
# Description: Web自动化测试之playwright
# http://www.51testing.com/html/99/n-7793599.html
# 　pip install playwright
# 　　playwright install # 安装支持的浏览器：cr, chromium, ff, firefox, wk 和 webkit
# 　　playwright install chromium # 安装指定的chromium浏览器

# *****************************************************************

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()