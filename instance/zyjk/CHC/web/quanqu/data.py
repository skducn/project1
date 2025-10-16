# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2025-10-15
# Description: 社区健康管理中心 - 数据流转
# 测试环境 # http://192.168.0.243:8010/#/login
# 账号: lbl 密码：Qa@123456
# # 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
#***************************************************************
from PO.SqlserverPO import *

# todo 社区健康平台（全市）
Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHCCONFIG", "GBK")

# Sqlserver_PO.record('sys_user', 'varchar', '%小茄子%')
# id=82,
# NAME:小茄子
# 机构名称, ORG_NAME :宝山社区卫生服务中
# 所属机构编码, ORG_CODE:0000001
# 人员类别编码, CATEGORY_CODE: 4
# 人员类别, CATEGORY_NAME:中心主任
# 第三方工号, THIRD_NO:1231231



Sqlserver_PO = SqlserverPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")

# todo 健康评估及干预
# Sqlserver_PO.record('*', 'varchar', '%白*均%')
# Sqlserver_PO.record('*', 'varchar', '%徐东%', False)
# ----------------------------------------------------------------------------------------------------
# NAME = %徐东% >> TB_RIS_REPORT2(检查报告表(通用检查格式)) >> 8条
# {'GUID': '唯一主键', 'VISITSTRNO': '就诊流水号门诊或住院流水号', 'ORGCODE': '医疗机构代码', 'ORGNAME': '机构名称', 'VISITTYPE': '就诊类型1：门诊，2：住院', 'STUDYUID': '检查号DICOM标准中每个STUDY的UID，多个时使用“,”连接', 'REPORTNO': '报告单号报告生成 DICOM 文件对应的SOP INSTANCE UID（0008，0018）', 'NAME': '患者姓名', 'SEXCODE': '性别代码', 'SEXVALUE': '性别名称', 'PATIENTID': '影像号被检查的病人在医院内部的影像号码，即影像图像DICOM文件中对应DICOM中位置(0010,0020)的值', 'ITEMCODE': '检查项目标准代码由医保统一要求的收费编码，若没有医保统一编码，则填写填写卫计委的收费代码（物价编码）', 'APPLYNO': '申请单号该检查在HIS或RIS中的申请单编号', 'CHECKDATE': '检查时间', 'CHECKTYPE': '检查类型01-计算机X线断层摄影  CT \r\n02-核磁共振成像  MR \r\n03-NUMBER减影血管造影  DSA \r\n04-普通X光摄影  X-RAY \r\n05-特殊X光摄影  X-RAY \r\n06-超声检查  US \r\n07-病理检查  MICROSCOPY \r\n08-內镜检查  ES \r\n09-核医学检查  NM \r\n10-其他检查  OT ', 'REPORTDATE': '报告日期', 'CHECKPART': '检查部位文字说明被检查的部位。', 'CHECKMETHOD': '检查方法', 'CHECKPARTACRCODE': '检查部位ACR编码表明病人的检查部位的编码', 'CHECKNAME': '检查名称检查内容名称的文字描述', 'TITLE1CODE': '标题一编码0001-检查部位\r\n0002-活检部位\r\n0003-检查名称\r\n0004-标本种类；按《标本字典表》中定义的填写\r\n0005-HP 检测\r\n0006-图像记录方式\r\n0007-放射性显示剂\r\n0008-检查方法或技术\r\n0009-放射性显示剂剂量\r\n0010-探头频率\r\n0011-显像项目\r\n0012-媒体号\r\n0013-图像等级\r\n0014-临床诊断\r\n0015-影像表现或检查所见\r\n0016-检查诊断或提示\r\n0017-备注或建议', 'TITLE1NAME': '标题一名称', 'TITLE1CONTENT': '标题一内容', 'TITLE2CODE': '标题二编码', 'TITLE2NAME': '标题二名称', 'TITLE2CONTENT': '标题二内容', 'TITLE3CODE': '标题三编码', 'TITLE3NAME': '标题三名称', 'TITLE3CONTENT': '标题三内容', 'TITLE4CODE': '标题四编码', 'TITLE4NAME': '标题四名称', 'TITLE4CONTENT': '标题四内容', 'TITLE5CODE': '标题五编码', 'TITLE5NAME': '标题五名称', 'TITLE5CONTENT': '标题五内容', 'TITLE6CODE': '标题六编码', 'TITLE6NAME': '标题六名称', 'TITLE6CONTENT': '标题六内容', 'TITLE7CODE': '标题七编码', 'TITLE7NAME': '标题七名称', 'TITLE7CONTENT': '标题七内容', 'TITLE8CODE': '标题八编码', 'TITLE8NAME': '标题八名称', 'TITLE8CONTENT': '标题八内容', 'TITLE9CODE': '标题九编码', 'TITLE9NAME': '标题九名称', 'TITLE9CONTENT': '标题九内容', 'TITLE10CODE': '标题十编码', 'TITLE10NAME': '标题十名称', 'TITLE10CONTENT': '标题十内容', 'TITLE11CODE': '标题十一编码', 'TITLE11NAME': '标题十一名称', 'TITLE11CONTENT': '标题十一内容', 'TITLE12CODE': '标题十二编码', 'TITLE12NAME': '标题十二名称', 'TITLE12CONTENT': '标题十二内容', 'TITLE13CODE': '标题十三编码', 'TITLE13NAME': '标题十三名称', 'TITLE13CONTENT': '标题十三内容', 'TITLE14CODE': '标题十四编码', 'TITLE14NAME': '标题十四名称', 'TITLE14CONTENT': '标题十四内容', 'TITLE15CODE': '标题十五编码', 'TITLE15NAME': '标题十五名称', 'TITLE15CONTENT': '标题十五内容', 'CREATEDATE': '数据插入时间'}
# ----------------------------------------------------------------------------------------------------
# NAME = %徐东% >> HEALTH_OUTPATIENT_REGISTRATION(健康管理门诊登记表) >> 1条
# {'ID': '主键自增', 'ID_CARD': '身份证号', 'NAME': '姓名', 'AGE': '登记时年龄', 'TELEPHONE': '联系电话', 'REGISTRATION_DATE': '登记日期时间', 'REGISTRATION_DOC_ID': '登记人ID', 'REGISTRATION_ORG_CODE': '登记机构编码', 'REGISTRATION_DOC_NAME': '登记人姓名', 'REGISTRATION_ORG_NAME': '登记机构名称', 'SEX_CODE': '性别'}
# ----------------------------------------------------------------------------------------------------
# NAME = %徐东% >> T_ASSESS_BATCH_ABNORMAL(None) >> 4条
# {'ID': '主键ID', 'INFO_ID': '关联ID', 'ID_CARD': '身份证号码', 'NAME': '姓名', 'CREATE_DATE': '创建时间', 'CATEGORY_CODE': '人群分类代码（1-0-6岁儿童，2-学生（7-17岁），3-普通人群，4-老年人，5-未分类）', 'ORG_CODE': '机构代码', 'EVALUATION_TYPE': '评估类型（0-健康评估 1-体重报告）', 'ORG_NAME': '机构名称'}
# ----------------------------------------------------------------------------------------------------
# NAME = %徐东% >> TB_CIS_LH_SUMMARY(出院小结表) >> 2条
# {'GUID': '唯一主键', 'IPVISITSTRNO': '住院流水号TB_HIS_OP_MEDICAL_RECORD.OPVISITSTRNO\r\nTB_HIS_IP_MEDICAL_RECORD.IPVISITSTRNO', 'ORGCODE': '医疗机构代码', 'ORGNAME': '机构名称', 'DISCHARGEDEPTCODE': '出院科室代码', 'DISCHARGEDEPTNAME': '出院科室名称', 'VISITCARDTYPECODESYSTEM': '卡类型代码类别标识', 'VISITCARDTYPE': '卡类型', 'VISITCARDNO': '卡号', 'NAME': '患者姓名', 'BEDNO': '床号', 'ADMISSIONDATE': '入院时间', 'DISCHARGEDATE': '出院时间', 'STAYDAYS': '住院天数', 'ADMISSIONSYMPTOM': '入院时主要症状及体征', 'LABANDCONSULATION': '实验室检查及主要会诊', 'SPECIALEXAMINATION': '住院期间特殊检查', 'TREATMENTPROCESS': '诊疗过程', 'CC': '合并症', 'DISCHARGESITUATION': '出院时情况', 'DISCHARGEINSTUCTIONS': '出院医嘱', 'TREATMENTRESULTCODESYSTEM': '治疗结果代码类别标识CV5501.11', 'TREATMENTRESULTCODE': '治疗结果代码治疗结果代码', 'TREATMENTRESULTNAME': '治疗结果名称1.治愈；2.好转；3.无效；4.未治；5.死亡；9.其他', 'TREATMENTRESULTDESC': '治疗结果描述', 'DOCTORNO': '主治医生工号', 'DOCTORNAME': '主治医生姓名', 'STATUS': '状态0：正常、1：撤销', 'CREATEDATE': '数据插入时间', 'ISCURRENT': '当前版本1：当前版本、0：历史版本'}
# ----------------------------------------------------------------------------------------------------
# JMXM = %徐东% >> QYYH(1+1+1签约信息表) >> 1条
# {'CZRYBM': '签约医生代码', 'CZRYXM': '签约医生名称', 'JMXM': '居民姓名', 'SJHM': '联系电话', 'SFZH': '身份证号', 'JJDZ': '居住地址', 'SFJD': '是否建档', 'ARCHIVEUNITCODE': '医疗机构代码', 'ARCHIVEUNITNAME': '医疗机构名称', 'DISTRICTORGCODE': '区级医疗机构代码', 'DISTRICTORGNAME': '区级医疗机构名称', 'TERTIARYORGCODE': '三级医疗机构代码', 'TERTIARYORGNAME': '三级医疗机构名称', 'PRESENTADDRDIVISIONCODE': '居住地-行政区划代码', 'PRESENTADDRPROVCODE': '居住地-省市编码', 'PRESENTADDRPROVVALUE': '居住地-省市名称', 'PRESENTADDRCITYCODE': '居住地-地市编码', 'PRESENTADDRCITYVALUE': '居住地-地市名称', 'PRESENTADDRDISTCODE': '居住地-区县编码', 'PRESENTADDDISTVALUE': '居住地-区县名称', 'PRESENTADDRTOWNSHIPCODE': '居住地-街道(乡镇)编码', 'PRESENTADDRTOWNSHIPVALUE': '居住地-街道(乡镇)名称', 'PRESENTADDRNEIGHBORHOODCODE': '居住地_居委编码', 'PRESENTADDRNEIGHBORHOODVALUE': '居住地_居委名称', 'SIGNSTATUS': '签约状态', 'SIGNDATE': '签约时间', 'ID': '主键', 'CATEGORY_CODE': '人群分类代码（1-0-6岁儿童，2-学生（7-17岁），3-普通人群，4-老年人，5-未分类，6-孕妇，7-产妇）', 'CATEGORY_NAME': '人群分类', 'SEX_CODE': '性别代码', 'SEX_NAME': '性别', 'LAST_SERVICE_DATE': '上次服务日期', 'ASSISTANT_DOC_ID': '家医助理id', 'ASSISTANT_DOC_NAME': '家医助理姓名', 'HEALTH_MANAGER_ID': '健康管理师id', 'HEALTH_MANAGER_NAME': '健康管理师姓名', 'ASSISTANT_DOC_PHONE': '家医助理手机号', 'HEALTH_MANAGER_PHONE': '健康管理师手机号', 'KEY_POPULATION': '重点人群（0-非重点人群，1-重点人群）', 'REPORT_STATUS': '评估状态(0:预评估；1:评估完成；2:未评估)', 'ASSESS_ORDER': '排序', 'STOP_ASSESS_STATUS': '数据状态(0:正常数据,1:死亡,2:精神障碍,3:易纠纷,4:其他)', 'STOP_ASSESS_DATA': '停止评估时间', 'STOP_ASSESS_DOC_ID': '停止评估医生工号', 'STOP_ASSESS_DOC_NAME': '停止评估医生名称', 'LATEST_ASSESS_DATE': '最新评估时间', 'LATEST_CONFIRM_DATE': '最新确认时间', 'REPORT_UPLOAD_STATUS': '年度报告上传状态（0-本年度未上传 1-本年度已上传）', 'IS_OPERATE': '是否点击上传（0-否，1-是）', 'IS_HP': '是否加入主动管理（0-否，1-是）', 'WEIGHT_STATUS': '体重状态：0-未评估 1-体重偏低 2-正常 3-超重 4-肥胖 5-孕期体重增长过快', 'LATEST_CHECKUP_DATE': '最近一次体检日期', 'LATEST_WEIGHTREPORT_DATE': '最新体重管理报告日期', 'WEIGHT_EFFECTIVE': '体重管理是否有效，0-无效；1-有效', 'PERSON_USE': '是否有使用居民端，0-否 1-有', 'WEIGHT_INTERVENTION': '是否进行体重干预，0-否 1-是', 'GENERATE_REPORT': '本年度生成报告，0-否；1-是', 'PDFFILE_STATUS': '是否生成pdf文件，0-否；1-是', 'READ_STATUS': '报告是否已在居民端阅读，0-否；1-是', 'SIGNORGID': None}
# ----------------------------------------------------------------------------------------------------
# NAME = %徐东% >> HP_PERSON(主动健康管理居民表) >> 1条
# {'ID': '主键', 'NAME': '姓名', 'ID_CARD': '身份证号', 'SEX_CODE': '性别编码', 'CONNECT_PHONE': '联系电话', 'ORG_CODE': '管理机构', 'PLAN_ID': '健康管理计划ID', 'ADD_DATE': '加入日期', 'CREATE_TIME': '创建日期', 'CREATE_USER_ID': '创建人ID', 'CREATE_USER': '创建人姓名', 'MODIFIED_TIME': '更改日期', 'MODIFIED_USER_ID': '更改人ID', 'MODIFIED_USER': '更改人姓名', 'STATUS': '管理状态 0-管理中 1-退出管理', 'QUIT_DATE': '退出日期', 'QUIT_USER_ID': '退出人ID', 'QUIT_USER': '退出人姓名', 'VIP_STATUSIS_PREVIOULY_VIP': 'VIP管理状态：0-否 1-是 ', 'IS_PREVIOUSLY_VIP': '是否曾经是VIP：0-否 1-是', 'SERVICE_DOC_ID': '当前VIP服务医生用户ID', 'SERVICE_DOC_NAME': '当前VIP服务医生用户姓名'}

# r = Sqlserver_PO.select("SELECT ID, REPORT_STATUS,CATEGORY_CODE,CATEGORY_NAME,KEY_POPULATION FROM %s where JMXM='%s'" % ('QYYH', '顾利'))
# r = Sqlserver_PO.select("SELECT * FROM %s where JMXM='%s'" % ('QYYH', '顾利'))
# print(r[0])  # {'REPORT_STATUS': 2}


# Sqlserver_PO.desc({'QYYH':['REPORT_STATUS']})  # 评估状态(0:预评估；1:评估完成；2:未评估)
# 页面：待评估， 数据库：未评估
# 页面：报告待审核， 数据库：预评估
# 页面：评估完成， 数据库：评估完成
# Sqlserver_PO.desc('QYYH')

# Sqlserver_PO.record('*', 'int', '68407', False)
# Sqlserver_PO.record('IMPORTANT_CATEGORY', 'int', '68407')
# Sqlserver_PO.desc('IMPORTANT_CATEGORY')  # 重点人群编码


# Sqlserver_PO.record('*', 'varchar', u'%310110194709162023%')

# todo 儿童 - 检查 'MODEL_CODE': '005'
# 006-宝山版成人模板,008-宝山版孕妇模板,005-宝山版儿童模版,010-宝山版产妇模板,012-宝山版学生模板,014-宝山版老年人模板,T001-标准版体重模版,S014-宝山版老年人上传模板
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512492))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512515))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512531))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512534))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512551))

# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%310110195007082023%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 511776))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# ID_CARD = %310110194709162023% >> T_ASSESS_INFO(评估表) >> 2条


# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 511442))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 6, 11), 'REPORT_STATUS': 0, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': None}
# 页面：待确认，数据库：REPORT_STATUS：0 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）

# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512571))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 9, 28), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '1', 'MODEL_CODE': None}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）

# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512580))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': '005'}
# 页面：已确认，数据库：REPORT_STATUS：0 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# todo 老年人 - 检查 'MODEL_CODE': '014'
# 006-宝山版成人模板,008-宝山版孕妇模板,005-宝山版儿童模版,010-宝山版产妇模板,012-宝山版学生模板,014-宝山版老年人模板,T001-标准版体重模版,S014-宝山版老年人上传模板
# 老年人
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512455))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512457))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512458))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512472))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512490))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512514))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512530))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512549))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512555))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512574))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512576))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512581))

# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%110101195804049038%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512617))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# todo 普通人群 - 检查 'MODEL_CODE': '006'
# 006-宝山版成人模板,008-宝山版孕妇模板,005-宝山版儿童模版,010-宝山版产妇模板,012-宝山版学生模板,014-宝山版老年人模板,T001-标准版体重模版,S014-宝山版老年人上传模板
# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%130102197708161811%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 511220))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）

# todo 学生 - 检查 'MODEL_CODE': '012'
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512602))
# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%310104201109132416%')
# r = Sqlserver_PO.select("SELECT * FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512585))
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512603))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）



# todo 孕妇 - 检查 'MODEL_CODE': '008'
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512221))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512560))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512568))
# Sqlserver_PO.select("delete FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512597))

# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%310110195303082052%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512615))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# todo 产妇 - 检查 'MODEL_CODE': '010'
# Sqlserver_PO.record('T_ASSESS_INFO', 'varchar', u'%310110195303084226%')
# r = Sqlserver_PO.select("SELECT ASSESS_DATE,REPORT_STATUS,UPLOAD_STATUS,UPLOAD_DOC_ID,PDF_REPORT_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('T_ASSESS_INFO', 512616))
# print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# r = Sqlserver_PO.select("SELECT * FROM %s where ID='%s'" % ('QYYH', 68418))
# print(r[0])
#
# r = Sqlserver_PO.select("SELECT * FROM %s where ID='%s'" % ('QYYH', 68419))
# print(r[0])

# Sqlserver_PO.desc('QYYH')
# Sqlserver_PO.desc({'QYYH': 'ASSESS_ORDER'})


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Sqlserver_PO.desc('QYYH')
# Sqlserver_PO.desc('ORG_MODEL_INFO')

# todo 体重管理
# Sqlserver_PO.execute("update WEIGHT_REPORT set MODEL_CODE='T001'")
# Sqlserver_PO.desc('WEIGHT_REPORT')
Sqlserver_PO.record('WEIGHT_REPORT', 'varchar', u'%310101195507234066%')
r = Sqlserver_PO.select("SELECT PDFFILE_STATUS,MODEL_CODE FROM %s where ID='%s'" % ('WEIGHT_REPORT', 1927))
print(r[0])  # {'ASSESS_DATE': datetime.date(2025, 10, 16), 'REPORT_STATUS': 1, 'UPLOAD_STATUS': '0', 'UPLOAD_DOC_ID': None, 'PDF_REPORT_STATUS': '0', 'MODEL_CODE': ''}
# 页面：已确认，数据库：REPORT_STATUS：1 ， 报告生成状态（0-预评估，1-评估完成，2-评估中，3-评估失败(取数据)，4-评估失败(执行规则)）


# Sqlserver_PO.record('*', 'varchar', '%T002%', False)


r = Sqlserver_PO.select("SELECT WEIGHT_INTERVENTION,PDFFILE_STATUS FROM %s where SFZH='%s'" % ('QYYH', 310101195507150428))
print(r[0])






# print("7.1 查看表结构".center(100, "-"))
# Sqlserver_PO.desc()
# Sqlserver_PO.desc(['id', 'page'])
# Sqlserver_PO.desc('a_c%')
# Sqlserver_PO.desc({'a_%':['id','sql']})
# Sqlserver_PO.desc('QYYH')
# Sqlserver_PO.desc({'a_test':['number', 'rule1']})

# print("7.2 查找记录".center(100, "-"))
# Sqlserver_PO.record('t_upms_user', 'varchar', '%e10adc3949ba59abbe56e057f20f883e')  # 搜索 t_upms_user 表中内容包含 admin 的 varchar 类型记录。
# Sqlserver_PO.record('*', 'varchar', '%13710078886%', False)
# Sqlserver_PO.record('*', 'varchar', '%192.168.0.248%')
# Sqlserver_PO.record('*', 'varchar', u'%ef04737c5b4f4b93be85576e58b97ff2%')
# Sqlserver_PO.record('*', 'varchar', u'%310110194709162023%')
# Sqlserver_PO.record('*','double', u'%35%')  # 模糊搜索所有表中带35的double类型。
# Sqlserver_PO.record('*', 'datetime', u'%2019-07-17 11:19%')  # 模糊搜索所有表中带2019-01的timestamp类型。

# print("7.3 插入记录".center(100, "-"))
# Sqlserver_PO.insert("a_test", {'result': str(Fake_PO.genPhone_number('Zh_CN', 1)), 'createDate': Time_PO.getDateTimeByPeriod(0), 'ruleParam': 'param'})


# r = Sqlserver_PO.select("SELECT tags,summary,path,method,query,body FROM %s where summary='%s'" % ('a_phs_auth_app', '登录'))
# print(r[0])  # {'tags': '登录模块', 'summary': '登录', 'path': '/auth/login', 'method': 'post', 'query': None, 'body': "{'password': 'Jinhao123', 'username': '11012'}"}




