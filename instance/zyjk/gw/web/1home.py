# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 首页
# *****************************************************************

from GwPO import *
Gw_PO = GwPO()

from PO.Base64PO import *
Base64_PO = Base64PO()

from PO.TesseractPO import *
Tesseract_PO = TesseractPO()

# 1，登录
Gw_PO.login('http://192.168.0.203:30080/#/login', '11011', 'HHkk2327447')

# 首页
Web_PO.clkByX("/html/body/div[1]/div/div[1]/div[2]/ul/li[1]", 2)  # 点击一级菜单首页

# 获取左边内容，生成字典
l_ = Web_PO.getTextByXs("//div[@class='dashed_left']")
l_1 = l_[0].split("\n")
# print(l_1)
d = {}
l_2 = List_PO.split(l_1, "三高概况", 0)
l_2.pop(0)
d_1 = List_PO.pair2dict(l_2)
d['档案概况'] = d_1
l_3 = List_PO.split(l_1, "三高概况", 1)
l_4 = List_PO.split(l_3, "重点人群分布情况", 0)
d_4 = List_PO.pair2dict(l_4)
d['三高概况'] = d_4
l_5 = List_PO.split(l_3, "重点人群分布情况", 1)
d['重点人群分布情况'] = l_5
# print(d)  # {'档案概况': {'个人档案（份）': '121', '家庭档案（份）': '106'}, '三高概况': {'三高居民(人)': '2', '两高居民(人)': '4'}, '重点人群分布情况': ['高血压', '糖尿病', '高血脂', '肺结核', '精神障碍', '老年人', '孕产妇', '0～6岁儿童', '脑卒中', '冠心病', '残疾人']}

# 获取重点人群分布情况各个疾病的图形
d['重点人群分布情况']  # ['高血压', '糖尿病', '高血脂', '肺结核', '精神障碍', '老年人', '孕产妇', '0～6岁儿童', '脑卒中', '冠心病', '残疾人']
d_ = {}
for i in range(len(d['重点人群分布情况'])):
    base64 = Web_PO.canvas2base64("/html/body/div[1]/div/div[2]/section/div/div/div[1]/div[6]/div[" + str(i+1) + "]/div[1]/div[1]/canvas")
    pathFile = Base64_PO.base64ToImg(base64, d['重点人群分布情况'][i])
    a = Tesseract_PO.image2string(pathFile, 'eng')
    a = a.split("\n")
    if "A" in a[1]:
        a[1] = a[1][:-1]
    elif 'T' in a[1]:
        a[1] = "7"
    elif "ZN" in a[1]:
        a[1] = "17"
    elif "ar" in a[1]:
        a[1] = "4"
    # print(a)
    a.pop(2)
    d_[d['重点人群分布情况'][i]] = a
# print(d_)
d['重点人群分布情况'] = d_

print(d)
# {'档案概况': {'个人档案（份）': '121', '家庭档案（份）': '106'},
# '三高概况': {'三高居民(人)': '2', '两高居民(人)': '4'},
# '重点人群分布情况': {'高血压': ['9.92%', '12', ''], '糖尿病': ['7.44%', '9', ''], '高血脂': ['8.26%', '10', ''], '肺结核': ['2.48%', '3', ''], '精神障碍': ['7.44%', '9', ''], '老年人': ['14.05%', '17', ''], '孕产妇': ['4.13%', '5', ''], '0～6岁儿童': ['14.05%', '17', ''], '脑卒中': ['3.31%', '4', ''], '冠心病': ['2.48%', '3', ''], '残疾人': ['5.79%', 'T', '']}}



# # 获取右边内容，生成列表
# l_ = Web_PO.getTextByXs("//div[@class='dashed_right']")
# l_1 = l_[0].split("\n")
# # print(l_1)
# print(List_PO.getNextEle(l_1, '高血压随访'))

