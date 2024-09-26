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

    def importFull(self, sheetName):

        # 全量更新表（删除旧表，插入新表）

        # 中文转拼音
        dboTable = Char_PO.chinese2pinyin(sheetName)
        dboTable = "a_" + dboTable
        # print(dboTable)

        # 删除旧表
        Sqlserver_PO.execute("drop table if exists " + dboTable)

        # sheetName导入数据库，并将身份证数字型转字段型
        Sqlserver_PO.xlsx2dbByConverters(Configparser_PO.FILE("case"), dboTable, {"idcard": str}, sheetName)

        # 修改其他规则表的字段类型
        if sheetName == "评估因素取值" :
            # Sqlserver_PO.execute("ALTER TABLE %s alter column id int not null" % (dboTable))  # 设置主id不能为Null
            # Sqlserver_PO.execute("ALTER TABLE %s add PRIMARY KEY (id)" % (dboTable))  # 设置主键（条件是id不能为Null）
            Sqlserver_PO.execute("ALTER table %s alter column result varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            Sqlserver_PO.execute("ALTER table %s alter column step varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            Sqlserver_PO.execute("ALTER table %s alter column updateDate char(11)" % (dboTable))  # 将float改为char类型
            Sqlserver_PO.execute("ALTER table %s alter column updateDate DATE" % (dboTable))  # 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
            # Sqlserver_PO.execute("ALTER TABLE %s ADD var varchar(111)" % (tableName))  # 临时变量
        if sheetName == "健康干预_已患疾病单病" or sheetName== '健康干预_已患疾病组合':
            Sqlserver_PO.execute("ALTER table %s alter column eachResult varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            Sqlserver_PO.execute("ALTER table %s alter column eachStep varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            Sqlserver_PO.execute("ALTER table %s alter column result varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            Sqlserver_PO.execute("ALTER table %s alter column step varchar(8000)" % (dboTable))  # 此列没数据，创建后是float，需转换成char
            Sqlserver_PO.execute("ALTER table %s alter column updateDate char(11)" % (dboTable))  # 将float改为char类型
            Sqlserver_PO.execute("ALTER table %s alter column updateDate DATE" % (dboTable))  # 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
        if sheetName != "测试规则":
            # 判断导入的表是否已有主键，没有主键则自动生成id自增主键
            isExistPrimaryKey = Sqlserver_PO.getPrimaryKey(dboTable)
            if isExistPrimaryKey == None:
                l_ = Sqlserver_PO.select("select name from sys.columns where object_id = OBJECT_ID('%s') " % (dboTable))
                for i in l_:
                    if i['name'] == 'id' or i['name'] == 'ID':
                        Sqlserver_PO.execute("ALTER TABLE %s DROP COLUMN id" % (dboTable))
                        break
                # 新增id自增主键（如果表中已存在id，则无法新增）
                Sqlserver_PO.execute("ALTER TABLE %s ADD id INT NOT NULL IDENTITY(1,1) primary key (id)" % (dboTable))

        # 添加表注释
        Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % ('(测试用)' + sheetName, dboTable))  # sheetName=注释，dboTable=表名

        # print("[ok] 表'%s(%s)'创建成功! " % (dbTable, sheetName))
        Color_PO.outColor([{"36": "[OK] => " + sheetName + "（" + dboTable + "）全量数据导入成功。"}, ])

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
        # print(l_d_) # [{'diseaseName': '高血压', 'diseaseRuleCode': 'JB001', 'sql1': "DELETE from [dbo].[HRPERSONBASICINFO] WHERE [ARCHIVENUM] ='310101202308070020';...
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

        l_d_diseaseRuleCode_idcard = Sqlserver_PO.select("select diseaseRuleCode, idcard from %s" % (self.jbsfz))
        # print(l_d_diseaseRuleCode_idcard)  # [{'diseaseRuleCode': 'YH_JB001', 'idcard': 310101202308070001}, {'diseaseRuleCode': 'YH_JB002', 'idcard': 310101202308070002}, ...]
        return l_d_diseaseRuleCode_idcard

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
        try:
            # Color_PO.consoleColor2({"35": str(self.sheetName) + " => " + str(self.dbId) + "(" + self.rule + ")" + " => " + self.tester})
            print(str(self.sheetName) + " => " + str(self.dbId) + "(" + self.rule + ")" + " => " + self.tester)
        except:
            print("error, rule不能为空！")
            sys.exit(0)
        l_d_ = Sqlserver_PO.select("select sql from %s where [rule]='%s'" % (self.csgz, self.rule))
        l_sql = []
        for i in range(len(l_d_)):
            if os.name == "posix":
                l_sql.append(l_d_[i]['sql'])
            else:
                l_sql.append(l_d_[i]['sql'].encode('latin1').decode('GB2312'))
        return l_sql

    def runSqls(self, varSql):

        # 执行sql
        d_var = {}

        if 'self.i_startAssess2' in varSql:
            self.ASSESS_ID = eval(varSql)
            # l_d_ASSESS_ID = [{'ASSESS_ID': self.ASSESS_ID}]
            # return l_d_ASSESS_ID
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
                if '{diseaseRuleCode}' in varSql:
                    l_diseaseRuleCode = self.diseaseRuleCode.split(",")
                    # print(4444,l_diseaseRuleCode)
                    if len(l_diseaseRuleCode) > 1:
                        d_tmp = {}
                        for i in l_diseaseRuleCode:
                            varSql1 = varSql.replace("{diseaseRuleCode}", i)
                            # print(varSql1)
                            if Configparser_PO.SWITCH("log") == "on":
                                Color_PO.outColor([{"33": varSql1}])
                            self.log = self.log + "\n" + ", " + varSql1
                            command = 'Sqlserver_PO.select("' + varSql1 + '")'
                            l_d_ = eval(command)
                            d_tmp.update(l_d_[0])
                            # print(d_tmp)
                            l_d_ = [d_tmp]
                elif '{assessRuleCode}' in varSql:
                    l_assessRuleCode = self.assessRuleCode.split(",")
                    # print(666,l_assessRuleCode)
                    if len(l_assessRuleCode) > 1:
                        d_tmp = {}
                        for i in l_assessRuleCode:
                            varSql1 = varSql.replace("{assessRuleCode}", i)
                            # print(varSql1)
                            if Configparser_PO.SWITCH("log") == "on":
                                Color_PO.outColor([{"33": varSql1}])
                            self.log = self.log + "\n" + ", " + varSql1
                            command = 'Sqlserver_PO.select("' + varSql1 + '")'
                            l_d_ = eval(command)
                            d_tmp.update(l_d_[0])
                        # print(d_tmp)
                        l_d_ = [d_tmp]
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


    def runSql11(self, varSql):

        # 执行sql

        if 'self.i_startAssess2' in varSql:
            self.ASSESS_ID = eval(varSql)
            l_d_ASSESS_ID = [{'ASSESS_ID': self.ASSESS_ID}]
            return l_d_ASSESS_ID
        else:
            varPrefix = varSql.split(" ")[0]
            varPrefix = varPrefix.lower()
            if varPrefix == 'select':
                command = 'Sqlserver_PO.select("' + varSql + '")'
                l_d_ = eval(command)
                # sleep(1)
                return l_d_
            elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete':
                command = 'Sqlserver_PO.execute("' + varSql + '")'
                l_d_ = eval(command)
                # sleep(1)
                return l_d_
            else:
                return None

    def runStep(self, varId):

        self.log = ""
        count = 1
        d_allSort = {}
        d_error = {}

        # 获取rule步骤
        l_d_ = Sqlserver_PO.select("select [rule],tester from %s where id = '%s'" % (self.dbTable, varId))
        l_rule = l_d_[0]['rule'].split("\n")
        # print(l_rule)  # ["update TB_PREGNANT_MAIN_INFO set MCYJ='2024-08-06' where ZJHM = '31010520161202008X'", "self.i_startAssess2('31010520161202008X','6','0000001')", 'select LMP from T_ASSESS_MATERNAL where ASSESS_ID={ASSESS_ID}']

        # 生成动态临时库，保存变量与值
        self.tmp_db = 'a_temp' + str(Data_PO.getFigures(10))
        if Configparser_PO.SWITCH("log") == "on":
            Color_PO.outColor([{"31": self.tmp_db}])
        Sqlserver_PO.crtTable(self.tmp_db, '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')


        for i, v in enumerate(l_rule, start=1):
            if "{随机11}" in v:
                v = v.replace("{随机11}", Data_PO.getFigures(11))
            if "{ASSESS_ID}" in v:
                v = v.replace('{ASSESS_ID}', str(self.ASSESS_ID))

            self.log = self.log + v + "\n"

            varPrefix = v.split(" ")[0]
            varPrefix = varPrefix.lower()
            if varPrefix == 'select':
                self.selectResult = eval('Sqlserver_PO.select("' + v + '")')
                if self.selectResult == []:
                    Color_PO.outColor([{"31": "error, select语句无值 => " + v }])
                    Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, varId))
                    Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), varId))
                    self.log = (self.log).replace("'", "''")
                    Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, varId))
                    Sqlserver_PO.execute("drop table %s" % (self.tmp_db))
                    sys.exit(0)
                # print(213,self.selectResult)
                for k1, v1 in self.selectResult[0].items():
                    Sqlserver_PO.execute("insert into %s(key1,value1) values('%s','%s')" % (self.tmp_db, k1, v1))
            elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete':
                eval('Sqlserver_PO.execute("' + v + '")')
            else:
                if 'self.i_startAssess2' in v:
                    self.ASSESS_ID = eval(v)
                    self.log = self.log + "{ASSESS_ID} = " + str(self.ASSESS_ID) + "\n"
                else:
                    # 必须字典结构，断言select
                    d_expect = eval(v)

                    l_tmp = []
                    d_tmp2 = {}
                    for k2, v2 in d_expect.items():
                        d_tmp2[k2] = v2
                        l_tmp.append(d_tmp2)
                        d_tmp2 = {}
                    # print(l_tmp)
                    # 排序
                    d_sort = dict(enumerate(l_tmp, start=count))
                    # print(d_sort)  # {1: {'LMP': '123'}, 2: {'ID': 1}}

                    for k3, v3 in d_sort.items():
                        l_d_ = Sqlserver_PO.select("select key1,value1 from %s where id=%s" % (self.tmp_db, int(k3)))
                        # print(l_d_)
                        # print(l_d_[0]['key1'], l_d_[0]['value1'])
                        # print(list(d_sort[k3].keys())[0])
                        if l_d_[0]['key1'] == list(d_sort[k3].keys())[0] and l_d_[0]['value1'] == str(list(d_sort[k3].values())[0]):
                            d_allSort[k3] = "ok"
                        else:
                            d_allSort[k3] = "error"
                            d_error[k3] = "expect: " + l_d_[0]['key1'] + " = " + str(list(d_sort[k3].values())[0]) + " actual: " + l_d_[0]['key1'] + " = "+l_d_[0]['value1']
                            self.log = self.log + d_error[k3] + "\n"

                    count = count + len(d_sort)
                    # print(d_allSort)  # {1: 'error', 2: 'ok', 3: 'ok', 4: 'ok'}

        if "error" in list(d_allSort.values()):
            Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, varId))
            Color_PO.outColor([{"31": "[ERROR] => " + self.sheetName + " => " + str(varId)}])
            print(self.log)
        else:
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, varId))
            Color_PO.outColor([{"36": "[OK] => " + self.sheetName + " => " + str(varId)}])
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), varId))
        self.log = (self.log).replace("'", "''")
        Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, varId))
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))
        if Configparser_PO.SWITCH("step") == "on":
            print(self.log)


    def getRandomAssessValuebyName(self, assessName):

        # 获取疾病取值判断中 评估名对应的值
        l_d_ = Sqlserver_PO.select("select assessValue from a_jibingquzhipanduan where assessName='%s'" % (assessName))
        # print(l_d_)  # [{'assessValue': 'I60,I61,I62,I63,I64,I69.0,I69.1,I69.2,I69.3,I69.4'}]
        l_assessValue = l_d_[0]['assessValue'].split(",")
        return random.sample(l_assessValue, 1)[0]

    def getRandomAssessValuebyErrName(self, assessName):

        # 获取疾病取值判断中 评估名对应的值
        l_d_ = Sqlserver_PO.select("select assessValue from a_jibingquzhipanduan where assessName!='%s'" % (assessName))
        # print(l_d_)  # [{'assessValue': 'I60,I61,I62,I63,I64,I69.0,I69.1,I69.2,I69.3,I69.4'}]
        l_assessValue = l_d_[0]['assessValue'].split(",")
        return random.sample(l_assessValue, 1)[0]

    def getRandomICDbyName(self, diseaseName):

        # 随机获取疾病取值判断中 疾病名字对应值。
        l_d_ = Sqlserver_PO.select("select prefixICD from a_jibingquzhipanduan where diseaseName='%s'" % (diseaseName))
        # print(l_d_)  # [{'prefixICD': 'I60,I61,I62,I63,I64,I69.0,I69.1,I69.2,I69.3,I69.4'}]
        l_prefixICD = l_d_[0]['prefixICD'].split(",")
        return random.sample(l_prefixICD, 1)[0]

    def getRandomICDbyErrName(self, diseaseName):

        # 随机获取疾病取值判断中 非疾病名字对应值。
        l_d_ = Sqlserver_PO.select("select prefixICD from a_jibingquzhipanduan where diseaseName!='%s'" % (diseaseName))
        # print(l_d_)  # [{'prefixICD': 'I60,I61,I62,I63,I64,I69.0,I69.1,I69.2,I69.3,I69.4'}]
        l_prefixICD = l_d_[0]['prefixICD'].split(",")
        return random.sample(l_prefixICD, 1)[0]


    def run11(self, dbId):

        # 按id执行

        if isinstance(int(dbId), int):
            self.dbId = dbId
        else:
            sys.exit(0)

        self.d_param = {}

        # 获取表字段值
        l_d_rows = Sqlserver_PO.select("select * from %s where id=%s" % (self.dbTable, self.dbId))
        # print(l_d_rows[0]) # {'id': 1, 'result': 'ok', 'updateDate': datetime.datetime(2023, 11, 7, 10, 4, 15), 'rule': 'r1', 'ruleParam': "AGE=55 .and. CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001', '分类': '年龄', '规则名称': '年龄≥55岁', '评估规则详细描述': '年龄≥55岁', '评估因素判断规则': '年龄>=55', 'tester': '刘斌龙', 'var': ''}

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
        self.ruleCode = l_d_rows[0]['ruleCode']
        if 'diseaseRuleCode' in l_d_rows[0].keys():
            self.diseaseRuleCode = l_d_rows[0]['diseaseRuleCode']
        else:
            self.diseaseRuleCode = ""
        if 'diseaseCodeDesc' in l_d_rows[0].keys():
            self.diseaseCodeDesc = l_d_rows[0]['diseaseCodeDesc']
        else:
            self.diseaseCodeDesc = ""
        if 'assessCodeDesc' in l_d_rows[0].keys():
            self.assessCodeDesc = l_d_rows[0]['assessCodeDesc']
        else:
            self.assessCodeDesc = ""
        if 'assessRuleCode' in l_d_rows[0].keys():
            self.assessRuleCode = l_d_rows[0]['assessRuleCode']
        else:
            self.assessRuleCode = ""

        d_2 = {}
        if 'assessDesc' in l_d_rows[0].keys():
            if l_d_rows[0]['assessDesc'] == None or l_d_rows[0]['assessDesc'] == "":
                self.assessDesc = ""
            else:
                self.assessDesc = l_d_rows[0]['assessDesc']
                l_assessDesc = self.assessDesc.split(",")
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

        if self.rule == 's3' or self.rule == 's4' or self.rule == 's5':
            if self.case == 'negative':
                # ，如：高血压，参数{'VISITTYPECODE':'31','DIAGNOSIS_CODE':'I15'} 或 {'DIAGNOSIS_CODE':'I15'} ，其中无参数‘VISITTYPECODE':'31'，自动从疾病取值判断中匹配高血压=31。
                # self.outNegative1(self.testRule11())
                if self.ruleParam == {}:
                    # 实例3：反向无参
                    l_diseaseCodeDesc = self.diseaseCodeDesc.split(",")
                    for i in l_diseaseCodeDesc:
                        s_prefixICD = self.getRandomICDbyErrName(i)
                        # print(i, s_prefixICD)  # 高血压, I13
                        self.d_param[i] = s_prefixICD
                    l_assessDesc = self.assessDesc.split(",")
                    for i in l_assessDesc:
                        s_assessValue = self.getRandomAssessValuebyErrName(i)
                        print(i, s_assessValue)  # 高血压, I13
                        self.d_param[i] = s_assessValue
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"35": self.d_param}])
                    self.outResults(0, self.testRules())  # 反向传0
                else:
                    # 实例4：反向带参，{'高血压':'G40'}
                    l_diseaseCodeDesc = self.diseaseCodeDesc.split(",")
                    # print(l_diseaseCodeDesc)  # ['高血压', '糖尿病']
                    # print(list(self.ruleParam.keys()))  # ['高血压', '糖尿病']
                    if l_diseaseCodeDesc == list(self.ruleParam.keys()):
                        self.d_param = self.ruleParam
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"35": self.d_param}])
                        self.outResults(0, self.testRules())  # 反向传0
                    else:
                        print("error, ruleParm的key与diseaseCodeDesc不匹配！")
                        sys.exit(0)
            else:
                if self.ruleParam == {}:
                    # 实例1：正向无参, 随机获取疾病的prefixICD
                    d_1 = {}
                    l_diseaseCodeDesc = self.diseaseCodeDesc.split(",")  # ['高血压'，'糖尿病']
                    for i in l_diseaseCodeDesc:
                        s_prefixICD = self.getRandomICDbyName(i)
                        # print(i, s_prefixICD)  # 高血压, I13
                        d_1[i] = s_prefixICD
                    self.d_param['prefixICD'] = d_1

                    # todo 2
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"35": self.d_param}])
                    self.outResults(1, self.testRules())  # 正向传1
                else:
                    # 实例2：正向带参，{'高血压':'I12','糖尿病':'E14'}
                    l_diseaseCodeDesc = self.diseaseCodeDesc.split(",")
                    # print(l_diseaseCodeDesc)  # ['高血压', '糖尿病']
                    # print(list(self.ruleParam.keys()))  # ['高血压', '糖尿病']
                    if l_diseaseCodeDesc == list(self.ruleParam.keys()):
                        self.d_param = self.ruleParam
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"35": self.d_param}])
                        self.outResults(1, self.testRules())  # 正向传1
                    else:
                        print("error, ruleParm的key与diseaseCodeDesc不匹配！")
                        sys.exit(0)

        if self.rule == 's1':
            if self.case == 'negative':
                if self.ruleParam == {}:
                    # 实例2：反无参
                    # s_prefixICD = self.getRandomICDbyName(self.diseaseCodeDesc)
                    # self.d_param[self.diseaseCodeDesc] = s_prefixICD  # {'慢性肾脏病':'?'}
                    # Color_PO.outColor([{"35": self.d_param}])
                    # self.outResults(0, self.testRules())  # 反向传0

                    l_d_ = Sqlserver_PO.select(
                        "select prefixICD from a_jibingquzhipanduan where diseaseName='%s'" % (self.diseaseCodeDesc))
                    # print(l_d_[0]['prefixICD'])  # I10,I11,I12,I13,I14,I15
                    l_prefixICD = l_d_[0]['prefixICD'].split(',')
                    # print(l_prefixICD)
                    s_prefixICD = random.sample(l_prefixICD, 1)[0]
                    # print(s_prefixICD)
                    self.d_param[self.diseaseCodeDesc] = s_prefixICD  # {'慢性肾脏病':'?'}
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"35": self.d_param}])

                    self.outResults(0, self.testRules())  # 反向传0
                else:
                    # 实例4：反有参 {'VISITTYPECODE':'34','慢性肾脏病':'?'}
                    if self.diseaseCodeDesc in list(self.ruleParam.keys()):
                        self.d_param = self.ruleParam
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"35": self.d_param}])

                        self.outResults(0, self.testRules())  # 反向传1


                    else:
                        print("error, ruleParm的key与diseaseCodeDesc不匹配！")
                        sys.exit(0)
            else:
                if self.ruleParam == {}:
                    # 实例1：正无参, 随机获取疾病的prefixICD
                    # 正向，无参数
                    l_ = []
                    # 1 遍历a_jiankangganyu_yihuanjibingzuhe,判断 diseaseCodeDesc 是否包含高血压及其他疾病
                    l_d_ = Sqlserver_PO.select(
                        "select diseaseCodeDesc from a_jiankangganyu_yihuanjibingzuhe where diseaseCodeDesc like '%s'" % (
                                '%' + self.diseaseCodeDesc + '%'))
                    # print(l_d_)  # [{'diseaseCodeDesc': '高血压'}, {'diseaseCodeDesc': '高血压,糖尿病'},
                    for d_ in l_d_:
                        if ',' in d_['diseaseCodeDesc']:
                            l_.append(d_['diseaseCodeDesc'])

                    # 2 获取疾病列表a，并去重
                    l_2 = List_PO.deduplication(l_)
                    l_4 = []
                    for j in l_2:
                        l_3 = j.split(",")
                        for j in l_3:
                            l_4.append(j)
                    l_5 = List_PO.deduplication(l_4)
                    # print(l_5)

                    # 3 遍历疾病取值判断(a_jibingquzhipanduan)，去掉疾病列表a中疾病，剩下的疾病中将prefixICD值组合成列表b
                    l_d_ = Sqlserver_PO.select("select diseaseName from a_jibingquzhipanduan")
                    # print(l_d_)
                    l_6 = []
                    for k in l_d_:
                        l_6.append(k['diseaseName'])
                    # print(l_6)
                    l_7 = [x for x in l_6 if x not in l_5]
                    # print(l_7)

                    # 4 随机获取l_7的prefixICD值，赋值给DIAGNOSIS_CODE
                    s_8 = random.sample(l_7, 1)[0]
                    # print(s_8)
                    l_d_ = Sqlserver_PO.select(
                        "select prefixICD from a_jibingquzhipanduan where diseaseName='%s'" % (s_8))
                    # print(l_d_)
                    # print(l_d_[0]['prefixICD'])  # A15,A16,A1,A18,A19,B90
                    l_9 = l_d_[0]['prefixICD'].split(",")
                    # print(l_9)
                    s_10 = random.sample(l_9, 1)[0]
                    # print(s_10)
                    # self.sql[i] = str(self.sql[i]).replace('{prefixErrICD}', str(s_10))

                    self.d_param[self.diseaseCodeDesc] = str(s_10)  # {'高血压':'？'}
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"35": self.d_param}])

                    self.outResults(1, self.testRules())  # 正向传1
                else:
                    # 实例3：正有参 {'VISITTYPECODE':'34','慢性肾脏病':'N03'}
                    # print(list(self.ruleParam.keys()))  # ['VISITTYPECODE', '慢性肾脏病']
                    if self.diseaseCodeDesc in list(self.ruleParam.keys()):
                        self.d_param = self.ruleParam
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"35": self.d_param}])

                        self.outResults(1, self.testRules())  # 正向传1
                    else:
                        print("error, ruleParm的key与diseaseCodeDesc不匹配！")
                        sys.exit(0)

        if self.rule == 's2':
            if self.case == 'negative':
                if self.ruleParam == {}:
                    # 实例2：反无参
                    s_prefixICD = self.getRandomICDbyErrName(self.diseaseCodeDesc)
                    self.d_param[self.diseaseCodeDesc] = s_prefixICD  # {'慢性肾脏病':'?'}
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"35": self.d_param}])
                    self.outResults(0, self.testRules())  # 反向传0
                else:
                    # 实例4：反有参 {'VISITTYPECODE':'34','慢性肾脏病':'?'}
                    if self.diseaseCodeDesc in list(self.ruleParam.keys()):
                        self.d_param = self.ruleParam
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"35": self.d_param}])
                        self.outResults(0, self.testRules())  # 反向传1
                    else:
                        print("error, ruleParm的key与diseaseCodeDesc不匹配！")
                        sys.exit(0)
            else:
                if self.ruleParam == {}:
                    # 实例1：正无参, 随机获取疾病的prefixICD
                    s_prefixICD = self.getRandomICDbyName(self.diseaseCodeDesc)
                    self.d_param[self.diseaseCodeDesc] = s_prefixICD  # {'慢性肾脏病':'N11'}
                    if Configparser_PO.SWITCH("log") == "on":
                        Color_PO.outColor([{"35": self.d_param}])
                    self.outResults(1, self.testRules())  # 正向传1
                else:
                    # 实例3：正有参 {'VISITTYPECODE':'34','慢性肾脏病':'N03'}
                    # print(list(self.ruleParam.keys()))  # ['VISITTYPECODE', '慢性肾脏病']
                    if self.diseaseCodeDesc in list(self.ruleParam.keys()):
                        self.d_param = self.ruleParam
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"35": self.d_param}])
                        self.outResults(1, self.testRules())  # 正向传1
                    else:
                        print("error, ruleParm的key与diseaseCodeDesc不匹配！")
                        sys.exit(0)


        if self.rule == 's2bak' :
            if self.case == 'negative':
                if self.ruleParam != None:
                    # 实例4：反向带参，如：{'DIAGNOSIS_CODE':'I15'}  ，'I15'是错误的值。
                    print(self.ruleParam['DIAGNOSIS_CODE'])
                    self.prefixICD = self.ruleParam['DIAGNOSIS_CODE']
                else:
                    # 实例3：反向无参
                    # print(self.diseaseCodeDesc)
                    l_d_ = Sqlserver_PO.select(
                        "select prefixICD from a_jibingquzhipanduan where diseaseName !='%s'" % (self.diseaseCodeDesc))
                    # print(l_d_)  # [{'prefixICD': 'I60,I61,I62,I63,I64,I69.0,I69.1,I69.2,I69.3,I69.4'}]
                    l_1 = l_d_[0]['prefixICD'].split(",")
                    l_3 = []
                    for i in l_d_:
                        l_2 = i['prefixICD'].split(",")
                        # print(l_2)
                        l_3 = l_3 + l_2
                    # print(l_3)
                    # sys.exit(0)
                    self.prefixICD = random.sample(l_3, 1)[0]
                    print(self.prefixICD)
                self.outNegative0(self.testRule11())
            else:
                if self.ruleParam != None:
                    # 实例2：带参，如：高血压 {'DIAGNOSIS_CODE':'I15'}
                    print(self.ruleParam['DIAGNOSIS_CODE'])
                    self.prefixICD = self.ruleParam['DIAGNOSIS_CODE']
                    self.outResult2(self.testRule11())
                else:
                    # 实例1：无参数，自动从疾病取值判断中匹配，建议使用。
                    # 1 遍历疾病取值判断(a_jibingquzhipanduan)，测试所有值
                    l_d_ = Sqlserver_PO.select("select prefixICD from a_jibingquzhipanduan where diseaseName='%s'" % (self.diseaseCodeDesc))
                    # print(l_d_)  # [{'prefixICD': 'I60,I61,I62,I63,I64,I69.0,I69.1,I69.2,I69.3,I69.4'}]
                    l_1 = l_d_[0]['prefixICD'].split(",")
                    d_eachResult = {}
                    d_eachStep = {}
                    for i in l_1:
                        # d['prefixICD'] = i
                        self.prefixICD = i
                        print(self.prefixICD)
                        # a = self.testRule11(d)
                        varQty = self.testRule11()

                        if varQty == 2:
                            # Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(
                            #     self.rule) + ") => OK]").center(100, '-')), "")
                            d_eachResult[self.prefixICD] = 'ok'
                            d_eachResult1 = str(d_eachResult).replace("'", "''")
                            # print(d_eachResult1)
                            Sqlserver_PO.execute("update %s set eachResult='%s' where id=%s" % (self.dbTable, str(d_eachResult1), self.dbId))
                            self.log = (self.log).replace("'", "''")
                            d_eachStep[self.prefixICD] = self.log
                            d_eachStep1 = str(d_eachStep).replace("'", "''")
                            # print(d_eachStep1)
                            Sqlserver_PO.execute("update %s set eachStep='%s' where id=%s" % (self.dbTable, str(d_eachStep1), self.dbId))
                        else:
                            Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
                            d_eachResult[self.prefixICD] = 'error'
                            Sqlserver_PO.execute("update %s set eachResult='%s' where id=%s" % (self.dbTable, str(d_eachResult), self.dbId))
                            print(self.log)
                            self.log = (self.log).replace("'", "''")
                            Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(
                                self.rule) + ") => ERROR]").center(100, '-')), "")
                            d_eachStep[self.prefixICD] = self.log
                            Sqlserver_PO.execute("update %s set eachStep='%s' where id=%s" % (self.dbTable, str(d_eachStep), self.dbId))
                            Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (
                                self.dbTable, self.dbId, Time_PO.getDateTimeByDivide(), self.log))
                        # Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
                        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))

                    l_d_ = Sqlserver_PO.select("select eachResult from %s where id='%s'" % (self.dbTable, self.dbId))
                    print(l_d_)
                    s_33 = l_d_[0]['eachResult']  #  {'N03': 'ok', 'N11': 'ok', 'N18': 'ok'}
                    # print(s_33)
                    d_33 = dict(eval(s_33))
                    # print(d_33)
                    # print(list(d_33.values()))
                    if "error" in list(d_33.values()):
                        self.outS2_2(1)
                    else:
                        self.outS2_2(2)

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


    def testRules(self):

        # 生成动态临时库，保存变量与值
        # todo 3
        self.tmp_db = 'a_temp' + str(Data_PO.getFigures(10))
        # print(self.tmp_db)
        if Configparser_PO.SWITCH("log") == "on":
            Color_PO.outColor([{"33": self.tmp_db}])
        Sqlserver_PO.crtTable(self.tmp_db, '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')

        # 获取临时变量
        d_update = {}
        self.ASSESS_ID = ""
        d_total = {}
        for i in range(len(self.sql)):

            # 格式化sql
            if "{随机11}" in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{随机11}", Data_PO.getFigures(11))
            if '{ruleCode}' in self.sql[i]:
                self.sql[i] = self.sql[i].replace("{ruleCode}", self.ruleCode)
            if '{diseaseRuleCode}' in self.sql[i]:
                l_diseaseRuleCode = self.diseaseRuleCode.split(",")
                if len(l_diseaseRuleCode) == 1:
                    self.sql[i] = self.sql[i].replace("{diseaseRuleCode}", self.diseaseRuleCode)
            if '{assessRuleCode}' in self.sql[i]:
                l_assessRuleCode = self.assessRuleCode.split(",")
                if len(l_assessRuleCode) == 1:
                    self.sql[i] = self.sql[i].replace("{assessRuleCode}", self.assessRuleCode)



            # s1/s2
            # 获取疾病取值判断对应的visitTypeCode，并替换VISITTYPECODE
            if 'VISITTYPECODE' in self.d_param:
                self.sql[i] = self.getVisitTypeCode(self.sql[i], 'VISITTYPECODE')
                del self.d_param['VISITTYPECODE']

            # 将db转换成字典
            l = Sqlserver_PO.select("select key1, value1 from %s" % (self.tmp_db))
            # print(l) # [{'key1': 'ID', 'value1': '499948'}, {'key1': 'QTY', 'value1': '1'}, {'key1': 'Q2', 'value1': '1'},
            for p in range(len(l)):
                d_update[l[p]['key1']] = l[p]['value1']
                if 'GUID' in d_update:
                    self.sql[i] = str(self.sql[i]).replace("{varGUID}", str(d_update['GUID']))

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
                self.log = str(i + 1) + ", " + self.sql[i]
            else:
                # self.log = self.log + "\n" + str(i + 1) + ", " + self.sql[i]

                if self.rule == 's4':
                    if "{'血脂异常'" in self.sql[i]:
                        if '血脂异常' in self.d_param:
                            self.log = self.log + "\n" + str(i + 1) + ", " + self.sql[i]
                    else:
                        self.log = self.log + "\n" + str(i + 1) + ", " + self.sql[i]
                else:
                    self.log = self.log + "\n" + str(i + 1) + ", " + self.sql[i]

            # todo 执行sql
            # sql返回值
            l_d_ = self.runSqls(self.sql[i])
            # print(666,l_d_)

            if l_d_ != None:
                if isinstance(l_d_, list) and l_d_ != []:
                    if isinstance(l_d_[0], dict):

                        # 将变量存入db
                        for k, v in l_d_[0].items():
                            Sqlserver_PO.execute("insert into %s (key1,value1) values ('%s', '%s')" % (self.tmp_db, str(k), str(v)))

                        # 打印返回值
                        if Configparser_PO.SWITCH("log") == "on":
                            Color_PO.outColor([{"35": l_d_[0]}])  # {'GUID': '65209815'}

                        d_total.update(l_d_[0])

        # print(d_total)

        self.log = self.log + "\n" + str(d_total)
        return d_total



    def outResult1(self, varQty):

        if varQty == 1:
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
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))
        Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (self.dbTable,self.dbId,Time_PO.getDateTimeByDivide(),self.log))

    def outResult2(self, varQty):

        if varQty == 2:
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

    def outResults(self, qty, d_total):

        # qty = 1 正向匹配所有value都为1
        # qty = 0 反向匹配所有value都为0

        varSign = 0
        print(d_total) #  {'GUID': '65209815', 'YH_JB001': 1, 'YH_JB002': 1, 'GY_YHZH078001': 1}
        l_diseaseRuleCode = self.diseaseRuleCode.split(",")
        # print(l_diseaseRuleCode)  # ['YH_JB001','YH_JB002']
        # print(self.ruleCode)  # GY_YHZH078001
        l_diseaseRuleCode.append(self.ruleCode)
        # print(l_diseaseRuleCode)  # ['YH_JB001','YH_JB002','GY_YHZH078001']
        for i in l_diseaseRuleCode:
            if i in d_total.keys():
                if d_total[i] == qty:
                    varSign = varSign + 0
                else:
                    varSign = varSign + 1

        if varSign == 0:
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


    def outS2_2(self, varQty):

        if varQty == 2:
            Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
            # print(self.log)
            # self.log = (self.log).replace("''", "\'")
            # print(self.log)
            # Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
        else:
            Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='error' where id=%s" % (self.dbTable, self.dbId))
            print(self.log)
            # self.log = (self.log).replace("''", "'")
            Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (
            self.dbTable, self.dbId, Time_PO.getDateTimeByDivide(), self.log))
            # Sqlserver_PO.execute("update %s set step='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))

    def outNegative1(self, varQty):

        # negative

        if varQty == 1:
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
            Sqlserver_PO.execute("insert into a_log (t,t_id,updateDate,step) values('%s',%s,'%s','%s')" % (
            self.dbTable, self.dbId, Time_PO.getDateTimeByDivide(), self.log))

        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))

    def outNegative0(self, varQty):

        # negative

        if varQty == 0:
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




    def _getParamByGW(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        self._getDiseaseIdcardGW(d)

    def outResultGW(self, d_actual):

        varSign = 0
        d_error = {}
        for k, v in d_actual.items():
            if (k == "QTY0" and v == 0) or (k != "QTY0" and v == 1):
                varSign = 0
            else:
                varSign = 1
                d_error[k] = v

        if Configparser_PO.SWITCH("log") == "on":
            print('值 => ' + str(d_actual))

        if varSign == 0:
            Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            # Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTable, self.dbId))
        else:
            Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
            print(self.log)
            Color_PO.consoleColor("31", "31", '错误值 => ' + str(d_error), "")
            self.log = self.log + str(d_error)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            # Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTable, self.dbId))
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))

    def _getAutoIdcard(self, d):

        # 随机获取疾病身份证中身份证

        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)  # [{'diseaseRuleCode': 'YH_JB001', 'idcard': 310101202308070001}, ...]
        l_1 = []
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            l_1.append(l_d_diseaseRuleCode_idcard[i]['idcard'])
        d["varIdcard"] = random.choice(l_1)
        # print(d["varIdcard"])
        self.verifyIdcard(varIdcard)
        if varIdcard != None:
            if 'hitQty' in d and d['hitQty'] == 2:
                self.outResult2(self.testRule(d))
            else:
                self.outResult1(self.testRule(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard2() => 身份证不能为None!]", "")

    def _getDiseaseIdcard2(self, d):

        # 健康干预命中次数之获取身份证

        # print(d)
        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            for k, v in l_d_diseaseRuleCode_idcard[i].items():
                # print(l_d_diseaseRuleCode_idcard[i][k])
                if l_d_diseaseRuleCode_idcard[i][k] == d['diseaseRuleCode']:
                    varIdcard = l_d_diseaseRuleCode_idcard[i]['idcard']
                    break

        d["varIdcard"] = varIdcard
        self.verifyIdcard(varIdcard)

        if varIdcard != None:
            if 'hitQty' in d and d['hitQty'] == 2:
                self.outResult2(self.testRule(d))
            else:
                self.outResult1(self.testRule(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard2() => 身份证不能为None!]", "")

    def _getDiseaseIdcardGW(self, d):

        # print(d)
        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            for k, v in l_d_diseaseRuleCode_idcard[i].items():
                # print(l_d_diseaseRuleCode_idcard[i][k])
                if l_d_diseaseRuleCode_idcard[i][k] == d['diseaseRuleCode']:
                    varIdcard = l_d_diseaseRuleCode_idcard[i]['idcard']
                    break
        d["varIdcard"] = varIdcard
        self.verifyIdcard(varIdcard)
        if varIdcard != None:
            # d_actual = self.gw(d)
            # l_ruleCode, d_actual = self.gw(d)
            # l_ruleCode.remove(d['diseaseRuleCode'])  # ['PG_JWS041', 'PG_JWS043']
            # print(d_actual)
            # self.outResultGW(l_ruleCode, d_all)
            # print(d_actual)
            self.outResultGW(self.gw(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard() => 身份证不能为None!]", "")

    def gw(self, d):

        l_sql = d['l_sql']
        d_actual = {}
        self.log = ""

        for i in range(len(l_sql)):

            if 'varIdcard' in d:
                l_sql[i] = str(l_sql[i]).replace("{身份证}", str(d['varIdcard']))
            if 'ruleParam1' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数1}", d['ruleParam1'])
            if 'ruleParam2' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数2}", d['ruleParam2'])
            if 'ruleParam3' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数3}", d['ruleParam3'])
            if 'ruleParam4' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数4}", d['ruleParam4'])
            if 'ruleParam' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数}", d['ruleParam'])
            if 'ruleCode' in d:
                l_sql[i] = str(l_sql[i]).replace("{规则编码}", d['ruleCode'])
            if "{随机数}" in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{随机数}", Data_PO.getPhone())
            if '{疾病评估规则编码}' in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{疾病评估规则编码}", d['diseaseRuleCode'])

        # pc.copy('')  # 清空剪贴板
        # 生成动态临时数据库
        self.tmp_db = 'a_temp' + str(Data_PO.getFigures(10))
        # print(self.tmp_db)
        Sqlserver_PO.crtTable(self.tmp_db, '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')

        # 获取临时变量 - gw
        d_update = {}  # 更新数据
        d_new = {}  # 新数据
        for i in range(len(l_sql)):
            # s = pc.paste()

            # 将db转换成字典
            l = Sqlserver_PO.select("select key1, value1 from %s" % (self.tmp_db))
            # print(l) # [{'key1': 'ID', 'value1': '499948'}, {'key1': 'QTY', 'value1': '1'}, {'key1': 'Q2', 'value1': '1'},
            d_update = {}
            for p in range(len(l)):
                d_update[l[p]['key1']] = l[p]['value1']

            # if "{" in s:
            #     d_new = Str_PO.str2dict(s)
            #     d_update.update(d_new)  # 新数据合并到更新数据中

            if 'ID' in d_update:
                l_sql[i] = str(l_sql[i]).replace("{ID}", str(d_update['ID']))
            if 'IDCARD' in d_update:
                l_sql[i] = str(l_sql[i]).replace("{IDCARD}", str(d_update['IDCARD']))
            if 'GUID' in d_update:
                l_sql[i] = str(l_sql[i]).replace("{GUID}", str(d_update['GUID']))

            # 输出sql语句 - gw
            if Configparser_PO.SWITCH("log") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 2, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'

            # 记录步骤日志 - gw
            if self.log == "":
                self.log = str(i + 1) + ", " + l_sql[i]
            else:
                self.log = self.log + "\n" + str(i + 1) + ", " + l_sql[i]

            # 执行sql - gw
            a = self.runSql(l_sql[i])

            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        # pc.copy(str(a[0]))

                        # 将变量存入db
                        for k, v in a[0].items():
                            Sqlserver_PO.execute("insert into %s (key1,value1) values ('%s', '%s')" % (self.tmp_db, str(k), str(v)))

                        self.log = self.log + "\n" + str(a[0])
                        if Configparser_PO.SWITCH("log") == "on":
                            for k, v in a[0].items():
                                if k == "QTY0" or k == "ID":
                                    Color_PO.consoleColor("31", "33", a[0], "")
                                else:
                                    if v != 1 :
                                        Color_PO.consoleColor("31", "31", a[0], "")
                                    else:
                                        Color_PO.consoleColor("31", "33", a[0], "")
                        # print(a[0])
                        # print(d_actual)
                        from collections import ChainMap
                        d_actual = dict(ChainMap(a[0], d_actual))
                        # d_actual = Dict_PO.mergeDictReserveFirstKey(a[0], d_actual)  # {'a': 1, 'b': 2, 'dev': 30, 'test': 3}

        # ruleCode = d['ruleCode'].replace("(", '').replace(")", '').replace("'", '')
        # # print(ruleCode)  # 'GW_JB011','PG_JWS041','PG_JWS043'
        # l_ruleCode = Str_PO.str2list(ruleCode)
        if "ID" in d_actual:
            del d_actual['ID']
        if "ID_CARD" in d_actual:
            del d_actual['ID_CARD']
        if "GUID" in d_actual:
            del d_actual['GUID']
        return d_actual
