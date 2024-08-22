# -*- coding: utf-8 -*-

import os,xlrd,xlwt,json,jsonpath
from datetime import datetime
from xlrd import open_workbook
from xlutils.copy import copy
import readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
import reflection
from iDriven import HTTP
http = HTTP()

class XLS:

    def __init__(self):
        self.varExcel = os.path.dirname(os.path.abspath("__file__")) + u'\config\\' + localReadConfig.get_system("excelName")
        self.rbk = xlrd.open_workbook(self.varExcel, formatting_info=True)
        self.wbk = copy(self.rbk)
        self.wSheet = self.wbk.get_sheet(1)
        self.styleBlue = xlwt.easyxf(u'font: height 260 ,name Times New Roman, color-index blue')
        self.styleRed = xlwt.easyxf(u'font: height 260 ,name Times New Roman, color-index red')
        sheetNums = 0
        l_sheetNames = 0
        l_sheetSerial = []  # 工作表序列
        l_sheetName = []  # 工作表名字
        d_sheetNames = {}
        sheetNums = len(self.rbk.sheet_names())  # 工作表数量：如 2
        l_sheetNames = self.rbk.sheet_names()  # 所有工作表名列表：如 ['inter', 'case']
        for i in range(sheetNums):
            l_sheetSerial.append(i)
            l_sheetName.append(l_sheetNames[i])
        d_sheetNames = dict(zip(l_sheetSerial, l_sheetName))  # 工作表名字典：{0: 'inter', 1: 'case'}
        self.sheet1 = self.rbk.sheet_by_name(d_sheetNames[0])  # 第1个工作表：inter
        self.sheet2 = self.rbk.sheet_by_name(d_sheetNames[1])  # 第2个工作表：case

        self.d_inter = {}

    def getInterIsRun(self):
        """
        判断inter工作表中接口是否执行。isRun一列，y=执行，n=不执行，返回列表如下。
        返回：'[[], [], 3]'  第一个[]表示没有Y，第二个[]标识没有N，3表示3个接口
        返回：[[], [2, 3, 5], 0] 第一个[]表示没有Y，第二个[2,3,5]表示第2第3第5个接口是N
        返回：[[2], [3, 5], 0] 第一个[2]表示有第二个接口是Y，第二个[3,5]表示第3第5个接口是N
        """
        serialNums = 0
        serialNumNull = 0
        l_serialNum = []
        l_excelNum = []
        d_serialRow = {}
        inter_joint = ''
        for i in range(1, self.sheet1.nrows):  # 当前工作表总行数：如 5
            if self.sheet1.cell_value(i, 0) != u"":
                serialNums += 1  # 接口总数量：如 3
                l_serialNum.append(int(self.sheet1.cell_value(i, 0)))  # 接口序列号列表：如 [1,2,3]
                l_excelNum.append(serialNums + serialNumNull + 1)  # excel序列号列表：如 [2,3,5]
            else:
                serialNumNull += 1  # 统计到最后一行记录为止，序号一列为空的总数量
            d_serialRow = dict(zip(l_serialNum, l_excelNum))  #  接口与excel序列号字典：如 {1: 2, 2: 3, 3: 5, 4: 6}

        # 遍历接口数量
        for j in range(len(l_excelNum)):
            # # 判断下一个接口是否是最后一个
            if j == len(l_excelNum)-1:
                # 最后一个接口的一个参数
                if self.sheet1.nrows == l_excelNum[-1]:
                    self.d_inter[self.sheet1.cell_value(l_excelNum[j] - 1, 3)] = self.sheet1.cell_value(l_excelNum[j] - 1, 5)
                else:
                # 最后一个接口的多个参数
                    lastInterParam = self.sheet1.nrows - l_excelNum[-1]
                    for i in range(lastInterParam+1):
                        inter_joint = inter_joint + ',' + self.sheet1.cell_value(l_excelNum[j] - 1 + i, 5)
                    self.d_inter[self.sheet1.cell_value(l_excelNum[j] - 1, 3)] = inter_joint[1:]
                    inter_joint =''
            else:
                # 1个参数
                if l_excelNum[j] + 1 == l_excelNum[j+1]:
                    self.d_inter[self.sheet1.cell_value(l_excelNum[j]-1, 3)] = self.sheet1.cell_value(l_excelNum[j]-1, 5)
                else:
                # 多个参数
                    x = l_excelNum[j + 1] - l_excelNum[j]
                    for k in range(x):
                        inter_joint = inter_joint + ',' + self.sheet1.cell_value(l_excelNum[j] -1 + k, 5)
                    self.d_inter[self.sheet1.cell_value(l_excelNum[j] - 1, 3)] = inter_joint[1:]
                    inter_joint = ''
        # print(self.d_inter)  # {'/inter/HTTP/auth': 'none', '/inter/HTTP/login': 'username,password', '/inter/HTTP/logout': 'test,hhh'}

        # 遍历接口表的isRun，获取isRunAll,isRunY,isNoRun ,如：[[], [], 5]
        isRunAll = 0
        l_isRunAll = []  # 执行所有接口列表
        l_isRunY = []  # 执行 isRun = Y 接口的列表
        l_isNoRun = []  # 不执行 isRun = N 接口的列表
        l_interName = []  # 接口名列表，通过isRun控制所需测试的接口，如： # ['/inter/HTTP/auth', '/inter/HTTP/login'] 表示只测试这2个接口
        l_isRun = []
        for i in range(1, len(d_serialRow) + 1):
            # 如果isRun为空
            if self.sheet1.cell_value(d_serialRow.get(i) - 1, 1) == 'Y' or self.sheet1.cell_value(d_serialRow.get(i) - 1, 1) == 'y':
                l_isRunY.append(d_serialRow.get(i))
                keyword = str(self.sheet1.cell_value(d_serialRow.get(i) - 1, 3))
                l_interName.append(keyword)
            elif self.sheet1.cell_value(d_serialRow.get(i) - 1, 1) == 'N' or self.sheet1.cell_value(d_serialRow.get(i) - 1, 1) == 'n':
                l_isNoRun.append(d_serialRow.get(i))
            else:
                isRunAll += 1
        if isRunAll == len(d_serialRow):
            for k, v in d_serialRow.items():
                l_isRunAll.append(v)
                l_interName.append(str(self.sheet1.cell_value(int(v-1), 3)))
        l_isRun.append(l_isRunY)
        l_isRun.append(l_isNoRun)
        l_isRun.append(len(l_isRunAll))
        # print(l_isRun)
        return l_isRun

    def getCaseParam(self):
        '''
        遍历case获取参数
        :param l_interIsRun: [[2, 3, 5], [], 0] , 3个列表分表表示isRunY,isNoRun,isRunAll
        :param interName: '/inter/HTTP/auth'
        :return: [[2，'获取Token', 'post', '/inter/HTTP/auth', 'None', '$.status','200']]
        '''
        l_case = []
        l_casesuit = []

        for i in range(1, self.sheet2.nrows):
            if self.sheet2.cell_value(i, 0) == 'N' or self.sheet2.cell_value(i, 0) == 'n':
                pass
            else:
                l_case.append(i)  # excelNO
                l_case.append(self.sheet2.cell_value(i, 3))  # caseName
                l_case.append(self.sheet2.cell_value(i, 4))  # method
                l_case.append(self.sheet2.cell_value(i, 5))  # interName
                l_case.append(self.sheet2.cell_value(i, 6))  # param
                l_case.append(self.sheet2.cell_value(i, 7))  # jsonpath
                l_case.append(self.sheet2.cell_value(i, 8))  # expected
                l_casesuit.append(l_case)
                l_case = []

        # print(l_casesuit)
        return l_casesuit

    def getCaseParam123(self, l_interIsRun, interName):
        '''
        遍历case获取参数
        :param l_interIsRun: [[2, 3, 5], [], 0] , 3个列表分表表示isRunY,isNoRun,isRunAll
        :param interName: '/inter/HTTP/auth'
        :return: [[2，'获取Token', 'post', '/inter/HTTP/auth', 'None', '$.status','200']]
        '''
        l_case = []
        l_casesuit = []

        # isRun 为空 （case工作表）
        if l_interIsRun[2] > 0:
            for i in range(1, self.sheet2.nrows):
                if self.sheet2.cell_value(i, 5) == interName:
                    if self.sheet2.cell_value(i, 0) == 'N' or self.sheet2.cell_value(i, 0) == 'n':
                        pass
                    else:
                        l_case.append(i)  # excelNO
                        l_case.append(self.sheet2.cell_value(i, 3))  # caseName
                        l_case.append(self.sheet2.cell_value(i, 4))  # method
                        l_case.append(self.sheet2.cell_value(i, 5))  # interName
                        l_case.append(self.sheet2.cell_value(i, 6))  # param
                        l_case.append(self.sheet2.cell_value(i, 7))  # jsonpath
                        l_case.append(self.sheet2.cell_value(i, 8))  # expected
                        l_casesuit.append(l_case)
                        l_case = []
        else:
            if len(l_interIsRun[0]) == 0:  # isNoRun
                # 遍历 inter 中 isRun <> N 的case
                l_isNoRun = []
                for i in l_interIsRun[1]:
                    l_isNoRun.append(self.sheet1.cell_value(i - 1, 4))
                for i in range(1, self.sheet2.nrows):
                    if self.sheet2.cell_value(i, 5) not in l_isNoRun:
                        if self.sheet2.cell_value(i, 5) == interName:
                            # 遍历 isRun from case
                            if self.sheet2.cell_value(i, 0) == 'N' or self.sheet2.cell_value(i, 0) == 'n':
                                pass
                            else:
                                l_case.append(i)  # excelNO
                                l_case.append(self.sheet2.cell_value(i, 3))  # caseName
                                l_case.append(self.sheet2.cell_value(i, 4))  # method
                                l_case.append(self.sheet2.cell_value(i, 5))  # interName
                                l_case.append(self.sheet2.cell_value(i, 6))  # param
                                l_case.append(self.sheet2.cell_value(i, 7))  # jsonpath
                                l_case.append(self.sheet2.cell_value(i, 8))  # expected
                                l_casesuit.append(l_case)
                                l_case = []
            else:
                # isRunY
                l_isRunY = []
                for i in l_interIsRun[0]:
                    l_isRunY.append(self.sheet1.cell_value(i - 1, 3))
                for i in range(1, self.sheet2.nrows):
                    if self.sheet2.cell_value(i, 4) in l_isRunY:
                        if self.sheet2.cell_value(i, 4) == interName:
                            # 遍历 isRun from case
                            if self.sheet2.cell_value(i, 0) == 'N' or self.sheet2.cell_value(i, 0) == 'n':
                                pass
                            else:
                                l_case.append(i)  # excelNO
                                l_case.append(self.sheet2.cell_value(i, 3))  # caseName
                                l_case.append(self.sheet2.cell_value(i, 4))  # method
                                l_case.append(self.sheet2.cell_value(i, 5))  # interName
                                l_case.append(self.sheet2.cell_value(i, 6))  # param
                                l_case.append(self.sheet2.cell_value(i, 7))  # jsonpath
                                l_case.append(self.sheet2.cell_value(i, 8))  # expected
                                l_casesuit.append(l_case)
                                l_case = []

        # print(l_casesuit)
        return l_casesuit

    def setCaseParam(self, excelNo, generation, result, response):
        '''
        将结果保存到case用例中，对应字段有 generation,result,resposne,执行日期
        :param excelNo: case编号
        :param generation: 生成关键字，如 userid=1 或 为空
        :param result: pass 或 Fail
        :param response: {'status': 200, 'msg': '恭喜您，登录成功', 'userid': '1'}
        '''
        self.wSheet.write(excelNo, 9, generation, self.styleBlue)  # generation
        if result =='pass':self.wSheet.write(excelNo, 10, result, self.styleBlue)  # result
        else:self.wSheet.write(excelNo, 10, result, self.styleRed)  # result
        self.wSheet.write(excelNo, 11, response, self.styleBlue)  # response
        self.wSheet.write(excelNo, 12, str(datetime.now().strftime("%Y%m%d%H%M%S")), self.styleBlue)  # 执行日期
        self.wbk.save(self.varExcel)

    def result(self, excelNo, caseName, method, interName, param, jsonpathKey, expected, d_inter, *generation):
        '''解析参数'''
        if len(generation) > 1 :
                param = param.replace(generation[0], generation[1])
        print(param)
        jsonres = reflection.run([caseName, method, interName, param])
        d_jsonres = json.loads(jsonres)
        jsonpathValue = jsonpath.jsonpath(d_jsonres, expr=jsonpathKey)
        jsonpathValue = str(jsonpathValue[0])
        # 断言预期结果
        if jsonpathValue != expected:
            self.setCaseParam(excelNo, '', 'Fail', str(d_jsonres))
            assert jsonpathValue == expected, "预期值是<" + expected + ">，而实测值是<" + jsonpathValue +">"
            return False
        else:
            self.setCaseParam(excelNo, '', 'pass', str(d_jsonres))
            return d_jsonres

if __name__ == '__main__':
    xls = XLS()
    # xls.setCaseParam(3,'userid=12', 'pass' ,"{'status': 200, 'msg': '恭喜您，登录成功', 'userid': '1'}")