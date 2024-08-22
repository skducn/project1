# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Created on : 2018-7-2
# Description: Web 对象层 （selenium 4.4.3）
# pip install opencv_python    // cv2

# https://www.cnblogs.com/FBGG/p/17975814
# selenium并不支持获取响应的数据，我们可以使用selenium-wire库，selenium-wire扩展了 Selenium 的 Python 绑定，可以访问浏览器发出的底层请求。seleniumwire只兼容Selenium 4.0.0+，
# pip install selenium-wire
# ***************************************************************
# todo selenium
# 查看版本：pip list | grep selenium 或 pip show selenium
# 查看可安装版本：pip install selenium==
# 安装指定版本：pip install selenium==4.4.3
# 注：selenium 4.10 会引起浏览器自动关闭现象，实测安装4.4.3 正常


# todo chrome
# 1，查看版本：chrome://version
# print(self.driver.capabilities['browserVersion'])  # 114.0.5735.198  //获取浏览器版本
# print(self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # 114.0.5735.90  //获取chrome驱动版本
# 注：以上两版本号前3位一样就可以，如 114.0.5735

# 2，下载驱动
# 下载1：https://googlechromelabs.github.io/chrome-for-testing/#stable （新）
# https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/mac-x64/chrome-mac-x64.zip
# 下载2：http://chromedriver.storage.googleapis.com/index.html （旧）
# 下载3：https://registry.npmmirror.com/binary.html?path=chromedriver （旧）

# 3，自动下载驱动
# from webdriver_manager.chrome import ChromeDriverManager
# ChromeDriverManager().install()
# self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# mac系统默认调用路径：/Users/linghuchong/.wdm/drivers/chromedriver/mac64/120.0.6099.109/chromedriver-mac-x64/chromedriver

# 4, 设置配置
# for win 路径：C:\Python38\Scripts\chromedrive.exe
# for mac 路径：
# from selenium.webdriver.chrome.service import Service
# self.driver = webdriver.Chrome(service=Service("/Users/linghuchong/Downloads/51/Python/project/instance/web/chromedriver"), options=options)

# 5，options参数
# https://www.bilibili.com/read/cv25916901/
# https://blog.csdn.net/xc_zhou/article/details/82415870
# https://blog.csdn.net/amberom/article/details/107980370
# https://www.5axxw.com/questions/content/ey8x1v  解决不安全下载被阻止问题
# 6，常见问题
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
import requests, bs4, subprocess

from PO.FilePO import *
File_PO = FilePO()

class WebPO(DomPO):

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
            # for win
            chromeVer = subprocess.check_output(
                "powershell -command \"&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}\"",
                shell=True)
            chromeVer = bytes.decode(chromeVer).replace("\n", '')
            chromeVer3 = chromeVer.replace(chromeVer.split(".")[3], '')  # 120.0.6099.
            defaultPath = "C:\\Users\\jh\\.wdm\\drivers\\chromedriver\\win64\\"
            s = Service(defaultPath + chromeVer3 + "\\chromedriver-win32\\chromedriver.exe")
        elif os.name == "posix":
            # for mac
            chromeVer = subprocess.check_output(
                "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version", shell=True)
            chromeVer = bytes.decode(chromeVer).replace("\n", '')
            chromeVer = chromeVer.split('Google Chrome ')[1].strip()
            # print("chromeVer:", chromeVer)  # 120.0.6099.129
            chromeVer3 = chromeVer.replace(chromeVer.split(".")[3], '')
            # print("chromeVer3 => ", chromeVer3)  # 120.0.6099.
            defaultPath = "/Users/linghuchong/.wdm/drivers/chromedriver/mac64/"
            currPath = defaultPath + chromeVer3
            # print(currPath)  # /Users/linghuchong/.wdm/drivers/chromedriver/mac64/127.0.6533.

            # 3 检查chromedriver主版本是否存在
            if os.path.isdir(currPath) == False:
                # 自动下载chrome驱动并修改成主板本
                print("chromedriver downloading ...")
                Service(ChromeDriverManager().install())
                l_folder = os.listdir(defaultPath)
                # print(l_folder)  # ['.DS_Store', '127.0.6533.88', '126.0.6478.']
                for i in range(len(l_folder)):
                    if chromeVer3 in l_folder[i]:
                        os.rename(defaultPath + l_folder[i], defaultPath + chromeVer3)
                        break
                os.chdir("/Users/linghuchong/.wdm/drivers/chromedriver/mac64/" + chromeVer3 + "/chromedriver-mac-x64")
                os.system("chmod 775 chromedriver")
                # os.system("chmod 775 THIRD_PARTY_NOTICES.chromedriver")

            s = Service(currPath + "/chromedriver-mac-x64/chromedriver")
            self.driver = webdriver.Chrome(service=s, options=options)
            # print("chromeVer:", self.driver.capabilities['browserVersion'])  # 115.0.5790.170  //获取浏览器版本
            # print("chromedriver:", self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # 115.0.5790.170 //获取chrome驱动版本


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

    def _openURL(self, varURL):

        # 1.1 打开

        if self.driver == "chrome":

            # 1 配置项
            options = Options()

            # todo 屏幕
            options.add_argument("--start-maximized")  # 最大化浏览器
            # options.add_argument("--start-fullscreen")  # 全屏模式，F11可退出
            # options.add_argument("--kiosk")  # 全屏模式，alt+tab切换。ctrl+f4退出
            # options.add_argument('--window-size=%s,%s' % (pyautogui.size()[0], pyautogui.size()[1])) # 指定窗口大小
            # width, height = pyautogui.size()  # 1440 900  //获取屏幕尺寸

            # todo 浏览器
            options.add_experimental_option("detach", True)  # 浏览器永不关闭
            options.add_argument("--allow-running-insecure-content") # Allow insecure content
            # options.add_argument("--unsafely-treat-insecure-origin-as-secure=http://192.168.0.243:8010/")  # Replace example.com with your site's domain (this is what worked for me)

            options.add_argument("--disable-blink-features=AutomationControlled")  # 禁止浏览器出现验证滑块
            options.add_argument('--incognito')  # 无痕模式

            options.add_argument('--disable-popup-blocking')  # 禁用弹窗阻止（可能有助于避免某些弹窗相关的崩溃）
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽--ignore-certificate-errors提示信息的设置参数项
            options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 屏蔽 "Chrome正受到自动测试软件的控制"提示，建议放在最后。
            # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片（提升速度）
            options.add_argument('--hide-scrollbars')  # 隐藏滚动条（因对一些特殊页面）
            # options.headless = True  # 无界面模式
            # options.add_argument("--lang=en")  # 指定浏览器的语言，避免出现“询问是否翻译非您所用语言的网页”

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

            # # 绕过检测（滑动验证码）
            # self.driver.execute_cdp_cmd("Page.addScriptToEvaluteOnNewDocument", {"source": """Object.defineProperty(navigator,'webdriver', {get: () => undefined})"""})

            self.driver.get(varURL)
            return self.driver

        elif self.driver == "noChrome":

            # 1 配置项
            options = Options()
            options.headless = True  # 无界面模式

            # todo 系统
            # options.add_argument("disable-cache")  # 禁用缓存
            # options.add_argument("--disable-extensions")  # 禁用所有插件和扩展（提高稳定性，有时插件可能引起稳定性问题）
            options.add_argument('--no-sandbox')  # 关闭沙盒模式（沙盒模式提一种提高安全性的技术，但可能与某系统不兼容，关闭可能会降低浏览器的安全性）
            options.add_argument('-disable-dev-shm-usage')  # 禁用/dev/shm使用（可减少内存使用，但影响性能）
            # options.add_argument('--disable-gpu')  # 禁用GPU加速（虽然GPU加速可以提高性能，但有些情况下会导致崩溃）
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
            # options.add_argument('--disable-logging')  # 禁用日志记录（减少日志记录的资源消耗）
            # options.add_argument('--disable-javascript')  # 禁用JavaScript（有时可以用来测试JavaScript相关的问题）
            # options.add_argument(r"--user-data-dir=c:\selenium_user_data")  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题

            # 更新下载chromedriver
            self.updateChromedriver(options)

            # # 绕过检测（滑动验证码）
            # self.driver.execute_cdp_cmd("Page.addScriptToEvaluteOnNewDocument", {"source": """Object.defineProperty(navigator,'webdriver', {get: () => undefined})"""})

            self.driver.get(varURL)
            return self.driver


        # elif self.driver == "firefox":
        #     if platform.system() == "Windows":
        #         # profile = webdriver.FirefoxProfile()
        #         # # profile = FirefoxProfile()
        #         # profile.native_events_enabled = True
        #         # # self.driver = Firefox(profile)
        #         # profile.set_preference("browser.startup.homepage", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
        #         # profile.set_preference("startup.homepage_welcome_url", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
        #         # profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
        #         # profile.assume_untrusted_cert_issuer = True  # 访问没有证书的https站点
        #         # accept_untrusted_certs = True  # 访问没有证书的https站点
        #         # profile.set_preference('permissions.default.image', 2)  # 不加载的图片，加快显示速度
        #         # profile.set_preference('browser.migration.version', 9001)  # 不加载过多的图片，加快显示速度
        #         # self.driver = webdriver.Firefox(profile)
        #         self.driver = webdriver.Firefox()
        #         self.driver.implicitly_wait(10)  # 隐性等待
        #         self.driver.get(varURL)
        #     elif platform.system() == "Darwin":
        #         options = webdriver.FirefoxOptions()
        #         options.add_argument("--start-maximized")  # 最大化浏览器
        #         # options.add_argument("--start-fullscreen")  # 全屏模式，F11可退出
        #         # options.add_argument("-headless")
        #         options.add_argument("--disable-gpu")
        #
        #         self.driver = webdriver.Firefox(
        #             # firefox_profile=None,
        #             # firefox_binary=None,
        #             # # timeout=30,
        #             # capabilities=None,
        #             # proxy=None,
        #             # executable_path="/usr/local/bin/geckodriver",
        #             # log_path="geckodriver.log",
        #             options=options
        #         )
        #         # self.driver._is_remote = False  # 解决mac电脑上传图片问题
        #         # self.driver.implicitly_wait(10)  # 隐性等待
        #         self.driver.get(varURL)
        #     return self.driver

    def openURL(self, varURL):
        self._openURL(varURL)


    def opn(self, varUrl, t=1):
        """1.1 打开网页"""
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(varUrl)
        sleep(t)

    def getSource(self):
        """1. 获取源码"""
        return self.driver.page_source


    def opnLabel(self, varURL, t=2):

        ''' 1.2 打开标签页 '''

        self.driver.execute_script('window.open("' + varURL + '");')
        sleep(t)

    def swhLabel(self, varSwitch, t=1):

        '''
        1.3 切换标签页
        # self.swhLabel(0) # 0 = 激活第一个标签页 ， 1 = 激活第二个标签页 , 以此类推。
        '''

        all_handles = self.driver.window_handles
        sleep(t)
        self.driver.switch_to.window(all_handles[varSwitch])

    def cls(self):

        '''
        1.4 关闭当前窗口
        :return:
        '''

        self.driver.close()

    def refresh(self):
        """刷新页面"""
        self.driver.refresh()

    def getBrowserSize(self):

        '''
        2.1 获取当前浏览器宽高
        :return:
        '''

        d_size = self.driver.get_window_size()  # {'width': 1936, 'height': 1056}
        return d_size
        # return (d_size["width"] - 16, d_size["height"] + 24)

    def setBrowserSize(self, width, height):

        '''
        2.2 设置浏览器分辨率
        :param width: 1366
        :param height: 768
        :return:
        # Web_PO.setBrowser(1366, 768) # 按分辨率1366*768打开浏览器
        '''

        self.driver.set_window_size(width, height)

    def setBrowserMax(self):

        '''
        2.3 设置浏览器全屏
        :return:
        '''

        self.driver.maximize_window()

    def zoom(self, percent):

        '''
        2.4 缩放页面内容比率
        :param percent:  50
        :return:
        30表示内容缩小到 50%
        '''

        self.driver.execute_script("document.body.style.zoom='" + str(percent) + "%'")

    def getBrowserScreen(self, varImageFile="browser.png"):

        '''
        2.5 截取浏览器内屏幕
        :param varImageFile:  "d:\\screenshot.png"
        :return:
        前置条件：先打开浏览器后才能截屏.
        '''

        try:
            self.driver.get_screenshot_as_file(varImageFile)
        except:
            print("error, 请检查浏览器是否打开！")

    def scrollBottom(self, t=2):

        '''
        2.6 页面滚动条到底部
        :param t:
        :return:
        '''

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        sleep(t)



    def popupAlert(self, varText, t=1):

        '''
        3.1 弹出框
        :param varText:
        :param t:
        :return:
        '''

        # 注意这里需要转义引号
        self.driver.execute_script("alert('" + varText + "');")
        sleep(t)

    def confirmAlert(self, varOperate, t=1):

        '''
        3.2 确认弹出框
        :param operate:
        :param t:
        :return:
        '''

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

        '''
        4.1 关闭浏览器应用
        :return:
        '''

        self.driver.quit()


    def scrollLeftByApp(self, location, t=1):

        '''
        5.1 app屏幕左移
        :param location: "1000"
        :param t:
        :return:
         # Web_PO.scrollLeft('1000')  # 屏幕向左移动1000个像素
        '''

        self.driver.execute_script("var q=document.documentElement.scrollLeft=" + location)
        sleep(t)

    def scrollRightByApp(self, location, t=1):

        '''
        5.2 app屏幕右移
        :param location: "1000"
        :param t:
        :return:
        Web_PO.scrollRight('1000', 2)  # 屏幕向右移动1000个像素
        '''

        self.driver.execute_script("var q=document.documentElement.scrollRight=" + location)
        sleep(t)

    def scrollUpByApp(self, location, t=1):

        '''
        5.3 app屏幕上移
        :param location: :1000
        :param t:
        :return:
        Web_PO.scrollTop("1000",2) # 屏幕向上移动1000个像素
        '''

        # self.driver.execute_script("var q=document.body.scrollTop=" + location)
        self.driver.execute_script("var q=document.documentElement.scrollTop=" + location)
        sleep(t)

    def scrollDownByApp(self, location, t=1):

        '''
        5.4 app屏幕下移
        :param location:
        :param t:
        :return:
        Web_PO.scrollDown("1000",2) # 屏幕向下移动1000个像素
        '''

        self.driver.execute_script("var q=document.documentElement.scrollDown=" + location)
        sleep(t)



    def scrollIntoView(self, varXpath, t=1):

        '''
        元素拖动到可见的元素
        :param varXpath:
        :param t:
        :return:
        '''

        element = self.driver.find_element_by_xpath(varXpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        sleep(t)

    def scrollTopById(self, varId, t=1):

        """2.10 内嵌窗口中滚动条操作"""

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


if __name__ == "__main__":

    # todo main
    Web_PO = WebPO("chrome")
    # Web_PO = WebPO("noChrome")
    # Web_PO = WebPO("firefox")

    # # print("1.1 打开网站".center(100, "-"))
    Web_PO.openURL("https://gitee.com/explore")
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
