# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-11-10
# Description: 体重管理 - 体重状态判断 （a_WSA）
# 需求：调用保存体重管理报告接口，判断体重状态。
# 实现方式：
# 1，自动获取身份证号，从QYYH和WEIGHT_REPORT中匹配相同身份证，同时获取WEIGHT_REPORT（ID）
# 2，测试数据导入DB，从word - excel - db

# todo 接口文档
# http://192.168.0.243:8014/doc.html#/default/
# 登录接口
# http://192.168.0.243:8011/doc.html#/chc-auth/%E7%99%BB%E5%BD%95%E6%A8%A1%E5%9D%97/loginUsingPOST
# 保存体重管理报告接口
# http://192.168.0.243:8014/doc.html#/default/Weight-%E4%BD%93%E9%87%8D%E6%8A%A5%E5%91%8A%E8%AE%B0%E5%BD%95%E8%A1%A8/saveOrUpdateWeightManageUsingPOST
# 注意：登录接口端口8011，保存体重管理报告接口端口8014

# todo 测试数据
# 数据源 - 体重状态判断1.23.5
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=01ia7z
# 使用ai，将表格内容转为列表，如：(7<=年龄<7.5 and 13.9<=BMI<17.0 and 性别=男) or (7.5<=年龄<8 and 13.9<=BMI<17.4 and 性别=男) ，将以上格式转换成['(7<=年龄<8 and 13.9>BMI and 性别=男)',' (8<=年龄<9 and 14.0>BMI and 性别=男)']格式
#***************************************************************
from WsaPO import *
Wsa_PO = WsaPO()

# # todo excel导入db
# Wsa_PO.excel2db()



# todo 执行规则
Wsa_PO.main()  # 执行所有


# Wsa_PO.main({"id": 1})
# Wsa_PO.main({"id": [6, 7, 8]})  # 执行3个

# todo 所有普通人
# Wsa_PO.main({"category": '普通人群'})  # 执行所有学生
# Wsa_PO.main({"category": '老年人'})  # 执行所有学生
# Wsa_PO.main({"category": '儿童'})  # 执行所有儿童
# Wsa_PO.main({"category": '学生'})  # 执行所有学生

# todo 所有体重偏低
# Wsa_PO.main({"weightStatus": '体重偏低'})

# todo 儿童
# Wsa_PO.main({"category": '儿童', "weightStatus": '体重偏低'})  # 执行学生和体重偏低
# Wsa_PO.main({"category": '儿童', "weightStatus": '正常'})
# Wsa_PO.main({"category": '儿童', "weightStatus": '超重'})
# Wsa_PO.main({"category": '儿童', "weightStatus": '肥胖'})

# todo 学生
# Wsa_PO.main({"category": '学生', "weightStatus": '体重偏低'})  # 执行学生和体重偏低
# Wsa_PO.main({"category": '学生', "weightStatus": '正常'})
# Wsa_PO.main({"category": '学生', "weightStatus": '超重'})
# Wsa_PO.main({"category": '学生', "weightStatus": '肥胖'})


