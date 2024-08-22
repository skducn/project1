# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2022-7-19
# Description: ERP 对象库
# *****************************************************************


import string, numpy
from string import digits
from PO.HtmlPO import *
from PO.ListPO import *
from PO.TimePO import *
from PO.ColorPO import *
from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.FilePO import *
from PO.StrPO import *
from PO.WebPO import *
from PO.ListPO import *
from PO.CharPO import *

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ErpPO():

    def __init__(self):
        self.List_PO = ListPO()
        self.Time_PO = TimePO()
        self.Color_PO = ColorPO()
        self.List_PO = ListPO()
        self.Str_PO = StrPO()
        self.Char_PO = CharPO()
        self.List_PO = ListPO()
        self.Char_PO = CharPO()

        self.oaURL = "http://192.168.0.65"



    def loginOA(self):

        '''登录oa'''

        self.Web_PO = WebPO("chrome")
        self.Web_PO.openURL(self.oaURL)
        self.Web_PO.driver.maximize_window()  # 全屏
        self.Web_PO.inputId("name", "liuting")
        # self.Web_PO.inputId("password", "")
        self.Web_PO.clickXpath(u"//button[@id='submit']", 2)

    def getToken(self, username):

        '''获取token'''

        url = self.oaURL + "/logincheck.php"
        header = {"content-type": "application/x-www-form-urlencoded"}
        d_iParam = {'USERNAME': username}
        r = requests.post(url, headers=header, data=d_iParam, verify=False)
        a = r.cookies.get_dict()
        url = self.oaURL + "/general/appbuilder/web/business/product/crm"
        r = requests.get(url, headers={"Cookie": "PHPSESSID=" + a["PHPSESSID"]}, verify=False)
        self.token = str(r.url).split("token=")[1]
        # print(self.token)
        return self.token

    def getResponseByApplet(self, url):
        r = requests.get(url,headers={"content-type": "application/json", "token": self.token,"traceId": "123"},verify=False)
        print(r.text)

    def postResponseByApplet(self, url, param):
        r = requests.post(url,headers={"content-type": "application/json", "token": self.token,"traceId": "123"}, json=param, verify=False)
        str1 = r.text.encode('gbk', 'ignore').decode('gbk')
        res_visitAnalysis = json.loads(str1)
        print(res_visitAnalysis)


    def clickMemuOA(self, varMemuName, varSubName):

        '''左侧菜单选择模块及浮层模块（无标题）'''

        sleep(2)
        x = self.Web_PO.getXpathsText("//div")
        list1 = []
        for i in x:
            if "快捷菜单" in i:
                list1.append(i)
                break
        list2 = []
        for i in range(len(str(list1[0]).split("\n"))):
            if Str_PO.isContainChinese(str(list1[0]).split("\n")[i]) == True:
                list2.append(str(list1[0]).split("\n")[i])
        # print(list2)
        for j in range(len(list2)):
            if list2[j] == varMemuName:
                self.Web_PO.clickXpath("//ul[@id='first_menu']/li[" + str(j + 1) + "]", 2)
                x = self.Web_PO.getXpathsText("//li")
                list3 = []
                list4 = []
                for i in x:
                    if varMemuName in i:
                        list3.append(i)
                        break
                # print(list3)
                for i in range(len(str(list3[0]).split("\n"))):
                    if str(list3[0]).split("\n")[i] != varMemuName and Str_PO.isContainChinese(
                            str(list3[0]).split("\n")[i]) == True:
                        list4.append(str(list3[0]).split("\n")[i])
                for k in range(len(list4)):
                    if list4[k] == varSubName:
                        self.Web_PO.clickXpath(
                            "//ul[@id='first_menu']/li[" + str(j + 1) + "]/div[2]/ul/li[" + str(k + 1) + "]/a", 2)

    def clickMemuERP(self, menu1, menu2):

        '''盛蕴ERP管理平台 之菜单树'''

        l_menu1 = self.Web_PO.getXpathsText("//li")
        l_menu1_tmp = self.List_PO.delRepeatElem(l_menu1)
        for i in range(len(l_menu1_tmp)):
            if menu1 in l_menu1_tmp[i]:
                self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/div', 2)
                l_menu2_a = self.Web_PO.getXpathsText('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/ul/li/ul/a')
                # print(l_menu2_a)  # ['拜访分析报表', '会议分析表', '投入产出分析表', '协访分析表', '重点客户投入有效性分析', '开发计划总揽']
                for j in range(len(l_menu2_a)):
                    if menu2 == l_menu2_a[j]:
                        self.Web_PO.clickXpath('//*[@id="app"]/section/section/aside/section/main/div/div[1]/div/ul/li[' + str(i + 1) + ']/ul/li/ul/a[' + str(j + 1) + ']', 2)

        # self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[2]/div/div[1]/input', "1234测试")



    def _visitAnalysis(self, res_visitAnalysis, tbl_report, tblField, iResField, sql, d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO):

        d = {}
        # visitAnalysis( '拜访分析报表', "计划拜访人次", "plannedVisitsNumber", "sql", {"endTime": "2022-06-30  23:59:59", "startTime": "2022-06-01", "uid": 0})
        sign = 0
        sign2 = 0
        l_result = []

        l_rowcol = Openpyxl_PO.getRowCol(varSheet)
        # print(l_rowcol)
        currCol = l_rowcol[1] + 1
        # print(currCol)
        currRow = 2
        Openpyxl_PO.setCellValue(1, currCol, tblField, varSheet)
        # print(tblField)

        if iResField != None and sql == None:
            pass

        elif iResField != None and "%s" in sql:

            # 遍历所有人的字段值
            s = 0
            sql_value = 0
            for i in range(len(res_visitAnalysis['data']['detail'])):
                # print(str(res_visitAnalysis['data']['detail'][i]) # {'delegateId': 84, 'managerName': '廖荣平', 'representativeName': '黄新晖', 'plannedVisitsNumber': 0, 'actualVisitsNumber': 0, 'actualVisitsPersonNumber': 0, 'actualVisitRate': 0, 'twoACustomerVisitNumber': 0, 'twoACustomerVisitRate': 0, 'highPotentialCustomerVisitNumber': 0, 'highPotentialCustomerVisitRate': 0, 'newAddCustomerNumber': 0, 'allNumber': 0, 'actualVisitCoverRate': 0, 'doubleTotal': 0, 'potentialityTotal': 0, 'plannedMeetingFollowNumber': 0, 'actualMeetingFollowNumber': 0, 'actualConcludeMeetingFollowNumber': 0, 'actualConcludeDoubleANumber': 0, 'actualConcludePotentialityNumber': 0, 'doubleARatioRate': 0, 'doubleAFrequencyRate': 0, 'highRatioRate': 0, 'highFrequencyRate': 0, 'meetingFollowRate': 0, 'locationMatchNumber': 0}

                if tbl_report == "拜访分析报表":
                    if Str_PO.getRepeatCount(sql, "%s") == 1:
                        sql1 = sql % (res_visitAnalysis['data']['detail'][i]['delegateId'])
                    elif Str_PO.getRepeatCount(sql, "%s") == 3:
                        sql1 = sql % (res_visitAnalysis['data']['detail'][i]['delegateId'], d_tbl_param["starTime"],
                                      d_tbl_param["endTime"])
                    sql_value = Mysql_PO.execQuery(sql1)

                    if len(sql_value) == 0:
                        sql_value = 0
                    else:
                        if sql_value[0][0] == None:
                            sql_value = 0
                        else:
                            sql_value = sql_value[0][0]

                    # 接口和sql比对
                    s = s + sql_value
                    Openpyxl_PO.setCellValue(currRow, 1, res_visitAnalysis['data']['detail'][i]['managerName'],
                                             varSheet)  # 第1列区域
                    Openpyxl_PO.setCellValue(currRow, 2, res_visitAnalysis['data']['detail'][i]['representativeName'],
                                             varSheet)  # 第二列代表名字

                if res_visitAnalysis['data']['detail'][i][iResField] == sql_value:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value), varSheet)  # 指标值
                else:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value) + "(sql)/" + str(
                        res_visitAnalysis['data']['detail'][i][iResField]), varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

                currRow = currRow + 1
                d[iResField] = s

            Openpyxl_PO.save()


        else:
            # 各比率的计算

            for i in range(len(res_visitAnalysis['data']['detail'])):
                # print(str(res_visitAnalysis['data']['detail'][i])
                if res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] == 0:
                    Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
                else:
                    tmp1 = Data_PO.newRound(res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] /
                                            res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] * 100)
                    if tmp1 == int(res_visitAnalysis['data']['detail'][i][iResField]):
                        Openpyxl_PO.setCellValue(currRow, currCol,
                                                 str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%",
                                                 varSheet)
                        # Openpyxl_PO.setCellValue(currRow, 1, "ok", varSheet)
                    else:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp1) + "%(计算)/" + str(
                            int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                        Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
                currRow = currRow + 1
            Openpyxl_PO.save()

        # 合计
        Openpyxl_PO.setCellValue(currRow, 1, "总计", varSheet)
        Openpyxl_PO.setCellValue(currRow, 2, "None", varSheet)

        if iResField in d:
            if d[iResField] == res_visitAnalysis['data']['total'][iResField]:
                Openpyxl_PO.setCellValue(currRow, currCol, str(res_visitAnalysis['data']['total'][iResField]), varSheet)
                # print(str(res_visitAnalysis['data']['total'][iResField])
            else:
                Openpyxl_PO.setCellValue(currRow, currCol, str(d[iResField]) + "%(计算1)/" + str(
                    res_visitAnalysis['data']['total'][iResField]), varSheet)
                Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
        else:
            if sql != None:
                if res_visitAnalysis['data']['total'][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['total'][
                    sql.split("/")[0]] == 0:
                    Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
                else:
                    tmp = Data_PO.newRound(
                        res_visitAnalysis['data']['total'][sql.split("/")[0]] / res_visitAnalysis['data']['total'][
                            sql.split("/")[1]] * 100)
                    # print(tmp)
                    if tmp == int(res_visitAnalysis['data']['total'][iResField]):
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%", varSheet)
                    else:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%(计算)/" + str(
                            int(res_visitAnalysis['data']['total'][iResField])) + "%", varSheet)
                        Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
        Openpyxl_PO.save()
    def visitAnalysis_I(self, db_ip, iUrl, Openpyxl_PO, Mysql_PO):

        l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
        for i in range(1, len(l_getRowValue_case)):
            if l_getRowValue_case[i][1] == "拜访分析报表":
                tbl_report = l_getRowValue_case[i][1]  # 报表
                d_tbl_param = Str_PO.str2dict(l_getRowValue_case[i][2])  # 参数2字典
                tbl_endTime = d_tbl_param["endTime"]
                tbl_endTime = tbl_endTime.split(" ")[0]
                tbl_startTime = d_tbl_param["starTime"]
                # print(tbl_startTime,tbl_endTime)
                # sys.exit(0)
                varNowTime = str(Time_PO.getDateTime())
                varTitle = "erp_" + tbl_report + "(" + str(tbl_startTime) + "~" + str(tbl_endTime) + ")_" + db_ip + "_" + varNowTime

                # 生成临时sheet
                varSheet = "i"
                Openpyxl_PO.delSheet(varSheet)
                Openpyxl_PO.addSheetCover(varSheet, 99)
                Openpyxl_PO.setRowValue({1: ["区域", "代表"]}, varSheet)

                # 遍历参数
                varSign1 = 0
                # 获取default（接口）
                l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
                for j in range(1, len(l_getRowValue_i)):
                    # summary
                    if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                        # paths
                        r = requests.post(iUrl + l_getRowValue_i[j][2],
                                          headers={"content-type": "application/json", "token": self.token,
                                                   "traceId": "123"},
                                          json=d_tbl_param, verify=False)
                        str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                        res_visitAnalysis = json.loads(str1)
                        l_getRowValue = (Openpyxl_PO.getRowValue(tbl_report))
                        varSign1 = 1
                        break

                if varSign1 == 0:
                    print("[warning], " + tbl_report + " 没有对应的接口文档，程序已退出！")
                    sys.exit(0)

                for j in range(1, len(l_getRowValue)):
                    if l_getRowValue[j][0] != "N":
                        self._visitAnalysis(res_visitAnalysis, tbl_report, l_getRowValue[j][1], l_getRowValue[j][2], l_getRowValue[j][3],
                                       d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO)

                # 忽略“拜访定位匹配人次”及之后的字段
                l_title = Openpyxl_PO.getOneRowValue(0, varSheet)
                # print(l_title)
                for i in range(len(l_title)):
                    if l_title[i] == '拜访定位匹配人次':
                        # print(i)
                        Openpyxl_PO.delSeriesCol(i + 1, 10, varSheet)  # 删除第“拜访定位匹配人次”列及之后的所有列
                        break
                Openpyxl_PO.save()
        return varTitle, tbl_startTime, tbl_endTime
    def getBrowserData_visitAnalysis(self, startTime, endTime, varSheet, Openpyxl_PO):

        # 获取浏览器页面数据

        # 1，打开oa
        self.loginOA()
        self.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
        self.Web_PO.maxBrowser(1)

        # 2，获取协访分析表字段与值
        self.clickMemuERP("统计报表", "拜访分析报表")

        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[3]/div/div/div/input[1]', startTime)
        self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[3]/div/div/div/input[1]', startTime)
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[3]/div/div/div/input[2]', endTime)
        self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[3]/div/div/div/input[2]', endTime)
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[4]/div/button', 2)

        self.Web_PO.zoom("20")  # 缩小页面20%便于抓取元素
        l_fieldValueArea = self.Web_PO.getXpathsText("//tr")  # 获取数据
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "明细")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "总计")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "操作")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "")
        l_fieldValue = self.List_PO.sliceList(l_fieldValueArea, '区域\n代表', 0)
        l_area = self.List_PO.sliceList(l_fieldValueArea, '区域\n代表', 1)
        l_area.insert(0, '区域\n代表')
        l_area.append('总计\nNone')

        # 3, 新建sheet
        Openpyxl_PO.delSheet(varSheet)
        Openpyxl_PO.addSheetCover(varSheet, 99)

        # 4, 将字段与值写入表格
        for i in range(len(l_fieldValue)):
            list3 = str(l_fieldValue[i]).split("\n")
            Openpyxl_PO.setRowValue({i + 1: list3}, varSheet)

        # 5, 将区域和代表插入表格
        Openpyxl_PO.insertCols(1, 2, varSheet)
        for i in range(len(l_area)):
            list4 = str(l_area[i]).split("\n")
            Openpyxl_PO.setRowValue({i + 1: list4}, varSheet)

        l_title = Openpyxl_PO.getOneRowValue(0, varSheet)
        # print(l_title)
        for i in range(len(l_title)):
            if l_title[i] == '拜访定位匹配人次':
                # print(i)
                Openpyxl_PO.delSeriesCol(i + 1, 10, varSheet)  # 删除第“拜访定位匹配人次”列及之后的所有列
                break

        self.Web_PO.close()



    def _meetingAnalysis(self, res_visitAnalysis, tbl_report, d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO):

        d = {}
        sign = 0
        sign2 = 0
        l_result = []

        l_rowcol = Openpyxl_PO.getRowCol(varSheet)
        # print(l_rowcol)
        currCol = l_rowcol[1] + 1
        # print(currCol)
        currRow = 2

        # print(str(res_visitAnalysis['data']['total'])

        # 遍历所有人的字段值
        s = 0
        sql_value = 0
        for i in range(len(res_visitAnalysis['data']['detail'])):
            if tbl_report == "会议分析-代表":

                # 区域经理
                Openpyxl_PO.setCellValue(currRow, 1, str(res_visitAnalysis['data']['detail'][i]['managerName']), varSheet)
                # 代表名字
                Openpyxl_PO.setCellValue(currRow, 2, str(res_visitAnalysis['data']['detail'][i]['delegateName']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 3, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['planMeetingNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 4, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['actualMeetingNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 5, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['planJoinMeetingPeopleNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 6, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['actualJoinMeetingPeopleNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 7, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['planDoubleAJoinMeetingPeopleNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 8, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['actualDoubleAJoinMeetingPeopleNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 9, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['planPotentialityJoinMeetingPeopleNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 10, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['actualPotentialityJoinMeetingPeopleNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 11, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['planMeetingCostBudget']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 12, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['actualMeetingCostBudget']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 13, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['planLaborCostBudget']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 14, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['actualLaborCostBudget']), varSheet)
                currRow = currRow + 1
        
        Openpyxl_PO.setCellValue(currRow, 1, str(res_visitAnalysis['data']['total']['managerName']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 2, str(res_visitAnalysis['data']['total']['delegateName']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 3, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['planMeetingNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 4, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['actualMeetingNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 5, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['planJoinMeetingPeopleNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 6, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['actualJoinMeetingPeopleNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 7, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['planDoubleAJoinMeetingPeopleNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 8, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['actualDoubleAJoinMeetingPeopleNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 9, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['planPotentialityJoinMeetingPeopleNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 10, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['actualPotentialityJoinMeetingPeopleNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 11, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['planMeetingCostBudget']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 12, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['actualMeetingCostBudget']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 13, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['planLaborCostBudget']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 14, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['actualLaborCostBudget']), varSheet)
        Openpyxl_PO.save()

        # else:
        #     # 各比率的计算
        #
        #     for i in range(len(str(res_visitAnalysis['data']['detail'])):
        #         # print(str(res_visitAnalysis['data']['detail'][i])
        #         if str(res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] == 0 or str(res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] == 0:
        #             Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
        #         else:
        #             tmp1 = Data_PO.newRound(str(res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] /
        #                                     str(res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] * 100)
        #             if tmp1 == int(str(res_visitAnalysis['data']['detail'][i][iResField]):
        #                 Openpyxl_PO.setCellValue(currRow, currCol,
        #                                          str(int(str(res_visitAnalysis['data']['detail'][i][iResField])) + "%",
        #                                          varSheet)
        #                 # Openpyxl_PO.setCellValue(currRow, 1, "ok", varSheet)
        #             else:
        #                 Openpyxl_PO.setCellValue(currRow, currCol, str(tmp1) + "%(计算)/" + str(
        #                     int(str(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
        #                 Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
        #         currRow = currRow + 1
        #     Openpyxl_PO.save()
        #
        # # 合计
        # Openpyxl_PO.setCellValue(currRow, 1, "总计", varSheet)
        # Openpyxl_PO.setCellValue(currRow, 2, "None", varSheet)
        #
        # if iResField in d:
        #     if d[iResField] == str(res_visitAnalysis['data']['total'][iResField]:
        #         Openpyxl_PO.setCellValue(currRow, currCol, str(str(res_visitAnalysis['data']['total'][iResField]), varSheet)
        #         # print(str(res_visitAnalysis['data']['total'][iResField])
        #     else:
        #         Openpyxl_PO.setCellValue(currRow, currCol, str(d[iResField]) + "%(计算1)/" + str(
        #             str(res_visitAnalysis['data']['total'][iResField]), varSheet)
        #         Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
        # else:
        #     if sql != None:
        #         if str(res_visitAnalysis['data']['total'][sql.split("/")[1]] == 0 or str(res_visitAnalysis['data']['total'][
        #             sql.split("/")[0]] == 0:
        #             Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
        #         else:
        #             tmp = Data_PO.newRound(
        #                 str(res_visitAnalysis['data']['total'][sql.split("/")[0]] / str(res_visitAnalysis['data']['total'][
        #                     sql.split("/")[1]] * 100)
        #             # print(tmp)
        #             if tmp == int(str(res_visitAnalysis['data']['total'][iResField]):
        #                 Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%", varSheet)
        #             else:
        #                 Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%(计算)/" + str(
        #                     int(str(res_visitAnalysis['data']['total'][iResField])) + "%", varSheet)
        #                 Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
        #
        # Openpyxl_PO.save()
    def meetingAnalysis_I(self, db_ip, iUrl, Openpyxl_PO, Mysql_PO):

        l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
        for i in range(1, len(l_getRowValue_case)):
            # summary
            if l_getRowValue_case[i][1] == "会议分析-代表":
                tbl_report = l_getRowValue_case[i][1]  # 报表
                d_tbl_param = Str_PO.str2dict(l_getRowValue_case[i][2])  # 参数转字典
                tbl_endTime = d_tbl_param["endTime"]
                tbl_endTime = tbl_endTime.split(" ")[0]
                tbl_startTime = d_tbl_param["beginTime"]
                varNowTime = str(Time_PO.getDateTime())
                varTitle = "erp_" + tbl_report + "(" + str(tbl_startTime) + "~" + str(tbl_endTime) + ")_" + db_ip + "_" + varNowTime

                # 生成临时sheet
                varSheet = "i"
                Openpyxl_PO.delSheet(varSheet)
                Openpyxl_PO.addSheetCover(varSheet, 99)
                Openpyxl_PO.setRowValue({1: ["区域经理", "代表名称"]}, varSheet)

                # 遍历参数
                varSign1 = 0
                # 获取default（接口）
                l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
                for j in range(1, len(l_getRowValue_i)):
                    # summary
                    if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                        # paths
                        r = requests.post(iUrl + l_getRowValue_i[j][2],
                                          headers={"content-type": "application/json", "token": self.getToken(),
                                                   "traceId": "123"},
                                          json=d_tbl_param, verify=False)
                        str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                        res = json.loads(str1)
                        # print(res)
                        # l_getRowValue = (Openpyxl_PO.getRowValue(tbl_report))
                        varSign1 = 1
                        break

                # print(l_getRowValue)


                if varSign1 == 0:
                    print("[warning], " + tbl_report + " 没有对应的接口文档，程序已退出！")
                    sys.exit(0)

                self._meetingAnalysis(res, tbl_report, d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO)

                # # 读取sheet中sal语句
                # for j in range(1, len(l_getRowValue)):
                #     if l_getRowValue[j][0] != "N":
                #         self._meetingAnalysis(res, tbl_report, l_getRowValue[j][1], l_getRowValue[j][2], l_getRowValue[j][3],
                #                        d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO)

                Openpyxl_PO.save()
        return varTitle, tbl_startTime, tbl_endTime
    def getBrowserData_meetingAnalysis(self, startTime, endTime, varSheet, Openpyxl_PO):

        # 《会议分析表》前端数据

        # 1，打开oa
        self.loginOA()
        self.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
        self.Web_PO.maxBrowser(1)

        # 2，获取协访分析表字段与值
        self.clickMemuERP("统计报表", "会议分析表")

        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[3]/div/input[1]', startTime)
        self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[3]/div/input[1]', startTime)
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[3]/div/input[2]', endTime)
        self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[3]/div/input[2]', endTime)
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/div[4]/button', 2)

        self.Web_PO.zoom("20")  # 缩小页面20%便于抓取元素
        l_fieldValueArea = self.Web_PO.getXpathsText("//tr")  # 获取数据
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "明细")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "总计")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "操作")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "")

        l_fieldValue = self.List_PO.sliceList(l_fieldValueArea, '区域经理\n代表名称', 0)
        l_area = self.List_PO.sliceList(l_fieldValueArea, '区域经理\n代表名称', 1)
        l_area.insert(0, '区域经理\n代表名称')
        l_area.append('总计\nNone')

        # 3, 新建sheet
        Openpyxl_PO.delSheet(varSheet)
        Openpyxl_PO.addSheetCover(varSheet, 99)

        # 4, 将字段与值写入表格
        for i in range(len(l_fieldValue)):
            list3 = str(l_fieldValue[i]).split("\n")
            list3 = [x.replace(",", "") for x in list3]
            Openpyxl_PO.setRowValue({i + 1: list3}, varSheet)

        # 5, 将区域和代表插入表格
        Openpyxl_PO.insertCols(1, 2, varSheet)
        for i in range(len(l_area)):
            list4 = str(l_area[i]).split("\n")
            Openpyxl_PO.setRowValue({i + 1: list4}, varSheet)

        self.Web_PO.close()


    def _inputOutput(self, res_visitAnalysis, tbl_report, Openpyxl_PO, varSheet, Mysql_PO):

        d = {}
        sign = 0
        sign2 = 0
        l_result = []

        l_rowcol = Openpyxl_PO.getRowCol(varSheet)
        # print(l_rowcol)
        currCol = l_rowcol[1] + 1
        # print(currCol)
        currRow = 2

        # print(str(res_visitAnalysis['data']['total'])

        # 遍历所有人的字段值
        s = 0
        sql_value = 0
        for i in range(len(res_visitAnalysis['data']['detail']['records'])):
            print(res_visitAnalysis['data']['detail']['records'][i])
            if tbl_report == "投入产出分析-医院":
                Openpyxl_PO.setCellValue(currRow, 1, str(res_visitAnalysis['data']['detail']['records'][i]['regionManagerName']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 2, str(res_visitAnalysis['data']['detail']['records'][i]['hospitalName']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 3, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['conferenceCost']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 4, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['conferenceLabourCost']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 5, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['lunchCost']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 6, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['deptConferenceCost']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 7, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['areaCost']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 8, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['cityConferenceCost']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 9, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['nationalConferenceCost']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 10, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['conferenceFee1']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 11, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['conferenceFee2']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 12, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['discussionFee']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 13, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['hospitalCasesNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 14, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['consultationCost']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 15, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['currentCaseNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 16, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['hospitalPatientNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 17, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['roi']) + "%", varSheet)
                # Openpyxl_PO.setCellValue(currRow, 16, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['purchaseNum']), varSheet)
                # Openpyxl_PO.setCellValue(currRow, 18, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail']['records'][i]['monthHypertensionNum']), varSheet)
                currRow = currRow + 1

        # 总计
        Openpyxl_PO.setCellValue(currRow, 1, str(res_visitAnalysis['data']['total']['regionManagerName']),varSheet)
        Openpyxl_PO.setCellValue(currRow, 2, str(res_visitAnalysis['data']['total']['hospitalName']),varSheet)
        Openpyxl_PO.setCellValue(currRow, 3, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['conferenceCost']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 4, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['conferenceLabourCost']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 5, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['lunchCost']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 6, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['deptConferenceCost']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 7, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['areaCost']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 8, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['cityConferenceCost']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 9, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['nationalConferenceCost']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 10, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['conferenceFee1']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 11, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['conferenceFee2']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 12, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['discussionFee']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 13, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['hospitalCasesNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 14, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['consultationCost']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 15, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['currentCaseNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 16, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['hospitalPatientNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 17, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['roi'])+ "%", varSheet)
        Openpyxl_PO.save()
    def inputOutput_I(self, db_ip, iUrl, Openpyxl_PO, Mysql_PO):

        l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
        for i in range(1, len(l_getRowValue_case)):
            # summary
            if l_getRowValue_case[i][1] == "投入产出分析-医院":
                tbl_report = l_getRowValue_case[i][1]  # 报表
                tbl_endTime = l_getRowValue_case[i][2].split("endDate=")[1]
                tbl_endTime = tbl_endTime.split("&")[0]
                tbl_startTime = l_getRowValue_case[i][2].split("startDate=")[1]
                varNowTime = str(Time_PO.getDateTime())
                varTitle = "erp_" + tbl_report + "(" + str(tbl_startTime) + "~" + str(
                    tbl_endTime) + ")_" + db_ip + "_" + varNowTime

                # 生成临时sheet
                varSheet = "i"
                Openpyxl_PO.delSheet(varSheet)
                Openpyxl_PO.addSheetCover(varSheet, 99)
                Openpyxl_PO.setRowValue({1: ["区域经理", "医院"]}, varSheet)

                # 遍历参数
                varSign1 = 0
                # 获取default（接口）
                l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
                for j in range(1, len(l_getRowValue_i)):
                    # summary
                    if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                        # paths
                        # print(iUrl + l_getRowValue_i[j][2] + "?" + str(l_getRowValue_case[i][2]))
                        r = requests.get(iUrl + l_getRowValue_i[j][2] + "?" + str(l_getRowValue_case[i][2]),
                                         headers={"content-type": "application/json", "token": self.getToken(),
                                                  "traceId": "123"},
                                         verify=False)


                        str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                        res = json.loads(str1)
                        print(res)
                        varSign1 = 1
                        break

                # print(l_getRowValue)

                if varSign1 == 0:
                    print("[warning], " + tbl_report + " 没有对应的接口文档，程序已退出！")
                    sys.exit(0)

                self._inputOutput(res, tbl_report, Openpyxl_PO, varSheet, Mysql_PO)

                Openpyxl_PO.save()
        return varTitle, tbl_startTime, tbl_endTime
    def getBrowserData_inputOutput(self, startTime, endTime, varSheet, Openpyxl_PO):


        # 1，打开oa
        self.loginOA()
        self.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
        self.Web_PO.maxBrowser(1)

        # 2，获取协访分析表字段与值
        self.clickMemuERP("统计报表", "投入产出分析表")

        self.Web_PO.clickXpath(
            '//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[2]/div/div/div/input[1]', 2)
        self.Web_PO.inputXpathClear(
            '//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[2]/div/div/div/input[1]', startTime)
        self.Web_PO.clickXpath(
            '//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[2]/div/div/div/input[2]', 2)
        self.Web_PO.inputXpathClear(
            '//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[2]/div/div/div/input[2]', endTime)
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/footer/div/span[2]/div/div/input', 2)
        self.Web_PO.clickXpath('/html/body/div[3]/div[1]/div[1]/ul/li[5]', 3)

        self.Web_PO.clickXpath(
            '//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[3]/div/button', 2)

        self.Web_PO.zoom("20")  # 缩小页面20%便于抓取元素
        l_fieldValueArea = self.Web_PO.getXpathsText("//tr")  # 获取数据
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "明细")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "总计")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "操作")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "")

        l_fieldValue = self.List_PO.sliceList(l_fieldValueArea, '区域经理\n医院', 0)
        l_area = self.List_PO.sliceList(l_fieldValueArea, '区域经理\n医院', 1)
        l_area.insert(0, '区域经理\n医院')
        l_area.append('总计\nNone')

        # 3, 新建sheet
        Openpyxl_PO.delSheet(varSheet)
        Openpyxl_PO.addSheetCover(varSheet, 99)

        x = l_fieldValue[1] + "\n"
        x = (l_fieldValue[0].replace("实际费用 ", x))
        l_fieldValue.pop(0)
        l_fieldValue.insert(0, x)
        l_fieldValue.pop(1)
        # print(l_fieldValue)

        # 4, 将字段与值写入表格
        for i in range(len(l_fieldValue)):
            list3 = str(l_fieldValue[i]).split("\n")
            list3 = [x.replace(",", "") for x in list3]
            Openpyxl_PO.setRowValue({i + 1: list3}, varSheet)

        # 5, 将区域和代表插入表格
        Openpyxl_PO.insertCols(1, 2, varSheet)
        for i in range(len(l_area)):
            list4 = str(l_area[i]).split("\n")
            Openpyxl_PO.setRowValue({i + 1: list4}, varSheet)

        self.Web_PO.close()


    def _helpingAnalysis(self, res_visitAnalysis, tbl_report, tblField, iResField, sql, d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO):

        d = {}

        # visitAnalysis( '拜访分析报表', "计划拜访人次", "plannedVisitsNumber", "sql", {"endTime": "2022-06-30  23:59:59", "startTime": "2022-06-01", "uid": 0})
        sign = 0
        sign2 = 0
        l_result = []

        l_rowcol = Openpyxl_PO.getRowCol(varSheet)
        # print(l_rowcol)
        currCol = l_rowcol[1] + 1
        # print(currCol)
        currRow = 2
        Openpyxl_PO.setCellValue(1, currCol, tblField, varSheet)
        # print(tblField)

        if iResField != None and sql == None:
            pass

        elif iResField != None and "%s" in sql:

            # 遍历所有人的字段值
            s = 0
            for i in range(len(res_visitAnalysis['data']['detail'])):
                if tbl_report == "协访分析":
                    sql_value = Mysql_PO.execQuery(sql % (res_visitAnalysis['data']['detail'][i]['uid'], d_tbl_param["startTime"], d_tbl_param["endTime"]))
                    # print(sql_value)

                    if len(sql_value) == 0:
                        sql_value = 0
                    else:
                        if sql_value[0][0] == None:
                            sql_value = 0
                        else:
                            sql_value = sql_value[0][0]
                    # 接口和sql比对
                    s = s + sql_value
                    Openpyxl_PO.setCellValue(currRow, 1, res_visitAnalysis['data']['detail'][i]['userName'], varSheet)  # 第1列区域
                if res_visitAnalysis['data']['detail'][i][iResField] == sql_value:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value), varSheet)  # 指标值
                else:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value) + "(sql)/" + str(res_visitAnalysis['data']['detail'][i][iResField]), varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

                currRow = currRow + 1
                d[iResField] = s
            Openpyxl_PO.save()
        else:
            # 各比率的计算

            for i in range(len(res_visitAnalysis['data']['detail'])):
                if res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] == 0 :
                    Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
                else:
                    tmp1 = Data_PO.newRound(res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] / res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] * 100)
                    if tmp1 == int(res_visitAnalysis['data']['detail'][i][iResField]):
                        Openpyxl_PO.setCellValue(currRow, currCol, str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                        # Openpyxl_PO.setCellValue(currRow, 1, "ok", varSheet)
                    else:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp1) + "%(计算)/" + str(int(res_visitAnalysis['data']['detail'][i][iResField])) + "%", varSheet)
                        Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
                currRow = currRow + 1
            Openpyxl_PO.save()

        # 合计
        Openpyxl_PO.setCellValue(currRow, 1, "总计", varSheet)

        if iResField in d:
            if d[iResField] == res_visitAnalysis['data']['total'][iResField]:
                Openpyxl_PO.setCellValue(currRow, currCol, str(res_visitAnalysis['data']['total'][iResField]), varSheet)
            else:
                Openpyxl_PO.setCellValue(currRow, currCol, str(d[iResField]) + "%(计算1)/" + str(res_visitAnalysis['data']['total'][iResField]), varSheet)
                Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
        else:
            if sql != None:
                if res_visitAnalysis['data']['total'][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['total'][sql.split("/")[0]] == 0:
                    Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
                else:
                    tmp = Data_PO.newRound(res_visitAnalysis['data']['total'][sql.split("/")[0]] / res_visitAnalysis['data']['total'][sql.split("/")[1]] * 100)
                    # print(tmp)
                    if tmp == int(res_visitAnalysis['data']['total'][iResField]):
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%", varSheet)
                    else:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%(计算)/" + str(int(res_visitAnalysis['data']['total'][iResField])) + "%", varSheet)
                        Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

        Openpyxl_PO.save()
    def helpingAnalysis_I(self, db_ip, iUrl, Openpyxl_PO, Mysql_PO):

        # 1，获取协访分析表接口数据

        l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
        for i in range(1, len(l_getRowValue_case)):
            if l_getRowValue_case[i][1] == "协访分析":
                tbl_report = l_getRowValue_case[i][1]  # 报表
                d_tbl_param = Str_PO.str2dict(l_getRowValue_case[i][2])  # 参数2字典
                tbl_endTime = d_tbl_param["endTime"]
                tbl_endTime = tbl_endTime.split(" ")[0]
                tbl_startTime = d_tbl_param["startTime"]
                # print(tbl_startTime,tbl_endTime)
                # sys.exit(0)
                varNowTime = str(Time_PO.getDateTime())
                varTitle = "erp_" + tbl_report + "(" + str(tbl_startTime) + "~" + str(tbl_endTime) + ")_" + db_ip + "_" + varNowTime

                # 生成临时sheet
                varSheet = "i"
                Openpyxl_PO.delSheet(varSheet)
                Openpyxl_PO.addSheetCover(varSheet, 99)
                Openpyxl_PO.setRowValue({1: ["区域经理"]}, varSheet)

                # 遍历参数
                varSign1 = 0
                # 获取default（接口）
                l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
                for j in range(1, len(l_getRowValue_i)):
                    # summary
                    if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                        # paths
                        r = requests.post(iUrl + l_getRowValue_i[j][2],
                                          headers={"content-type": "application/json", "token": self.getToken(),
                                                   "traceId": "123"},
                                          json=d_tbl_param, verify=False)
                        str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                        res_visitAnalysis = json.loads(str1)
                        l_getRowValue = (Openpyxl_PO.getRowValue(tbl_report))
                        varSign1 = 1
                        break

                if varSign1 == 0:
                    print("[warning], " + tbl_report + " 没有对应的接口文档，程序已退出！")
                    sys.exit(0)

                for j in range(1, len(l_getRowValue)):
                    if l_getRowValue[j][0] != "N":
                        self._helpingAnalysis(res_visitAnalysis, tbl_report, l_getRowValue[j][1], l_getRowValue[j][2],
                                              l_getRowValue[j][3], d_tbl_param, Openpyxl_PO, varSheet, Mysql_PO)

        return varTitle, tbl_startTime, tbl_endTime
    def getBrowserData_helpingAnalysis(self, startTime, endTime, varSheet, Openpyxl_PO):

        # 获取浏览器页面数据

        # 1，打开oa
        self.loginOA()
        self.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
        self.Web_PO.maxBrowser(1)

        # 2，获取协访分析表字段与值
        self.clickMemuERP("统计报表", "协访分析表")

        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[1]/div/div/div/input[1]', startTime)
        self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[1]/div/div/div/input[1]', startTime)
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[1]/div/div/div/input[2]', endTime)
        self.Web_PO.inputXpathClear('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[1]/div/div/div/input[2]', endTime)
        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[2]/div/button', 2)

        self.Web_PO.zoom("20")  # 缩小页面20%便于抓取元素
        l_fieldValueArea = self.Web_PO.getXpathsText("//tr")  # 获取数据
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "明细")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "总计")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "操作")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "")
        l_fieldValue = self.List_PO.sliceList(l_fieldValueArea, '区域经理', 0)
        l_area = self.List_PO.sliceList(l_fieldValueArea, '区域经理', 1)
        l_area.insert(0, '区域经理')
        l_area.append('总计')

        # 3, 新建sheet
        Openpyxl_PO.delSheet(varSheet)
        Openpyxl_PO.addSheetCover(varSheet, 99)

        # 4, 将字段与值写入表格
        for i in range(len(l_fieldValue)):
            list3 = str(l_fieldValue[i]).split("\n")
            Openpyxl_PO.setRowValue({i + 1: list3}, varSheet)

        # 5, 将区域经理插入表格
        Openpyxl_PO.insertCols(1, 1, varSheet)
        Openpyxl_PO.setColValue({"A": l_area}, varSheet)

        self.Web_PO.close()


    def _customerInput(self, res_visitAnalysis, tbl_report, Openpyxl_PO, varSheet, Mysql_PO):

        d = {}
        sign = 0
        sign2 = 0
        l_result = []

        l_rowcol = Openpyxl_PO.getRowCol(varSheet)
        # print(l_rowcol)
        currCol = l_rowcol[1] + 1
        # print(currCol)
        currRow = 2

        # print(str(res_visitAnalysis['data']['total'])

        # 遍历所有人的字段值
        s = 0
        sql_value = 0
        for i in range(len(res_visitAnalysis['data']['detail'])):
            print(res_visitAnalysis['data']['detail'][i])
            if tbl_report == "重点客户投入有效性分析":
                Openpyxl_PO.setCellValue(currRow, 1, str(res_visitAnalysis['data']['detail'][i]['managerName']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 2, str(res_visitAnalysis['data']['detail'][i]['delegateName']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 3, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['totalNumber']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 4, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['potentialityPeopleNumber']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 5, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['potentialityPeopleRate']) + "%", varSheet)
                Openpyxl_PO.setCellValue(currRow, 6, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['doubleAPeopleNumber']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 7, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['doubleAPeopleRate']) + "%", varSheet)

                Openpyxl_PO.setCellValue(currRow, 8, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['totalCurrentCaseNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 9, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['potentialityCurrentCaseNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 10, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['potentialityCurrentCaseRate']) + "%", varSheet)
                Openpyxl_PO.setCellValue(currRow, 11, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['doubleAcurrentCaseNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 12, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['doubleAcurrentCaseRate']) + "%", varSheet)
                Openpyxl_PO.setCellValue(currRow, 13, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['consultationCost']), varSheet)

                Openpyxl_PO.setCellValue(currRow, 14, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['totalTargetCaseNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 15, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['addCurrentCasNum']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 16, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['potentialityAddCurrentCaseNum']) , varSheet)
                Openpyxl_PO.setCellValue(currRow, 17, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['doubleAAddCurrentCaseNum']) , varSheet)
                Openpyxl_PO.setCellValue(currRow, 18, self.Char_PO.zeroByDel(
                    res_visitAnalysis['data']['detail'][i]['conferenceFeeToOneAddTwo']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 19, self.Char_PO.zeroByDel(
                    res_visitAnalysis['data']['detail'][i]['conferenceFeeToMarket']), varSheet)

                Openpyxl_PO.setCellValue(currRow, 20, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['nextTotalCurrentCaseNum']) , varSheet)
                Openpyxl_PO.setCellValue(currRow, 21, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['addTargetCaseNum']) , varSheet)
                Openpyxl_PO.setCellValue(currRow, 22, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['addPotentialityTargetCaseNum']) , varSheet)
                Openpyxl_PO.setCellValue(currRow, 23, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['addDoubleATargetCaseNum']) , varSheet)
                Openpyxl_PO.setCellValue(currRow, 24, self.Char_PO.zeroByDel(
                    res_visitAnalysis['data']['detail'][i]['actualConferenceFeeToOneAddTwo']), varSheet)
                Openpyxl_PO.setCellValue(currRow, 25, self.Char_PO.zeroByDel(
                    res_visitAnalysis['data']['detail'][i]['actuaConferenceFeeToMarket']), varSheet)

                Openpyxl_PO.setCellValue(currRow, 26, self.Char_PO.zeroByDel(res_visitAnalysis['data']['detail'][i]['actualInOutRate']) + "%", varSheet)

                currRow = currRow + 1

        # 总计

        Openpyxl_PO.setCellValue(currRow, 1, str(res_visitAnalysis['data']['total']['managerName']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 2, str(res_visitAnalysis['data']['total']['delegateName']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 3, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['totalNumber']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 4, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['potentialityPeopleNumber']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 5, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['potentialityPeopleRate']) + "%", varSheet)
        Openpyxl_PO.setCellValue(currRow, 6, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['doubleAPeopleNumber']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 7, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['doubleAPeopleRate']) + "%", varSheet)

        Openpyxl_PO.setCellValue(currRow, 8, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['totalCurrentCaseNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 9, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['potentialityCurrentCaseNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 10, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['potentialityCurrentCaseRate']) + "%", varSheet)
        Openpyxl_PO.setCellValue(currRow, 11, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['doubleAcurrentCaseNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 12, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['doubleAcurrentCaseRate']) + "%", varSheet)
        Openpyxl_PO.setCellValue(currRow, 13, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['consultationCost']), varSheet)

        Openpyxl_PO.setCellValue(currRow, 14, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['totalTargetCaseNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 15, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['addCurrentCasNum']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 16, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['potentialityAddCurrentCaseNum']) , varSheet)
        Openpyxl_PO.setCellValue(currRow, 17, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['doubleAAddCurrentCaseNum']) , varSheet)

        Openpyxl_PO.setCellValue(currRow, 18, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['conferenceFeeToOneAddTwo']) , varSheet)
        Openpyxl_PO.setCellValue(currRow, 19, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['conferenceFeeToMarket']) , varSheet)
        Openpyxl_PO.setCellValue(currRow, 20, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['nextTotalCurrentCaseNum']) , varSheet)
        Openpyxl_PO.setCellValue(currRow, 21, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['addTargetCaseNum']) , varSheet)
        Openpyxl_PO.setCellValue(currRow, 22, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['addPotentialityTargetCaseNum']) , varSheet)
        Openpyxl_PO.setCellValue(currRow, 23, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['addDoubleATargetCaseNum']) , varSheet)

        Openpyxl_PO.setCellValue(currRow, 24, self.Char_PO.zeroByDel(
            res_visitAnalysis['data']['total']['actualConferenceFeeToOneAddTwo']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 25, self.Char_PO.zeroByDel(
            res_visitAnalysis['data']['total']['actuaConferenceFeeToMarket']), varSheet)
        Openpyxl_PO.setCellValue(currRow, 26, self.Char_PO.zeroByDel(res_visitAnalysis['data']['total']['actualInOutRate']) + "%", varSheet)

        Openpyxl_PO.save()
    def customerInput_I(self, db_ip, iUrl, Openpyxl_PO, Mysql_PO):

        l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
        for i in range(1, len(l_getRowValue_case)):
            # summary
            if l_getRowValue_case[i][1] == "重点客户投入有效性分析":
                tbl_report = l_getRowValue_case[i][1]  # 报表
                tbl_month = l_getRowValue_case[i][2]
                varNowTime = str(Time_PO.getDateTime())
                varTitle = "erp_" + tbl_report + "(" + str(tbl_month) + ")_" + db_ip + "_" + varNowTime

                # 生成临时sheet
                varSheet = "i"
                Openpyxl_PO.delSheet(varSheet)
                Openpyxl_PO.addSheetCover(varSheet, 99)
                Openpyxl_PO.setRowValue({1: ["区域经理", "代表"]}, varSheet)

                # 遍历参数
                varSign1 = 0
                # 获取default（接口）
                l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
                for j in range(1, len(l_getRowValue_i)):
                    # summary
                    if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                        # paths
                        # print(iUrl + l_getRowValue_i[j][2] + "?" + str(l_getRowValue_case[i][2]))
                        r = requests.get(iUrl + l_getRowValue_i[j][2] + "?" + str(l_getRowValue_case[i][2]),
                                         headers={"content-type": "application/json", "token": self.getToken(),
                                                  "traceId": "123"},
                                         verify=False)

                        str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                        res = json.loads(str1)
                        print(res)
                        varSign1 = 1
                        break

                # print(l_getRowValue)

                if varSign1 == 0:
                    print("[warning], " + tbl_report + " 没有对应的接口文档，程序已退出！")
                    sys.exit(0)

                self._customerInput(res, tbl_report, Openpyxl_PO, varSheet, Mysql_PO)
                Openpyxl_PO.save()
        return varTitle, tbl_month
    def getBrowserData_customerInput(self, varMonth, varSheet, Openpyxl_PO):

        month = str(varMonth).split("=")[1]
        # print(month)

        # 1，打开oa
        self.loginOA()
        self.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
        self.Web_PO.maxBrowser(1)

        # 2，获取协访分析表字段与值
        self.clickMemuERP("统计报表", "重点客户投入有效性分析")

        self.Web_PO.clickXpath(
            '//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[3]/div/div/div/input', 2)
        self.Web_PO.inputXpathClear(
            '//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[3]/div/div/div/input',
            month)

        self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[4]/div/button', 2)

        self.Web_PO.zoom("20")  # 缩小页面20%便于抓取元素
        l_fieldValueArea = self.Web_PO.getXpathsText("//tr")  # 获取数据
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "明细")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "总计")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "操作")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "")

        # print(l_fieldValueArea)
        l_fieldValueArea.pop(0)
        l_fieldValueArea.pop(0)


        # 3, 新建sheet
        Openpyxl_PO.delSheet(varSheet)
        Openpyxl_PO.addSheetCover(varSheet, 99)
        Openpyxl_PO.setRowValue({1: ["区域经理", "代表"]}, varSheet)

        # 4, 将字段与值写入表格
        for i in range(len(l_fieldValueArea)):
            list3 = str(l_fieldValueArea[i]).split("\n")
            list3 = [x.replace(",", "") for x in list3]
            if "总计" in list3:
                list3.insert(1, "")
                Openpyxl_PO.setRowValue({i + 2: list3}, varSheet)
            else:
                Openpyxl_PO.setRowValue({i + 2: list3}, varSheet)


        self.Web_PO.close()


    def _devPlanOverall(self, res_visitAnalysis, tbl_report, tblField, iResField, sql, product_id, Openpyxl_PO, varSheet, Mysql_PO):

        d = {}

        # visitAnalysis( '拜访分析报表', "计划拜访人次", "plannedVisitsNumber", "sql", {"endTime": "2022-06-30  23:59:59", "startTime": "2022-06-01", "uid": 0})
        sign = 0
        sign2 = 0
        l_result = []

        l_rowcol = Openpyxl_PO.getRowCol(varSheet)
        # print(l_rowcol)
        currCol = l_rowcol[1] + 1
        # print(currCol)
        currRow = 2
        Openpyxl_PO.setCellValue(1, currCol, tblField, varSheet)
        # print(tblField)

        if iResField != None and sql == None:
            pass

        elif iResField != None and "%s" in sql:

            # 遍历所有人的字段值
            s = 0

            for i in range(len(res_visitAnalysis['data']['detail'])):

                if tbl_report == "开发计划总揽":
                    if product_id == "None":
                        sql = sql.replace("and product_id=%s","")
                        sql1 = sql % (res_visitAnalysis['data']['detail'][i]['areaManagerId'])
                    else:
                        sql1 = sql % (res_visitAnalysis['data']['detail'][i]['areaManagerId'], str(product_id))
                    sql_value = Mysql_PO.execQuery(sql1)
                    # print(sql_value)


                    if len(sql_value) == 0:
                        sql_value = 0
                    else:
                        if sql_value[0][0] == None:
                            sql_value = 0
                        else:
                            sql_value = sql_value[0][0]

                    # 接口和sql比对
                    s = s + sql_value
                    Openpyxl_PO.setCellValue(currRow, 1, res_visitAnalysis['data']['detail'][i]['areaManagerName'], varSheet)  # 第1列区域

                if res_visitAnalysis['data']['detail'][i][iResField] == sql_value:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value), varSheet)  # 指标值
                else:
                    Openpyxl_PO.setCellValue(currRow, currCol, str(sql_value) + "(sql)/" + str(
                        res_visitAnalysis['data']['detail'][i][iResField]), varSheet)
                    Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

                currRow = currRow + 1
                d[iResField] = s

            Openpyxl_PO.save()


        else:
            # 各比率的计算

            for i in range(len(res_visitAnalysis['data']['detail'])):
                if res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] == 0 or \
                        res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] == 0:
                    Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
                else:
                    tmp1 = Data_PO.newRound(res_visitAnalysis['data']['detail'][i][sql.split("/")[0]] /
                                            res_visitAnalysis['data']['detail'][i][sql.split("/")[1]] * 100, 2)
                    if tmp1 == res_visitAnalysis['data']['detail'][i][iResField]:
                        Openpyxl_PO.setCellValue(currRow, currCol,
                                                 str(res_visitAnalysis['data']['detail'][i][iResField]) + "%",
                                                 varSheet)
                    else:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp1) + "%(计算)/" + str(
                            res_visitAnalysis['data']['detail'][i][iResField]) + "%", varSheet)
                        Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
                currRow = currRow + 1
            Openpyxl_PO.save()

        # 总计
        Openpyxl_PO.setCellValue(currRow, 1, "总计", varSheet)

        if iResField in d:
            if d[iResField] == res_visitAnalysis['data']['total'][iResField]:
                Openpyxl_PO.setCellValue(currRow, currCol, str(res_visitAnalysis['data']['total'][iResField]), varSheet)
            else:
                Openpyxl_PO.setCellValue(currRow, currCol, str(d[iResField]) + "%(计算1)/" + str(
                    res_visitAnalysis['data']['total'][iResField]), varSheet)
                Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色
        else:
            if sql != None:
                if res_visitAnalysis['data']['total'][sql.split("/")[1]] == 0 or res_visitAnalysis['data']['total'][
                    sql.split("/")[0]] == 0:
                    Openpyxl_PO.setCellValue(currRow, currCol, "0%", varSheet)
                else:
                    tmp = Data_PO.newRound(
                        res_visitAnalysis['data']['total'][sql.split("/")[0]] / res_visitAnalysis['data']['total'][
                            sql.split("/")[1]] * 100, 2)
                    # print(tmp)
                    if tmp == res_visitAnalysis['data']['total'][iResField]:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%", varSheet)
                    else:
                        Openpyxl_PO.setCellValue(currRow, currCol, str(tmp) + "%(计算2)/" + str(
                            res_visitAnalysis['data']['total'][iResField]) + "%", varSheet)
                        Openpyxl_PO.setCellColor(currRow, currCol, "ff0000", varSheet)  # 错误标红色

        Openpyxl_PO.save()
    def devPlanOverall_I(self, db_ip, iUrl, Openpyxl_PO, Mysql_PO):

        # 1，获取协访分析表接口数据

        l_getRowValue_case = (Openpyxl_PO.getRowValue("case"))
        for i in range(1, len(l_getRowValue_case)):
            if l_getRowValue_case[i][1] == "开发计划总揽" and l_getRowValue_case[i][0] != "N":
                tbl_report = l_getRowValue_case[i][1]  # 报表
                product_id = str(l_getRowValue_case[i][2])
                varNowTime = str(Time_PO.getDateTime())
                d_title = Str_PO.str2dict(l_getRowValue_case[i][3])  # 参数2字典
                # print(d_title)
                # print(product_id)
                if product_id == "None":
                    varTitle = "erp_" + tbl_report + "(所有产品)_" + db_ip + "_" + varNowTime
                else:
                    varTitle = "erp_" + tbl_report + "(" + str(d_title[product_id]) + ")_" + db_ip + "_" + varNowTime

                # 生成临时sheet
                varSheet = "i"
                Openpyxl_PO.delSheet(varSheet)
                Openpyxl_PO.addSheetCover(varSheet, 99)
                Openpyxl_PO.setRowValue({1: ["区域"]}, varSheet)

                # 遍历参数
                varSign1 = 0
                # 获取default（接口）
                l_getRowValue_i = (Openpyxl_PO.getRowValue("default"))
                for j in range(1, len(l_getRowValue_i)):
                    # summary
                    if l_getRowValue_case[i][1] == l_getRowValue_i[j][1]:
                        # paths
                        # print(iUrl + l_getRowValue_i[j][2] + "?productId=" + str(product_id))
                        if product_id == 'None':
                            r = requests.get(
                                iUrl + l_getRowValue_i[j][2] ,
                                headers={"content-type": "application/json", "token": self.getToken(),
                                         "traceId": "123"},
                                verify=False)
                        else:
                            r = requests.get(iUrl + l_getRowValue_i[j][2] + "?productId=" + str(l_getRowValue_case[i][2]),
                                             headers={"content-type": "application/json", "token": self.getToken(), "traceId": "123"},
                                             verify=False)
                        str1 = r.text.encode('gbk', 'ignore').decode('gbk')
                        res_visitAnalysis = json.loads(str1)
                        l_getRowValue = (Openpyxl_PO.getRowValue(tbl_report))
                        varSign1 = 1
                        break

                if varSign1 == 0:
                    print("[warning], " + tbl_report + " 没有对应的接口文档，程序已退出！")
                    sys.exit(0)


                for j in range(1, len(l_getRowValue)):
                    if l_getRowValue[j][0] != "N":
                        self._devPlanOverall(res_visitAnalysis, tbl_report, l_getRowValue[j][1], l_getRowValue[j][2], l_getRowValue[j][3], product_id, Openpyxl_PO, varSheet, Mysql_PO)

        return varTitle, product_id
    def getBrowserData_devPlanOverall(self, product_id, varSheet, Openpyxl_PO):

        # 获取浏览器页面数据

        # 1，打开oa
        self.loginOA()
        self.clickMemuOA("盛蕴ERP", "盛蕴ERP（演示）")
        self.Web_PO.maxBrowser(1)

        # 2，获取协访分析表字段与值
        self.clickMemuERP("统计报表", "开发计划总揽")
        if product_id == "None":
            ...
        else:
            self.Web_PO.jsXpathReadonly('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[1]/div/div/div/div[1]/input', 2)
            self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[1]/div/div/div/div/input', 2)
            self.Web_PO.clickXpath('/html/body/div[2]/div[1]/div[1]/ul/li[' + str(product_id) + ']', 2)
            # self.Web_PO.clickXpath('/html/body/div[2]/div[1]/div[1]/ul/li[1]', 2)
            self.Web_PO.clickXpath('//*[@id="app"]/section/section/section/main/div[2]/section/header/div/form/div[2]/div/button', 2)
        self.Web_PO.zoom("20")  # 缩小页面20%便于抓取元素
        l_fieldValueArea = self.Web_PO.getXpathsText("//tr")  # 获取数据
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "明细")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "总计")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "操作")
        l_fieldValueArea = self.List_PO.listBatchDel(l_fieldValueArea, "")
        l_fieldValueArea1 = l_fieldValueArea[0].split("\n")
        l_area = self.List_PO.sliceList(l_fieldValueArea1, '区域', 1)
        l_area.insert(0, '区域')
        l_area.append('总计')

        # 3, 新建sheet
        Openpyxl_PO.delSheet(varSheet)
        Openpyxl_PO.addSheetCover(varSheet, 99)

        # 4, 将字段与值写入表格
        for i in range(len(l_fieldValueArea)):
            list3 = str(l_fieldValueArea[i]).split("\n")
            Openpyxl_PO.setRowValue({i + 1: list3}, varSheet)

        # # 5, 将区域列插入表格
        # Openpyxl_PO.insertCols(1, 1, varSheet)
        # Openpyxl_PO.setColValue({"A": l_area}, varSheet)

        self.Web_PO.close()



    def getResult(self, varSheet, Openpyxl_PO):

        # 对新表生成结果状态

        r = Openpyxl_PO.getRowCol(varSheet)[0]
        c = Openpyxl_PO.getRowCol(varSheet)[1]

        varSign = 0
        list11 = []
        for i in range(r):
            for j in range(c):
                if Openpyxl_PO.getCellValue(i + 1, j + 1, varSheet) is None :
                    pass

                elif "/" in Openpyxl_PO.getCellValue(i + 1, j + 1, varSheet):
                    varSign = 1
            if varSign == 1:
                list11.append("error")
            else:
                list11.append("ok")
            varSign = 0

        Openpyxl_PO.insertCols(1, 1, varSheet)
        Openpyxl_PO.setColValue({"A": list11}, varSheet)
        Openpyxl_PO.setCellValue(1, 1, "结果", varSheet)
        list4 = Openpyxl_PO.getOneColValue(0, varSheet)
        # print(list4)
        for i in range(len(list4)):
            if list4[i] == "ok":
                Openpyxl_PO.setCellColor(i+1, 1, "00E400", varSheet)

    def db2html(self, Mysql_PO, varTitle):

        # 生成report.html
        # varNowTime = str(Time_PO.getDateTime())
        # varTitle = "erp_" + tbl_report + "(" + str(l_getRowValue_case[i][4]) + ")_" + db_ip + "_" + varNowTime
        df = pd.read_sql(sql="select * from `12345`", con=Mysql_PO.getPymysqlEngine())
        pd.set_option('colheader_justify', 'center')  # 对其方式居中
        html = '''<html><head><title>''' + varTitle + '''</title></head>
        <body><b><caption>''' + varTitle + '''</caption></b><br><br>{table}</body></html>'''
        style = '''<style>.mystyle {font-size: 11pt; font-family: Arial;    border-collapse: collapse;     border: 1px solid silver;}.mystyle td, th {    padding: 5px;}.mystyle tr:nth-child(even) {    background: #E0E0E0;}.mystyle tr:hover {    background: silver;    cursor: pointer;}</style>'''
        rptNameDate = "report/" + varTitle + ".html"
        with open(rptNameDate, 'w') as f:
            f.write(style + html.format(table=df.to_html(classes="mystyle", col_space=100, index=False)))
        from bs4 import BeautifulSoup
        # 优化report.html, 去掉None、修改颜色
        html_text = BeautifulSoup(open(rptNameDate), features='html.parser')
        html_text = str(html_text).replace("<td>None</td>", "<td></td>").replace("<td>error</td>",'<td bgcolor="#ed1941">error</td>'). \
            replace("<td>ok</td>", '<td bgcolor="#00ae9d">ok</td>')
        # 另存为report.html
        tf = open(rptNameDate, 'w', encoding='utf-8')
        tf.write(str(html_text))
        tf.close()
        Sys_PO.openFile(rptNameDate)

