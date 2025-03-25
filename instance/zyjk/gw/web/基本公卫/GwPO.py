# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2023-7-25
# Description:
# https://chromedriver.storage.googleapis.com/index.html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import sys
sys.path.append("/Users/linghuchong/Downloads/51/Python/project/")
# sys.path.append('../../..')

from PO.WebPO import *
Web_PO = WebPO("chrome")

from PO.ListPO import *
List_PO = ListPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.SysPO import *
Sys_PO = SysPO()

from PO.Base64PO import *
Base64_PO = Base64PO()

import logging, os, sys
import signal
import ddddocr

from collections import ChainMap

# d_g_type_func = {}

# exec("""for i in range(2):
#     self.dropdownDateByOne(dd_text_xpath[k], v[i])""")


class GwPO():

    def __init__(self, varFile):
        # 配置日志
        if os.name == 'nt':
            logging.basicConfig(filename=varFile, level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
        else:
            logging.basicConfig(filename=varFile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        # print(varFile, datetime.datetime.now())

        self.selectors = {
            'form': "//form",
            'dropdown_class': "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']",
            'dropdown_class_dropdown': "//div[@class='el-popper is-pure is-light el-select__dropdown' and @aria-hidden='false']",
            'dropdown_dropdown_1': "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']/div/div/div[1]/ul/li",
            'dropdown_dropdown_2': "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']/div/div[2]/div[1]/ul/li",
            'dropdown_dropdown_3': "//div[@class='el-popper is-pure is-light el-cascader__dropdown' and @aria-hidden='false']/div/div[3]/div[1]/ul/li",
            'dropdown_popper': "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li",
            'button_save_only': ".//span[text()='仅保存']",
            'button_save_review': ".//span[text()='保存复核']",
            'button_cancel': ".//span[text()='取消']",
            'associate_family_confirm': ".//div[3]/div/button[1]",
            'associate_family_cancel': ".//div[3]/div/button[2]"
        }

        self.d_g_type_func = {'文本': 'Web_PO.setTextEnterByX(dd_text_xpath[k], v)',
                         '单下拉框': "Web_PO.dropdown(dd_text_xpath[k],  v)",
                         '管理机构': 'self.__gljg(ele, k, v)',
                         '日期': 'Web_PO.dropdownDate1(dd_text_xpath[k], v)'}

    def __handle_signal(self, signum, frame):
        # 定义信号处理函数
        self.logger.info('Received signal: {}'.format(signal.Signals(signum).name))
        self.logger.info('Program is terminating...')
        # 在这里可以添加额外的清理代码或日志记录

    def clsApp(self, varApp):

        '''
        关闭应用程序
         # clsApp("chrome.exe")
        '''

        l_pid = []
        pids = psutil.pids()
        for pid in pids:
            p = psutil.Process(pid)
            if p.name() == varApp:
                l_pid.append(pid)
        for i in range(len(l_pid)):
            p = psutil.Process(l_pid[i])
            p.terminate()

    def _sm2(self, Web_PO):

        # Web_PO.openURL("https://config.net.cn/tools/sm2.html")
        Web_PO.opnLabel("https://config.net.cn/tools/sm2.html")
        # 私钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[1]",
                          "124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62")
        # 公钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[2]",
                          '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249')

    def encrypt(self, varSource):
        # 在线sm2加密
        # Web_PO = WebPO("noChrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", varSource)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[1]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", "value")
        return r

    def decrypt(self, varEncrypt):
        # 在线sm2解密
        # Web_PO = WebPO("chrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", varEncrypt)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[2]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", "value")
        Web_PO.cls()
        return r

    def getDecode(self, varKey, varSm2Data):

        # 在线sm2解密数据
        d = {}
        # Web_PO.openURL("https://the-x.cn/zh-cn/cryptography/Sm2.aspx")
        Web_PO.opnLabel("https://the-x.cn/zh-cn/cryptography/Sm2.aspx")
        Web_PO.swhLabel(1)
        # 解密秘钥：124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
        Web_PO.setTextByX("/html/body/div/form/div[1]/div[1]/div[1]/textarea",
                          "124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62")
        Web_PO.setTextByX("/html/body/div/form/div[1]/div[1]/div[2]/textarea", varSm2Data)
        Web_PO.clkByX("/html/body/div/form/div[2]/div[2]/input[2]", 2)
        s_result = Web_PO.getAttrValueByX("/html/body/div/form/div[3]/textarea", "value")
        d_result = eval(s_result)
        d[varKey] = d_result
        Web_PO.cls()
        Web_PO.swhLabel(0)
        return d

    def login(self, varUrl, varUser, varPass):
        # 登录
        Web_PO.openURL(varUrl)
        Web_PO.driver.maximize_window()  # 全屏
        # Web_PO.setTextByX("//input[@placeholder='请输入用户名']", varUser)
        # Web_PO.setTextByX("//input[@placeholder='输入密码']", varPass)
        # Web_PO.clkByX("//button[@type='button']", 2)

        d_ = Web_PO.getValueXpathByLabel("input", "placeholder")
        Web_PO.setTextByX(d_['请输入用户名'], varUser)
        Web_PO.setTextByX(d_['输入密码'], varPass)

        d_ = Web_PO.getTextXpathByLabel("button", "/span")
        Web_PO.clkByX(d_['登录'], 2)

        # 系统接口404
        l_ = Web_PO.getTextByXs("//div")
        if '系统接口404异常' in l_:
            print('系统接口404异常')
            self.logger.error('系统接口404异常')
            Web_PO.cls()
            sys.exit(0)

    def getMenu2Url(self):

        # 获取菜单连接

        # 统计ur数量
        # c = Web_PO.getCount("ul")
        c = Web_PO.getCountByTag("ul")
        varLabelCount = c - 3

        # 获取二级菜单名
        Web_PO.clsDisplayByTagName("ul", varLabelCount)  # 展开所有二级菜单（去掉display：none）
        l_menu2 = Web_PO.getTextByXs("//ul/div/a/li/span[2]")
        # print(l_menu2)  # ['健康档案概况', '个人健康档案', '家庭健康档案', ...

        # 获取二级菜单链接
        l_menu2Url = Web_PO.getAttrValueByXs("//a", "href")
        # print(l_menu2Url) # ['http://192.168.0.203:30080/#/phs/HealthRecord/ehrindex', 'http://192.168.0.203:30080/#/phs/HealthRecord/Personal', ...

        # 生成字典{菜单：URL}
        d_menuUrl = dict(zip(l_menu2, l_menu2Url))
        # print(d_menuUrl)  # {'健康档案概况': 'http://192.168.0.203:30080/#/phs/HealthRecord/ehrindex',...

        return d_menuUrl

    def menu1(self, varMenu1):

        '''格式化一级菜单'''

        l_menu = Web_PO.getTextByXs("//li")
        # 去掉''
        l_menu = [i for i in l_menu if i != '']  # ['首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu = (dict(enumerate(l_menu, start=1)))
        # print(d_menu)  # {1: '首页', 2: '基本公卫', 3: '三高共管六病同防', 4: '系统配置', 5: '社区管理', 6: '报表', 7: '更多菜单'}

        # 序列化反转
        d_menu = {v: k for k, v in d_menu.items()}
        print(d_menu)  # {'首页': 1, '基本公卫': 2, '三高共管六病同防': 3, '系统配置': 4, '社区管理': 5, '报表': 6, '更多菜单': 7}

        if varMenu1 == '更多菜单':
            Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[" + (str(d_menu[varMenu1])) + "]")
        else:
            Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[" + (str(d_menu[varMenu1])) + "]")
            # /html/body/div[1]/div/div[1]/div[2]/ul/li[2]
            # /html/body/div[1]/div/div[2]/div[2]/ul/li[3]
            # /html/body/div[1]/div/div[2]/div[2]/ul/li[4]
            # /html/body/div[1]/div/div[2]/div[2]/ul/li[3]
            # /html/body/div[1]/div/div[1]/div[2]/ul/li[3]
            # /html/body/div[1]/div/div[2]/div[2]/ul/li[1]
        # return d_menu

    def menu2(self, d_menu1, varMenuName):

        '''格式化二级菜单'''
        # ['健康档案管理', '', '', '', '', '', '儿童健康管理', '', '', '', '', '孕产妇管理', '', '', '', '', '老年人健康管理', '', '', '', '', '', '肺结核患者管理', '', '', '', '', '残疾人健康管理', '', '', '', '', '严重精神障碍健康管理', '', '', '', '', '健康教育', '', '高血压管理', '', '', '', '糖尿病管理', '', '', '', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单', '', '', '', '', '', '', '']

        Web_PO.clkByX('//*[@id="topmenu-container"]/li[' + str(d_menu1[varMenuName]) + ']', 2)

        # 获取二级菜单
        l_menu2 = Web_PO.getTextByXs("//li")

        # 去掉''
        l_menu2 = [i for i in l_menu2 if i != '']
        # print(l_menu2)  # ['健康档案管理', '儿童健康管理', '孕产妇管理', '老年人健康管理', '肺结核患者管理', '残疾人健康管理', '严重精神障碍健康管理', '健康教育', '高血压管理', '糖尿病管理', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu2 = (dict(enumerate(l_menu2, start=1)))
        # print(d_menu2)  # {1: '健康档案管理', 2: '儿童健康管理', 3: '孕产妇管理', 4: '老年人健康管理', 5: '肺结核患者管理', 6: '残疾人健康管理', 7: '严重精神障碍健康管理', 8: '健康教育', 9: '高血压管理', 10: '糖尿病管理', 11: '首页', 12: '基本公卫', 13: '三高共管六病同防', 14: '系统配置', 15: '社区管理', 16: '报表', 17: '更多菜单'}

        # 序列化反转
        d_menu2 = {v: k for k, v in d_menu2.items()}
        # print(d_menu2)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理': 9, '糖尿病管理': 10, '首页': 11, '基本公卫': 12, '三高共管六病同防': 13, '系统配置': 14, '社区管理': 15, '报表': 16, '更多菜单': 17}

        return d_menu2

        # return d_menu2[varMenuName]

    def menu3(self, d_menu2, varMenu2Name, varMenu3Name):

        '''格式化三级菜单'''
        # ['健康档案管理', '', '', '', '', '', '儿童健康管理', '', '', '', '', '孕产妇管理', '', '', '', '', '老年人健康管理', '', '', '', '', '', '肺结核患者管理', '', '', '', '', '残疾人健康管理', '', '', '', '', '严重精神障碍健康管理', '', '', '', '', '健康教育', '', '高血压管理\n高血压专项\n高血压随访\n高血压报病', '高血压专项', '高血压随访', '高血压报病', '糖尿病管理', '', '', '', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单', '', '', '', '', '', '', '']
        # 定位 '高血压管理\n高血压专项\n高血压随访\n高血压报病'

        Web_PO.clk('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[' + str(d_menu2[varMenu2Name]) + ']/li', 2)

        # 获取三级菜单
        l_menu3 = Web_PO.getTexts("//li")

        # 去掉''
        l_menu3 = [i for i in l_menu3 if i != '']
        # print(l_menu3)  # ['健康档案管理', '儿童健康管理', '孕产妇管理', '老年人健康管理', '肺结核患者管理', '残疾人健康管理', '严重精神障碍健康管理', '健康教育', '高血压管理\n高血压专项\n高血压随访\n高血压报病', '高血压专项', '高血压随访', '高血压报病', '糖尿病管理', '首页', '基本公卫', '三高共管六病同防', '系统配置', '社区管理', '报表', '更多菜单']

        # 序列化成字典
        d_menu3 = (dict(enumerate(l_menu3, start=1)))
        # print(d_menu3)  # {1: '健康档案管理', 2: '儿童健康管理', 3: '孕产妇管理', 4: '老年人健康管理', 5: '肺结核患者管理', 6: '残疾人健康管理', 7: '严重精神障碍健康管理', 8: '健康教育', 9: '高血压管理\n高血压专项\n高血压随访\n高血压报病', 10: '高血压专项', 11: '高血压随访', 12: '高血压报病', 13: '糖尿病管理', 14: '首页', 15: '基本公卫', 16: '三高共管六病同防', 17: '系统配置', 18: '社区管理', 19: '报表', 20: '更多菜单'}

        # 序列化反转
        d_menu3 = {v: k for k, v in d_menu3.items()}
        # print(d_menu3)  # {'健康档案管理': 1, '儿童健康管理': 2, '孕产妇管理': 3, '老年人健康管理': 4, '肺结核患者管理': 5, '残疾人健康管理': 6, '严重精神障碍健康管理': 7, '健康教育': 8, '高血压管理\n高血压专项\n高血压随访\n高血压报病': 9, '高血压专项': 10, '高血压随访': 11, '高血压报病': 12, '糖尿病管理': 13, '首页': 14, '基本公卫': 15, '三高共管六病同防': 16, '系统配置': 17, '社区管理': 18, '报表': 19, '更多菜单': 20}

        for k, v in d_menu3.items():
            if varMenu2Name + "\n" in k:
                list1 = k.split("\n")  # ['高血压管理', '高血压专项', '高血压随访', '高血压报病']
                for i in range(len(list1)):
                    if list1[i] == varMenu3Name:
                        Web_PO.clk('//*[@id="app"]/div/div[1]/div/div[1]/div/ul/div[' + str(
                            d_menu2[varMenu2Name]) + ']/li/ul/div[' + str(i) + ']/a', 2)
                        break
                break



    # todo common

    def __loggerPrint(self, varStatus, varInfor):
        # 日志和打印
        if varStatus == 'info':
            self.logger.info(varInfor)
        elif varStatus == 'error':
            self.logger.error(varInfor)
        print(varInfor)

    def export(self, varFile):
        # 导出
        try:
            ele = Web_PO.getSuperEleByX("//form", ".")
            ele2 = Web_PO.eleGetSuperEleByX(ele, ".//span[text()='导出']", "..")
            Web_PO.eleClkByX(ele2, ".", 2)  # 点击导出
            if os.access(varFile, os.F_OK):
                Web_PO.exportExistFile(varFile)
            else:
                Web_PO.exportFile(varFile)
        except Exception as e:
            print(f"导出过程中发生错误: {e}")

    def __gljg(self, ele, k, v):
        # 管理机构
        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//input", 2)
        if isinstance(v, str):
            if v == '招远市卫健局':
                # 卫健局
                Web_PO.clkByX(self.selectors['dropdown_dropdown_1'] + "/label")
                Web_PO.clkTabByX(self.selectors['dropdown_dropdown_1'] + "/label")
            else:
                # 卫生院
                Web_PO.clkByX(self.selectors['dropdown_dropdown_1'])
                l_2 = Web_PO.getTextByXs(self.selectors['dropdown_dropdown_2'])
                # print(l_2)  # ['金岭镇卫生院', '阜山卫生院', '蚕庄卫生院', '玲珑卫生院', '大秦家卫生院', '道头卫生院', '夏甸卫生院', '毕郭卫生院', '宋家卫生院', '大户卫生院', '南院庄卫生院', '大吴家卫生院', '东庄卫生院', '空挂户', '泉山街道社区卫生服务中心', '梦芝社区卫生服务中心', '辛庄镇卫生院', '张星卫生院', '妇幼保健院']
                if v in l_2:
                    for i in range(len(l_2)):
                        if l_2[i] == v:
                            Web_PO.clkByX(self.selectors['dropdown_dropdown_2'] + "[" + str(i + 1) + "]/label")
                            Web_PO.clkTabByX(self.selectors['dropdown_dropdown_2'] + "[" + str(i + 1) + "]/label")
                            break
        elif isinstance(v, dict):
            # 卫生院
            Web_PO.clkByX(self.selectors['dropdown_dropdown_1'])
            l_2 = Web_PO.getTextByXs(self.selectors['dropdown_dropdown_2'])
            varKey = list(v.keys())[0]
            if varKey in l_2:
                for i in range(len(l_2)):
                    if l_2[i] == varKey:
                        # 卫生室
                        Web_PO.clkByX(self.selectors['dropdown_dropdown_2'] + "[" + str(i + 1) + "]")
                        l_3 = Web_PO.getTextByXs(self.selectors['dropdown_dropdown_3'])
                        # print(l_3)  # ['玲珑镇鲁格庄村卫生室', '玲珑镇官家河村卫生室', '玲珑镇罗山李家村卫生室', '玲珑镇大蒋家村卫生室', '玲珑镇玲珑台上村卫生室']
                        if v[varKey] in l_3:
                            for i in range(len(l_3)):
                                if l_3[i] == v[varKey]:
                                    Web_PO.clkByX(self.selectors['dropdown_dropdown_3'] + "[" + str(i + 1) + "]/label")
                                    Web_PO.clkTabByX(self.selectors['dropdown_dropdown_3'] + "[" + str(i + 1) + "]/label")
                                    break



    def pagination(self, varGoto):

        # 获取页面，跳转页码
        d_ = {}
        ele = Web_PO.getSuperEleByX("//div[@class='my-table-pagination']", '.')
        s_totalRecord = Web_PO.eleGetTextByX(ele, './/div/span[1]')
        s_totalRecord = s_totalRecord.split('共 ')[1].split(' 条')[0]
        d_['totalRecord'] = int(s_totalRecord)  # 共 17 条

        s_totalPage = int(d_['totalRecord'] / 10) + 1
        d_['totalPage'] = s_totalPage  # 2   //2页

        # 设置每页显示40条
        # Web_PO.eleClkByX(ele, './/input', 1)
        # Web_PO.clkByX('/html/body/div[2]/div[15]/div/div/div[1]/ul/li[4]')

        # 前往第几页
        Web_PO.eleSetTextBackspaceEnterByX(ele, './/div/span[3]/div/input', 3, varGoto)
        s_gotoPage = Web_PO.eleGetShadowByXByC(ele, './/div/span[3]/div/input', 'div:nth-last-of-type(1)')
        d_['gotoPage'] = int(s_gotoPage)
        return d_


    def newMedicalInstitution(self, hospital, hospitalCode, hospitalReg, hospitalLevel, hospitalPerson, hospitalAddress, hospitalPhone, hospitalIntro):

        # 新增医疗机构
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[1]/button', 1)
        Web_PO.setText("//input[@placeholder='请输入医院名称']", hospital)
        Web_PO.setText("//input[@placeholder='请输入医院代码']", hospitalCode)
        Web_PO.setText("//input[@placeholder='请输入医院登记号']", hospitalReg)
        Web_PO.jsReadonly("//input[@placeholder='请输入级别']")
        Web_PO.setText("//input[@placeholder='请输入级别']", hospitalLevel)
        Web_PO.setText("//input[@placeholder='请输入医院负责人姓名']", hospitalPerson)
        Web_PO.setText("//input[@placeholder='请输入医院详细地址']", hospitalAddress)
        Web_PO.setText("//input[@placeholder='请输入医院联系电话']", hospitalPhone)
        Web_PO.setText("//textarea[@placeholder='请输入医院介绍']", hospitalIntro)
        Web_PO.clk('/html/body/div[4]/div/div/div[3]/div/button[1]', 1)

    def editMedicalInstitution(self, oldHospital, hospital, hospitalCode, hospitalReg, hospitalLevel, hospitalPerson, hospitalAddress, hospitalPhone, hospitalIntro):

        # 编辑医疗机构
        # 获取列表中指定医院所在的行，点击次行的'编辑'
        varTr = self.getHospitalTR(oldHospital)
        if varTr == None:
            print("warning, 未找到医院名称")
            return None
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(varTr) + ']/td[8]/div/button[1]', 1)

        Web_PO.setText("//input[@placeholder='请输入医院名称']", hospital)
        Web_PO.setText("//input[@placeholder='请输入医院代码']", hospitalCode)
        Web_PO.setText("//input[@placeholder='请输入医院登记号']", hospitalReg)
        Web_PO.jsReadonly("//input[@placeholder='请输入级别']")
        Web_PO.setText("//input[@placeholder='请输入级别']", hospitalLevel)
        Web_PO.setText("//input[@placeholder='请输入医院负责人姓名']", hospitalPerson)
        Web_PO.setText("//input[@placeholder='请输入医院详细地址']", hospitalAddress)
        Web_PO.setText("//input[@placeholder='请输入医院联系电话']", hospitalPhone)
        Web_PO.setText("//textarea[@placeholder='请输入医院介绍']", hospitalIntro)
        Web_PO.clk('/html/body/div[4]/div/div/div[3]/div/button[1]', 1)

    def getHospitalTR(self, varHospital):

        '''获取行'''

        l_1 = Web_PO.getTexts("//tr")
        # 序列化成字典
        d_1 = (dict(enumerate(l_1, start=0)))
        # 序列化反转
        d_1 = {v: k for k, v in d_1.items()}
        for k, v in d_1.items():
            if varHospital + "\n" in k:
                return v

    def editOffice(self, hospital, d_officeCode):

        # 科室维护
        # 获取列表中指定医院所在的行，点击次行的'科室维护'

        varTr = self.getHospitalTR(hospital)
        if varTr == None:
            print("warning, 未找到医院名称")
            return None
        Web_PO.clk('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(varTr) + ']/td[8]/div/button[2]', 1)

        # 获取所有科室
        if Web_PO.isElement("//input"):
            l_office_Code = Web_PO.getValuesByAttr("//input", "value")
            # print(l_office_Code)  # ['骨科', '000', '儿科', '9876']
            d_officeCode_old = List_PO.list2dictBySerial(l_office_Code)
            print(d_officeCode_old)  # {'骨科': '000', '儿科': '9876'}

            # 删除所有科室
            for i in range(len(d_officeCode_old)):
                Web_PO.clk('/html/body/div[5]/div/div/div[2]/form/div[' + str(2) + ']/div[3]/i', 1)

        # 新增科室
        for index, (k, v) in enumerate(d_officeCode.items()):
            Web_PO.clk('/html/body/div[5]/div/div/div[2]/form/div[1]/div[2]/i', 1)
            Web_PO.setText("/html/body/div[5]/div/div/div[2]/form/div[" + str(index+2) + "]/div[1]/div/div/div/input", k)
            Web_PO.setText("/html/body/div[5]/div/div/div[2]/form/div[" + str(index+2) + "]/div[2]/div/div/div/input", v)
        # 保存
        Web_PO.clk('/html/body/div[5]/div/div/div[3]/div/button[1]', 1)

    def _getQty(self):
        # 获取查询结果数量

        if Web_PO.isEleExistByX("//div[@class='el-pagination is-background']/span"):
            if Web_PO.getTextByX("//div[@class='el-pagination is-background']/span") == "共 1 条":
                return 1
            else:
                s_ = Web_PO.getTextByX("//div[@class='el-pagination is-background']/span")
                s_ = s_.split("共 ")[1].split(" 条")[0]
                return s_
        else:
            return 0



    def _jws(self, ele, k, k_sub, v1, _dropdownByX, varLoc):

        if isinstance(v1, list):
            Web_PO.eleRadioSplitLabels(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "无")
            Web_PO.eleRadioSplitLabels(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "有")
            for i in range(len(v1) - 1):
                # +
                Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/i", 2)
            for i in range(len(v1)):
                # 名称
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), "./div[2]/div[" + str(varLoc) + "]/div[2]/div[" + str(i + 1) + "]/div[1]/div[2]/div/div/div/input", v1[i][0])
                # 时间
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), "./div[2]/div[" + str(varLoc) + "]/div[2]/div[" + str(i + 1) + "]/div[2]/div[1]/div/div/div/input", v1[i][1])
        else:
            if v1 != "remain":
                Web_PO.eleRadioSplitLabels(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varLoc) + "]/div[1]/div[2]/div/div/div", "无")
    def _getRadio(self, varField):
        d_ = {}
        ele2 = Web_PO.getSuperEleByX("//div[text()='" + varField + "']", "..")
        l_blood_1 = Web_PO.eleGetTextByXs(ele2, ".//label/span[2]")
        # print(l_blood_1)
        l_blood_tmp = Web_PO.eleGetAttrValueByXs(ele2, ".//label", "class")
        # print(l_blood_tmp)
        l_blood_2 = []
        for i in range(len(l_blood_tmp)):
            if l_blood_tmp[i] == 'el-radio is-disabled is-checked el-radio--default':
                l_blood_2.append(1)
            else:
                l_blood_2.append(0)
        d_blood = dict(zip(l_blood_1, l_blood_2))
        varField = varField.strip()
        d_[varField] = d_blood
        # print(d_)
        return d_
    def _getCheckbox(self, varField):
        d_ = {}
        ele2 = Web_PO.getSuperEleByX("//div[text()='" + varField + "']", "..")
        l_blood_1 = Web_PO.eleGetTextByXs(ele2, ".//label/span[2]")
        # print(l_blood_1)
        l_blood_tmp = Web_PO.eleGetAttrValueByXs(ele2, ".//label", "class")
        # print(l_blood_tmp)
        l_blood_2 = []
        for i in range(len(l_blood_tmp)):
            if l_blood_tmp[i] == 'el-checkbox el-checkbox--default is-disabled is-checked':
                l_blood_2.append('Y')
            else:
                l_blood_2.append('N')
        d_blood = dict(zip(l_blood_1, l_blood_2))
        varField = varField.strip()
        d_[varField] = d_blood
        # print(d_)
        return d_
    def _getText(self, varField, varLoc=".."):
        d_ = {}
        ele = Web_PO.getSuperEleByX("//div[text()='" + varField + "']", varLoc)
        l_ = Web_PO.eleGetShadowByXsByC(ele, ".//div/div/div/input", 'div:nth-last-of-type(1)')
        varField = varField.strip()
        d_[varField] = l_
        return d_
    def _getTextarea(self, varField):
        d_ = {}
        ele = Web_PO.getSuperEleByX("//div[text()='" + varField + "']", "../..")
        l_ = Web_PO.eleGetShadowByXsByC(ele, ".//div/div/div/textarea", 'div:nth-last-of-type(1)')
        varField = varField.strip()
        d_[varField] = l_
        # print(d_)
        return d_
    def _getJWS(self, varField, varQty, l_):
        l_4 = []
        d_2 = {}
        for _ in range(varQty*2):
            l_4.append(l_.pop(0))
        d_2[varField] = l_4
        return d_2
    # def __eleRadioLeftLabel(self, ele, varXpaths, v):
    #     # eleRadioLabels
    #     # 选择单选框
    #     # 内部调用，用于随访
    #     l_ = Web_PO.eleGetTextByXs(ele, varXpaths)
    #     d_3 = dict(enumerate(l_, start=1))
    #     d_4 = {v: k for k, v in d_3.items()}
    #     # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
    #     Web_PO.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]/label", 1)
    # def __eleRadioRightLabel(self, ele, varXpaths, v):
    #     # eleRadioLabels
    #     # 选择单选框
    #     # self.__eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div/div[1]/label", v)
    #     l_ = Web_PO.eleGetTextByXs(ele, varXpaths)
    #     d_3 = dict(enumerate(l_, start=1))
    #     d_4 = {v: k for k, v in d_3.items()}
    #     # print(d_4)  # {'总院': 1, '分院': 2, '门诊部': 3}
    #     Web_PO.eleClkByX(ele, varXpaths + "[" + str(d_4[v]) + "]", 1)


  
 
# =========================================================================================================================================
# =========================================================================================================================================
# =========================================================================================================================================


    # todo 2.1.2 基本公卫 - 健康档案管理 - 个人健康档案

    def __setHealthrecord(self, d_):
        # 居民健康档案（新增、编辑）

        try:
            ele = Web_PO.getSuperEleByX("//form", ".")

            for k, v in d_['data'].items():
                if k in [' 性别 ', ' 民族 ', ' 文化程度 ', ' 职业 ', ' 婚姻状况 ', ' 档案是否开放 ']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input",
                                        v)
                elif k in [' 现住址 ']:
                    address_selectors = [
                        ".//div[1]/div[2]/div/div/div/div/div/input",
                        ".//div[2]/div[1]/div/div/div/div/div/input",
                        ".//div[2]/div[2]/div/div/div/div/div/input",
                        ".//div[3]/div[1]/div/div/div/div/div/input",
                        ".//div[3]/div[2]/div/div/div/div/div/input"
                    ]
                    for i in range(5):
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), address_selectors[i],
                                            v[i])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[4]/div[2]/div/div/div/input", v[5])

                elif k in [' 姓名 ', ' 本人电话 ', ' 联系人姓名 ', ' 联系人电话 ', ' 工作单位 ']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)

                elif k in [' 出生日期 ', ' 建档日期 ']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)

                elif k in [' 血型 ', ' 常住类型 ', ' 血型 ', ' RH血型 ', ' 厨房排风设施 ', ' 燃料类型 ', ' 饮水 ', ' 厕所 ', ' 禽畜栏 ', ' 更新方式 ']:
                    Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)

                elif k in [' 医疗费用支付方式 ']:
                    for i in range(len(v)):
                        self._eleCheckboxPay(Web_PO.eleCommon(ele, k), v[i])

                elif k in [' 药物过敏史 ']:
                    Web_PO.eleCheckboxLeftLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div[1]/div",
                                                       v, ".//div[2]/div/div/div/div/textarea")

                elif k in [' 暴露史 ']:
                    Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon(ele, k), './/div[2]/div/div/div[1]/div', v)

                elif k in [' 既往史 ']:
                    for k1, v1 in v.items():
                        if k1 == '疾病':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[1]/div[1]/div[2]/div/div/div[1]/label",
                                                      list(v1.keys())[0])
                            if list(v1.keys())[0] == "有":
                                for i in range(len(v1['有']) - 1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                                     ".//div[2]/div[1]/div[1]/div[2]/div/div/i", 2)  # +
                                for i in range(len(v1['有'])):
                                    # 疾病名称
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[" + str(
                                        i + 1) + "]/div[1]/div[2]/div/div/div/div/div/input",
                                                        v1['有'][i][0])
                                    # 确诊时间
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[" + str(
                                        i + 1) + "]/div[2]/div[1]/div/div/div/input", v1['有'][i][1])

                        if k1 == '手术':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[2]/div[1]/div[2]/div/div/div[1]/label",
                                                      list(v1.keys())[0])
                            if list(v1.keys())[0] == "有":
                                for i in range(len(v1['有']) - 1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                                     ".//div[2]/div[2]/div[1]/div[2]/div/div/i",
                                                     2)  # +
                                for i in range(len(v1['有'])):
                                    # 手术名称
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[" + str(
                                        i + 1) + "]/div[1]/div[2]/div/div/div/input", v1['有'][i][0])
                                    # 手术时间
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[" + str(
                                        i + 1) + "]/div[2]/div[1]/div/div/div/input", v1['有'][i][1])

                        if k1 == '外伤':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[3]/div[1]/div[2]/div/div/div/label",
                                                      list(v1.keys())[0])
                            if list(v1.keys())[0] == "有":
                                for i in range(len(v1['有']) - 1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                                     ".//div[2]/div[3]/div[1]/div[2]/div/div/i",
                                                     2)  # +
                                for i in range(len(v1['有'])):
                                    # 外伤名称
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div[2]/div[" + str(
                                        i + 1) + "]/div[1]/div[2]/div/div/div/input", v1['有'][i][0])
                                    # 外伤时间
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div[2]/div[" + str(
                                        i + 1) + "]/div[2]/div[1]/div/div/div/input", v1['有'][i][1])

                        if k1 == '输血':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[4]/div[1]/div[2]/div/div/div/label",
                                                      list(v1.keys())[0])
                            if list(v1.keys())[0] == "有":
                                for i in range(len(v1['有']) - 1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                                     ".//div[2]/div[4]/div[1]/div[2]/div/div/i",
                                                     2)  # +
                                for i in range(len(v1['有'])):
                                    # 输血原因
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div[2]/div[" + str(
                                        i + 1) + "]/div[1]/div[2]/div/div/div/input", v1['有'][i][0])
                                    # 输血时间
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[4]/div[2]/div[" + str(
                                        i + 1) + "]/div[2]/div[1]/div/div/div/input", v1['有'][i][1])

                elif k in [' 家族史 ']:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/label",
                                              list(v.keys())[0])
                    if list(v.keys())[0] == '有':
                        for i in range(len(v['有']) - 1):
                            Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/i", 2)  # +
                        for i in range(len(v['有'])):
                            # 疾病名称
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//div[" + str(i + 1) + "]/div[1]/div[2]/div/div/div/div/div/input",
                                                v['有'][i][0])
                            # 与本人关系
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//div[" + str(i + 1) + "]/div[2]/div[2]/div/div/div/div/div/input",
                                                v['有'][i][1])

                elif k in [' 遗传病史 ']:
                    Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/label", v,
                                                     ".//div[2]/div[2]/div/div/div/input")

                elif k in [' 残疾情况 ']:
                    l_ = []
                    for i in range(len(v)):
                        if isinstance(v[i], list):
                            l_ = v[i]
                            Web_PO.eleCheckboxLeftLabelAndText(Web_PO.eleCommon(ele, k),
                                                               ".//div[2]/div/div/div/div[1]/div", v[i],
                                                               ".//div[2]/div/div/div/div[2]/div/div[1]/input")
                        if isinstance(v[i], dict):
                            # print(l_)
                            # 勾选无残疾时，无法输入残疾证号
                            if "无残疾" not in l_:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                     ".//div[2]/div[2]/div/div/div/input", v[i][' 残疾证号 '])

                elif k in [' 家庭情况 ']:
                    for k1, v1 in v.items():
                        if k1 in [' 与户主关系 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input",
                                                v1)
                        elif k1 in [' 户主姓名 ', ' 户主身份证号 ', ' 家庭人口数 ', ' 家庭结构 ']:
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                        elif k1 in [' 居住情况 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div", v1)

                elif k in [' 管理机构 ']:
                    self.__gljg(ele, k, v)

                elif k in [' 更新内容 ']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input", v)

            if d_['button'] == '仅保存':
                Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='仅保存']", ".."), ".", 2)
            elif d_['button'] == '保存复核':
                Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='保存复核']", ".."), ".", 2)
            elif d_['button'] == '取消':
                Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='取消']", ".."), ".", 2)

            #  关联家庭
            # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='关联家庭']", "../.."), ".//div[3]/div/button[1]", 2)  # 确认
            Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='关联家庭']", "../.."), ".//div[3]/div/button[2]",
                             2)  # 取消

            self.logger.info("保存 => " + str(d_))
        except Exception as e:
            self.logger.error(f"Health record update failed: {e}")

    def __getHealthrecord(self, varStatus='更新信息'):
        # 获取居民健康档案

        d_ = self._getText(' 身份证号码 ')
        d_.update(self._getText(' 档案编号 '))
        d_.update(self._getText(' 姓名 '))
        d_.update(self._getText(' 性别 '))
        d_.update(self._getText(' 出生日期 '))
        d_.update(self._getText(' 民族 '))
        d_.update(self._getText(' 现住址 ', "../.."))
        d_.update(self._getText(' 本人电话 '))
        d_.update(self._getText(' 联系人姓名 '))
        d_.update(self._getText(' 联系人电话 '))
        d_.update(self._getRadio(' 常住类型 '))
        d_.update(self._getText(' 文化程度 '))
        d_.update(self._getText(' 职业 '))
        d_.update(self._getText(' 工作单位 '))
        d_.update(self._getText(' 婚姻状况 '))
        d_.update(self._getRadio(' 血型 '))
        d_.update(self._getRadio(' RH血型 '))

        # 医疗费用支付方式
        d_1 = self._getCheckbox(' 医疗费用支付方式 ')
        if d_1['医疗费用支付方式']['城镇职工基本医疗保险'] == 'Y':
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['城镇职工基本医疗保险'] = {'Y': d_2['医疗费用支付方式'][0]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['城镇居民基本医疗保险'] == 'Y':
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['城镇居民基本医疗保险'] = {'Y': d_2['医疗费用支付方式'][1]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['贫困救助'] == 'Y':
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['贫困救助'] = {'Y': d_2['医疗费用支付方式'][2]}
            d_.update(d_1)
        if d_1['医疗费用支付方式']['其他'] == 'Y':
            d_2 = self._getText(' 医疗费用支付方式 ')
            d_1['医疗费用支付方式']['其他'] = {'Y': d_2['医疗费用支付方式'][3]}
            # d_1['医疗费用支付方式']['input'] = d_2['医疗费用支付方式'][3]
            d_.update(d_1)

        # 药物过敏史
        d_1 = self._getCheckbox(' 药物过敏史 ')
        d_.update(d_1)
        if d_1['药物过敏史']['其他药物过敏源'] == "Y":
            d_2 = self._getTextarea(' 药物过敏史 ')
            d_1['药物过敏史']['其他药物过敏源'] = {'Y': d_2['药物过敏史'][0]}
            d_.update(d_1)

        # 暴露史
        d_.update(self._getCheckbox(' 暴露史 '))

        # 既往史
        ele = Web_PO.getSuperEleByX("//div[text()=' 既往史 ']", "..")
        l_ = Web_PO.eleGetTextByXs(ele, ".//div")
        a = (l_[1].count("疾病名称"))
        b = (l_[1].count("手术名称"))
        c = (l_[1].count("外伤名称"))
        d = (l_[1].count("输血原因"))
        l_ = Web_PO.eleGetShadowByXsByC(ele, ".//div/div/div/input", 'div:nth-last-of-type(1)')
        d_1 = self._getJWS("疾病", a, l_)
        d_2 = self._getJWS("手术", b, l_)
        d_1.update(d_2)
        d_3 = self._getJWS("外伤", c, l_)
        d_1.update(d_3)
        d_4 = self._getJWS("输血", d, l_)
        d_1.update(d_4)
        d_5 = {}
        d_5['既往史'] = d_1
        d_.update(d_5)

        # 家族史
        d_1 = self._getRadio(' 家族史 ')
        # print(d_1)  # {'家族史': {'有': 1, '无': 0}}
        if d_1['家族史'] == {}:
            d_1['家族史'] = '无'
        elif d_1['家族史']['有'] == 1:
            d_2 = self._getText(' 家族史 ')
            d_1['家族史']['input'] = d_2['家族史']
        d_.update(d_1)

        # 遗传病史
        d_1 = self._getRadio(' 遗传病史 ')
        d_2 = self._getText(' 遗传病史 ', "../..")
        d_1['遗传病史']['疾病名称'] = d_2['遗传病史'][0]
        d_.update(d_1)

        # 残疾情况
        d_1 = self._getCheckbox(' 残疾情况 ')
        d_.update(d_1)
        if d_1['残疾情况']['其他残疾'] == "Y":
            d_2 = self._getText(' 残疾情况 ')
            d_1['残疾情况']['其他残疾'] = {'Y': d_2['残疾情况'][0]}
            d_.update(d_1)
        d_.update(self._getText(' 残疾证号 '))

        # 家庭情况
        d_1 = self._getText(' 与户主关系 ')
        d_1.update(self._getText(' 户主姓名 '))
        d_1.update(self._getText(' 户主身份证号 '))
        d_1.update(self._getText(' 家庭人口数 '))
        d_1.update(self._getText(' 家庭结构 '))
        d_1.update(self._getRadio(' 居住情况 '))
        d_.update({'家庭情况': d_1})

        # 生活环境
        d_1 = self._getRadio(' 厨房排风设施 ')
        d_1.update(self._getRadio(' 燃料类型 '))
        d_1.update(self._getRadio(' 饮水 '))
        d_1.update(self._getRadio(' 厕所 '))
        d_1.update(self._getRadio(' 禽畜栏 '))
        d_.update({'生活环境': d_1})

        # 建档单位
        d_.update(self._getText(' 建档单位 '))
        d_.update(self._getText(' 管理机构 '))
        d_.update(self._getText(' 档案是否开放 '))

        # 建档日期
        d_.update(self._getText(' 建档日期 '))
        d_.update(self._getText(' 建档人 '))

        if varStatus == '更新信息':
            # 更新信息
            d_.update(self._getText(' 更新日期 '))
            d_.update(self._getRadio(' 更新方式 '))
            d_.update(self._getText(' 更新人 '))
            d_.update(self._getText(' 更新内容 ', "../.."))

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='关闭']", ".."), ".", 2)
        return d_

    def _eleCheckboxPay(self, ele, v, default='remain'):
        # 医疗费用支付方式
        # 选择复选框的值

        # 1, 全部不勾选
        if default != "remain":
            # 城镇职工基本医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div/label", "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div/label", 1)
            # 城镇居民基本医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div/label", 1)
            # 贫困救助
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/label", 1)
            # 商业医疗保险
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", 1)
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[4]/label", 1)
            # 全公费
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[5]/label", 1)
            # 全自费
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[6]/label", 1)
            # 其他
            varClass = Web_PO.eleGetAttrValueByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label",
                                                 "class")
            if varClass == 'el-checkbox el-checkbox--default is-checked':
                Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[2]/div[1]/div/div/div/div[7]/label", 1)

        # 更改
        if isinstance(v, list):
            Web_PO.eleCheckboxLeftLabelAndText(ele, ".//div[2]/div/div/div[1]/div[2]/div[1]/div/div/div/div", v,
                                               ".//div[2]/div/div/div/div[2]/div[2]/div/div/div/div/input")

        if isinstance(v, dict):
            for k1, v1 in v.items():
                if k1 == '城镇职工基本医疗保险':
                    Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[1]/div/div/div")
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/div/input", v1)
                if k1 == '城镇居民基本医疗保险':
                    Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[2]/div[2]/div/div")
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[3]/div/div/div/div/input", v1)
                if k1 == '贫困救助':
                    Web_PO.eleClkByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[1]/div/div")
                    Web_PO.eleSetTextByX(ele, ".//div[2]/div/div/div/div[1]/div[4]/div[2]/div/div/div/input", v1)
  
    def phs_healthrecord_personal_query(self, d_):

        # 个人健康档案 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, "./div/div", 1)  # 展开

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建档人', '本人电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v[1])
                elif k in ['性别', '人群分类', '档案是否开放', '档案状态', '血型', '常住类型', '是否签约', '是否残疾', '今年是否体检', '既往史', '今年是否已更新', '医疗费用支付方式', '档案缺失项目']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期范围', '今年体检日期', '今年更新日期', '建档日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[2]/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div/div[2]/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_personal_new(self, d_):

        # 个人健康档案 - 新增

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='新增']", ".."), ".", 2)

        # 居民健康档案
        self.__setHealthrecord(d_)

    def _phs_healthrecord_personal_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '提醒', '性别', '出生日期时间', '年龄', '上次完成检查类型', '上次随访日期', '下次随访日期', '母亲姓名', '母亲联系电话', '父亲姓名', '父亲联系电话', '管理状态', '管理类别', '登记机构', '身份证号', '家庭住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        # print(l_value)
        l_value = List_PO.dels(l_value, '查看')
        l_value = List_PO.dels(l_value, '更新')
        l_value = List_PO.dels(l_value, '更多')
        # print(l_value)
        l_group = (List_PO.split2(l_value, varOperation))
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 处理人群分类数据
        for i in l_group:
            if '\n' in i[3]:
                t = len(i[3].split("\n"))
                for j in range(t):
                    i.pop(4)
                i.pop(4)
            else:
                i.pop(4)
                i.pop(4)
        # print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_healthrecord_personal_operation(self, d_):

        # 个人健康档案 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                if d_['operate'] == ' 查看 ':
                    ele3 = Web_PO.getSuperEleByX("(//div[text()=' 查看 '])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    self.logger.info(str(d_))
                    return self.__getHealthrecord('查看')
                if d_['operate'] == ' 更新 ':
                    ele3 = Web_PO.getSuperEleByX("(//div[text()=' 更新 '])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                elif d_['operate'] == '终结':
                    ele3 = Web_PO.getSuperEleByX("(//div[text()='更多'])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    Web_PO.clkByX("//div[@class='el-popper is-light el-popover' and @role='tooltip' and @aria-hidden='false']/div[1]", 2)
                elif d_['operate'] == '更新历史':
                    ele3 = Web_PO.getSuperEleByX("(//div[text()='更多'])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    Web_PO.clkByX("//div[@class='el-popper is-light el-popover' and @role='tooltip' and @aria-hidden='false']/div[2]", 2)
                elif d_['operate'] == '姓名':
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]/td[2]/div", 2)
                else:
                    ele3 = Web_PO.getSuperEleByX("(//div[text()='" + d_['operate'] + "'])[position()=" + str(
                        self._phs_healthrecord_personal_operation('查看 更新 更多', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)


            elif d_['operate'] == '更新' and d_['operate2'] in ['仅保存', '保存复核']:
                # 居民健康档案
                self.__setHealthrecord(d_)

            elif d_['operate'] == '终结':
                ele = Web_PO.getSuperEleByX("//span[text()='终结健康档案']", "../..")
                # 判断档案状态
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                for k, v in d_['data']['档案状态'].items():
                    # 选择档案状态
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '档案状态'), ".//div/div/label", k)
                    if k == '暂不管理':
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, '暂不管理原因'), ".//input", _dropdownByX, v['暂不管理原因'])
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, '暂不管理日期'), ".//input", v['暂不管理日期'])
                    elif k == '已死亡':
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, '档案注销日期'), ".//input", v['档案注销日期'])
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, '死亡日期'), ".//input", v['死亡日期'])
                # Web_PO.eleClkByX(ele2, ".//button[1]")  # 确认
                Web_PO.eleClkByX(ele, ".//button[2]")  # 取消

            elif d_['operate'] == '更新历史':
                ele2 = Web_PO.getSuperEleByX("//span[text()='更新历史']", "../..")
                Web_PO.eleClkByX(ele2, ".//button[1]")  # 关闭

            elif d_['operate'] == '姓名' and d_['operate2'] == '更新':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='更新']", ".."), ".", 2)
                # 居民健康档案
                self.__setHealthrecord(d_)

            elif d_['operate'] == '姓名' and d_['operate2'] == '获取':
                self.logger.info(str(d_))
                # 居民健康档案
                return self.__getHealthrecord()

            else:
                print("error, 无法操作!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))





    # todo 2.1.3 基本公卫 - 健康档案管理 - 家庭健康档案

    def phs_healthrecord_family_query(self, d_):

        # 家庭健康档案 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '现住址']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div/div/div/input",  v)
                elif k in ['家庭住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/input",  v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_healthrecord_family_operation(self, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '身份证号', '现住址']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        # print(l_value)  # ['王丽丽', '370624195305061323', '山东省烟台市招远市罗峰街道文化区社区居民委员会打撒发生的', '李丽丽', '372922198510281068', '山东省烟台市招远市罗峰街道文化区社区居民委员会阿德']
        l_group = List_PO.group(l_value, len(l_field))
        # print(l_group)  # [['王丽丽', '370624195305061323', '山东省烟台市招远市罗峰街道文化区社区居民委员会打撒发生的'], ['李丽丽', '372922198510281068', '山东省烟台市招远市罗峰街道文化区社区居民委员会阿德']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_healthrecord_family_operation(self, d_):

        # 家庭健康档案 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                if d_['operate'] == '姓名':
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_healthrecord_family_operation(d_['option'])) + "]/td[1]/div", 2)

            elif d_['operate'] == '更新':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='更新']", ".."), ".", 2)
                # 居民健康档案
                self.__setHealthrecord(d_)

            elif d_['operate'] == '获取':
                self.logger.info(str(d_))
                # # 居民健康档案
                return self.__getHealthrecord()

            else:
                print("error, 无法操作!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))

    def phs_healthrecord_family_maintenance(self, d_):

        # 维护家庭成员

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        Web_PO.clkByX("//tbody/tr[" + str(self._phs_healthrecord_family_operation(d_['option'])) + "]", 2)
        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='维护家庭成员']", ".."), ".")

        ele = Web_PO.getSuperEleByX("(//span[text()='维护家庭成员'])[last()]", "../..")
        Web_PO.eleSetTextEnterByX(ele, ".//div[2]/div/form/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div/div/input", d_['data']['户主姓名'])
        Web_PO.eleSetTextEnterByX(ele, ".//div[2]/div/form/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[3]/div/div/input", d_['data']['户主身份证号'])
        Web_PO.eleDropdown(ele, ".//div[2]/div/form/div/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[4]/div/div/div/div/div/input",  d_['data']['与户主关系'])

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存 ']", ".."), ".", 2)
        # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='取消']", ".."), ".", 2)

        self.logger.info("维护家庭成员 => " + str(d_))





    # todo 2.1.4 基本公卫 - 健康档案管理 - 迁入申请

    def phs_healthrecord_immigration_query(self, d_):

        # 迁入申请 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '申请人']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['状态', '是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['申请日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                elif k in ['申请机构']:
                    self.__gljg(Web_PO.eleCommon(ele, k), k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

            # 查询
            Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

            # 日志
            self.logger.info("查询 => " + str(d_))

    def _phs_healthrecord_immigration_operation(self, varOperation, d_option):

        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '提醒', '性别', '出生日期时间', '年龄', '上次完成检查类型', '上次随访日期', '下次随访日期', '母亲姓名', '母亲联系电话', '父亲姓名', '父亲联系电话', '管理状态', '管理类别', '登记机构', '身份证号', '家庭住址', '操作']

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def _phs_healthrecord_immigration_information(self):

        # 迁入申请 - 查看 - 档案迁移信息

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        d_1 = {}
        # 申请信息
        ele = Web_PO.getSuperEleByX("//div[text()='申请信息']", "../..")
        l_1 = Web_PO.eleGetTextByXs(ele, ".//div")
        l_2 = l_1[0].split("\n")
        l_2.pop(0) # 去掉申请信息
        # print(l_2)  # ['姓名', '六四', '性别', '女', '身份证号', '
        l_application = List_PO.pair2dict(l_2)
        # print(l_application)  # {'姓名': '六四', '性别': '女',
        d_1['申请信息'] = l_application

        # 审批信息
        ele2 = Web_PO.getSuperEleByX("//div[text()='审批信息']")
        l_3 = Web_PO.eleGetTextByXs(ele2, ".//span")
        # print(l_3)  # ['审核结果', '同意', '审核日期', '2025-02-14', '审核人', '卫生院']
        l_approval = List_PO.pair2dict(l_3)
        # print(l_approval)  # {'审核日期': '2024-11-29', '审核人': '1'}
        d_1['审批信息'] = l_approval

        # 关闭
        ele3 = Web_PO.getSuperEleByX("//span[text()='档案迁移信息']", "../..")
        Web_PO.eleClkByX(ele3, ".//button")

        return d_1
    def phs_healthrecord_immigration_operation(self, d_):

        # 迁入申请 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                if d_['operate'] == "查看":
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='查看'])[position()=" + str(
                        self._phs_healthrecord_immigration_operation('查看', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    return self._phs_healthrecord_immigration_information()
                if d_['operate'] == '姓名':
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_healthrecord_family_operation(d_['option'])) + "]/td[1]/div", 2)

            elif d_['operate'] == '更新':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='更新']", ".."), ".", 2)
                # 居民健康档案
                self.__setHealthrecord(d_)

            elif d_['operate'] == '获取':
                self.logger.info(str(d_))
                # # 居民健康档案
                return self.__getHealthrecord()

            else:
                print("error, 无法操作!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))

    def phs_healthrecord_immigration_new(self, d_):

        # 迁入申请 - 新增

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()=' 新增']", ".."), ".", 2)
        ele = Web_PO.getSuperEleByX("//span[text()='新增档案迁入']", "../..")
        varSign = 0
        for k, v in d_.items():
            try:
                if k in ['身份证号']:
                    # 身份证号": {"370685196005183025": ['六四']}
                    # 身份证号": {"370685196005183025": '无'}
                    # 身份证号": {"370685196005183025": ['六四','444']}
                    # 身份证号": {"370685196005183025": '全选'}
                    idcard = list(v.keys())[0]
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/input", idcard)
                    Web_PO.eleClkByX(ele, ".//div[2]/button", 2)  # 查询
                    if isinstance(v[idcard], str):
                        # 全选
                        if v[idcard] == '全选':
                            # 勾选全部
                            Web_PO.eleClkByX(ele, ".//table/tbody/tr/td[1]/div/label")
                    elif isinstance(v[idcard], list):
                        # 勾选单个或多个
                        for i in range(len(v[idcard])):
                            if Web_PO.eleGetTextByX(ele, ".//table/tbody/tr[" + str(i+1) + "]/td[2]/div") == v[i]:
                                Web_PO.eleClkByX(ele, ".//table/tbody/tr[" + str(i+1) + "]/td[1]/div/label")
                if k in ['申请迁入原因']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['迁入地址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[3]/div/div/div/div/input",  v[2])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/input",  v[3])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/div/input",  v[4])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div/div/input", v[5])
            except:
                self.logger.error("新增失败 => " + str(k) + ": " + str(v))

        # Web_PO.eleClkByX(ele, ".//div[3]/div/button[1]", 2)  # 申请键入
        # Web_PO.eleClkByX(ele, ".//div[3]/div/button[2]", 2)  # 取消
        self.logger.info("新增 => " + str(d_))



    # todo 2.1.5 基本公卫 - 健康档案管理 - 迁出审核

    def phs_healthrecord_exit_query(self, d_):

        # 迁出审核 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '申请人']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['状态','是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['申请日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def phs_healthrecord_exit_operation(self, varOperation):

        # 迁出审核 - 操作

        # 获取查询数量
        s_ = self._getQty()
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")

        try:
            # 操作
            if s_ == 1 and varOperation == '同意':
                Web_PO.eleClkByX(ele2, ".//button[1]", 2)
                ele3 = Web_PO.getSuperEleByX("//div[text()=' 同意迁出该居民个人健康档案？ ']", "../..")
                # Web_PO.eleClkByX(ele3, ".//button[1]")  # 确认
                Web_PO.eleClkByX(ele3, ".//button[2]")  # 取消
                self.logger.info("点击" + varOperation)
            elif s_ == 1 and varOperation == '拒绝':
                Web_PO.eleClkByX(ele2, ".//button[2]", 2)
                ele3 = Web_PO.getSuperEleByX("//div[text()='拒绝迁出原因']")
                Web_PO.setTextByX(ele3, ".//textarea", "test222")
                ele4 = Web_PO.getSuperEleByX("//span[text()='档案迁移信息']", "../..")
                # Web_PO.eleClkByX(ele4, ".//button[1]") # 确认
                Web_PO.eleClkByX(ele4, ".//button[2]") # 取消
                self.logger.info("点击" + varOperation)
            else:
                print("查询数量不等于1，无法操作")
                self.logger.error("查询数量不等于1，无法操作")
        except:
            self.logger.error(varOperation + "失败！")



    # todo 2.1.7 基本公卫 - 健康档案管理 - 死亡管理

    def phs_healthrecord_deathmanagement_query(self, d_):

        # 死亡管理 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['死亡日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div/div/div[3]/div/input", v[1])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div/div/div[1]/div/input", v[0])
                elif k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div/div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div/div[1]/div[2]/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/input", v[2])
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_healthrecord_deathmanagement_operation(self, varOperation, d_option):

        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '提醒', '性别', '出生日期时间', '年龄', '上次完成检查类型', '上次随访日期', '下次随访日期', '母亲姓名', '母亲联系电话', '父亲姓名', '父亲联系电话', '管理状态', '管理类别', '登记机构', '身份证号', '家庭住址', '操作']

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key

    def phs_healthrecord_deathmanagement_operation(self, d_):

        # 死亡管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                if d_['operate'] == "档案查看":
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='档案查看'])[position()=" + str(
                        self._phs_healthrecord_deathmanagement_operation('档案查看', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    self.logger.info(str(d_))
                    # 居民健康档案
                    return self.__getHealthrecord('查看')
            else:
                print("error, 无法操作!")

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 => " + str(d_))




    # todo 2.1.8 基本公卫 - 健康档案管理 - 区域档案查询

    def phs_healthrecord_regionalfile_query(self, d_):

        # 区域档案查询 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))



    # todo 2.1.9 基本公卫 - 健康档案管理 - 接诊信息查询

    def phs_healthrecord_diagnosis_query(self, d_):

        # 接诊信息查询 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['就诊日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div/div/div[3]/div/input", v[1])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div/div/div[1]/div/input", v[0])
                elif k in ['导入状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))



    # todo 2.1.10 基本公卫 - 健康档案管理 - 就诊管理

    def phs_healthrecord_visit_query(self, d_):

        # 就诊管理 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div/div/div/input",  v)
                elif k in ['就诊日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div/div/div[3]/div/input", v[1])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div/div/div[1]/div/input", v[0])
                elif k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))




    

    def __isText1(self, ele, d_value, varField, varXpath):
        # 随访表（高血压，糖尿病）， 判断字段是否存在
        # self.__isText1(ele, d_, '随访方式', ".//div[2]/div/div/div")
        if varField in d_value:
            Web_PO.eleScrollViewByX(ele, varXpath, 1)
            Web_PO.eleSetTextByX(ele, varXpath, d_value[varField])

    def __isText2(self, ele, d_value, varField, varXpath1, varXpath2):
        # 随访表（高血压，糖尿病）， 判断字段是否存在
        # self.__isText1(ele, d_, '随访方式', ".//div[2]/div/div/div")
        if varField in d_value:
            Web_PO.eleScrollViewByX(ele, varXpath1, 1)
            Web_PO.eleSetTextByX(ele, varXpath1, d_value[varField][0])
            Web_PO.eleSetTextByX(ele, varXpath2, d_value[varField][1])

    def __isRadioLeft(self, ele, d_value, varField, varTextByX):
        # 随访表（高血压，糖尿病）， 判断字段是否存在
        # self.__isText1(ele, d_, '随访方式', ".//div[2]/div/div/div")
        if varField in d_value:
            Web_PO.eleRadioLeftLabel(ele, varTextByX, d_value[varField])

    def __isRadioRight(self, ele, d_value, varField, varTextByX):
        # 随访表（高血压，糖尿病）， 判断字段是否存在
        # self.__isText1(ele, d_, '随访方式', ".//div[2]/div/div/div")
        if varField in d_value:
            Web_PO.eleRadioRightLabel(ele, varTextByX, d_value[varField])





    # todo 2.2.1 基本公卫 - 高血压管理(common)
    def _setHypertensionFollowUp(self, d_, index=1):
        # 高血压随访（新增）
        ele = Web_PO.getSuperEleByX("(//form)[position()=" + str(index) + "]", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        Web_PO.eleDropdownDate1(ele, ".//div[1]/input", d_['随访日期'])
        self.__isRadioLeft(ele, d_, '随访方式', ".//div[2]/div/div/div")
        if '症状' in d_:
            Web_PO.eleScrollViewByX(ele, ".//div[3]/div/div/div[1]/div", 1)
            Web_PO.eleCheckboxLeftLabel(ele, ".//div[3]/div/div/div[1]/div", d_['症状'])
            for i in d_['症状']:
                if isinstance(i, dict):
                    Web_PO.eleSetTextByX(ele, ".//div[3]/div/div/div[2]/input", i['其他'])
        self.__isText2(ele, d_, '血压', ".//div[4]/div[1]/div/div/input", ".//div[4]/div[2]/div/div/input")
        self.__isText1(ele, d_, '身高', ".//div[5]/div/div/div/input")
        self.__isText2(ele, d_, '体重', ".//div[6]/div[1]/div/div/input", ".//div[6]/div[2]/div/div/input")
        self.__isText1(ele, d_, '心率', ".//div[8]/div/div/div/input")
        self.__isText1(ele, d_, '其他', ".//div[9]/div/div/div/input")
        self.__isText2(ele, d_, '日吸烟量', ".//div[10]/div[1]/div/div/input",
                           ".//div[10]/div[2]/div/div/input")
        self.__isText2(ele, d_, '日饮酒量', ".//div[11]/div[1]/div/div/input",
                           ".//div[11]/div[2]/div/div/input")
        self.__isRadioRight(ele, d_, '运动频率实际', ".//div[12]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '运动频率目标', ".//div[13]/div/div/div[1]/label")
        self.__isText2(ele, d_, '运动时长', ".//div[14]/div[1]/div/div/input",
                           ".//div[14]/div[2]/div/div/input")
        self.__isRadioRight(ele, d_, '摄盐量分级实际', ".//div[15]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '摄盐量分级目标', ".//div[16]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '随访饮食合理性评价', ".//div[17]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '心理调整评价结果', ".//div[18]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '随访遵医行为', ".//div[19]/div/div/div[1]/label")
        self.__isText1(ele, d_, '辅助检查', ".//div[20]/div/div/div/input")
        self.__isRadioRight(ele, d_, '服药依从性', ".//div[21]/div/div/div[1]/label")
        if '药物不良反应' in d_:
            Web_PO.eleRadioLeftLabel(ele, ".//div[22]/div[1]/div/div", d_['药物不良反应'][0])
            if d_['药物不良反应'][0] == '有':
                Web_PO.eleSetTextByX(ele, ".//div[22]/div[2]/div/div/input", d_['药物不良反应'][1])
        self.__isRadioRight(ele, d_, '随访评价结果', ".//div[23]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '下一步管理措施', ".//div[24]/div/div/div[1]/label")
        if '用药情况药物名称1' in d_:
            Web_PO.eleScrollViewByX(ele, ".//div[25]/div/div/div/div/div/input", 2)

            Web_PO.eleClsReadonlyByX(ele, ".//div[25]/div/div/div/div/div/input", 2)
            Web_PO.eleSetTextByX(ele, ".//div[25]/div/div/div/div/div/input", d_['用药情况药物名称1'])
            # 引用HIS
            # Web_PO.eleDropdown(ele, ".//div[25]/div/div/div/div/div/input", _dropdownByX, d_['用药情况药物名称1'])
            Web_PO.eleDropdown(ele, ".//div[26]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药情况用法用量1每日'])  # 每日
            Web_PO.eleSetTextByX(ele, ".//div[26]/div/div[2]/div/div/input", d_['用药情况用法用量1每次'])  # 每次
        if '用药情况药物名称2' in d_:
            Web_PO.eleClsReadonlyByX(ele, ".//div[27]/div/div/div/div/div/input", 2)
            Web_PO.eleSetTextByX(ele, ".//div[27]/div/div/div/div/div/input", d_['用药情况药物名称2'])
            # 引用HIS
            # Web_PO.eleDropdown(ele, ".//div[27]/div/div/div/div/div/input", _dropdownByX, d_['用药情况药物名称2'])
            Web_PO.eleDropdown(ele, ".//div[28]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药情况用法用量2每日'])
            Web_PO.eleSetTextByX(ele, ".//div[28]/div/div[2]/div/div/input", d_['用药情况用法用量2每次'])
        if '用药情况药物名称3' in d_:
            Web_PO.eleClsReadonlyByX(ele, ".//div[29]/div/div/div/div/div/input", 2)
            Web_PO.eleSetTextByX(ele, ".//div[29]/div/div/div/div/div/input", d_['用药情况药物名称3'])
            # 引用HIS
            # Web_PO.eleDropdown(ele, ".//div[29]/div/div/div/div/div/input", _dropdownByX, d_['用药情况药物名称3'])
            Web_PO.eleDropdown(ele, ".//div[30]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药情况用法用量3每日'])
            Web_PO.eleSetTextByX(ele, ".//div[30]/div/div[2]/div/div/input", d_['用药情况用法用量3每次'])
        if '用药调整意见药物名称1' in d_:
            Web_PO.eleScrollViewByX(ele, ".//div[31]/div/div/div/div/div/input", 2)
            Web_PO.eleClsReadonlyByX(ele, ".//div[31]/div/div/div/div/div/input", 2)
            Web_PO.eleSetTextByX(ele, ".//div[31]/div/div/div/div/div/input", d_['用药调整意见药物名称1'])
            # 引用HIS
            # Web_PO.eleDropdown(ele, ".//div[31]/div/div/div/div/div/input", _dropdownByX, d_['用药调整意见药物名称1'])
            Web_PO.eleDropdown(ele, ".//div[32]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药调整意见用法用量1每日'])
            Web_PO.eleSetTextByX(ele, ".//div[32]/div/div[2]/div/div/input", d_['用药调整意见用法用量1每次'])
        if '用药调整意见药物名称2' in d_:
            Web_PO.eleClsReadonlyByX(ele, ".//div[33]/div/div/div/div/div/input", 2)
            Web_PO.eleSetTextByX(ele, ".//div[33]/div/div/div/div/div/input", d_['用药调整意见药物名称2'])
            # 引用HIS
            # Web_PO.eleDropdown(ele, ".//div[33]/div/div/div/div/div/input", _dropdownByX, d_['用药调整意见药物名称2'])
            Web_PO.eleDropdown(ele, ".//div[34]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药调整意见用法用量2每日'])
            Web_PO.eleSetTextByX(ele, ".//div[34]/div/div[2]/div/div/input", d_['用药调整意见用法用量2每次'])
        if '用药调整意见药物名称3' in d_:
            Web_PO.eleClsReadonlyByX(ele, ".//div[35]/div/div/div/div/div/input", 2)
            Web_PO.eleSetTextByX(ele, ".//div[35]/div/div/div/div/div/input", d_['用药调整意见药物名称3'])
            # 引用HIS
            # Web_PO.eleDropdown(ele, ".//div[35]/div/div/div/div/div/input", _dropdownByX, d_['用药调整意见药物名称3'])
            Web_PO.eleDropdown(ele, ".//div[36]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药调整意见用法用量3每日'])
            Web_PO.eleSetTextByX(ele, ".//div[36]/div/div[2]/div/div/input", d_['用药调整意见用法用量3每次'])
        self.__isText1(ele, d_, '转诊原因', ".//div[37]/div/div/div/input")
        self.__isText1(ele, d_, '转入医疗机构及科室', ".//div[38]/div/div/div/input")
        self.__isText1(ele, d_, '联系人', ".//div[39]/div/div/div/input")
        self.__isText1(ele, d_, '联系人电话', ".//div[40]/div/div/div/input")
        self.__isRadioLeft(ele, d_, '结果', ".//div[41]/div/div/div")
        self.__isText1(ele, d_, '备注', ".//div[42]/div/div/div/input")
        if '下次随访日期' in d_:
            Web_PO.eleScrollViewByX(ele, ".//div[43]/div/div/div/input", 2)
            Web_PO.eleDropdownDate1(ele, ".//div[43]/div/div/div/input", d_['下次随访日期'])
        if '随访医生' in d_:
            Web_PO.eleScrollViewByX(ele, "..//div[44]/div/div/div/div/div/input", 2)
            Web_PO.eleDropdown(ele, ".//div[44]/div/div/div/div/div/input", _dropdownByX, d_['随访医生'])
        self.__isText1(ele, d_, '居民签字', ".//div[45]/div/div/div/input")

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", "."), ".", 2)
    def _phs_hypertension_gxyregister_operation_common(self, ele, k, varValue, l_):

        # 获取所有选项，生成映射字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.eleCommon(ele, k), './/label/span[2]')
        # print(l_value)
        d_3 = dict(enumerate(l_value, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        # print(d_4)  # {'男性>55 岁或女性>65 岁': 1, '吸烟': 2, '糖耐量受损': 3, '血脂异常TC≥5.7mmol/L（220mg/dL） 或LDL-C>3.6mmol/L （140mg/dL） 或 HDL-C<1.0mmol/L （40mg/dL）': 4, '早 发 心血 管病家族 史 （一级亲属发病年龄男 性小于 55 岁，女性小于 65 岁）': 5, '腹型肥胖': 6, '血同型半胱氨酸升高': 7, '糖尿病伴微白蛋白尿': 8, '以静息为主的生活方式': 9, '血浆纤维蛋白原增高': 10, '高敏C反应蛋白≥3mg/L或C反应蛋白≥10mg/L': 11, '以上都无': 12}

        # 默认已勾选以上都无，先取消勾选
        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),".//div[2]/div/div/div/div[" + str(d_4[varValue]) + "]/label")  # 不勾选'以上都无'

        # 勾选选项
        for i in range(len(l_)):
            Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), './/div[2]/div/div/div[1]/div[' + str(d_4[l_[i]]) + ']/label', 2)

    # todo 2.2.1 基本公卫 - 高血压管理 - 高血压专项
    def phs_hypertension_gxyregister_query(self, d_):

        # 高血压专项 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建卡医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['收缩压范围', '舒张压范围']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['高血压危险分层', '是否终止管理', '随访提醒分类', '档案状态', '随访评价结果']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['上次随访日期', '下次随访日期', '建卡日期', '建档日期', '出生日期范围']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['档案管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))
    def _phs_hypertension_gxyregister_operation(self, varOperation, d_option):

        # 遍历高血压专项、高血压随访的列表页
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['个人档案编号', '姓名', '提醒', '身份证号', '年龄', '性别', '电话', '居住地址', '建卡日期', '建卡医生', '上次随访日期', '下次随访日期', '操作']
        Web_PO.zoom(100)

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)
        s_class_warn = Web_PO.eleGetAttrValueByX(ele2, ".//td[3]/div/div/div", "style")
        # print(s_class_warn)  # background: rgb(223, 57, 38); width: 16px; height: 16px;
        s_class_warn = s_class_warn.split("rgb")[1].split(";")[0]
        l_value[2] = s_class_warn
        # print(l_value)

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
            if "提醒" in l_field:
                for i in l_group:
                    i.pop(3)
                    i.pop(3)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
            if "提醒" in l_field:
                for i in l_group:
                    i.pop(3)
                    i.pop(3)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_hypertension_gxyregister_operation(self, d_):

        # 高血压专项 - 操作

        try:
            if "data" not in d_:
                if d_['operate'] == '姓名':
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_healthrecord_personal_operation('详情\n评估\n随访', d_['option'])) + "]/td[2]/div", 2)
                else:
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                        self._phs_hypertension_gxyregister_operation('详情\n评估\n随访', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '详情' and d_["operate2"] == '编辑':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='编辑']", ".."), ".", 2)
                ele = Web_PO.getSuperEleByX("//div[text()='高血压患者管理卡']", "..")
                for k, v in d_['data'].items():
                    if k in [' 居住地址 ']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),
                                           ".//div[1]/div[2]/div/div/div/div/div/input",  v[0])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),
                                           ".//div[2]/div[1]/div/div/div/div/div/input",  v[1])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),
                                           ".//div[2]/div[2]/div/div/div/div/div/input",  v[2])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),
                                           ".//div[3]/div[1]/div/div/div/div/div/input",  v[3])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),
                                           ".//div[3]/div[2]/div/div/div/div/div/input",  v[4])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k),
                                                  ".//div[4]/div[2]/div/div/div/input", v[5])
                    elif k in [' 建卡医疗机构 ']:
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                    elif k in [' 终止管理原因 ']:
                        if d_[' 是否终止管理 '] == "是":
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                    elif k in [' 终止管理日期 ']:
                        if d_[' 是否终止管理 '] == "是":
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v)
                    elif k in [' 管理级别 ']:
                        Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)
                    elif k in [' 是否终止管理 ']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                    elif k in [' 建卡医生 ']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                    elif k in [' 确诊日期 ', ' 建卡时间 ']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v)

                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
            elif d_['operate'] == '评估' and d_['operate2'] == '新增':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增']", ".."), ".", 2)
                ele = Web_PO.getSuperEleByX("//div[text()='高血压患者评估']", "..")
                for k, v in d_['data'].items():
                    if k in [' 身高(cm) ', ' 体重(kg) ']:
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                    elif k in [' 血压 ']:
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", v[0])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v[1])
                    elif k in [' 危险因素 ']:
                        if isinstance(v, list):
                            self._phs_hypertension_gxyregister_operation_common(ele, k, '以上都无', v)
                    elif k in [' 靶器官损害 ']:
                        if isinstance(v, list):
                            self._phs_hypertension_gxyregister_operation_common(ele, k, '以上都无', v)
                    elif k in [' 并发症情况 ']:
                        if isinstance(v, list):
                            self._phs_hypertension_gxyregister_operation_common(ele, k, '以上情况均无', v)
                    elif k in [' 高血压分级 ', ' 危险分层 ']:
                        Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)
                    elif k in [' 评估日期 ']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v)

                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

                # ele3 = Web_PO.getSuperEleByX("//div[text()='高血压患者评估']", "../../..")
                # Web_PO.eleClkByX(ele3, ".//button[1]", 2)  # 保存
                # Web_PO.eleClkByX(ele3, ".//button[2]", 2)  # 取消
            elif d_['operate'] == '随访':
                if d_["operate2"] == '新增':
                    # # 判断血压是否有值，如果没值，表示一条随访记录都没有，编辑(第一个)
                    # ele = Web_PO.getSuperEleByX("//form", ".")
                    # s_temp = Web_PO.eleGetShadowByXByC(ele, ".//div[4]/div[1]/div/div[1]/input", "div:nth-last-of-type(1)")
                    # if s_temp != '':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增']", "."), ".", 2)
                elif d_['operate2'] == '引入上次新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上次新增']", "."), ".", 2)
                # 新增、引入上次新增
                self._setHypertensionFollowUp(d_['data'])
            elif d_['operate'] == '姓名' and d_["operate2"] == '更新':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='更新']", ".."), ".", 2)
                # 居民健康档案
                self.__setHealthrecord(d_)
            elif d_['operate'] == '姓名' and d_["operate2"] == '获取':
                self.logger.info(str(d_))
                return self.__getHealthrecord()

            else:
                print("error,无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")

    # todo 2.2.2 基本公卫 - 高血压管理 - 高血压随访
    def phs_hypertension_gxyjob_query(self, d_):

        # 高血压随访 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '随访医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['收缩压范围', '舒张压范围']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访方式', '是否终止管理', '数据源', '随访评价结果']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['随访日期', '出生日期范围']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))
        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)
        # 日志
        self.logger.info("查询 => " + str(d_))
    def _phs_hypertension_gxyjob_operation(self, varOperation, d_option):

        # 遍历高血压专项、高血压随访的列表页
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['个人档案编号', '姓名', '提醒', '身份证号', '年龄', '性别', '电话', '居住地址', '建卡日期', '建卡医生', '上次随访日期', '下次随访日期', '操作']
        Web_PO.zoom(100)

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)  # ['李常', '110101199003075678', '1990-03-07',

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['李常', '110101199003075678', '1990-03-07', ...

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        if d_1 == {}:
            print("warning, 未匹配记录！")
        else:
            max_key = max(d_1, key=d_1.get)
            print("ok, 匹配到第" + str(max_key) + "条记录。")
        return max_key
    def phs_hypertension_gxyjob_operation(self, d_):

        # 高血压随访 - 操作

        try:
            if "data" not in d_:
                if d_['operate'] == '姓名':
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_hypertension_gxyjob_operation('详情\n编辑\n删除', d_['option'])) + "]/td[1]/div", 2)
                else:
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                        self._phs_hypertension_gxyjob_operation('详情\n编辑\n删除', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '详情' and d_["operate2"] == '编辑':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='编辑']", "."), ".", 2)
                # 判断随访日期参数是否存在
                # 获取所有随访日期
                Web_PO.zoom(50)
                ele = Web_PO.getEleByClassName("formList")
                # ele = Web_PO.getSuperEleByX("//div[@class='formList']", '.')
                l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input", 'div:nth-last-of-type(1)')
                print(l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
                index = 0
                for i in range(len(l_followUp_date)):
                    if l_followUp_date[i] == d_['data']['随访日期']:
                        index = index + 1
                Web_PO.zoom(100)
                if index == 0:
                    self.__loggerPrint('info', "高血压随访 - 详情 - 编辑，未匹配到随访日期为", d_['data']['随访日期'], '的记录！')
                else:
                    print("ok, 匹配到第", index, "列随访记录，可编辑。")
                    # 编辑
                    self._setHypertensionFollowUp(d_, index)

            elif d_['operate'] == '编辑':
                if d_["operate2"] == '新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增']", "."), ".", 2)
                elif d_['operate2'] == '引入上次新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上次新增']", "."), ".", 2)
                # 新增、引入上次新增
                self._setHypertensionFollowUp(d_['data'])

            elif d_['operate'] == '删除':
                Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 二次确认

            elif d_['operate'] == '姓名' and d_["operate2"] == '更新':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='更新']", ".."), ".", 2)
                # 居民健康档案
                self.__setHealthrecord(d_)
            elif d_['operate'] == '姓名' and d_["operate2"] == '获取':
                self.logger.info(str(d_))
                return self.__getHealthrecord()

            self.logger.info(str(d_))
        except:
            self.logger.error(str(d_) + "失败！")






    # todo 2.3 基本公卫 - 糖尿病管理(common)
    def _setDiabetesFollowUp(self, d_, index=1):
        # 糖尿病随访
        ele = Web_PO.getSuperEleByX("(//form)[position()=" + str(index) + "]", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        Web_PO.eleDropdownDate1(ele, ".//div[1]/input", d_['随访日期'])
        self.__isRadioLeft(ele, d_, '随访方式', ".//div[2]/div/div/div")
        # Web_PO.eleRadioLeftLabel(ele, ".//div[2]/div/div/div", d_['随访方式'])
        if '症状' in d_:
            Web_PO.eleScrollViewByX(ele, ".//div[3]/div/div/div[1]/div", 1)
            Web_PO.eleCheckboxLeftLabel(ele, ".//div[3]/div/div/div[1]/div", d_['症状'])
            for i in d_['症状']:
                if isinstance(i, dict):
                    Web_PO.eleSetTextByX(ele, ".//div[3]/div/div/div[2]/input", i['其他'])
        self.__isText2(ele, d_, '血压', ".//div[4]/div[1]/div/div/input", ".//div[4]/div[2]/div/div/input")
        # Web_PO.eleSetTextByX(ele, ".//div[4]/div[1]/div/div/input", d_['血压'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[4]/div[2]/div/div/input", d_['血压'][1])
        # Web_PO.eleSetTextByX(ele, ".//div[5]/div/div/div/input", d_['身高'])
        self.__isText1(ele, d_, '身高', ".//div[5]/div/div/div/input")
        self.__isText2(ele, d_, '体重', ".//div[6]/div[1]/div/div/input", ".//div[6]/div[2]/div/div/input")
        # Web_PO.eleSetTextByX(ele, ".//div[6]/div[1]/div/div/input", d_['体重'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[6]/div[2]/div/div/input", d_['体重'][1])
        # self.__eleRadioRightLabel(ele, ".//div[8]/div/div/div/label", d_['足背动脉搏动'])
        self.__isRadioRight(ele, d_, '足背动脉搏动', ".//div[8]/div/div/div/label")

        self.__isText1(ele, d_, '其他', ".//div[9]/div/div/div/input")
        # Web_PO.eleSetTextByX(ele, ".//div[9]/div/div/div/input", d_['其他'])

        # Web_PO.eleSetTextByX(ele, ".//div[10]/div[1]/div/div/input", d_['日吸烟量'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[10]/div[2]/div/div/input", d_['日吸烟量'][1])
        # Web_PO.eleSetTextByX(ele, ".//div[11]/div[1]/div/div/input", d_['日饮酒量'][0])
        # Web_PO.eleSetTextEnterByX(ele, ".//div[11]/div[2]/div/div/input", d_['日饮酒量'][1])
        # Web_PO.eleRadioRightLabel(ele, ".//div[12]/div/div/div[1]/label", d_['运动频率实际'])
        # Web_PO.eleRadioRightLabel(ele, ".//div[13]/div/div/div[1]/label", d_['运动频率目标'])
        # Web_PO.eleSetTextByX(ele, ".//div[14]/div[1]/div/div/input", d_['运动时长'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[14]/div[2]/div/div/input", d_['运动时长'][1])

        self.__isText2(ele, d_, '日吸烟量', ".//div[10]/div[1]/div/div/input", ".//div[10]/div[2]/div/div/input")
        self.__isText2(ele, d_, '日饮酒量', ".//div[11]/div[1]/div/div/input", ".//div[11]/div[2]/div/div/input")
        self.__isRadioRight(ele, d_, '运动频率实际', ".//div[12]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '运动频率目标', ".//div[13]/div/div/div[1]/label")
        self.__isText2(ele, d_, '运动时长', ".//div[14]/div[1]/div/div/input", ".//div[14]/div[2]/div/div/input")

        self.__isText2(ele, d_, '日主食量', ".//div[15]/div[1]/div/div/input", ".//div[15]/div[2]/div/div/input")
        # Web_PO.eleSetTextByX(ele, ".//div[15]/div[1]/div/div/input", d_['日主食量'][0])
        # Web_PO.eleSetTextByX(ele, ".//div[15]/div[2]/div/div/input", d_['日主食量'][1])
        # self.__eleRadioRightLabel(ele, ".//div[16]/div/div/div/label", d_['饮食情况'])
        self.__isRadioRight(ele, d_, '饮食情况', ".//div[16]/div/div/div/label")

        self.__isRadioRight(ele, d_, '心理调整评价结果', ".//div[17]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '随访遵医行为', ".//div[18]/div/div/div[1]/label")
        self.__isText1(ele, d_, '辅助检查', ".//div[19]/div/div/div/input")
        # self.__eleRadioRightLabel(ele, ".//div[17]/div/div/div[1]/label", d_['心理调整评价结果'])
        # self.__eleRadioRightLabel(ele, ".//div[18]/div/div/div[1]/label", d_['随访遵医行为'])
        # Web_PO.eleSetTextByX(ele, ".//div[19]/div/div/div/input", d_['辅助检查'])

        self.__isRadioRight(ele, d_, '服药情况', ".//div[20]/div/div/div[1]/label")
        # self.__eleRadioRightLabel(ele, ".//div[20]/div/div/div[1]/label", d_['服药情况'])

        # Web_PO.eleRadioLeftLabel(ele, ".//div[21]/div[1]/div/div", d_['药物不良反应'][0])
        # if d_['药物不良反应'][0] == '有':
        #     Web_PO.eleSetTextByX(ele, ".//div[21]/div[2]/div/div/input", d_['药物不良反应'][1])

        if '药物不良反应' in d_:
            Web_PO.eleRadioLeftLabel(ele, ".//div[21]/div[1]/div/div", d_['药物不良反应'][0])
            if d_['药物不良反应'][0] == '有':
                Web_PO.eleSetTextByX(ele, ".//div[21]/div[2]/div/div/input", d_['药物不良反应'][1])

        self.__isRadioRight(ele, d_, '随访评价结果', ".//div[22]/div/div/div[1]/label")
        self.__isRadioRight(ele, d_, '下一步管理措施', ".//div[23]/div/div/div[1]/label")
        # self.__eleRadioRightLabel(ele, ".//div[22]/div/div/div[1]/label", d_['随访评价结果'])
        # self.__eleRadioRightLabel(ele, ".//div[23]/div/div/div[1]/label", d_['下一步管理措施'])

        if '用药情况药物名称1' in d_:
            Web_PO.eleScrollViewByX(ele, ".//div[24]/div/div/div/div/div/input", 2)
            Web_PO.eleDropdown(ele, ".//div[24]/div/div/div/div/div/input", _dropdownByX, d_['用药情况药物名称1'])
            Web_PO.eleDropdown(ele, ".//div[25]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药情况用法用量1每日'])  # 每日
            Web_PO.eleSetTextByX(ele, ".//div[25]/div/div[2]/div/div/input", d_['用药情况用法用量1每次'])  # 每次

        # Web_PO.eleClsReadonlyByX(ele, ".//div[24]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[24]/div/div/div/div/div/input", d_['用药情况药物名称1'])
        # Web_PO.eleDropdown(ele, ".//div[25]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['用药情况用法用量1每日'])

        if '用药情况药物名称2' in d_:
            Web_PO.eleDropdown(ele, ".//div[26]/div/div/div/div/div/input", _dropdownByX, d_['用药情况药物名称2'])
            Web_PO.eleDropdown(ele, ".//div[27]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药情况用法用量2每日'])
            Web_PO.eleSetTextByX(ele, ".//div[27]/div/div[2]/div/div/input", d_['用药情况用法用量2每次'])

        # Web_PO.eleClsReadonlyByX(ele, ".//div[26]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[26]/div/div/div/div/div/input", d_['用药情况药物名称2'])
        # Web_PO.eleDropdown(ele, ".//div[27]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['用药情况用法用量2每日'])
        # Web_PO.eleSetTextByX(ele, ".//div[27]/div/div[2]/div/div/input", d_['用药情况用法用量2每次'])

        if '用药情况药物名称3' in d_:
            Web_PO.eleDropdown(ele, ".//div[28]/div/div/div/div/div/input", _dropdownByX, d_['用药情况药物名称3'])
            Web_PO.eleDropdown(ele, ".//div[29]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药情况用法用量3每日'])
            Web_PO.eleSetTextByX(ele, ".//div[29]/div/div[2]/div/div/input", d_['用药情况用法用量3每次'])

        # Web_PO.eleClsReadonlyByX(ele, ".//div[28]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[28]/div/div/div/div/div/input", d_['用药情况药物名称3'])
        # Web_PO.eleDropdown(ele, ".//div[29]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['用药情况用法用量3每日'])
        # Web_PO.eleSetTextByX(ele, ".//div[29]/div/div[2]/div/div/input", d_['用药情况用法用量3每次'])

        if '用药调整意见药物名称1' in d_:
            Web_PO.eleScrollViewByX(ele, ".//div[30]/div/div/div/div/div/input", 2)
            Web_PO.eleDropdown(ele, ".//div[30]/div/div/div/div/div/input", _dropdownByX, d_['用药调整意见药物名称1'])
            Web_PO.eleDropdown(ele, ".//div[31]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药调整意见用法用量1每日'])
            Web_PO.eleSetTextByX(ele, ".//div[31]/div/div[2]/div/div/input", d_['用药调整意见用法用量1每次'])

        # Web_PO.eleScrollViewByX(ele, ".//div[30]/div/div/div/div/div/input", 2)
        # Web_PO.eleClsReadonlyByX(ele, ".//div[30]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[30]/div/div/div/div/div/input", d_['用药调整意见药物名称1'])
        # Web_PO.eleDropdown(ele, ".//div[31]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['用药调整意见用法用量1每日'])

        if '用药调整意见药物名称2' in d_:
            Web_PO.eleDropdown(ele, ".//div[32]/div/div/div/div/div/input", _dropdownByX, d_['用药调整意见药物名称2'])
            Web_PO.eleDropdown(ele, ".//div[33]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药调整意见用法用量2每日'])
            Web_PO.eleSetTextByX(ele, ".//div[33]/div/div[2]/div/div/input", d_['用药调整意见用法用量2每次'])

        # Web_PO.eleSetTextByX(ele, ".//div[31]/div/div[2]/div/div/input", d_['用药调整意见用法用量1每次'])
        # Web_PO.eleClsReadonlyByX(ele, ".//div[32]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[32]/div/div/div/div/div/input", d_['用药调整意见药物名称2'])
        # Web_PO.eleDropdown(ele, ".//div[33]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['用药调整意见用法用量2每日'])

        if '用药调整意见药物名称3' in d_:
            Web_PO.eleDropdown(ele, ".//div[34]/div/div/div/div/div/input", _dropdownByX, d_['用药调整意见药物名称3'])
            Web_PO.eleDropdown(ele, ".//div[35]/div/div[1]/div/div/div/div/input", _dropdownByX, d_['用药调整意见用法用量3每日'])
            Web_PO.eleSetTextByX(ele, ".//div[35]/div/div[2]/div/div/input", d_['用药调整意见用法用量3每次'])

        # Web_PO.eleSetTextByX(ele, ".//div[33]/div/div[2]/div/div/input", d_['用药调整意见用法用量2每次'])
        # Web_PO.eleClsReadonlyByX(ele, ".//div[34]/div/div/div/div/div/input", 2)
        # Web_PO.eleSetTextByX(ele, ".//div[34]/div/div/div/div/div/input", d_['用药调整意见药物名称3'])
        # Web_PO.eleDropdown(ele, ".//div[35]/div/div[1]/div/div/div/div/input", _dropdownByX,
        #                      d_['用药调整意见用法用量3每日'])
        # Web_PO.eleSetTextByX(ele, ".//div[35]/div/div[2]/div/div/input", d_['用药调整意见用法用量3每次'])

        self.__isText1(ele, d_, '转诊原因', ".//div[36]/div/div/div/input")
        self.__isText1(ele, d_, '转入医疗机构及科室', ".//div[37]/div/div/div/input")
        self.__isText1(ele, d_, '联系人', ".//div[38]/div/div/div/input")
        self.__isText1(ele, d_, '联系人电话', ".//div[39]/div/div/div/input")
        self.__isRadioRight(ele, d_, '结果', ".//div[40]/div/div/div/label")
        self.__isText1(ele, d_, '备注', ".//div[41]/div/div/div/input")

        # Web_PO.eleSetTextByX(ele, ".//div[36]/div/div/div/input", d_['转诊原因'])
        # Web_PO.eleSetTextByX(ele, ".//div[37]/div/div/div/input", d_['转入医疗机构及科室'])
        # Web_PO.eleSetTextByX(ele, ".//div[38]/div/div/div/input", d_['联系人'])
        # Web_PO.eleSetTextByX(ele, ".//div[39]/div/div/div/input", d_['联系人电话'])
        # self.__eleRadioRightLabel(ele, ".//div[40]/div/div/div/label", d_['结果'])
        # Web_PO.eleSetTextByX(ele, ".//div[41]/div/div/div/input", d_['备注'])

        if '下次随访日期' in d_:
            Web_PO.eleScrollViewByX(ele, ".//div[42]/div/div/div/input", 2)
            Web_PO.eleDropdownDate1(ele, ".//div[42]/div/div/div/input", d_['下次随访日期'])
        if '随访医生' in d_:
            Web_PO.eleScrollViewByX(ele, "..//div[43]/div/div/div/div/div/input", 2)
            Web_PO.eleDropdown(ele, ".//div[43]/div/div/div/div/div/input", _dropdownByX, d_['随访医生'])
        self.__isText1(ele, d_, '居民签字', ".//div[44]/div/div/div/input")

        # Web_PO.eleDropdownDate1(ele, ".//div[42]/div/div/div/input", d_['下次随访日期'])
        # Web_PO.eleDropdown(ele, ".//div[43]/div/div/div/div/div/input", _dropdownByX, d_['随访医生'])
        # Web_PO.eleSetTextByX(ele, ".//div[44]/div/div/div/input", d_['居民签字'])

        ele = Web_PO.getSuperEleByX("//span[text()='保存']", ".")
        Web_PO.eleClkByX(ele, ".", 2)

    # todo 2.3.1 基本公卫 - 糖尿病管理 - 糖尿病专项
    def phs_diabetes_tnbregister_query(self, d_):

        # 糖尿病专项 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建卡医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否终止管理', '随访提醒分类', '档案状态', '随访评价结果']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期范围']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['上次随访日期', '下次随访日期', '建卡日期', '建档日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['档案管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))
    def _phs_diabetes_tnbregister_operation(self, varOperation, d_option):

        # 糖尿病专项、随访的列表页
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['个人档案编号', '姓名', '提醒', '身份证号', '年龄', '性别', '电话', '居住地址', '建卡日期', '建卡医生', '上次随访日期', '下次随访日期', '操作']
        Web_PO.zoom(100)

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)

        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
        print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        # print(max_key)
        return max_key
    def phs_diabetes_tnbregister_operation(self, d_):

        # 糖尿病专项 - 操作

        try:
            if "data" not in d_:
                if d_['operate'] == '姓名':
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_diabetes_tnbregister_operation('详情\n评估\n随访', d_['option'])) + "]/td[2]/div", 2)
                else:
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                        self._phs_diabetes_tnbregister_operation('详情\n评估\n随访', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '详情' and d_["operate2"] == '编辑':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='编辑']", ".."), ".", 2)

                ele = Web_PO.getSuperEleByX("//th[text()=' 糖尿病患者管理卡 ']", "../..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                for k, v in d_['data'].items():
                    if k in [' 居住地址 ']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/div/div/input", _dropdownByX, v[1])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v[2])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/div/div/input", _dropdownByX, v[3])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/div/div/input", _dropdownByX, v[4])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//td[7]/div/div/div/input", v[5])
                    elif k in ['终止管理原因']:
                        if d_['data'][' 是否终止管理 '] == "是":
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['终止管理日期']:
                        if d_['data'][' 是否终止管理 '] == "是":
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[6]/div/div/div/input", v)
                    elif k in [' 是否终止管理 ']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['建卡医生']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v)
                    elif k in [' 确诊日期 ']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['建卡时间']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)

                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
            elif d_['operate'] == '评估' and d_['operate2'] == '新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//th[text()=' 糖尿病患者评估 ']", "../..")
                    for k, v in d_['data'].items():
                        if k in [' 空腹血糖 ', ' 糖化血红蛋白 ', ' BMI评价 ', ' 高密度脂蛋白胆固醇 ', ' 吸烟 ', ' 体育锻炼 ', ' 遵医行为 ', ' 心理状态 ', ' 降糖效果 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                        if k in [' 餐后血糖 ', ' 血压评价 ', ' 总胆固醇 ', ' 低密度脂蛋白胆固醇 ', ' 饮酒 ', ' 食盐摄入量 ',' 饮食 ', ' 总体评价 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label", v)
                        if k in ['管理程度']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/label", v)
                        elif k in ['评估日期']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/input", v)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
            elif d_['operate'] == '随访':
                if d_["operate2"] == '新增':
                    # # 判断血压是否有值，如果没值，表示一条随访记录都没有，编辑(第一个)
                    # ele = Web_PO.getSuperEleByX("//form", ".")
                    # s_temp = Web_PO.eleGetShadowByXByC(ele, ".//div[4]/div[1]/div/div[1]/input", "div:nth-last-of-type(1)")
                    # if s_temp != '':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增']", "."), ".", 2)
                if d_['operate2'] == '引入上次新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上次新增']", "."), ".", 2)
                # 新增\引入上次新增
                self._setDiabetesFollowUp(d_['data'])

            elif d_['operate'] == '姓名' and d_["operate2"] == '更新':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='更新']", ".."), ".", 2)
                # 居民健康档案
                self.__setHealthrecord(d_)
            elif d_['operate'] == '姓名' and d_["operate2"] == '获取':
                self.logger.info(str(d_))
                return self.__getHealthrecord()

            else:
                print("error,无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")

    # todo 2.3.2 基本公卫 - 糖尿病管理 - 糖尿病随访
    def phs_diabetes_tnbjob_query(self, d_):

        # 糖尿病随访 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '随访医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['空腹血糖']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访方式', '是否终止管理', '数据源', '随访评价结果']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期范围']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))
        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)
        # 日志
        self.logger.info("查询 => " + str(d_))
    def _phs_diabetes_tnbjob_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        # 缩小页面，获取所有的字段
        Web_PO.zoom(50)
        # 获取字段列表
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['姓名', '身份证号', '出生日期', '电话', '居住地址', '性别', '随访医生', '空腹血糖', '随访方式', '随访日期', '随访评价结果', '下次随访日期', '数据源', '操作']
        Web_PO.zoom(100)

        # 获取列表所有制
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        if d_1 == {}:
            print("warning, 未匹配记录, 请检查字段是否存在！")
        else:
            print("ok, 匹配到", d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_diabetes_tnbjob_operation(self, d_):

        # 糖尿病随访 - 操作

        try:
            if "data" not in d_:
                if d_['operate'] == '姓名':
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_diabetes_tnbjob_operation('详情\n编辑\n删除', d_['option'])) + "]/td[1]/div", 2)
                else:
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                        self._phs_diabetes_tnbjob_operation('详情\n编辑\n删除', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '详情' and d_["operate2"] == '编辑':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='编辑']", "."), ".", 2)

                # 定位第几个随访日期
                Web_PO.zoom(50)
                ele = Web_PO.getEleByClassName("formList")
                # ele = Web_PO.getSuperEleByX("//div[@class='formList']", '.')
                l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input", 'div:nth-last-of-type(1)')
                # print(l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
                index = 0
                for i in range(len(l_followUp_date)):
                    if l_followUp_date[i] == d_['data']['随访日期']:
                        index = index + 1
                Web_PO.zoom(100)
                if index == 0:
                    self.__loggerPrint('info', "糖尿病随访 - 详情 - 编辑，未匹配到随访日期为", d_['data']['随访日期'], '的记录！')
                else:
                    print("ok, 匹配到第", index, "列随访记录，可编辑。")
                    # 编辑
                    self._setDiabetesFollowUp(d_['data'], index)

            elif d_['operate'] == '编辑':
                if d_["operate2"] == '新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增']", "."), ".", 2)
                elif d_['operate2'] == '引入上次新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上次新增']", "."), ".", 2)
                # 新增、引入上次新增
                self._setDiabetesFollowUp(d_['data'])

            elif d_['operate'] == '删除':
                Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 二次确认

            elif d_['operate'] == '姓名' and d_["operate2"] == '更新':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='更新']", ".."), ".", 2)
                # 居民健康档案
                self.__setHealthrecord(d_)
            elif d_['operate'] == '姓名' and d_["operate2"] == '获取':
                self.logger.info(str(d_))
                return self.__getHealthrecord()



            # elif d_['operate'] == '编辑' and "operate2" in d_['index']:
            #     if d_['index']['operate2'] == '编辑或新增':
            #         # 获取所有随访日期
            #         Web_PO.zoom(50)
            #         ele = Web_PO.getEleByClassName("formList")
            #         # ele = Web_PO.getSuperEleByX("//div[@class='formList']", '.')
            #         l_followUp_date = Web_PO.eleGetShadowByXsByC(ele, ".//form/div[1]/div/div/div/input", 'div:nth-last-of-type(1)')
            #         print(l_followUp_date)  # ['2025-02-21', '2025-02-19', '2025-02-14', '2025-02-13']
            #         index = 0
            #         for i in range(len(l_followUp_date)):
            #             if l_followUp_date[i] == d_['index']['随访日期']:
            #                 index = i + 1
            #         Web_PO.zoom(100)
            #         if index == 0:
            #             print("warning, 未匹配记录, 新增随访日期为", d_['index']['随访日期'], '的记录.')
            #             ele3 = Web_PO.getSuperEleByX("//span[text()='新增']", ".")
            #             Web_PO.eleClkByX(ele3, ".", 2)
            #         else:
            #             print("ok, 匹配到第", index, "列随访记录，可编辑。")
            #     elif d_['index']['operate2'] == '引入上次新增':
            #         ele3 = Web_PO.getSuperEleByX("//span[text()='引入上次新增']", ".")
            #         Web_PO.eleClkByX(ele3, ".", 2)
            #         index = 1
            #
            #     # 新增、编辑、引入上次新增
            #     self._setDiabetesFollowUp(d_, index)

            # elif d_['operate'] == '删除':
            #     # ...
            #     Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 二次确认

            self.logger.info(str(d_))
        except:
            self.logger.error(str(d_) + "失败！")





    # todo 2.4 基本公卫 - 慢性阻塞性肺病管理(common)

    def __phs(self, d_, index=1):

        # 慢性阻塞性肺病管理随访
        # ele = Web_PO.getSuperEleByX("//form", ".")
        ele = Web_PO.getSuperEleByX("(//form)[position()=" + str(index) + "]", ".")

        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        Web_PO.eleDropdownDate1(ele, ".//div[1]/input", d_['随访日期'])
        Web_PO.eleRadioLeftLabel(ele, ".//div[2]/div/div/div", d_['随访方式'])
        Web_PO.eleCheckboxLeftLabel(ele, ".//div[3]/div/div/div[1]/div", d_['症状'])
        for i in d_['症状']:
            if isinstance(i, dict):
                Web_PO.eleSetTextByX(ele, ".//div[3]/div/div/div[2]/input", i['其他'])
        Web_PO.eleSetTextByX(ele, ".//div[4]/div/div/div/input", d_['口唇紫绀'][0])
        Web_PO.eleSetTextByX(ele, ".//div[5]/div/div/div/input", d_['外周水肿'][1])
        Web_PO.eleSetTextByX(ele, ".//div[6]/div/div/div/input", d_['呼吸频率'])
        Web_PO.eleSetTextByX(ele, ".//div[7]/div/div/div/input", d_['心率'])
        Web_PO.eleSetTextByX(ele, ".//div[8]/div/div/div/input", d_['体质指数'])
        Web_PO.eleSetTextByX(ele, ".//div[9]/div/div/div/input", d_['其他'])
        Web_PO.eleCheckboxLeftLabel(ele, ".//div[10]/div/div/div[1]/div[1]/label", d_['症状'])
        for i in d_['合并症']:
            if isinstance(i, dict):
                Web_PO.eleSetTextByX(ele, ".//div[3]/div/div/div[2]/input", i['其他'])

        Web_PO.eleSetTextByX(ele, ".//div[10]/div[1]/div/div/input", d_['日吸烟量'][0])
        Web_PO.eleSetTextByX(ele, ".//div[10]/div[2]/div/div/input", d_['日吸烟量'][1])
        Web_PO.eleSetTextByX(ele, ".//div[11]/div[1]/div/div/input", d_['日饮酒量'][0])
        Web_PO.eleSetTextEnterByX(ele, ".//div[11]/div[2]/div/div/input", d_['日饮酒量'][1])

        Web_PO.eleScrollViewByX(ele, ".//div[12]/div/div/div[1]/label", 2)
        Web_PO.eleRadioRightLabel(ele, ".//div[12]/div/div/div[1]/label", d_['运动频率实际'])
        Web_PO.eleRadioRightLabel(ele, ".//div[13]/div/div/div[1]/label", d_['运动频率目标'])
        Web_PO.eleSetTextByX(ele, ".//div[14]/div[1]/div/div/input", d_['运动时长'][0])
        Web_PO.eleSetTextByX(ele, ".//div[14]/div[2]/div/div/input", d_['运动时长'][1])

        Web_PO.eleScrollViewByX(ele, ".//div[15]/div/div/div[1]/label", 2)
        Web_PO.eleRadioRightLabel(ele, ".//div[15]/div/div/div[1]/label", d_['摄盐量分级实际'])
        Web_PO.eleRadioRightLabel(ele, ".//div[16]/div/div/div[1]/label", d_['摄盐量分级目标'])
        Web_PO.eleRadioRightLabel(ele, ".//div[17]/div/div/div[1]/label", d_['随访饮食合理性评价'])

        Web_PO.eleScrollViewByX(ele, ".//div[18]/div/div/div[1]/label", 2)
        self.__eleRadioRightLabel(ele, ".//div[18]/div/div/div[1]/label", d_['心理调整评价结果'])
        self.__eleRadioRightLabel(ele, ".//div[19]/div/div/div[1]/label", d_['随访遵医行为'])
        Web_PO.eleSetTextByX(ele, ".//div[20]/div/div/div/input", d_['辅助检查'])
        self.__eleRadioRightLabel(ele, ".//div[21]/div/div/div[1]/label", d_['服药依从性'])
        Web_PO.eleRadioLeftLabel(ele, ".//div[22]/div[1]/div/div", d_['药物不良反应'][0])
        if d_['药物不良反应'][0] == '有':
            Web_PO.eleSetTextByX(ele, ".//div[22]/div[2]/div/div/input", d_['药物不良反应'][1])
        self.__eleRadioRightLabel(ele, ".//div[23]/div/div/div[1]/label", d_['随访评价结果'])
        self.__eleRadioRightLabel(ele, ".//div[24]/div/div/div[1]/label", d_['下一步管理措施'])

        Web_PO.eleScrollViewByX(ele, ".//div[25]/div/div/div/div/div/input", 2)
        Web_PO.eleClsReadonlyByX(ele, ".//div[25]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[25]/div/div/div/div/div/input", d_['用药情况药物名称1'])
        Web_PO.eleDropdown(ele, ".//div[26]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['用药情况用法用量1每日'])
        Web_PO.eleSetTextByX(ele, ".//div[26]/div/div[2]/div/div/input", d_['用药情况用法用量1每次'])

        Web_PO.eleClsReadonlyByX(ele, ".//div[27]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[27]/div/div/div/div/div/input", d_['用药情况药物名称2'])
        Web_PO.eleDropdown(ele, ".//div[28]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['用药情况用法用量2每日'])
        Web_PO.eleSetTextByX(ele, ".//div[28]/div/div[2]/div/div/input", d_['用药情况用法用量2每次'])

        Web_PO.eleClsReadonlyByX(ele, ".//div[29]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[29]/div/div/div/div/div/input", d_['用药情况药物名称3'])
        Web_PO.eleDropdown(ele, ".//div[30]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['用药情况用法用量3每日'])
        Web_PO.eleSetTextByX(ele, ".//div[30]/div/div[2]/div/div/input", d_['用药情况用法用量3每次'])

        Web_PO.eleScrollViewByX(ele, ".//div[31]/div/div/div/div/div/input", 2)
        Web_PO.eleClsReadonlyByX(ele, ".//div[31]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[31]/div/div/div/div/div/input", d_['用药调整意见药物名称1'])
        Web_PO.eleDropdown(ele, ".//div[32]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['用药调整意见用法用量1每日'])
        Web_PO.eleSetTextByX(ele, ".//div[32]/div/div[2]/div/div/input", d_['用药调整意见用法用量1每次'])

        Web_PO.eleClsReadonlyByX(ele, ".//div[33]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[33]/div/div/div/div/div/input", d_['用药调整意见药物名称2'])
        Web_PO.eleDropdown(ele, ".//div[34]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['用药调整意见用法用量2每日'])
        Web_PO.eleSetTextByX(ele, ".//div[34]/div/div[2]/div/div/input", d_['用药调整意见用法用量2每次'])

        Web_PO.eleClsReadonlyByX(ele, ".//div[35]/div/div/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[35]/div/div/div/div/div/input", d_['用药调整意见药物名称3'])
        Web_PO.eleDropdown(ele, ".//div[36]/div/div[1]/div/div/div/div/input", _dropdownByX,
                             d_['用药调整意见用法用量3每日'])
        Web_PO.eleSetTextByX(ele, ".//div[36]/div/div[2]/div/div/input", d_['用药调整意见用法用量3每次'])

        Web_PO.eleScrollViewByX(ele, ".//div[37]/div/div/div/input", 2)
        Web_PO.eleSetTextByX(ele, ".//div[37]/div/div/div/input", d_['转诊原因'])
        Web_PO.eleSetTextByX(ele, ".//div[38]/div/div/div/input", d_['转入医疗机构及科室'])
        Web_PO.eleSetTextByX(ele, ".//div[39]/div/div/div/input", d_['联系人'])
        Web_PO.eleSetTextByX(ele, ".//div[40]/div/div/div/input", d_['联系人电话'])

        Web_PO.eleScrollViewByX(ele, ".//div[41]/div/div/div", 2)
        Web_PO.eleRadioLeftLabel(ele, ".//div[41]/div/div/div", d_['结果'])
        Web_PO.eleSetTextByX(ele, ".//div[42]/div/div/div/input", d_['备注'])
        Web_PO.eleDropdownDate1(ele, ".//div[43]/div/div/div/input", d_['下次随访日期'])
        Web_PO.eleDropdown(ele, ".//div[44]/div/div/div/div/div/input", _dropdownByX, d_['随访医生'])
        Web_PO.eleSetTextByX(ele, ".//div[45]/div/div/div/input", d_['居民签字'])

        ele = Web_PO.getSuperEleByX("//span[text()='保存']", ".")
        Web_PO.eleClkByX(ele, ".", 2)

    # todo 糖尿病、慢性阻塞性肺病 公共操作
    def _phs_diabetes_copd_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        # 缩小页面，获取所有的字段
        Web_PO.zoom(50)
        # 获取字段列表
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        print(l_field)  # ['姓名', '身份证号', '出生日期', '电话', '居住地址', '性别', '随访医生', '空腹血糖', '随访方式', '随访日期', '随访评价结果', '下次随访日期', '数据源', '操作']
        Web_PO.zoom(100)

        # 获取值列表
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        print(l_value)
        s_class_warn = Web_PO.eleGetAttrValueByX(ele2, ".//td[3]/div/span", "class")
        # print(s_class_warn) # warn-tag warn-red
        l_value[2] = s_class_warn
        print(l_value)
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
        print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        if d_1 == {}:
            print("warning, 未匹配记录, 请检查字段是否存在！")
        else:
            print("ok, 匹配到", d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key


    # todo 2.4.1  基本公卫 - 慢性阻塞性肺病管理 - 慢阻肺病登记

    def phs_copd_register_query(self, d_):

        # 慢阻肺病登记 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '联系电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['档案状态', '既往疾病史']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def _phs_copd_register_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        # 缩小页面，获取所有的字段
        Web_PO.zoom(50)
        # 获取字段列表
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['姓名', '年龄', '性别', '身份证号', '家庭住址', '联系电话', '操作']
        Web_PO.zoom(100)

        # 获取值列表
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        print(l_group)  # [['女-1', '0', '女', '340203202407017263', '罗峰街道文化区社区居民委员会1', '1']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        # if d_1 == {}:
        #     print("warning, 未匹配记录, 请检查字段是否存在！")
        # else:
        #     print("ok, 匹配到", d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_copd_register_operation(self, d_):

        # 慢阻肺病登记 - 操作

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_copd_register_operation('专项登记', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '专项登记':
                ele = Web_PO.getSuperEleByX("//th[text()=' 慢性阻塞性肺患者管理卡 ']", "../..")
                for k, v in d_['data'].items():
                    if k in [' 居住地址 ']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/div/div/input",  v[0])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/div/div/input",  v[1])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div/div/input",  v[2])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/div/div/input",  v[3])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/div/div/input",  v[4])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//td[7]/div/div/div/input", v[5])
                    elif k in ['终止管理原因']:
                        if d_[' 是否终止管理 '] == "是":
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    elif k in ['终止管理日期']:
                        if d_[' 是否终止管理 '] == "是":
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[6]/div/div/div/input", v)
                    elif k in [' 是否终止管理 ']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['建卡医生']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input",  v)
                    elif k in [' 确诊日期 ']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v)
                    elif k in ['建卡时间']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
            else:
                print("error, 无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")




    # todo 2.4.2  基本公卫 - 慢性阻塞性肺病管理 - 慢阻肺病专项

    def phs_copd_project_query(self, d_):

        # 慢阻肺病专项 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '建卡医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否终止管理', '随访提醒分类', '档案状态', '随访评价结果']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期范围']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['上次随访日期', '下次随访日期', '建卡日期', '建档日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX, v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['档案管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))


    def phs_copd_project_operation(self, d_):

        # 慢阻肺病专项 - 操作

        try:
            if "index" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_diabetes_copd_operation('详情\n随访', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '详情' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑':
                    ele2 = Web_PO.getSuperEleByX("//span[text()='编辑']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                    ele = Web_PO.getSuperEleByX("//th[text()=' 慢性阻塞性肺患者管理卡 ']", "../..")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                    for k, v in d_.items():
                        if k in [' 居住地址 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/div/div/input", _dropdownByX, v[1])
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v[2])
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/div/div/input", _dropdownByX, v[3])
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/div/div/input", _dropdownByX, v[4])
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//td[7]/div/div/div/input", v[5])
                        elif k in ['终止管理原因']:
                            if d_[' 是否终止管理 '] == "是":
                                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                        elif k in ['终止管理日期']:
                            if d_[' 是否终止管理 '] == "是":
                                Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[6]/div/div/div/input", v)
                        elif k in [' 是否终止管理 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label", v)
                        elif k in ['建卡医生']:
                            Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input", _dropdownByX, v)
                        elif k in [' 确诊日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v)
                        elif k in ['建卡时间']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//td[2]/div/div/div/input", v)
                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['operate'] == '随访' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增']", "."), ".", 2)
                if d_['index']['operate2'] == '引入上次新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上次新增']", "."), ".", 2)
                # 新增、引入上次新增
                self.__phs(d_)

            else:
                print("error, 无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")




    # todo 2.4.3 基本公卫 - 慢性阻塞性肺病管理 - 慢阻肺病随访

    def phs_copd_visit_query(self, d_):

        # 慢阻肺病随访 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '随访医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['血氧饱和度']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['空腹血糖']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访方式', '是否终止管理', '数据源', '随访评价结果']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期范围']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input", _dropdownByX,
                                            v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",
                                            _dropdownByX, v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_copd_visit_export(self, varFile):

        # 慢阻肺病随访 - 导出

        ele = Web_PO.getSuperEleByX("//form", ".")
        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击导出

        if os.access(varFile + ".xlsx", os.F_OK):
            Web_PO.exportExistFile(varFile)
        else:
            Web_PO.exportFile(varFile)

    def phs_copd_visit_operation(self, d_):

        # 慢阻肺病随访 - 操作

        try:
            if "index" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_diabetes_tnbjob_operation('详情\n编辑\n删除', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            if d_['operate'] == '详情' and "operate2" in d_['index']:
                if d_['index']['operate2'] == '编辑':
                    ele3 = Web_PO.getSuperEleByX("//span[text()='编辑']", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
                    # 操作
                    # if l_[1] == '详情':
                    #     ele3 = Web_PO.getSuperEleByX("(//span[text()='" + l_[1] + "'])[position()=" + str(self.__phs_diabetes_operation('详情\n编辑\n删除', l_)) + "]", ".")
                    #     Web_PO.eleClkByX(ele3, ".", 2)
                    # elif l_[1] == '详情编辑':
                    ele = Web_PO.getSuperEleByX("//div[text()='高血压患者管理卡']", "..")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                    ele2 = Web_PO.getSuperEleByX("//span[text()='编辑']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)
                    for k, v in d_.items():
                        if k in [' 居住地址 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k, '../..'),
                                                    ".//div[1]/div[2]/div/div/div/div/div/input", _dropdownByX, v[0])
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k, '../..'),
                                                    ".//div[2]/div[1]/div/div/div/div/div/input", _dropdownByX, v[1])
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k, '../..'),
                                                    ".//div[2]/div[2]/div/div/div/div/div/input", _dropdownByX, v[2])
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k, '../..'),
                                                    ".//div[3]/div[1]/div/div/div/div/div/input", _dropdownByX, v[3])
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k, '../..'),
                                                    ".//div[3]/div[2]/div/div/div/div/div/input", _dropdownByX, v[4])
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k, '../..'), ".//div[4]/div[2]/div/div/div/input",
                                                      v[5])
                        elif k in [' 建卡医疗机构 ']:
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                        elif k in [' 终止管理原因 ']:
                            if d_[' 是否终止管理 '] == "是":
                                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                        elif k in [' 终止管理日期 ']:
                            if d_[' 是否终止管理 '] == "是":
                                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v)
                        elif k in [' 管理级别 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)
                        elif k in [' 是否终止管理 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                        elif k in [' 建卡医生 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                        elif k in [' 确诊日期 ', ' 建卡时间 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v)
                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['operate'] == '删除':
                Web_PO.clkByX("/html/body/div[4]/div/div/div[3]/button[1]")  # 二次确认

            else:
                print("error, 无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")




    # todo 2.5.2 基本公卫 - 儿童健康管理 - 儿童健康档案

    def phs_child_etfiles_query(self, d_):

        # 儿童健康档案 - 查询

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='展开'])[last()]", "."), ".", 2)
        ele = Web_PO.getSuperEleByX("//label[text()='姓名']", "../../../..")  # form
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '母亲姓名', '父亲姓名', '身份证号', '随访医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['上次完成 检查类型', '管理状态', '管理类别', '月龄', '新生儿异常情况', '喂养方式', '是否满6周岁', '身份证号 是否填写', '是否仅查询机构', '随访提醒分类']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期', '上次 随访日期', '下次 随访日期', '随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['出生地址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k, "../../.."), ".//div[11]/div/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k, "../../.."), ".//div[12]/div/div/div/input", v[2])
                elif k in ['儿童管理机构']:
                    self.__gljg(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def phs_child_etfiles_new(self, d_):

        # 儿童健康档案 - 新增

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='展开'])[last()]", "."), ".", 2)
        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()=' 新增 ']", ".."), ".", 2)

        ele = Web_PO.getSuperEleByX("//span[text()='新增儿童健康档案']", "../..")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '母亲姓名',  '母亲身份证号', '母亲联系电话', '父亲姓名', '父亲身份证号', '父亲联系电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['出生地址', '家庭住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", _dropdownByX, v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/input", _dropdownByX, v[2])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/input", _dropdownByX, v[3])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/div/input", _dropdownByX, v[4])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/input", v[5])
                elif k in ['性别', '母亲职业', '父亲职业']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['管理类别']:
                    self.__eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div/div[1]/label", v[0])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div/div[2]/input", v[1])
                elif k in ['同步出生地']:
                    if v == "是":
                        Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div/div/div/div[2]/form/div[2]/div/div/div/div/label/span[1]/span', 2)
            except:
                self.logger.error("新增 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, "//span[text()='确认并填表']", "."), ".")
        # 二次确认
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, "//span[text()='确认']", "../.."), ".")

        Web_PO.clkByX('/html/body/div[4]/div/div/div[3]/button')  # 自动创建健康档案信息未成功，请手动新增个人健康档案

    def phs_child_etfiles_edit(self, d_):

        # 儿童健康档案 - 儿童信息

        # Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='展开'])[last()]", "."), ".", 2)
        # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()=' 新增 ']", ".."), ".", 2)

        ele = Web_PO.getSuperEleByX("//span[text()='新增儿童健康档案']", "../..")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '母亲姓名',  '母亲身份证号', '母亲联系电话', '父亲姓名', '父亲身份证号', '父亲联系电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['出生地址', '家庭住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", _dropdownByX, v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/input", _dropdownByX, v[2])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/input", _dropdownByX, v[3])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/div/input", _dropdownByX, v[4])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/input", v[5])
                elif k in ['性别', '母亲职业', '父亲职业']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['管理类别']:
                    self.__eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div/div[1]/label", v[0])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div/div[2]/input", v[1])
                elif k in ['同步出生地']:
                    if v == "是":
                        Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div/div/div/div[2]/form/div[2]/div/div/div/div/label/span[1]/span', 2)
            except:
                self.logger.error("新增 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, "//span[text()='确认']", "."), ".")

    def _phs_child_etfiles_operation(self, varOperation, d_option):

        # 遍历高血压专项、高血压随访的列表页
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['姓名', '提醒', '性别', '出生日期时间', '年龄', '上次完成检查类型', '上次随访日期', '下次随访日期', '母亲姓名', '母亲联系电话', '父亲姓名', '父亲联系电话', '管理状态', '管理类别', '登记机构', '身份证号', '家庭住址', '操作']
        Web_PO.zoom(100)

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)
        s_class_warn = Web_PO.eleGetAttrValueByX(ele2, ".//td[2]/div/div", "style")
        # /html/body/div[1]/div/div[3]/section/div/main/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/div/div
        # print(s_class_warn)  # background-color: red;
        s_class_warn = s_class_warn.split("background-color: ")[1].split(";")[0]
        l_value[1] = s_class_warn
        # print(l_value)

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
            if "提醒" in l_field:
                for i in l_group:
                    i.pop(2)
                    i.pop(2)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
            if "提醒" in l_field:
                for i in l_group:
                    i.pop(2)
                    i.pop(2)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_child_etfiles_operation(self, d_):

        # 儿童健康档案 - 操作

        # try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_child_etfiles_operation('健康检查\n儿童信息', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)

            elif d_['operate'] == '健康检查' :
                if d_['title'] == '新生儿家庭访视记录表':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[1]/div', 2)
                    ele = Web_PO.getSuperEleByX("//td[text()='新生儿家庭访视记录表']", "../..")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                    for k, v in d_['新生儿'].items():
                        if k in ['本次访视时间', '下次访视时间']:
                            Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."), ".//div[1]/input", v)
                        elif k in ['出生孕周']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//div[1]/div/div/input", v[0])
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//div[2]/div/div/input", v[1])
                        elif k in ['母亲妊娠期']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//td[5]/div/div/div/input", i['其他'])
                        elif k in ['出生情况']:
                            Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[5]/div/div/div/input", i['其他'])
                        elif k in ['助产机构名称']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//input", v)
                        elif k in ['新生儿出生时', '体温']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div/input", v)
                        elif k in ['目前体重', '吃奶量', '心率', '下次随访地点']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/input", v)
                        elif k in ['出生身长', '吃奶次数', '大便次数', '呼吸频率']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[6]/div/div/div/input", v)
                        elif k in ['新生儿疾病筛查 ', '指导 ']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", i['其他'])
                        elif k in ['新生儿窒息', '新生儿听力检查', '喂养方式', '呕吐']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                        elif k in ['大便']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label", v)
                        elif k in ['Apgar评分']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div/label", v[0])
                            if v[0] == '有':
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div[2]/span[1]/div/input", v[1][0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div[2]/span[2]/div/input", v[1][1])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div[2]/span[3]/div/input", v[1][2])
                        elif k in [' 是否有畸形 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v[0])
                            # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/form/table/tbody/tr[8]/td[2]/div/div/div/label[2]
                            if v[0] == '有':
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v[1]['畸形详细'])
                        elif k in ['面色 ']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//td[2]", 2)
                            if isinstance(v, dict):
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", '其他')
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", v['其他'])
                            else:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                        elif k in ['黄疸部位']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label", v)
                        elif k in ['前囟']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[1]/input", v[0])
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[2]/input", v[1])
                            if isinstance(v[2], dict):
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[3]/label", '其他')
                                Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[3]/div/div/div/input", v[2]['其他'])
                            else:
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[3]/label", v[2])
                        elif k in [' 眼睛 ', ' 耳外观 ', ' 鼻 ', ' 口腔 ', ' 心肺听诊 ', ' 腹部触诊 ', ' 外生殖器 ']:
                            if isinstance(v, dict):
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", '异常')
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", v['异常'])
                            else:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                        elif k in [' 四肢活动度 ', ' 颈部包块 ', ' 肛门 ', ' 胸部 ', ' 脊柱 ', '皮肤 ', '脐带 ']:
                            if isinstance(v, dict):
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label", list(v.keys())[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/input", v[list(v.keys())[0]])
                            else:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label", v)
                        elif k in ['转诊']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div/label", v[0])
                            if v[0] == '有':
                                Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/input", v[1]['原因'])
                                Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[6]/div/div/div/input", v[1]['机构'])
                                Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[8]/div/div/div/input", v[1]['科室'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[2]/div/div/div/input", v[1]['联系人'])
                                Web_PO.eleSetTextByX(ele3, ".//td[4]/div/div/div/input", v[1]['联系方式'])
                                Web_PO.eleRadioRightLabel(ele3, ".//td[6]/div/div/div/label", v[1]['结果'])
                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                        elif k in ['家长签名']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)

                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                elif d_['title'] == '1-8月龄儿童健康检查记录表':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[2]/div', 2)
                    ele = Web_PO.getSuperEleByX("//td[text()='1-8月龄儿童健康检查记录表']", "../..")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                    for k1, v1 in d_['data'].items():
                        if '满月' == k1:
                            varTd = 2
                        elif '3月龄' == k1:
                            varTd = 3
                        elif '6月龄' == k1:
                            varTd = 4
                        elif '8月龄' == k1:
                            varTd = 5

                        for k, v in v1.items():
                            if k in ['随访日期', '下次随访日期']:
                                Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in ['本次服务类别']:
                                for i in v:
                                    if isinstance(i, dict):
                                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                        Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", i['失访原因'])
                                    else:
                                        Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/label", i)
                            elif k in ['体重(kg)', '身长(cm)']:
                                Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3, v[0], 1)
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                            elif k in ['头围(cm)', '户外活动(小时/日)', '服用维生素D(IU/日)']:
                                Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in [' 血红蛋白值 ']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in ['面色']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd+1) + "]/div/div/div/label", v)
                            elif k in ['皮肤', '颈部包块', '眼睛', '耳', '听力', '胸部', '腹部', '脐部', '四肢', '可疑佝偻病', '体征', '肛门/外生殖器']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/label", v)
                            elif k in ['前囟']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[1]/label", v[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[2]/input", v[1])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[3]/input", v[2])
                            elif k in ['口腔']:
                                if varTd <= 3:
                                    Web_PO.eleRadioRightLabel(self._eleSpan(ele, k,"../.."), ".//td[" + str(varTd) + "]/div/div/div/label", v)
                                else:
                                    Web_PO.eleSetTextByX(self._eleSpan(ele, k,"../.."), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in ['两次随访间']:
                                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                                Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label", ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                            elif k in ['指导', '中医药健康']:
                                Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                                for i in v:
                                    if isinstance(i, dict):
                                        if '其他' in i:
                                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/div/input", i['其他'])
                            elif k in ['发育评估', '管理服务 ']:
                                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                                for i in v:
                                    if isinstance(i, dict):
                                        if '其他' in i:
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[2]/div/input", i['其他'])
                            elif k in ['转诊']:
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                                if v[0] == '有':
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['原因'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['机构及科室'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['联系人'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['联系方式'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                    Web_PO.eleRadioRightLabel(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/label", v[1]['结果'])
                            elif k in ['随访医生签名']:
                                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX, v)
                            elif k in ['家长签名']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)

                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                elif d_['title'] == '12-30月龄儿童健康检查记录表':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[3]/div', 2)
                    ele = Web_PO.getSuperEleByX("//td[text()='12-30月龄儿童健康检查记录表']", "../..")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                    for k1, v1 in d_['data'].items():
                        if '12月龄' == k1:
                            varTd = 2
                        elif '18月龄' == k1:
                            varTd = 3
                        elif '24月龄' == k1:
                            varTd = 4
                        elif '30月龄' == k1:
                            varTd = 5

                        for k, v in v1.items():
                            if k in ['随访日期', '下次随访日期']:
                                Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in ['本次服务类别']:
                                for i in v:
                                    if isinstance(i, dict):
                                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                        Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", i['失访原因'])
                                    else:
                                        Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/label", i)
                            elif k in ['体重(kg)', '身长(cm)']:
                                Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3, v[0], 1)
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                            elif k in ['头围(cm)', '户外活动(小时/日)', '服用维生素D(IU/日)']:
                                Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in [' 血红蛋白值 ']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in ['面色']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd+1) + "]/div/div/div/label", v)
                            elif k in ['皮肤', '颈部包块', '眼睛', '耳', '听力', '胸部', '腹部', '脐部', '四肢', '步态', '可疑佝偻病', '体征', '肛门/外生殖器']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/label", v)
                            elif k in ['出牙/龋齿数']:
                                    Web_PO.eleSetTextByX(self._eleSpan(ele, k,"../.."), ".//td[" + str(varTd) + "]/div/div/div[1]/input", v[0])
                                    Web_PO.eleSetTextByX(self._eleSpan(ele, k,"../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/input", v[1])
                            elif k in ['前囟']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[1]/label", v[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[2]/input", v[1])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[3]/input", v[2])
                            elif k in ['两次随访间']:
                                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                                Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label", ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                            elif k in ['指导']:
                                Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                                for i in v:
                                    if isinstance(i, dict):
                                        if '其他' in i:
                                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/div/input", i['其他'])
                            elif k in ['发育评估', '管理服务 ']:
                                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                                for i in v:
                                    if isinstance(i, dict):
                                        if '其他' in i:
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[2]/div/input", i['其他'])
                            elif k in ['转诊']:
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                                if v[0] == '有':
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['原因'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['机构及科室'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['联系人'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['联系方式'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                    Web_PO.eleRadioRightLabel(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/label", v[1]['结果'])
                            elif k in ['随访医生签名']:
                                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX, v)
                            elif k in ['家长签名']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)

                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                elif d_['title'] == '3～6岁儿童健康检查记录表':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[4]/div', 2)
                    ele = Web_PO.getSuperEleByX("//td[text()='3-6岁儿童健康检查记录表']", "../..")
                    sleep(3)
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                    for k1, v1 in d_['data'].items():
                        if '3岁' == k1:
                            varTd = 2
                        elif '4岁' == k1:
                            varTd = 3
                        elif '5岁' == k1:
                            varTd = 4
                        elif '6岁' == k1:
                            varTd = 5

                        for k, v in v1.items():
                            if k in ['随访日期', '下次随访日期']:
                                Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in ['本次服务类别']:
                                for i in v:
                                    if isinstance(i, dict):
                                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                        Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", i['失访原因'])
                                    else:
                                        Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/label", i)
                            elif k in ['体重(kg)', '身长(cm)']:
                                Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3, v[0], 1)
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                            elif k in ['体重/身高']:
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/label", v)
                            elif k in [' 血红蛋白值 ']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                            elif k in ['耳', '听力', '胸部', '腹部']:
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/label", v)
                            elif k in ['体格发育评估']:
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k,"../.."), ".//td[" + str(varTd) + "]/div/div/div/label", v)
                            elif k in ['出牙/龋齿数']:
                                    Web_PO.eleSetTextByX(self._eleSpan(ele, k,"../.."), ".//td[" + str(varTd) + "]/div/div/div[1]/input", v[0])
                                    # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/div/form/table/tbody/tr[13]/td[3]/div/div/div[1]/input
                                    # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/div/form/table/tbody/tr[10]/td[4]/div/div/div[1]/input
                                    Web_PO.eleSetTextByX(self._eleSpan(ele, k,"../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/input", v[1])
                            elif k in ['视力']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd+1) + "]/div/div/div[1]/input", v[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd+1) + "]/div/div/div[2]/input", v[1])
                            elif k in ['两次随访间']:
                                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                                Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label", ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                            elif k in ['指导']:
                                Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                                for i in v:
                                    if isinstance(i, dict):
                                        if '其他' in i:
                                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div[2]/div/input", i['其他'])
                            elif k in ['发育评估', '管理服务 ']:
                                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                                for i in v:
                                    if isinstance(i, dict):
                                        if '其他' in i:
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[2]/div/input", i['其他'])
                            elif k in ['转诊']:
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                                if v[0] == '有':
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['原因'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['机构及科室'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['联系人'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/input", v[1]['联系方式'])
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                    Web_PO.eleRadioRightLabel(ele3, ".//td[" + str(varTd*2-2) + "]/div/div/div/label", v[1]['结果'])
                            elif k in ['随访医生签名']:
                                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX, v)
                            elif k in ['家长签名']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)

                    ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

                elif d_['title'] == '结案':
                    ele2 = Web_PO.getSuperEleByX("//span[text()='结案']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)
                    ele3 = Web_PO.getSuperEleByX(".//span[text()='结案原因：']")
                    Web_PO.eleRadioRightLabel(ele3, ".//div/label", d_['data']['结案原因'])
                    ele2 = Web_PO.getSuperEleByX("//span[text()='确定']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['operate'] == '儿童信息':
                if d_['title'] == '编辑':
                    self.phs_child_etfiles_edit(d_['data'])
                elif d_['title'] == '删除':
                    ele2 = Web_PO.getSuperEleByX("//span[text()='删除档案']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)
                    ele2 = Web_PO.getSuperEleByX("//span[text()='确认']", "..")
                    Web_PO.eleClkByX(ele2, ".", 2)



    # todo 2.5.3 基本公卫 - 儿童健康管理 - 中医体质辨识列表

    def phs_child_tcm_query(self, d_):

        # 中医体质辨识列表 - 查询

        ele = Web_PO.getSuperEleByX("//label[text()='儿童管理机构']", "../../../..")  # form
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '随访医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '检查类型', '管理状态', '管理类型']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                elif k in ['出生日期', '随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['家庭地址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input", _dropdownByX, v[1])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['儿童管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def _phs_child_tcm_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['姓名', '提醒', '性别', '出生日期时间', '年龄', '上次完成检查类型', '上次随访日期', '下次随访日期', '母亲姓名', '母亲联系电话', '父亲姓名', '父亲联系电话', '管理状态', '管理类别', '登记机构', '身份证号', '家庭住址', '操作']
        Web_PO.zoom(100)

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)

        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_child_tcm_operation(self, d_):

        # 中医体质辨识列表 - 操作

        if "data" not in d_:
            ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                self._phs_child_tcm_operation('编辑', d_['option'])) + "]", ".")
            Web_PO.eleClkByX(ele3, ".", 2)

        elif d_['operate'] == '编辑':
            if d_['title'] == '新生儿家庭访视记录表':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[1]/div', 2)
                ele = Web_PO.getSuperEleByX("//td[text()='新生儿家庭访视记录表']", "../..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                for k, v in d_['data']['新生儿'].items():
                    if k in ['本次访视时间', '下次访视时间']:
                        Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."), ".//div[1]/input", v)
                    elif k in ['出生孕周']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//div[1]/div/div/input", v[0])
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//div[2]/div/div/input", v[1])
                    elif k in ['母亲妊娠期']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/label", v)
                        for i in v:
                            if isinstance(i, dict):
                                if '其他' in i:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//td[5]/div/div/div/input",
                                                         i['其他'])
                    elif k in ['出生情况']:
                        Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/label", v)
                        for i in v:
                            if isinstance(i, dict):
                                if '其他' in i:
                                    Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[5]/div/div/div/input",
                                                         i['其他'])
                    elif k in ['助产机构名称']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//input", v)
                    elif k in ['新生儿出生时', '体温']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div/input", v)
                    elif k in ['目前体重', '吃奶量', '心率', '下次随访地点']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/input", v)
                    elif k in ['出生身长', '吃奶次数', '大便次数', '呼吸频率']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[6]/div/div/div/input", v)
                    elif k in ['新生儿疾病筛查 ', '指导 ']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                        for i in v:
                            if isinstance(i, dict):
                                if '其他' in i:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", i['其他'])
                    elif k in ['新生儿窒息', '新生儿听力检查', '喂养方式', '呕吐']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['大便']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['Apgar评分']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div/label", v[0])
                        if v[0] == '有':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div[2]/span[1]/div/input",
                                                 v[1][0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div[2]/span[2]/div/input",
                                                 v[1][1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div[2]/span[3]/div/input",
                                                 v[1][2])
                    elif k in [' 是否有畸形 ']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v[0])
                        # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/form/table/tbody/tr[8]/td[2]/div/div/div/label[2]
                        if v[0] == '有':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v[1]['畸形详细'])
                    elif k in ['面色 ']:
                        Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//td[2]", 2)
                        if isinstance(v, dict):
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", '其他')
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", v['其他'])
                        else:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['黄疸部位']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label", v)
                    elif k in ['前囟']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[1]/input", v[0])
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[2]/input", v[1])
                        if isinstance(v[2], dict):
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[3]/label",
                                                      '其他')
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[3]/div/div/div/input",
                                                 v[2]['其他'])
                        else:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[3]/label",
                                                      v[2])
                    elif k in [' 眼睛 ', ' 耳外观 ', ' 鼻 ', ' 口腔 ', ' 心肺听诊 ', ' 腹部触诊 ', ' 外生殖器 ']:
                        if isinstance(v, dict):
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", '异常')
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", v['异常'])
                        else:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in [' 四肢活动度 ', ' 颈部包块 ', ' 肛门 ', ' 胸部 ', ' 脊柱 ', '皮肤 ', '脐带 ']:
                        if isinstance(v, dict):
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label",
                                                      list(v.keys())[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/input",
                                                 v[list(v.keys())[0]])
                        else:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label", v)
                    elif k in ['转诊']:
                        Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div/label", v[0])
                        if v[0] == '有':
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/input",
                                                 v[1]['原因'])
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[6]/div/div/div/input",
                                                 v[1]['机构'])
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[8]/div/div/div/input",
                                                 v[1]['科室'])
                            ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                            Web_PO.eleSetTextByX(ele3, ".//td[2]/div/div/div/input", v[1]['联系人'])
                            Web_PO.eleSetTextByX(ele3, ".//td[4]/div/div/div/input", v[1]['联系方式'])
                            Web_PO.eleRadioRightLabel(ele3, ".//td[6]/div/div/div/label", v[1]['结果'])
                    elif k in ['随访医生签名']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                    elif k in ['家长签名']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)

                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['title'] == '1-8月龄儿童健康检查记录表':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[2]/div', 2)
                ele = Web_PO.getSuperEleByX("//td[text()='1-8月龄儿童健康检查记录表']", "../..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                for k1, v1 in d_['data'].items():
                    if '满月' == k1:
                        varTd = 2
                    elif '3月龄' == k1:
                        varTd = 3
                    elif '6月龄' == k1:
                        varTd = 4
                    elif '8月龄' == k1:
                        varTd = 5

                    for k, v in v1.items():
                        if k in ['随访日期', '下次随访日期']:
                            Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."),
                                                        ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['本次服务类别']:
                            for i in v:
                                if isinstance(i, dict):
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                         i['失访原因'])
                                else:
                                    Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                              ".//td[" + str(varTd) + "]/div/div/div/label", i)
                        elif k in ['体重(kg)', '身长(cm)']:
                            Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."),
                                                               ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3,
                                                               v[0], 1)
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                        elif k in ['头围(cm)', '户外活动(小时/日)', '服用维生素D(IU/日)']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in [' 血红蛋白值 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['面色']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd + 1) + "]/div/div/div/label", v)
                        elif k in ['皮肤', '颈部包块', '眼睛', '耳', '听力', '胸部', '腹部', '脐部', '四肢', '可疑佝偻病', '体征', '肛门/外生殖器']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v)
                        elif k in ['前囟']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div[1]/label", v[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[2]/input",
                                                 v[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[3]/input",
                                                 v[2])
                        elif k in ['口腔']:
                            if varTd <= 3:
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                          ".//td[" + str(varTd) + "]/div/div/div/label", v)
                            else:
                                Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                     ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['两次随访间']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k),
                                                    ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                            Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label",
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                        elif k in ['指导', '中医药健康']:
                            Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['发育评估', '管理服务 ']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['转诊']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                            if v[0] == '有':
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['原因'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['机构及科室'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系人'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系方式'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                Web_PO.eleRadioRightLabel(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/label",
                                                          v[1]['结果'])
                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX, v)
                        elif k in ['家长签名']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)

                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['title'] == '12-30月龄儿童健康检查记录表':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[3]/div', 2)
                ele = Web_PO.getSuperEleByX("//td[text()='12-30月龄儿童健康检查记录表']", "../..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                for k1, v1 in d_['data'].items():
                    if '12月龄' == k1:
                        varTd = 2
                    elif '18月龄' == k1:
                        varTd = 3
                    elif '24月龄' == k1:
                        varTd = 4
                    elif '30月龄' == k1:
                        varTd = 5

                    for k, v in v1.items():
                        if k in ['随访日期', '下次随访日期']:
                            Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."),
                                                        ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['本次服务类别']:
                            for i in v:
                                if isinstance(i, dict):
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                         i['失访原因'])
                                else:
                                    Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                              ".//td[" + str(varTd) + "]/div/div/div/label", i)
                        elif k in ['体重(kg)', '身长(cm)']:
                            Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."),
                                                               ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3,
                                                               v[0], 1)
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                        elif k in ['头围(cm)', '户外活动(小时/日)', '服用维生素D(IU/日)']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in [' 血红蛋白值 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['面色']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd + 1) + "]/div/div/div/label", v)
                        elif k in ['皮肤', '颈部包块', '眼睛', '耳', '听力', '胸部', '腹部', '脐部', '四肢', '步态', '可疑佝偻病', '体征',
                                   '肛门/外生殖器']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v)
                        elif k in ['出牙/龋齿数']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div[1]/input", v[0])
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div[2]/input", v[1])
                        elif k in ['前囟']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div[1]/label", v[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[2]/input",
                                                 v[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div[3]/input",
                                                 v[2])
                        elif k in ['两次随访间']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k),
                                                    ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                            Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label",
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                        elif k in ['指导']:
                            Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['发育评估', '管理服务 ']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['转诊']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                            if v[0] == '有':
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['原因'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['机构及科室'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系人'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系方式'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                Web_PO.eleRadioRightLabel(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/label",
                                                          v[1]['结果'])
                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX, v)
                        elif k in ['家长签名']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)

                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

            elif d_['title'] == '3～6岁儿童健康检查记录表':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[4]/div', 2)
                ele = Web_PO.getSuperEleByX("//td[text()='3-6岁儿童健康检查记录表']", "../..")
                sleep(3)
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                for k1, v1 in d_['data'].items():
                    if '3岁' == k1:
                        varTd = 2
                    elif '4岁' == k1:
                        varTd = 3
                    elif '5岁' == k1:
                        varTd = 4
                    elif '6岁' == k1:
                        varTd = 5

                    for k, v in v1.items():
                        if k in ['随访日期', '下次随访日期']:
                            Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."),
                                                        ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['本次服务类别']:
                            for i in v:
                                if isinstance(i, dict):
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                    Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                         i['失访原因'])
                                else:
                                    Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                              ".//td[" + str(varTd) + "]/div/div/div/label", i)
                        elif k in ['体重(kg)', '身长(cm)']:
                            Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."),
                                                               ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3,
                                                               v[0], 1)
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                        elif k in ['体重/身高']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div[2]/label", v)
                        elif k in [' 血红蛋白值 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['耳', '听力', '胸部', '腹部']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v)
                        elif k in ['体格发育评估']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v)
                        elif k in ['出牙/龋齿数']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div[1]/input", v[0])
                            # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/div/form/table/tbody/tr[13]/td[3]/div/div/div[1]/input
                            # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/div/form/table/tbody/tr[10]/td[4]/div/div/div[1]/input
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div[2]/input", v[1])
                        elif k in ['视力']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[" + str(varTd + 1) + "]/div/div/div[1]/input", v[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[" + str(varTd + 1) + "]/div/div/div[2]/input", v[1])
                        elif k in ['两次随访间']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k),
                                                    ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                            Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label",
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                        elif k in ['指导']:
                            Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['发育评估', '管理服务 ']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['转诊']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                            if v[0] == '有':
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['原因'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['机构及科室'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系人'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系方式'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                Web_PO.eleRadioRightLabel(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/label",
                                                          v[1]['结果'])
                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX, v)
                        elif k in ['家长签名']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input", v)

                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['title'] == '结案':
                ele2 = Web_PO.getSuperEleByX("//span[text()='结案']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)
                ele3 = Web_PO.getSuperEleByX(".//span[text()='结案原因：']")
                Web_PO.eleRadioRightLabel(ele3, ".//div/label", d_['data']['结案原因'])
                ele2 = Web_PO.getSuperEleByX("//span[text()='确定']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)



    # todo 2.5.5 基本公卫 - 儿童健康管理 - 儿童检查记录

    def phs_child_etjob_query(self, d_):

        # 儿童检查记录 - 查询

        ele = Web_PO.getSuperEleByX("//label[text()='儿童管理机构']", "../../../..")  # form
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['随访医生']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k,"../.."), ".//input", v)
                elif k in ['是否仅查询机构', '检查类型']:
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//input", _dropdownByX, v)
                elif k in ['登记日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['随访日期', '下次随访日期', '出生日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k), ".//div[2]/input", v[1])
                elif k in ['血红蛋白']:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div[1]/input", v[0])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div[2]/input", v[1])
                elif k in ['儿童管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        Web_PO.eleClkByX(ele, ".//button[2]", 2)  # 点击查询
        self.logger.info("查询 => " + str(d_))

    def _phs_child_etjob_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '提醒', '性别', '出生日期时间', '年龄', '上次完成检查类型', '上次随访日期', '下次随访日期', '母亲姓名', '母亲联系电话', '父亲姓名', '父亲联系电话', '管理状态', '管理类别', '登记机构', '身份证号', '家庭住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_child_etjob_operation(self, d_):

        # 儿童检查记录 - 操作

        if "data" not in d_:
            ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                self._phs_child_etjob_operation('编辑\n删除', d_['option'])) + "]", ".")
            Web_PO.eleClkByX(ele3, ".", 2)
            if d_['operate'] == '删除':
                ele2 = Web_PO.getSuperEleByX("//span[text()='确定']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)

        elif d_['operate'] == '编辑':
            if d_['title'] == '新生儿家庭访视记录表':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[1]/div', 2)
                ele = Web_PO.getSuperEleByX("//td[text()='新生儿家庭访视记录表']", "../..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                for k, v in d_['data']['新生儿'].items():
                    if k in ['本次访视时间', '下次访视时间']:
                        Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."), ".//div[1]/input", v)
                    elif k in ['出生孕周']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//div[1]/div/div/input", v[0])
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//div[2]/div/div/input", v[1])
                    elif k in ['母亲妊娠期']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/label",v)
                        for i in v:
                            if isinstance(i, dict):
                                if '其他' in i:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                         ".//td[5]/div/div/div/input",
                                                         i['其他'])
                    elif k in ['出生情况']:
                        Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/label",
                                                      v)
                        for i in v:
                            if isinstance(i, dict):
                                if '其他' in i:
                                    Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                         ".//td[5]/div/div/div/input",
                                                         i['其他'])
                    elif k in ['助产机构名称']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//input", v)
                    elif k in ['新生儿出生时', '体温']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div/input", v)
                    elif k in ['目前体重', '吃奶量', '心率', '下次随访地点']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/input", v)
                    elif k in ['出生身长', '吃奶次数', '大便次数', '呼吸频率']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[6]/div/div/div/input", v)
                    elif k in ['新生儿疾病筛查 ', '指导 ']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                        for i in v:
                            if isinstance(i, dict):
                                if '其他' in i:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", i['其他'])
                    elif k in ['新生儿窒息', '新生儿听力检查', '喂养方式', '呕吐']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['大便']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/label", v)
                    elif k in ['Apgar评分']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/div/label", v[0])
                        if v[0] == '有':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[4]/div/div/div/div[2]/span[1]/div/input",
                                                 v[1][0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[4]/div/div/div/div[2]/span[2]/div/input",
                                                 v[1][1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[4]/div/div/div/div[2]/span[3]/div/input",
                                                 v[1][2])
                    elif k in [' 是否有畸形 ']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v[0])
                        # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/form/table/tbody/tr[8]/td[2]/div/div/div/label[2]
                        if v[0] == '有':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v[1]['畸形详细'])
                    elif k in ['面色 ']:
                        Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//td[2]", 2)
                        if isinstance(v, dict):
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", '其他')
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", v['其他'])
                        else:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['黄疸部位']:
                        Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label", v)
                    elif k in ['前囟']:
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[1]/input", v[0])
                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div[2]/input", v[1])
                        if isinstance(v[2], dict):
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[2]/div/div/div[3]/label",
                                                      '其他')
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[3]/div/div/div/input",
                                                 v[2]['其他'])
                        else:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[2]/div/div/div[3]/label",
                                                      v[2])
                    elif k in [' 眼睛 ', ' 耳外观 ', ' 鼻 ', ' 口腔 ', ' 心肺听诊 ', ' 腹部触诊 ', ' 外生殖器 ']:
                        if isinstance(v, dict):
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", '异常')
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[3]/div/div/div/input", v['异常'])
                        else:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in [' 四肢活动度 ', ' 颈部包块 ', ' 肛门 ', ' 胸部 ', ' 脊柱 ', '皮肤 ', '脐带 ']:
                        if isinstance(v, dict):
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label",
                                                      list(v.keys())[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[6]/div/div/div/input",
                                                 v[list(v.keys())[0]])
                        else:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//td[5]/div/div/div/label", v)
                    elif k in ['转诊']:
                        Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."), ".//td[2]/div/div/div/label",
                                                  v[0])
                        if v[0] == '有':
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[4]/div/div/div/input",
                                                 v[1]['原因'])
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[6]/div/div/div/input",
                                                 v[1]['机构'])
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."), ".//td[8]/div/div/div/input",
                                                 v[1]['科室'])
                            ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                            Web_PO.eleSetTextByX(ele3, ".//td[2]/div/div/div/input", v[1]['联系人'])
                            Web_PO.eleSetTextByX(ele3, ".//td[4]/div/div/div/input", v[1]['联系方式'])
                            Web_PO.eleRadioRightLabel(ele3, ".//td[6]/div/div/div/label", v[1]['结果'])
                    elif k in ['随访医生签名']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                    elif k in ['家长签名']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)

                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['title'] == '1-8月龄儿童健康检查记录表':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[2]/div', 2)
                ele = Web_PO.getSuperEleByX("//td[text()='1-8月龄儿童健康检查记录表']", "../..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                for k1, v1 in d_['data'].items():
                    if '满月' == k1:
                        varTd = 2
                    elif '3月龄' == k1:
                        varTd = 3
                    elif '6月龄' == k1:
                        varTd = 4
                    elif '8月龄' == k1:
                        varTd = 5

                    for k, v in v1.items():
                        if k in ['随访日期', '下次随访日期']:
                            Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."),
                                                        ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['本次服务类别']:
                            for i in v:
                                if isinstance(i, dict):
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                    Web_PO.eleSetTextByX(ele3,
                                                         ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                         i['失访原因'])
                                else:
                                    Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                              ".//td[" + str(varTd) + "]/div/div/div/label", i)
                        elif k in ['体重(kg)', '身长(cm)']:
                            Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."),
                                                               ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3,
                                                               v[0], 1)
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                        elif k in ['头围(cm)', '户外活动(小时/日)', '服用维生素D(IU/日)']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in [' 血红蛋白值 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input",
                                                 v)
                        elif k in ['面色']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd + 1) + "]/div/div/div/label", v)
                        elif k in ['皮肤', '颈部包块', '眼睛', '耳', '听力', '胸部', '腹部', '脐部', '四肢', '可疑佝偻病', '体征', '肛门/外生殖器']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v)
                        elif k in ['前囟']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div[1]/label", v[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[" + str(varTd) + "]/div/div/div[2]/input",
                                                 v[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[" + str(varTd) + "]/div/div/div[3]/input",
                                                 v[2])
                        elif k in ['口腔']:
                            if varTd <= 3:
                                Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                          ".//td[" + str(varTd) + "]/div/div/div/label", v)
                            else:
                                Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                     ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['两次随访间']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k),
                                                    ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                            Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label",
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                        elif k in ['指导', '中医药健康']:
                            Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['发育评估', '管理服务 ']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['转诊']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                            if v[0] == '有':
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['原因'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['机构及科室'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系人'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系方式'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                Web_PO.eleRadioRightLabel(ele3,
                                                          ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/label",
                                                          v[1]['结果'])
                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX,
                                               v)
                        elif k in ['家长签名']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input",
                                                 v)

                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['title'] == '12-30月龄儿童健康检查记录表':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[3]/div', 2)
                ele = Web_PO.getSuperEleByX("//td[text()='12-30月龄儿童健康检查记录表']", "../..")
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                for k1, v1 in d_['data'].items():
                    if '12月龄' == k1:
                        varTd = 2
                    elif '18月龄' == k1:
                        varTd = 3
                    elif '24月龄' == k1:
                        varTd = 4
                    elif '30月龄' == k1:
                        varTd = 5

                    for k, v in v1.items():
                        if k in ['随访日期', '下次随访日期']:
                            Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."),
                                                        ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['本次服务类别']:
                            for i in v:
                                if isinstance(i, dict):
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                    Web_PO.eleSetTextByX(ele3,
                                                         ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                         i['失访原因'])
                                else:
                                    Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                              ".//td[" + str(varTd) + "]/div/div/div/label", i)
                        elif k in ['体重(kg)', '身长(cm)']:
                            Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."),
                                                               ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3,
                                                               v[0], 1)
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                        elif k in ['头围(cm)', '户外活动(小时/日)', '服用维生素D(IU/日)']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in [' 血红蛋白值 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input",
                                                 v)
                        elif k in ['面色']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd + 1) + "]/div/div/div/label", v)
                        elif k in ['皮肤', '颈部包块', '眼睛', '耳', '听力', '胸部', '腹部', '脐部', '四肢', '步态', '可疑佝偻病', '体征',
                                   '肛门/外生殖器']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v)
                        elif k in ['出牙/龋齿数']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div[1]/input", v[0])
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div[2]/input", v[1])
                        elif k in ['前囟']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div[1]/label", v[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[" + str(varTd) + "]/div/div/div[2]/input",
                                                 v[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[" + str(varTd) + "]/div/div/div[3]/input",
                                                 v[2])
                        elif k in ['两次随访间']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k),
                                                    ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                            Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label",
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                        elif k in ['指导']:
                            Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['发育评估', '管理服务 ']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['转诊']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                            if v[0] == '有':
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['原因'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['机构及科室'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系人'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系方式'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                Web_PO.eleRadioRightLabel(ele3,
                                                          ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/label",
                                                          v[1]['结果'])
                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX,
                                               v)
                        elif k in ['家长签名']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input",
                                                 v)

                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['title'] == '3～6岁儿童健康检查记录表':
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/main/div[2]/ul/li[4]/div', 2)
                ele = Web_PO.getSuperEleByX("//td[text()='3-6岁儿童健康检查记录表']", "../..")
                sleep(3)
                _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

                for k1, v1 in d_['data'].items():
                    if '3岁' == k1:
                        varTd = 2
                    elif '4岁' == k1:
                        varTd = 3
                    elif '5岁' == k1:
                        varTd = 4
                    elif '6岁' == k1:
                        varTd = 5

                    for k, v in v1.items():
                        if k in ['随访日期', '下次随访日期']:
                            Web_PO.eleDropdownDate1(self._eleSpan(ele, k, "../.."),
                                                        ".//td[" + str(varTd) + "]/div/div/div/input", v)
                        elif k in ['本次服务类别']:
                            for i in v:
                                if isinstance(i, dict):
                                    ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='失访原因 ']", "..")
                                    Web_PO.eleSetTextByX(ele3,
                                                         ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                         i['失访原因'])
                                else:
                                    Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                              ".//td[" + str(varTd) + "]/div/div/div/label", i)
                        elif k in ['体重(kg)', '身长(cm)']:
                            Web_PO.eleSetTextBackspaceEnterByX(self._eleSpan(ele, k, "../.."),
                                                               ".//td[" + str(varTd) + "]/div/div/div[1]/input", 3,
                                                               v[0], 1)
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div[2]/label", v[1])
                        elif k in ['体重/身高']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div[2]/label", v)
                        elif k in [' 血红蛋白值 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input",
                                                 v)
                        elif k in ['耳', '听力', '胸部', '腹部']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v)
                        elif k in ['体格发育评估']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v)
                        elif k in ['出牙/龋齿数']:
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div[1]/input", v[0])
                            # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/div/form/table/tbody/tr[13]/td[3]/div/div/div[1]/input
                            # /html/body/div[1]/div/div[3]/section/div/main/div[2]/div[3]/div/form/table/tbody/tr[10]/td[4]/div/div/div[1]/input
                            Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                 ".//td[" + str(varTd) + "]/div/div/div[2]/input", v[1])
                        elif k in ['视力']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[" + str(varTd + 1) + "]/div/div/div[1]/input", v[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                 ".//td[" + str(varTd + 1) + "]/div/div/div[2]/input", v[1])
                        elif k in ['两次随访间']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k),
                                                    ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label")
                            Web_PO.eleCheckboxRightLabel3(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[1]/div/label",
                                                          ".//td[" + str(varTd) + "]/div/div/div/div[2]/div", v)
                        elif k in ['指导']:
                            Web_PO.eleCheckboxRightLabel2(self._eleSpan(ele, k, "../.."),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(self._eleSpan(ele, k, "../.."),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['发育评估', '管理服务 ']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k),
                                                          ".//td[" + str(varTd) + "]/div/div/div[1]/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                                             ".//td[" + str(varTd) + "]/div/div/div[2]/div/input",
                                                             i['其他'])
                        elif k in ['转诊']:
                            Web_PO.eleRadioRightLabel(self._eleSpan(ele, k, "../.."),
                                                      ".//td[" + str(varTd) + "]/div/div/div/label", v[0])
                            if v[0] == '有':
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='原因']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['原因'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='机构及科室']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['机构及科室'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系人']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系人'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='联系方式']", "..")
                                Web_PO.eleSetTextByX(ele3, ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/input",
                                                     v[1]['联系方式'])
                                ele3 = Web_PO.eleGetSuperEleByX(ele, ".//td[text()='结果']", "..")
                                Web_PO.eleRadioRightLabel(ele3,
                                                          ".//td[" + str(varTd * 2 - 2) + "]/div/div/div/label",
                                                          v[1]['结果'])
                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                               ".//td[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX,
                                               v)
                        elif k in ['家长签名']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//td[" + str(varTd) + "]/div/div/div/input",
                                                 v)

                ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)

            elif d_['title'] == '结案':
                ele2 = Web_PO.getSuperEleByX("//span[text()='结案']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)
                ele3 = Web_PO.getSuperEleByX(".//span[text()='结案原因：']")
                Web_PO.eleRadioRightLabel(ele3, ".//div/label", d_['data']['结案原因'])
                ele2 = Web_PO.getSuperEleByX("//span[text()='确定']", "..")
                Web_PO.eleClkByX(ele2, ".", 2)


        # todo 2.6.2  基本公卫 - 孕产妇管理 - 孕产妇登记

        def phs_maternalRecord_ycfregister_query(self, d_):

            # 孕产妇登记 - 查询

            ele = Web_PO.getSuperEleByX("//form", ".")
            _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

            for k, v in d_.items():
                try:
                    if k in ['姓名', '身份证号', '联系电话']:
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                    elif k in ['年龄']:
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                    elif k in ['档案状态']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                    elif k in ['管理机构']:
                        self.__gljg(ele, k, v)
                except:
                    self.logger.error("查询 => " + str(k) + ": " + str(v))

            Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询
            self.logger.info("查询 => " + str(d_))

        def phs_maternalRecord_ycfregister_operation(self, d_):

            # 孕产妇登记 - 操作

            try:
                if "data" not in d_:
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                        self._phs_child_etjob_operation('新增登记及第一次产前随访', d_['option'])) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)

                elif d_['operate'] == '新增登记及第一次产前随访':
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
                    for k, v in d_['data'].items():
                        if k in ['填表日期', '末次月经', '预产期', '建册日期', '下次访视时间']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)

                        elif k in ['是否高危产妇', 'RH血型']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)

                        elif k in ['丈夫姓名', '丈夫电话', '孕次', '身高(cm)', '体重(kg)', '体质指数(kg/m²)', '血红蛋白值', '白细胞计数值', '血小板计数值', ' 其他', 'B超', '建册单位', '居民签名']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//input", v)

                        elif k in ['丈夫年龄', ' 血糖']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)

                        elif k in ['产次', '孕周']:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", v[0])
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v[1])

                        elif k in ['末次月经']:
                            if isinstance(v, str):
                                Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div", v)
                            elif isinstance(v, list):
                                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)

                        elif k in ['既往史']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input", i[list(i.keys())[0]])
                        elif k in ['家族史']:
                            Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/div/div", v)
                            for i in v:
                                if isinstance(i, dict):
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", i[list(i.keys())[0]])
                        elif k in ['个人史']:
                            Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div/div", v)
                            for i in v:
                                if isinstance(i, dict):
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input", i[list(i.keys())[0]])
                        elif k in ['孕产史']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", v[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/input", v[2])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/input", v[3])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/input", v[4])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/input", v[5])

                        elif k in ['血压(mmHg)']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/input", v[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[2]/input", v[1])

                        elif k in ['妇科手术史', '肺部', '外阴', '宫颈', '附件']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", list(v.keys())[0])
                            if list(v.keys())[0] == '有' or list(v.keys())[0] == '异常':
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/input", v[list(v.keys())[0]])

                        elif k in ['心脏']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div[1]/div/div/div/label", list(v.keys())[0])
                            if list(v.keys())[0] == '异常':
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div[2]/div/div/div/input", v[list(v.keys())[0]])
                        elif k in ['阴道', '子宫']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[4]/div[1]/div/div/div/label", list(v.keys())[0])
                            if list(v.keys())[0] == '异常':
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div[2]/div/div/div/input", v[list(v.keys())[0]])

                        elif k in ['血常规']:
                            for k1, v1 in v.items():
                                if k1 == '血红蛋白值':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[2]/div/div/div/input", v1)
                                elif k1 == '白细胞计数值':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[1]/div[4]/div/div/div/input", v1)
                                elif k1 == '血小板计数值':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[2]/div[2]/div/div/div/input", v1)
                                elif k1 == '其他':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[2]/div[4]/div/div/div/input", v1)
                        elif k in ['尿常规']:
                            for k1, v1 in v.items():
                                if k1 == '尿蛋白':
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input", _dropdownByX, v1)
                                elif k1 == '尿糖':
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input", _dropdownByX, v1)
                                elif k1 == '尿酮体':
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[3]/div[4]/div/div/div/div/div/input", _dropdownByX, v1)
                                elif k1 == '尿潜血':
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input", _dropdownByX, v1)
                                elif k1 == '其他':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[4]/div/div/div/input", v1)

                        elif k in ['血型', ' 梅毒血清学试验']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div", v)

                        elif k in ['肝功能']:
                            for k1, v1 in v.items():
                                if k1 in ['血清谷丙转氨酶', '血清谷草转氨酶', '总胆红素']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                                elif k1 in ['白蛋白', '结合胆红素']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/input", v1)
                        elif k in ['肾功能']:
                            for k1, v1 in v.items():
                                if k1 in ['血清肌酐']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                                elif k1 in ['血尿素']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/input", v1)

                        elif k in ['阴道清洁度', ' HIV抗体检测']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)

                        elif k in [' 阴道分泌物']:
                            Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[1]/div/div/div/div", v, 'clear')
                            for i in v:
                                if isinstance(i, dict):
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div/input", i[list(i.keys())[0]])

                        elif k in ['乙型肝炎五项']:
                            for k1, v1 in v.items():
                                if k1 in ['乙型肝炎表面抗原', ' 乙型肝炎表面抗体',' 乙型肝炎e抗体']:
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input", _dropdownByX, v1)
                                elif k1 in [' 乙型肝炎e抗原',' 乙型肝炎核心抗体']:
                                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/div/div/input", _dropdownByX, v1)

                        elif k in ['总体评估', '建册情况']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", list(v.keys())[0])
                            if list(v.keys())[0] == '异常':
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v[list(v.keys())[0]])
                            elif list(v.keys())[0] == '已在其他机构建册':
                                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k,"../.."), ".//div[2]/div/div/div/div/input", v[list(v.keys())[0]])

                        elif k in ['保健指导']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", i[list(i.keys())[0]])

                        elif k in ['转诊']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[1]/div[1]/div/div/div/label", list(v.keys())[0])
                            if list(v.keys())[0] == '有':
                                for k1, v1 in v[list(v.keys())[0]].items():
                                    if k1 == '原因':
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[3]/div/div/div/input", v1)
                                    if k1 in ['机构及科室', '联系人', '联系方式']:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                                    if k1 == '结果':
                                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v1)

                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/div/input", _dropdownByX,  v)


                    # ele2 = Web_PO.getSuperEleByX("//span[text()='保存']", "..")
                    # Web_PO.eleClkByX(ele2, ".", 2)
                else:
                    print("error, 无法操作!")
                self.logger.info("点击" + str(d_))
            except:
                self.logger.error(str(d_) + "失败！")




    


    # todo 2.6.2  基本公卫 - 孕产妇管理 - 公共

    def __theFirstPrenatal(self, d_):

        # 第1次产前随访服务记录表

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        for k, v in d_.items():
            if k in ['填表日期', '末次月经', '预产期', '建册日期', '下次访视时间']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['是否高危产妇', 'RH血型']:
                Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)
            elif k in ['丈夫姓名', '丈夫电话', '孕次', '身高(cm)', '体重(kg)', '体质指数(kg/m²)', '血红蛋白值', '白细胞计数值', '血小板计数值',
                       ' 其他', 'B超', '建册单位', '居民签名']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['丈夫年龄', ' 血糖']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
            elif k in ['产次', '孕周']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", v[0])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v[1])
            elif k in ['末次月经']:
                if isinstance(v, str):
                    Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div", v)
                elif isinstance(v, list):
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['既往史']:
                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                for i in v:
                    if isinstance(i, dict):
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input", i[list(i.keys())[0]])
            elif k in ['家族史']:
                Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/div/div", v)
                for i in v:
                    if isinstance(i, dict):
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", i[list(i.keys())[0]])
            elif k in ['个人史']:
                Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div/div", v)
                for i in v:
                    if isinstance(i, dict):
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input", i[list(i.keys())[0]])
            elif k in ['孕产史']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/input", v[0])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/input", v[1])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/input", v[2])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/input", v[3])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/input", v[4])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/input", v[5])
            elif k in ['血压(mmHg)']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/input", v[0])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[2]/input", v[1])
            elif k in ['妇科手术史', '肺部', '外阴', '宫颈', '附件']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", list(v.keys())[0])
                if list(v.keys())[0] == '有' or list(v.keys())[0] == '异常':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/input", v[list(v.keys())[0]])
            elif k in ['心脏']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div[1]/div/div/div/label", list(v.keys())[0])
                if list(v.keys())[0] == '异常':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div[2]/div/div/div/input", v[list(v.keys())[0]])
            elif k in ['阴道', '子宫']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[4]/div[1]/div/div/div/label", list(v.keys())[0])
                if list(v.keys())[0] == '异常':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[4]/div[2]/div/div/div/input", v[list(v.keys())[0]])
            elif k in ['血常规']:
                for k1, v1 in v.items():
                    if k1 == '血红蛋白值':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[1]/div[2]/div/div/div/input", v1)
                    elif k1 == '白细胞计数值':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[1]/div[4]/div/div/div/input", v1)
                    elif k1 == '血小板计数值':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[2]/div[2]/div/div/div/input", v1)
                    elif k1 == '其他':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[2]/div[4]/div/div/div/input", v1)
            elif k in ['尿常规']:
                for k1, v1 in v.items():
                    if k1 == '尿蛋白':
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input",_dropdownByX, v1)
                    elif k1 == '尿糖':
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input",_dropdownByX, v1)
                    elif k1 == '尿酮体':
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),".//div[2]/div[1]/div[3]/div[4]/div/div/div/div/div/input",_dropdownByX, v1)
                    elif k1 == '尿潜血':
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input",_dropdownByX, v1)
                    elif k1 == '其他':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),".//div[2]/div[2]/div[4]/div/div/div/input", v1)
            elif k in ['血型', ' 梅毒血清学试验']:
                Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div", v)
            elif k in ['肝功能']:
                for k1, v1 in v.items():
                    if k1 in ['血清谷丙转氨酶', '血清谷草转氨酶', '总胆红素']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                    elif k1 in ['白蛋白', '结合胆红素']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/input", v1)
            elif k in ['肾功能']:
                for k1, v1 in v.items():
                    if k1 in ['血清肌酐']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                    elif k1 in ['血尿素']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/input", v1)
            elif k in ['阴道清洁度', ' HIV抗体检测']:
                Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div", v)
            elif k in [' 阴道分泌物']:
                Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon(ele, k),".//div[2]/div[1]/div[1]/div/div/div/div", v, 'clear')
                for i in v:
                    if isinstance(i, dict):
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),".//div[2]/div[1]/div[2]/div/div/div/input",i[list(i.keys())[0]])
            elif k in ['乙型肝炎五项']:
                for k1, v1 in v.items():
                    if k1 in ['乙型肝炎表面抗原', ' 乙型肝炎表面抗体', ' 乙型肝炎e抗体']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input",_dropdownByX, v1)
                    elif k1 in [' 乙型肝炎e抗原', ' 乙型肝炎核心抗体']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/div/div/input",_dropdownByX, v1)
            elif k in ['总体评估', '建册情况']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label",list(v.keys())[0])
                if list(v.keys())[0] == '异常':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input",v[list(v.keys())[0]])
                elif list(v.keys())[0] == '已在其他机构建册':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),".//div[2]/div/div/div/div/input", v[list(v.keys())[0]])
            elif k in ['保健指导']:
                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                for i in v:
                    if isinstance(i, dict):
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input",i[list(i.keys())[0]])
            elif k in ['转诊']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),".//div[2]/div[1]/div[1]/div[1]/div/div/div/label",list(v.keys())[0])
                if list(v.keys())[0] == '有':
                    for k1, v1 in v[list(v.keys())[0]].items():
                        if k1 == '原因':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[3]/div/div/div/input",v1)
                        if k1 in ['机构及科室', '联系人', '联系方式']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input",v1)
                        if k1 == '结果':
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k),".//div[2]/div/div/div/label", v1)
            elif k in ['随访医生签名']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/div/input", _dropdownByX, v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

    def __theSecondAndFifthPrenatal(self, d_):

        # 第2～5次产前随访服务记录表

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        for k1, v1 in d_.items():
            if '第2次' == k1:
                varTd = 1
            elif '第3次' == k1:
                varTd = 2
            elif '第4次' == k1:
                varTd = 3
            elif '第5次' == k1:
                varTd = 4

            for k, v in v1.items():
                if k in ['日期', '下次随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon2(ele, k),
                                              ".//div[2]/div[" + str(varTd) + "]/div/div/div/input", v)
                elif k in ['本次服务类别']:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k),
                                              ".//div[2]/div[" + str(varTd) + "]/div[1]/div/div/div/label",
                                              list(v.keys())[0])
                    if isinstance(v[list(v.keys())[0]], dict):
                        if '失访原因' in v[list(v.keys())[0]]:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                 ".//div[2]/div[" + str(varTd) + "]/div[2]/div[2]/div/div/div/input",
                                                 v[list(v.keys())[0]]['失访原因'])
                elif k in ['随访方式']:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k),
                                              ".//div[2]/div[" + str(varTd) + "]/div/div/div/label", v)
                elif k in ['孕周']:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                         ".//div[2]/div[" + str(varTd) + "]/div[1]/div/div/input", v[0])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                         ".//div[2]/div[" + str(varTd) + "]/div[2]/div/div/input", v[1])
                elif k in ['血压（mmHg）']:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                         ".//div[2]/div[" + str(varTd) + "]/div/div[1]/div/div/input", v[0])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                         ".//div[2]/div[" + str(varTd) + "]/div/div[2]/div/div/input", v[1])
                elif k in ['产前检查机构名称', '主诉', '体重（kg）', '宫底高度(cm)', '血红蛋白（g/L）', '其他辅助检查', '居民签名']:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                         ".//div[2]/div[" + str(varTd) + "]/div/div/div/input", v)
                elif k in ['宫底高度(cm)', '腹围(cm)']:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varTd) + "]/div/div/div/input", v)
                elif k in ['胎位']:
                    if len(v) == 1:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div[" + str(varTd) + "]/div/div[1]/div/div/div/div/div/input",
                                           _dropdownByX, v[0])
                    else:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div[" + str(varTd) + "]/div/div[1]/div/div/div/div/div/input",
                                           _dropdownByX, v[0])
                        v.pop(0)
                        for i in range(len(v)):
                            Web_PO.eleClkByX(Web_PO.eleCommon(ele, k),
                                             ".//div[2]/div[" + str(varTd) + "]/div/div[2]")  # 点击 +
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varTd) + "]/div[" + str(
                                i + 2) + "]/div[1]/div/div/div/div/div/input", _dropdownByX, v[i])
                elif k in ['胎心率(次/分钟)']:
                    for i in range(len(v)):
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(varTd) + "]/div[" + str(
                            i + 1) + "]/div/div/div[1]/input", v[i])
                elif k in ['尿蛋白', '随访医生签名']:
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k),
                                       ".//div[2]/div[" + str(varTd) + "]/div/div/div/div/div/input", _dropdownByX, v)
                elif k in ['免费血清学产前筛查']:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k),
                                              ".//div[2]/div[" + str(varTd) + "]/div[1]/div/div/div/label",
                                              list(v.keys())[0])
                    Web_PO.eleCheckboxLeftLabel(Web_PO.eleCommon2(ele, k),
                                                ".//div[2]/div[" + str(varTd) + "]/div[2]/div/div/div[1]/div",
                                                v[list(v.keys())[0]])

                elif k in ['随访结果分类']:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k),
                                              ".//div[2]/div[" + str(varTd) + "]/div[1]/div/div/div/label",
                                              list(v.keys())[0])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                         ".//div[2]/div[" + str(varTd) + "]/div[2]/div/div/div/textarea",
                                         v[list(v.keys())[0]])
                elif k in ['指导']:
                    Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon2(ele, k),
                                                 ".//div[2]/div[" + str(varTd) + "]/div[1]/div/div/div/div", v)
                    for i in v:
                        if isinstance(i, dict):
                            if '其他' in i:
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                     ".//div[2]/div[" + str(varTd) + "]/div[2]/div/div/div/input", i['其他'])
                elif k in ['转诊']:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k),
                                              ".//div[2]/div[" + str(varTd) + "]/div[1]/div/div/div/label",
                                              list(v.keys())[0])
                    if '有' in v:
                        if '原因' in v[list(v.keys())[0]]:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                 ".//div[2]/div[" + str(varTd) + "]/div[2]/div[2]/div/div/div/input",
                                                 v[list(v.keys())[0]]['原因'])
                        if '机构及科室' in v[list(v.keys())[0]]:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                 ".//div[2]/div[" + str(varTd) + "]/div[3]/div[2]/div/div/div/input",
                                                 v[list(v.keys())[0]]['机构及科室'])
                        if '联系人' in v[list(v.keys())[0]]:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                 ".//div[2]/div[" + str(varTd) + "]/div[4]/div[2]/div/div/div/input",
                                                 v[list(v.keys())[0]]['联系人'])
                        if '联系方式' in v[list(v.keys())[0]]:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                                 ".//div[2]/div[" + str(varTd) + "]/div[5]/div[2]/div/div/div/input",
                                                 v[list(v.keys())[0]]['联系方式'])
                        if '结果' in v[list(v.keys())[0]]:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k),
                                                      ".//div[2]/div[" + str(varTd) + "]/div[6]/div[2]/div/div/div/label",
                                                      v[list(v.keys())[0]]['结果'])
                elif k in ['居民签名']:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k),
                                         ".//div[2]/div[" + str(varTd) + "]/div/div/div/input", v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

    def __postpartumVisit(self, d_):

        # 产后访视记录表

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        for k, v in d_.items():
            if k in ['随访日期', '分娩日期', '出院日期', '下次随访日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            elif k in ['本次服务类别']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", list(v.keys())[0])
                if isinstance(v[list(v.keys())[0]], dict):
                    if '失访原因' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='失访原因']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['失访原因'])
            elif k in ['体温(­°C)', '一般健康情况', '一般心理状况', '其他']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            elif k in ['血压(mmHg)']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/input", v[0])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[2]/input", v[1])
            elif k in ['乳房', '子宫', '分类']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div/label",
                                          list(v.keys())[0])
                if '异常' in v:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input",
                                         v[list(v.keys())[0]])
            elif k in ['恶露', '伤口']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div/label",
                                          list(v.keys())[0])
                if '异常' in v:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input",
                                         v[list(v.keys())[0]])
            elif k in ['指导']:
                Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div", v)
                for i in v:
                    if isinstance(i, dict):
                        if '其他' in i:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", i['其他'])
            elif k in ['转诊']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[1]/div/div/div/label",
                                          list(v.keys())[0])
                if '有' in v:
                    if '转诊原因' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='转诊原因']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['转诊原因'])
                    if '转诊机构及科室' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='转诊机构及科室']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['转诊机构及科室'])
                    if '联系人' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='联系人']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['联系人'])
                    if '联系方式' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='联系方式']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['联系方式'])
                    if '结果' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='结果']", "..")
                        Web_PO.eleRadioRightLabel(ele3, ".//div[2]/div/div/div/label", v[list(v.keys())[0]]['结果'])
            elif k in ['随访医生签名']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input", _dropdownByX, v)
            elif k in ['居民签名']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

    def __42daysPostpartum(self, d_):

        # 产后42天健康检查记录表

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        for k, v in d_.items():
            if k in ['随访日期', '分娩日期', '出院日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            elif k in ['本次服务类别']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", list(v.keys())[0])
                if isinstance(v[list(v.keys())[0]], dict):
                    if '失访原因' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='失访原因']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['失访原因'])
            elif k in ['一般健康情况', '一般心理状况', '其他', '产后检查机构名称']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            elif k in ['血压(mmHg)']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/input", v[0])
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[2]/input", v[1])
            elif k in ['乳房', '子宫']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div/label",
                                          list(v.keys())[0])
                if '异常' in v:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input",
                                         v[list(v.keys())[0]])
            elif k in ['恶露', '伤口']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div/label",
                                          list(v.keys())[0])
                if '异常' in v:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input",
                                         v[list(v.keys())[0]])
            elif k in ['分类']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon2(ele, k), ".//div[1]/div[2]/div/div/div/label",
                                          list(v.keys())[0])
                if '未恢复' in v:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/input",
                                         v[list(v.keys())[0]])
            elif k in ['指导']:
                Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div", v)
                for i in v:
                    if isinstance(i, dict):
                        if '其他' in i:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", i['其他'])
            elif k in ['处理']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[1]/div/div/div/label",
                                          list(v.keys())[0])
                if '转诊' in v:
                    if '转诊原因' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='转诊原因']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['转诊原因'])
                    if '转诊机构及科室' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='转诊机构及科室']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['转诊机构及科室'])
                    if '联系人' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='联系人']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['联系人'])
                    if '联系方式' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='联系方式']", "..")
                        Web_PO.eleSetTextByX(ele3, ".//div[2]/div/div/div/input", v[list(v.keys())[0]]['联系方式'])
                    if '结果' in v[list(v.keys())[0]]:
                        ele3 = Web_PO.eleGetSuperEleByX(ele, ".//div[text()='结果']", "..")
                        Web_PO.eleRadioRightLabel(ele3, ".//div[2]/div/div/div/label", v[list(v.keys())[0]]['结果'])
            elif k in ['随访医生签名']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input", _dropdownByX, v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

    # todo 2.6.2  基本公卫 - 孕产妇管理 - 孕产妇登记

    def phs_maternalRecord_ycfregister_query(self, d_):

        # 孕产妇登记 - 查询

        ele = Web_PO.getSuperEleByX("//form", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '联系电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['档案状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input", _dropdownByX, v)
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)
        # 日志
        self.logger.info("查询 => " + str(d_))

    def phs_maternalRecord_ycfregister_operation(self, d_):

        # 孕产妇登记 - 操作

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_child_etjob_operation('新增登记及第一次产前随访', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
            elif d_['operate'] == '新增登记及第一次产前随访':
                self.__theFirstPrenatal(d_['data'])
            else:
                print("error, 无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")



    # todo 2.6.3  基本公卫 - 孕产妇管理 - 孕产妇档案

    def phs_maternalRecord_ycffiles_query(self, d_):

        # 孕产妇档案 - 查询

        # 获取字段和xpath字典
        ele = Web_PO.getSuperEleByX("//form", ".")
        l_text = Web_PO.eleGetTextByLabel(ele, 'label')
        l_xpath = Web_PO.eleGetXpathByLabel(ele, 'input')
        dd_text_xpath = dict(zip(l_text, l_xpath))
        print("孕产妇档案 =>", dd_text_xpath)  # {'管理机构': 'id("app")/DIV[1]/D...

        # 获取字段和类型字典
        d_local = d_tmp = {}
        for k, v in dd_text_xpath.items():
            if Web_PO.isEleAttrExistByX(v, 'readonly'):
                d_local[k] = '单下拉框'
            else:
                d_local[k] = '文本'
        d_tmp['管理机构'] = '管理机构'
        d_local.update(d_tmp)
        print("孕产妇档案 =>", d_local) # {'管理机构': '管理机构', '是否仅查询机构': '单下拉框', '档案状态': '单下拉框', '姓名': '文本', '身份证号': '文本', '上次完成 检查类型': '单下拉框'}

        # 遍历字段和值
        for k, v in d_.items():
            try:
                eval(self.d_g_type_func[d_local[k]])
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)
        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_maternalRecord_ycffiles_operation(self, varOperation, d_option):

        # 孕产妇档案 - 操作

        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '提醒', '性别', '出生日期时间', '年龄', '上次完成检查类型', '上次随访日期', '下次随访日期', '母亲姓名', '母亲联系电话', '父亲姓名', '父亲联系电话', '管理状态', '管理类别', '登记机构', '身份证号', '家庭住址', '操作']

        # 获取列表所有值
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
            if "提醒" in l_field:
                for i in l_group:
                    i.pop(3)
                    i.pop(3)
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_maternalRecord_ycffiles_operation(self, d_):

        # 孕产妇档案 - 操作

        if "data" not in d_:
            ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                self._phs_maternalRecord_ycffiles_operation('健康检查记录', d_['option'])) + "]", ".")
            Web_PO.eleClkByX(ele3, ".", 2)
        elif d_['title'] == '第一次产前随访服务记录表':
            Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div/div[1]', 2)
            self.__theFirstPrenatal(d_['data'])
        elif d_['title'] == '第2～5次产前随访服务记录表':
            Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[2]/div/div[1]', 2)
            self.__theSecondAndFifthPrenatal(d_['data'])
        elif d_['title'] == '产后访视记录表':
            Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[3]/div/div[1]', 2)
            self.__postpartumVisit(d_['data'])
        elif d_['title'] == '产后42天健康检查记录表':
            Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[4]/div/div', 2)
            self.__42daysPostpartum(d_['data'])
        elif d_['title'] == '结案':
            Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='结案']", ".."), ".", 2)
            Web_PO.eleRadioRightLabel(Web_PO.getSuperEleByX(".//span[text()='结案原因：']"), ".//div/label", d_['data']['结案原因'])
            Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确定']", ".."), ".", 2)



    # todo 2.6.4  基本公卫 - 孕产妇管理 - 孕产妇随访

    def phs_maternalRecord_ycfjob_query(self, d_):

        # 孕产妇随访 - 查询

        # 获取字段和xpath字典
        ele = Web_PO.getSuperEleByX("//form", ".")
        l_text = Web_PO.eleGetTextByLabel(ele, 'label')
        if '随访日期' in l_text:
            index = l_text.index('随访日期')
            l_text.insert(index+1, '随访日期2')
        l_xpath = Web_PO.eleGetXpathByLabel(ele, 'input')
        dd_text_xpath = dict(zip(l_text, l_xpath))
        print("孕产妇随访 =>", dd_text_xpath)  # {'管理机构': 'id("app")/DIV[1]/D...

        # 获取字段和类型字典
        d_local = d_tmp = {}
        for k, v in dd_text_xpath.items():
            if Web_PO.isEleAttrExistByX(v, 'readonly'):
                d_local[k] = '单下拉框'
            else:
                d_local[k] = '文本'
        d_tmp['管理机构'] = '管理机构'
        d_local.update(d_tmp)
        print("孕产妇随访 =>", d_local)  # {'管理机构': '管理机构', '是否仅查询机构': '单下拉框', '姓名': '文本', '身份证号': '文本', '检查类型': '单下拉框', '随访日期': '文本', '随访日期2': '文本'}

        # 遍历字段和值
        for k, v in d_.items():
            try:
                if k in ['随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                else:
                    eval(self.d_g_type_func[d_local[k]])
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(ele, ".//button[1]", 2)
        self.logger.info("查询 => " + str(d_))

    def _phs_maternalRecord_ycfjob_operation(self, varOperation, d_option):

        # 孕产妇随访 - 操作

        # 获取字段列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '登记时年龄', '出生日期', '身份证号', '联系电话', '随访日期', '检查类型', '家庭住址', '操作']

        # 获取字段值列表
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['李明明', '35', '1990-01-01', '110101199001014243', '13818882722', '2025-01-20', '产后访视', '罗峰街道文化区社区居民委员会测'], ...

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def phs_maternalRecord_ycfjob_operation(self, d_):

        # 孕产妇档案 - 操作

        if "data" not in d_:
            ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                self._phs_maternalRecord_ycfjob_operation('编辑\n删除', d_['option'])) + "]", ".")
            Web_PO.eleClkByX(ele3, ".", 2)
            if d_['operate'] == '删除':
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='是']", ".."), ".", 2)
                self.logger.info("删除 => " + str(d_))
        elif d_['title'] == '第一次产前随访服务记录表':
            Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div/div[1]', 2)
            self.__theFirstPrenatal(d_['data'])
        elif d_['title'] == '第2～5次产前随访服务记录表':
            Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[2]/div/div[1]', 2)
            self.__theSecondAndFifthPrenatal(d_['data'])
        elif d_['title'] == '产后访视记录表':
            Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[3]/div/div[1]', 2)
            self.__postpartumVisit(d_['data'])
        elif d_['title'] == '产后42天健康检查记录表':
            Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[4]/div/div', 2)
            self.__42daysPostpartum(d_['data'])
        elif d_['title'] == '结案':
            ele2 = Web_PO.getSuperEleByX("//span[text()='结案']", "..")
            Web_PO.eleClkByX(ele2, ".", 2)
            ele3 = Web_PO.getSuperEleByX(".//span[text()='结案原因：']")
            Web_PO.eleRadioRightLabel(ele3, ".//div/label", d_['data']['结案原因'])
            ele2 = Web_PO.getSuperEleByX("//span[text()='确定']", "..")
            Web_PO.eleClkByX(ele2, ".", 2)



    # todo 2.7.1  基本公卫 - 老年人健康管理 - common

    def __tjb(self, d_):
        # 体检表
        ele = Web_PO.getSuperEleByX("//div[text()='国家基本公共卫生服务项目健康体检表']", "../..")
        ele4 = Web_PO.getSuperEleByX("//div[text()='辅助检查']", "../../..")

        for k, v in d_['data'].items():
            if k in ['体检来源']:
                Web_PO.eleRadioRightLabel(Web_PO.eleDiv(ele, k), './/div[2]/div/div/div/label', v)
            elif k in ['体检日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['责任医生', '体温', '脉率', '呼吸频率', '腰围', '身高', '体重']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['右侧血压']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
            elif k in ['症状']:
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleP(ele, k, "../.."), './/div[2]/div/div[1]/div/div/label',
                                                    v, './/div[2]/div/div[1]/div/div/div/input')
            elif k in [' 老年人健康', ' 老年人生活自理', '饮酒频率', '是否戒酒', ' 听力 ', ' 运动能力 ', ' 眼底 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), './/div[2]/div/div/div/label', v)
            elif k in ['老年人认知能力', '老年人情感状态']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), './/div[4]/div/div/div/label')
                if isinstance(v, str):
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), './/div[4]/div/div/div/label', v)
                elif isinstance(v, dict):
                    Web_PO.eleRadioRightLabel(Web_PO.eleDiv(ele, k), './/div[4]/div/div/div/label', list(v.keys())[0])
                    Web_PO.eleClsReadonlyByX(Web_PO.eleDiv(ele, k), ".//div[4]/div[2]/div/div/input", 2)
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[4]/div[2]/div/div/input", v[list(v.keys())[0]])
            elif k in ['体育锻炼']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '锻炼频率'), ".//div/div/label")
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '锻炼频率'), ".//div/div/label", v['锻炼频率'])
                if v['锻炼频率'] != '不锻炼':
                    for k1, v1 in v.items():
                        if k1 != '锻炼频率':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div/div/input", v1)
            elif k in [' 饮食习惯 ']:
                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in [' 吸烟情况 ']:
                Web_PO.eleDropdown(Web_PO.eleDiv(ele, k), './/div[2]/div/div/div/div/div/input',
                                    v['吸烟状况'])
                if v['吸烟状况'] != '从不吸':
                    for k1, v1 in v.items():
                        if k1 != '吸烟状况':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div/div/input", v1)
            elif k in [' 饮酒情况 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '饮酒频率'), ".//div/div/label", v['饮酒频率'])
                if v['饮酒频率'] != '从不':
                    for k1, v1 in v.items():
                        if k1 == '日饮酒量' or k1 == '开始饮酒年龄':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div/div/input", v1)
                        elif k1 == '近一年内是否曾醉酒':
                            Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele, '近一年内是否曾醉酒'), ".//div/div/label", v1)
                for k1, v1 in v.items():
                    if k1 == '是否戒酒':
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '是否戒酒'), ".//div/div/label", list(v1.keys())[0])
                        if list(v1.keys())[0] == '已戒酒':
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, '戒酒年龄'), ".//div/div/input", v1['已戒酒'])
                    if k1 == '饮酒种类':
                        Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele, '饮酒种类'), ".//div/div/label", v1)
            elif k in ['职业病危害']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[1]/div/div/label")
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[1]/div/div/label",
                                                 list(v.keys())[0])
                for k1, v1 in v.items():
                    if k1 == '有':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[2]/div[1]/input", v1[0])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[1]/div[2]/div[2]/input", v1[1])
                    if k1 == '毒物种类':
                        for k2, v2 in v1.items():
                            if k2 == '粉尘':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[2]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[2]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[2]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[2]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '化学有害因素':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[3]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '物理有害因素':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[4]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '生物因素':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[5]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '放射物质类':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[6]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[6]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[6]/div[3]/div/div/label",
                                                                 list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[6]/div[4]/input",
                                                         v2[2]['防护措施']['有'])
                            if k2 == '不详':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[7]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[7]/div[2]/input", v2[1])
                                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele, k),
                                                                 ".//div[2]/div[7]/div[3]/div/div/label",list(v2[2]['防护措施'].keys())[0])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[7]/div[4]/input",v2[2]['防护措施']['有'])
                            if k2 == '其他':
                                if v2[0] == '勾选':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[8]/div[1]/div/label")
                                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[8]/div[2]/input", v2[1])
                                if list(v2[2]['防护措施'].keys())[0] == '有':
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[8]/div[3]/div/div/label[2]", 2)
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[8]/div[4]/input",v2[2]['防护措施']['有'])
                                else:
                                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k),".//div[2]/div[8]/div[3]/div/div/label[1]", 2)
            elif k in [' 口腔 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '口唇'), ".//div/div/label")
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele, '口唇'), ".//div/div/label", v['口唇'])
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele, '咽部'), ".//div/div/label", v['咽部'])
                if '正常' in v['齿列']:
                    Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/label[1]")
                else:
                    for k1, v1 in v['齿列'].items():
                        if k1 == '缺齿':
                            Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/label[2]")
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[1]/div[1]/div/input",
                                                 v1[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[1]/div[2]/div/input",
                                                 v1[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[4]/div[1]/div/input",
                                                 v1[2])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[3]/div[4]/div[2]/div/input",
                                                 v1[3])
                        if k1 == '龋齿':
                            Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/label[3]")
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[1]/div[1]/div/input",
                                                 v1[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[1]/div[2]/div/input",
                                                 v1[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[4]/div[1]/div/input",
                                                 v1[2])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[4]/div[4]/div[2]/div/input",
                                                 v1[3])
                        if k1 == '义齿(假牙)':
                            Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), ".//div[2]/label[4]")
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[1]/div[1]/div/input",
                                                 v1[0])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[1]/div[2]/div/input",
                                                 v1[1])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[4]/div[1]/div/input",
                                                 v1[2])
                            Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele, k), ".//div[2]/div[5]/div[4]/div[2]/div/input",
                                                 v1[3])
            elif k in [' 视力 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '口唇'), ".//div/div/label")
                for k1, v1 in v.items():
                    if k1 == '左眼':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/input", v1)
                    if k1 == '右眼':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/input", v1)
                    if k1 == '矫正视力左眼':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/input", v1)
                    if k1 == '矫正视力右眼':
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/input", v1)
            elif k in [' 皮肤 ', ' 巩膜 ', ' 淋巴结 ']:
                if '其他' in v:
                    Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                     ".//div[2]/div/div/div/div/input")
                else:
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label",
                                              list(v.keys())[0])
            elif k in [' 肺 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '桶状胸'), ".//div/div/label")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '桶状胸'), ".//div/div/label", v['桶状胸'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '呼吸音'), ".//div/div/label", v['呼吸音'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '罗音'), ".//div/div/label", v['罗音'],
                                                 ".//div/div/div/input")
            elif k in [' 心脏 ']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, '心率'), ".//div/div/input", v['心率'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '心律'), ".//div/div/label", v['心律'])
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '杂音'), ".//div/div/label", v['杂音'],
                                                 ".//div/div/div/input")
            elif k in [' 腹部 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '压痛'), ".//div/div/label")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '压痛'), ".//div/div/label", v['压痛'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '包块'), ".//div/div/label", v['包块'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '肝大'), ".//div/div/label", v['肝大'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '脾大'), ".//div/div/label", v['脾大'],
                                                 ".//div/div/div/input")
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, '移动性浊音'), ".//div/div/label", v['移动性浊音'],
                                                 ".//div/div/div/input")
            elif k in [' 下肢水肿 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in [' 足背动脉搏动 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in [' 肛门指诊 ']:
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                 ".//div[2]/div/div/div/div/input")
            elif k in [' 乳腺 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label")
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                    ".//div[2]/div/div/div/div/input")
            elif k in [' 妇科 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '外阴'), ".//div/div/label", v['外阴'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '阴道'), ".//div/div/label", v['阴道'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '宫颈'), ".//div/div/label", v['宫颈'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '宫体'), ".//div/div/label", v['宫体'])
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, '附件'), ".//div/div/label", v['附件'])
            elif k in [' 其他 ']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/textarea", v)
            elif k in [' 脑血管疾病 ', ' 肾脏疾病 ', ' 心血管疾病 ', ' 眼部疾病 ', ' 神经系统疾病 ', ' 其他系统疾病 ']:
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                    ".//div[2]/div/div/div/div/input")
            elif k in [' 住院史 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div[1]/div/div/div/input")
                if len(v) == 1:
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[1]/div/div/div/input",
                                            v[0]['入院日期'])
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[2]/div/div/div/input",
                                            v[0]['出院日期'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[3]/div/div/div/input",
                                         v[0]['原因'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[4]/div/div/div/input",
                                         v[0]['医疗机构及科室名称'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[5]/div/div/div/input",
                                         v[0]['病案号'])
                else:
                    for i in range(len(v) - 1):
                        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div[6]/button")  # 添加
                    for i in range(len(v)):
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k),
                                                ".//div[2]/div/div[" + str(i + 2) + "]/div[1]/div/div/div/input",
                                                v[i]['入院日期'])
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k),
                                                ".//div[2]/div/div[" + str(i + 2) + "]/div[2]/div/div/div/input",
                                                v[i]['出院日期'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[3]/div/div/div/input",
                                             v[i]['原因'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[4]/div/div/div/input",
                                             v[i]['医疗机构及科室名称'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[5]/div/div/div/input",
                                             v[i]['病案号'])
            elif k in [' 家庭病床 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div[1]/div/div/div/input")
                if len(v) == 1:
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[1]/div/div/div/input",
                                            v[0]['建床日期'])
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[2]/div/div/div/input",
                                            v[0]['撤床日期'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[3]/div/div/div/input",
                                         v[0]['原因'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[4]/div/div/div/input",
                                         v[0]['医疗机构及科室名称'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k), ".//div[2]/div/div[2]/div[5]/div/div/div/input",
                                         v[0]['病案号'])
                else:
                    for i in range(len(v) - 1):
                        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div[6]/button")  # 添加
                    for i in range(len(v)):
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k),
                                                ".//div[2]/div/div[" + str(i + 2) + "]/div[1]/div/div/div/input",v[i]['建床日期'])
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, k),
                                                ".//div[2]/div/div[" + str(i + 2) + "]/div[2]/div/div/div/input",v[i]['撤床日期'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[3]/div/div/div/input",v[i]['原因'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[4]/div/div/div/input",v[i]['医疗机构及科室名称'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[5]/div/div/div/input",v[i]['病案号'])
            elif k in ['主要用药情况']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/div/input")
                if len(v) == 1:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/div/input",v[0]['药物名称'])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/div/div/input",v[0]['途径'])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div/div/div/div/div/input",v[0]['频次'])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/div/div/div/input", v[0]['单次剂量'])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[5]/div/div/div/input",v[0]['剂量单位'])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[6]/div/div/div/input", v[0]['每日剂量'])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[7]/div/div/div/input", v[0]['用药时间'])
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[8]/div/div/div/div/div/input",v[0]['服药依从性'])
                else:
                    for i in range(len(v) - 1):
                        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div[9]/button")  # 添加
                    for i in range(len(v)):
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div/div[" + str(i + 2) + "]/div[1]/div/div/div/div/div/input",v[i]['药物名称'])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div/div[" + str(i + 2) + "]/div[2]/div/div/div/div/div/input",v[i]['途径'])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div/div[" + str(i + 2) + "]/div[3]/div/div/div/div/div/input",v[i]['频次'])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[4]/div/div/div/input",v[i]['单次剂量'])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k),
                                                  ".//div[2]/div/div[" + str(i + 2) + "]/div[5]/div/div/div/input", v[i]['剂量单位'])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[6]/div/div/div/input",v[i]['每日剂量'])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k),
                                             ".//div[2]/div/div[" + str(i + 2) + "]/div[7]/div/div/div/input", v[i]['用药时间'])
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k),
                                           ".//div[2]/div/div[" + str(i + 2) + "]/div[8]/div/div/div/div/div/input",v[i]['服药依从性'])
            elif k in [' 非免疫规划预防接种史 ']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, '主要用药情况'),".//div[4]/div/div[2]/div[1]/div/div/div/div/div/input")
                if len(v) == 1:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, '主要用药情况'),".//div[4]/div/div[2]/div[1]/div/div/div/div/div/input",v[0]['接种名称'])
                    Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, '主要用药情况'),".//div[4]/div/div[2]/div[2]/div/div/div/input", v[0]['接种日期'])
                    Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, '主要用药情况'), ".//div[4]/div/div[2]/div[3]/div/div/div/input",v[0]['接种机构'])
                else:
                    for i in range(len(v) - 1):
                        Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div[1]/div[4]/button")  # 添加
                    for i in range(len(v)):
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, '主要用药情况'),".//div[4]/div/div[" + str(i + 2) + "]/div[1]/div/div/div/div/div/input",v[i]['接种名称'])
                        Web_PO.eleDropdownDate1(Web_PO.eleDiv(ele, '主要用药情况'),".//div[4]/div/div[" + str(i + 2) + "]/div[2]/div/div/div/input",v[i]['接种日期'])
                        Web_PO.eleSetTextByX(Web_PO.eleDiv(ele, '主要用药情况'),".//div[4]/div/div[" + str(i + 2) + "]/div[3]/div/div/div/input",v[i]['接种机构'])

            # //form2
            elif k in ['血常规']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele4, '血红蛋白值 '), ".//div/div/input")
                for k1, v1 in v.items():
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele4, k1), ".//div/div/input", v1)
            elif k in ['尿常规']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele4, '血红蛋白值 '), ".//div/div/input")
                for k1, v1 in v.items():
                    if k1 in ['尿蛋白定性检测结果', '尿糖定性检测结果 ', '尿酮体定性检测结果', '尿潜血定性检测结果', '尿白细胞']:
                        Web_PO.eleDropdown(Web_PO.eleCommon(ele4, k1), ".//div/div/div/div/input", v1)
                    else:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele4, k1), ".//div/div/input", v1)
            elif k in ['血糖', '肝功能', '肾功能', '血脂']:
                for k1, v1 in v.items():
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele4, k1), ".//div/div/input", v1)
            elif k in ['尿微量白蛋白', '糖化血红蛋白']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele4, k), ".//div[2]/div/div/div/input", v)
            elif k in ['大便潜血']:
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleP(ele4, k, "../.."), ".//div[2]/div/div/div/label", v)
            elif k in ['乙型五项检查']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele4, '乙型肝炎病毒表面抗原检测结果'), ".//div/div/label")
                for k1, v1 in v.items():
                    Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon(ele4, k1), ".//div/div/label", v1)
            elif k in ['心电图', '胸部X线片', 'B超', '宫颈涂片']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon2(ele4, k), ".//div[2]/label")
                Web_PO.eleRadioRightLabelByCheck(Web_PO.eleCommon2(ele4, k), ".//div[2]/label", list(v.keys())[0])
                if list(v.keys())[0] == '异常':
                    Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele4, k), ".//div[2]/div/textarea", v['异常'])
            elif k in ['其他辅助检查']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon2(ele4, k), ".//div[2]/div/textarea", v)

            # 无 form
            elif k in ['健康评价']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='健康评价']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                Web_PO.eleRadioRightLabelByCheck(ele5, ".//div[2]/div[1]/span[1]/label", list(v.keys())[0])
                if list(v.keys())[0] == '有异常':
                    for i in range(len(v['有异常'])):
                        Web_PO.eleClkByX(ele5, ".//div[2]/div[1]/div/button", 2)
                        Web_PO.eleSetTextByX(ele5, ".//div[2]/div[2]/div[1]/div[" + str(i + 1) + "]/div[1]/input", v['有异常'][i])

            elif k in ['健康指导']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='健康指导']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                for i in range(len(v)):
                    if v[i] == '纳入慢性病患者健康管理':
                        Web_PO.eleClkByX(ele5, ".//div[2]/div/div[1]/div/label", 2)
                    elif v[i] == '建议复查':
                        Web_PO.eleClkByX(ele5, ".//div[2]/div/div[2]/label", 2)
                    elif v[i] == '建议转诊':
                        Web_PO.eleClkByX(ele5, ".//div[2]/div/div[3]/label", 2)
            elif k in ['危险因素控制']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='危险因素控制']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                Web_PO.eleCheckboxRightLabel2(ele5, ".//div[2]/div/div[1]/label", v[0])
                if v[1][0] == '减体重':
                    Web_PO.eleClkByX(ele5, ".//div[2]/div/div[2]/label", 2)
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div/div[2]/div/input", v[1][1])
                if v[2][0] == '建议接种疫苗':
                    Web_PO.eleClkByX(ele5, ".//div[2]/div/div[3]/label", 2)
                    Web_PO.eleDropdown(ele5, ".//div[2]/div/div[3]/div/div/div[1]/input",v[2][1])
                if v[3][0] == '其他':
                    Web_PO.eleClkByX(ele5, ".//div[2]/div/div[4]/label", 2)
                    Web_PO.eleSetTextByX(ele5, ".//div[2]/div/div[4]/div/textarea", v[3][1])
            elif k in ['建议']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='建议']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div/textarea", v)
            elif k in ['结果反馈']:
                ele5 = Web_PO.getSuperEleByX("//h4[text()='结果反馈']", "../..")
                Web_PO.eleScrollViewByX(ele5, ".")
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div[2]/div[1]/span[2]/span/span[2]/span/span[1]/div/input",v['本人'])
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div[2]/div[1]/span[2]/span/span[2]/span/span[3]/div/input",v['家属'])
                Web_PO.eleSetTextByX(ele5, ".//div[2]/div[2]/div[2]/span[2]/span/span[2]/div/input", v['反馈人'])
                Web_PO.eleDropdownDate1(ele5, ".//div[2]/div[2]/div[3]/span[2]/span/span[2]/div/input", v['时间'])
            elif k in ['医生签名']:
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[4]/div[2]/div/div[2]/span[2]/div/input',
                    v['症状'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[6]/div[2]/div/span[2]/div/input',
                    v['一般状况'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[8]/div[2]/div/span[2]/div/input',
                    v['生活方式'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[10]/div[2]/div/span[2]/div/input',
                    v['脏器功能'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[11]/div[2]/div/span[2]/div/input',
                    v['查体'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[12]/div[2]/div/span[2]/div/input',
                    v['皮肤'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[13]/div[2]/div/span[2]/div/input',
                    v['肛门指诊'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[14]/div[2]/div/span[2]/div/input',
                    v['乳腺'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[15]/div[2]/div/span[2]/div/input',
                    v['妇科'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[16]/div[2]/div/span[2]/div/input',
                    v['其他'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[17]/div[2]/div/span[2]/div/input',
                    v[' 现存主要健康问题 '])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[1]/form/div[2]/div[18]/div[2]/div/span[2]/div/input',
                    v['主要用药情况'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[2]/div/div[1]/div[2]/div/span[2]/div/input',
                    v['血常规'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[2]/div/div[2]/div[2]/div/span[2]/div/input',
                    v['尿微量白蛋白'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[2]/div/div[3]/div[2]/div/span[2]/div/input',
                    v['大便潜血'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[1]/div[2]/div/span[2]/div/input',
                    v['心电图'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[2]/div[2]/div/span[2]/div/input',
                    v['胸部X线片'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[3]/div[2]/div/span[2]/div/input',
                    v['B超'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[4]/div[2]/div/span[2]/div/input',
                    v['宫颈涂片'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[2]/div[1]/form/div/div[4]/div/div[5]/div[2]/div/span[2]/div/input',
                    v['其他辅助检查'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[3]/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/span[2]/div/input',
                    v['健康评价'])
                Web_PO.setTextByX(
                    '/html/body/div[1]/div/div[3]/section/div/div/div[1]/div[2]/form/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/span[2]/div/input',
                    v['健康指导'])
        Web_PO.button1('保存')

    def __chineseMedicineHealthManagementServiceRecord(self, d_):
        # 老年人中医药健康管理服务记录表
        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in ["1.你精力充沛吗？(指精神头足,乐于做事)", "2.您容易疲乏吗？(指体力如何，是否稍微活动一下或做一点家务劳动就感觉到累)",
                     "3.您容易气短，呼吸短促，接不上气吗？", "4.您说话声音低弱无力吗？(指说话没有力气)", "5.您感觉到闷闷不乐，情绪低沉吗？(指心情不愉快，情绪低落)",
                     "6.您容易情绪紧张吗，焦虑不安吗？(指遇事是否心情紧张)", "7.您因为生活状态改变而感到孤独，失落？", "8.您容易感到害怕或受到惊吓？",
                     "9.您感到身体超重不轻松吗？(感觉身体沉重)[BMI指数=体重(kg)/身高(m)]", "10.您眼睛干涩吗？", "11.您手脚发凉吗？(不包含因周围温度低或穿的少导致的手脚发冷)",
                     "12.您胃脘部，背部或腰部怕冷吗？(指上腹部，背部，腰部或膝关节等，有一处或多处怕冷)", "13.您比一般人耐受不了寒冷吗？(指比别人容易怕冬天或是夏天的冷空调，电扇等)",
                     "14.您容易患感冒吗？(指每年感冒次数)", "15.您没有感冒时会鼻塞，流鼻涕吗？", "16.您有口粘口腻，或睡眠打鼾？",
                     "17.您容易过敏吗？(指对药物，食物，气味，花粉或在季节交替，气候变化时)",
                     "18.您的皮肤容易起荨麻疹吗？(包括风团，风疹块，风疙瘩)", "19.您的皮肤在不知不觉中会出现青紫癫斑，皮下出血吗？(指皮肤在没有外伤的情况下出现青一块紫一块的情况)",
                     "20.您的皮肤一抓就红，并出现抓痕吗？(指被指甲或钝物或过后皮肤的反应)", "21.您皮肤或口唇干吗？", "22.您有肢体麻木或固定部位疼痛的感觉吗？",
                     "23.您面部或鼻部有油腻感或者油光发亮吗？(指脸上或鼻子)", "24.您面色或目眶晦暗，或出现褐色板块/斑点吗？",
                     "25.您有皮肤湿疹，疮疖吗？", "26.您感到口干咽燥，总想喝水吗？", "27.您感到口苦或嘴里有异味吗？(指口苦或口臭)", "28.您腹部肥大吗？(指腹部脂肪肥厚)",
                     "29.您吃(喝)凉的东西会感到不舒服或者怕吃(喝)凉的东西吗？(指不喜欢凉的食物，或吃了凉的食物后会不舒服)", "30.您有大便黏滞不爽，解不尽的感觉吗？(答辩容易粘在马桶或便坑壁上)",
                     "31.您容易大便干燥吗？", "32.您舌苔厚腻或有舌苔厚厚的感觉吗？(如果自我感觉不清楚可由调查员观察后填写)", "33.您舌下静脉淤紫或增粗吗？(可由调查人员辅助观察后填写)"]:
                Web_PO.eleClkByX(Web_PO.eleCommon2(ele, k), './/div[' + str(int(v) + 1) + ']/label')
            if k in ['气虚质', '阳虚质', '阴虚质', '痰湿质', '平和质', '湿热质', '血瘀质', '气郁质', '特禀质']:
                Web_PO.eleScrollViewByX(Web_PO.eleCommon2(ele, k), ".//div[4]/div/div/div")
                Web_PO.eleCheckboxLeftLabel2(Web_PO.eleDiv(ele, k, "../.."), ".//div[4]/div/div/div", v)
            elif k in ['填表日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()=' 保存']", "."), ".", 2)

    def __selfCareAbilityAssessmentInquiry(self, d_):
        # 老年人生活自理能力评估表
        ele = Web_PO.getSuperEleByX("//div[text()='老年人生活自理能力评估表']", "..")
        for k, v in d_['data'].items():
            if k in ['进餐：使用餐具将饭菜送入口、咀嚼、吞咽等活动']:
                d_tmp = {' 独立完成(0) ': 1, '/': 2, ' 需要协助，如切碎、搅拌食 物等(3) ': 3, ' 完全需要帮助(5) ': 4}
                s_class = Web_PO.eleGetAttrValueByX(Web_PO.eleP(ele, k, "../.."),
                                                    ".//div[2]/div[" + str(d_tmp[v]) + "]/label", "class")
                if s_class != 'el-checkbox el-checkbox--default is-checked':
                    Web_PO.eleClkByX(Web_PO.eleP(ele, k, "../.."), ".//div[2]/div[" + str(d_tmp[v]) + "]/label")
            if k in ['梳洗：梳头、洗脸、刷牙、剃须洗澡等活动']:
                d_tmp = {' 独立完成(0) ': 1, ' 能独立的洗头、梳头、洗脸、刷牙、剃须等；洗澡需要协助(1) ': 2, ' 在协助下和适当的时间内 能完成部分梳洗活动(3) ': 3,
                         ' 完全需要帮助(5) ': 4}
                s_class = Web_PO.eleGetAttrValueByX(Web_PO.eleP(ele, k, "../.."),
                                                    ".//div[2]/div[" + str(d_tmp[v]) + "]/label", "class")
                if s_class != 'el-checkbox el-checkbox--default is-checked':
                    Web_PO.eleClkByX(Web_PO.eleP(ele, k, "../.."),
                                     ".//div[2]/div[" + str(d_tmp[v]) + "]/label")
            if k in ['穿衣：穿衣裤、袜子、鞋子等活动']:
                d_tmp = {' 独立完成(0) ': 1, '/': 2, ' 需要协助，在适当的时间内完成部分穿衣(3) ': 3, ' 完全需要帮助(5) ': 4}
                s_class = Web_PO.eleGetAttrValueByX(Web_PO.eleP(ele, k, "../.."),
                                                    ".//div[2]/div[" + str(d_tmp[v]) + "]/label", "class")
                if s_class != 'el-checkbox el-checkbox--default is-checked':
                    Web_PO.eleClkByX(Web_PO.eleP(ele, k, "../.."),
                                     ".//div[2]/div[" + str(d_tmp[v]) + "]/label")
            if k in ['如厕：小便、大便等活动及自控']:
                d_tmp = {' 不需协助，可自控(0) ': 1, ' 偶尔失禁，但基本上能如厕或 使用便具(1) ': 2, ' 经常失禁，在很多提示和协助下尚能如厕或使用便具(5) ': 3,
                         ' 完全需要帮助(10) ': 4}
                s_class = Web_PO.eleGetAttrValueByX(Web_PO.eleP(ele, k, "../.."),
                                                    ".//div[2]/div[" + str(d_tmp[v]) + "]/label", "class")
                if s_class != 'el-checkbox el-checkbox--default is-checked':
                    Web_PO.eleClkByX(Web_PO.eleP(ele, k, "../.."),
                                     ".//div[2]/div[" + str(d_tmp[v]) + "]/label")
            if k in ['活动：站立、室内行走、上下楼梯、户外活动']:
                d_tmp = {' 独立完成所有活动(0) ': 1, ' 借助较小的外力或辅助装置 能完成站立、行走、上下楼梯等(1) ': 2, ' 借助较大的外力才能完成站立、行走，不能上下楼梯(5) ': 3,
                         ' 卧床不起，活动完全需要帮助(10) ': 4}
                s_class = Web_PO.eleGetAttrValueByX(Web_PO.eleP(ele, k, "../.."),
                                                    ".//div[2]/div[" + str(d_tmp[v]) + "]/label", "class")
                if s_class != 'el-checkbox el-checkbox--default is-checked':
                    Web_PO.eleClkByX(Web_PO.eleP(ele, k, "../.."),
                                     ".//div[2]/div[" + str(d_tmp[v]) + "]/label")
        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", "."), ".", 2)

        # 老年人自理能力评估查询

    def __depressionAssessmentQuery(self, d_):
        # 老年人抑郁评估查询
        ele = Web_PO.getSuperEleByX("//div[text()='老年抑郁量表（GDS）']", "..")
        for k, v in d_['data'].items():
            if k in [' 你对生活基本上满意吗？ ', " 你是否已经放弃了许多活动和兴趣？ ", " 你是否觉的生活空虚？ ", " 你是否常感到厌倦？ ", " 你觉的未来有希望吗？ ",
                     " 你是否因为脑子里有一些想法摆脱不掉而烦恼？ ",
                     " 你是否大部分时间精力充沛？ ", " 你是否害怕会有不幸的事落在你头上？ ",
                     " 你是否大部分时间感到幸福？ ",
                     " 你是否常感到孤立无援？ ",
                     " 你是否经常坐立不安，心烦意乱？ ",
                     " 你是否希望呆在家里而不愿意去做些新鲜事？ ",
                     " 你是否常常担心将来？ ",
                     " 你是否觉得记忆力比以前差？ ",
                     " 你觉得现在生活很惬意？ ",
                     " 你是否常感到心情沉重、郁闷？ ",
                     " 你是否觉得像现在这样生活毫无意义？ ",
                     " 你是否常为过去的事忧愁？ ",
                     " 你开始一件新的工作困难吗？ ",
                     " 你觉得生活充满活力吗？ ",
                     " 你是否觉得你的处境毫无希望？ ", " 你是否觉得大多数人比你强的多？ ",
                     " 你是否常为些小事伤心？ ",
                     " 你是否常觉得想哭？ ",
                     " 你集中精力困难吗？ ",
                     " 你早晨起的很快活吗？ ",
                     " 你希望避开聚会吗？ ",
                     " 你的头脑像往常一样清晰吗？ "
                     ]:
                if v == '是':
                    s_style = Web_PO.eleGetAttrValueByX(Web_PO.eleDiv(ele, k), ".//div[3]/div[1]/div", "style")
                    # print(s_style)
                    if 'display: none' in s_style:
                        Web_PO.eleClkByX(Web_PO.eleDiv(ele, k), ".//div[3]/div[1]")
                else:
                    s_style = Web_PO.eleGetAttrValueByX(Web_PO.eleDiv(ele, k), ".//div[3]/div[2]/div", "style")
                    # print(s_style)
                    if 'display: none' in s_style:
                        Web_PO.eleClkByX(Web_PO.eleDiv(ele, k), ".//div[3]/div[2]")
        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", "."), ".", 2)

    def __simpleIntelligenceTestQuery(self, d_):
        # 简易智力检查查询
        ele = Web_PO.getSuperEleByX("//div[text()=' 简易智力状态检查表 (MMSE) ']", "..")
        for k, v in d_['data'].items():
            #   "2.地点定向力 (5)": {"我们现在在哪个国家?": "0", "我们现在在哪个城市": "0", "我们现在在城市的哪一部分": "0", "我们现在在哪个建筑物": "0", "我们现在在第几层": "0"},
            #     "3.即刻回忆 (3)": {"皮球": "0", "国旗": "0", "树": "0"},
            #     "4.注意力与计算力 (5)": {"100减7等于? 93": "0", "100减7等于? 86": "0", "100减7等于? 79": "0", "100减7等于? 72": "0", "100减7等于? 65": "0"},
            #     "5.回忆能力 (3)": {"皮球": "0", "国旗": "0", "树": "0"},
            #     "6.命名能力 (2)": {"问:这是什么? 展示 (铅笔)": "0", "问:这是什么? 展示 (手表)": "0"},
            #     "7.语言重复能力 (1)": {"说:我现在让你重复我说的。准备好了吗？瑞雪兆丰年。你说一遍 ": "0"},
            #     "8.理解力 (3)": {"左手拿着这张纸": "0", "把它对折": "0", "把它放在你的右腿上": "0"},
            #     "9.阅读能力 (1)": {"闭上你的眼睛": "0"},
            #     "10.写的能力 (1)": {"说:写一个句子。": "0"},
            #     "11.画画的能力 (1)": {"说:照下图画。 ": "0"}
            if k in ["1.时间定力 (5)", "2.地点定向力 (5)", "6.命名能力 (2)", "7.语言重复能力 (1)", "10.写的能力 (1)", "11.画画的能力 (1)"]:
                for index, (k1, v1) in enumerate(v.items()):
                    if v1 == '1':
                        isDiv = Web_PO.eleIsEleExistByX(Web_PO.eleDiv(ele, k),
                                                        ".//div[2]/div[" + str(index + 1) + "]/div[2]/div[1]/div")
                        if isDiv == False:
                            Web_PO.eleClkByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div[" + str(index + 1) + "]/div[2]/div[1]")
                    else:
                        isDiv = Web_PO.eleIsEleExistByX(Web_PO.eleDiv(ele, k),
                                                        ".//div[2]/div[" + str(index + 1) + "]/div[2]/div[2]/div")
                        if isDiv == False:
                            Web_PO.eleClkByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div[" + str(index + 1) + "]/div[2]/div[2]")
            if k in [
                "3.即刻回忆 (3)", "4.注意力与计算力 (5)", "5.回忆能力 (3)", "8.理解力 (3)", "9.阅读能力 (1)"]:
                for index, (k1, v1) in enumerate(v.items()):
                    if v1 == '1':
                        isDiv = Web_PO.eleIsEleExistByX(Web_PO.eleDiv(ele, k),
                                                        ".//div[2]/div[" + str(index + 2) + "]/div[2]/div[1]/div")
                        if isDiv == False:
                            Web_PO.eleClkByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div[" + str(index + 2) + "]/div[2]/div[1]")
                    else:
                        isDiv = Web_PO.eleIsEleExistByX(Web_PO.eleDiv(ele, k),
                                                        ".//div[2]/div[" + str(index + 2) + "]/div[2]/div[2]/div")
                        if isDiv == False:
                            Web_PO.eleClkByX(Web_PO.eleDiv(ele, k),
                                             ".//div[2]/div[" + str(index + 2) + "]/div[2]/div[2]")

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", "."), ".", 2)

    # todo 2.7.2  基本公卫 - 老年人健康管理 - 老年人专项登记

    def phs_snr_special_query(self, d_):

        # 老年人专项登记 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['出生日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div/div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div/div[2]/input", v[1])
                elif k in ['档案状态', '性别', '是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)
        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_snr_special_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        # 缩小页面，获取所有的字段
        Web_PO.zoom(50)
        # 获取字段列表
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        print(l_field)  # ['姓名', '身份证号', '出生日期', '电话', '居住地址', '性别', '随访医生', '空腹血糖', '随访方式', '随访日期', '随访评价结果', '下次随访日期', '数据源', '操作']
        Web_PO.zoom(100)

        # 获取值列表
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        print(l_value)
        s_class_warn = Web_PO.eleGetAttrValueByX(ele2, ".//td[3]/div/span", "class")
        # print(s_class_warn) # warn-tag warn-red
        l_value[2] = s_class_warn
        print(l_value)
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        elif "详情" in l_value:
            i_row = len(List_PO.split(l_value, "详情", 0))
            l_value = List_PO.dels(l_value, "详情")
            l_group = List_PO.group(l_value, i_row)
        print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        if d_1 == {}:
            print("warning, 未匹配记录, 请检查字段是否存在！")
        else:
            print("ok, 匹配到", d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key
    def _phs_snr_special_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        # 缩小页面，获取所有的字段
        Web_PO.zoom(50)
        # 获取字段列表
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['姓名', '年龄', '性别', '身份证号', '家庭住址', '联系电话', '操作']
        Web_PO.zoom(100)

        # 获取值列表
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        # print(l_value)
        if varOperation in l_value:
            i_row = len(List_PO.split(l_value, varOperation, 0))
            l_value = List_PO.dels(l_value, varOperation)
            l_group = List_PO.group(l_value, i_row)
        # print(l_group)  # [['女-1', '0', '女', '340203202407017263', '罗峰街道文化区社区居民委员会1', '1']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)
        # if d_1 == {}:
        #     print("warning, 未匹配记录, 请检查字段是否存在！")
        # else:
        #     print("ok, 匹配到", d_1)
        max_key = max(d_1, key=d_1.get)
        return max_key

    def phs_snr_special_operation(self, d_):

        # 老年人专项登记 - 操作

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_snr_special_operation('专项登记', d_['option'])) + "]", ".")
                Web_PO.eleClkByX(ele3, ".", 2)
            elif d_['operate'] == '批量登记':
                if d_['option'] == 'all':
                    # 全选
                    ele = Web_PO.getSuperEleByX("//thead", ".")
                    Web_PO.eleClkByX(ele, ".//tr/th[1]/div/label", 1)
                elif isinstance(d_['option'], dict):
                    # 单选或多选
                    Web_PO.clkByX("//tbody/tr[" + str(self._phs_snr_special_operation('专项登记', d_['option'])) + "]/td[1]/div", 2)
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='批量登记']", ".."), ".", 2)
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='取消']", ".."), ".", 2)
                # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确定']", ".."), ".", 2)

            elif d_['operate'] == '专项登记':
                ele = Web_PO.getSuperEleByX("//form", ".")
                for k, v in d_['data'].items():
                    if k in ['生活赡养']:
                        Web_PO.eleCheckboxRightLabel(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                    elif k in ['护理情况']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input",  v)
                    elif k in ['登记日期']:
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)
                Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
            else:
                print("error, 无法操作!")
            self.logger.info("点击" + str(d_))
        except:
            self.logger.error(str(d_) + "失败！")



    # todo 2.7.3  基本公卫 - 老年人健康管理 - 老年人专项管理

    def phs_snr_lnrfiles_query(self, d_):

        # 老年人专项管理 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['性别', '是否仅查询机构', '档案状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_snr_lnrfiles_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '性别', '年龄', '身份证号', '联系电话', '现住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        # print(l_value)
        l_value = List_PO.dels(l_value, varOperation)
        l_value = List_PO.dels(l_value, '新增评估')
        # print(l_value)
        l_group = (List_PO.group(l_value, 6))
        # print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_snr_lnrfiles_operation(self, d_):

        # 老年人专项管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                if d_['operate'] == '详情':
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='"+d_['operate']+"'])[position()=" +
                         str(self._phs_snr_lnrfiles_operation('详情\n体检记录\n新增评估', d_['option'])) + "]", "..")
                    Web_PO.eleClkByX(ele3, ".", 2)
                elif d_['operate'] == '体检记录':
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='"+d_['operate']+"'])[position()=" + str(
                        self._phs_snr_lnrfiles_operation('详情\n体检记录\n新增评估', d_['option'])+1) + "]", ".")
                    Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '详情':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='编辑']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in ['生活赡养']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//td[2]/div/div/div/label", v)
                        elif k in ['护理情况']:
                            Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//td[4]/div/div/div/div/div/input",
                                                v)
                        elif k in ['登记日期']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//td[4]/div/div/div/input", v)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '新增体验':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增体检 ']", ".."), ".", 2)
                    # 体检表
                    self.__tjb(d_)

                elif d_['operate'] == '新增中医药健康管理':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div/div[1]/div/div/div/div[3]', 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增评估 ']", ".."), ".", 2)
                    # 老年人中医药健康管理服务记录表
                    self.__chineseMedicineHealthManagementServiceRecord(d_)

                elif d_['operate'] == '新增老年人生活自理能力评估表':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div/div[1]/div/div/div/div[4]', 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增评估 ']", ".."), ".", 2)
                    # 老年人生活自理能力评估表
                    self.__selfCareAbilityAssessmentInquiry(d_)

                elif d_['operate'] == '新增老年人忧郁评估表':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div/div[1]/div/div/div/div[5]', 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增评估 ']", ".."), ".", 2)
                    # 老年人抑郁评估查询
                    self.__depressionAssessmentQuery(d_)

                elif d_['operate'] == '新增简易智力检查':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div/div[1]/div/div/div/div[6]', 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增评估 ']", ".."), ".", 2)
                    # 简易智力检查查询
                    self.__simpleIntelligenceTestQuery(d_)



            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))


    # todo 2.7.4  基本公卫 - 老年人健康管理 - 本年度未体检

    def phs_snr_unexamined_query(self, d_):

        # 本年度未体检 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",
                                        v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",
                                        v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_snr_unexamined_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        # print(l_field)  # ['姓名', '性别', '年龄', '身份证号', '联系电话', '现住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        # print(l_value)
        l_value = List_PO.dels(l_value, varOperation)
        l_value = List_PO.dels(l_value, '新增')
        # print(l_value)
        l_group = (List_PO.group(l_value, 6))
        print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_snr_unexamined_operation(self, d_):

        # 本年度未体检 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                if d_['operate'] == '新增':
                    ele3 = Web_PO.getSuperEleByX("(//span[text()='"+d_['operate']+"'])[position()=" +
                         str(self._phs_snr_unexamined_operation('新增', d_['option'])) + "]", "..")
                    Web_PO.eleClkByX(ele3, ".", 2)

            else:
                if d_['operate'] == '新增':
                    # 体检表
                    self.__tjb(d_)

                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", "."), ".", 2)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.7.5  基本公卫 - 老年人健康管理 - 老年人中医体质辨识

    def phs_snr_chmedicine_query(self, d_):

        # 老年人中医体质辨识 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['评估日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",
                                        v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",
                                        v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_snr_chmedicine_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '性别', '年龄', '身份证号', '联系电话', '现住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)  # [['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2024-07-09', '村卫生室', '2024-10-24', '2024-11-30', '详情\n评估\n随访'], ['37068500100100104', '刘长春', '', '110101199001012256', '35', '男', '13818882732', '罗峰街道文化区社区居民委员会发', '2025-01-14', '卫健委', '', '', '详情\n评估\n随访']]

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_snr_chmedicine_operation(self, d_):

        # 老年人中医体质辨识 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='"+d_['operate']+"'])[position()=" +
                     str(self._phs_snr_chmedicine_operation('查看\n编辑\n删除', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='否'])[last()]", "."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='是'])[last()]", "."), ".", 2)
            else:
                if d_['operate'] == '查看':
                    ...

                elif d_['operate'] == '编辑':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='修改']", "."), ".", 2)
                    # 老年人中医药健康管理服务记录表
                    self.__chineseMedicineHealthManagementServiceRecord(d_)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.7.5  基本公卫 - 老年人健康管理 - 老年人自理能力评估查询

    def phs_snr_selfcareassess_query(self, d_):

        # 老年人自理能力评估查询 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期', '评估日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",
                                        v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",
                                        v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_snr_selfcareassess_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '性别', '年龄', '身份证号', '联系电话', '现住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_snr_selfcareassess_operation(self, d_):

        # 老年人自理能力评估查询 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(self._phs_snr_selfcareassess_operation('详情\n编辑\n删除', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='否'])[last()]", "."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='是'])[last()]", "."), ".", 2)
            else:
                if d_['operate'] == '详情':
                    ...

                elif d_['operate'] == '编辑':
                    # 老年人自理能力评估查询
                    self.__selfCareAbilityAssessmentInquiry(d_)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.7.5  基本公卫 - 老年人健康管理 - 老年人抑郁评估查询

    def phs_snr_depressed_query(self, d_):

        # 老年人抑郁评估查询 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期', '评估日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",
                                        v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",
                                        v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_snr_depressed_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '性别', '年龄', '身份证号', '联系电话', '现住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_snr_depressed_operation(self, d_):

        # 老年人抑郁评估查询 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_snr_depressed_operation('详情\n编辑\n删除', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='否'])[last()]", "."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='是'])[last()]", "."), ".", 2)
            else:
                if d_['operate'] == '详情':
                    ...

                elif d_['operate'] == '编辑':
                    # 老年人抑郁评估查询
                    self.__depressionAssessmentQuery(d_)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))


    # todo 2.7.8  基本公卫 - 老年人健康管理 - 简易智力检查查询

    def phs_snr_intelligence_query(self, d_):

        # 简易智力检查查询 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期', '评估日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",
                                        v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",
                                        v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_snr_intelligence_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '性别', '年龄', '身份证号', '联系电话', '现住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_snr_intelligence_operation(self, d_):

        # 简易智力检查查询 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_snr_intelligence_operation('详情\n编辑\n删除', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='取消'])[last()]", "."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='确定'])[last()]", "."), ".", 2)
            else:
                if d_['operate'] == '详情':
                    ...

                elif d_['operate'] == '编辑':
                    # 简易智力检查查询
                    self.__simpleIntelligenceTestQuery(d_)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.8.1  基本公卫 - 健康体检 - 体检登记

    def phs_healthExamination_tjregister_query(self, d_):

        # 体检登记 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['建档日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",
                                        v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",
                                        v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
                elif k in ['人群分类']:
                    Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div/div/label", v)
                    # /html/body/div[1]/div/div[3]/section/div/main/div[1]/form/div/div[9]/div/div/div/label[3]
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_healthExamination_tjregister_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '性别', '年龄', '身份证号', '联系电话', '现住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_healthExamination_tjregister_operation(self, d_):

        # 体检登记 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_healthExamination_tjregister_operation('新增', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '新增':
                    # 体检表
                    self.__tjb(d_)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.8.2  基本公卫 - 健康体检 - 体检记录

    def phs_healthExamination_tjrecord_query(self, d_):

        # 体检记录 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['出生日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_healthExamination_tjrecord_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '年龄', '身份证号', '性别', '联系电话', '人群分类', '居住住址', '体检日期', '体检医生', '体检来源', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)
        for i in l_group:
            del i[5]
            l_5 = i[5].split("\n")
            # print(l_5)
            for j in range(len(l_5)):
                if l_5[j] in i:
                    i.remove(l_5[j])
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_healthExamination_tjrecord_operation(self, d_):

        # 体检记录 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_healthExamination_tjrecord_operation('详情\n编辑\n删除', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='否'])[last()]", "."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='确定'])[last()]", "."), ".", 2)
            else:
                if d_['operate'] == '详情':
                    ...

                elif d_['operate'] == '编辑':
                    # 国家基本公共卫生服务项目健康体检表
                    self.__tjb(d_)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))




    # todo 2.8.3  基本公卫 - 健康体检 - 未体检人员

    def phs_healthExamination_tjunexam_query(self, d_):

        # 未体检人员 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['未体检日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                if k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[1]/div[1]/div/div/input",
                                        v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",
                                        v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
                elif k in ['人群分类']:
                    Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div/div/label", v)
            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_healthExamination_tjunexam_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '性别', '年龄', '身份证号', '联系电话', '现住址', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)
        for i in l_group:
            del i[1]
            l_1 = i[1].split("\n")
            # print(l_5)
            for j in range(len(l_1)):
                if l_1[j] in i:
                    i.remove(l_1[j])
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_healthExamination_tjunexam_operation(self, d_):

        # 未体检人员 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_healthExamination_tjunexam_operation('新增', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '新增':
                    # 体检表
                    self.__tjb(d_)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.9.2  基本公卫 - 肺结核患者管理 - 肺结核登记

    def phs_tuberculosis_fjhregister_query(self, d_):

        # 肺结核登记 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '联系电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_tuberculosis_fjhregister_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '年龄', '性别', '身份证号', '家庭住址', '联系电话', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_tuberculosis_fjhregister_operation(self, d_):

        # 肺结核登记 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_tuberculosis_fjhregister_operation('新增登记及第一次入户随访', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '新增登记及第一次入户随访':
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in ["随访日期", "下次随访日期"]:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
                        elif k in ['随访方式','痰菌情况']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/label", v)
                        elif k in ['耐药情况']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                        elif k in ['患者类型']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/label", v)
                        elif k in ['症状及体征']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div/input", i['其他'])
                        elif k in ['用药']:
                            for k1, v1 in v.items():
                                if k1 in ['化疗方案']:
                                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k1), ".//input", v1)
                                elif k1 in ['用法']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/label", v1)
                                elif k1 in ['药品剂型']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/label", v1)
                        elif k in ['督导人员选择']:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/label", v, ".//div[2]/div/div/div[2]/div/div/input")
                        elif k in ['家庭居住环境']:
                            for k1, v1 in v.items():
                                if k1 in ['单独的居室']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/label", v1)
                                elif k1 in ['通风情况']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/label", v1)
                        #  '生活方式评估':{'吸烟':[1,3],'饮酒':[4,6]},
                        elif k in ['生活方式评估']:
                            for k1, v1 in v.items():
                                if k1 in ['吸烟']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div[1]/div/div/input", v1[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[3]/div/div[1]/div/div/input", v1[1])
                                elif k1 in ['饮酒']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[5]/div/div[1]/div/div/input", v1[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[6]/div/div[1]/div/div/input", v1[1])
                        elif k in ['健康教育及培训']:
                            for k1, v1 in v.items():
                                if k1 in ['取药地点、时间']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1[0])
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k1), ".//div[3]/div/div/div/input", v1[1])
                                elif k1 in ['服药记录卡的填写']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[5]/div/div/div/label", v1)
                                elif k1 in ['服药方法及药品存放', '不规律服药危害', '治疗期间复诊查痰', '生活习惯及注意事项']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/label", v1)
                                elif k1 in ['肺结核治疗疗程', '服药后不良反应及处理', '外出期间如何坚持服药', '密切接触者检查']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/label", v1)
                        elif k in ['随访医生']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/div/input",  v)
                        elif k in ['患者（家属）签字']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)

                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))




    # todo 2.9.3  基本公卫 - 肺结核患者管理 - common
    def __tuberculosisFollowup(self, d_):
        # 肺结核入户随访
        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in ["随访日期", "下次随访日期"]:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
            elif k in ['随访方式', '痰菌情况']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/label", v)
            elif k in ['耐药情况']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in ['患者类型']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/label", v)
            elif k in ['症状及体征']:
                Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/label", v)
                for i in v:
                    if isinstance(i, dict):
                        if '其他' in i:
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k),
                                                      ".//div[2]/div[2]/div[2]/div/div/div/input", i['其他'])
            elif k in ['用药']:
                for k1, v1 in v.items():
                    if k1 in ['化疗方案']:
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k1), ".//input", v1)
                    elif k1 in ['用法']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/label", v1)
                    elif k1 in ['药品剂型']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/label", v1)
            elif k in ['督导人员选择']:
                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/label", v,
                                                 ".//div[2]/div/div/div[2]/div/div/input")
            elif k in ['家庭居住环境']:
                for k1, v1 in v.items():
                    if k1 in ['单独的居室']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/label", v1)
                    elif k1 in ['通风情况']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/label", v1)
            #  '生活方式评估':{'吸烟':[1,3],'饮酒':[4,6]},
            elif k in ['生活方式评估']:
                for k1, v1 in v.items():
                    if k1 in ['吸烟']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div[1]/div/div/input", v1[0])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[3]/div/div[1]/div/div/input", v1[1])
                    elif k1 in ['饮酒']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[5]/div/div[1]/div/div/input", v1[0])
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[6]/div/div[1]/div/div/input", v1[1])
            elif k in ['健康教育及培训']:
                for k1, v1 in v.items():
                    if k1 in ['取药地点、时间']:
                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1[0])
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k1), ".//div[3]/div/div/div/input", v1[1])
                    elif k1 in ['服药记录卡的填写']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[5]/div/div/div/label", v1)
                    elif k1 in ['服药方法及药品存放', '不规律服药危害', '治疗期间复诊查痰', '生活习惯及注意事项']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/label", v1)
                    elif k1 in ['肺结核治疗疗程', '服药后不良反应及处理', '外出期间如何坚持服药', '密切接触者检查']:
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/label", v1)
            elif k in ['随访医生']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/div/input",
                                    v)
            elif k in ['患者（家属）签字']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

    # todo 2.9.3  基本公卫 - 肺结核患者管理 - 肺结核管理

    def phs_tuberculosis_fjhfiles_query(self, d_):

        # 肺结核管理 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态', '停止治疗原因', '随访提醒分类', '管理状态', '患者类型', '痰菌情况']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['上次随访日期','登记日期','随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/input", v[1])
                elif k in ['登记时年龄']:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[1]/div/div/div/input", v[0])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v[1])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_tuberculosis_fjhfiles_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        print(l_field)  # ['姓名', '提醒', '性别', '登记时年龄', '联系电话', '上次随访日期', '下次随访日期', '登记日期', '登记机构', '患者类型', '菌痰情况', '停止治疗原因', '身份证号', '家庭住址', '管理状态', '操作']
        Web_PO.zoom(100)

        # # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        for i in l_group:
            i.pop(2)
            i.pop(2)
        # print(l_group)

        l_class_warn = Web_PO.eleGetAttrValueByXs(ele2, ".//td[2]/div/div", "style")
        print(l_class_warn)  # background: rgb(223, 57, 38); width: 16px; height: 16px;
        for i in range(len(l_class_warn)):
            l_class_warn[i] = l_class_warn[i].split("background-color: ")[1].split(";")[0]
        # print(l_class_warn)  # ['red', 'red']

        for i in range(len(l_group)):
            l_group[i][1] = l_class_warn[i]
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_tuberculosis_fjhfiles_operation(self, d_):

        # 肺结核管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_tuberculosis_fjhfiles_operation('访视记录', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '访视记录':
                    # 肺结核患者第一次入户随访记录表
                    self.__tuberculosisFollowup(d_)
                elif d_['operate'] == '入户随访之编辑':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='修改']", ".."), ".", 2)
                    # 肺结核患者第一次入户随访记录表
                    self.__tuberculosisFollowup(d_)
                elif d_['operate'] == '入户随访之删除':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='删除']", "../.."), ".", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='确定'])[last()]", ".."), ".", 2)

                elif d_['operate'] == '历次随访之新增随访':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div/div[2]/div/div[1]/div[2]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()=' 新增随访 ']", ".."), ".", 2)

                    # # 肺结核患者随访服务记录表
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in ["随访日期", '下次随访时间']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
                        elif k in ['治疗月序']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                        elif k in ['督导人员选择']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/label", v)
                        elif k in ['随访方式']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/label", v)
                        elif k in ['症状及体征']:
                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k),".//div[2]/div[1]/div/div/div/div/label", v)
                            for i in v:
                                if isinstance(i, dict):
                                    if '其他' in i:
                                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k),".//div[2]/div[2]/div[2]/div/div/div/input", i['其他'])
                        elif k in ['生活方式评估']:
                            for k1, v1 in v.items():
                                if k1 in ['吸烟']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1),".//div[2]/div/div[1]/div/div/input", v1[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1),".//div[3]/div/div[1]/div/div/input", v1[1])
                                elif k1 in ['饮酒']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1),".//div[5]/div/div[1]/div/div/input", v1[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1),".//div[6]/div/div[1]/div/div/input", v1[1])
                        elif k in ['用药']:
                            for k1, v1 in v.items():
                                if k1 in ['化疗方案']:
                                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k1), ".//input", v1)
                                elif k1 in ['用法']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/label", v1)
                                elif k1 in ['药品剂型']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/label",v1)
                                elif k1 in ['漏服药次数']:
                                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div[1]/div/div/input", v1)
                        elif k in ['药物不良反应']:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/label", v, ".//div[2]/div/div[1]/div/div/div[2]/div/div[1]/input")
                        elif k in ['并发症或合并症']:
                                Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/label", v, ".//div[3]/div/div/div[2]/div/div/input")
                        elif k in ['转诊']:
                            for k1, v1 in v.items():
                                if k1 in ['转诊']:
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div[1]/div[1]/div/div/div/label", v1)
                                elif k1 in ['机构及科别']:
                                    if v['转诊'] == '有':
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                                elif k1 in ['原因']:
                                    if v['转诊'] == '有':
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[3]/div/div/div/input", v1)
                                elif k1 in ['2周内随访,随访结果']:
                                    if v['转诊'] == '有':
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/input", v1)
                        elif k in ['处理意见']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//input", v)
                        elif k in ['是否停止治疗']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)

                        elif k in ['停止治疗及原因']:
                            if d_['data']['是否停止治疗'] == '是':
                                for k1,v1 in v.items():
                                    if k1 in ['出现停止治疗时间']:
                                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                                    elif k1 in ['停止治疗原因']:
                                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div[1]/label", v1)
                        elif k in ['全程管理情况']:
                            if d_['data']['是否停止治疗'] == '是':
                                for k1, v1 in v.items():
                                    if k1 in ['应访视患者', '患者在疗程,应服药']:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/input", v1)
                                    elif k1 in ['实际访视', '实际服药']:
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/input", v1)
                                    elif k1 in ['评估医生签名']:
                                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div/div/input",  v1)
                        elif k in ['随访医生签名']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/div/input",  v)
                        elif k in ['患者（家属）签字']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)

                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

                    if d_['data']['是否停止治疗'] == '是':
                        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确定']", ".."), ".", 2)
                        # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()=' 取消 ']", ".."), ".", 2)

                elif d_['operate'] == '历次随访之结案':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div/div[2]/div/div[1]/div[2]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='结案']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//div[text()='提示']", "../..")
                    for k, v in d_['data'].items():
                        if k in ["结案原因："]:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[1]/label", v, ".//div[2]/input")
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确定']", ".."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()=' 取消 ']", ".."), ".", 2)


            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))


    # todo 2.10.2  基本公卫 - 残疾人健康管理 - common
    def __disabled_register(self, d_):
        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in ['残疾人证号 ', ' 赡养老人数 ', '培训经历 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            if k in ["致残时间 "]:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
            elif k in ['自理程度 ']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input",  v)
            elif k in [' 生活来源 ', ' 管理等级 ']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/div/div/input",  v)
            elif k in [' 当前状态 ']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input",  v)
            elif k in [' 监护人 ', ' 功能障碍 ',' 特长 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/input", v)
            elif k in [' 抚养子女数 ', '备注 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
            elif k in [' 主要情况 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[8]/div/div/div/input", v)
            elif k in [' 与残疾人关系 ']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[8]/div/div/div/div/div/input",  v)
            elif k in [' 致残原因 ', ' 主要残疾类型 ', ' 多重残疾类型 ']:
                Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div", v)
            elif k in [' 残疾程度 ']:
                Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div", v)
            elif k in [' 登记人']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div/input",  v)
            elif k in [' 登记时间']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[4]/div/input", v)
            elif k in [' 居民（家属）签字']:
                Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[6]/div/input", v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

    # todo 2.10.2  基本公卫 - 残疾人健康管理 - 残疾人登记

    def phs_disabled_cjrregister_query(self, d_):

        # 残疾人登记 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '联系电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_disabled_cjrregister_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '年龄', '性别', '身份证号', '家庭住址', '联系电话', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_disabled_cjrregister_operation(self, d_):

        # 残疾人登记 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_disabled_cjrregister_operation('新增专项登记', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '新增专项登记':
                    self.__disabled_register(d_)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.10.3  基本公卫 - 残疾人健康管理 - 残疾人管理

    def phs_disabled_cjrfiles_query(self, d_):

        # 残疾人管理 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '残疾人证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态', '登记机构', '管理状态', '管理等级', '主要残疾类型', '随访提醒分类']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['上次随访日期','登记日期','随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                elif k in ['登记时年龄']:
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)
                elif k in ['现住址']:
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), "./div[1]/div/div/div/div/input",  v[0])
                        Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), "./div[2]/div/div/div/div/input",  v[1])
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), "./div[3]/div/div/input", v[2])

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_disabled_cjrfiles_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['姓名', '性别', '提醒', '登记年龄', '联系电话', '上次随访日期', '下次随访日期', '管理等级', '监护人', '登记日期', '登记机构', '残疾证号', '身份证号', '家庭住址', '主要残疾类型', '管理状态', '操作']
        Web_PO.zoom(100)

        # # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        # print(l_group)

        l_tmp = []
        qty = Web_PO.eleGetCountByXs(ele2, './/tr')
        for i in range(qty):
            if Web_PO.eleIsEleExistByX(ele2, ".//tr["+ str(i+1)+ "]/td[3]/div/div/div"):
                l_class_warn = Web_PO.eleGetAttrValueByXs(ele2, ".//td[3]/div/div/div", "style")
                l_tmp.append(l_class_warn[0].split("background-color: ")[1].split(";")[0])
            else:
                l_tmp.append("0")
        # print(l_tmp)

        for i in range(len(l_group)):
            if l_tmp[i] == "0":
                l_group[i].pop(2)
                l_group[i][2] = 'noColor'
            else:
                l_group[i].pop(2)
                l_group[i].pop(2)
                l_group[i][2] = l_tmp[i]
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_disabled_cjrfiles_operation(self, d_):

        # 残疾人管理 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_disabled_cjrfiles_operation('访视记录', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '专项登记之编辑':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='修改']", ".."), ".", 2)
                    self.__disabled_register(d_)

                elif d_['operate'] == '随访记录之新增':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[2]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增随访记录']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in [' 主要残疾 ', ' 多重残疾 ',]:
                            Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div", v)
                        elif k in [' 残疾程度 ', ' 此次随访分类 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div", v)
                        elif k in [' 随访方式 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div", v)
                        elif k in [' 体征 ']:
                            for k1, v1 in v.items():
                                if k1 in [' 体征 ']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div[1]/div/div/input", v1[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div[2]/div/div/input", v1[1])
                                elif k1 in ['体重', '心率']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//input", v1)
                                elif k1 in ['其他']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[5]/div/div/input", v1)
                        elif k in [' 就业情况 ']:
                            for k1, v1 in v.items():
                                if k1 in [' 康复训练情况 ']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//input", v1)
                                elif k1 in [' 功能训练 ']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div[1]/div/div/input", v1[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div[2]/div/div/input", v1[1])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div[3]/div/div/input", v1[2])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[2]/div[4]/div/div/input", v1[3])
                                elif k1 in [' 训练场地 ', ' 遵医行为 ']:
                                    Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div", v1)
                                elif k1 in [' 训练效果 ']:
                                    Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/div", v1)
                                elif k1 in [' 康复目标 ']:
                                    Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k1), ".//div[2]/div/div/div/div", list(v1.keys())[0])
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[3]/div/div/div/input", v1[list(v1.keys())[0]])
                        elif k in [' 转诊 ']:
                            for k1, v1 in v.items():
                                if k1 in [' 转诊原因 ']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//input", v1)
                                elif k1 in [' 转诊机构及科室 ']:
                                    Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k1), ".//div[4]/div/div/div/input", v1)
                        elif k in [" 随访日期 "]:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/input", v)
                        elif k in [' 下次随访时间 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
                        elif k in [' 随访医生签名 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/div/input",  v)
                        elif k in [' 患者(家属)签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '随访记录之引入上一次数据':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[2]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上一次数据']", ".."), ".", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '随访记录之结案':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[2]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='结案']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//span[text()='结案原因：']", "..")
                    for k, v in d_['data'].items():
                        if k in ["结案原因："]:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div/label", v, ".//div[2]/div/textarea")

                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", ".."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='取 消']", ".."), ".", 2)
                    # Web_PO.eleClkByX(ele, "div[3]/button[1]", 2)

                elif d_['operate'] == '康复需求登记之新增':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[3]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增康复需求登记']", ".."), ".", 2)

                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in [' 听力语言 ', ' 视力 ', ' 肢体 ', ' 智力 ', ' 是否精神功能训练 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v)
                        elif k in [' 康复医疗服务 ', ' 听力语言器具名称 ', ' 视力辅助器具 ', ' 肢体器具名称 ', ' 智力服务项目 ', ' 精神器具名称 ', ' 知识普及 ',' 心理服务 ', ' 转介服务 ']:
                            Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div", v)
                        elif k in [' 听力服务项目 ', ' 视力服务项目 ', ' 肢体服务项目 ', ' 智力器具名称 ', ' 精神服务项目 ']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div")
                            Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div", v)
                        elif k in [' 其他需求 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//input", v)
                        elif k in  [' 登记人 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/div/div/input",  v)
                        elif k in [' 登记时间 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                        elif k in [' 居民签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)
                        elif k in [' 家属签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[7]/div/div/div/input", v)

                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '康复需求登记之引入上一次数据':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[3]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上一次数据']", ".."), ".", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '康复需求登记之结案':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[3]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='结案']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//span[text()='结案原因：']", "..")
                    for k, v in d_['data'].items():
                        if k in ["结案原因："]:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div/label", v, ".//div[2]/div/textarea")

                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", ".."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='取 消']", ".."), ".", 2)
                    # Web_PO.eleClkByX(ele, "div[3]/button[1]", 2)

                elif d_['operate'] == '健教记录之新增':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[4]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增健教记录']", ".."), ".", 2)

                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in [' 教育内容 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/textarea", v)
                        elif k in [' 居民签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
                        elif k in [' 家属签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                        elif k in [' 健教医生 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/div/div/input",  v)
                        elif k in [' 健教日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                        elif k in [' 登记日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[7]/div/div/div/input", v)

                        elif k in [' 登记人 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/div/div/input",  v)

                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '健教记录之引入上一次数据':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[4]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上一次数据']", ".."), ".", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '健教记录之结案':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[4]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='结案']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//span[text()='结案原因：']", "..")
                    for k, v in d_['data'].items():
                        if k in ["结案原因："]:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div/label", v, ".//div[2]/div/textarea")

                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", ".."), ".", 2)
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='取 消']", ".."), ".", 2)
                    # Web_PO.eleClkByX(ele, "div[3]/button[1]", 2)

                elif d_['operate'] == '服务登记之新增':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[5]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增服务登记']", ".."), ".", 2)

                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in [' 是否视力功能训练 ', ' 是否听力语言训练 ', ' 是否肢体功能训练 ', ' 是否智力功能训练 ', ' 是否精神功能训练 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v)
                        elif k in [' 康复情况 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div", v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[19]/div[2]/div/div/div/div/div[3]/label
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[19]/div[2]/div/div/div/div/div[3]/label
                        elif k in [' 康复医疗服务信息 ', ' 听力辅助器具 ', ' 视力辅助器具 ', ' 肢体辅助器具 ', ' 智力功能训练 ', ' 精神功能训练 ', ' 其他器具服务 ', ' 知识普及 ', ' 心理服务 ',
                                   ' 转介服务 ', ' 服务方式 ']:
                            Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div", v)

                        elif k in [' 视力功能训练 ', ' 听力功能项目 ', ' 肢体功能训练 ', ' 智力辅助器具 ', ' 精神器具名称 ', ' 下次服务方式 ']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div")
                            Web_PO.eleCheckboxLeftLabel2(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div", v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[22]/div[2]/div/div[3]/div/div/div/div[1]/label

# /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[3]/div[2]/div[3]/div/div/div/div[2]/label
# /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[20]/div[2]/div[3]/div/div/div/div[2]/label

                        elif k in [' 服务场所 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div", v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[22]/div[2]/div/div[3]/div/div/div/div[1]/label
                        elif k in [' 其他服务 ', ' 下次服务计划 ', ' 服务备注 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//input", v)
                        elif k in [' 服务医生 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[7]/div/div/div/div/div/input",  v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[22]/div[2]/div/div[7]/div/div/div/div/div/input
                        elif k in [' 服务日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[22]/div[2]/div/div[1]/div/div/div/input
                        elif k in [' 下次服务日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[22]/div[2]/div/div[5]/div/div/div/input
                        elif k in [' 居民签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[23]/div[2]/div/div[1]/div/div/div/input
                        elif k in [' 家属签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[23]/div[2]/div/div[3]/div/div/div/input

                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '服务登记之引入上一次数据':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[5]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上一次数据']", ".."), ".", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '服务登记之结案':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[3]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='结案']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//span[text()='结案原因：']", "..")
                    for k, v in d_['data'].items():
                        if k in ["结案原因："]:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div/label", v,
                                                             ".//div[2]/div/textarea")

                        # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", ".."), ".", 2)
                        # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='取 消']", ".."), ".", 2)
                        # Web_PO.eleClkByX(ele, "div[3]/button[1]", 2)

                elif d_['operate'] == '服务评估之新增':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[6]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增服务评估']", ".."), ".", 2)

                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in [' 评估年度 ', ' 残疾人或监护人 ', ' 下年度服务建议 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/input", v)
                        elif k in [' 康复满意程度 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div", v)
                        elif k in [' 服务医生 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/div/input",  v)
                        elif k in [' 下次服务日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                        elif k in [' 服务效果 ']:
                            Web_PO.eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div", v)
                        elif k in [' 评估人 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/div/div/input",  v)
                        elif k in [' 评估日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                        elif k in [' 登记人 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/div/div/input",  v)
                        elif k in [' 登记日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[7]/div/div/div/input", v)
                        elif k in [' 居民签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[1]/div/div/div/input", v)
                        elif k in [' 家属签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '服务评估之引入上一次数据':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[6]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='引入上一次数据']", ".."), ".", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                elif d_['operate'] == '服务评估之结案':
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[6]", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='结案']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//span[text()='结案原因：']", "..")
                    for k, v in d_['data'].items():
                        if k in ["结案原因："]:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon2(ele, k), ".//div[1]/div/label", v, ".//div[2]/div/textarea")

                        # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", ".."), ".", 2)
                        # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='取 消']", ".."), ".", 2)
                        # Web_PO.eleClkByX(ele, "div[3]/button[1]", 2)


            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.11.1  基本公卫 - 严重精神障碍健康管理 - 严重精神障碍登记

    def phs_memtalDisorder_jsregister_query(self, d_):

        # 严重精神障碍登记 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号', '联系电话']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_memtalDisorder_jsregister_operation(self, varOperation, d_option):

        # 获取字段和xpath字典
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//thead", "."), ".//div")
        Web_PO.zoom(100)
        print(l_field)  # ['姓名', '年龄', '性别', '身份证号', '家庭住址', '联系电话', '操作']

        # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(Web_PO.getSuperEleByX("//tbody", "."), ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_memtalDisorder_jsregister_operation(self, d_):

        # 严重精神障碍登记 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_memtalDisorder_jsregister_operation('新增登记及信息补充', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '新增登记及信息补充':
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in ['监护人地址 ', '辖区村(居)委联系人 ', ' 专科医生的意见（如果有请记录）']:
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
                        if k in ['监护人姓名 ', ' 监护人电话 ', ' 联系人电话 ', ' 签字 ']:
                            Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div[1]/input", v)
                        elif k in [' 与患者关系 ']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/div/div/input",  v)
                        elif k in [' 签字日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/input", v)
                        elif k in [' 初次发病时间 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
                        elif k in [' 既往治疗情况 ']:
                            for k1, v1 in v.items():
                                if k1 == '门诊':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div[1]/label", v1)
                                elif k1 == '住院':
                                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div[1]/input", v1)
                        elif k in [' 目前诊断情况 ']:
                            for k1, v1 in v.items():
                                if k1 == '诊断':
                                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div/div/div[1]/input", v1)
                                elif k1 == '确诊医院':
                                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[4]/div/div/div[1]/input", v1)
                                elif k1 == '确诊日期':
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[6]/div/div/div[1]/input", v1)
                        elif k in [' 危险行为 ']:
                            for k1, v1 in v.items():
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/label", k1)
                                if k1 == '有':
                                    for i in range(len(v1)):
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div[" + str(i+1) + "]/input", v1[i])
                        elif k in [' 既往主要症状 ']:
                            Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v, './/div[3]/div/div/div[1]/input')
                        elif k in ['户别 ', '就业情况 ', '知情同意 ', ' 重性精神疾病分类 ', ' 既往关锁情况 ',' 经济状况 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
                        elif k in [' 最近一次治疗效果 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div[1]/label", v)
                        elif k in [' 建卡日期']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/input", v)

                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)


            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.11.2  基本公卫 - 严重精神障碍健康管理 - 严重精神障碍患者

    def __seriousMentalDisorderRegistration1(self, d_):

        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in ['监护人地址 ', '辖区村(居)委联系人 ', ' 专科医生的意见（如果有请记录）']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            if k in ['监护人姓名 ', ' 监护人电话 ', ' 联系人电话 ', ' 签字 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div[1]/input", v)
            elif k in [' 与患者关系 ']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/div/div/input",
                                    v)
            elif k in [' 签字日期 ']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/input", v)
            elif k in [' 初次发病时间 ']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
            elif k in [' 既往治疗情况 ']:
                for k1, v1 in v.items():
                    if k1 == '门诊':
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div[1]/label", v1)
                    elif k1 == '住院':
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div[1]/input", v1)
            elif k in [' 目前诊断情况 ']:
                for k1, v1 in v.items():
                    if k1 == '诊断':
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div/div/div[1]/input", v1)
                    elif k1 == '确诊医院':
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[4]/div/div/div[1]/input", v1)
                    elif k1 == '确诊日期':
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[6]/div/div/div[1]/input", v1)
            elif k in [' 危险行为 ']:
                for k1, v1 in v.items():
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div[1]/label", k1)
                    if k1 == '有':
                        for i in range(len(v1)):
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div[" + str(i + 1) + "]/input", v1[i])
            elif k in [' 既往主要症状 ']:
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                    './/div[3]/div/div/div[1]/input')
            elif k in ['户别 ', '就业情况 ', '知情同意 ', ' 重性精神疾病分类 ', ' 既往关锁情况 ', ' 经济状况 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in [' 最近一次治疗效果 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div/div[1]/label", v)
            elif k in [' 建卡日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/input", v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
    def __seriousMentalDisorderRegistration2(self, d_):

        ele = Web_PO.getSuperEleByX("//form", ".")
        for k, v in d_['data'].items():
            if k in ['监护人地址 ', '辖区村(居)委联系人 ', ' 专科医生的意见（如果有请记录）']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)
            if k in ['监护人姓名 ', ' 监护人电话 ', ' 联系人电话 ', ' 签字 ']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div[1]/input", v)
            elif k in [' 与患者关系 ']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/div/div/input",
                                    v)
            elif k in [' 签字日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/input", v)
            elif k in [' 初次发病时间 ']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
            elif k in [' 既往治疗情况 ']:
                for k1, v1 in v.items():
                    if k1 == '门诊':
                        Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div[1]/label",
                                                  v1)
                    elif k1 == '住院':
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div[1]/input",
                                                  v1)
            elif k in [' 目前诊断情况 ']:
                for k1, v1 in v.items():
                    if k1 == '诊断':
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div/input", v1)
                        # Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div/div/div[1]/input", v1)
                        # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[12]/div[2]/div/div[2]/div/input
                    elif k1 == '确诊医院':
                        Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[4]/div/input", v1)
                        # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[12]/div[2]/div/div[4]/div/input
                    elif k1 == '确诊日期':
                        Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[6]/div/div/div/input", v1)
                        # /html/body/div[1]/div/div[3]/section/div/div[2]/form/div[12]/div[2]/div/div[6]/div/div/div/input
            elif k in [' 危险行为 ']:
                for k1, v1 in v.items():
                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", k1)
                    if k1 == '有':
                        for i in range(len(v1)):
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[3]/div[" + str(i + 1) + "]/input", v1[i])
            elif k in [' 既往主要症状 ']:
                Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v,
                                                    './/div[3]/div/div/div[1]/input')
            elif k in ['户别 ', '就业情况 ', '知情同意 ', ' 重性精神疾病分类 ', ' 既往关锁情况 ', ' 最近一次治疗效果 ', ' 经济状况 ']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in [' 建卡日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/input", v)

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
    def __eleRadioLeftLabel(self, ele, varTextByXs, v):
        # 单选框LL - 死亡原因：{'躯体疾病': 1, '自杀': 2, '他杀': 3, '意外': 4, '精神疾病相关并发症': 5, '其他': 6}
        l_ = Web_PO.eleGetTextByXs(ele, varTextByXs)  # ".//td[4]/div/div/div/label"
        # print(l_)  # ['躯体疾病(\n传染病和寄生虫病\n肿瘤\n心脏病\n脑血管病\n呼吸系统疾病\n消化系统疾病\n其他疾病\n不详\n)', '自杀\n他杀\n意外\n精神疾病相关并发症\n其他']
        l_ = l_[1].split("\n")
        l_.insert(0, '躯体疾病(')
        # print(l_)
        d_3 = dict(enumerate(l_, start=1))
        d_4 = {v1: k1 for k1, v1 in d_3.items()}
        print(d_4)  # {'躯体疾病': 1, '自杀': 2, '他杀': 3, '意外': 4, '精神疾病相关并发症': 5, '其他': 6}
        Web_PO.eleClkByX(ele, varTextByXs + "[" + str(d_4[v]) + "]/label", 2)
    def rgb_to_hex(self,rgb):
        # 从rgb字符串中提取红、绿、蓝的值
        r, g, b = map(int, rgb.strip('rgb()').split(', '))
        # 将每个值转换为两位十六进制字符串
        hex_r = '{:02x}'.format(r)
        hex_g = '{:02x}'.format(g)
        hex_b = '{:02x}'.format(b)
        # 组合成完整的十六进制颜色码
        hex_color = '#' + hex_r + hex_g + hex_b
        return hex_color

    def phs_memtalDisorder_jsfiles_query(self, d_):

        # 严重精神障碍患者 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构', '档案状态','服药依从性','管理状态','随访提醒分类','重性精神疾病分类']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ["上次随访时间", '登记日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                elif k in ['登记时年龄']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[1]/input", v[0])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[2]/input", v[1])
                elif k in ['现住址']:
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[1]/div/div/div/div/input",  v[0])
                    Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), ".//div[2]/div/div/div/div/input",  v[1])
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), ".//div[3]/div/div/input", v[2])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_memtalDisorder_jsfiles_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        # print(l_field)  # ['姓名', '提醒', '性别', '登记时年龄', '联系电话', '上次随访日期', '下次随访日期', '登记日期', '登记机构', '患者类型', '菌痰情况', '停止治疗原因', '身份证号', '家庭住址', '管理状态', '操作']
        Web_PO.zoom(100)

        # # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        for i in l_group:
            i.pop(2)
            i.pop(2)
        # print(l_group)

        l_class_warn = Web_PO.eleGetAttrValueByXs(ele2, ".//td[3]/div/div/div", "style")
        # print(l_class_warn)  # ['background-color: rgb(223, 57, 38);']
        for i in range(len(l_class_warn)):
            l_class_warn[i] = l_class_warn[i].split("background-color: ")[1].split(";")[0]
        # print(l_class_warn)  # ['rgb(223, 57, 38)']

        # 测试
        # rgb = 'rgb(223, 57, 38)'
        hex_color = self.rgb_to_hex(l_class_warn[0])
        # print(hex_color)  # 输出: #df3926

        for i in range(len(l_group)):
            # l_group[i][2] = l_class_warn[i]
            l_group[i][2] = hex_color
        # print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_memtalDisorder_jsfiles_operation(self, d_):

        # 严重精神障碍患者 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_memtalDisorder_jsfiles_operation('访视记录', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
            else:
                if d_['operate'] == '新增登记及信息补充':
                    self.__seriousMentalDisorderRegistration1(d_)

                elif d_['operate'] == '访视记录之编辑患者登记':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[1]', 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='修改']", ".."), ".", 2)
                    self.__seriousMentalDisorderRegistration2(d_)
                elif d_['operate'] == '访视记录之新增随访记录':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[2]', 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()=' 新增随访']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in [' 随访日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/input", v)
                        elif k in [' 下次随访日期 ']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/input")
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/input", v)
                        elif k in [' 本次随访形式 ', ' 饮食情况 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div[1]/label", v)
                        elif k in [' 若失访，原因 ']:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v, './/div[2]/div[2]/div/div/div/input')
                        elif k in [' 如死亡 ']:
                            for k1, v1 in v.items():
                                if k1 == '死亡日期':
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div/input", v1)
                                elif k1 == '死亡原因':
                                    for k2, v2 in v1.items():
                                        self.__eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div/div/div", k2)
                                        if k2 == '躯体疾病(':
                                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div/div/div[1]/div/div/div[1]/label", v2)
                        elif k in [' 危险性评估 ', ' 自知力 ', ' 两次随访期间 关锁情况 ', ' 治疗效果 ', ' 随访评价结果 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div[1]/label", v)
                        elif k in [' 睡眠情况 ', ' 两次随访期间 住院情况 ', ' 用药依从性 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/label", v)
                        elif k in [' 目前症状 ']:
                            Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/label", v, './/div[2]/div[2]/div/div/div/input')
                        elif k in [' 社会功能情况 ']:
                            for k1, v1 in v.items():
                                if k1 == '个人生活料理':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div[1]/label", v1)
                                if k1 == '家务劳动':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[4]/div/div/div[1]/label", v1)
                                if k1 == '生产劳动及工作':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div[1]/label", v1)
                                if k1 == '学习能力':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[4]/div/div/div[1]/label", v1)
                                if k1 == '社会人际交往':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div/div[1]/label", v1)
                        elif k in [' 危险行为 ']:
                            for k1, v1 in v.items():
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/label", k1)
                                if k1 == '有':
                                    for i in range(len(v1)):
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[" + str(i+1) + "]/input", v1[i])
                        elif k in [' 末次出院日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                        elif k in [' 实验室检查 ']:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/label", v, ".//div[2]/div[2]/div/div/div/input")
                        elif k in [' 用药情况 ', ' 调整用药情况 ']:
                            if len(v) == 1:
                                for k1, v1 in v[0].items():
                                    if k1 == '药品名称':
                                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div/div/div/input",  v1)
                                    elif k1 == '用法用量':
                                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[4]/div/div/div/input",  v1[0])
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[5]/div/input", v1[1])
                            else:
                                for _ in range(len(v)-1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[6]/div")
                                for i in range(len(v)):
                                    for k1, v1 in v[i].items():
                                        if k1 == '药品名称':
                                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[2]/div/div/div/input",  v1)
                                        elif k1 == '用法用量':
                                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[4]/div/div/div/input",  v1[0])
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[5]/div/input", v1[1])
                        elif k in [' 药物不良反应 ']:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[3]/div[1]/div/div/div/label", v, ".//div[3]/div[2]/div/div/input")
                        elif k in [' 康复措施 ']:
                            Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v, 'div[2]/div[2]/div/div/div/input')
                        elif k in [' 通知联席部门 ']:
                            for k1, v1 in v.items():
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", k1)
                                if k1 == '是':
                                    for k2, v2 in v1.items():
                                        if k2 == '公安部门/社区综治 中心受理人姓名':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div/div/div/input", v2[0])
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/div/div/div/input", v2[1])
                                        elif k2 == '电话':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[6]/div/div/div/input", v2[0])
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[7]/div/div/div/input", v2[1])
                        elif k in [' 转诊 ']:
                            for k1, v1 in v.items():
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div/label", k1)
                                if k1 == '是':
                                    for k2, v2 in v1.items():
                                        if k2 == '转诊原因':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[4]/div/input", v2)
                                        elif k2 == '转诊机构':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/input", v2)
                                        elif k2 == '转诊诊室':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[4]/div/input", v2)
                        elif k in [' 随访医师']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/div/input",  v)
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/div[5]/form/div[22]/div[2]/div[3]/div/div/div/div/div/input
                        elif k in [' 随访医疗机构 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)
                        elif k in [' 患者（家属）签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[7]/div/div/div/input", v)

                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

                elif d_['operate'] == '访视记录之结案随访记录':
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/div[1]/div[2]', 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='结案']", ".."), ".", 2)
                    ele = Web_PO.getSuperEleByX("//span[text()='结案原因：']", "../..")
                    for k, v in d_['data'].items():
                        if k in ["结案原因："]:
                            Web_PO.eleRadioRightLabelAndText(ele, ".//div[1]/div/label", v, ".//div[2]/div/textarea")
                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='确 定']", ".."), ".", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='取 消']", ".."), ".", 2)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))



    # todo 2.11.3  基本公卫 - 严重精神障碍健康管理 - 严重精神障碍患者随访

    def phs_memtalDisorder_jsjob_query(self, d_):

        # 严重精神障碍患者随访 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            try:
                if k in ['姓名', '身份证号']:
                    Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
                elif k in ['是否仅查询机构']:
                    Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
                elif k in ['随访日期']:
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])
                elif k in ['管理机构']:
                    self.__gljg(ele, k, v)

            except:
                self.logger.error("查询 => " + str(k) + ": " + str(v))

        # 查询
        Web_PO.eleClkByX(Web_PO.eleGetSuperEleByX(ele, ".//span[text()='查询 ']", ".."), ".", 2)

        # 日志
        self.logger.info("查询 => " + str(d_))

    def _phs_memtalDisorder_jsjob_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        print(l_field)  # ['姓名', '提醒', '性别', '登记时年龄', '联系电话', '上次随访日期', '下次随访日期', '登记日期', '登记机构', '患者类型', '菌痰情况', '停止治疗原因', '身份证号', '家庭住址', '管理状态', '操作']
        Web_PO.zoom(100)

        # # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_memtalDisorder_jsjob_operation(self, d_):

        # 严重精神障碍患者 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_memtalDisorder_jsjob_operation('编辑\n删除', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)
                if d_['operate'] == '删除':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='否'])[last()]", ".."), ".", 2)
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("(//span[text()='是'])[last()]", ".."), ".", 2)
                    self.logger.info("删除 => " + str(d_))
            else:
                if d_['operate'] == '编辑':
                    ele = Web_PO.getSuperEleByX("//form", ".")
                    for k, v in d_['data'].items():
                        if k in [' 随访日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/input", v)
                        elif k in [' 下次随访日期 ']:
                            Web_PO.eleScrollViewByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/input")
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/input", v)
                        elif k in [' 本次随访形式 ', ' 饮食情况 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div[1]/label", v)
                        elif k in [' 若失访，原因 ']:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v, './/div[2]/div[2]/div/div/div/input')
                        elif k in [' 如死亡 ']:
                            for k1, v1 in v.items():
                                if k1 == '死亡日期':
                                    Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div/input", v1)
                                elif k1 == '死亡原因':
                                    for k2, v2 in v1.items():
                                        self.__eleRadioLeftLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div/div/div", k2)
                                        if k2 == '躯体疾病(':
                                            Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div/div/div[1]/div/div/div[1]/label", v2)
                        elif k in [' 危险性评估 ', ' 自知力 ', ' 两次随访期间 关锁情况 ', ' 治疗效果 ', ' 随访评价结果 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/div[1]/label", v)
                        elif k in [' 睡眠情况 ', ' 两次随访期间 住院情况 ', ' 用药依从性 ']:
                            Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/label", v)
                        elif k in [' 目前症状 ']:
                            Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/label", v, './/div[2]/div[2]/div/div/div/input')
                        elif k in [' 社会功能情况 ']:
                            for k1, v1 in v.items():
                                if k1 == '个人生活料理':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div[1]/label", v1)
                                if k1 == '家务劳动':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[4]/div/div/div[1]/label", v1)
                                if k1 == '生产劳动及工作':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/div/div[1]/label", v1)
                                if k1 == '学习能力':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[4]/div/div/div[1]/label", v1)
                                if k1 == '社会人际交往':
                                    Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div[2]/div/div/div[1]/label", v1)
                        elif k in [' 危险行为 ']:
                            for k1, v1 in v.items():
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/label", k1)
                                if k1 == '有':
                                    for i in range(len(v1)):
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[" + str(i+1) + "]/input", v1[i])
                        elif k in [' 末次出院日期 ']:
                            Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/input", v)
                        elif k in [' 实验室检查 ']:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div[1]/label", v, ".//div[2]/div[2]/div/div/div/input")
                        elif k in [' 用药情况 ', ' 调整用药情况 ']:
                            # /html/body/div[1]/div/div[3]/section/div/div[2]/div[5]/form/div[14]/div[2]/div[2]/div[6]/div
                            if k == ' 用药情况 ':
                                for _ in 5:
                                    if Web_PO.isEleExistByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[5]/form/div[14]/div[2]/div[2]/div[6]/div"):
                                        Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[5]/form/div[14]/div[2]/div[2]/div[6]/div")
                            if k == ' 调整用药情况 ':
                                for _ in 5:
                                    if Web_PO.isEleExistByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[5]/form/div[21]/div[2]/div[2]/div[6]/div"):
                                        Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[5]/form/div[21]/div[2]/div[2]/div[6]/div")

                            if len(v) == 1:
                                for k1, v1 in v[0].items():
                                    if k1 == '药品名称':
                                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[2]/div/div/div/input",  v1)
                                    elif k1 == '用法用量':
                                        Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[4]/div/div/div/input",  v1[0])
                                        Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[5]/div/input", v1[1])
                            elif len(v) > 1:
                                for _ in range(len(v)-1):
                                    Web_PO.eleClkByX(Web_PO.eleCommon(ele, k), ".//div[2]/div/div[6]/div")
                                for i in range(len(v)):
                                    for k1, v1 in v[i].items():
                                        if k1 == '药品名称':
                                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[2]/div/div/div/input",  v1)
                                        elif k1 == '用法用量':
                                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[4]/div/div/div/input",  v1[0])
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[" + str(i+1) + "]/div[5]/div/input", v1[1])


                        elif k in [' 药物不良反应 ']:
                            Web_PO.eleRadioRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[3]/div[1]/div/div/div/label", v, ".//div[3]/div[2]/div/div/input")
                        elif k in [' 康复措施 ']:
                            Web_PO.eleCheckboxRightLabelAndText(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", v, 'div[2]/div[2]/div/div/div/input')
                        elif k in [' 通知联席部门 ']:
                            for k1, v1 in v.items():
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/label", k1)
                                if k1 == '是':
                                    for k2, v2 in v1.items():
                                        if k2 == '公安部门/社区综治 中心受理人姓名':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[3]/div/div/div/input", v2[0])
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[4]/div/div/div/input", v2[1])
                                        elif k2 == '电话':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[6]/div/div/div/input", v2[0])
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[7]/div/div/div/input", v2[1])
                        elif k in [' 转诊 ']:
                            for k1, v1 in v.items():
                                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[2]/div/div/div/label", k1)
                                if k1 == '是':
                                    for k2, v2 in v1.items():
                                        if k2 == '转诊原因':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div[4]/div/input", v2)
                                        elif k2 == '转诊机构':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[2]/div/input", v2)
                                        elif k2 == '转诊诊室':
                                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div[4]/div/input", v2)
                        elif k in [' 随访医师']:
                            Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div[3]/div/div/div/div/div/input",  v)
                        elif k in [' 随访医疗机构 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[5]/div/div/div/input", v)
                        elif k in [' 患者（家属）签名 ']:
                            Web_PO.eleSetTextByX(Web_PO.eleCommon(ele, k), ".//div[7]/div/div/div/input", v)

                    # Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)
                    # 保存
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[5]/div/div/button[1]", 2)

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))




    # todo 2.12.1 基本公卫 - 健康教育 - 健康教育活动

    def phs_healtheducation_healthactivity_query(self, d_):

        # 健康教育活动 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")  # form

        for k, v in d_.items():
            if k in ['活动地点', '活动形式', '活动主题', '主讲人']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['活动日期']:
                 Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[1]/div/input", v[0])
                 Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[3]/div/input", v[1])

        # Web_PO.eleClkByX(ele, ".//button[1]")  # 查询
        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='查询']", ".."), ".", 2)

    def __healthactivity(self, d_, varLabel= '新增'):

        # 健康教育活动 - 新增

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        for k, v in d_.items():
            if k in ['主讲人', '活动内容', '活动总结评价', '填表人']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//input", v)
            if k in ['活动地点', '活动人数', '主讲人单位', '负责人', '健康教育资源发放数量']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[4]/div/div/div/input", v)
            if k in ['组织者', '职称']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/input", v)
            elif k in ['活动时间']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//input", v)
            elif k in ['填表时间']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), ".//div[6]/div/div/div/input", v)
            elif k in ['活动形式', '活动主题', '接受健康教育人员类别']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//input",  v)
            elif k in ['健康教育资源发放种类']:
                Web_PO.eleRadioRightLabel(Web_PO.eleCommon(ele, k), ".//div[2]/div/div/div/label", v)
            elif k in ['存档资料类型']:
                if v[0] != []:
                    Web_PO.eleCheckboxRightLabel2(Web_PO.eleCommon(ele, k), ".//div[2]/div[1]/div/div/div/div/label", v[0])
                if varLabel == '编辑':
                    # 定位元素，按delete
                    for _ in range(10):
                        if Web_PO.eleIsEleExistByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/ul/li[1]"):
                            Web_PO.eleSendKeysByX(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/ul/li[1]", Keys.DELETE)
                        else:
                            break
                if v[1] != []:
                    Web_PO.upFile(Web_PO.eleCommon(ele, k), ".//div[2]/div[2]/div/div/div/ul/div", v[1])

        Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='保存']", ".."), ".", 2)

    def _phs_healtheducation_healthactivity_operation(self, varOperation, d_option):

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        ele1 = Web_PO.getSuperEleByX("//thead", ".")

        d_1 = {}
        # 获取字典列表
        Web_PO.zoom(50)
        l_field = Web_PO.eleGetTextByXs(ele1, ".//div")
        print(
            l_field)  # ['姓名', '提醒', '性别', '登记时年龄', '联系电话', '上次随访日期', '下次随访日期', '登记日期', '登记机构', '患者类型', '菌痰情况', '停止治疗原因', '身份证号', '家庭住址', '管理状态', '操作']
        Web_PO.zoom(100)

        # # 获取字段和类型字典
        l_value = Web_PO.eleGetTextByXs(ele2, ".//div")
        l_group = (List_PO.split2(l_value, varOperation))
        print(l_group)

        # 遍历获取每行数据中全部符合要求的字段索引max_key
        d_1 = {}
        s = 0
        for i in range(len(l_group)):
            for k, v in d_option.items():
                if k in l_field:
                    s_fieldIndex = l_field.index(k)
                    if l_group[i][s_fieldIndex] == v:
                        s = s + 1
                        d_1[i + 1] = s
            s = 0
        # print(d_1)  # {2: 1, 3: 2}
        max_key = max(d_1, key=d_1.get)
        # print(max_key)  # 3   表示有2条记录，分别是第二和第三行记录，其中第三条记录有两个条件命中，返回命中多的哪一行记录，所以返回3
        return max_key
    def phs_healtheducation_healthactivity_operation(self, d_):

        # 健康教育活动 - 操作

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        try:
            if "data" not in d_:
                ele3 = Web_PO.getSuperEleByX("(//span[text()='" + d_['operate'] + "'])[position()=" + str(
                    self._phs_healtheducation_healthactivity_operation('查看', d_['option'])) + "]", "..")
                Web_PO.eleClkByX(ele3, ".", 2)

            else:

                if d_['operate'] == '新增':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='新增']", ".."), ".", 2)
                    self.__healthactivity(d_['data'], '新增')

                if d_['operate'] == '编辑':
                    Web_PO.eleClkByX(Web_PO.getSuperEleByX("//span[text()='修改']", ".."), ".", 2)
                    self.__healthactivity(d_['data'], '编辑')

            self.logger.info(str(d_))
        except:
            self.logger.error("失败 =>" + str(d_))




    # todo 2.13.1 基本公卫 - 健康行为积分 - 本年度未评

    def phs_hbp_noassessdata_query(self, d_):

        # 本年度未评 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//label[text()='管理机构']", "../../../..")  # form
        # _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            if k in ['姓名', '身份证号']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div/input", v)
            elif k in ['人群分类']:
                Web_PO.eleCheckboxLabels(Web_PO.eleCommon(ele, k), ".//span[2]", v)
            elif k in ['档案状态']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div/div/div/input",  v)
            elif k in ['现住址']:
                Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), "./div[1]/div/div/div/div/input",  v[0])
                Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), "./div[2]/div/div/div/div/input",  v[1])
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), "./div[3]/div/div/input", v[2])
            elif k in ['管理机构']:
                self.__gljg(ele, k, v)

        Web_PO.eleClkByX(ele, "./div[2]/div[2]/div/button[1]", 2)  # 点击查询

        # 2 获取查询数量
        s_ = self._getQty()
        return s_

    def phs_hbp_noassessdata_new(self, d_):

        # 本年度未评 - 2025年居民健康行为积分卡

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        # ele = Web_PO.getSuperEleByX("//div[text()='2025年居民健康行为积分卡']", ".")
        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        varTrQty = Web_PO.eleGetQtyByXs(ele2, ".//tr")

        for k, v in d_.items():
            if k in ['积分']:
                l_ = []
                l_all = []
                for i in range(varTrQty-1):
                    varTdQty = Web_PO.eleGetQtyByXByXs(ele2, "./tr[" + str(i+1) + "]", "./td")
                    # print(varTdQty)
                    if varTdQty == 10:
                        varCrowd = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]")
                        varSeriea = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[2]")
                        varActionName = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[3]")
                    else:
                        varSeriea = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]")
                        varActionName = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[2]")
                    l_.append(varCrowd)
                    l_.append(varSeriea)
                    l_.append(varActionName)
                    l_all.append(l_)
                    l_ = []
                # print(l_all)  # [['所有人', '1', '健康素养'], ['所有人', '2', '健康教育'],...
                d_1 = dict(enumerate(l_all, start=1))
                # print(d_1)  # {1: ['所有人', '1', '健康素养'], 2: ['所有人', '2', '健康教育'],...
                for i in range(len(v)):
                    for k1, v1 in d_1.items():
                        if v1 == v[i][0]:
                            varTdQty = Web_PO.eleGetQtyByXByXs(ele2, "./tr[" + str(k1) + "]", "./td")
                            Web_PO.eleScrollViewByX(ele2, "./tr[" + str(k1) + "]/td["+ str(varTdQty-2) + "]/div/div/div/div/input")
                            Web_PO.eleDropdownDate1(ele2, ".//tr[" + str(k1) + "]/td["+ str(varTdQty-2) + "]/div/div/div/div/input", v[i][1])
                            Web_PO.eleSetTextByX(ele2, ".//tr[" + str(k1) + "]/td["+ str(varTdQty-1) + "]/div/div/div/div/input", v[i][2])

            elif k in ['评分日期']:
                Web_PO.eleDropdownDate1(ele2, ".//tr[" + str(varTrQty) + "]/td[2]/div/div/div/div/input", v)

            elif k in ['是否兑换']:
                Web_PO.eleDropdown(ele2, ".//tr[" + str(varTrQty) + "]/td[3]/div/div/div[1]/div/div/div/div/div/input", _dropdownByX, v)

        Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/button[2]")  # 取消
        # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/button[1]")  # 保存

    def phs_hbp_noassessdata_batch(self, d_):
        # Gw_PO.noScored_batch({'身份证号': ['110101194301191302', '340203202407018290']})

        # 本年度未评 - 批量评分
        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        varTrQty = Web_PO.eleGetQtyByXs(ele2, ".//tr")
        l_ = []
        for k, v in d_.items():
            if k in ['身份证号']:
                # 1 勾选
                if isinstance(v, str):
                    # 全勾选
                    Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/main/div[2]/div/div[1]/div[2]/table/thead/tr/th[1]/div/label")
                else:
                    # 按照身份证勾选
                    for i in range(varTrQty):
                        varIdcard = Web_PO.eleGetTextByX(ele2, "./tr[" + str(i+1) + "]/td[5]/div")
                        l_.append(varIdcard)
                    d_1 = dict(enumerate(l_, start=1))
                    # print(d_1)  # {1: '341226199708114773', 2: '110101194301191302',
                    for k1, v1 in d_1.items():
                        if v1 in v:
                            Web_PO.eleClkByX(ele2, "./tr[" + str(k1) + "]/td[1]/div/label")
                # 2 点击批量评分
                ele = Web_PO.getSuperEleByX("//label[text()='管理机构']", "../../../..")  # form
                Web_PO.eleClkByX(ele, "./div[2]/div[2]/div/button[2]", 2)  # 点击批量评分
                varText = Web_PO.getTextByX("/html/body/div[1]/div/div[3]/section/div/div/div/div/div[2]/div")
                print(varText) # 批量执行完成，成功1条数据，失败0条数据
                varNum1 = Web_PO.getTextByX("/html/body/div[1]/div/div[3]/section/div/div/div/div/div[2]/div/span[1]")
                print(varNum1) # 1
                varNum2 = Web_PO.getTextByX("/html/body/div[1]/div/div[3]/section/div/div/div/div/div[2]/div/span[2]")
                print(varNum2) # 0
                Web_PO.eleClkByX("/html/body/div[1]/div/div[3]/section/div/div/div/div/div[3]/div/button") # 关闭



    # todo 2.13.2 基本公卫 - 健康行为积分 - 评分信息查询

    def phs_hbp_assessdata_query(self, d_):

        # 评分信息查询 - 查询

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//label[text()='管理机构']", "../../../..")  # form
        # _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"

        for k, v in d_.items():
            if k in ['姓名', '身份证号']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div/input", v)
            elif k in ['得分范围']:
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div/div[1]/div/input", v[0])
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon(ele, k), ".//div/div/div[3]/div/input", v[1])
            elif k in ['评分日期']:
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), "./div/div/div[1]/div/input", v[0])
                Web_PO.eleDropdownDate1(Web_PO.eleCommon(ele, k), "./div/div/div[3]/div/input", v[1])
            elif k in ['人群分类']:
                Web_PO.eleCheckboxLabels(Web_PO.eleCommon(ele, k), ".//span[2]", v)
            elif k in ['档案状态', '是否兑换']:
                Web_PO.eleDropdown(Web_PO.eleCommon(ele, k), ".//div/div/div/div/input",  v)
            elif k in ['现住址']:
                Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), "./div[1]/div/div/div/div/input",  v[0])
                Web_PO.eleDropdown(Web_PO.eleCommon2(ele, k), "./div[2]/div/div/div/div/input",  v[1])
                Web_PO.eleSetTextEnterByX(Web_PO.eleCommon2(ele, k), "./div[3]/div/div/input", v[2])
            elif k in ['管理机构']:
                self.__gljg(ele, k, v)

        Web_PO.eleClkByX(ele, ".//button[1]", 2)  # 点击查询

        # 2 获取查询数量
        s_ = self._getQty()
        return s_

    def phs_hbp_assessdata_modify(self, d_):

        # 评分信息查询 - 修改

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        _dropdownByX = "//div[@class='el-popper is-pure is-light el-select__popper' and @aria-hidden='false']/div/div/div[1]/ul/li"
        ele2 = Web_PO.getSuperEleByX("//tbody", ".")
        varTrQty = Web_PO.eleGetQtyByXs(ele2, ".//tr")

        for k, v in d_.items():
            if k in ['积分']:
                l_ = []
                l_all = []
                for i in range(varTrQty-1):
                    varTdQty = Web_PO.eleGetQtyByXByXs(ele2, "./tr[" + str(i+1) + "]", "./td")
                    # print(varTdQty)
                    if varTdQty == 10:
                        varCrowd = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]")
                        varSeriea = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[2]")
                        varActionName = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[3]")
                    else:
                        varSeriea = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[1]")
                        varActionName = Web_PO.eleGetTextByX(ele2, ".//tr[" + str(i+1) + "]/td[2]")
                    l_.append(varCrowd)
                    l_.append(varSeriea)
                    l_.append(varActionName)
                    l_all.append(l_)
                    l_ = []
                # print(l_all)  # [['所有人', '1', '健康素养'], ['所有人', '2', '健康教育'],...
                d_1 = dict(enumerate(l_all, start=1))
                # print(d_1)  # {1: ['所有人', '1', '健康素养'], 2: ['所有人', '2', '健康教育'],...
                for i in range(len(v)):
                    for k1, v1 in d_1.items():
                        if v1 == v[i][0]:
                            varTdQty = Web_PO.eleGetQtyByXByXs(ele2, "./tr[" + str(k1) + "]", "./td")
                            Web_PO.eleScrollViewByX(ele2, "./tr[" + str(k1) + "]/td["+ str(varTdQty-2) + "]/div/div/div/div/input")
                            Web_PO.eleDropdownDate1(ele2, ".//tr[" + str(k1) + "]/td["+ str(varTdQty-2) + "]/div/div/div/div/input", v[i][1])
                            Web_PO.eleSetTextByX(ele2, ".//tr[" + str(k1) + "]/td["+ str(varTdQty-1) + "]/div/div/div/div/input", v[i][2])

            elif k in ['评分日期']:
                Web_PO.eleDropdownDate1(ele2, ".//tr[" + str(varTrQty) + "]/td[2]/div/div/div/div/input", v)

            elif k in ['是否兑换']:
                Web_PO.eleDropdown(ele2, ".//tr[" + str(varTrQty) + "]/td[3]/div/div/div[1]/div/div/div/div/div/input", _dropdownByX, v)

        Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/button[2]")  # 取消
        # Web_PO.clkByX("/html/body/div[1]/div/div[3]/section/div/div[2]/div[2]/button[1]")  # 保存

    def phs_hbp_assessdata_detail(self):

        # 评分信息查询 - 详情

        signal.signal(signal.SIGINT, self.__handle_signal)
        signal.signal(signal.SIGTERM, self.__handle_signal)

        ele = Web_PO.getSuperEleByX("//form", ".")

        a = Web_PO.eleGetTextByXs(ele, ".//div")
        b = Web_PO.eleGetTextByXs(ele, ".//span")
        print("a", a)
        print("b", b)









    def yjzx(self, varDisease, varProject):

        # 已建专项

        l_disease = Web_PO.getTextByXs("//button/span")
        # print(l_disease)
        for i in range(len(l_disease)):
            if l_disease[i] == varDisease:
                Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/button[" + str(i+1) + "]", 2)
                if varDisease == '高血压专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血压患者管理卡
                        print(self.hypertensionPatientCard())
                if varDisease == '糖尿病专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血压患者管理卡
                        print(self.diabetesPatientCard())
                if varDisease == '高血脂专项':
                    if varProject == '专项登记':
                        Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div[1]", 2)
                        # 高血脂患者管理卡
                        print(self.hyperlipidemiaPatientCard())
                break

    def hypertensionPatientCard(self):

        # 高血压患者管理卡

        # 获取字段名
        l_div = Web_PO.getTextByXs("//div[@class='table_line']/div")
        # print(l_div)  # ['管理卡号', '信息来源\n健康档案\n首诊测压\n普查\n门诊就诊\n其他', '', '档案编号'...
        l_div.remove('吸烟情况\n吸烟状况\n戒烟开始日期\n开始吸烟年龄\n岁')
        l_div.remove("未服药血压\nmmHg\nmmHg")
        # print(l_div)  # ['管理卡号', '信息来源\n健康档案\n首诊测压\n普查\n门诊就诊\n其他', '', '档案编号'...

        # 获取radio或checkbox状态
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"

        d_radio = {}
        d_radio1 = {}
        l_2 = []
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_div[i] = l_div[i].replace('饮酒情况\n饮酒频率\n从不\n偶尔\n经常\n每天\n开始饮酒年龄\n岁\n是否饮酒过量\n是\n否','饮酒频率\n从不\n偶尔\n经常\n每天\n是\n否')
                l_div[i] = l_div[i].replace('体育锻炼\n锻炼频率\n每天\n每周一次以上\n偶尔\n不运动','锻炼频率\n每天\n每周一次以上\n偶尔\n不运动')
                l_div[i] = l_div[i].replace('有\n无\n职业暴露危险因素','职业病危害因素接触史\n有\n无')
                l_div[i] = l_div[i].replace('有危害因素的具体职业\n从事职业时长\n年\n防护措施\n无\n有','防护措施\n无\n有')
                l_1 = l_div[i].split("\n")
                l_2.append(l_1.pop(0))
                # print(l_1)  # ['健康档案', '首诊测压', '普查', '门诊就诊', '其他']

                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                    # l_2.append(l_1[i].split("\n")[0])
                # print(l_2)
                d_box = dict(zip(l_1, l_bool))
                d_radio[l_div[ele_n]] = d_box

        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_radio1 = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print(d_radio1)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        l_field = ['管理卡号','其他情况说明','档案编号', '姓名', '性别', '出生日期', '联系电话',
                    '身份证号码', '居住地址', '身高(cm)', '体重(kg)', '吸烟状况', '戒烟开始日期', '开始吸烟年龄',
                    '开始饮酒年龄', '职业暴露危险因素', '有危害因素的具体职业', '从事职业时长',
                    '毫米汞柱起','毫米汞柱始','确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        # print(l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(8))
        l_input.insert(8, ll)

        d_other = dict(zip(l_field, l_input))
        # print(d_other)  # {'管理卡号': '135', '其他情况说明': '', ...

        d_other.update(d_radio1)
        return d_other

    def diabetesPatientCard(self):

        # 糖尿病患者管理卡

        # 1，获取所有字段名和checkbox值
        l_trtd = Web_PO.getTextByXs("//tr/td")
        l_trtd = [i for i in l_trtd if i != '']
        # print(l_trtd)

        # 2.1，获取非checkbox字段
        ll = []
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                ll.append(l_trtd[ele_before_n])
        l_normalfield = [i for i in l_trtd if "\n" not in i]
        for i in range(len(ll)):
            l_normalfield.remove(ll[i])
        # print(l_normalfield)  # ['档案编号', '姓名', '性别', '出生日期', '身份证号', '职业', '居住地址', '身高(cm)', '体重(kg)', '确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        # 2.2，获取非checkbox值
        l_normalValue = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        # print(l_normalValue)  # ['37068500200200014', '6月26日测试', '女', '1960-01-19'
        # 将居住地址6个值（索引5）组成列表
        l_tmp = []
        for i in range(6):
            l_tmp.append(l_normalValue.pop(5))
        l_normalValue.insert(5, l_tmp)
        # 2.3，合成非checkbox字典
        d_normal = dict(zip(l_normalfield, l_normalValue))
        # print(d_normal)  # {'档案编号': '543912fd978b4634bae81a7b556b95cb', '姓名': '6月26日测试', '性别': '女', '出生日期': '1960-01-19', '身份证号': '110101196001193209', '居住地址': ['山东省', '烟台市', '招远市', '泉山街道', '魁星东社区居民委员会', '1'], '身高(cm)': '145', '体重(kg)': '67', '其他特殊类型糖尿病说明': '', '确诊日期': '2024-06-13', '终止管理日期': '1900-01-01', '终止管理原因': '', '建卡时间': '2024-06-28', '建卡医生': '卫健委', '建卡医疗机构': '招远市卫健局'}

        # 3.1，获取checkbox值(# el-radio__input is-checked)
        l_checkbox = Web_PO.isBooleanAttrValueListByX("//div/label/span[1]", 'class',
                                                      'el-radio__input is-disabled is-checked')
        # print(l_checkbox)  # ['False', 'True', 'False', 'False', ...
        # 3.2，合成checkbox字典
        d_checkbox = {}
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                l_1 = l_trtd[i].split("\n")
                # print(l_1)  # ['健康档案', '社区门诊', '流行病学调查', '其他']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_checkbox.pop(0))
                l_all = dict(zip(l_1, l_bool))
                d_checkbox[l_trtd[ele_before_n]] = l_all
        # print(d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 4，按页面字段名顺序输出
        d_result = {}
        l_trtd1 = [i for i in l_trtd if "\n" not in i and i != '']
        for i in range(len(l_trtd1)):
            for k, v in d_normal.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
        return d_result

    def hyperlipidemiaPatientCard(self):

        # 高血脂患者管理卡

        # 1，获取所有字段名和checkbox值
        l_trtd = Web_PO.getTextByXs("//tr/td")
        l_trtd = [i for i in l_trtd if i != '']
        # print(l_trtd)

        # 2.1，获取非checkbox字段
        ll = []
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                ll.append(l_trtd[ele_before_n])
        l_normalfield = [i for i in l_trtd if "\n" not in i]
        for i in range(len(ll)):
            l_normalfield.remove(ll[i])
        # print(l_normalfield)  # ['档案编号', '姓名', '性别', '出生日期', '身份证号', '职业', '居住地址', '身高(cm)', '体重(kg)', '确诊日期', '终止管理日期', '终止管理原因', '建卡时间', '建卡医生', '建卡医疗机构']
        # 2.2，获取非checkbox值
        l_normalValue = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        # print(l_normalValue)  # ['37068500200200014', '6月26日测试', '女', '1960-01-19'
        # 将居住地址6个值（索引5）组成列表
        l_tmp = []
        for i in range(6):
            l_tmp.append(l_normalValue.pop(6))
        l_normalValue.insert(6, l_tmp)
        # 2.3，合成非checkbox字典
        d_normal = dict(zip(l_normalfield, l_normalValue))
        # print(d_normal)  # {'档案编号': '543912fd978b4634bae81a7b556b95cb', '姓名': '6月26日测试', '性别': '女', '出生日期': '1960-01-19', '身份证号': '110101196001193209', '居住地址': ['山东省', '烟台市', '招远市', '泉山街道', '魁星东社区居民委员会', '1'], '身高(cm)': '145', '体重(kg)': '67', '其他特殊类型糖尿病说明': '', '确诊日期': '2024-06-13', '终止管理日期': '1900-01-01', '终止管理原因': '', '建卡时间': '2024-06-28', '建卡医生': '卫健委', '建卡医疗机构': '招远市卫健局'}

        # 3.1，获取checkbox值(# el-radio__input is-checked)
        l_checkbox = Web_PO.isBooleanAttrValueListByX("//div/label/span[1]", 'class', 'el-radio__input is-checked')
        # print(l_checkbox)  # ['False', 'True', 'False', 'False', ...
        # 3.2，合成checkbox字典
        d_checkbox = {}
        for i in range(len(l_trtd)):
            if "\n" in l_trtd[i]:
                ele_n = l_trtd.index(l_trtd[i])
                ele_before_n = ele_n - 1
                l_1 = l_trtd[i].split("\n")
                # print(l_1)  # ['健康档案', '社区门诊', '流行病学调查', '其他']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_checkbox.pop(0))
                l_all = dict(zip(l_1, l_bool))
                d_checkbox[l_trtd[ele_before_n]] = l_all
        # print(d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 4，按页面字段名顺序输出
        d_result = {}
        l_trtd1 = [i for i in l_trtd if "\n" not in i and i != '']
        for i in range(len(l_trtd1)):
            for k,v in d_normal.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if l_trtd1[i] == k:
                    d_result[k] = v
        return d_result

    def runUser(self, *varUsername):

        l_username = Web_PO.getTextByXs("//tr/td[1]/div")
        # print(l_username) # ['零跑', '测试', '黎明', '李永波', '胡军', '张建民', '舒雅有', '赵爽', '陈平安']

        if len(varUsername) == 1 and varUsername[0] != 'all':
            for i in range(len(l_username)):
                if l_username[i] == varUsername[0]:
                    # print(l_username[i])
                    Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                    self.residentHealthRecord(l_username[i])
        elif len(varUsername) > 1:
            print(varUsername)
            for i in range(len(l_username)):
                for j in range(len(varUsername)):
                    if l_username[i] == varUsername[j]:
                        # print(l_username[i])
                        Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                        self.residentHealthRecord(l_username[i])
                        # 关闭当前标签
                        l_a = Web_PO.getAttrValueByXs("//a",'href')
                        # print(l_a)
                        for i in range(len(l_a)):
                            if "http://192.168.0.203:30080/#/phs/personalAddOrUpdate/addOrUpdate" in l_a[i]:
                                Web_PO.clkByX('/html/body/div[1]/div/div[3]/div[1]/div/div/div[1]/div/a[' + str(i + 1) + ']/span', 2)
        elif len(varUsername) == 1 and varUsername[0] == 'all':
            print(l_username)
            for i in range(len(l_username)):
                Web_PO.clkByX('/html/body/div[1]/div/div[3]/section/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[1]/div', 2)
                self.residentHealthRecord(l_username[i])
                # 关闭当前标签
                l_a = Web_PO.getAttrValueByXs("//a", 'href')
                for i in range(len(l_a)):
                    if "http://192.168.0.203:30080/#/phs/personalAddOrUpdate/addOrUpdate" in l_a[i]:
                        Web_PO.clkByX(
                            '/html/body/div[1]/div/div[3]/div[1]/div/div/div[1]/div/a[' + str(i + 1) + ']/span', 2)

    def _residentHealthRecord(self, l_div, i, varDisease, varDiseaseName, varDiseaseTime):

        #  _residentHealthRecord(self, l_div, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
        if l_div[i] == varDisease:
            ele_n = l_div.index(l_div[i])
            ele_after_n = ele_n + 1
            a = len(l_div[ele_after_n].split("\n"))
            # print(a)
            if a == 1:
                l_div[ele_after_n] = varDiseaseName
                ele_n = l_div.index(l_div[ele_after_n])
                ele_after_n = ele_n + 1
                l_div.insert(ele_after_n, varDiseaseTime)
            else:
                l_ = l_div[ele_after_n].split("\n")
                # print(l_)  # ['手术名称', '手术名称', '手术名称']
                if len(l_) > 1:
                    l_div[ele_after_n] = varDiseaseName + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, varDiseaseTime + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(len(l_) - 1):
                        l_div.insert(ele_after_n + j, varDiseaseName + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, varDiseaseTime + str(j + 2))

    def residentHealthRecord(self, varUsername):

        # 居民健康档案

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//div[@class='table_line']/div")
        print("1.1 原始l_div => ", l_div)

        # 1.2 清洗字段
        # 删除
        l_div = [i for i in l_div if i != '']
        for i in range(len(l_div)):
            if l_div[i] == '现住址必填':
                l_div.remove('现住址必填')
            if l_div[i] == '关联户主':
                l_div.remove('关联户主')
        l_div.remove('城镇职工基本医疗保险')
        l_div.remove('城镇居民基本医疗保险')
        l_div.remove('贫困救助')

        # 修改
        for i in range(len(l_div)):
            if l_div[i] == '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾\n残疾情况必填':
                l_div[i] = '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾'
            if l_div[i] == '商业医疗保险\n全公费\n全自费\n其他':
                l_div[i] = '医疗费用支付方式\n城镇职工基本医疗保险'

        # 插入
        l_div[l_div.index('遗传病史\n有\n无') + 1] = '遗传病史疾病名称'
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 1, '职工医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 2, '医疗费用支付方式2\n城镇居民基本医疗保险')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 3, '居民医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 4, '医疗费用支付方式3\n贫困救助')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 5, '贫困救助卡号')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 6, '医疗费用支付方式4\n商业医疗保险\n全公费\n全自费\n其他')
        l_div.insert(l_div.index('医疗费用支付方式\n城镇职工基本医疗保险') + 7, '医疗费用支付方式备注')

        # 动态自增字段 （33是随意值，确保遍历不中断）
        for i in range(len(l_div) + 33):
            if l_div[i] == '更新内容':
                break

            # 既往史，动态自增字段（选择恶性肿瘤时，显示输入框）
            self._residentHealthRecord(l_div, i, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
            self._residentHealthRecord(l_div, i, '手术\n有\n无', '手术名称', '手术时间')
            self._residentHealthRecord(l_div, i, '外伤\n有\n无', '外伤名称', '外伤时间')
            self._residentHealthRecord(l_div, i, '输血\n有\n无', '输血原因', '输血时间')

            # 家族史，动态自增字段（选择恶性肿瘤时，显示输入框）
            if l_div[i] == '有\n无':
                l_div[i] = '家族史\n有\n无'
                ele_n = l_div.index(l_div[i])
                ele_after_n = ele_n + 1
                if l_div[ele_after_n] == '疾病名称\n与本人关系':
                    l_div[ele_after_n] = '家族史疾病名称'
                    l_div.insert(ele_after_n + 1, "与本人关系")
                else:
                    n = int(len(l_div[ele_after_n].split("\n")) / 2)
                    l_div[ele_after_n] = '家族史疾病名称' + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, "与本人关系" + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(n - 1):
                        l_div.insert(ele_after_n + j, '家族史疾病名称' + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, "与本人关系" + str(j + 2))

        # print('1.2 清洗l_div => ', l_div)


        # 2 生成checkbox字典
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"
        # el-radio__input is-disabled is-checked
        d_radio = {}
        d_checkbox = {}
        l_2 = []
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4,d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 生成d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}


        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')

        # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
        if d_checkbox['药物过敏史']['其他药物过敏源'] == 'True':
            l_field.insert(l_field.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')
            # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
            l_textarea = Web_PO.getAttrValueByXs("//div/div/div/textarea", 'value')
            # 在input中23位置插入textarea值
            l_input.insert(23, l_textarea[0])
            print('3.3 l_textarea => ', l_textarea)
            # 更新div
            l_div.insert(l_div.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')

        # 当残疾情况中选择其他残疾时，显示输入框（其他残疾备注）
        if d_checkbox['残疾情况']['其他残疾'] == 'True':
            l_field.insert(l_field.index('残疾证号'), '其他残疾备注')
            # 更新div
            l_div.insert(l_div.index('残疾证号'), '其他残疾备注')

        # 如果既往史或家族史中疾病名称选择了恶性肿瘤，显示输入框（恶性肿瘤备注），插入XXX恶性肿瘤备注字段
        for i in range(len(l_input)):
            if l_input[i] == '恶性肿瘤':
                p = l_field[i - 5] + '恶性肿瘤备注'
                l_field.insert(i - 4, p)
                # 更新div
                for j in range(len(l_div)):
                    ele_n = l_div.index(l_field[i - 5])
                    l_div.insert(ele_n + 1, l_field[i - 5] + '恶性肿瘤备注')

        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(6))
        l_input.insert(6, ll)
        d_normal = dict(zip(l_field, l_input))
        # print(100, d_normal)  # {'管理卡号': '135', '其他情况说明': '', ...
        d_normal.update(d_checkbox)
        # print('混合结果 =>', d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result

    def residentHealthRecord_update(self, varUsername, varTestUrl):

        # 居民健康档案(更新健康档案)

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//div[@class='table_line']/div")
        # print("1.1 原始l_div => ", l_div)

        # 1.2 清洗字段
        # 删除
        l_div = [i for i in l_div if i != '']
        for i in range(len(l_div)):
            if l_div[i] == '现住址必填':
                l_div.remove('现住址必填')
            if l_div[i] == '关联户主':
                l_div.remove('关联户主')
        l_div.remove('城镇职工基本医疗保险')
        l_div.remove('城镇居民基本医疗保险')
        l_div.remove('贫困救助')

        # 修改
        for i in range(len(l_div)):
            if l_div[i] == '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾\n残疾情况必填':
                l_div[i] = '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾'
            if l_div[i] == '商业医疗保险\n全公费\n全自费\n其他':
                l_div[i] = '医疗费用支付方式1\n城镇职工基本医疗保险'

        # 插入
        l_div[l_div.index('遗传病史\n有\n无') + 1] = '遗传病史疾病名称'
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 1, '职工医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 2, '医疗费用支付方式2\n城镇居民基本医疗保险')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 3, '居民医保卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 4, '医疗费用支付方式3\n贫困救助')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 5, '贫困救助卡号')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 6, '医疗费用支付方式4\n商业医疗保险\n全公费\n全自费\n其他')
        l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 7, '医疗费用支付方式备注')

        # 动态自增字段 （33是随意值，确保遍历不中断）
        for i in range(len(l_div) + 33):
            if l_div[i] == '建档人':
                break

            # 既往史，动态自增字段（选择恶性肿瘤时，显示输入框）
            self._residentHealthRecord(l_div, i, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
            self._residentHealthRecord(l_div, i, '手术\n有\n无', '手术名称', '手术时间')
            self._residentHealthRecord(l_div, i, '外伤\n有\n无', '外伤名称', '外伤时间')
            self._residentHealthRecord(l_div, i, '输血\n有\n无', '输血原因', '输血时间')

            # 家族史，动态自增字段（选择恶性肿瘤时，显示输入框）
            if l_div[i] == '有\n无':
                l_div[i] = '家族史\n有\n无'
                ele_n = l_div.index(l_div[i])
                ele_after_n = ele_n + 1
                if l_div[ele_after_n] == '疾病名称\n与本人关系':
                    l_div[ele_after_n] = '家族史疾病名称'
                    l_div.insert(ele_after_n + 1, "与本人关系")
                else:
                    n = int(len(l_div[ele_after_n].split("\n")) / 2)
                    l_div[ele_after_n] = '家族史疾病名称' + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, "与本人关系" + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(n - 1):
                        l_div.insert(ele_after_n + j, '家族史疾病名称' + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, "与本人关系" + str(j + 2))
        # print('1.2 清洗l_div => ', l_div)

        # 2 生成checkbox字典
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(len(l_isRadioStatus), l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"
        # el-radio__input is-disabled is-checked
        d_radio = {}
        d_checkbox = {}
        l_2 = []
        ee = 0
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(len(l_1), l_1)  # ['户籍', '非户籍']
                # ee = ee + len(l_1)
                # print(ee)
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4,d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')

        # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
        if d_checkbox['药物过敏史']['其他药物过敏源'] == 'True':
            l_field.insert(l_field.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')
            # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
            l_textarea = Web_PO.getAttrValueByXs("//div/div/div/textarea", 'value')
            # 在input中23位置插入textarea值
            l_input.insert(23, l_textarea[0])
            print('3.3 l_textarea => ', l_textarea)
            # 更新div
            l_div.insert(l_div.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')

        # 当残疾情况中选择其他残疾时，显示输入框（其他残疾备注）
        if d_checkbox['残疾情况']['其他残疾'] == 'True':
            l_field.insert(l_field.index('残疾证号'), '其他残疾备注')
            # 更新div
            l_div.insert(l_div.index('残疾证号'), '其他残疾备注')

        # 如果既往史或家族史中疾病名称选择了恶性肿瘤，显示输入框（恶性肿瘤备注），插入XXX恶性肿瘤备注字段
        for i in range(len(l_input)):
            if l_input[i] == '恶性肿瘤':
                p = l_field[i - 5] + '恶性肿瘤备注'
                l_field.insert(i - 4, p)
                # 更新div
                for j in range(len(l_div)):
                    ele_n = l_div.index(l_field[i - 5])
                    l_div.insert(ele_n + 1, l_field[i - 5] + '恶性肿瘤备注')

        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(6))
        l_input.insert(6, ll)
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        # print('d_normal =>', d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result


    def physicalExamination(self, varUsername, varTestUrl):

        # 健康体检

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//div[@class='table_line']/div")
        print("1.1 原始l_div => ", l_div)

        # 1.2 清洗字段
        # 删除
        l_div = [i for i in l_div if i != '']
        # for i in range(len(l_div)):
        #     if l_div[i] == '现住址必填':
        #         l_div.remove('现住址必填')
        #     if l_div[i] == '关联户主':
        #         l_div.remove('关联户主')
        # l_div.remove('城镇职工基本医疗保险')
        # l_div.remove('城镇居民基本医疗保险')
        # l_div.remove('贫困救助')

        # 修改
        # for i in range(len(l_div)):
        #     if l_div[i] == '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾\n残疾情况必填':
        #         l_div[i] = '残疾情况\n无残疾\n视力残疾\n听力残疾\n言语残疾\n肢体残疾\n智力残疾\n精神残疾\n其他残疾'
        #     if l_div[i] == '商业医疗保险\n全公费\n全自费\n其他':
        #         l_div[i] = '医疗费用支付方式1\n城镇职工基本医疗保险'

        # 插入
        # l_div[l_div.index('遗传病史\n有\n无') + 1] = '遗传病史疾病名称'
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 1, '职工医保卡号')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 2, '医疗费用支付方式2\n城镇居民基本医疗保险')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 3, '居民医保卡号')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 4, '医疗费用支付方式3\n贫困救助')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 5, '贫困救助卡号')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 6, '医疗费用支付方式4\n商业医疗保险\n全公费\n全自费\n其他')
        # l_div.insert(l_div.index('医疗费用支付方式1\n城镇职工基本医疗保险') + 7, '医疗费用支付方式备注')

        # 动态自增字段 （33是随意值，确保遍历不中断）
        for i in range(len(l_div) + 33):
            if l_div[i] == '建档人':
                break

            # 既往史，动态自增字段（选择恶性肿瘤时，显示输入框）
            self._residentHealthRecord(l_div, i, '疾病\n有\n无', '既往史疾病名称', '确诊时间')
            self._residentHealthRecord(l_div, i, '手术\n有\n无', '手术名称', '手术时间')
            self._residentHealthRecord(l_div, i, '外伤\n有\n无', '外伤名称', '外伤时间')
            self._residentHealthRecord(l_div, i, '输血\n有\n无', '输血原因', '输血时间')

            # 家族史，动态自增字段（选择恶性肿瘤时，显示输入框）
            if l_div[i] == '有\n无':
                l_div[i] = '家族史\n有\n无'
                ele_n = l_div.index(l_div[i])
                ele_after_n = ele_n + 1
                if l_div[ele_after_n] == '疾病名称\n与本人关系':
                    l_div[ele_after_n] = '家族史疾病名称'
                    l_div.insert(ele_after_n + 1, "与本人关系")
                else:
                    n = int(len(l_div[ele_after_n].split("\n")) / 2)
                    l_div[ele_after_n] = '家族史疾病名称' + "1"
                    ele_n = l_div.index(l_div[ele_after_n])
                    ele_after_n = ele_n + 1
                    l_div.insert(ele_after_n, "与本人关系" + "1")
                    ele_after_n = ele_after_n + 1
                    for j in range(n - 1):
                        l_div.insert(ele_after_n + j, '家族史疾病名称' + str(j + 2))
                        ele_n = l_div.index(l_div[ele_after_n + j])
                        ele_after_n = ele_n + 1
                        l_div.insert(ele_after_n, "与本人关系" + str(j + 2))
        print('1.2 清洗l_div => ', l_div)

        # 2 生成checkbox字典
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        # print(len(l_isRadioStatus), l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        # class="el-checkbox__input is-disabled is-checked"
        # el-radio__input is-disabled is-checked
        d_radio = {}
        d_checkbox = {}
        l_2 = []
        ee = 0
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(len(l_1), l_1)  # ['户籍', '非户籍']
                # ee = ee + len(l_1)
                # print(ee)
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4,d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')

        # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
        if d_checkbox['药物过敏史']['其他药物过敏源'] == 'True':
            l_field.insert(l_field.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')
            # 当药物过敏史中选择其他药物过敏源时，显示文本域输入框（医疗费用支付方式备注）
            l_textarea = Web_PO.getAttrValueByXs("//div/div/div/textarea", 'value')
            # 在input中23位置插入textarea值
            l_input.insert(23, l_textarea[0])
            print('3.3 l_textarea => ', l_textarea)
            # 更新div
            l_div.insert(l_div.index('医疗费用支付方式备注') + 1, '其他药物过敏源备注')

        # 当残疾情况中选择其他残疾时，显示输入框（其他残疾备注）
        if d_checkbox['残疾情况']['其他残疾'] == 'True':
            l_field.insert(l_field.index('残疾证号'), '其他残疾备注')
            # 更新div
            l_div.insert(l_div.index('残疾证号'), '其他残疾备注')

        # 如果既往史或家族史中疾病名称选择了恶性肿瘤，显示输入框（恶性肿瘤备注），插入XXX恶性肿瘤备注字段
        for i in range(len(l_input)):
            if l_input[i] == '恶性肿瘤':
                p = l_field[i - 5] + '恶性肿瘤备注'
                l_field.insert(i - 4, p)
                # 更新div
                for j in range(len(l_div)):
                    ele_n = l_div.index(l_field[i - 5])
                    l_div.insert(ele_n + 1, l_field[i - 5] + '恶性肿瘤备注')

        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)

        # # 将居住地址6个值（索引5）组成列表
        ll = []
        for i in range(6):
            ll.append(l_input.pop(6))
        l_input.insert(6, ll)
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        # print('d_normal =>', d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result

    def phthisisVisit(self, varUsername, varTestUrl):

        # 肺结核患者第一次入户随访记录表

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//form/div")
        # print("1.1 原始l_div => ", l_div)

        # # 1.2 清洗字段
        # # 删除
        l_div.remove("肺结核患者第一次入户随访记录表")
        # # 插入
        l_div.insert(l_div.index('随访日期\n随访方式\n门诊\n家庭\n电话'), '随访日期')
        # 用药
        l_div.insert(l_div.index('用药\n化疗方案\n用法\n每日\n间歇\n药品剂型\n固定剂量复合制剂\n散装药\n板式组合药\n注射剂'), '化疗方案')
        l_div.insert(l_div.index('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天'), '吸烟1')
        l_div.insert(l_div.index('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天') + 1, '吸烟2')
        l_div.insert(l_div.index('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天') + 2, '饮酒1')
        l_div.insert(l_div.index('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天') + 3, '饮酒2')
        l_div.remove('生活方式评估\n吸烟\n支/天\n支/天\n饮酒\n两/天\n两/天')
        l_div.insert(l_div.index('化疗方案'), '症状及体征其他')
        # 健康教育及培训
        l_div.insert(l_div.index('健康教育及培训\n取药地点、时间\n服药记录卡的填写\n掌握\n未掌握\n服药方法及药品存放\n掌握\n未掌握\n肺结核治疗疗程\n掌握\n未掌握\n不规律服药危害\n掌握\n未掌握\n服药后不良反应及处理\n掌握\n未掌握\n治疗期间复诊查痰\n掌握\n未掌握\n外出期间如何坚持服药\n掌握\n未掌握\n生活习惯及注意事项\n掌握\n未掌握\n密切接触者检查\n掌握\n未掌握'),  '取药地点')
        l_div.insert(l_div.index('健康教育及培训\n取药地点、时间\n服药记录卡的填写\n掌握\n未掌握\n服药方法及药品存放\n掌握\n未掌握\n肺结核治疗疗程\n掌握\n未掌握\n不规律服药危害\n掌握\n未掌握\n服药后不良反应及处理\n掌握\n未掌握\n治疗期间复诊查痰\n掌握\n未掌握\n外出期间如何坚持服药\n掌握\n未掌握\n生活习惯及注意事项\n掌握\n未掌握\n密切接触者检查\n掌握\n未掌握') + 1,  '取药时间')
        l_div.remove('健康教育及培训\n取药地点、时间\n服药记录卡的填写\n掌握\n未掌握\n服药方法及药品存放\n掌握\n未掌握\n肺结核治疗疗程\n掌握\n未掌握\n不规律服药危害\n掌握\n未掌握\n服药后不良反应及处理\n掌握\n未掌握\n治疗期间复诊查痰\n掌握\n未掌握\n外出期间如何坚持服药\n掌握\n未掌握\n生活习惯及注意事项\n掌握\n未掌握\n密切接触者检查\n掌握\n未掌握')
        # # 修改
        for i in range(len(l_div) + 33):
            # 随访方式
            if l_div[i] == '随访日期\n随访方式\n门诊\n家庭\n电话':
                l_div[i] = '随访方式\n门诊\n家庭\n电话'
            # 患者类型\痰菌情况
            if l_div[i] == '患者类型\n初治\n复治\n痰菌情况\n阳性\n阴性\n未查痰':
                l_div[i] = '患者类型\n初治\n复治'
                l_div.insert(l_div.index(l_div[i]) + 1, '痰菌情况\n阳性\n阴性\n未查痰')
            # # 症状及体征
            if l_div[i] == '症状及体征\n没有症状\n咳嗽咳痰\n低热盗汗\n咯血或血痰\n胸痛消瘦\n恶心纳差\n头痛失眠\n视物模糊\n皮肤瘙痒皮疹\n耳鸣听力下降\n其他\n其他':
                l_div[i] = '症状及体征\n没有症状\n咳嗽咳痰\n低热盗汗\n咯血或血痰\n胸痛消瘦\n恶心纳差\n头痛失眠\n视物模糊\n皮肤瘙痒皮疹\n耳鸣听力下降\n其他'
            # 用药
            if l_div[i] == '用药\n化疗方案\n用法\n每日\n间歇\n药品剂型\n固定剂量复合制剂\n散装药\n板式组合药\n注射剂':
                l_div[i] = '用法\n每日\n间歇'
                l_div.insert(l_div.index(l_div[i]) + 1, '药品剂型\n固定剂量复合制剂\n散装药\n板式组合药\n注射剂')
            # 家庭居住环境
            if l_div[i] == '家庭居住环境\n单独的居室\n无\n有\n通风情况\n良好\n一般\n差':
                l_div[i] = '单独的居室\n无\n有'
                l_div.insert(l_div.index(l_div[i]) + 1, '通风情况\n良好\n一般\n差')
            if l_div[i] == '取药时间':
                l_div.insert(l_div.index(l_div[i]) + 1, '服药记录卡的填写\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 2, '服药方法及药品存放\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 3, '肺结核治疗疗程\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 4, '不规律服药危害\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 5, '服药后不良反应及处理\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 6, '治疗期间复诊查痰\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 7, '外出期间如何坚持服药\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 8, '生活习惯及注意事项\n掌握\n未掌握')
                l_div.insert(l_div.index(l_div[i]) + 9, '密切接触者检查\n掌握\n未掌握')
            if l_div[i] == '下次随访日期\n随访医生\n患者（家属）签字':
                l_div.insert(l_div.index(l_div[i]), '下次随访日期')
                l_div.insert(l_div.index(l_div[i])+1, '随访医生')
                l_div.insert(l_div.index(l_div[i])+2, '患者（家属）签字')
                l_div.remove('下次随访日期\n随访医生\n患者（家属）签字')
                break
        # print('1.2 清洗l_div => ', l_div)

        # 2 生成checkbox字典
        # l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        d_radio = {}
        d_checkbox = {}
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4, d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        # 选择其他，显示输入框
        if d_checkbox['督导人员选择']['其他'] == 'True':
            l_field.insert(l_field.index('吸烟1'), '督导人员选择其他备注')
            l_div.insert(l_div.index('吸烟1'), '督导人员选择其他备注')  # 更新div
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)
        # print('3.3 d_normal => ', , d_normal)  # {'管理卡号': '135', '其他情况说明': '', ...

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ',  d_result)
        # return d_result


    def _checkbox(self, var_l_div, varContainClassValue):

        # _checkbox(l_div, 'el-radio__input is-disabled is-checked')
        l_tmp = []
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', varContainClassValue)
        l_tmp = l_isRadioStatus[-2:]
        print(l_tmp)  # ['False', 'True', 'False', 'False', ...
        d_radio = {}
        d_checkbox = {}
        for i in range(len(var_l_div)):
            if "\n" in var_l_div[i]:
                ele_n = var_l_div.index(var_l_div[i])
                l_1 = var_l_div[i].split("\n")
                l_1.pop(0)
                print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_tmp.pop(0))

                d_box = dict(zip(l_1, l_bool))
                print(4, d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[var_l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k, v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        print('d_checkbox2 => ', d_checkbox)

        return d_checkbox

    def pregnantWoman(self, varUsername, varTestUrl):

        # 孕产妇

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        # l_div = Web_PO.getTextByXs("//form/div")
        # print("1.1 原始l_div => ", l_div)

        l_div = ['填表日期','是否高危产妇\n是\n否', '丈夫姓名', '丈夫年龄', '丈夫电话', '孕次', '阴1道分娩', '剖宫产', '末次月经\n不详', '周', '天','预产期',
                 '既往史\n无\n心脏病\n肾脏疾病\n肝脏疾病\n高血压\n贫血\n糖尿病\n其他',
                 '家族史\n无\n遗传性疾病史\n精神病史\n其他', '妇科手术史\n有\n无',
                 '个人史\n无特殊\n吸烟\n饮酒\n服用药物\n接触有毒害物质\n接触放射线\n其他',
                 '自然流产', '人工流产','死胎', '死产', '新生儿死亡', '出生缺陷儿',
                 '身高(cm)', '体重(kg)', '体质指数(kg/m²)', '血压收缩压','血压舒张压',
                 '听诊心脏\n未见异常\n异常','听诊肺部\n未见异常\n异常',
                 '外阴\n未见异常\n异常', '阴道\n未见异常\n异常', '宫颈\n未见异常\n异常', '子宫\n未见异常\n异常', '附件\n未见异常\n异常',
                 '血红蛋白值','白细胞计数值','血小板计数值','血常规其他' ,
                 '尿蛋白','尿糖','尿酮体','尿潜血','尿常规其他',
                 '血型\nA型\nB型\nO型\nAB型\n不详','RH血型\nRh阴性\nRh阳性\n不详','血糖',
                 '血清谷丙转氨酶','血清谷草转氨酶','白蛋白','总胆红素','结合胆红素',
                 '血清肌酐','血尿素',
                 '阴道分泌物\n未见异常\n滴虫\n假丝酵母菌\n其他', '阴道清洁度\nI度\nII度\nIII度\nIV度',
                 '乙型肝炎表面抗原','乙型肝炎表面抗体','乙型肝炎e抗原','乙型肝炎e抗体','乙型肝炎核心抗体',
                 '梅毒血清学试验\n阴性\n阳性','HIV抗体检测\n阴性\n阳性',
                 'B超','辅助检查其他',
                 '总体评估\n未见异常\n异常',
                 '保健指导\n生活方式\n心理\n营养\n避免致畸因素和疾病对胚胎的不良影响\n产前筛选宣传告知\n其他',
                 '建册情况\n本次随访同时建册\n已在其他机构建册','建册日期','建册单位',
                 '转诊\n有\n无',
                 '下次访视时间','随访医生签名','居民签名']
        # l_field.insert(l_field.index('末次月经\n不详'), '末次月经日期')

        # 2 生成checkbox字典
        # l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        d_radio = {}
        d_checkbox = {}
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4, d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        # print(l_field)
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        if d_checkbox['末次月经']['不详'] == 'False':
            l_field.insert(l_field.index('周'), '末次月经日期')
            l_div.insert(l_div.index('周'), '末次月经日期')  # 更新div
        if d_checkbox['既往史']['其他'] == 'True':
            # l_field.insert(l_field.index('自然流产'), '既往史其他备注')
            l_div.insert(l_div.index('既往史\n无\n心脏病\n肾脏疾病\n肝脏疾病\n高血压\n贫血\n糖尿病\n其他')+1 , '既往史其他备注')  # 更新div
        if d_checkbox['家族史']['其他'] == 'True':
            # l_field.insert(l_field.index('自然流产'), '家族史其他备注')
            l_div.insert(l_div.index('家族史\n无\n遗传性疾病史\n精神病史\n其他')+1, '家族史其他备注')  # 更新div
        if d_checkbox['妇科手术史']['有'] == 'True':
            # l_field.insert(l_field.index('自然流产'), '妇科手术史有备注')
            l_div.insert(l_div.index('妇科手术史\n有\n无')+1, '妇科手术史有备注')  # 更新div
        if d_checkbox['个人史']['其他'] == 'True':
            # l_field.insert(l_field.index('自然流产'), '个人史其他备注')
            l_div.insert(l_div.index('个人史\n无特殊\n吸烟\n饮酒\n服用药物\n接触有毒害物质\n接触放射线\n其他')+1, '个人史其他备注')  # 更新div
        if d_checkbox['听诊心脏']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '心脏异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '心脏异常备注')  # 更新div
        if d_checkbox['听诊肺部']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '肺部异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '肺部异常备注')  # 更新div
        if d_checkbox['外阴']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '外阴异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '外阴异常备注')  # 更新div
        if d_checkbox['阴道']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '阴道异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '阴道异常备注')  # 更新div
        if d_checkbox['宫颈']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '宫颈异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '宫颈异常备注')  # 更新div
        if d_checkbox['子宫']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '子宫异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '子宫异常备注')  # 更新div
        if d_checkbox['附件']['异常'] == 'True':
            # l_field.insert(l_field.index('血红蛋白值'), '附件异常备注')
            l_div.insert(l_div.index('血红蛋白值'), '附件异常备注')  # 更新div
        if d_checkbox['阴道分泌物']['其他'] == 'True':
            # l_field.insert(l_field.index('乙型肝炎表面抗原'), '阴道分泌物其他备注')
            l_div.insert(l_div.index('阴道分泌物\n未见异常\n滴虫\n假丝酵母菌\n其他')+1, '阴道分泌物其他备注')  # 更新div
        if d_checkbox['总体评估']['异常'] == 'True':
            # l_field.insert(l_field.index('总体评估\n未见异常\n异常'), '总体评估异常备注')
            l_div.insert(l_div.index('总体评估\n未见异常\n异常')+1, '总体评估异常备注')  # 更新div
        if d_checkbox['保健指导']['其他'] == 'True':
            # l_field.insert(l_field.index('建册日期'), '保健指导其他备注')
            l_div.insert(l_div.index('保健指导\n生活方式\n心理\n营养\n避免致畸因素和疾病对胚胎的不良影响\n产前筛选宣传告知\n其他')+1, '保健指导其他备注')  # 更新div
        if d_checkbox['转诊']['有'] == 'True':
            # l_field.insert(l_field.index('下次访视时间'), '转诊原因')
            l_div.insert(l_div.index('下次访视时间'), '转诊原因')  # 更新div
            # l_field.insert(l_field.index('下次访视时间'), '转诊机构及科室')
            l_div.insert(l_div.index('下次访视时间'), '转诊机构及科室')  # 更新div
            # l_field.insert(l_field.index('下次访视时间'), '转诊联系人')
            l_div.insert(l_div.index('下次访视时间'), '转诊联系人')  # 更新div
            # l_field.insert(l_field.index('下次访视时间'), '转诊方式')
            l_div.insert(l_div.index('下次访视时间'), '转诊方式')  # 更新div
            # l_field.insert(l_field.index('下次访视时间'), '结果\n到位\n未到位')
            l_div.insert(l_div.index('下次访视时间'), '结果\n到位\n未到位')  # 更新div
            d_checkbox2 = self._checkbox(['结果\n到位\n未到位'], 'is-disabled is-checked')

        if d_checkbox['建册情况']['已在其他机构建册'] == 'True':
            # l_field.insert(l_field.index('建册日期'), '已在其他机构建册备注')
            l_div.insert(l_div.index('建册情况\n本次随访同时建册\n已在其他机构建册'), '已在其他机构建册备注')  # 更新div
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        d_normal.update(d_checkbox2)
        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)
        print('3.3 d_normal_checkbox => ', d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
            # for k, v in d_checkbox2.items():
            #     if k in l_div[i]:
            #         d_result[k] = v
        print(varUsername + ' => ', d_result)
        # return d_result


    def hypophrenia(self, varUsername, varTestUrl):

        # 严重精神障碍患者

        Web_PO.opnLabel(varTestUrl)
        Web_PO.swhLabel(1)

        # 1.1 获取字段
        l_div = Web_PO.getTextByXs("//form/div")
        # print("1.1 原始l_div => ", l_div)

        # # 1.2 清洗字段
        # # 删除
        l_div = [i for i in l_div if i != '']
        l_div.remove("严重精神障碍患者个人信息补充表")
        # # 插入
        l_div.insert(l_div.index('档案编号\n监护人姓名\n与患者关系'), '档案编号')
        l_div.insert(l_div.index('档案编号\n监护人姓名\n与患者关系'), '监护人姓名')
        l_div.insert(l_div.index('档案编号\n监护人姓名\n与患者关系'), '与患者关系')
        l_div.remove('档案编号\n监护人姓名\n与患者关系')
        l_div.insert(l_div.index('监护人地址\n监护人电话'), '监护人地址')
        l_div.insert(l_div.index('监护人地址\n监护人电话'), '监护人电话')
        l_div.remove('监护人地址\n监护人电话')
        l_div.insert(l_div.index('辖区村(居)委联系人\n联系人电话'), '辖区村(居)委联系人')
        l_div.insert(l_div.index('辖区村(居)委联系人\n联系人电话'), '联系人电话')
        l_div.remove('辖区村(居)委联系人\n联系人电话')
        l_div.insert(l_div.index('知情同意\n不同意参加管理\n同意参加管理\n签字\n签字日期') + 1, '签字日期')
        l_div.insert(l_div.index('知情同意\n不同意参加管理\n同意参加管理\n签字\n签字日期') + 1, '签字')
        l_div.insert(l_div.index('重性精神疾病分类\n精神分裂症\n双向障碍\n偏执性精神病\n分裂情感障碍\n癫痫所致精神障碍\n精神发育迟滞伴发精神障碍\n其他\n初次发病时间') + 1, '初次发病时间')
        l_div.insert(l_div.index('既往治疗情况\n门诊\n未治\n间断门诊治疗\n连续门诊治疗\n住院\n曾住精神病专科医院/综合医院精神专科\n次') + 1, '住院')
        l_div.insert(l_div.index('目前诊断情况\n诊断\n确诊医院\n确诊日期'), '诊断')
        l_div.insert(l_div.index('目前诊断情况\n诊断\n确诊医院\n确诊日期'), '确诊医院')
        l_div.insert(l_div.index('目前诊断情况\n诊断\n确诊医院\n确诊日期'), '确诊日期')
        l_div.remove('目前诊断情况\n诊断\n确诊医院\n确诊日期')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '自杀未遂')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '自伤')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '其他危害行为')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '肇祸')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '肇事')
        l_div.insert(l_div.index('危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次') + 1 , '轻度滋事')
        l_div.insert(l_div.index('建卡日期\n登记人\n建卡医疗机构') , '建卡日期')
        l_div.insert(l_div.index('建卡日期\n登记人\n建卡医疗机构') , '登记人')
        l_div.insert(l_div.index('建卡日期\n登记人\n建卡医疗机构') , '建卡医疗机构')
        l_div.remove('建卡日期\n登记人\n建卡医疗机构')
        # # 修改
        for i in range(len(l_div) + 33):
            if l_div[i] == '知情同意\n不同意参加管理\n同意参加管理\n签字\n签字日期':
                l_div[i] = '知情同意\n不同意参加管理\n同意参加管理'
            if l_div[i] == '重性精神疾病分类\n精神分裂症\n双向障碍\n偏执性精神病\n分裂情感障碍\n癫痫所致精神障碍\n精神发育迟滞伴发精神障碍\n其他\n初次发病时间':
                l_div[i] = '重性精神疾病分类\n精神分裂症\n双向障碍\n偏执性精神病\n分裂情感障碍\n癫痫所致精神障碍\n精神发育迟滞伴发精神障碍\n其他'
            if l_div[i] == '既往治疗情况\n门诊\n未治\n间断门诊治疗\n连续门诊治疗\n住院\n曾住精神病专科医院/综合医院精神专科\n次':
                l_div[i] = '既往治疗情况门诊\n未治\n间断门诊治疗\n连续门诊治疗'
            if l_div[i] == '危险行为\n无\n有\n轻度滋事\n次,\n肇事\n次,\n肇祸\n次,\n其他危害行为\n次,\n自伤\n次,\n自杀未遂\n次':
                l_div[i] = '危险行为\n无\n有'
            if l_div[i] == '建卡医疗机构':
                break
        # print('1.2 清洗l_div => ', l_div)

        # 2 生成checkbox字典
        # l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', '__input is-disabled is-checked')
        l_isRadioStatus = Web_PO.isBooleanAttrContainValueListByX("//div/label/span[1]", 'class', 'is-checked')
        # print(l_isRadioStatus)  # ['False', 'True', 'False', 'False', ...
        d_radio = {}
        d_checkbox = {}
        for i in range(len(l_div)):
            if "\n" in l_div[i] :
                ele_n = l_div.index(l_div[i])
                l_1 = l_div[i].split("\n")
                l_1.pop(0)
                # print(l_1)  # ['户籍', '非户籍']
                l_bool = []
                for i in range(len(l_1)):
                    l_bool.append(l_isRadioStatus.pop(0))
                d_box = dict(zip(l_1, l_bool))
                # print(4, d_box)  # {'户籍': 'True', '非户籍': 'False'}
                d_radio[l_div[ele_n]] = d_box
        l_3 = []
        l_4 = []
        for k,v in d_radio.items():
            a = k.split("\n")[0]
            l_3.append(a)
            l_4.append(v)
        d_checkbox = dict(zip(l_3, l_4))
        # print(d_radio)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}
        # print('2 d_checkbox => ', d_checkbox)  # {'病例来源': {'健康档案': 'False', '社区门诊': 'True', '流行病学调查': 'False', '其他': 'False'}, '婚姻状况': {'未婚': 'False', '已婚': 'True', '初婚': 'False', '再婚': 'False', '复婚': 'False', '丧偶': 'False', '离婚': 'False', '未说明的婚姻状况': 'False'}, '糖尿病家族史': {'否': 'False', '是': 'False', '不知道': 'True'}, '糖尿病分型': {'1型糖尿病': 'False', '2型糖尿病': 'True', '妊娠糖尿病': 'False', '其他特殊类型糖尿病': 'False'}, '是否终止管理': {'否': 'True', '是': 'False'}}

        # 3 生成normal字段
        l_field = [i for i in l_div if "\n" not in i]
        l_input = Web_PO.getAttrValueByXs("//div/div/div/input", 'value')
        if d_checkbox['既往主要症状']['其他'] == 'True':
            l_field.insert(l_field.index('住院'), '既往主要症状其他备注')
            l_div.insert(l_div.index('住院'), '既往主要症状其他备注')  # 更新div
        d_normal = dict(zip(l_field, l_input))
        d_normal.update(d_checkbox)
        # print('3.1 l_field => ', l_field)
        # print('3.2 l_input => ', l_input)
        # print('3.3 d_normal_checkbox => ', , d_normal)

        # 4，按页面字段名顺序输出
        d_result = {}
        for i in range(len(l_div)):
            for k, v in d_normal.items():
                if l_div[i] == k:
                    d_result[k] = v
            for k, v in d_checkbox.items():
                if k in l_div[i]:
                    d_result[k] = v
        print(varUsername + ' => ', d_result)
        # return d_result


