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

import datetime

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



class ChcRulePO():

    def __init__(self, sheetName=''):

        self.TOKEN = self.getToken(Configparser_PO.USER("user"), Configparser_PO.USER("password"))
        self.dbTable = Char_PO.chinese2pinyin(sheetName)
        self.dbTable = "a_" + self.dbTable
        self.sheetName = sheetName

        # # 读取疾病身份证对应的表(a_jibingshenfenzheng)
        self.jbsfz = "a_" + Char_PO.chinese2pinyin(Configparser_PO.FILE("jbsfz"))
        # print(self.jbsfz)
        # 读取测试规则对应的表(a_ceshiguize)
        self.csgz = "a_" + Char_PO.chinese2pinyin(Configparser_PO.FILE("csgz"))
        # print(self.csgz)

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

    def crtRuleList(self):

        # 创建规则名列表

        dboTable = "a_ruleList"

        # 删除表
        Sqlserver_PO.execute("drop table if exists " + dboTable)

        # 创建表
        Sqlserver_PO.crtTable(dboTable, '''
                ruleName VARCHAR(40) NOT NULL,
                ruleNameTbl VARCHAR(40) NOT NULL''')

        # 添加字段注释
        Sqlserver_PO.setFieldComment(dboTable, 'ruleName', '规则名')
        Sqlserver_PO.setFieldComment(dboTable, 'ruleNameTbl', '规则名表名')

        # 添加表注释
        Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % ('(测试用)规则名列表' , dboTable))  # sheetName=注释，dboTable=表名

        Color_PO.outColor([{"36": "[OK] => " + "（" + dboTable + "）创建成功。"}, ])

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
            print(Configparser_PO.FILE("case"))
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
                Sqlserver_PO.execute("ALTER table %s alter column step varchar(-1)" % (dboTable))
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

    def i_rerunExecuteRule(self, varId):

        # 重新评估

        command = "curl -X GET \"" + Configparser_PO.HTTP("url") + ":8011/server/tAssessInfo/rerunExecuteRule/" + str(
            varId) + "\" -H \"accept: */*\" -H \"Content-Type: application/json\" -H \"Authorization:" + str(
            self.TOKEN) + "\""
        if Configparser_PO.SWITCH("interface") == "on":
            Color_PO.consoleColor2({"34": command})
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        sleep(2)
        l_msg = [{'name': '重新评估', 'value': "[ERROR => 重新评估(i_rerunExecuteRule) => " + str(str_r) + "]"}]

        if 'code' in d_r:
            if d_r['code'] != 200:
                if Configparser_PO.SWITCH("interface") == "on":
                    Color_PO.consoleColor2({"31": str_r})
                self.log = self.log + "\n" + str_r
                return (l_msg)
            else:
                if Configparser_PO.SWITCH("interface") == "on":
                    Color_PO.consoleColor2({"34": d_r})
                return None
        else:
            if Configparser_PO.SWITCH("interface") == "on":
                Color_PO.consoleColor2({"31": str_r})
            self.log = self.log + "\n" + str_r
            # 如：{"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return (l_msg)

    def i_startAssess2(self, varIdcard):

        '''
        新增评估
        :param varIdcard:
        :param token:
        :return:
        '''

        self.verifyIdcard(varIdcard)

        l_d_ = Sqlserver_PO.select("select ARCHIVEUNITCODE,CATEGORY_CODE from QYYH where SFZH='%s'" % (varIdcard))

        command = "curl -X POST \"" + Configparser_PO.HTTP("url") + ":8014/tAssessInfo/startAssess\" " \
                                                                    "-H \"Request-Origion:SwaggerBootstrapUi\" -H \"accept:*/*\" -H \"Authorization:" + self.TOKEN + "\" " + \
                  "-H \"Content-Type:application/json\" " \
                  "-d \"{\\\"assessDocName\\\":\\\"\\\",\\\"assessThirdNo\\\":\\\"\\\", " \
                  "\\\"categoryCode\\\":\\\"" + str(l_d_[0]['CATEGORY_CODE']) + "\\\",\\\"idCard\\\":\\\"" + str(
            varIdcard) + "\\\",\\\"orgCode\\\":\\\"" + str(
            l_d_[0]['ARCHIVEUNITCODE']) + "\\\",\\\"assessDocId\\\":" + str(0) + "}\""

        if Configparser_PO.SWITCH("interface") == "on":
            Color_PO.outColor([{"34": command}])

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        sleep(1)

        if Configparser_PO.SWITCH("interface") == "on":
            Color_PO.outColor([{"34": str_r}])

        if 'code' in d_r:
            if d_r['code'] != 200:
                if Configparser_PO.SWITCH("log") == "on":
                    Color_PO.outColor([{"31": str_r}])
                # self.log = self.log + "\n" + str_r
                return ([{'name': '新增评估', 'value': "[ERROR => 新增评估(i_startAssess) => " + str(str_r) + "]"}])
            else:
                return d_r['data']
                # if Configparser_PO.SWITCH("log") == "on":
                #     Color_PO.consoleColor("31", "33", "新增评估(i_startAssess) =>  => " + str_r, "")
                # return ([{'name':'新增评估', 'value': 200}])
        else:
            if Configparser_PO.SWITCH("log") == "on":
                Color_PO.outColor([{"31": str_r}])
            # self.log = self.log + "\n" + str_r
            # 如：{"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return ([{'name': '新增评估', 'value': "[ERROR => 新增评估(i_startAssess) => " + str(str_r) + "]"}])

    def i_startAssess(self, varIdcard):

        '''
        新增评估
        :param varIdcard:
        :param token:
        :return:
        '''

        self.verifyIdcard(varIdcard)

        command = "curl -X POST \"" + Configparser_PO.HTTP("url") + ":8014/tAssessInfo/startAssess\" -H \"token:" + \
                  self.TOKEN + "\" -H \"Request-Origion:SwaggerBootstrapUi\" -H \"accept:*/*\" -H \"Authorization:\" " \
                               "-H \"Content-Type:application/json\" -d \"{\\\"categoryCode\\\":\\\"\\\",\\\"idCard\\\":\\\"" + str(
            varIdcard) + "\\\",\\\"orgCode\\\":\\\"\\\"}\""

        if Configparser_PO.SWITCH("interface") == "on":
            Color_PO.consoleColor2({"34": command})

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        sleep(2)
        l_msg = [{'name': '新增评估', 'value': "[ERROR => 新增评估(i_startAssess) => " + str(str_r) + "]"}]

        if 'code' in d_r:
            if d_r['code'] != 200:
                if Configparser_PO.SWITCH("interface") == "on":
                    Color_PO.consoleColor2({"31": str_r})
                self.log = self.log + "\n" + str_r
                return (l_msg)
            else:
                if Configparser_PO.SWITCH("interface") == "on":
                    Color_PO.consoleColor2({"34": str_r})
                return None
                # return ([{'name':'新增评估', 'value': 200}])
        else:
            if Configparser_PO.SWITCH("interface") == "on":
                Color_PO.consoleColor2({"31": str_r})
            self.log = self.log + "\n" + str_r
            # 如：{"timestamp":"2023-08-12T20:56:45.715+08:00","status":404,"error":"Not Found","path":"/qyyh/addAssess/310101202308070001"}
            return (l_msg)



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
        d_['家庭医生'] = l_[0]['NAME']
        # print("家庭医生 => ", varNAME)  # 小茄子

        d_['家庭医生的工号'] = l_[0]['THIRD_NO']
        # print("家庭医生的工号 => ", varTHIRD_NO)  # 1231231

        d_['机构编号'] = l_[0]['ORG_CODE']
        # print("机构编号 => ", varORG_CODE)  # 0000001

        l_ = Sqlserver_PO2.select("select ORG_NAME from SYS_hospital where org_code='%s'" % (l_[0]['ORG_CODE']))
        d_['机构名称'] = l_[0]['ORG_NAME']
        # print("机构名称 => ", varORG_NAME)  # 静安精神病院

        return d_





    def getRuleList(self):

        d_ = {}
        l_d_ = Sqlserver_PO.select("select * from a_ruleList")
        # print(l_d_)  # [{'ruleName': '评估因素取值', 'ruleNameTbl': 'a_jibingquzhipanduan'},...
        for d in l_d_:
            d_[d['ruleName']] = d['ruleNameTbl']
        # print(d_)
        return d_


    def runId(self, l_dbId):

        # 按id执行

        if isinstance(l_dbId, list):
            for i in range(len(l_dbId)):
                self.run11(l_dbId[i])

    def runIdArea(self, l_dbId):

        # 按id区间执行

        if isinstance(l_dbId, list):
            if len(l_dbId) == 2:
                for i in range(l_dbId[0], l_dbId[1]):
                    self.run11(i)

    def runRule(self, l_dbRule):

        # 按rule规则执行

        if len(l_dbRule) == 1:
            l_dbRule.append('')
        elif len(l_dbRule) > 1:
            ...
        else:
            sys.exit(0)

        t_dbRule = tuple(l_dbRule)
        l_d_id = Sqlserver_PO.select("select id from %s where [rule] in %s" % (self.dbTable, t_dbRule))
        # print(l_d_id)  # [{'id': 2}, {'id': 3}]
        for i in range(len(l_d_id)):
            self.run11(l_d_id[i]['id'])

    def runResult(self, varResult):

        # 按result执行
        # r.runResult("error")  # 执行result为error的规则
        # r.runResult("all")  # 执行所有的规则(谨慎)

        if varResult == "all":
            l_d_id = Sqlserver_PO.select("select id from %s" % (self.dbTable))
            for i in range(len(l_d_id)):
                self.run11(l_d_id[i]['id'])
        elif varResult != "ok":
            l_d_id = Sqlserver_PO.select("select id from %s where result <> 'ok'" % (self.dbTable))
            for i in range(len(l_d_id)):
                self.run11(l_d_id[i]['id'])

    def runDate(self, varDate=''):

        # 按照时间执行
        # 如果updateDate不是2024-07-19，就执行
        # r.runDate("2024-07-19")

        if  varDate == '':
            varDate = Time_PO.getDateByMinus()
        l = Sqlserver_PO.select("select id, updateDate from %s" % (self.dbTable))
        for i in range(len(l)):
            if str(varDate) != str(l[i]['updateDate']):
                self.run11(l[i]['id'])

    def runDateAgo(self, varN):

        # 执行N天以前的规则
        beforeDate = Time_PO.getDateByMinusPeriod(varN)
        # print(beforeDate)  # 2024-07-16
        l = Sqlserver_PO.select("select id, updateDate from %s" % (self.dbTable))
        for i in range(len(l)):
            if beforeDate > l[i]['updateDate']:
                self.run11(l[i]['id'])

    def runDateAgoResult(self, varN, varResult):

        # r.runDateAgoResult(-3, 'error')
        # 执行几天以前且状态是error的规则
        beforeDate = Time_PO.getDateByMinusPeriod(varN)
        # print(beforeDate)  # 2024-07-16
        l = Sqlserver_PO.select("select id, result, updateDate from %s" % (self.dbTable))
        for i in range(len(l)):
            if beforeDate > l[i]['updateDate'] and varResult == l[i]['result']:
                self.run11(l[i]['id'])



    def getSql(self):

        # 获取sql语句

        # todo 1
        # print(str(self.sheetName) + " => " + str(self.dbId) + "(" + self.rule + ")" + " => " + self.tester)
        try:
            Color_PO.consoleColor2({"35": str(self.sheetName) + " => " + str(self.dbId) + "(" + self.rule + ")" + " => " + self.tester})
        except:
            print("error, rule或tester不能为空！")
            sys.exit(0)
        l_d_ = Sqlserver_PO.select("select sql from %s where [rule]='%s'" % (self.csgz, self.rule))
        # print(self.csgz, self.rule)
        # print("l_d_", l_d_)
        l_sql = []
        for i in range(len(l_d_)):
            if os.name == "posix":
                l_sql.append(l_d_[i]['sql'])
            else:
                l_sql.append(l_d_[i]['sql'].encode('latin1').decode('GB2312'))
        # print("l_sql", l_sql)
        return l_sql

    def assert1(self, varResult, varExpect):

        if varResult in self.d_param:
            # 有result
            if str(self.d_param[varResult]) == varExpect:
                self.assertAssess(self.d_param[varResult])
            else:
                self.assertAssess('')
        else:
            # 无result
            if varResult not in self.d_param:
                if varResult != varExpect:
                    self.assertAssess([])
                    # self.assertAssess(self.d_param[varResult])
                else:
                    self.assertAssess('')


    def runSqls(self, varSql):

        # 执行sql

        if '--' in varSql:
            ...
        elif 'self.i_startAssess2' in varSql:
            self.ASSESS_ID = eval(varSql)
        # elif 'self.assert1' in varSql:
        #     self.log = self.log + "\n" + varSql
        #     eval(varSql)
        else:
            varPrefix = varSql.split(" ")[0]
            varPrefix = varPrefix.lower()
            # S4 处理 血脂异常 语句
            if "{'血脂异常'" in varSql:
                varSql1 = varSql.replace("{assessValue}", self.getRandomAssessValuebyName('血脂异常'))
                d_varSql = dict(eval(varSql1))
                # print(d_varSql) # {'血脂异常': "UPDATE TB_DC_EXAMINATION_INFO set TRIGLYCERIDE=2.3 WHERE EMPIGUID='65209815'"}
                # print(self.d_param)
                if '血脂异常' in self.d_param:
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"33": str(d_varSql['血脂异常'])}])
                    self.log = self.log + "\n" + ", " + str(d_varSql['血脂异常'])
                    command = 'Sqlserver_PO.execute("' + str(d_varSql['血脂异常']) + '")'
                    eval(command)
            elif varPrefix == 'select':
                # print(555,varSql)
                if '{diseaseCode}' in varSql:
                    l_diseaseCode = self.diseaseCode.split(",")
                    # print(4444,l_diseaseCode)
                    if len(l_diseaseCode) > 1:
                        d_tmp = {}
                        for i in l_diseaseCode:
                            varSql1 = varSql.replace("{diseaseCode}", i)
                            # print(varSql1)
                            if Configparser_PO.SWITCH("log") == "on":
                                Color_PO.outColor([{"33": varSql1}])
                            self.log = self.log + "\n" + ", " + varSql1
                            command = 'Sqlserver_PO.select("' + varSql1 + '")'
                            l_d_ = eval(command)
                            d_tmp.update(l_d_[0])
                            # print(d_tmp)
                            l_d_ = [d_tmp]
                elif '{assessCode}' in varSql:
                    l_assessCode = self.assessCode.split(",")
                    # print(666,l_assessCode)
                    if len(l_assessCode) > 1:
                        d_tmp = {}
                        for i in l_assessCode:
                            varSql1 = varSql.replace("{assessCode}", i)
                            # print(varSql1)
                            if Configparser_PO.SWITCH("log") == "on":
                                Color_PO.outColor([{"33": varSql1}])
                            self.log = self.log + "\n" + ", " + varSql1
                            command = 'Sqlserver_PO.select("' + varSql1 + '")'
                            l_d_ = eval(command)
                            d_tmp.update(l_d_[0])
                        # print(d_tmp)
                        l_d_ = [d_tmp]
                elif 'as result' in varSql:
                    command = 'Sqlserver_PO.select("' + varSql + '")'
                    l_d_ = eval(command)
                    # print(command, l_d_)
                    d_tmp = {}
                    l_1 = []
                    if l_d_ == []:
                        d_tmp['result'] = None
                        l_1.append(d_tmp)
                        return l_1
                else:
                    command = 'Sqlserver_PO.select("' + varSql + '")'
                    l_d_ = eval(command)
                return l_d_
            elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete':
                if '{prefixICD}' in varSql:
                    # print(self.d_param)  # {'prefixICD': {'心律失常': 'I45'}, 'assessValue': {'胺碘酮服药史': 'XC01BD'}}
                    for k, v in self.d_param['prefixICD'].items():
                        varSql1 = varSql.replace("{prefixICD}", v)
                        # print(varSql1)
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"33": varSql1}])
                        self.log = self.log + "\n" + ", " + varSql1
                        command = 'Sqlserver_PO.execute("' + varSql1 + '")'
                        eval(command)
                elif '{assessValue}' in varSql:
                    for k, v in self.d_param['assessValue'].items():
                        # if "血脂异常" != k:
                        varSql1 = varSql.replace("{assessValue}", v)
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"33": varSql1}])
                        self.log = self.log + "\n" + ", " + varSql1
                        command = 'Sqlserver_PO.execute("' + varSql1 + '")'
                        eval(command)
                else:
                    command = 'Sqlserver_PO.execute("' + varSql + '")'
                    eval(command)
            else:
                return None

    # def runSql11(self, varSql):
    #
    #     # 执行sql
    #
    #     if 'self.i_startAssess2' in varSql:
    #         self.ASSESS_ID = eval(varSql)
    #         l_d_ASSESS_ID = [{'ASSESS_ID': self.ASSESS_ID}]
    #         return l_d_ASSESS_ID
    #     else:
    #         varPrefix = varSql.split(" ")[0]
    #         varPrefix = varPrefix.lower()
    #         if varPrefix == 'select':
    #             command = 'Sqlserver_PO.select("' + varSql + '")'
    #             l_d_ = eval(command)
    #             # sleep(1)
    #             return l_d_
    #         elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete':
    #             command = 'Sqlserver_PO.execute("' + varSql + '")'
    #             l_d_ = eval(command)
    #             # sleep(1)
    #             return l_d_
    #         else:
    #             return None

    # def runStep(self, varId):
    #
    #     print(self.sheetName + " => " + str(varId))
    #     # Color_PO.outColor([{"35": self.sheetName + " => " + str(varId)}])
    #
    #     self.log = ""
    #     count = 1
    #     d_allSort = {}
    #     d_error = {}
    #
    #     # 获取rule步骤
    #     l_d_ = Sqlserver_PO.select("select [rule],tester from %s where id = '%s'" % (self.dbTable, varId))
    #     l_rule = l_d_[0]['rule'].split("\n")
    #     # print(l_rule)  # ["update TB_PREGNANT_MAIN_INFO set MCYJ='2024-08-06' where ZJHM = '31010520161202008X'", "self.i_startAssess2('31010520161202008X','6','0000001')", 'select LMP from T_ASSESS_MATERNAL where ASSESS_ID={ASSESS_ID}']
    #
    #     # # 生成动态临时库，保存变量与值
    #     # self.tmp_db = 'a_temp' + str(Data_PO.getFigures(10))
    #     # if Configparser_PO.SWITCH("log") == "on":
    #     #     Color_PO.outColor([{"31": self.tmp_db}])
    #     # Sqlserver_PO.crtTable(self.tmp_db, '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')
    #
    #     self.d_ = {}
    #
    #     for i, v in enumerate(l_rule, start=1):
    #
    #         if "{随机11}" in v:
    #             v = v.replace("{随机11}", Data_PO.getFigures(11))
    #         if "{ASSESS_ID}" in v:
    #             v = v.replace('{ASSESS_ID}', str(self.ASSESS_ID))
    #         if "{昨天日期}" in v:
    #             v = v.replace('{昨天日期}', str(Time_PO.getDateByMinusPeriod(-1)))
    #         if "{YCFID}" in v:
    #             v = v.replace('{YCFID}', str(self.d_['YCFID']))
    #
    #         # v = v.lower()
    #         # print(v)
    #         varPrefix = v.split(" ")[0]
    #         varPrefix = varPrefix.lower()
    #         if varPrefix == 'select':
    #             l_d_ = eval('Sqlserver_PO.select("' + v + '")')
    #             self.log = self.log + str(i) + ", " + str(v) + "\n"
    #             if Configparser_PO.SWITCH("log") == "on":
    #                 # Color_PO.outColor([{"35": v}])
    #                 print(i, v)
    #
    #             if l_d_ == []:
    #                 s_key = v.split("select ")[1].split("from")[0]
    #                 s_key = s_key.strip()
    #                 # print(s_key)
    #                 self.d_[s_key] = ''
    #             else:
    #                 self.d_.update(l_d_[0])
    #             self.log = self.log + str(self.d_) + "\n"
    #             Color_PO.outColor([{"35": self.d_}])
    #
    #             # for k1, v1 in self.selectResult[0].items():
    #             #     Sqlserver_PO.execute("insert into %s(key1,value1) values('%s','%s')" % (self.tmp_db, k1, v1))
    #
    #         elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete':
    #             eval('Sqlserver_PO.execute("' + v + '")')
    #             self.log = self.log + str(i) + ", " + str(v) + "\n"
    #             if Configparser_PO.SWITCH("log") == "on":
    #                 # Color_PO.outColor([{"35": v}])
    #                 print(i, v)
    #         else:
    #             if 'self.i_startAssess2' in v:
    #                 if Configparser_PO.SWITCH("log") == "on":
    #                     # Color_PO.outColor([{"35": v}])
    #                     print(i, v)
    #                 self.ASSESS_ID = eval(v)
    #                 self.log = self.log + str(i) + ", " + str(v) + "\n"
    #                 self.log = self.log + "{ASSESS_ID} = " + str(self.ASSESS_ID) + "\n"
    #                 Color_PO.outColor([{"35": "{ASSESS_ID} = " + str(self.ASSESS_ID)}])
    #             else:
    #                 # 断言select, 判断====
    #                 # print(222, v)
    #                 # print(999, self.d_)
    #                 if "===" in v:
    #                     s_1 = v.split("===")[0]
    #                     s_2 = v.split("===")[1]
    #                     if s_1 in self.d_ and s_2 in self.d_ and self.d_[s_1] != '':
    #                         if self.d_[s_1] == self.d_[s_2]:
    #                             Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, varId))
    #                             Color_PO.consoleColor("31", "36", ("[OK] => " + self.sheetName + " => " + str(varId)).center(100, '-'), "")
    #                         else:
    #                             Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, varId))
    #                             Color_PO.consoleColor("31", "31", ("[ERROR log] => " + self.sheetName + " => " + str(varId)).center(100, '-'), "")
    #                             Color_PO.outColor([{"31": self.log}])
    #                         Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), varId))
    #                         self.log = (self.log).replace("'", "''")
    #                         Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, varId))
    #                         # Sqlserver_PO.execute("drop table %s" % (self.tmp_db))
    #                     else:
    #                         Color_PO.outColor([{"31": "error, 值为空或不存在！"}])


    def run11(self, dbId):

        # 按id执行

        if isinstance(int(dbId), int):
            self.dbId = dbId
        else:
            sys.exit(0)

        self.d_param = {}

        # 获取表字段值
        l_d_rows = Sqlserver_PO.select("select * from %s where id=%s" % (self.dbTable, self.dbId))

        try:
            self.rule = l_d_rows[0]['rule']
        except:
            print("warning, rule不存在！")
            sys.exit(0)

        self.case = l_d_rows[0]['case']

        if l_d_rows[0]['ruleParam'] != None:
            if l_d_rows[0]['ruleParam'] == '':
                self.ruleParam = {}
            else:
                try:
                    self.ruleParam = dict(eval(l_d_rows[0]['ruleParam']))
                except:
                    print("error, ruleparam不是字典形式字符串或不为空！")
                    sys.exit(0)
        else:
            self.ruleParam = {}

        # 规则编码（健康干预_已患疾病单病、健康干预_已患疾病组合）
        if 'ruleCode' in l_d_rows[0].keys():
            self.ruleCode = l_d_rows[0]['ruleCode']
        else:
            self.ruleCode = ""

        # 干预规则（健康干预_已患疾病单病、健康干预_已患疾病组合）
        if 'diseaseCode' in l_d_rows[0].keys():
            self.diseaseCode = l_d_rows[0]['diseaseCode']
        else:
            self.diseaseCode = ""

        # 疾病编码描述（健康干预_已患疾病单病、健康干预_已患疾病组合）
        if 'diseaseCodeDesc' in l_d_rows[0].keys():
            self.diseaseCodeDesc = l_d_rows[0]['diseaseCodeDesc']
        else:
            self.diseaseCodeDesc = ""

        # if 'assessCodeDesc' in l_d_rows[0].keys():
        #     self.assessCodeDesc = l_d_rows[0]['assessCodeDesc']
        # else:
        #     self.assessCodeDesc = ""

        # 评估因素编码（健康干预_已患疾病组合）
        if 'assessCode' in l_d_rows[0].keys():
            self.assessCode = l_d_rows[0]['assessCode']
        else:
            self.assessCode = ""


        # 评估因素描述（健康干预_已患疾病组合）
        d_2 = {}
        if 'assessDesc' in l_d_rows[0].keys():
            if l_d_rows[0]['assessDesc'] == None or l_d_rows[0]['assessDesc'] == "":
                self.assessDesc = ""
            else:
                self.assessDesc = l_d_rows[0]['assessDesc']
                l_assessDesc = self.assessDesc.split(",")
                # print(11,self.assessDesc)
                # print(22,l_assessDesc)
                for i in l_assessDesc:
                    s_assessValue = self.getRandomAssessValuebyName(i)
                    if self.rule == 's4' and i == '血脂异常':
                        self.d_param['血脂异常'] = s_assessValue
                    else:
                        d_2[i] = s_assessValue
                self.d_param['assessValue'] = d_2

        self.tester = l_d_rows[0]['tester']
        self.sql = self.getSql()
        self.log = ""

        if self.rule == 's1':
            # 获取组合与非组合的疾病
            self._s1_noParam()

            if self.case == 'negative':
                if self.ruleParam == {}:
                    # 实例3：反无参
                    diseaseName = random.sample(self.l_combination_s1, 1)[0]
                    self.getPrefixICD(diseaseName)
                    self.testRules()
                    # self.d_param.update(self.testRules())
                    self.assertS1()
                else:
                    # 实例4：反有参  {'prefixICD': {'高血压': 'I10'}}
                    self.haveParam()
            else:
                if self.ruleParam == {}:
                    # 实例1：正无参
                    diseaseName = random.sample(self.l_noCombination_s1, 1)[0]
                    self.getPrefixICD(diseaseName)
                    self.testRules()
                    self.assertS1()
                else:
                    # 实例2：正有参 {'prefixICD': {'高血压': 'G40'}}
                    self.haveParam()

        elif self.rule == 's2' or self.rule == 's3' or self.rule == 's4' or self.rule == 's5':
            if self.case == 'negative':
                if self.ruleParam == {}:
                    # 实例3：反无参
                    self.getErrPrefixICD(self.diseaseCodeDesc)
                    self.testRules()
                    self.assertS1()
                else:
                    # 实例4：反有参 {'VISITTYPECODE':'34','prefixICD':{'慢性肾脏病':'?'}}
                    self.haveParam()
            else:
                if self.ruleParam == {}:
                    # 实例1：正无参
                    self.getPrefixICD(self.diseaseCodeDesc)
                    self.testRules()
                    self.assertS1()
                else:
                    # 实例2：正有参  {'VISITTYPECODE':'34','prefixICD':{'慢性肾脏病':'N11'}}
                    self.haveParam()
        else:
            # 评估因素取值
            # a1,a2,a3,HDL
            if self.case == 'negative':
                if self.ruleParam == {}:
                    # 反无参
                    Color_PO.outColor([{"31": "error, 反向用例ruleParam不能为空！"}])
                    sys.exit(0)
                else:
                    # 反有参
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"35": "self.ruleParam => " + str(self.ruleParam)}])
                    self.testRules()
                    self.assertAssess()
            else:
                if self.ruleParam == {}:
                    # 正无参
                    # self.d_param = self.ruleParam
                    self.testRules()
                else:
                    # 正有参
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"35": '({})self.ruleParam => '.format(sys._getframe().f_lineno) + str(self.ruleParam)}])
                    self.testRules()
                    self.assertAssess()
                    # try:
                    #     if Configparser_PO.SWITCH("log") == "on":
                    #         Color_PO.outColor([{"35": "self.ruleParam => " + str(self.ruleParam)}])
                    #     self.testRules()
                    #     self.assertAssess()
                    # except:
                    #     Color_PO.outColor([{"35": "error,请检查测试规则中评估因素取值是否存在 a1,a2,a3 规则！"}])


    def _s1_noParam(self):

        # 如：高血压
        # 1, 在"健康干预_已患疾病组合"中，获取疾病编码描述(diseaseCodeDesc)为高血压及包含高血压的组合，生成列表l_1
        l_d_ = Sqlserver_PO.select(
            "select diseaseCodeDesc from a_jiankangganyu_yihuanjibingzuhe where diseaseCodeDesc like '%s'" % (
                        '%' + self.diseaseCodeDesc + '%'))
        # print(l_d_)  # [{'diseaseCodeDesc': '高血压'}, {'diseaseCodeDesc': '高血压,糖尿病'},
        l_1 = []
        for d_ in l_d_:
            if ',' in d_['diseaseCodeDesc']:
                l_1.append(d_['diseaseCodeDesc'])

        # 2，对l_1去重，生成self.l_combination_s1
        l_2 = List_PO.deduplication(l_1)
        l_4 = []
        for j in l_2:
            l_3 = j.split(",")
            for k in l_3:
                l_4.append(k)
        self.l_combination_s1 = List_PO.deduplication(l_4)
        # print(555,self.l_combination_s1)

        # 3，遍历疾病取值判断表，过滤掉列表self.l_combination_s1，生成列表l_7。
        l_d_ = Sqlserver_PO.select("select diseaseName from a_jibingquzhipanduan")
        l_6 = []
        for k in l_d_:
            l_6.append(k['diseaseName'])

        self.l_noCombination_s1 = [x for x in l_6 if x not in self.l_combination_s1]

    def haveParam(self):
        self.d_param = self.ruleParam
        if Configparser_PO.SWITCH("log") == "on":
            Color_PO.outColor([{"35": '({})self.d_param  => '.format(sys._getframe().f_lineno) + str(self.d_param)}])

        self.testRules()
        self.assertS1()


    def getVisitTypeCode(self, varSql, varFieldName):

        # 获取疾病取值判断对应的visitTypeCode，并替换VISITTYPECODE
        # self.sql[i] = self.getVisitTypeCode(self.sql[i], 'VISITTYPECODE')

        if self.ruleParam != None:
            if varFieldName in self.ruleParam:
                for k, v in self.ruleParam.items():
                    if '{' + k + '}' in varSql:
                        varSql = varSql.replace('{' + k + '}', self.ruleParam[k])
                        # print(self.ruleParam[k])  # 31
            else:
                for k, v in self.ruleParam.items():
                    if '{' + k + '}' in varSql:
                        varSql = varSql.replace('{' + k + '}', self.ruleParam[k])
                if self.diseaseCodeDesc != None and isinstance(self.diseaseCodeDesc, str):
                    l_d_ = Sqlserver_PO.select(
                        "select visitTypeCode from a_jibingquzhipanduan where diseaseName='%s'" % (
                            self.diseaseCodeDesc))
                    varSql = varSql.replace('{' + varFieldName + '}', str(l_d_[0]['visitTypeCode']))
                    # print(str(l_d_[0]['visitTypeCode']))  # 31
            # print(self.sql[i])
        else:
            tmp = '{' + varFieldName + '}'
            if tmp in varSql:
                if self.diseaseCodeDesc != None and isinstance(self.diseaseCodeDesc, str):
                    l_d_ = Sqlserver_PO.select(
                        "select visitTypeCode from a_jibingquzhipanduan where diseaseName='%s'" % (
                            self.diseaseCodeDesc))
                    # print(l[0]['visitTypeCode'])
                    varSql = varSql.replace('{' + varFieldName + '}', str(l_d_[0]['visitTypeCode']))
                    # print(l_sql[i])
        return varSql

    def getRandomAssessValuebyName(self, assessName):

        # 获取疾病取值判断中 评估名对应的值
        l_d_ = Sqlserver_PO.select("select assessValue from a_jibingquzhipanduan where assessName='%s'" % (assessName))
        print(l_d_)
        l_assessValue = l_d_[0]['assessValue'].split(",")
        return random.sample(l_assessValue, 1)[0]

    def getRandomAssessValuebyErrName(self, assessName):

        # 获取疾病取值判断中 评估名对应的值
        l_d_ = Sqlserver_PO.select("select assessValue from a_jibingquzhipanduan where assessName !='%s'" % (assessName))
        l_assessValue = l_d_[0]['assessValue'].split(",")
        # s_assessValue = random.sample(l_assessValue, 1)[0]
        # self.d_param['assessValue'][assessName] = str(s_assessValue)
        return random.sample(l_assessValue, 1)[0]

    def getPrefixICD(self, diseaseName):

        # 获取疾病取值判断中疾病名(diseaseName)对应随机值。
        self.d_param['prefixICD'] = {}
        # print(self.diseaseCodeDesc)
        l_diseaseCodeDesc = diseaseName.split(",")
        for i in l_diseaseCodeDesc:
            l_d_ = Sqlserver_PO.select("select prefixICD from a_jibingquzhipanduan where diseaseName = '%s'" % (i))
            l_prefixICD = l_d_[0]['prefixICD'].split(",")
            s_prefixICD = random.sample(l_prefixICD, 1)[0]
            self.d_param['prefixICD'][i] = str(s_prefixICD)
        if Configparser_PO.SWITCH("log") == "on":
            Color_PO.outColor([{"35": '({})self.d_param  => '.format(sys._getframe().f_lineno) + str(self.d_param)}])


    def getErrPrefixICD(self, diseaseName):

        # 随机获取疾病取值判断中 非疾病名字对应值。
        self.d_param['prefixICD'] = {}
        # print(self.diseaseCodeDesc)
        l_diseaseCodeDesc = diseaseName.split(",")

        # 获取其他疾病列表
        l_all = []
        l_d_ = Sqlserver_PO.select('select diseaseName from a_jibingquzhipanduan')
        for i in l_d_:
            l_all.append(i['diseaseName'])
        # print(l_all)
        l_all = [x for x in l_all if x not in l_diseaseCodeDesc]
        l_2 = random.sample(l_all, 2)
        # print(l_2)

        for i in l_2:
            l_d_ = Sqlserver_PO.select("select prefixICD from a_jibingquzhipanduan where diseaseName = '%s'" % (i))
            l_prefixICD = l_d_[0]['prefixICD'].split(",")
            s_prefixICD = random.sample(l_prefixICD, 1)[0]
            self.d_param['prefixICD'][i] = str(s_prefixICD)
        if Configparser_PO.SWITCH("log") == "on":
            Color_PO.outColor([{"35": '({})self.d_param  => '.format(sys._getframe().f_lineno) + str(self.d_param)}])


    def testRules(self):

        # 生成动态临时库，保存变量与值
        # todo 3
        self.tmp_db = 'a_temp' + str(Data_PO.getFigures(10))
        if Configparser_PO.SWITCH("log") == "on":
            Color_PO.outColor([{"33": '({})self.tmp_db  => '.format(sys._getframe().f_lineno) + str(self.tmp_db)}])
        Sqlserver_PO.crtTableByCover(self.tmp_db, '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')

        # 获取临时变量
        d_update = {}
        self.ASSESS_ID = ""
        # d_total = {}
        s_random8 = Data_PO.getFigures(8)
        s_random9 = Data_PO.getFigures(9)
        s_random10 = Data_PO.getFigures(10)
        s_random11 = Data_PO.getFigures(11)
        s_random12 = Data_PO.getFigures(12)

        for i in range(len(self.sql)):

            # 格式化sql
            if "{引用随机值8}" in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{引用随机值8}", s_random8)
            if "{引用随机值9}" in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{引用随机值9}", s_random9)
            if "{引用随机值10}" in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{引用随机值10}", s_random10)
            if "{引用随机值11}" in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{引用随机值11}", s_random11)
            if "{引用随机值12}" in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{引用随机值12}", s_random12)
            if "{随机值11}" in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{随机值11}", Data_PO.getFigures(11))
            if '{ruleCode}' in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{ruleCode}", self.ruleCode)
            if '{diseaseCode}' in self.sql[i]:
                l_diseaseCode = self.diseaseCode.split(",")
                if len(l_diseaseCode) == 1:
                    self.sql[i] = self.sql[i].replace("{diseaseCode}", self.diseaseCode)
            if '{assessCode}' in self.sql[i]:
                l_assessCode = self.assessCode.split(",")
                if len(l_assessCode) == 1:
                    self.sql[i] = self.sql[i].replace("{assessCode}", self.assessCode)

            if "{今天往前一年内的日期}" in self.sql[i]:
                if '今天往前一年内的日期' in self.ruleParam:
                    self.sql[i] = self.sql[i].replace('{今天往前一年内的日期}', str(self.ruleParam['今天往前一年内的日期']))
            if "{今天往前一年内的日期1}" in self.sql[i]:
                if '今天往前一年内的日期1' in self.ruleParam:
                    self.sql[i] = self.sql[i].replace('{今天往前一年内的日期1}', str(self.ruleParam['今天往前一年内的日期1']))
            if "{今天往前一年内的日期2}" in self.sql[i]:
                if '今天往前一年内的日期2' in self.ruleParam:
                    self.sql[i] = self.sql[i].replace('{今天往前一年内的日期2}', str(self.ruleParam['今天往前一年内的日期2']))
            if "{今天往前一年内的日期3}" in self.sql[i]:
                if '今天往前一年内的日期3' in self.ruleParam:
                    self.sql[i] = self.sql[i].replace('{今天往前一年内的日期3}', str(self.ruleParam['今天往前一年内的日期3']))
            if "{今天往前一年内的日期4}" in self.sql[i]:
                if '今天往前一年内的日期4' in self.ruleParam:
                    self.sql[i] = self.sql[i].replace('{今天往前一年内的日期4}', str(self.ruleParam['今天往前一年内的日期4']))
            # s1/s2
            if '{VISITTYPECODE}' in self.sql[i]:
                self.sql[i] = self.getVisitTypeCode(self.sql[i], 'VISITTYPECODE')

            # 评估因素取值 - 高密度脂蛋白（HDL）(dm\htn\examination\op\ip)
            if self.ruleParam.get('HDL'):
                self.sql[i] = self.sql[i].replace('{今天往前一年内的日期1}', str(self.ruleParam['HDL']['今天往前一年内的日期1']))\
                    .replace('{今天往前一年内的日期2}', str(self.ruleParam['HDL']['今天往前一年内的日期2']))\
                    .replace('{今天往前一年内的日期3}', str(self.ruleParam['HDL']['今天往前一年内的日期3']))\
                    .replace('{今天往前一年内的日期4}', str(self.ruleParam['HDL']['今天往前一年内的日期4']))\
                    .replace('{今天往前一年内的日期5}', str(self.ruleParam['HDL']['今天往前一年内的日期5']))\
                    .replace('{今天往前一年内的日期6}', str(self.ruleParam['HDL']['今天往前一年内的日期6']))\
                    .replace('{今天往前一年内的日期7}', str(self.ruleParam['HDL']['今天往前一年内的日期7']))\
                    .replace('{今天往前一年内的日期8}', str(self.ruleParam['HDL']['今天往前一年内的日期8']))\
                    .replace('{今天往前一年内的日期9}', str(self.ruleParam['HDL']['今天往前一年内的日期9']))\
                    .replace('{今天往前一年内的日期10}', str(self.ruleParam['HDL']['今天往前一年内的日期10']))



            # 将db转换成字典
            l = Sqlserver_PO.select("select key1, value1 from %s" % (self.tmp_db))
            # print(l) # [{'key1': 'ID', 'value1': '499948'}, {'key1': 'QTY', 'value1': '1'}, {'key1': 'Q2', 'value1': '1'},
            for p in range(len(l)):
                d_update[l[p]['key1']] = l[p]['value1']
                if 'GUID' in d_update:
                    self.sql[i] = str(self.sql[i]).replace("{GUID}", str(d_update['GUID']))
                if 'YCFID' in d_update:
                    self.sql[i] = str(self.sql[i]).replace("{YCFID}", str(d_update['YCFID']))

            if str(self.ASSESS_ID) != "":
                self.sql[i] = str(self.sql[i]).replace('{ASSESS_ID}', str(self.ASSESS_ID))


            # todo 输出sql
            if Configparser_PO.SWITCH("log") == "on":
                if self.rule == 's4':
                    if "{'血脂异常'" in self.sql[i]:
                        if '血脂异常' in self.d_param:
                            print(str(i + 1) + ", " + self.sql[i])
                    else:
                        print(str(i + 1) + ", " + self.sql[i])
                else:
                    print(str(i + 1) + ", " + self.sql[i])


            # 记录步骤日志
            if self.log == "":
                self.log = str(i + 1) + " " + self.sql[i]
            else:
                if self.rule == 's4':
                    if "{'血脂异常'" in self.sql[i]:
                        if '血脂异常' in self.d_param:
                            self.log = self.log + "\n" + str(i + 1) + " " + self.sql[i]
                    else:
                        self.log = self.log + "\n" + str(i + 1) + " " + self.sql[i]
                else:
                    self.log = self.log + "\n" + str(i + 1) + " " + self.sql[i]


            # todo 执行sql
            # sql返回值
            # print("1201", self.sql[i])
            l_d_ = self.runSqls(self.sql[i])

            if 'self.i_startAssess2' in self.sql[i]:
                self.log = self.log + "\n" + "ASSESS_ID = " + str(self.ASSESS_ID)

            if l_d_ != None:
                if isinstance(l_d_, list) and l_d_ != []:
                    if isinstance(l_d_[0], dict):

                        # 将变量存入db
                        for k, v in l_d_[0].items():
                            Sqlserver_PO.execute("insert into %s (key1,value1) values ('%s', '%s')" % (self.tmp_db, str(k), str(v)))

                        # 打印返回值
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"33": l_d_[0]}])  # {'GUID': '65209815'}

                        self.d_param.update(l_d_[0])

        self.log = self.log + "\n" + str(self.d_param)



    def assertS1(self):

        if Configparser_PO.SWITCH("log") == "on":
            Color_PO.outColor([{"35": '({})self.d_param  => '.format(sys._getframe().f_lineno) + str(self.d_param)}])

        if self.case != 'negative':
            # 正向
            if self.d_param[self.ruleCode] == 1:
                Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
                self.log = (self.log).replace("'", "''")
                Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
            else:
                Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, self.dbId))
                print(self.log)
                self.log = (self.log).replace("'", "''")
                Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
                Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (self.dbTable, self.dbId, Time_PO.getDateTimeByDivide(), self.log))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            Sqlserver_PO.execute("drop table %s" % (self.tmp_db))
        elif self.case == 'negative':
            # 反向
            if self.d_param[self.ruleCode] == 0:
                Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
                self.log = (self.log).replace("'", "''")
                Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
            else:
                Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, self.dbId))
                print(self.log)
                self.log = (self.log).replace("'", "''")
                Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
                Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (self.dbTable, self.dbId, Time_PO.getDateTimeByDivide(), self.log))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            Sqlserver_PO.execute("drop table %s" % (self.tmp_db))

    def _assertAssessOk(self):

        Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
        Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
        self.log = (self.log).replace("'", "''")
        Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))

    def _assertAssessErr(self):

        Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
        Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, self.dbId))
        print(self.log)
        self.log = (self.log).replace("'", "''")
        Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
        Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
        Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (self.dbTable, self.dbId, Time_PO.getDateTimeByDivide(), self.log))
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))

    def _assertAssessOk_HDL(self, info):
        Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + "_" + info + ") => OK]").center(100, '-')), "")
        self.log = (self.log).replace("'", "''")


    def _assertAssessErr_HDL(self,info):
        Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
        print(self.log)
        self.log = (self.log).replace("'", "''")
        Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + "_" + info + ") => ERROR]").center(100, '-')), "")

    def _result_HDL(self, d_date_value):
        # 获取最大日期的值
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))
        # print(d_date_value)
        l_ = list(d_date_value.keys())
        dt_tmpDate = datetime.datetime(2024, 1, 1, 0, 0)
        for dt_date in l_:
            if dt_tmpDate < dt_date:
                dt_tmpDate = dt_date
        # print(dt_tmpDate)
        return(d_date_value[dt_tmpDate])


    def assertAssess(self):

        if Configparser_PO.SWITCH("log") == "on":
            Color_PO.outColor([{"35": '({})self.d_param  => '.format(sys._getframe().f_lineno) + str(self.d_param)}])

        if self.case != 'negative':
            # 正向
            if self.ruleParam.get('HDL'):
                d_ = {}
                if str(int(self.d_param["result1"])) == str(self.ruleParam['HDL']['result1']) \
                        and str(self.d_param["result2"]) == str(self.ruleParam['HDL']['result2']) \
                        and self.d_param["maxvisitdate12"].strftime('%Y-%m-%d') == str(self.ruleParam['HDL']['maxvisitdate12']):
                    Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + "_糖尿病) => OK]").center(100, '-')), "")
                    d_[self.d_param['maxvisitdate12']] = self.d_param['result2']
                else:
                    Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + "_糖尿病) => ERROR]").center(100, '-')), "")
                    sys.exit(0)
                if str(int(self.d_param["result3"])) == str(self.ruleParam['HDL']['result3']) \
                        and str(self.d_param["result4"]) == str(self.ruleParam['HDL']['result4']) \
                        and self.d_param["maxvisitdate34"].strftime('%Y-%m-%d') == str(self.ruleParam['HDL']['maxvisitdate34']):
                    Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(
                        self.rule) + "_高血压) => OK]").center(100, '-')), "")
                    d_[self.d_param['maxvisitdate34']] = self.d_param['result4']
                else:
                    Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(
                        self.rule) + "_高血压) => ERROR]").center(100, '-')), "")
                    sys.exit(0)
                if str(int(self.d_param["result5"])) == str(self.ruleParam['HDL']['result5']) \
                        and str(self.d_param["result6"]) == str(self.ruleParam['HDL']['result6']) \
                        and self.d_param["maxvisitdate56"].strftime('%Y-%m-%d') == str(self.ruleParam['HDL']['maxvisitdate56']):
                    Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(
                        self.rule) + "_体检) => OK]").center(100, '-')), "")
                    d_[self.d_param['maxvisitdate56']] = self.d_param['result6']
                else:
                    Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(
                        self.rule) + "_体检) => ERROR]").center(100, '-')), "")
                    sys.exit(0)
                if str(int(self.d_param["result7"])) == str(self.ruleParam['HDL']['result7']) \
                        and str(self.d_param["result8"]) == str(self.ruleParam['HDL']['result8']) \
                        and self.d_param["maxvisitdate78"].strftime('%Y-%m-%d') == str(self.ruleParam['HDL']['maxvisitdate78']):
                    Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + "_门诊就诊) => OK]").center(100, '-')), "")
                    d_[self.d_param['maxvisitdate78']] = self.d_param['result8']
                else:
                    Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + "_门诊就诊) => ERROR]").center(100, '-')), "")
                    sys.exit(0)

                if str(int(self.d_param["result9"])) == str(self.ruleParam['HDL']['result9']) \
                        and str(self.d_param["result10"]) == str(self.ruleParam['HDL']['result10']) \
                        and self.d_param["maxvisitdate910"].strftime('%Y-%m-%d') == str(self.ruleParam['HDL']['maxvisitdate910']):
                    Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(
                        self.rule) + "_住院) => OK]").center(100, '-')), "")
                    d_[self.d_param['maxvisitdate910']] = self.d_param['result10']
                else:
                    Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(
                        self.rule) + "_住院) => ERROR]").center(100, '-')), "")
                    sys.exit(0)

                valueByMaxDate = self._result_HDL(d_)
                # print(valueByMaxDate)
                print("({})valueByMaxDate =>".format(sys._getframe().f_lineno), valueByMaxDate)

                if str(valueByMaxDate) == self.ruleParam['result']:
                    Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
                    Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
                    self.log = (self.log).replace("'", "''")
                    print("self.log", self.log)
                    Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
                    Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))

                else:
                    Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
                    Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, self.dbId))
                    # print(self.log)
                    self.log = (self.log).replace("'", "''")
                    Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
                    Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
                    # Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (self.dbTable, self.dbId, Time_PO.getDateTimeByDivide(), self.log))
                    Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))

            elif 'result1' in self.d_param:
                if str(self.d_param["result"]) == str(self.ruleParam['result']) and str(self.d_param["result1"]) == str(self.ruleParam['result1']):
                    self._assertAssessOk()
                else:
                    self._assertAssessErr()
            else:
                # print("self.d_param => ", self.d_param)
                if str(self.d_param["result"]) == str(self.ruleParam['result']):
                    self._assertAssessOk()
                else:
                    self._assertAssessErr()


        elif self.case == 'negative':
            # 反向
            if str(self.d_param["result"]) == str(self.ruleParam['result']):
                Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
                self.log = (self.log).replace("'", "''")
                Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
            else:
                Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, self.dbId))
                print(self.log)
                self.log = (self.log).replace("'", "''")
                Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
                Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
                Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (self.dbTable, self.dbId, Time_PO.getDateTimeByDivide(), self.log))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            Sqlserver_PO.execute("drop table %s" % (self.tmp_db))



