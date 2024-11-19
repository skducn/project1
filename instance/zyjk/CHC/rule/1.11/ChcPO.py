# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2024-3-8
# Description: CHC规则包
# http://192.168.0.243:8010/
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import subprocess
import pyperclip as pc
# 1、复制内容到剪贴板
# 2、粘贴剪贴板里的内容

from ConfigparserPO import *
import random
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database"))  # 测试环境
Sqlserver_PO2 = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database2"))  # 测试环境
# SqlServerPO = SqlServerPO(Configparser_PO.DB_DM("host"), Configparser_PO.DB_DM("user"), Configparser_PO.DB_DM("password"), Configparser_PO.DB_DM("port"))  # 测试环境

from PO.StrPO import *
Str_PO = StrPO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.ListPO import *
List_PO = ListPO()

from PO.DictPO import *
Dict_PO = DictPO()

from PO.DataPO import *
Data_PO = DataPO()

from PO.CharPO import *
Char_PO = CharPO()



class ChcPO():


    def getToken(self, varUser, varPass):

        # 获取登录用户的token

        command = "curl -X POST \"" + Configparser_PO.HTTP(
            "url") + ":8012/login\" -H \"accept: */*\" -H \"Content-Type: application/json\" -d \"{ \\\"password\\\": \\\"" + str(
            varPass) + "\\\", \\\"username\\\": \\\"" + str(varUser) + "\\\"}\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        if Configparser_PO.SWITCH("token") == "on":
            print(d_r['data']['access_token'])
        return d_r['data']['access_token']


    def importFull(self, sheetName):

        # 全量更新表（删除旧表，插入新表）

        try:
            # 中文转拼音
            dboTable = Char_PO.chinese2pinyin(sheetName)
            dboTable = "a_" + dboTable
            # print(dboTable)

            # 删除表
            Sqlserver_PO.execute("drop table if exists " + dboTable)

            # sheetName导入数据库，并将身份证数字型转字段型
            Sqlserver_PO.xlsx2dbByConverters(Configparser_PO.FILE("case"), dboTable, {"idcard": str}, sheetName)

            # 修改其他规则表的字段类型
            if sheetName == "测试规则" :
                Sqlserver_PO.execute("ALTER table %s alter column seq varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            #     # Sqlserver_PO.execute("ALTER TABLE %s alter column id int not null" % (dboTable))  # 设置主id不能为Null
            #     # Sqlserver_PO.execute("ALTER TABLE %s add PRIMARY KEY (id)" % (dboTable))  # 设置主键（条件是id不能为Null）
            #     Sqlserver_PO.execute("ALTER table %s alter column result varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            #     Sqlserver_PO.execute("ALTER table %s alter column step varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            #     Sqlserver_PO.execute("ALTER table %s alter column updateDate char(11)" % (dboTable))  # 将float改为char类型
            #     Sqlserver_PO.execute("ALTER table %s alter column updateDate DATE" % (dboTable))  # 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
            #     # Sqlserver_PO.execute("ALTER TABLE %s ADD var varchar(111)" % (tableName))  # 临时变量
            else:
                # 如果此列没数据，则创建后是float，需转换成char
                Sqlserver_PO.execute("ALTER table %s alter column result varchar(8000)" % (dboTable))
                Sqlserver_PO.setFieldComment(dboTable, 'result', '结果')
                Sqlserver_PO.execute("ALTER table %s alter column step varchar(8000)" % (dboTable))
                Sqlserver_PO.setFieldComment(dboTable, 'step', '步骤')
                Sqlserver_PO.execute("ALTER table %s alter column [rule] varchar(8000)" % (dboTable))
                Sqlserver_PO.setFieldComment(dboTable, 'rule', '规则集')
                Sqlserver_PO.execute("ALTER table %s alter column [case] varchar(8000)" % (dboTable))
                Sqlserver_PO.setFieldComment(dboTable, 'case', '用例')
                Sqlserver_PO.execute("ALTER table %s alter column ruleParam varchar(8000)" % (dboTable))
                Sqlserver_PO.setFieldComment(dboTable, 'ruleParam', '参数')
                # 注意如果是日期字段且没有数据，则创建后是float，需转换成char(11)，再将char改为data
                Sqlserver_PO.execute("ALTER table %s alter column updateDate char(11)" % (dboTable))  # 将float转char(11)类型
                Sqlserver_PO.execute("ALTER table %s alter column updateDate DATE" % (dboTable))  # 将char转data类型
                Sqlserver_PO.setFieldComment(dboTable, 'updateDate', '更新日期')
                Sqlserver_PO.setFieldComment(dboTable, 'tester', '测试者')

                # 评估因素取值
                Sqlserver_PO.setFieldComment(dboTable, 'assessName', '评估因素名称')
                Sqlserver_PO.setFieldComment(dboTable, 'assessRule', '取值规则')

                # # 健康干预_已患疾病单病
                Sqlserver_PO.setFieldComment(dboTable, 'ruleCode', '规则编码')
                Sqlserver_PO.setFieldComment(dboTable, 'diseaseCode', '疾病编码')
                Sqlserver_PO.setFieldComment(dboTable, 'diseaseCodeDesc', '疾病编码描述')
                #
                # # 健康干预_已患疾病组合（包含单病）
                Sqlserver_PO.setFieldComment(dboTable, 'assessCode', '评估因素编码')
                Sqlserver_PO.setFieldComment(dboTable, 'assessDesc', '评估因素描述')
                Sqlserver_PO.setFieldComment(dboTable, 'priority', '优先级')
                # 健康干预
                Sqlserver_PO.setFieldComment(dboTable, 'hitQty', '命中次数')


            # 判断导入的表是否已有主键，没有则自动生成id自增主键
            isExistPrimaryKey = Sqlserver_PO.getPrimaryKey(dboTable)
            if isExistPrimaryKey == None:
                l_ = Sqlserver_PO.select("select name from sys.columns where object_id = OBJECT_ID('%s') " % (dboTable))
                for i in l_:
                    # 删除id字段（普通字段）
                    if i['name'] == 'id' or i['name'] == 'ID':
                        Sqlserver_PO.execute("ALTER TABLE %s DROP COLUMN id" % (dboTable))
                        break
                # 新增id自增主键（如果表中已存在id，则无法新增，所以要先删除id）
                Sqlserver_PO.execute("ALTER TABLE %s ADD id INT NOT NULL IDENTITY(1,1) primary key (id)" % (dboTable))

            # 添加表注释
            Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % ('(测试用)' + sheetName, dboTable))  # sheetName=注释，dboTable=表名
            # Color_PO.outColor([{"36": "[OK] => " + sheetName + "（" + dboTable + "）全量数据导入成功。"}, ])
            return 1
        except:
            return 0

    def importIncremental(self, sheetName):

        # 增量导入

        # 中文转拼音
        dbTable = Char_PO.chinese2pinyin(sheetName)
        dbTable = "a_" + dbTable

        # 获取id最大值
        max = Sqlserver_PO.getPrimaryKeyMaxValue(dbTable)
        # print(max['id'])

        # 增量导入
        Sqlserver_PO.xlsx2dbAppendById(Configparser_PO.FILE("case"), dbTable, max['id'], sheetName)

        # print("[ok] 表'%s(%s)'创建成功! " % (dbTable, sheetName))
        Color_PO.outColor([{"36": "[OK] => " + sheetName + "（" + dbTable + "）增量导入成功。"}, ])


    def genIdcard(self, sheetName):

        # 生成身份证(评估疾病表)

        # 中文转拼音
        dboTable = Char_PO.chinese2pinyin(sheetName)
        dboTable = "a_" + dboTable
        # print(dboTable)

        l_d_ = Sqlserver_PO.select("select idcard from %s " % (dboTable))
        # print(l_d_)  # [{'idcard': '310101202308070001'}, {'idcard': '310101202308070002'},
        # sys.exit(0)
        for i in range(len(l_d_)):
            self._genIdcard(dboTable, str(l_d_[i]['idcard']))

    def _genIdcard(self, varTable, varIdcard):

        # 生成单个疾病身份证
        # 对三张表进行先删除后插入操作

        l_d_ = Sqlserver_PO.select(
            "select diseaseName,diseaseCode from %s where [idcard]='%s'" % (varTable, str(varIdcard)))
        # print(l_d_) # [{'diseaseName': '高血压', 'diseaseCode': 'JB001', 'sql1': "DELETE from [dbo].[HRPERSONBASICINFO] WHERE [ARCHIVENUM] ='310101202308070020';...
        diseaseName = l_d_[0]['diseaseName']  # 高血压
        diseaseCode = l_d_[0]['diseaseCode']  # JB001

        # 1.1 删除, HRPERSONBASICINFO(基本信息表)
        Sqlserver_PO.execute("delete from HRPERSONBASICINFO where ARCHIVENUM = '%s'" % (varIdcard))
        # 1.2 插入, HRPERSONBASICINFO(基本信息表)
        Sqlserver_PO.execute('set identity_insert HRPERSONBASICINFO on')
        r = Sqlserver_PO.select('select max(ID) as qty from HRPERSONBASICINFO')
        a = r[0]['qty'] + 1
        Sqlserver_PO.execute("insert into HRPERSONBASICINFO(ARCHIVENUM,NAME,sex,IDCARD,CREATETIME,ID,ISGOVERNANCE) "
                             "values ('%s', '%s', '1', '%s','%s', %s, '0')"
                             % (varIdcard, Data_PO.getChineseName(), varIdcard, time.strftime("%Y-%m-%d %H:%M:%S.000"),
                                str(a)))
        Sqlserver_PO.execute('set identity_insert HRPERSONBASICINFO off')
        Color_PO.outColor(
            [{"35": "基本信息表 => select * from HRPERSONBASICINFO where ARCHIVENUM = '" + str(varIdcard) + "'"}])

        # 2.1 删除, QYYH(1+1+1签约信息表)
        Sqlserver_PO.execute("delete from QYYH where SFZH = '%s'" % (varIdcard))

        # 2.2 插入, QYYH(1+1+1签约信息表)
        Sqlserver_PO.execute('set identity_insert QYYH on')
        r = Sqlserver_PO.select('select max(ID) as qty from QYYH')
        a = r[0]['qty'] + 1
        Sqlserver_PO.execute(
            "insert into QYYH(CZRYBM, CZRYXM, JMXM, SJHM, SFZH, JJDZ, ARCHIVEUNITCODE, ARCHIVEUNITNAME, "
            "DISTRICTORGCODE, DISTRICTORGNAME, TERTIARYORGCODE, TERTIARYORGNAME, SIGNSTATUS, SIGNDATE, ID, "
            "CATEGORY_CODE, CATEGORY_NAME, SEX_CODE, SEX_NAME) "
            "values ('%s', '%s','%s', '13817261777', '%s', '上海浦东100号', '0000001', '彭浦新村街道社区健康管理中心', "
            "'310118000000', '青浦区', '12345', '上海人民医院', 1, '2020-03-23', %s, '4', N'老年人', '2', N'女')"
            % (diseaseCode, diseaseName, Data_PO.getChineseName(), varIdcard, a))
        Sqlserver_PO.execute('set identity_insert QYYH off')
        Color_PO.outColor([{"35": "签约信息表 => select * from QYYH where SFZH = '" + str(varIdcard) + "'"}])

        # 3.1 删除, TB_EMPI_INDEX_ROOT(患者主索引表)
        Sqlserver_PO.execute("delete from TB_EMPI_INDEX_ROOT where IDCARDNO = '%s'" % (varIdcard))
        # 3.2 插入, TB_EMPI_INDEX_ROOT(患者主索引表)
        Sqlserver_PO.execute("insert into TB_EMPI_INDEX_ROOT(GUID, NAME, IDCARDNO) values('%s', '%s', '%s')" % (
        diseaseCode, Data_PO.getChineseName(), varIdcard))
        Color_PO.outColor(
            [{"35": "患者主索引表 => select * from TB_EMPI_INDEX_ROOT where IDCARDNO = '" + str(varIdcard) + "'"}])

        Color_PO.outColor([{"36": "[OK] => " + diseaseName + "（" + varIdcard + "）创建成功。\n"}])

    def getDiseaseIdcard(self):

        # 获取疾病身份证中对应疾病的身份证号码

        l_d_diseaseCode_idcard = Sqlserver_PO.select("select diseaseCode, idcard from %s" % (self.jbsfz))
        # print(l_d_diseaseCode_idcard)  # [{'diseaseCode': 'YH_JB001', 'idcard': 310101202308070001}, {'diseaseCode': 'YH_JB002', 'idcard': 310101202308070002}, ...]
        return l_d_diseaseCode_idcard

    def verifyIdcard(self, varIdcard):

        # 检查患者主索引表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from TB_EMPI_INDEX_ROOT where IDCARDNO='%s'" % (varIdcard))
        # print(l_d_qty)  # [{'qty': 1}]
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            name = Data_PO.getChineseName()
            Sqlserver_PO.execute("INSERT INTO [TB_EMPI_INDEX_ROOT] ([GUID], [NAME], [SEXCODE], [SEXVALUE], [DATEOFBIRTH], [IDCARDNO]) VALUES ('" + str(guid) + "', N'" + str(name) + "', '2', '女', '1940-05-11', '" + str(varIdcard) + "')")

        # 检查基本信息表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from HRPERSONBASICINFO where IDCARD='%s'" % (varIdcard))
        if l_d_qty[0]['qty'] == 0:
            Sqlserver_PO.execute("INSERT INTO [dbo].[HRPERSONBASICINFO] ([ARCHIVENUM], [NAME], [SEX], [DATEOFBIRTH], [IDCARD], [WORKUNIT], [PHONE], [CONTACTSNAME], [CONTACTSPHONE], [RESIDENCETYPE], [NATIONCODE], [BLOODTYPE], [RHBLOODTYPE], [DEGREE], [OCCUPATION], [MARITALSTATUS], [HEREDITYHISTORYFLAG], [HEREDITYHISTORYCODE], [ENVIRONMENTKITCHENAERATION], [ENVIRONMENTFUELTYPE], [ENVIRONMENTWATER], [ENVIRONMENTTOILET], [ENVIRONMENTCORRAL], [DATASOURCES], [CREATEID], [CREATENAME], [CREATETIME], [UPDATEID], [UPDATENAME], [UPDATETIME], [STATUS], [ISDELETED], [VERSION], [WORKSTATUS], [TELEPHONE], [OCCUPATIONALDISEASESFLAG], [OCCUPATIONALDISEASESWORKTYPE], [OCCUPATIONALDISEASESWORKINGYEARS], [DUSTNAME], [DUSTFLAG], [RADIOACTIVEMATERIALNAME], [RADIOACTIVEMATERIALFLAG], [CHEMICALMATERIALNAME], [CHEMICALMATERIALFLAG], [OTHERNAME], [OTHERFLAG], [PHYSICSMATERIALNAME], [PHYSICSMATERIALFLAG], [DOWNLOADSTATUS], [NONUMBERPROVIDED], [YLZFMC], [PERSONID], [MEDICAL_PAYMENTCODE], [KALEIDOSCOPE], [ISGOVERNANCE]) VALUES ('" + str(varIdcard) + "', '高血压已患', '2', '1959-03-28 00:00:00.000', '" + str(varIdcard) + "', NULL, '13585543856', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2022-11-14 16:49:32.357', NULL, NULL, '2020-02-19 00:00:00.000', NULL, NULL, NULL, NULL, '13585543856', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,'0')")

        # 检查签约信息表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from QYYH where SFZH='%s'" % (varIdcard))
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            Sqlserver_PO.execute("INSERT INTO [dbo].[QYYH] ([CZRYBM], [CZRYXM], [JMXM], [SJHM], [SFZH], [JJDZ], [SFJD], [SIGNORGID], [ARCHIVEUNITCODE], [ARCHIVEUNITNAME], [DISTRICTORGCODE], [DISTRICTORGNAME], [TERTIARYORGCODE], [TERTIARYORGNAME], [PRESENTADDRDIVISIONCODE], [PRESENTADDRPROVCODE], [PRESENTADDRPROVVALUE], [PRESENTADDRCITYCODE], [PRESENTADDRCITYVALUE], [PRESENTADDRDISTCODE], [PRESENTADDDISTVALUE], [PRESENTADDRTOWNSHIPCODE], [PRESENTADDRTOWNSHIPVALUE], [PRESENTADDRNEIGHBORHOODCODE], [PRESENTADDRNEIGHBORHOODVALUE], [SIGNSTATUS], [SIGNDATE],[CATEGORY_CODE], [CATEGORY_NAME], [SEX_CODE], [SEX_NAME], [LAST_SERVICE_DATE], [ASSISTANT_DOC_ID], [ASSISTANT_DOC_NAME], [HEALTH_MANAGER_ID], [HEALTH_MANAGER_NAME], [ASSISTANT_DOC_PHONE], [HEALTH_MANAGER_PHONE]) VALUES ('" + str(guid) + "', N'姚皎情', N'肝癌高危', NULL, '" + str(varIdcard) + "', N'平安街道16号', NULL, NULL, '0000001', '静安精神病院', '310118000000', '青浦区', '12345', '上海人民医院', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2020-06-01', 166, '4', N'1',N'男', NULL, NULL, NULL, NULL, NULL, NULL, NULL)")



    def getHospital(self):
        # 1，获取医院信息表字典（机构编码：机构名）
        d_hospital = {}
        l_ = Sqlserver_PO2.select("select ORG_CODE,ORG_NAME from SYS_hospital")
        for d in l_:
            d_hospital[d['ORG_CODE']] = d['ORG_NAME']
        # print(d_hospital)  # {'0000001': '静安精神病院', 'csdm': '彭浦新村街道社区健康管理中心', ...
        return d_hospital


    def getUserInfo(self):

        # 2，获取当前用户信息
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

    # 4，随机获取人群分类
    def getCategoryList(self, l_category):

        # getCategoryList(['0-6岁儿童', '学生（7-17岁）', '普通人群', '老年人', '未分类', '孕妇', '产妇'])

        d_category = dict(enumerate(l_category, start=1))
        return (d_category)  # {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}

        # print(list(d_category.keys()))  # [1, 2, 3, 4, 5, 6, 7]
        # randomCategoryKey = random.sample(list(d_category.keys()), 1)[0]
        # print(randomCategoryKey, d_category[randomCategoryKey])   # 随机获取字典的key, 如：("2", d_category[2])

    def getIdcardByCategory (self, varCategory):

        # 通过人群分类生成身份证
        # print(d_category)  # {1: '0-6岁儿童', 2: '学生（7-17岁）', 3: '普通人群', 4: '老年人', 5: '未分类', 6: '孕妇', 7: '产妇'}
        # self.getIdcardByCategory(4)


        import random
        # d_category = self.getCategory()
        if varCategory == 1:
            birthyear = "2023"
            birthmonth = "01"
            birthday = "01"
        elif varCategory == 2:
            birthyear = "2016"
            birthmonth = "02"
            birthday = "02"
        elif varCategory == 3:
            birthyear = "1990"
            birthmonth = "03"
            birthday = "03"
        elif varCategory == 4:
            birthyear = "1950"
            birthmonth = "04"
            birthday = "04"
        elif varCategory == 5:
            birthyear = "2016"
            birthmonth = "05"
            birthday = "05"
        elif varCategory == 6:
            birthyear = "1990"
            birthmonth = "06"
            birthday = "06"
        elif varCategory == 7:
            birthyear = "1990"
            birthmonth = "07"
            birthday = "07"
        # 预设地区:
        codelist = ["110101", "110102", "110105", "110106", "110107", "420117", "420200", "420202", "420203", "420204",
                    "420205", "420222"]  # 随便设置了几个地区，基本都是湖北和北京的；
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
        return (result_id)

