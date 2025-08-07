# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2025-8-4
# Description: 专病库
# 需求gitlab：http://192.168.0.241/cdrd_product_doc/product_doc
# 接口：http://192.168.0.243:8083/prod-api/doc.html#/home/
# 接口json：http://192.168.0.243:8083/prod-api/v2/api-docs
# *****************************************************************

from CdrdPO import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Cdrd_PO = CdrdPO()


# 登录
print(Cdrd_PO.getTokenByLogin())

# # 获取科室列表
# print(Cdrd_PO.getDepartment())

# 用户,批量生成N个
print(Cdrd_PO.crtUser(2))










