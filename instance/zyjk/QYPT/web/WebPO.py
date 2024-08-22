# -*- coding: utf-8 -*-
# ***************************************************************
# Author     : John
# Created on : 2018-7-2
# Description: Web 对象层
# ***************************************************************
# selenium
# 查看可安装的selenium版本， pip install selenium==
# 注：部分新版本 selenium 4.10 会引起浏览器自动关闭现象，实测建议安装4.4.3, pip install selenium==4.4.3

# pip install opencv_python    // cv2
# ***************************************************************
# chrome
# 1，查看Chrome浏览器版本，chrome://version
# print(driver.capabilities['browserVersion'])  # 浏览器版本，如：114.0.5735.198
# print(driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])  # chrome驱动版本，如：114.0.5735.90
# 以上两版本号前3位一样就可以，如 114.0.5735

# 2，下载及配置 chromedriver 驱动
# 下载1：http://chromedriver.storage.googleapis.com/index.html
# 下载2：https://npm.taobao.org/mirrors/chromedriver
# 系统默认调用路径：C:\Python38\Scripts\chromedrive.exe
# 自定义调用路径：
# from selenium.webdriver.chrome.service import Service
# driver = webdriver.Chrome(service=Service("/Users/linghuchong/Downloads/51/Python/project/instance/web/chromedriver"), options=options)

# 3，chrome的options参数
# https://blog.csdn.net/xc_zhou/article/details/82415870
# https://blog.csdn.net/amberom/article/details/107980370

# Q1：MAC 移动chromedriver时报错，如 sudo mv chromedriver /usr/bin 提示： Operation not permitted
# A1: 重启按住command + R,进入恢复模式，实用工具 - 终端，输入 csrutil disable , 重启电脑。
# ***************************************************************

# firefox
# geckodriver 0.14.0 for selenium3.0
# 下载地址：https://github.com/mozilla/geckodriver/releases
# ff 66.0.4 (64 位) , selenium =3.141.0，gecko = 0.24.0
# geckodriver下载：https://github.com/mozilla/geckodriver/releases

# Q1：WebDriverException:Message:'geckodriver'executable needs to be in Path
# A1：geckodriver是原生态的第三方浏览器，对于selenium3.x版本使用geckodriver来驱动firefox，需下载geckodriver.exe,下载地址：https://github.com/mozilla/geckodriver/releases
# 将 geckodriver 放在 C:\Python38\Scripts
# ***************************************************************


"""
1.1 打开网站 open()
1.2 打开标签页 openLabel("http://www.jd.com")
1.3 切换标签页 switchLabel(1)
1.4 关闭当前窗口 close()

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
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.common.action_chains import ActionChains
# # from selenium.webdriver.support.select import Select
# # from selenium.webdriver.support.wait import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# from PIL import ImageGrab
# import cv2, requests, bs4
# # from pytesseract import *
# from PIL import Image, ImageDraw, ImageGrab
# import pyautogui


class WebPO(DomPO):


    def _openURL(self, varURL):

        """1.1 打开"""

        if self.driver == "firefox":
            if platform.system() == "Windows":
                # profile = webdriver.FirefoxProfile()
                # # profile = FirefoxProfile()
                # profile.native_events_enabled = True
                # # self.driver = Firefox(profile)
                # profile.set_preference("browser.startup.homepage", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
                # profile.set_preference("startup.homepage_welcome_url", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
                # profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")  # 解决跳转到firefox官网指定页，过慢问题。
                # profile.assume_untrusted_cert_issuer = True  # 访问没有证书的https站点
                # accept_untrusted_certs = True  # 访问没有证书的https站点
                # profile.set_preference('permissions.default.image', 2)  # 不加载的图片，加快显示速度
                # profile.set_preference('browser.migration.version', 9001)  # 不加载过多的图片，加快显示速度
                # self.driver = webdriver.Firefox(profile)
                self.driver = webdriver.Firefox()
                self.driver.implicitly_wait(10)  # 隐性等待
                self.driver.get(varURL)
            elif platform.system() == "Darwin":
                self.driver = webdriver.Firefox(
                    firefox_profile=None,
                    firefox_binary=None,
                    timeout=30,
                    capabilities=None,
                    proxy=None,
                    executable_path="/usr/local/bin/geckodriver",
                    firefox_options=None,
                    log_path="geckodriver.log",
                )
                self.driver._is_remote = False  # 解决mac电脑上传图片问题
                self.driver.implicitly_wait(10)  # 隐性等待
                self.driver.get(varURL)
            return self.driver

        if self.driver == "chrome":
            options = Options()
            # option = webdriver.ChromeOptions()

            options.add_argument("--start-maximized")  # 最大化
            # driver_width, driver_height = pyautogui.size()  # 通过pyautogui方法获得屏幕尺寸
            # print(driver_width, driver_height)
            # option.add_argument('--window-size=%sx%s' % (driver_width, driver_height))

            # option.add_argument(
            #     "--disable-blink-features=AutomationControlled"
            # )  # 禁止浏览器出现验证滑块
            # options.add_argument(
            #     r"--user-data-dir=c:\selenium_user_data"
            # )  # 设置用户文件夹，可存储登录信息，解决每次要求登录问题
            # option.add_argument('--incognito')  # 无痕隐身模式
            # # option.add_argument('disable-infobars')  # 不显示 Chrome正在受到自动软件的控制的提示（已废弃，替代者excludeSwitches）
            options.add_argument("disable-cache")  # 禁用缓存
            # # option.add_argument('--ignore-certificate-errors')
            # option.add_argument("--disable-extensions")  # 禁用扩展插件的设置参数项
            # option.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # 屏蔽--ignore-certificate-errors提示信息的设置参数项
            options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )  # 不显示 chrome正受到自动测试软件的控制的提示
            # option.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁止打印日志
            # option.headless = True  # 无界面模式
            options.add_argument('--no-sandbox')  # 解决文件不存咋的报错
            options.add_argument('-disable-dev-shm-usage')  # 解决DevToolsActivePort文件不存咋的报错
            options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
            options.add_argument('--hide-scrollbars')  # 隐藏滚动条，因对一些特殊页面
            options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升速度
            # self.driver = webdriver.Chrome(options=option)
            # ver1 = self.driver.capabilities['browserVersion']
            # ver2 = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
            # print(ver1)
            # print(ver2)

            s = Service("/Users/linghuchong/Downloads/51/Python/project/instance/web/chromedriver")
            # self.driver = webdriver.Chrome(executable_path="/Users/linghuchong/miniconda3/envs/py308/bin/chromedriver", chrome_options=options) # 启动带有自定义设置的Chrome浏览器
            self.driver = webdriver.Chrome(service=s, options=options)  # 启动带有自定义设置的Chrome浏览器
            print(self.driver.capabilities['browserVersion'])
            print(self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0])
            self.driver.get(varURL)
            # sleep(5)
            return self.driver
    def openURL(self, varURL):
        self._openURL(varURL)


    def opn(self, varUrl):

        '''
        1.1 打开网页
        :param varURL:
        :return:
        '''
        self.driver.get(varUrl)

    def opnLabel(self, varURL):

        '''
        1.2 打开标签页
        :param varURL:
        :return:
        '''

        self.driver.execute_script('window.open("' + varURL + '");')

    def swhLabel(self, varSwitch, t=1):

        '''
        1.3 切换标签页
        :param varSwitch: 1
        :param t:
        :return:
         # self.Web_PO.switchLabel(0) # 0 = 激活第一个标签页 ， 1 = 激活第二个标签页 , 以此类推。
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

    Web_PO = WebPO("chrome")
    # Web_PO = WebPO("chromeHeadless")
    # Web_PO = WebPO("firefox")

    # # print("1.1 打开网站".center(100, "-"))
    # Web_PO.openURL("https://baijiahao.baidu.com/s?id=1753450036624046728&wfr=spider&for=pc")
    Web_PO.openURL("http://www.baidu.com")
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
