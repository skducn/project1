# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-5-9
# Description: 体重管理1.0, 体重状态
# 需求：体重管理1.18
# 【腾讯文档】体重管理1.18规则自动化
# https://docs.qq.com/sheet/DYmxVUGFZRWhTSHND?tab=rprd0r
#***************************************************************

from WeightPO import *
Weight_PO = WeightPO()

# 参数
varBMI = 18.4

# 跑接口
command = 'curl -X POST "http://192.168.0.243:8014/weight/saveOrUpdateWeightManage" -H "Request-Origion:SwaggerBootstrapUi" -H "accept:*/*" -H "Authorization:" -H "Content-Type:application/json" -d "{\\"age\\":15,\\"ageFloat\\":0,\\"ageMonth\\":40,\\"basicIntake\\":100,\\"bmi\\":' + str(varBMI) + ',\\"categoryCode\\":\\"4\\",\\"disease\\":\\"无\\",\\"foodAdvice\\":\\"建议饮食\\",\\"height\\":175,\\"hipline\\":33,\\"id\\":2,\\"idCard\\":\\"420204202201011268\\",\\"orgCode\\":\\"0000001\\",\\"orgName\\":\\"静安精神病院\\",\\"sex\\":\\"男\\",\\"sexCode\\":\\"1\\",\\"sportAdvice\\":\\"建议运动\\",\\"targetWeight\\":50,\\"waistHip\\":0.9,\\"waistline\\":33,\\"weight\\":55,\\"weightRecordId\\":0}"'
# print(command)
p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
str_r = bytes.decode(out)
d_r = json.loads(str_r)
print(d_r)

# 检查


# # todo 2, 运行主程序
Weight_PO.main(Configparser_PO.DB("table"), 'all')  # 执行全部记录






