# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2024-3-8
# Description: CHC规则包
# http://192.168.0.243:8010/
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import random

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database"))  # 测试环境
Sqlserver_PO2 = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database2"))  # 测试环境

from PO.TimePO import *
Time_PO = TimePO()

from PO.DataPO import *
Data_PO = DataPO()

from PO.FakePO import *
Fake_PO = FakePO()


class ChcPO():


    def getHospital(self):

        # 获取医院信息表字典（机构编码：机构名）
        d_hospital = {}
        l_ = Sqlserver_PO2.select("select ORG_CODE,ORG_NAME from SYS_hospital")
        for d in l_:
            d_hospital[d['ORG_CODE']] = d['ORG_NAME']
        # print(d_hospital)  # {'0000001': '静安精神病院', 'csdm': '彭浦新村街道社区健康管理中心', ...
        return d_hospital

    def getUserInfo(self):

        # 获取当前用户信息
        d_ = {}
        l_ = Sqlserver_PO2.select(
            "select NAME,THIRD_NO,ORG_CODE from SYS_USER where user_name='%s'" % (Configparser_PO.USER("user")))
        d_['doctorName'] = l_[0]['NAME']
        # print("家庭医生 => ", varNAME)  # 小茄子

        d_['wkno'] = l_[0]['THIRD_NO']
        # print("家庭医生的工号 => ", varTHIRD_NO)  # 1231231

        d_['orgCode'] = l_[0]['ORG_CODE']
        # print("机构编号 => ", varORG_CODE)  # 0000001

        l_ = Sqlserver_PO2.select("select ORG_NAME from SYS_hospital where org_code='%s'" % (l_[0]['ORG_CODE']))
        d_['orgName'] = l_[0]['ORG_NAME']
        # print("机构名称 => ", varORG_NAME)  # 静安精神病院

        return d_

    def getCategoryList(self, l_category):

        # 获取人群分类
        # getCategoryList(['0-6岁儿童', '学生（7-17岁）', '普通人群', '老年人', '未分类', '孕妇', '产妇'])
        d_category = dict(enumerate(l_category, start=1))
        return (d_category)  # {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}

        # print(list(d_category.keys()))  # [1, 2, 3, 4, 5, 6, 7]
        # randomCategoryKey = random.sample(list(d_category.keys()), 1)[0]
        # print(randomCategoryKey, d_category[randomCategoryKey])   # 随机获取字典的key, 如：("2", d_category[2])

    def genIdcardByCategory(self, varCategory):

        # 通过人群分类生成身份证
        # {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}
        # self.getIdcardByCategory(4)

        currYear = Time_PO.getYear()

        if varCategory == 1:
            birthyear = int(currYear) - 2
            birthmonth = "01"
            birthday = "01"
        elif varCategory == 2:
            birthyear = int(currYear) - 8
            birthmonth = "02"
            birthday = "02"
        elif varCategory == 3:
            birthyear = int(currYear) - 20
            birthmonth = "03"
            birthday = "03"
        elif varCategory == 4:
            birthyear = int(currYear) - 66
            birthmonth = "04"
            birthday = "04"
        elif varCategory == 5:
            birthyear = int(currYear) - 40
            birthmonth = "05"
            birthday = "05"
        elif varCategory == 6:
            birthyear = int(currYear) - 30
            birthmonth = "06"
            birthday = "06"
        elif varCategory == 7:
            birthyear = int(currYear) - 35
            birthmonth = "07"
            birthday = "07"

        # 预设地区:
        codelist = ["110101", "110102", "110105", "110106", "110107", "420117", "420200", "420202", "420203", "420204",
                    "420205", "310101"]  # 随便设置了几个地区，基本都是湖北和北京的；
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                     '10': '2'}  # 校验码映射

        # 身份证前6位
        try:
            id = codelist[random.randint(0, len(codelist))]  # 地区项
        except:
            id = "110101"

        # 7-10位，出生年份
        try:
            birthdayStr = str(birthyear).zfill(4) + str(birthmonth).zfill(2) + str(birthday).zfill(2)
            id = id + birthdayStr
        except:
            id = id + "19900101"

        # 最后4位的随机前3位
        sex = ""
        try:
            sign = random.randint(1, 999)
            if sign % 2 == 0:
                sex = "女"
            else:
                sex = "男"
            id = id + str(sign).zfill(3)  # 顺序号简单处理
        except:
            id = id + "999"
        # 判断性别

        sum_1 = 0
        for a in range(17):
            sum_1 = sum_1 + int(id[a]) * weight[a]
        index_id = sum_1 % 11
        result_id = id + str(checkcode[str(index_id)])  # 最终号码

        return (result_id,sex)


    # todo HRPERSONBASICINFO(基本信息表)
    def insert_HRPERSONBASICINFO(self, idcard, residentName):
        # 删除已存在记录
        Sqlserver_PO.execute("delete from HRPERSONBASICINFO where ARCHIVENUM = '%s'" % (idcard))
        # 插入记录
        Sqlserver_PO.insert("HRPERSONBASICINFO", {"ARCHIVENUM": idcard, "NAME": residentName, "IDCARD": idcard,
                                                  "CREATETIME": time.strftime("%Y-%m-%d %H:%M:%S")})

    # todo TB_EMPI_INDEX_ROOT(患者主索引表)
    def insert_TB_EMPI_INDEX_ROOT(self, idcard, residentName):

        varGUID = Data_PO.getFigures(8)
        # 删除已存在记录
        Sqlserver_PO.execute("delete from TB_EMPI_INDEX_ROOT where IDCARDNO = '%s'" % (idcard))
        # 插入记录
        Sqlserver_PO.insert("TB_EMPI_INDEX_ROOT", {"GUID": varGUID, "NAME": residentName, "IDCARDNO": idcard})

    # todo 新建居民(签约信息表、基本信息表、患者主索引表)
    def newResident(self, CATEGORY_CODE):

        # 新建一个签约客户QYYH，同时更新签约信息表、基本信息表、患者主索引表 3张表
        # {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}
        d_category = {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}

        # 通过人群分类生成身份证
        d_sex = {'男': 1, '女': 2, '未知性别': 3}
        for i in range(20):
            idcard, sexName = self.genIdcardByCategory(CATEGORY_CODE)
            if (CATEGORY_CODE == 6 or CATEGORY_CODE == 7) and sexName == '女':
                break
        # print(idcard, sexName)

        # 获取当前登录用户信息, {'doctorName': '小茄子', 'wkno': '1231231', 'orgCode': '0000001', 'orgName': '静安精神病院'}
        d_getUserInfo = self.getUserInfo()

        # 生成随机姓名
        residentName = Fake_PO.genName('Zh_CN', 1)

        # 随机地址
        JJDZ = Fake_PO.genAddress('zh_CN', 1)

        # 随机电话
        SJHM = Fake_PO.genPhone_number('Zh_CN', 1)

        # 1，签约信息表
        # QYYH，删除已存在记录
        Sqlserver_PO.execute("delete from QYYH where SFZH = '%s'" % (idcard))

        # QYYH，插入记录
        Sqlserver_PO.insert("QYYH", {"CZRYBM": d_getUserInfo['wkno'], "CZRYXM": d_getUserInfo['doctorName'],
                                     "JMXM": residentName, "SJHM": SJHM,
                                     "SFZH": idcard, "JJDZ": JJDZ,
                                     "ARCHIVEUNITCODE": d_getUserInfo['orgCode'],
                                     "ARCHIVEUNITNAME": d_getUserInfo['orgName'],
                                     "SIGNSTATUS": 1, "SIGNDATE": "2023-01-01", "CATEGORY_CODE": CATEGORY_CODE,
                                     "CATEGORY_NAME": d_category[CATEGORY_CODE], "SEX_CODE": d_sex[sexName], "SEX_NAME": sexName, "LAST_SERVICE_DATE": "2023-05-06",
                                     "KEY_POPULATION": 1, "REPORT_STATUS": 0, "LATEST_ASSESS_DATE": "2024-10-10",
                                     "LATEST_CONFIRM_DATE": "2024-11-11"})

        # 2，基本信息表
        self.insert_HRPERSONBASICINFO(idcard, residentName)

        # 3，患者主索引表
        self.insert_TB_EMPI_INDEX_ROOT(idcard, residentName)

        s_getUserInfo = json.dumps(d_getUserInfo, ensure_ascii=False)
        Sqlserver_PO.execute("insert a_autoIdcard (tblName,idcard,category,userInfo) values ('%s','%s','%s','%s')" % (u'签约信息表,基本信息表,患者主索引表',str(idcard), str(CATEGORY_CODE), s_getUserInfo))

