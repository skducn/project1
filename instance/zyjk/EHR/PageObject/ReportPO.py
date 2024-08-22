# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-12-9
# Description:  质控报告 EHR对象库
# *****************************************************************


# [ERROR] 表13.签约居民中高血压患者管理人数占家庭医生签约总人数占比，line 2,expected(9.55) <> actual(9.41)
# [ERROR] 表13.签约居民中高血压患者管理人数占家庭医生签约总人数占比，line 2,expected(9.55) <> actual(9.41)
# [ERROR] 表13.签约居民中高血压患者管理人数占家庭医生签约总人数占比，line 2,expected(9.55) <> actual(9.41)
# [ERROR] 表13.签约居民中高血压患者管理人数占家庭医生签约总人数占比, line 2, expected(9.55) <> actual(9.41)
# [ERROR] Excel No.2, expected(9.55) <> actual(9.41)

from PO.OpenpyxlPO import *
import sys,os
from PO.StrPO import *
Str_PO = StrPO()
from PO.ColorPO import *
Color_PO = ColorPO()

class ReportPO():

    def __init__(self):
        self.Openpyxl_PO = OpenpyxlPO("v2.xlsx")

    def colResult(self, l_param):

        ''' 表格列统计验证 '''
        # colResult(["表1.电子健康档案建档率", "=", "辖区内常住人口建立电子健康档案人数", "/", "辖区内常住人口数", 2])
        # colResult(["表13.签约居民中高血压患者管理人数占家庭医生签约总人数占比", "=", "签约居民中高血压患者管理人数", "/", "签约人数", "*100", 2, ["if" "签约居民中高血压患者电子健康档案建档率", "=", "100", 2]]])

        varTest = ""
        l_decide = []
        for k in range(len(l_param)):
            # 1，如果有条件，则获取条件列表，如：['if', '签约居民中高血压患者电子健康档案建档率', '=', '100']
            for j in range(len(l_param[k])):
                if isinstance(l_param[k][j], list):
                    l_decide = l_param[k].pop(j)
                    # print(l_decide)  # ['if', '签约居民中高血压患者电子健康档案建档率', '=', '100']
                    break

            # 2，去条件后的参数
            # print(l_param)  # [['表13.签约居民中高血压患者管理人数占家庭医生签约总人数占比', '=', '签约居民中高血压患者管理人数', '/', '签约人数', '*100', 2]]

            varTitle = l_param[k][0]

            # 目标列
            try:
                destSheetName = str(l_param[k][0]).split(".")[0]  # 表1
                destTestResult = str(l_param[k][0]).split(".")[1]  # 电子健康档案建档率
                allData = self.Openpyxl_PO.l_getRowData(destSheetName)
                # print(allData[0])  # 第一行数据（标题）
                for i in range(len(allData[0])):
                    if allData[0][i] == destTestResult:
                        destTestResult = i
            except:
                print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")
                exit(0)

            # 处理小数点进度 0=取整，2=保留2位小数四舍五入
            varDot = l_param[k].pop(-1)

            # 逻辑列
            sum = ""
            l_param[k].pop(0)
            l_param[k].pop(0)
            # print(l_param[k])  # ['辖区内常住人口建立电子健康档案人数', '/', '辖区内常住人口数', '*100']
            # 3，将 ['辖区内常住人口建立电子健康档案人数', '/', '辖区内常住人口数', '*100']  转成  "allData[i][3]/allData[i][2]*100"
            for i in range(len(l_param[k])):
                if "." in str(l_param[k][i]) and Str_PO.isContainChinese(l_param[k][i]):
                    # 跨表比较（未完成）
                    srcSheetName = str(l_param[k][i]).split(".")[0]  # 表1
                    src1 = str(l_param[k][i]).split(".")[1]  # 辖区内常住人口建立电子健康档案人数
                else:
                    src1 = l_param[k][i]  # 辖区内常住人口建立电子健康档案人数

                    # 遍历菜单
                    for j in range(len(allData[0])):
                        if l_decide:
                            if allData[0][j] == l_decide[1]:
                                sub_col = j
                        if allData[0][j] == src1:
                            src1 = "allData[i][" + str(j) + "]"

                sum = sum + src1
                src1 = ""
            # print(sum)  # allData[i][3]/allData[i][2]*100

            # 测试
            varStatus = 0
            for i in range(1, len(allData)):
                # if round(allData[i][4], 2) == int((allData[i][3])/(allData[i][2]) * 100) :
                if varDot == 0:
                    # 精度取整
                    try:
                        if round(allData[i][destTestResult], 2) == int(eval(sum)):
                            # print("[ok] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)))
                            self.Openpyxl_PO.setCellColor(i + 1, destTestResult+1, "00E400", destSheetName)  # 正确标绿色
                            if "ok" not in varTest:
                                varTest = varTest + "ok"
                            varStatus = varStatus + 0
                        else:
                            Color_PO.consoleColor("31", "31", "[ERROR] " + varTitle + " line " + str(i + 1) + ", expected(" + str(round(allData[i][destTestResult], 2)) + ") <> actual(" + str(int(eval(sum))) + ")", "")
                            # print("[error] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)) + ", 测试值" + str(int(eval(sum))))
                            self.Openpyxl_PO.setCellColor(i + 1, destTestResult+1, "FF0000", destSheetName)  # 错误标红色
                            if "error" not in varTest:
                                varTest = varTest + "error"
                            varStatus = varStatus + 1
                    except Exception as e:
                        pass
                elif varDot == 2:
                    # 精度保留2位
                    try:
                        # 判断是否有条件
                        if l_decide:
                            # if allData[i][7] == int(l_decide[3]):
                            if eval("allData["+ str(i) + "][sub_col]" + l_decide[2] + "int(l_decide[3])") == True:

                                if round(allData[i][destTestResult], 2) == round(eval(sum), 2):
                                    # print("[ok] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)))
                                    self.Openpyxl_PO.setCellColor(i + 1, destTestResult + 1, "00E400", destSheetName)  # 正确标绿色
                                    if "ok" not in varTest:
                                        varTest = varTest + "ok"
                                    varStatus = varStatus + 0
                                else:
                                    Color_PO.consoleColor("31", "31", "[ERROR] " + varTitle + " line " + str(
                                        i + 1) + ", expected(" + str(
                                        round(allData[i][destTestResult], 2)) + ") <> actual(" + str(
                                        round(eval(sum), 2)) + ")", "")
                                    # print("[error] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)) + ", 测试值" + str(round(eval(sum), 2)))
                                    self.Openpyxl_PO.setCellColor(i + 1, destTestResult + 1, "FF0000", destSheetName)  # 错误标红色
                                    if "error" not in varTest:
                                        varTest = varTest + "error"
                                    varStatus = varStatus + 1
                        else:
                            if round(allData[i][destTestResult], 2) == round(eval(sum), 2):
                                # print("[ok] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)))
                                self.Openpyxl_PO.setCellColor(i + 1, destTestResult+1, "00E400", destSheetName)  # 正确标绿色
                                if "ok" not in varTest:
                                    varTest = varTest + "ok"
                                varStatus = varStatus + 0
                            else:
                                Color_PO.consoleColor("31", "31", "[ERROR] " + varTitle + " line " + str(i+1) + ", expected(" + str(round(allData[i][destTestResult], 2)) + ") <> actual(" + str(round(eval(sum), 2)) + ")", "")
                                # print("[error] No." + str(i+1) + ", 表格值" + str(round(allData[i][destTestResult], 2)) + ", 测试值" + str(round(eval(sum), 2)))
                                self.Openpyxl_PO.setCellColor(i + 1, destTestResult+1, "FF0000", destSheetName)  # 错误标红色
                                if "error" not in varTest:
                                    varTest = varTest + "error"
                                varStatus = varStatus + 1
                    except Exception as e:
                        pass

            if varStatus == 0 :
                print(varTitle + "（通过）")

            # 工作表标注颜色
            if varTest == "":
                self.Openpyxl_PO.setSheetColor("f1f1f1", destSheetName)
            elif "error" in varTest:
                self.Openpyxl_PO.setSheetColor("FF0000", destSheetName)
            else:
                self.Openpyxl_PO.setSheetColor("00E400", destSheetName)
            l_decide = []


    def save(self):
        self.Openpyxl_PO.save()

    def openFile(self):
        self.Openpyxl_PO.open()

    def closeExcelPid(self):
        self.Openpyxl_PO.closeExcelPid('EXCEL.EXE')