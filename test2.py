# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
#  publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
#  privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# *****************************************************************
# pip install selenium tensorflow numpy scikit-learn

# # 3. 数据准备
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
# # 4. 构建RNN模型
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense

import numpy as np
from PO.WebPO import *
Web_PO = WebPO("chrome")
Web_PO.openURL("http://192.168.0.203:30080/login?redirect=/index")
# 提取按钮元素的特征
l_ = Web_PO.getXpathByLabel('button')
print(l_)
d_ = Web_PO.getTextXpathByLabel("button", "/span")
print(d_)

l_ = Web_PO.getXpathByLabel('input')
print(l_)
d_ = Web_PO.getValueXpathByLabel("input", "placeholder")
print(d_)





# features = []
# labels = []
#
# for button in buttons:
#     text = button.text
#     size = button.size
#     location = button.location
#
#     # 将特征转换为数值
#     feature = [len(text), size['width'], size['height'], location['x'], location['y']]
#     features.append(feature)
#     labels.append('button')  # 假设所有提取的元素都是按钮
#
# # 关闭浏览器
Web_PO.quit()
# //*[@id="app"]/div/div/div/div/div[4]/div[2]/form/div[7]/button
# /html/body/div[1]/div/div/div/div/div[2]/div[2]/form/div[4]/button
# /html/body/div[1]/div/div/div/div/div[3]/div[2]/form/div[4]/button
# /html/body/div[1]/div/div/div/div/div[4]/div[2]/form/div[7]/button


# /html/body/  div[1]/div/div/div/div/div[2]/div[2]/form/div[1]/div/div[1]/input
# id("app")/   DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[1]/DIV[1]/DIV[1]/INPUT[1]

# /html/body/  div[1]/div/div/div/div/div[2]/div[2]/form/div[2]/div/div[1]/input
# Button 2: XPath = id("app")/DIV[1]/DIV[1]/DIV[1]/DIV[1]/DIV[2]/DIV[2]/FORM[1]/DIV[2]/DIV[1]/DIV[1]/INPUT[1]

#
# # 将特征和标签转换为numpy数组
# features = np.array(features)
# labels = np.array(labels)

# /html/body/div[1]/div/div/div/div/div[2]/div[2]/form/div[4]/button


