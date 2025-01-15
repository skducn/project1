# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-7-25
# Description:
# https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
varUrl = Configparser_PO.HTTP("url")
varUrlTest = Configparser_PO.HTTP("testUrl")

from PO.WebPO import *

from PO.LogPO2 import *
# Log_PO2 = LogPO2("./LogPO3.log")

from PO.CaptchaPO import *
Captcha_PO = CaptchaPO()

from PO.Base64PO import *
Base64_PO = Base64PO()

from PO.FilePO import *
File_PO = FilePO()

import logging
import signal
import sys

from time import sleep
import datetime


class ChcWebPO():


    def __init__(self, varFile):

        # 配置日志
        if os.name == 'nt':
            logging.basicConfig(filename=varFile, level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
        else:
            logging.basicConfig(filename=varFile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        # print(varFile, datetime.datetime.now())


    # 定义信号处理函数
    def handle_signal(self, signum, frame):
        self.logger.info('Received signal: {}'.format(signal.Signals(signum).name))
        self.logger.info('Program is terminating...')
        # 在这里可以添加额外的清理代码或日志记录
        sys.exit(0)
        # # 信号处理函数需要2个参数,这里放在了类里面,所以还需要额外的self参数
        # logger.info("Get TERM signal {0}".format(signal_num))
        # self.terminated_flag = True
        # self._kill_sleep_gevent()  # 轮询结束休眠的协程


    def runTest(self, varJsonFile):

        # 1，登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrlTest)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", Configparser_PO.USER("user"))
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", Configparser_PO.USER("password"))
        # 验证码
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", "1")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)

        # 2，遍历身份id
        varJsonFile = varJsonFile + ".json"
        d_2 = File_PO.jsonfile2dict(varJsonFile)
        for k1, v1 in d_2.items():
            for k, v in v1.items():
                l_1 = []
                l_2 = []
                for i in v:
                    s = varUrlTest + "#/SignManage/signAssess/component/basicReport?idCard=" + str(i)
                    l_1.append(s)
                    l_2.append(i)
                # print(l_1)

                for i in range(len(l_1)):
                    self.Web_PO.opnLabel(l_1[i])
                    self.Web_PO.swhLabel(i + 1)

                # sleep(8)
                # self.Web_PO.isEleTextExistByXForWait("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", '待上传市级平台', 30)
                print("已完成,", k1, "第", k, "页 =>", l_2)

                for i in range(len(l_1)):
                    self.Web_PO.swhLabel(1)
                    self.Web_PO.cls()
                self.Web_PO.swhLabel(0)

    def run(self, varUser, varPass, d_2):

        # 1，登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrl + "/login")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        # 验证码
        # self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", "1")
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
        for i in range(10):
            dataURI = self.Web_PO.getAttrValueByX(u"//img[@class='login-code-img']", "src")
            imgFile = Base64_PO.base64ToImg(dataURI)
            captcha = Captcha_PO.getCaptchaByDdddOcr(imgFile)
            File_PO.removeFile('', imgFile)
            # print(captcha)
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", captcha)
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
            if self.Web_PO.isEleExistByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button") == False:
                break

        # 2，遍历身份id
        for k1, v1 in d_2.items():
            for k, v in v1.items():
                l_1 = []
                for i in v:
                    s = varUrl + "#/SignManage/signAssess/component/basicReport?idCard=" + str(i)
                    # s = "http://10.207.237.160:8088/login#/SignManage/signAssess/component/basicReport?idCard=" + str(i)
                    l_1.append(s)
                print(l_1)

                for i in range(len(l_1)):
                    self.Web_PO.opnLabel(l_1[i])
                    self.Web_PO.swhLabel(i + 1)
                    sleep(2)
                    self.Web_PO.isEleExistByXForWait("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", 30)
                    s_text = self.Web_PO.getTextByX("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]")
                    if s_text == "上传报告":
                        self.Web_PO.scrollViewByX(
                            "/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]")
                        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", 1)
                        if self.Web_PO.isEleExistByX("/html/body/div[5]/div/div/div[3]/button[2]"):
                            self.Web_PO.clkByX("/html/body/div[5]/div/div/div[3]/button[2]", 1)
                        elif self.Web_PO.isEleExistByX("/html/body/div[3]/div/div/div[3]/button[2]"):
                            self.Web_PO.clkByX("/html/body/div[3]/div/div/div[3]/button[2]", 1)

                    # sleep(2)
                    # l_ = self.Web_PO.getTextByXs("//span")
                    # sleep(1)
                    # for j in l_:
                    #     if j == "上传报告":
                    #         self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]")
                    #         self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", 1)
                    #         if self.Web_PO.isEleExistByX("/html/body/div[5]/div/div/div[3]/button[2]"):
                    #             self.Web_PO.clkByX("/html/body/div[5]/div/div/div[3]/button[2]", 1)
                    #         elif self.Web_PO.isEleExistByX("/html/body/div[3]/div/div/div[3]/button[2]"):
                    #             self.Web_PO.clkByX("/html/body/div[3]/div/div/div[3]/button[2]", 1)
                sleep(8)
                self.Web_PO.isEleTextExistByXForWait("/html/body/div[1]/div/div[2]/section/div/div/section/footer/button[3]", '待上传市级平台', 30)
                print("已完成", k1, "第", k, "页")

                for i in range(10):
                    self.Web_PO.swhLabel(1)
                    self.Web_PO.cls()
                self.Web_PO.swhLabel(0)



    def getIdcardTest(self, varDoc):
        # 获取每个医生所管理的身份证列表

        # 注册信号处理函数
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

        # 登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrlTest)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", Configparser_PO.USER("user"))
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", Configparser_PO.USER("password"))
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", "1")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)

        # 居民健康服务 - 健康评估及干预
        self.Web_PO.opnLabel(varUrlTest + "/#/SignManage/signAssess", 1)
        self.Web_PO.swhLabel(1)

        # # 人群分类
        # self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[3]/div/div/div/div/div/input", 2)
        # # 老年人
        # self.Web_PO.clkByX("/html/body/div[2]/div[2]/div/div/div[1]/ul/li[4]", 2)
        #
        # # 家庭医生
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input",2)
        li_qty = self.Web_PO.getQtyByXs("/html/body/div[2]/div[3]/div/div/div[1]/ul/li")
        for i in range(int(li_qty)):
            varDocName = self.Web_PO.getTextByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[" + str(i+1) + "]/span")
            if varDocName == varDoc:
                self.Web_PO.clkByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[" + str(i+1) + "]")  # 修改l[2]
                break
        #
        # # 本年度上传情况
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input", 2)
        self.Web_PO.clkByX("/html/body/div[2]/div[12]/div/div/div[1]/ul/li[1]", 2)
        #
        # 已点击上传
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[2]/div/div/div/div/div/input", 2)
        self.Web_PO.clkByX("/html/body/div[2]/div[13]/div/div/div[1]/ul/li[1]", 2)
        #
        # # 查询
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[3]/div/button")

        # 定位到底部
        self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input")
        # 获取 共 ？条
        isQty = self.Web_PO.getTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[1]")
        # print(isQty)  # 共 12 条
        if isQty != "共 0 条":
            # qty  获取总页数

            li_qty = self.Web_PO.getQtyByXs("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/ul/li")
            # print(li_qty)

            if int(li_qty) < 7:
                qty = int(li_qty)
            else:
                qty = 111111

            d_1 = {}
            d_2 = {}
            for k in range(qty):
                # 前往第几页
                self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input")
                self.Web_PO.setTextTabByX2("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input", k+1, 2)
                ele = self.Web_PO.getSuperEleByX("//div[text()='姓名']", "../../../../../..")
                tr_qty = self.Web_PO.eleGetQtyByX(ele, ".//div[3]/div/div[1]/div/table/tbody/tr")
                # print(tr_qty)
                l_ = []
                for i in range(int(tr_qty)):
                    idcard = self.Web_PO.eleGetTextByX(ele, ".//div[3]/div/div[1]/div/table/tbody/tr["+ str(i+1)+ "]/td[9]/div")
                    l_.append(idcard)
                pp = (str(varDoc) + str(k+1) + str(l_))
                self.logger.info(pp)
                print(varDoc, k+1, l_)
                d_1[k+1] = l_
            d_2[varDoc] = d_1
            # print(d_2)
            File_PO.dict2jsonfile(varDoc + ".json", d_2)
            # dd_ = File_PO.jsonfile2dict(varDoc + ".json")
            # print(dd_)
            return d_2

    def getIdcard(self, varUser, varPass, varDoc):
        # 获取每个医生所管理的身份证列表
        # 登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrlTest)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        for i in range(10):
            dataURI = self.Web_PO.getAttrValueByX(u"//img[@class='login-code-img']", "src")
            imgFile = Base64_PO.base64ToImg(dataURI)
            captcha = Captcha_PO.getCaptchaByDdddOcr(imgFile)
            File_PO.removeFile('', imgFile)
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", captcha)
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
            if self.Web_PO.isEleExistByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button") == False:
                break

        # 居民健康服务 - 健康评估及干预
        self.Web_PO.opnLabel(varUrlTest + "/#/SignManage/signAssess", 1)
        self.Web_PO.swhLabel(1)

        # # 人群分类
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[3]/div/div/div/div/div/input", 2)
        # # 老年人
        self.Web_PO.clkByX("/html/body/div[2]/div[2]/div/div/div[1]/ul/li[4]", 2)
        #
        # # 家庭医生
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input",2)
        li_qty = self.Web_PO.getQtyByXs("/html/body/div[2]/div[3]/div/div/div[1]/ul/li")
        # print(li_qty)
        for i in range(int(li_qty)):
            varDocName = self.Web_PO.getTextByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[" + str(i+1) + "]/span")
            if varDocName == varDoc:
                self.Web_PO.clkByX("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[" + str(i+1) + "]")  # 修改l[2]
                break
        #
        # # 本年度上传情况
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[1]/div/div/div/div/div/input", 2)
        self.Web_PO.clkByX("/html/body/div[2]/div[12]/div/div/div[1]/ul/li[1]", 2)
        #
        # 已点击上传
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[2]/div/div/div/div/div/input", 2)
        self.Web_PO.clkByX("/html/body/div[2]/div[13]/div/div/div[1]/ul/li[1]", 2)
        #
        # # 查询
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[3]/div[3]/div/button")

        # 定位到底部
        self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input")
        # 获取 共 ？条
        isQty = self.Web_PO.getTextByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[1]")
        print(isQty)  # 共 12 条
        if isQty != "共 0 条":
            # qty  获取总页数

            li_qty = self.Web_PO.getQtyByXs("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/ul/li")
            print(li_qty)

            if int(li_qty) < 7:
                qty = int(li_qty)
            else:
                qty = 111111

            d_1 = {}
            for k in range(qty):
                # 前往第几页
                self.Web_PO.scrollViewByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input")
                self.Web_PO.setTextTabByX2("/html/body/div[1]/div/div[2]/section/div/div/main/div[3]/div/span[3]/div/input", k+1, 2)
                ele = self.Web_PO.getSuperEleByX("//div[text()='姓名']", "../../../../../..")
                tr_qty = self.Web_PO.eleGetQtyByX(ele, ".//div[3]/div/div[1]/div/table/tbody/tr")
                # print(tr_qty)
                l_ = []
                for i in range(int(tr_qty)):
                    idcard = self.Web_PO.eleGetTextByX(ele, ".//div[3]/div/div[1]/div/table/tbody/tr["+ str(i+1)+ "]/td[9]/div")
                    l_.append(idcard)
                print(k+1, l_)
                d_1[k+1] = l_
            return d_1



    def getDocTest(self, varUser, varPass):
        # 获取家庭医生列表顺序名单(测试环境)
        # 登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrlTest)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", "1")
        self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)

        # 居民健康服务 - 健康评估及干预
        self.Web_PO.opnLabel(varUrlTest + "/#/SignManage/signAssess", 1)
        self.Web_PO.swhLabel(1)

        # # 家庭医生
        self.Web_PO.clkByX(
            "/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input")
        l_doc = self.Web_PO.getTextByXs("/html/body/div[2]/div[3]/div/div/div[1]/ul/li")
        d_doc = dict(enumerate(l_doc, start=1))
        d_doc = {v: k for k, v in d_doc.items()}
        return d_doc

    def getDoc(self, varUser, varPass):
        # 获取家庭医生列表顺序名单
        # 登录
        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(varUrl + "/login")
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[1]/div/div/div/input", varUser)
        self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[2]/div/div/div/input", varPass)
        for i in range(10):
            dataURI = self.Web_PO.getAttrValueByX(u"//img[@class='login-code-img']", "src")  # getValueByAttr
            imgFile = Base64_PO.base64ToImg(dataURI)
            captcha = Captcha_PO.getCaptchaByDdddOcr(imgFile)
            File_PO.removeFile('', imgFile)
            # print(captcha)
            self.Web_PO.setTextByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[3]/div/div/div[1]/input", captcha)
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button", 2)
            if self.Web_PO.isEleExistByX("/html/body/div[1]/div/div[2]/div[1]/div[2]/form/div[5]/button") == False:
                break

            # 居民健康服务 - 健康评估及干预
            self.Web_PO.opnLabel(varUrl + "/#/SignManage/signAssess", 1)
            self.Web_PO.swhLabel(1)

            # # 家庭医生
            self.Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div[1]/form/div[1]/div[4]/div/div/div/div/div/input")
            l_doc = self.Web_PO.getTextByXs("/html/body/div[2]/div[3]/div/div/div[1]/ul/li")
            d_doc = dict(enumerate(l_doc, start=1))
            d_doc = {v: k for k, v in d_doc.items()}
            return d_doc

