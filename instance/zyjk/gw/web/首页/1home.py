# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 首页
# *****************************************************************
import sys,os
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)
from GwPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO = GwPO(logName)
from PO.Base64PO import *
Base64_PO = Base64PO()
from PO.StrPO import *
Str_PO = StrPO()
from PO.TesseractPO import *
Tesseract_PO = TesseractPO()
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('../config.ini')
# 登录
Gw_PO.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))

# 首页
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[1]", 2)  # 点击一级菜单首页



# todo 获取左边内容(档案概况、三高概况、重点人群分布情况)
d_left = {}
l_ = Web_PO.getTextByXs("//div[@class='dashed_left']")
l_1 = l_[0].split("\n")
# print(l_1)

l_2 = List_PO.split(l_1, "三高概况", 0)
l_2.pop(0)
d_1 = List_PO.pair2dict(l_2)
d_left['档案概况'] = d_1
l_3 = List_PO.split(l_1, "三高概况", 1)
l_4 = List_PO.split(l_3, "重点人群分布情况", 0)
d_4 = List_PO.pair2dict(l_4)
d_left['三高概况'] = d_4
l_5 = List_PO.split(l_3, "重点人群分布情况", 1)
d_left['重点人群分布情况'] = l_5
# print(d_left)  # {'档案概况': {'个人档案（份）': '121', '家庭档案（份）': '106'}, '三高概况': {'三高居民(人)': '2', '两高居民(人)': '4'}, '重点人群分布情况': ['高血压', '糖尿病', '高血脂', '肺结核', '精神障碍', '老年人', '孕产妇', '0～6岁儿童', '脑卒中', '冠心病', '残疾人']}

# 获取重点人群分布情况各个疾病的图形
# d['重点人群分布情况']  # ['高血压', '糖尿病', '高血脂', '肺结核', '精神障碍', '老年人', '孕产妇', '0～6岁儿童', '脑卒中', '冠心病', '残疾人']
d_ = {}
for k in range(len(d_left['重点人群分布情况'])):
    base64 = Web_PO.canvas2base64("/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[6]/div[" + str(k+1) + "]/div[1]/div[1]/canvas")
    image_path = Base64_PO.base64ToImg(base64, d_left['重点人群分布情况'][k])
    # print(image_path)  # /Users/linghuchong/Downloads/51/Python/project/instance/zyjk/gw/web/首页/高血压.png
    img = Image.open(image_path)
    recognized_text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    l_result = recognized_text.strip().split()
    print(d_left['重点人群分布情况'][k], l_result)
    l_1 = []
    for i in range(len(l_result)):
        if '%' in l_result[i]:
            l_1.append(l_result[i])
        if Str_PO.isNumber(l_result[i]):
            l_1.append(l_result[i])
        elif l_result[i] == '4A':
            l_1.append('14')
        elif l_result[i] == '8A':
            l_1.append('8')
        elif l_result[i] == '20A':
            l_1.append('20')
        elif l_result[i] == '3A':
            l_1.append('3')
        elif l_result[i] == '1A':
            l_1.append('1')
    # print(l_1)
    d_[d_left['重点人群分布情况'][k]] = l_1
# print(d_)
d_left['重点人群分布情况'] = d_
# print(d_left)
# {'档案概况': {'个人档案（份）': '121', '家庭档案（份）': '106'},
# '三高概况': {'三高居民(人)': '2', '两高居民(人)': '4'},
# '重点人群分布情况': {'高血压': ['9.92%', '12', ''], '糖尿病': ['7.44%', '9', ''], '高血脂': ['8.26%', '10', ''], '肺结核': ['2.48%', '3', ''], '精神障碍': ['7.44%', '9', ''], '老年人': ['14.05%', '17', ''], '孕产妇': ['4.13%', '5', ''], '0～6岁儿童': ['14.05%', '17', ''], '脑卒中': ['3.31%', '4', ''], '冠心病': ['2.48%', '3', ''], '残疾人': ['5.79%', 'T', '']}}



# todo 获取右边内容（建卡档案、任务提醒）
l_ = Web_PO.getTextByXs("//div[@class='dashed_right']")
l_2 = l_[0].split("\n")
# print(l_2)  # ['健康档案', '档案迁出待审', '0', '暂不管理', '3', '死亡', '19', '任务提醒', '高血压随访', '10', '糖尿病随访', '8', '0～6岁儿童随访', '7', '孕产妇随访', '4', '肺结核随访', '9', '残疾人随访', '5', '精神病障碍随访', '2']
d_right = {}
l_3 = List_PO.split(l_2, '任务提醒', 0)
l_3.pop(0)
# print(l_3)
d_3 = List_PO.pair2dict(l_3)
# print(d_3)
d_right['健康档案'] = d_3

l_4 = List_PO.split(l_2, '任务提醒', 1)
# print(l_4)
d_4 = List_PO.pair2dict(l_4)
# print(d_4)
d_right['任务提醒'] = d_4
# d_3.update(d_4)
# print(d_right)

d_left.update(d_right)
print(d_left)
