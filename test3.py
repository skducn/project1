# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
#  publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
#  privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# *****************************************************************
import json
d_query = {'id': 123}
# d_query = json.dumps(d_query)
# print(d_query['id'])
key = list(d_query.keys())[0]
print(key)
# d_query = {'id':123}
# print(list(d_query.keys())[0])

# pip install selenium tensorflow numpy scikit-learn
# # 3. 数据准备
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
#
# # 3. 数据准备
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
# # 2. 使用Selenium提取网页元素特征
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import numpy as np
# from PO.WebPO import *
#
# Web_PO = WebPO("chrome")
#
# # # print("1.1 打开网站".center(100, "-"))
# # Web_PO.openURL("http://192.168.0.243:5000/")
# Web_PO.openURL("http://192.168.0.203:30080/login?redirect=/index")
#
#
# # 3. 数据准备
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
#
# # 4. 构建RNN模型
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
#
#
# # 提取按钮元素的特征
# # 提取按钮元素的特征
# buttons = Web_PO.test1()
# predicted_labels = []
#
# for button in buttons:
#     text = button.text
#     size = button.size
#     location = button.location
#
#     # 将特征转换为数值
#     feature = [len(text), size['width'], size['height'], location['x'], location['y']]
#     feature = np.array(feature).reshape(1, -1)
#
#     # 使用模型进行预测
#     model = Sequential()
#     prediction = model.predict(feature)
#     label_encoder = LabelEncoder()
#     predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])
#     predicted_labels.append(predicted_label[0])
#
# # 输出预测结果
# for i, button in enumerate(buttons):
#     print(f'Button {i}: Predicted Label = {predicted_labels[i]}')
#
# # 关闭浏览器
# Web_PO.quit()