# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Created on : 2018-7-2
# Description: Web 对象层 （selenium 4.4.3）
# pip install opencv_python  下载cv2
# https://www.cnblogs.com/FBGG/p/17975814
# selenium并不支持获取响应的数据，我们可以使用selenium-wire库，selenium-wire扩展了 Selenium 的 Python 绑定，可以访问浏览器发出的底层请求。seleniumwire只兼容Selenium 4.0.0+，
# pip install selenium-wire
# ***************************************************************
# todo selenium
# 查看版本：pip list | grep selenium 或 pip show selenium
# 查看可安装版本：pip install selenium==
# 安装指定版本：pip install selenium==4.4.3
# 注：selenium 4.10 会引起浏览器自动关闭现象，实测安装4.4.3 正常

# todo chrome浏览器
# 1，查看chrome浏览器版本：chrome://version
# print(self.driver.capabilities['browserVersion'])  # 114.0.5735.198  //获取浏览器版本
# print(self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # 114.0.5735.90  //获取chrome驱动版本
# 注：以上两版本号前3位一样就可以，如 114.0.5735

# todo chrome驱动
# 下载1：https://googlechromelabs.github.io/chrome-for-testing/#stable （新）
# https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/mac-x64/chrome-mac-x64.zip
# https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.96/mac-x64/https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.114/mac-arm64/chromedriver-mac-arm64.zip
# https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/mac-x64/chromedriver-mac-x64.zip
# 下载2：http://chromedriver.storage.googleapis.com/index.html （旧）
# 下载3：https://registry.npmmirror.com/binary.html?path=chromedriver （旧）

# todo 自动下载驱动
# from webdriver_manager.chrome import ChromeDriverManager
# ChromeDriverManager().install()
# self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# mac系统默认调用路径：/Users/linghuchong/.wdm/drivers/chromedriver/mac64/120.0.6099.109/chromedriver-mac-x64/chromedriver
# python -m pip install --upgrade pip && python -m pip install chromedriver-binary==135.0.7049.97.0

# todo 设置配置
# for win 路径：C:\Python38\Scripts\chromedrive.exe
# for mac 路径：
# from selenium.webdriver.chrome.service import Service
# self.driver = webdriver.Chrome(service=Service("/Users/linghuchong/Downloads/51/Python/project/instance/web/chromedriver"), options=options)

# todo options参数
# https://www.bilibili.com/read/cv25916901/
# https://blog.csdn.net/xc_zhou/article/details/82415870
# https://blog.csdn.net/amberom/article/details/107980370
# https://www.5axxw.com/questions/content/ey8x1v  解决不安全下载被阻止问题
# https://zhuanlan.zhihu.com/p/612823571

# todo 常见问题
# Q1：MAC 移动chromedriver时报错，如 sudo mv chromedriver /usr/bin 提示： Operation not permitted
# A1: 重启按住command + R,进入恢复模式，实用工具 - 终端，输入 csrutil disable , 重启电脑。

# todo edge
# edge 114.0.1823.37 (64 位) , selenium =3.141.0，edge = 114.0.1823.37
# edge下载：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# mac系统默认调用路径：/usr/local/bin/msedgedriver
# win系统默认调用路径：c:\python39\msedgedriver.exe

# todo firefox
# geckodriver 0.14.0 for selenium3.0
# ff 66.0.4 (64 位) , selenium =3.141.0，gecko = 0.24.0
# 下载驱动：
# https://github.com/mozilla/geckodriver/releases
# https://github.com/mozilla/geckodriver/releases/tag/v0.33.0
# mac系统默认调用路径：/usr/local/bin/geckodriver
# win系统默认调用路径：c:\python39\geckodriver.exe

# Q1：WebDriverException:Message:'geckodriver'executable needs to be in Path
# A1：geckodriver是原生态的第三方浏览器，对于selenium3.x版本使用geckodriver来驱动firefox，需下载geckodriver.exe
# 将 geckodriver 放在 C:\Python38\Scripts
# ***************************************************************

"""
1.1 打开网站 open()
1.2 打开标签页 opnLabel("http://www.jd.com")
1.3 切换标签页 swhLabel(1)
1.4 关闭当前窗口 cls()

2.1 获取当前浏览器宽高 getBrowserSize()
2.2 设置浏览器分辨率 setBrowserSize()
2.3 设置浏览器全屏 setBrowserMax()
2.4 缩放页面比率 zoom(20)
2.5 截取浏览器内屏幕 getBrowserScreen()
2.6 页面滚动条到底部 scrollBottom()

3.1 弹出框 popupAlert()
3.2 确认弹出框 confirmAlert("accept", 2)

4.1 关闭浏览器应用 quit()

5.1 app屏幕左移 scrollLeftByApp('1000',9)
5.2 app屏幕右移 scrollRightByApp('1000', 5)
5.3 app屏幕上移 scrollUpByApp('1000', 5)
5.4 app屏幕下移 scrollDownByApp('1000', 5)

元素拖动到可见的元素 scrollIntoView(varXpath)
内嵌窗口中滚动条操作 scrollTopById(varId)
动态加载页面滚动到底部（加载所有数据） dynamicLoadToEnd()
获取验证码 getCode()
"""

from PO.DomPO import *

import requests, subprocess, os, json
# import bs4, ddddocr
import random

from selenium.webdriver.support.ui import Select

import logging
from selenium.webdriver.remote.remote_connection import LOGGER


class WebPO(DomPO):

    def __init__(self, browser_type="chrome"):
        self.browser_type = browser_type
        self.driver = self._initialize_driver()
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='Web_selenium_detailed.log'
        )
        # 设置 Selenium 远程连接日志级别
        LOGGER.setLevel(logging.INFO)


    def _initialize_driver(self):

        # 1.1 初始化chrome

        # 1 配置项
        options = Options()

        if self.browser_type == "chrome":

            # todo 屏幕
            options.add_argument("--start-maximized")  # 最大化浏览器
            # width, height = pyautogui.size()  # 1440 900  # 自动获取屏幕尺寸，即最大化
            # options.add_argument('--window-size=%s,%s' % (pyautogui.size()[0], pyautogui.size()[1])) # 自动获取屏幕尺寸，即最大化浏览器 1440 900
            # options.add_argument("--start-fullscreen")  # 全屏模式，F11可退出
            # options.add_argument("--kiosk")  # 全屏模式，alt+tab切换。ctrl+f4退出
            # options.add_argument('--window-size=%s,%s' % (320, 800)) # 指定窗口大小320 800

            # todo 浏览器
            options.add_experimental_option("detach", True)  # 浏览器永不关闭
            options.add_argument('--incognito')  # 无痕模式
            # options.add_argument('--disable-popup-blocking')  # 禁用弹窗阻止（可能有助于避免某些弹窗相关的崩溃）
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽--ignore-certificate-errors提示信息的设置参数项
            options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 屏蔽 "Chrome正受到自动测试软件的控制"提示，建议放在最后。
            # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片（提升速度）
            options.add_argument('--hide-scrollbars')  # 隐藏滚动条（因对一些特殊页面）
            # options.headless = True  # 无界面模式
            # options.add_argument("--lang=en")  # 指定浏览器的语言，避免出现“询问是否翻译非您所用语言的网页”

            # todo 安全性
            options.add_argument("--allow-running-insecure-content")  # 允许HTTPS页面从HTTP链接引用JavaScript、CSS和插件内容，该参数会降低浏览器的安全性，因为它允许HTTPS页面加载未加密的HTTP资源。这可能导致中间人攻击（MITM），从而危及用户的数据安全和隐私。
            # options.add_argument("--disable-blink-features=AutomationControlled")  # 禁止浏览器出现验证滑块，防止自动化检测，关闭浏览器控制显示
            # options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://192.168.0.203:30080/")  # 解决下载文件是提示：已阻止不安全的文件下载，允许不安全的文件下载
            # 禁用“保存密码”弹出窗口
            options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})

            # todo 系统
            # options.add_argument("disable-cache")  # 禁用缓存
            options.add_argument("--disable-extensions")  # 禁用所有插件和扩展（提高稳定性，有时插件可能引起稳定性问题）
            # options.add_argument('--no-sandbox')  # 关闭沙盒模式（沙盒模式提一种提高安全性的技术，但可能与某系统不兼容，关闭可能会降低浏览器的安全性）,会引起tab stash无法打开标签页。
            options.add_argument('-disable-dev-shm-usage')  # 禁用/dev/shm使用（可减少内存使用，但影响性能）
            # options.add_argument('--disable-gpu')  # 禁用GPU加速（虽然GPU加速可以提高性能，但有些情况下会导致崩溃）
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
            # options.add_argument('--disable-logging')  # 禁用日志记录（减少日志记录的资源消耗）
            # options.add_argument('--disable-javascript')  # 禁用JavaScript（有时可以用来测试JavaScript相关的问题）
            # options.add_argument(r"--user-data-dir=c:\selenium_user_data")  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题

            # # 绕过检测（滑动验证码）
            # self.driver.execute_cdp_cmd("Page.addScriptToEvaluteOnNewDocument", {"source": """Object.defineProperty(navigator,'webdriver', {get: () => undefined})"""})

            try:
                # 更新下载chromedriver
                self.updateChromedriver(options)
            except Exception as e:
                logging.error(f"发生错误: {e}")

            return self.driver

        elif self.browser_type == "noChrome":

            # 无界面模式
            # options.headless = True  # 弃用
            options.add_argument('--headless=new')  # 如果你使用的是 Chrome 109 及以上版本，推荐使用 '--headless=new'
            # options.add_argument('--headless')  # 如果你使用的是旧版本 Chrome，使用 '--headless'

            # todo 系统
            # options.add_argument("disable-cache")  # 禁用缓存
            # options.add_argument("--disable-extensions")  # 禁用所有插件和扩展（提高稳定性，有时插件可能引起稳定性问题）
            # options.add_argument('--no-sandbox')  # 关闭沙盒模式（沙盒模式提一种提高安全性的技术，但可能与某系统不兼容，关闭可能会降低浏览器的安全性）
            options.add_argument('-disable-dev-shm-usage')  # 禁用/dev/shm使用（可减少内存使用，但影响性能）
            # options.add_argument('--disable-gpu')  # 禁用GPU加速（虽然GPU加速可以提高性能，但有些情况下会导致崩溃）
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
            # options.add_argument('--disable-logging')  # 禁用日志记录（减少日志记录的资源消耗）
            # options.add_argument('--disable-javascript')  # 禁用JavaScript（有时可以用来测试JavaScript相关的问题）
            # options.add_argument(r"--user-data-dir=c:\selenium_user_data")  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题

            try:
                # 更新下载chromedriver
                self.updateChromedriver(options)
            except Exception as e:
                logging.error(f"发生错误: {e}")

            return self.driver

        elif self.browser_type == "chromeCookies":

            # todo 屏幕
            options.add_argument("--start-maximized")  # 最大化浏览器
            # width, height = pyautogui.size()  # 1440 900  # 自动获取屏幕尺寸，即最大化
            # options.add_argument('--window-size=%s,%s' % (pyautogui.size()[0], pyautogui.size()[1])) # 自动获取屏幕尺寸，即最大化浏览器 1440 900
            # options.add_argument("--start-fullscreen")  # 全屏模式，F11可退出
            # options.add_argument("--kiosk")  # 全屏模式，alt+tab切换。ctrl+f4退出
            # options.add_argument('--window-size=%s,%s' % (320, 800)) # 指定窗口大小320 800

            # todo 浏览器
            options.add_experimental_option("detach", True)  # 浏览器永不关闭
            options.add_argument('--incognito')  # 无痕模式
            options.add_argument('--disable-popup-blocking')  # 禁用弹窗阻止（可能有助于避免某些弹窗相关的崩溃）
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽--ignore-certificate-errors提示信息的设置参数项
            options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 屏蔽 "Chrome正受到自动测试软件的控制"提示，建议放在最后。
            # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片（提升速度）
            options.add_argument('--hide-scrollbars')  # 隐藏滚动条（因对一些特殊页面）
            # options.headless = True  # 无界面模式
            # options.add_argument("--lang=en")  # 指定浏览器的语言，避免出现“询问是否翻译非您所用语言的网页”

            # todo 安全性
            options.add_argument("--allow-running-insecure-content")  # 允许HTTPS页面从HTTP链接引用JavaScript、CSS和插件内容，该参数会降低浏览器的安全性，因为它允许HTTPS页面加载未加密的HTTP资源。这可能导致中间人攻击（MITM），从而危及用户的数据安全和隐私。
            options.add_argument("--disable-blink-features=AutomationControlled")  # 禁止浏览器出现验证滑块，防止自动化检测，关闭浏览器控制显示
            options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://192.168.0.203:30080/")  # 解决下载文件是提示：已阻止不安全的文件下载，允许不安全的文件下载
            # 禁用“保存密码”弹出窗口
            options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})

            # todo 系统
            # options.add_argument("disable-cache")  # 禁用缓存
            options.add_argument("--disable-extensions")  # 禁用所有插件和扩展（提高稳定性，有时插件可能引起稳定性问题）
            # options.add_argument('--no-sandbox')  # 关闭沙盒模式（沙盒模式提一种提高安全性的技术，但可能与某系统不兼容，关闭可能会降低浏览器的安全性）
            options.add_argument('-disable-dev-shm-usage')  # 禁用/dev/shm使用（可减少内存使用，但影响性能）
            # options.add_argument('--disable-gpu')  # 禁用GPU加速（虽然GPU加速可以提高性能，但有些情况下会导致崩溃）
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
            # options.add_argument('--disable-logging')  # 禁用日志记录（减少日志记录的资源消耗）
            # options.add_argument('--disable-javascript')  # 禁用JavaScript（有时可以用来测试JavaScript相关的问题）
            # options.add_argument(r"--user-data-dir=c:\selenium_user_data")  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题

            try:
                # 更新下载chromedriver
                self.updateChromedriver(options)
            except Exception as e:
                logging.error(f"发生错误: {e}")

            return self.driver

        elif self.browser_type == "appChrome":

            # todo 屏幕
            options.add_argument('--window-size=%s,%s' % (320, 1000))  # 指定窗口大小

            # todo 浏览器
            options.add_experimental_option("detach", True)  # 浏览器永不关闭
            options.add_argument("--allow-running-insecure-content")  # Allow insecure content
            # options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://192.168.0.243:8010/")  # Replace example.com with your site's domain (this is what worked for me)

            options.add_argument("--disable-blink-features=AutomationControlled")  # 禁止浏览器出现验证滑块
            options.add_argument('--incognito')  # 无痕模式

            options.add_argument('--disable-popup-blocking')  # 禁用弹窗阻止（可能有助于避免某些弹窗相关的崩溃）
            options.add_argument('-ignore-ssl-errors')  # 忽略相关错误
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 忽略证书错误
            options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 防止自动化检测, 解决"Chrome正受到自动测试软件的控制"提示，建议放在最后。
            # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片（提升速度）
            options.add_argument('--hide-scrollbars')  # 隐藏滚动条（因对一些特殊页面）
            # options.headless = True  # 无界面模式
            # options.add_argument("--lang=en")  # 指定浏览器的语言，避免出现“询问是否翻译非您所用语言的网页”

            # todo 系统
            # options.add_argument("disable-cache")  # 禁用缓存
            options.add_argument("--disable-extensions")  # 禁用所有插件和扩展（提高稳定性，有时插件可能引起稳定性问题）
            # options.add_argument('--no-sandbox')  # 关闭沙盒模式（沙盒模式提一种提高安全性的技术，但可能与某系统不兼容，关闭可能会降低浏览器的安全性）
            # options.add_argument('-disable-dev-shm-usage')  # 禁用/dev/shm使用（可减少内存使用，但影响性能）
            # options.add_argument('--disable-gpu')  # 禁用GPU加速（虽然GPU加速可以提高性能，但有些情况下会导致崩溃）
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志，防止自动化日志输出检测
            options.add_argument('--disable-logging')  # 禁用日志记录（减少日志记录的资源消耗）
            # options.add_argument('--disable-javascript')  # 禁用JavaScript（有时可以用来测试JavaScript相关的问题）
            # options.add_argument(r"--user-data-dir=c:\selenium_user_data")  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题

            try:
                # 更新下载chromedriver
                self.updateChromedriver(options)
            except Exception as e:
                logging.error(f"发生错误: {e}")

            return self.driver


    def openURL(self, varURL, t=2):
        self.opn(varURL, t)

    def opn(self, varUrl, t=2):
        # 1.1 打开网页
        self.driver.get(varUrl)
        sleep(t)


    def _openUrlByAuth(self, var1genCookies, varPrefixUrl, varProtectedUrl):

        # 1.1 # 鉴权token，cookies鉴权自动化 打开chrome

        # 1 配置项
        options = Options()

        if self.driver == "chromeCookies":

            # todo 屏幕
            options.add_argument("--start-maximized")  # 最大化浏览器

            # todo 浏览器
            options.add_experimental_option("detach", True)  # 浏览器永不关闭
            options.add_argument('--incognito')  # 无痕模式
            options.add_argument('--disable-popup-blocking')  # 禁用弹窗阻止（可能有助于避免某些弹窗相关的崩溃）
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽--ignore-certificate-errors提示信息的设置参数项
            options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 屏蔽 "Chrome正受到自动测试软件的控制"提示，建议放在最后。
            # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片（提升速度）
            options.add_argument('--hide-scrollbars')  # 隐藏滚动条（因对一些特殊页面）

            # todo 安全性
            options.add_argument("--allow-running-insecure-content")  # 允许HTTPS页面从HTTP链接引用JavaScript、CSS和插件内容，该参数会降低浏览器的安全性，因为它允许HTTPS页面加载未加密的HTTP资源。这可能导致中间人攻击（MITM），从而危及用户的数据安全和隐私。
            options.add_argument("--disable-blink-features=AutomationControlled")  # 禁止浏览器出现验证滑块，防止自动化检测，关闭浏览器控制显示
            options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://192.168.0.203:30080/")  # 解决下载文件是提示：已阻止不安全的文件下载，允许不安全的文件下载
            options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})  # 禁用“保存密码”弹出窗口

            # todo 系统
            # options.add_argument("disable-cache")  # 禁用缓存
            options.add_argument("--disable-extensions")  # 禁用所有插件和扩展（提高稳定性，有时插件可能引起稳定性问题）
            options.add_argument('--no-sandbox')  # 关闭沙盒模式（沙盒模式提一种提高安全性的技术，但可能与某系统不兼容，关闭可能会降低浏览器的安全性）
            options.add_argument('-disable-dev-shm-usage')  # 禁用/dev/shm使用（可减少内存使用，但影响性能）
            options.add_argument('--disable-gpu')  # 禁用GPU加速（虽然GPU加速可以提高性能，但有些情况下会导致崩溃）
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
            options.add_argument('--disable-logging')  # 禁用日志记录（减少日志记录的资源消耗）
            # options.add_argument('--disable-javascript')  # 禁用JavaScript（有时可以用来测试JavaScript相关的问题）
            # options.add_argument(r"--user-data-dir=c:\selenium_user_data")  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题

            # 更新下载chromedriver
            self.updateChromedriver(options)


            # 鉴权，必须先打开目标域名
            self.driver.get(varPrefixUrl)
            # 如：driver.get('http://192.168.0.243:8010/')

            # try:
            # session = requests.Session()

            # 读取 cookies文件
            with open(var1genCookies, 'r') as f:
                loaded_cookies = json.load(f)
                # print("1genAuthorization :", loaded_cookies)  # 打印内容
                # print("Type of loaded_cookies:", type(loaded_cookies))  # 打印类型

                if 'Admin-Token' in loaded_cookies:
                    # 手动设置 Admin-Token 到 local storage
                    self.driver.execute_script(f"window.localStorage.setItem('Admin-Token', '{loaded_cookies['Admin-Token']}');")
                    # 打开受保护页面
                    self.driver.get(varProtectedUrl)
                    print("成功访问受保护页面2 =>", varProtectedUrl)
                else:
                    # 添加 cookies
                    for cookie in loaded_cookies:
                        self.driver.add_cookie(cookie)

                    # 如果 loaded_cookies 是列表，转换为字典
                    if isinstance(loaded_cookies, list):
                        loaded_cookies = {item['name']: item['value'] for item in loaded_cookies}
                        # cookies: [{'domain': '192.168.0.243', 'httpOnly': False, 'name': 'Admin-Token', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9pZCI6ODUsImNhdGVnb3J5X2NvZGUiOiI0IiwidXNlcl9rZXkiOiIxMjkwYTE0OC1jY2VhLTQwNTktYjU1YS04OTU4MWU4MzE4ODQiLCJ0aGlyZF9ubyI6IjEyMyIsImhvc3BpdGFsX2lkIjoiY3NkbSIsInVzZXJuYW1lIjoi5rWL6K-VIiwiaG9zcGl0YWxfbmFtZSI6IuW9rea1puaWsOadkeihl-mBk-ekvuWMuuWBpeW6t-euoeeQhuS4reW_gyIsImFmZmlsaWF0ZWRfbmFtZSI6IiJ9.NzctL_ySvo8uwFikWJ5LbOpDOVfWnAEM2GLVRt23-qgmh9SPAuKQwiWbXkl9jIl_FHckzphSsa9zPIYjAYlzXQ'}]
                        # name和value，对应的键值对是 {'Admin-Token'：'eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9p...'}
                        # print(loaded_cookies)

                        self.driver.execute_script(
                            f"window.localStorage.setItem('Admin-Token', '{loaded_cookies['Admin-Token']}');")
                        # 打开受保护页面
                        self.driver.get(varProtectedUrl)
                        print("成功访问受保护页面1 =>", varProtectedUrl)

                    else:
                        raise ValueError("Invalid format of loaded_cookies")

                    # # 使用 cookies 访问受保护的页面
                    # new_session = requests.Session()
                    # new_session.cookies.update(loaded_cookies)
                    # protected_response = new_session.get(varProtectedUrl)
                    # if protected_response.status_code == 200:
                    #     print("成功访问受保护页面 =>", varProtectedUrl)
                    #     self.driver.get(varProtectedUrl)
                    #     # driver.get('http://192.168.0.243:8010/#/SignManage/service')
                    #     # input("按 Enter 键关闭浏览器...")
                    # else:
                    #     print(f"访问受保护页面失败，状态码: {protected_response.status_code}")

                    # 关闭会话
                    # session.close()
                    # if 'new_session' in locals():
                    #     new_session.close()

            # except FileNotFoundError:
            #     print("未找到保存的 cookies 文件。")
            # except Exception as e:
            #     print(f"发生错误: {e}")

            return self.driver


    def openUrlByAuth(self, varAuthFile, varPrefixUrl, varProtectedUrl):
        # cookies鉴权自动化，通过cookies访问授权页面
        # varAuthFile, cookies.json
        # varPrefixUrl, 导航到目标域名下的某个页面
        # varProtectedUrl, 打开受保护页面
        # Web_PO.openUrlByAuth('cookies.json','http://192.168.0.243:8010/','http://192.168.0.243:8010/#/SignManage/signAssess')
        self._openUrlByAuth(varAuthFile, varPrefixUrl, varProtectedUrl)


    def delRequests(self):

        # 清除浏览器的请求历史记录
        del self.driver.requests

    def requests(self, varInterFace):

        # 获取页面接口请求
        for request in self.driver.requests:
            if varInterFace in request.url:
                return str(request.url).split(varInterFace)[1]
                # return request.url

    def requestsExcept(self, varIgnore):

        # 获取当前页面除以下之外的所有请求地址

        # # 清除浏览器的请求历史记录
        # self.driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
        # self.driver.execute_cdp_cmd("Network.clearBrowserCache", {})

        for request in self.driver.requests:
            if (request.url)[-3:] in varIgnore or (request.url)[-4:] in varIgnore:
                ...
            else:
                print(request.method, request.url)
                # print(request.method)
                # print(request.body)
                # print(request.headers)
                # print(request.response.status_code)
                # print(request.response.body.decode('utf-8'))  # 解决中文乱码
                # return request.method, request.url
            # return None

    def saveas(self):

        # 等待并接受"另存为"弹框
        try:
            save_as = WebDriverWait(self.driver, 10).until(
                element_to_be_clickable((By.CSS_SELECTOR, "存储"))  # "Save As"
            )
            save_as.click()  # 或者
            # save_as.send_keys("/Users/linghuchong/Downloads/123.xlsx") # 手动指定保存位置和文件名
        except Exception as e:
            print(f"未找到'另存为'弹框: {e}")

    def updateChromedriver(self, options):

        # 获取浏览器版本及主版本（前三位如果相同，则为同一版本）
        if os.name == "nt":
            varChromePath = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            varDriverPath = r"C:\\Users\\jh\\.wdm\\drivers\\chromedriver\\win64\\"

            # 1 本机chrome程序路径
            chromeVer = subprocess.check_output("powershell -command \"&{(Get-Item '" + varChromePath + "').VersionInfo.ProductVersion}\"", shell=True)
            chromeVer = bytes.decode(chromeVer).replace("\n", '')
            chromeVer3 = chromeVer.replace(chromeVer.split(".")[3], '')  # 120.0.6099.

            # 2 驱动路径
            currPath = varDriverPath + chromeVer3

            # 3 检查chromedriver主版本是否存在
            if os.path.isdir(currPath) == False:
                # 自动下载chrome驱动并修改成主板本
                print("chromedriver downloading...")
                Service(ChromeDriverManager().install())
                print("done")
                l_folder = os.listdir(varDriverPath)
                for i in range(len(l_folder)):
                    if chromeVer3 in l_folder[i]:
                        os.rename(varDriverPath + l_folder[i], varDriverPath + chromeVer3)
                        break
                os.chdir(varDriverPath + chromeVer3 + "\\chromedriver-win32")
            # s = Service(varDriverPath + chromeVer3 + "\\chromedriver-win32\\chromedriver.exe")
            currPath = varDriverPath + chromeVer3 + "\\chromedriver-win32\\chromedriver.exe"
            s = Service(executable_path=currPath, service_args=["--verbose"],log_output='Web_chromedriver_win.log')
            self.driver = webdriver.Chrome(service=s, options=options)

            # print("浏览器版本：", self.driver.capabilities['browserVersion'])  # 114.0.5735.198  //浏览器版本
            # print("chrome驱动版本：", self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # 114.0.5735.90  //chrome驱动版本

        elif os.name == "posix":
            # for mac
            # chromedriver --version
            # (py310) localhost-2:project linghuchong$ which chromedriver
            # /usr/local/bin/chromedriver

            varDriverPath = r"/Users/linghuchong/.wdm/drivers/chromedriver/mac64/"

            # 1 本机chrome浏览器程序路径
            chromeVer = subprocess.check_output(r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version", shell=True)
            chromeVer = bytes.decode(chromeVer).replace("\n", '')
            chromeVer = chromeVer.split('Google Chrome ')[1].strip()
            chromeVer3 = chromeVer.replace(chromeVer.split(".")[3], '')
            # print("浏览器版本：", chromeVer3)

            # 2 驱动路径
            currPath = varDriverPath + chromeVer3
            # print(currPath)  # /Users/linghuchong/.wdm/drivers/chromedriver/mac64/135.0.7049.

            # 3 检查chromedriver主版本是否存在
            if os.path.isdir(currPath) == False:
                print("chromedriver downloading...")
                Service(ChromeDriverManager().install())
                print("done")
                l_folder = os.listdir(varDriverPath)
                for i in range(len(l_folder)):
                    if chromeVer3 in l_folder[i]:
                        os.rename(varDriverPath + l_folder[i], varDriverPath + chromeVer3)
                        break
                os.chdir(varDriverPath + chromeVer3 + "/chromedriver-mac-x64")
                os.system("chmod 775 chromedriver")
                # os.system("chmod 775 THIRD_PARTY_NOTICES.chromedriver")
                print(currPath + "/chromedriver-mac-x64/chromedriver")  # /Users/linghuchong/.wdm/drivers/chromedriver/mac64/135.0.7049./chromedriver-mac-x64/chromedriver
                currPath = currPath + "/chromedriver-mac-x64/chromedriver"
                s = Service(executable_path=currPath, service_args=["--verbose"], log_output='Web_chromedriver_mac.log')
                self.driver = webdriver.Chrome(service=s, options=options)
                print("浏览器版本：", self.driver.capabilities['browserVersion'])  # 114.0.5735.198  //浏览器版本
                print("chromedriver版本：", self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # 114.0.5735.90  //chrome驱动版本
            else:
                currPath = currPath + "/chromedriver-mac-x64/chromedriver"
                # self.driver = webdriver.Chrome(service=s, options=options)
                # from webdriver_manager.chrome import ChromeDriverManager
                # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                s = Service(executable_path=currPath, service_args=["--verbose"],log_output='Web_chromedriver_mac.log')
                # s = Service(executable_path='/usr/local/bin/chromedriver', service_args=["--verbose"],log_output='chromedriver_verbose.log')
                self.driver = webdriver.Chrome(service=s, options=options)
                # print("浏览器版本：",self.driver.capabilities['browserVersion'])  # 114.0.5735.198  //浏览器版本
                # print("chromedriver版本：",self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # 114.0.5735.90  //chrome驱动版本



            # try:
            #     self.driver = webdriver.Chrome(service=s, options=options)
            # except:
            #     # 下载失败通过网站下载文件
            #     print("chromedriver updated failed!")
            #     print("download from https://googlechromelabs.github.io/chrome-for-testing/#stable")
            #     sys.exit(0)
            #     # shutil.rmtree("/Users/linghuchong/.wdm/drivers/chromedriver/mac64/" + chromeVer3)
            #     # os.mkdir("/Users/linghuchong/.wdm/drivers/chromedriver/mac64/" + chromeVer3)
            #     # os.chdir("/Users/linghuchong/.wdm/drivers/chromedriver/mac64/" + chromeVer3)
            #     # print(os.getcwd())
            #     # os.system("curl -o chromedriver-mac-x64.zip https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.88/mac-x64/chromedriver-mac-x64.zip")
            #     # shutil.unpack_archive('./chromedriver-mac-x64.zip', './', 'zip')
            #     # # sys.exit(0)

    def load_cookies(self, driver, file_path):
        """从文件加载 Cookies 到当前会话"""
        try:
            with open(file_path, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except FileNotFoundError:
            print("未找到保存的 Cookies 文件。")




    def getSource(self):
        # 1. 获取源码
        return self.driver.page_source

    def opnLabel(self, varURL, t=2):
        # 1.2 打开标签页，获取链接和句柄字典
        # 创建URL与句柄的字典
        d_url_handle = {}
        self.driver.execute_script('window.open("' + varURL + '");')
        sleep(t)
        l_handles = self.driver.window_handles
        d_url_handle[varURL] = l_handles[-1]
        return d_url_handle


    def swhLabelByLoc(self, varLoc, t=1):
        # 1.3 通过位置切换标签页
        # self.swhLabel(0) # 0 = 激活第一个标签页 ， 1 = 激活第二个标签页 , 以此类推。
        l_handles = self.driver.window_handles
        # print(l_handles)
        sleep(t)
        self.driver.switch_to.window(l_handles[varLoc])

    def swhLabelByHandle(self, varHandle, t=1):
        # 1.3 通过handle切换标签页
        # self.swhLabelByHandle('C40A2687783C79C8CF72F617DB52CC11')
        self.driver.switch_to.window(varHandle)
        sleep(t)

    def cls(self):
        # 1.4 关闭窗口
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def refresh(self):
        # 刷新页面
        self.driver.refresh()



    def getBrowserSize(self):
        # 2.1 获取当前浏览器宽高
        d_size = self.driver.get_window_size()  # {'width': 1936, 'height': 1056}
        return d_size
        # return (d_size["width"] - 16, d_size["height"] + 24)

    def setBrowserSize(self, width, height):
        # 2.2 设置浏览器分辨率
        # Web_PO.setBrowserSize(1366, 768) # 按分辨率1366*768打开浏览器
        self.driver.set_window_size(width, height)

    def setBrowserMax(self):
        # 2.3 设置浏览器全屏
        self.driver.maximize_window()

    def zoom(self, percent, t=2):
        # 2.4 缩放页面内容比率
        # zoom(50) 内容缩小50%
        self.driver.execute_script("document.body.style.zoom='" + str(percent) + "%'")
        sleep(t)

    def getBrowserScreen(self, varImageFile="browser.png"):
        # 2.5 截取浏览器内屏幕
        # getBrowserScreen("d:\\screenshot.png")
        try:
            self.driver.get_screenshot_as_file(varImageFile)
        except:
            print("error, 请检查浏览器是否打开！")

    def scrollBottom(self, t=2):
        # 2.6 页面滚动条到底部
        sleep(2)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(t)


    def popupAlert(self, varText, t=1):
        # 3.1 弹出框
        # 注意这里需要转义引号
        self.driver.execute_script("alert('" + varText + "');")
        sleep(t)

    def confirmAlert(self, varOperate, t=1):
        # 3.2 确认弹出框
        if varOperate == "accept":
            self.driver.switch_to.alert.accept()
            sleep(t)
        if varOperate == "dismiss":
            self.driver.switch_to.alert.dismiss()
            sleep(t)
        if varOperate == "text":
            x = self.driver.switch_to.alert.text
            self.driver.switch_to.alert.accept()
            return x


    def kilBrowser(self):
        # 4.1 关闭浏览器应用
        self.driver.quit()


    def scrollLeftByApp(self, location, t=1):
        # 5.1 app屏幕左移
        # Web_PO.scrollLeftByApp('1000')  # 屏幕向左移动1000个像素
        self.driver.execute_script("var q=document.documentElement.scrollLeft=" + location)
        sleep(t)

    def scrollRightByApp(self, location, t=1):
        # 5.2 app屏幕右移
        # Web_PO.scrollRightByApp('1000', 2)  # 屏幕向右移动1000个像素
        self.driver.execute_script("var q=document.documentElement.scrollRight=" + location)
        sleep(t)

    def scrollUpByApp(self, location, t=1):
        # 5.3 app屏幕上移
        # Web_PO.scrollUpByApp("1000",2) # 屏幕向上移动1000个像素
        # self.driver.execute_script("var q=document.body.scrollTop=" + location)
        self.driver.execute_script("var q=document.documentElement.scrollTop=" + location)
        sleep(t)

    def scrollDownByApp(self, location, t=1):
        # 5.4 app屏幕下移
        # Web_PO.scrollDownByApp("1000",2) # 屏幕向下移动1000个像素
        self.driver.execute_script("var q=document.documentElement.scrollDown=" + location)
        sleep(t)


    def scrollIntoView(self, varXpath, t=1):
        # 元素拖动到可见的元素
        element = self.driver.find_element_by_xpath(varXpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(t)

    def scrollTopById(self, varId, t=1):
        # 2.10 内嵌窗口中滚动条操作
        # 若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
        # self.screenTopId("zy.android.healthstatisticssystem:id/vp_content",2)
        js = "var q=document.getElementById('" + varId + "').scrollTop=100000"
        self.driver.execute_script(js)
        sleep(t)

    def getCode(self, capScrnPic, xStart, yStart, xEnd, yEnd):
        """8 获取验证码 ？？"""
        # Level_PO.getCode(u"test.jpg",2060, 850, 2187, 900）
        # 注：地址是图片元素中的位置。
        self.driver.save_screenshot(capScrnPic)
        i = Image.open(capScrnPic)
        frame4 = i.crop((xStart, yStart, xEnd, yEnd))
        frame4.save(capScrnPic)
        # im = Image.open(capScrnPic)
        # imgry = im.convert('L')
        # # 去噪,G = 50,N = 4,Z = 4
        # self.clearNoise(imgry, 50, 0, 4)
        # # imgry.save(capScrnPic)
        # filename = self.saveAsBmp(capScrnPic)
        # self.RGB2BlackWhite(filename)
        # im = Image.open(capScrnPic)
        # imgry = im.convert('L')
        # ''''''''''''''''''''''''''''''''''''''
        img = Image.open(capScrnPic)
        img = img.convert("RGBA")
        pixdata = img.load()

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][0] < 90:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][1] < 136:
                    pixdata[x, y] = (0, 0, 0, 255)

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        img.save(capScrnPic)
        im = Image.open(capScrnPic)
        imgry = im.resize((1000, 500), Image.NEAREST)
        return image_to_string(imgry)

    def dynamicLoadToEnd(self, varClassValue):

        """2.3 动态加载页面滚动到底部（加载所有数据）????

        varClassValue 参数是所需加载数据，如list中class值
        Web_PO.driver.find_elements(By.CLASS_NAME, "Eie04v01")
        return: 返回所需加载数据的数量
        """

        # dynamicLoadToEnd('Eie04v01')
        num, len_now = 0, 0
        _input = self.driver.find_element(By.TAG_NAME, "body")
        while True:
            _input.send_keys(Keys.PAGE_DOWN)
            self.driver.implicitly_wait(2)
            elem = self.driver.find_elements(By.CLASS_NAME, varClassValue)
            len_cur = len(elem)
            # print(len_now, len_cur)
            if len_now != len_cur:
                len_now = len_cur
                num = 0
            elif len_now == len_cur and num <= 2:
                num = num + 1
                sleep(0.5)
            else:
                sleep(2)
                break
        return len_cur



    # test_count = 10
    def click_random_element(self):
        # 点击随机元素

        action_type = "点击随机元素"
        try:
            # 查找所有可点击的元素
            clickable_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a, button, input[type="submit"]')
            if clickable_elements:
                random_element = random.choice(clickable_elements)
                # 获取元素的 XPath 地址
                element_xpath = self.get_element_xpath(random_element)
                element_text = random_element.text if random_element.text else "无文本内容"
                logging.info(f"操作类型: {action_type}, 输入: 点击元素 - XPath: {element_xpath}, 文本内容: {element_text}")
                random_element.click()
                logging.info(f"操作类型: {action_type}, 结果: 成功")
            else:
                logging.info(f"操作类型: {action_type}, 结果: 未找到可点击元素")
        except Exception as e:
            logging.error(f"操作类型: {action_type}, 结果: 出错 - {e}")

    # 1 usage
    def input_random_text(self):
        # 输入随机文本
        action_type = "输入随机文本"
        try:
            # 查找所有输入框
            input_elements = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"], textarea')
            if input_elements:
                random_input = random.choice(input_elements)
                # 获取输入框元素的 XPath 地址
                input_xpath = self.get_element_xpath(random_input)
                random_text = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
                logging.info(f"操作类型: {action_type}, 输入: 在 XPath 为 {input_xpath} 的输入框输入 - {random_text}")
                random_input.send_keys(random_text)
                logging.info(f"操作类型: {action_type}, 结果: 成功")
            else:
                logging.info(f"操作类型: {action_type}, 结果: 未找到输入框")
        except Exception as e:
            logging.error(f"操作类型: {action_type}, 结果: 出错 - {e}")

    # 1 usage
    def scroll_page(self):
        action_type = "滚动页面"
        try:
            # 随机滚动页面
            scroll_distance = random.randint(100, 500)
            logging.info(f"操作类型: {action_type}, 输入: 滚动距离 - {scroll_distance}")
            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            logging.info(f"操作类型: {action_type}, 结果: 成功")
        except Exception as e:
            logging.error(f"操作类型: {action_type}, 结果: 出错 - {e}")


    def get_element_xpath(self, element):
        """
        获取元素的 XPath 地址
        """
        xpath = self.driver.execute_script('''
            var getPathTo = function (element) {
                if (element.id!=='') {
                    return '//*[@id="' + element.id + '"]';
                }

                if (element === document.body) {
                    return element.tagName;
                }

                var ix = 0;
                var siblings = element.parentNode.childNodes;
                for (var i = 0; i < siblings.length; i++) {
                    var sibling = siblings[i];
                    if (sibling === element) {
                        return getPathTo(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
                    }

                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                        ix++;
                    }
                }
            };
            return getPathTo(arguments[0]);
        ''', element)
        return xpath


if __name__ == "__main__":

    # todo main
    Web_PO = WebPO("chrome")
    # Web_PO = WebPO("noChrome")
    # Web_PO = WebPO("firefox")

    # # print("1.1 打开网站".center(100, "-"))
    Web_PO.openURL("https://www.baidu.com")
    # Web_PO.openURL("https://quote.eastmoney.com/sz002132.html#fullScreenChart")
    # Web_PO.clkByX("/html/body/div[1]/div[3]/form/input")

    # Web_PO.clkByX("/html/body/article/section/div/div/div/div/div/div[1]/div[2]/form/div/div[1]/div/div/select")
    # Web_PO.sltTextByX("/html/body/article/section/div/div/div/div/div/div[1]/div[2]/form/div/div[1]/div/div/select", '健康干预')
    # Web_PO.sltValueByX("/html/body/article/section/div/div/div/div/div/div[1]/div[2]/form/div/div[1]/div/div/select", 'none')
    # Web_PO.sltIndexByX("/html/body/article/section/div/div/div/div/div/div[1]/div[2]/form/div/div[1]/div/div/select", 3)
    # assert s.first_selected_option.text == '健康干预_已患疾病组合'

    # 定位下拉框
    # dropdown = Select(driver.find_element("id", "dropdown_id"))
    #   # 通过以下三种方式选择单个选项
    # dropdown.select_by_visible_text("Option Text")  # 根据选项文本选择
    # dropdown.select_by_value("option_value")  # 根据选项的 value 属性选择
    # dropdown.select_by_index(2)  # 根据选项的索引（从 0 开始）选择
    #   # 验证选择
    # assert dropdown.first_selected_option.text == "Option Text"

    # Web_PO.setTextByX("/html/body/div[2]/div[2]/div[2]/div/div[2]/form/div/div/input", "drissionpage")
    # Web_PO.clkByX("/html/body/div[2]/div[2]/div[2]/div/div[2]/form/div/div/button", 2)
    # a = Web_PO.getAttrValueListByX("//div[@class='card-body']/h4/a", "href")
    # print(a)
    # b= Web_PO.getTextListByX("//div[@class='card-body']/h4/a")
    # print(b)
    # Web_PO.openURL("https://kyfw.12306.cn/otn/resources/login.html")
    # Web_PO.openURL("https://www.xvideos.com/video76932809/_")
    # Xvideos_PO.getInfo("https://www.xvideos.com/video76932809/_")

    # # print("1.2 打开标签页".center(100, "-"))
    # Web_PO.openLabel("http://www.jd.com")

    # # print("1.3 切换标签页".center(100, "-"))
    # Web_PO.switchLabel(0)

    # print("1.4 获取当前浏览器宽高".center(100, "-"))
    # print(Web_PO.getBrowserSize())  # (1536, 824)

    # print("1.5 截取浏览器内屏幕".center(100, "-"))
    # Web_PO.getBrowserScreen("d:/222333browserScreen.png")

    # # print("2.0 指定分辨率浏览器".center(100, "-"))
    # Web_PO.setBrowser(1366, 768)

    # # print("2.1 全屏浏览器".center(100, "-"))
    # Web_PO.maxBrowser()

    # # print("2.2 缩放页面比率".center(100, "-"))
    # Web_PO.zoom(20)
    # Web_PO.zoom(220)

    # print("2.3 动态加载页面滚动到底部（加载所有数据）".center(100, "-"))
    # Web_PO.openURL('https://www.douyin.com/user/MS4wLjABAAAARzph2dTaIfZG4w_8czG9Yf5YiqHqc7RGXrqUM3fHtBU?vid=7180299495916326181')
    # qty = Web_PO.dynamicLoadToEnd('Eie04v01')  # 动态加载页面直到最后一个 类与实例=Eie04v01 ,并返回加载的数量。
    # print(qty)
    # text = Web_PO.driver.page_source
    # text = bs4.BeautifulSoup(text, 'lxml')
    # link = text.find_all('a')
    # for a in link:
    #     href = a['href']
    #     if "/video" in href:
    #         print("https://www.douyin.com" + href)

    # # print("2.4 页面滚动条到底部".center(100, "-"))
    # Web_PO.openURL('https://baijiahao.baidu.com/s?id=1753450036624046728&wfr=spider&for=pc')
    # sleep(2)
    # Web_PO.scrollToEnd(2)

    # print("2.5 app屏幕左移".center(100, "-"))
    # Web_PO.scrollLeft('1000',9)

    # print("2.6 app屏幕右移".center(100, "-"))
    # Web_PO.scrollRight('1000', 5)

    # print("2.7 app屏幕上移".center(100, "-"))
    # Web_PO.scrollTop('1000', 5)

    # print("2.8 app屏幕下移".center(100, "-"))
    # Web_PO.scrollDown('1000', 5)

    # print("2.9 元素拖动到可见的元素".center(100, "-"))
    # Web_PO.scrollIntoView(varXpath)

    # print("2.10 内嵌窗口中滚动条操作".center(100, "-"))
    # Web_PO.scrollTopById(varId)

    # # print("3.1 弹出框".center(100, "-"))
    # Web_PO.popupAlert("你好吗？")

    # # print("3.2 确认弹出框".center(100, "-"))
    # Web_PO.confirmAlert("accept", 2)
    # Web_PO.confirmAlert("dismiss", 2)
    # print(Web_PO.confirmAlert("text", 2))

    # print("4.1 关闭当前窗口".center(100, "-"))
    # Web_PO.close()
    #
    # print("4.2 退出浏览器应用".center(100, "-"))
    # Web_PO.quit()
