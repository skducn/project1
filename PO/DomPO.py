# coding: utf-8
# ***************************************************************
# Author     : John
# Created on : 2020-3-20
# Description: 通过DOM来操作页面中各种元素，例如添加元素、删除元素、替换元素等
# 重新定义 find_element, find_elements, send_keys,
# clk, get, set, checkbox, select, iframe, js, boolean
# pip install selenium-wire

# https://blog.csdn.net/m0_57162664/article/details/134266949  Css
# 使用 nth-of-type(n)，可以指定选择的元素是父元素的第几个某类型的子节点。, 如 span:nth-of-type(2) 定位父元素第二个span类型子节点
# nth-last-of-type(n)，可以倒过来， 选择父元素的倒数第几个某类型的子节点。
# ***************************************************************
'''
重新定义
find_element
find_elements
send_keys
sendKeysByX
sendKeysById
sendKeysByname


todo clk
单点击 clkByX(varXpath)
多点击 clkByXs(varXpaths)
单点击某个索引号 clkIndexByXs(varXpaths, varIndex)
单点击超链接文本（文本中包含部分内容）clkTextByTpcByXs(varXpaths, varTpc, t=1):
单点击超链接文本 clkTextByXs(varXpaths, varText)
单点击超链接文本（属性中包含部分内容）clkTextByApcByXs(varXpaths, varAttr, varApc)
单点击超链接文本（属性中对应的值）clkTextByAcByXs(varXpaths, varAttr, varValue)
二次确认 clkByXsByX（varXpaths, varXpath）
clkById
clkByName
clkByTagname
clkByLinktext(varText)
clkByLinkstext(varText)

todo get
获取标签数量 getQtyByXs(varXpaths)
获取文本 getTextByX(varXpath)
获取文本列表 getListTextByX(varXpaths)
获取文本的索引号 getIndexByXs(varXpaths, varText)
获取文本包含部分内容(TPC)的索引号 getIndexByTpcByXs(varXpaths, varText)
获取指定文本之前的文本列表 getBeforeTextByXs(varXpaths, varText)
获取属性值 getAttrValueByX(varXpath, varAttr)
获取所有相同属性值的列表 getAttrValueByXs(varXpaths, varAttr)
获取超链接文本的属性值 getAttrValueByLt(varText, varAttr)
获取属性值的索引号 getIndexByAttrByXs(varXpaths, varAttr, varValue)
获取部分包含属性值所在的位置 getIndexByApcByXs(varXpaths, varAttr, varValue)
获取超链接文本及href getDictTextAttrValueByXs(varXpaths, varAttr)

通过标签下文本获取上一层元素 getUpEleByX(varLabel, varText)
通过标签下文本获取上层或上上层元素 getSuperEleByX(varLabel, varText, varXpath)

todo set
通过id设置文本 setTextById()
通过id追加文本 appendTextById()
通过name设置文本 setTextByName()
通过name追加文本 appendTextByName()
通过xpath设置文本 setTextByX()
通过xpath追加文本 appendTextByX()
通过xpath键盘设置文本 setTextEnterByX()
通过xpath键盘追加文本  appendTextEnterByX()

todo checkbox
是否选中复选框 isSelectedByX(varXpath)
取消所有已勾选的复选框clsSelected(varXpaths)

todo select
通过id选择文本 sltTextById(varId, varText)
通过id选择值 sltValueById(varId, varValue)
通过name选择文本 sltTextByName(varName, varText)
通过name选择值 sltValueByName(varName, varValue)

todo iframe
通过Xpath切换到iframe swhIframeByX(varXpath)
通过id切换到iframe   swhIframeById(varId)
通过xpaths遍历遍历属性中包含指定值切换iframe  swhIframeFromApcByXs(varXpaths,varAttr,varValue,2)
多个iframe之间切换  swhIframe(0)
退出iframe  quitIframe(0)

todo js
清除input输入框内容 clsText()
清除readonly属性，是元素可见  clsReadonlyByX(varXpath)
通过id去掉控件只读属性 clsReadonlyById(varId)
通过name去掉只读属性 clsReadonlyByName(varName)
通过name去掉隐藏属性 clsDisplayByName(varName)
通过tagname去掉隐藏属性 clsDisplayByTagName(varLabel, varLen)

todo boolean
通过xpath判断ture或false isEleExistByX(varXpath)
通过xpath判断属性是否存在 isBooleanAttr(varXpath, varAttr)
通过xpath判断属性值是否存在 isBooleanAttrValue(varXpath, varAttr, varValue)
通过Id判断ture或false isEleExistById(varId)
通过name判断ture或false isEleExistByName(varName)
通过超链接判断是否包含varText  isElePartExistByP(varPartText)
通过超链接判断是否存在varText isEleExistByL(varText)
通过xpath判断varText是否存在  isEleTextExistByX(varXpath, varText)

todo alert(system)
点击弹框中的确认 alertAccept()
点击弹框中的取消 alertDismiss()
获取弹框中的文案 alertText()
'''

import sys, os, platform, platform, psutil, ddddocr, requests, bs4, subprocess
# import pyscreeze, pyautogui, cv2
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.abstract_event_listener import *
from selenium.webdriver.support.event_firing_webdriver import *
from selenium.webdriver.support.expected_conditions import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image, ImageDraw, ImageGrab
from pytesseract import *
# from seleniumwire import webdriver

# from lxml import etree
import lxml.html
from lxml import etree
# from lxml.html.clean import Cleaner

from lxml_html_clean import clean_html
#  pip3 install lxml_html_clean

class DomPO(object):

    def __init__(self, driver):
        self.driver = driver


    def gettest(self, varUrl):


        # cleaned_html = clean_html(raw_html)
        # cleaner = Cleaner()
        # cleaner.javascript = True
        # cleaner.page_structure = False
        # cleaner.style = True

        # base_url = 'http://xxxxxxxxxx'
        # 需要提前下载一个网页，并保存为本地文件test.html

        print(varUrl)

        # with open('/Users/linghuchong/Downloads/51/Python/project/instance/zyjk/ERP/web/test.html', 'r', encoding='utf-8') as f:
        #     html_str = f.read()

# /html/body/div[1]/div/div[1]/div/div[2]/div/div[5]/div/div/div[2]/div/div/div[1]/ul/li[11]/div
#         self.clkByX("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span[2]/span/span[1]")

        # /html/body/div[1]/div/div[1]/div/div[2]/div/div[3]/div[3]/div[2]/div[2]/div[1]

        r = requests.get(varUrl)
        text = r.content.decode('utf8')
        # tree = lxml.html.fromstring(text)
        print(text)
        sleep(6)
        tree = etree.HTML(text)
        sleep(6)
        print(tree)

        # etree_root = clean_html(tree)
        # dom_tree = etree.ElementTree(etree_root)
        # dom_tree = etree.ElementTree(tree)
        # for e in dom_tree.iter():
        #     xpath = dom_tree.getpath(e)
        #     print(xpath)

        # # 解析HTML
        # # tree = etree.HTML(html_content)
        #
        # # 定位元素
        element = tree.xpath('//div[@class="top-main-list"]')[0]
        #
        # # 获取元素的XPath
        xpath = element.getroottree().getpath(element)
        print(xpath)  # 输出: /html/body/div/ul/li[1]



    def find_element(self, *loc):
        """重写元素定位"""
        try:
            # Python特性，将入参放在元组里，入参loc，加*，变成元组。
            # WebDriverWait(self.driver,5).until(lambda driver: driver.find_element(*loc).is_displayed())
            # 注意：以下loc入参本身就是元组，所以不需要再加*
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            print("未找到元素 %s " % (loc))

    def waitLoading(self, varXpath):
        # 创建WebDriverWait对象
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, varXpath)))

    def find_elements(self, *loc):
        """重写元素集定位"""
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_elements(*loc)
        except:
            print("未找到元素集 %s " % (loc))

    def send_keys(self, loc, vaule, clear_first=True, click_first=True):
        """重写键盘方法"""
        try:
            loc = getattr(self, "_%s" % loc)  # getattr相当于实现self.loc
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            print("未找到元素 %s " % (loc))



   # todo assert


    def assertTrue(self, testValue, errMsg):
        # ???
        try:
            if testValue == True:
                return True
            else:
                print(errMsg)
                return False
        except:
            return None

    def assertEqualTrue(self, varExpected, varActual):
        try:
            if varExpected == varActual:
                return True
            else:
                return False
        except:
            return None

    def assertEqual(self, varExpected, varActual, okMsg, errMsg):
        try:
            if varExpected == varActual:
                print(okMsg)
                return True
            else:
                print(errMsg)
                return False
        except:
            return None


    def assertContain(self, one, all, okMsg, errMsg):
        try:
            if one in all:
                print(okMsg)
                return True
            else:
                print(errMsg)
                return False
        except:
            return None

    def assertEqualNotNone(self, expected, actual):
        try:
            if (expected and actual) and (expected != None and actual != None):
                return 1, expected
            else:
                return 0, 0
        except:
            return None

    # def getError(self, varStatus, varErrorInfo, varErrorRow):
    #     # 当函数返回error时，获取当前语句行号及错误提示。
    #     # 因此函数必须要有返回值
    #     # Level_PO.getError(Level_PO.inputId(u"officebundle_tmoffice_officeName", u"自动化科室123"), u"输入框定位错误！",sys._getframe().f_lineno)
    #     # errorrrrrrrrrrr, 101行, '获取科室文本与对应值的字典'。
    #     if varStatus == "error":
    #         print("errorrrrrrrrrrr,", varErrorRow, "行,", varErrorInfo)
    #         sys.exit(0)



    # todo clk



    def getUrlByclkByX(self, varXpath, t=1):
        # 单点击，并返回url
        self.find_element(*(By.XPATH, varXpath)).click()
        sleep(t)
        return (self.driver.current_url)

    def clkByX(self, varXpath, t=1):
        # 单点击
        self.find_element(*(By.XPATH, varXpath)).click()
        sleep(t)


    def clkByXs(self, varXpaths, t=1):
        # 多点击
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)

    def clkIndexByXs(self, varXpaths, varIndex, t=1):
        # 单点击某个索引号
        # 如：遍历按钮点击第5个。clkIndexByXs(u"//button[@ng-click='action.callback()']",5)
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if index == varIndex:
                a.click()
                break
        sleep(t)

    def clkTextByTpcByXs(self, varXpaths, varTpc, t=1):
        # 单点击超链接文本（文本中包含部分内容））（varTPC = TextPartialContent)
        # 如：遍历按钮点击所有文本中包含20190506059的内容。clkTextByTpcByXs(u"//td[@aria-describedby='gridTable_run_name']/a",u"20190506059")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varTpc in a.text:
                a.click()
                break
        sleep(t)

    def clkTextByXs(self, varXpaths, varText, t=1):
        # 单点击超链接文本
        # 如：遍历按钮点击所有文本中包含20190506059的内容。clkTextsContain(u"//td[@aria-describedby='gridTable_run_name']/a",u"20190506059")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varText == a.text:
                a.click()
                break
        sleep(t)

    def clkTextByApcByXs(self, varXpaths, varAttr, varApc, t=1):
        # 单点击超链接文本（属性中包含部分内容）varAPC = (AttrPartialContent)
        # 如：遍历点击a链接属性href中包含www内容， clkTextByApcByXs("//a","href","www")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varApc in a.get_attribute(varAttr):
                a.click()
                break
        sleep(t)

    def clkTextByAcByXs(self, varXpaths, varAttr, varValue, t=1):
        # 单点击超链接文本（属性中对应的值）
        # 如：遍历点击a链接属性href = www.baidu.com， clkTextByAcByXs("//a","href","www.baidu.com")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varValue == a.get_attribute(varAttr):
                a.click()
                break
        sleep(t)

    def clkByXsByX(self, varXpaths, varXpath, t=1):
        # 二次确认
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)
            self.find_element(*(By.XPATH, varXpath)).click()
        sleep(t)

    def clkById(self, varId, t=1):
        self.find_element(*(By.ID, varId)).click()
        sleep(t)

    def clkByName(self, varName, t=1):
        self.find_element(*(By.NAME, varName)).click()
        sleep(t)

    def clkByTagname(self, varText, t=1):
        self.find_element(*(By.TAG_NAME, varText)).click()
        sleep(t)

    def clkByLinktext(self, varText, t=1):
        self.find_element(*(By.LINK_TEXT, varText)).click()
        sleep(t)

    def clkByLinkstext(self, varText, t=1):
        """通过linkstext点击"""
        for a in self.find_elements(*(By.LINK_TEXT, varText)):
            a.click()
        sleep(t)



    # todo get

    def getQtyByXs(self, varXpaths):
        # 获取标签数量
        # 如：获取tr下有多少个div标签 getQtyByXs('//*[@id="app"]/tr/div')
        qty = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            qty = qty + 1
        return qty

    def eleGetQtyByX(self, ele, varXpaths):
        # 获取标签数量
        # 如：获取tr下有多少个div标签 getQtyByXs('//*[@id="app"]/tr/div')
        qty = 0
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            qty = qty + 1
        return qty

    def getTextByX(self, varXpath):
        # 获取文本
        # 如：getTextByX(u"//input[@class='123']")
        return self.find_element(*(By.XPATH, varXpath)).text

    def getTextByXs(self, varXpaths):
        # 获取文本列表
        # 如：getTextByXs(u"//input[@class='123']")
        l_ = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_.append(a.text)
        return l_

    def eleGetQtyByXs(self, ele, varXpaths):
        # 获取标签数量
        # 如：eleGetQtyByXs(ele, "//ul/li")
        varQty = 0
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            varQty = varQty + 1
        return varQty

    def getIndexByXs(self, varXpaths, varText):
        # 获取文本的索引号
        # 获取test文本在tr里的位置，返回3，表示在第三个tr里，未找到返回none， 如：getIndexByXs("//tr",'test')
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if a.text == varText:
                return index
        return None

    def getIndexByTpcByXs(self, varXpaths, varTPC):
        # 获取文本包含部分内容(TPC)的索引号
        # 如：getIndexByTpcByXs("//tr","test")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varTPC in a.text:
                return index

    def getBeforeTextByXs(self, varXpaths, varText):
        # 获取指定文本之前的文本列表
        # 如文本集 a,b,c,d, getBeforeTextByXs("//tr",'c'), 返回列表【a,b】
        l_beforeText = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varText == a.text:
                break
            else:
                l_beforeText.append(a.text)
        return l_beforeText

    def getAttrValueByX(self, varXpath, varAttr):
        # 获取属性值
        # 如：getAttrValueByX(u"//input[@class='123']","href")
        return self.find_element(*(By.XPATH, varXpath)).get_attribute(varAttr)

    def getAttrValueByXs(self, varXpaths, varAttr):
        # 获取所有相同属性值的列表
        # 如：获取所有tr标签中 href的值 getAttrValueByXs("//tr", "href")
        l_attrValue = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_attrValue.append(a.get_attribute(varAttr))
        return l_attrValue

    def getAttrValueByLt(self, varText, varAttr):
        # 获取超链接文本的属性值
        # 如：getAttrValueByLt("超链接文本", "href")
        return self.find_element(*(By.LINK_TEXT, varText)).get_attribute(varAttr)

    def getIndexByAttrByXs(self, varXpaths, varAttr, varValue):
        # 获取属性值的索引号
        # 如：getIndexByAttrByXs("//a","href","http://www.baidu.com")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varValue == a.get_attribute(varAttr):
                return index

    def getIndexByApcByXs(self, varXpaths, varAttr, varValue):
        # 获取部分包含属性值的索引号 APC = attribute part content
        # 如：getIndexByApcByXs("//td[9]/a","href","http://")
        index = 0
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            index = index + 1
            if varValue in a.get_attribute(varAttr):
                return index

    def getDictTextAttrValueByXs(self, varXpaths, varAttr):
        # 获取超链接文本及href，并组合成字典{文本：属性值}
        # 如获取所有a标签下的文本，getDictTextAttrValueByXs("//a","href")
        # {'首页': 'http://192.168.0.202:28098/index', '医院管理': 'http://192.168.0.202:28098/mainData/mainData/hospital'}
        l_text = []
        l_attrValue = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_text.append(a.text)
            l_attrValue.append(a.get_attribute(varAttr))
        return dict(zip(l_text, l_attrValue))

    def getUpEleByX(self, varXpath):
        # 通过标签下文本获取上一层元素
        # getUpEleByX("//div[@class='van-col']")  # 获取div下文本上一层的元素
        # getUpEleByX("//div[text()='文本']")  # 获取div下文本上一层的元素
        # getUpEleByX("//span[text()='文本']")  # 获取span下文本上一层的元素
        ele = self.find_element(*(By.XPATH, varXpath))
        return self.driver.execute_script("return arguments[0].parentNode;", ele)


    def getSuperEleByX(self, varXpath, varXpath2):
        # 通过标签下文本获取上层或上上层元素
        # 如：ele = self.getSuperEleByX("//span[text()='过会']", '../..') # 获取span标签下文本上上层的元素
        # 如：ele = self.getSuperEleByX("//div[text()='过会']", '../../..') # 获取div标签下文本上上上层的元素
        # ele = self.find_element(*(By.XPATH, "//" + varLabel + "[text()='" + str(varText) + "']"))
        ele = self.find_element(*(By.XPATH, varXpath))
        return ele.find_element(*(By.XPATH, varXpath2))



    # todo set

    def setTextById(self, varId, varText):
        """通过id设置文本"""
        self.find_element(*(By.ID, varId)).clear()
        self.find_element(*(By.ID, varId)).send_keys(varText)

    def appendTextById(self, varId, varText):
        """通过id追加文本"""
        self.find_element(*(By.ID, varId)).send_keys(varText)

    def setTextByName(self, varName, varText):
        """通过name设置文本"""
        self.find_element(*(By.ID, varName)).clear()
        self.find_element(*(By.NAME, varName)).send_keys(varText)

    def appendTextByName(self, varName, varText):
        """通过name追加文本"""
        self.find_element(*(By.NAME, varName)).send_keys(varText)

    def setTextByX(self, varXpath, varText, t=1):
        # 输入框清空后输入文本
        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        sleep(t)

    def setTextEnterByX(self, varXpath, varText, t=1):
        # 输入框清空后输入文本，按回车
        self.find_element(*(By.XPATH, varXpath)).clear()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)

    def setTextTabByX(self, varXpath, varText, t=1):
        # 输入框双击后输入文本，按Tab
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.double_click(ele).perform()
        sleep(t)
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.TAB)
        sleep(t)

    def setTextTabByX2(self, varXpath, varText, t=1):
        # 输入框双击后输入文本，按Tab
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        actions.double_click(ele).perform()
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.TAB)
        sleep(t)

    def appentTextByX(self, varXpath, varText, t=1):
        # 输入框追加文本
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        sleep(t)

    def appendTextEnterByX(self, varXpath, varText, t=1):
        # 输入框追加文本，按回车
        self.find_element(*(By.XPATH, varXpath)).send_keys(varText)
        self.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)




    # todo shadow-root元素

    def getShadowByXByC(self, varXpath, varCss, t=1):
        # shadow-root元素通过CSS_SELECTOR方法获得，不支持Xpath
        ele = self.find_element(*(By.XPATH, varXpath))
        shadow_root = ele.shadow_root
        ele2 = shadow_root.find_element(By.CSS_SELECTOR, varCss)
        sleep(t)
        return (ele2.text)

    def getShadowByXsByC(self, varXpaths, varCss, t=1):
        # shadow-root元素通过CSS_SELECTOR方法获得，不支持Xpath
        # 如：input下shadow-root元素div的文本，返回列表
        # getShadowByXsByC("//input", "div")
        eles = self.find_elements(*(By.XPATH, varXpaths))
        l_shadow = []
        for i in eles:
            shadow_root = i.shadow_root
            ele2 = shadow_root.find_element(By.CSS_SELECTOR, varCss)
            l_shadow.append(ele2.text)
        sleep(t)
        return l_shadow


    # todo ele元素再定位

    def eleClkByX(self, ele, varXpath, t=2):
        # 元素再定位后点击
        e = ele.find_element(*(By.XPATH, varXpath))
        e.click()
        sleep(t)

    def eleClkByXs(self, ele, varXpaths, t=1):
        # 元素再定位后点击
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            a.click()
            sleep(t)
        
    def eleGetShadowByXsByC(self, ele, varXpaths, varCss, t=1):
        # shadow-root元素通过CSS_SELECTOR方法获得，不支持Xpath
        # 遍历所有shadow-root元素input下div的文本，返回列表
        # eleGetShadowByXsByC(ele, "//table[1]", "div")
        eles = ele.find_elements(*(By.XPATH, varXpaths))
        l_shadow = []
        for i in eles:
            shadow_root = i.shadow_root
            ele2 = shadow_root.find_element(By.CSS_SELECTOR, varCss)
            l_shadow.append(ele2.text)
        sleep(t)
        return l_shadow

    def eleGetValueByAttr(self, ele, varAttr):
        # 元素再定位后获取属性
        return ele.get_attribute(varAttr)

    def eleGetQtyByXs(self, ele, varXpaths):
        # 元素再定位后获取标签数量
        # 如：获取tr下有多少个div标签 getQtyByXs('//*[@id="app"]/tr/div')
        qty = 0
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            qty = qty + 1
        return qty

    def eleGetTextByX(self, ele, varXpath):
        # 元素再定位后获取文本
        return ele.find_element(*(By.XPATH, varXpath)).text

    def eleGetTextByXs(self, ele, varXpaths):
        # 元素再定位后获取文本
        l_ = []
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            l_.append(a.text)
        return l_

    def eleGetTextByXsByX(self, ele, varXpaths, varXpath):
        # eleGetTextByXsByX(ele, "//div[3]/div", ".//div")  # div下的text
        # eleGetTextByXsByX(ele, "//div[3]/div", ".//span") # span下的text
        # 元素再定位后获取div文本
        l_ = []
        for a in ele.find_elements(*(By.XPATH, varXpaths)):
            l_.append(a.find_element(*(By.XPATH, varXpath)).text)
        return l_

    def eleSetTextByX(self, ele, varXpath, varValue):
        # 元素再定位后输入和提交
        ele.find_element(*(By.XPATH, varXpath)).clear()
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)

    def eleSetTextEnterByX(self, ele, varXpath, varValue, t=1):
        # 元素再定位后输入和提交

        ele.find_element(*(By.XPATH, varXpath)).clear()
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)
        ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)

    def eleSetTextBackspaceEnterByX(self, ele, varXpath, varN, varValue, t=3):
        # 元素再定位后输入和提交
        for i in range(varN):
            ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.BACKSPACE)
        # ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.CONTROL, 'a')
        # ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.CONTROL, 'x')
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)
        ele.find_element(*(By.XPATH, varXpath)).send_keys(Keys.ENTER)
        sleep(t)


    def eleSetTextClkByXByX(self, ele, varXpath, varValue, varXpath2, t=1):
        # 元素再定位后输入和提交
        ele.find_element(*(By.XPATH, varXpath)).clear()
        ele.find_element(*(By.XPATH, varXpath)).send_keys(varValue)
        sleep(t)
        ele.find_element(*(By.XPATH, varXpath2)).click()

    def eleDoubleClkByX(self, ele, varXpath, t=2):
        # 定位元素后，上下滚动
        # step 负数向上滚动，正数向下滚动
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.double_click(ele2).perform()
        sleep(t)

    def eleCtrlAByX(self, ele, varXpath, t=2):
        # 定位元素后，上下滚动
        # step 负数向上滚动，正数向下滚动
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        ele2.click()
        actions = ActionChains(self.driver)
        actions.key_down(ele2, "Control").send_keys('a').key_up('Control').perform()
        sleep(t)

    def eleScrollUpDownByX(self, ele, varXpath, varStep, t=2):
        # 定位元素后，上下滚动
        # step 负数向上滚动，正数向下滚动
        sleep(t)
        # print(varStep)
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele2)
        actions.click_and_hold()
        # actions.move_by_offset(0, varStep)
        if varStep != 0:
            if varStep >= 150:
                actions.move_by_offset(0, 150)
            elif varStep <= -500:
                actions.move_by_offset(0, -500)
            else:
                actions.move_by_offset(0, varStep)

        actions.release()
        actions.perform()
        sleep(t)

    def eleScrollLeftRightByX(self, ele, varXpath, varStep, t=2):
        # 定位元素后, 左右滚动
        sleep(t)
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele2)
        actions.click_and_hold()
        actions.move_by_offset(varStep, 0)
        actions.release()
        actions.perform()
        sleep(t)

    def eleScrollViewByX(self, ele, varXpath, t=1):
        # 将元素滚动到可见区域。
        # 先定位元素，然后使用JavaScript脚本将元素滚动到可见区域。
        # element = self.driver.find_element_by_id(varId)  id方式定位
        # element = self.find_element(*(By.XPATH, "//a[@href='#/meeting']"))  Xpath方式定位
        # ErpApp_PO.Web_PO.scrollViewByX("//a[last()]")  # 拖动到最后一个a标签
        element = ele.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)  # 将元素滚动到可见区域
        sleep(t)

    def eleScrollKeysEndByXByX(self, ele, varXpath, varCount, varXpath2, t=2):
        # 键盘keys.End滚动到底部
        # 逻辑：定位varPath元素，遍历keys.end N次, 判断varPath2元素退出
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        for i in range(varCount):
            ActionChains(self.driver).send_keys_to_element(ele2, Keys.END).perform()
            sleep(1)
            if self.isEleExistByX(varXpath2):
                break
        sleep(t)

    def eleScrollKeysEndByX(self, ele, varXpath, t=2):
        # 键盘keys.End滚动到底部
        ele2 = ele.find_element(*(By.XPATH, varXpath))
        ActionChains(self.driver).send_keys_to_element(ele2, Keys.END).perform()
        sleep(t)



    # todo checkbox

    def isSelectedByX(self, varXpath):
       # 复选框是否选中？ True 或 False"""
        # isSelectedByX(u"//input[@class='123']")
        return self.find_element(*(By.XPATH, varXpath)).is_selected()

    def clrSelectedByXs(self, varXpaths):
        # 取消所有已勾选的复选框
        # clrSelectedByXs(u"//input[@type='checkbox']")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if a.is_selected() == True:
                a.click()



    # todo select

    def sltTextById(self, varId, varText):
        """通过id选择文本"""
        # 如：value=1 , Text=启用 ，sltTextById("id", u'启用')
        Select(self.find_element(*(By.ID, varId))).select_by_visible_text(varText)

    def sltValueById(self, varId, varValue):
        """通过id选择值"""
        # 如：value=10 , Text=启用 ，sltTextById("id", '10')
        Select(self.find_element(*(By.ID, varId))).select_by_value(varValue)

    def sltTextByName(self, varName, varText):
        """通过name选择文本"""
        # 如：value=10 , Text=启用 ，sltTextByName("isAvilable", '启动')
        Select(self.find_element(*(By.NAME, varName))).select_by_visible_text(varText)

    def sltValueByName(self, varName, varValue):
        """通过name选择值"""
        # 如：value=10 , Text=启用 ，sltValueByName("isAvilable", '10')
        Select(self.find_element(*(By.NAME, varName))).select_by_value(varValue)

    def sltValueByX(self, varXpath, varValue):
        """通过xpath选择值"""
        # 如：value=10 , Text=启用 ，sltValueByName("isAvilable", '10')
        Select(self.find_element(*(By.XPATH, varXpath))).select_by_visible_text(varValue)

    def selectXpathText(self, varXpath, varText):
        # 遍历Xpath下的Option,(待确认)
        # self.selectXpathText(u"//select[@regionlevel='1']", u'启用'), （一般情况 value=1 , Text=启用）
        s1 = self.driver.find_element_by_xpath(varXpath)
        l_content1 = []
        l_value1 = []
        # varContents = self.driver.find_elements_by_xpath(varByXpath + "/option")
        varContents = self.driver.find_elements_by_xpath(varXpath + "/option")
        for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute("value"))
        d_total1 = dict(zip(l_content1, l_value1))
        for i in range(len(d_total1)):
            if sorted(d_total1.items())[i][0] == varText:
                Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                break
    def selectIdStyle(self, varByID, varText):
        # ？ 遍历某ID的下的option (不包含 隐藏的属性，如style=display:none），获取varText对应的值(待确认)
        # self.selectIdStyle(u"id", u'启用')  # （一般情况 value=1 , Text=启用）
        l_content1 = []
        l_value1 = []
        varCount = 0
        s1 = self.driver.find_element_by_id(varByID)
        varContents = s1.find_elements_by_tag_name("option")
        for a in varContents:
            if a.get_attribute("style") == "" and a.text == varText:
                l_content1.append(a.text)
                l_value1.append(a.get_attribute("value"))
                varCount = 1
        if varCount == 1:
            d_total1 = dict(zip(l_content1, l_value1))
            for i in range(len(d_total1)):
                if sorted(d_total1.items())[i][0] == varText:
                    Select(s1).select_by_value(sorted(d_total1.items())[i][1])
                    break
        else:
            return None
    def selectXpathsMenu1Menu2(self, varXpaths1, varMenu, varXpaths2, varMenu2, t):
        # 遍历级联菜单（选择一级菜单后再选择二级菜单）(待确认)
        # Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理", 3)
        try:
            for a in self.driver.find_elements_by_xpath(varXpaths1):
                if varMenu == a.text:
                    a.click()
                    sleep(t)
                    for a2 in self.driver.find_elements_by_xpath(varXpaths2):
                        if varMenu2 == a2.text:
                            a2.click()
                            sleep(t)
                            break
                    break
        except:
            return None
    def get_selectNAMEvalue(self, varByname, varContent):
        # 获取某select下text的value值。（下拉框，定位ByName，选择内容，text != value ）(待确认)
        s1 = self.driver.find_element_by_name(varByname)
        l_content1 = []
        l_value1 = []
        varContents = self.driver.find_elements_by_xpath(
            "//select[@name='" + varByname + "']/option"
        )
        for a in varContents:
            l_content1.append(a.text)
            l_value1.append(a.get_attribute("value"))
        d_total1 = dict(zip(l_content1, l_value1))
        for i in range(len(d_total1)):
            if sorted(d_total1.items())[i][0] == varContent:
                value = sorted(d_total1.items())[i][1]
                return value
    def get_selectOptionValue(self, varByname, varNum):
        # 获取某个select中text的value值。(待确认)
        varValue = self.driver.find_element_by_xpath(
            "//select[@name='" + varByname + "']/option[" + varNum + "]"
        ).get_attribute("value")
        return varValue



    # todo iframe

    def swhIframeByX(self, varXpath, t=1):
        """通过Xpath切换到iframe"""
        # 如：swhIframeByX("//body[@class='gray-bg top-navigation']/div[4]/iframe")
        self.driver.switch_to_frame(self.find_element(*(By.XPATH, varXpath)))
        sleep(t)

    def swhIframeById(self, varId, t=1):
        """通过id切换到iframe"""
        #如：swhIframeById（"layui-layer-iframe1"）
        self.driver.switch_to_frame(self.find_element(*(By.ID, varId)))
        sleep(t)

    def swhIframeFromApcByXs(self, varXpaths, varAttr, varValue, t=1):
        """通过xpaths遍历遍历属性中包含指定值切换iframe"""
        # 如：swhIframeFromApcByXs（"//iframe", "src", "/general/workflow/new/"）
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            if varValue in a.get_attribute(varAttr):
                self.driver.switch_to_frame(self.find_element(*(By.XPATH, varXpaths)))
                # self.driver.switch_to_frame(self.driver.find_element_by_xpath(varXpaths))
                break
        sleep(t)

    def swhIframe(self, t=1):
        """多个iframe之间切换"""
        # 如：如第一层iframe1，第二层iframe2，两者之间切换
        self.driver.switch_to.parent_frame()
        sleep(t)

    def quitIframe(self, t=1):
        """退出iframe"""
        self.driver.switch_to_default_content()
        sleep(t)

    def inIframeTopDiv(self, varXpath, t=1):
        # 定位iframe的div路径?(未确认)
        # evel_PO.inIframeDiv("[@id='showRealtime']", 2)
        # Home_PO.inIframeDiv("[@class='cetc-popup-content']/div", 2)
        iframe = self.driver.find_element_by_xpath("//div" + varXpath + "/iframe")
        # print iframe.get_attribute("src")
        self.driver.switch_to_frame(iframe)
        sleep(t)


    # todo ActionChains
    # https://fishpi.cn/article/1713864467902




    def scrollKeysEndByXs2(self, varValue, varXpaths, varXpath2):
        # 每滚动一次（到底部）返回字典的值
        # self.Web_PO.scrollKeysEndByXs2("45%", "//div[@class='van-picker-column']/ul/li", "//div[@class='van-picker-column']")
        l_2 = []
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            l_ = self.getTextByXs(varXpath2)
            ActionChains(self.driver).send_keys_to_element(a, Keys.END).perform()
            # print(l_)
            l_1 = l_[0].split("\n")
            for i in l_1:
                l_2.append(i)
            # print(l_2)
            # 去重
            l_3 = sorted(set(l_2), key=l_2.index)
            # print(l_3)
            # 成字典
            d_ = {v: k for k, v in dict(enumerate(l_3, start=1)).items()}
            print(d_)
            if varValue in l_[0]:
                return d_[varValue]


    def scrollKeysEndByXs(self, varXpaths, t=2):
        # 遍历滚动到底部
        # self.Web_PO.scrollKeysEndByXs("//div[@class='van-picker-column']/ul/li")
        for a in self.find_elements(*(By.XPATH, varXpaths)):
            ActionChains(self.driver).send_keys_to_element(a, Keys.END).perform()
        sleep(t)

    def scrollKeysEndByX(self, varXpath, t=2):
        # 一次性滚动到底部
        # 逻辑：定位varPath元素，遍历keys.end N次, 判断varPath2元素退出
        ele = self.find_element(*(By.XPATH, varXpath))
        ActionChains(self.driver).send_keys_to_element(ele, Keys.END).perform()
        sleep(t)

    def scrollKeysEndByXByX(self, varXpath, varCount, varXpath2, t=2):
        # 键盘keys.End滚动到底部
        # 逻辑：定位varPath元素，遍历keys.end N次, 判断varPath2元素退出
        ele = self.find_element(*(By.XPATH, varXpath))
        for i in range(varCount):
            ActionChains(self.driver).send_keys_to_element(ele, Keys.END).perform()
            sleep(1)
            if self.isEleExistByX(varXpath2):
                break
        sleep(t)
        # ActionChains(self.driver).send_keys_to_element(ele, Keys.PAGE_DOWN).perform()
        # ActionChains(self.driver).send_keys_to_element(ele, Keys.ARROW_DOWN).perform()



    def scrollUpDownByX(self, varXpath, varStep, t=2):
        # 上下滚动
        # step 负数向上滚动，正数向下滚动
        # ActionChains(self.driver).move_to_element(elements).click_and_hold().move_by_offset(0, varStep).release().perform()
        sleep(t)
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele)
        actions.click_and_hold()
        if varStep != 0:
            if varStep >= 150:
                actions.move_by_offset(0, 150)
            elif varStep <= -500:
                actions.move_by_offset(0, -500)
            else:
                actions.move_by_offset(0, varStep)
        actions.release()
        actions.perform()
        sleep(t)

    def scrollLeftRightByX(self, varXpath, varStep, t=2):
        # 左右滚动
        sleep(t)
        ele = self.find_element(*(By.XPATH, varXpath))
        actions = ActionChains(self.driver)
        actions.move_to_element(ele)
        actions.click_and_hold()
        actions.move_by_offset(varStep, 0)
        actions.release()
        actions.perform()
        sleep(t)

    # todo js
    
    
    def scrollBy(self, varStep, t=2):
        # 按步长滚动，模拟用户拖动滚动条的行为。
        # step 负数向上滚动，正数向下滚动
        # scrollByStep(-500)
        # self.driver.execute_script("window.scrollBy(0, -500);")
        self.driver.execute_script('window.scrollBy(0, ' + str(varStep) + ');')
        sleep(t)

    def scrollToLocation(self, varLoc):
        # 滚动到指定位置。
        self.driver.execute_script('window.scrollTo(0, %s)' % varLoc)

    def scrollByStep(self, varStep, t=1):
        # 按步长逐步向下滚动直到页面底部
        # scrollByAuto(50)
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        for i in range(0, new_height, varStep):
            sleep(t)
            self.driver.execute_script('window.scrollTo(0, %s)' % i)

    def scrollBottom(self, t=1):
        # 直接滚动到页面底部
        # self.driver.execute_script('window.scrollTo(0, 1000)')  # 滚动到页面底部
        # self.driver.execute_script("document.documentElement.scrollTop=1000")  # 滚动到页面底部
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(t)

    def scrollViewByX(self, varXpath, t=1):
        # 将元素滚动到可见区域。
        # 先定位元素，然后使用JavaScript脚本将元素滚动到可见区域。
        # element = self.driver.find_element_by_id(varId)  id方式定位
        # element = self.find_element(*(By.XPATH, "//a[@href='#/meeting']"))  Xpath方式定位
        # ErpApp_PO.Web_PO.scrollViewByX("//a[last()]")  # 拖动到最后一个a标签
        ele = self.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)  # 将元素滚动到可见区域
        sleep(t)



    def clsText(self, t=1):
        # 清除input输入框内容
        self.driver.execute_script('document.querySelector("input[type=number]").value=""')
        sleep(t)

    def clsReadonlyByX(self, varXpath, t=1):
        # 去掉只读属性
        ele = self.find_element(*(By.XPATH, varXpath))
        self.driver.execute_script('arguments[0].removeAttribute("readonly")', ele)
        sleep(t)

    def clsReadonlyById(self, varId, t=1):
        # 通过id去掉只读属性, 一般用于第三方日期控件
        self.driver.execute_script('document.getElementById("' + varId + '").removeAttribute("readonly")')
        sleep(t)

    def clsReadonlyByName(self, varName, t=1):
        # 通过name去掉只读属性
        # 注意：document只支持getElementsByName方法获取标签数组，如 array[0]
        self.driver.execute_script('document.getElementsByName("' + varName + '")[0].removeAttribute("readonly")')
        sleep(t)

    def clsDisplayByName(self, varName, t=1):
        # 通过name去掉隐藏属性
        self.driver.execute_script('document.getElementsByName("' + varName + '")[0].style.display=""')
        sleep(t)

    def clsDisplayByTagName(self, varLabel, varLen, t=1):
        # 通过tagname去掉隐藏属性
        # 如：清除30个ul标签的display，30是ul数量，可以通过其他方式获取。 jsDisplayByTagName(30, "ul")
        for i in range(varLen):
            self.driver.execute_script('document.getElementsByTagName("' + varLabel + '")[' + str(i) + '].style.display=""')
        sleep(t)

    def displayBlockID(self, varID):
        # 未验证？(未确认)
        varJs = 'document.getElementById("filePath").style.display="block"'
        # document.getElementByPath
        return self.driver.find_element_by_id(varID).style.display



    # todo True or False



    def eleIsEleExistByX(self, ele, varXpath):
        # 判断元素是否存在
        flag = False
        try:
            ele.find_element(*(By.XPATH, varXpath))
            flag = True
        except:
            flag = False
        return flag


    def isEleExistByX(self, varXpath):
        # 判断元素是否存在
        flag = False
        try:
            self.find_element(*(By.XPATH, varXpath))
            flag = True
        except:
            flag = False
        return flag

    def isEleExistByXForWait(self, varXpath, varCycle):
        # 循环等待时间，判断元素是否存在，存在则退出

        for i in range(varCycle):
            if self.isEleExistByX(varXpath):
                break
            else:
                sleep(1)







    def isEleAttrExistByX(self, varXpath, varAttr):
        # 判断元素属性是否存在
        flag = False
        try:
            ele = self.find_element(*(By.XPATH, varXpath))
            if ele.get_attribute(varAttr):
                flag = True
        except:
            flag = False
        return flag

    def isEleAttrValueExistByX(self, varXpath, varAttr, varValue):
        # 判断元素属性的值是否存在
        # 如：isEleAttrValueExistByX("//tr","href","www.badu.com")
        flag = False
        try:
            for ele in self.find_elements(*(By.XPATH, varXpath)):
                if varValue == ele.get_attribute(varAttr):
                    flag = True
                    break
        except:
            flag = False
        return flag

    def isEleExistById(self, varId):
        # 通过Id判断ture或false
        flag = False
        try:
            self.find_element(*(By.ID, varId))
            flag = True
        except:
            flag = False
        return flag

    def isEleExistByName(self, varName):
        # 通过name判断ture或false
        flag = False
        try:
            self.find_element(*(By.NAME, varName))
            flag = True
        except:
            flag = False
        return flag

    def isElePartExistByP(self, varPartText):
        # 通过超链接判断是否包含varText
        flag = False
        try:
            self.driver.find_element_by_partial_link_text(varPartText)
            flag = True
        except:
            flag = False
        return flag

    def isEleExistByL(self, varText):
        # 通过超链接判断是否存在varText
        flag = False
        try:
            self.driver.find_element_by_link_text(varText)
            flag = True
        except:
            flag = False
        return flag

    def isEleTextExistByX(self, varXpath, varText):
        # 通过xpath判断文本是否存在
        flag = False
        try:
            if self.find_element(*(By.XPATH, varXpath)).text == varText:
                flag = True
        except:
            flag = False
        return flag

    def isEleTextExistByXForWait(self, varXpath, varText, varCycle):
        # 循环等待时间，通过xpath判断文本是否存在，存在则退出
        for i in range(varCycle):
            if self.isEleTextExistByX(self, varXpath, varText):
                break
            else:
                sleep(1)

    def isBooleanAttrValueListByX(self, varXpath, varAttr, varValue):
        """通过xpath判断属性等于值"""
        # 如：isBooleanAttrValueListByX("//tr","href","www.badu.com")
        # .isBooleanAttrValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-disabled is-checked')
        # 判断单选框是否被选中。

        l1 = []
        for a in self.find_elements(*(By.XPATH, varXpath)):
            if varValue == a.get_attribute(varAttr):
                l1.append("True")
            else:
                l1.append("False")
        return l1

    def isBooleanAttrContainValueListByX(self, varXpath, varAttr, varValue):

        """通过xpath判断属性包含值"""
        # .isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-disabled is-checked')
        # 判断单选框是否被选中。

        l1 = []
        for a in self.find_elements(*(By.XPATH, varXpath)):
            if varValue in a.get_attribute(varAttr):
                l1.append("True")
            else:
                l1.append("False")
        return l1


    def isElementVisibleXpath(self, element):
        # 未验证？？？（未确认）
        driver = self.driver
        try:
            the_element = EC.visibility_of_element_located(
                driver.find_element_by_partial_link_text(element)
            )
            assert the_element(driver)
            flag = True
        except:
            flag = False
        return flag
    def locElement(self, varXpath, t=1):
        # 定位到某元素???（未确认）
        try:
            elements = self.find_element(*(By.XPATH, varXpath))
            actions = ActionChains(self.driver)
            actions.move_to_element(elements).perform()
            sleep(t)
        except:
            return None



    # todo alert(system)

    def alertAccept(self):

        # 点击弹框中的确认

        alert = self.driver.switch_to.alert
        alert.accept()

    def alertDismiss(self):

        # 点击弹框中的取消

        alert = self.driver.switch_to.alert
        alert.dismiss()

    def alertText(self):

        # 获取弹框中的文案

        alert = self.driver.switch_to.alert
        return alert.text


    def getCount(self, varLabel):
        c = self.find_elements(*(By.TAG_NAME, varLabel))
        return len(c)


    def zoom(self, percent):
        # 缩放页面
        # js = "document.body.style.zoom='70%'"
        js = "document.body.style.zoom='" + str(percent) + "%'"
        self.driver.execute_script(js)



    def canvas2base64(self, varXpath):
        # canvas元素转base64图片
        canvas = self.find_element(*(By.XPATH, varXpath))
        data_url = self.driver.execute_script("return arguments[0].toDataURL('image/png');", canvas)
        return data_url
