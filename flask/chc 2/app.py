# https://blog.csdn.net/qq_36545573/article/details/142639082 用户认证系统，实现登录
# https://www.sohu.com/a/788524743_121124359

from flask import Flask, render_template, jsonify, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os

# from flask_cors import *
# from tqdm import tqdm
# import settings
from flask_sqlalchemy import SQLAlchemy
# import pyodbc,time, subprocess, pymssql,
# from flask_cors import CORS
from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
# from flask_login import LoginManager
# from flask_login import UserMixin
# from flask_login import login_user, logout_user, current_user

from wtforms import SelectMultipleField, Form
from wtforms.fields import core
# from wtforms.fields import html5
from wtforms import validators

from flask import Flask, render_template
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField, FileRequired, FileAllowed

sys.path.append(os.getcwd())

from ChcRulePO import *
from PO.OpenpyxlPO import *

from PO.TimePO import *
Time_PO = TimePO()

from PO.CharPO import *
Char_PO = CharPO()

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHC", "GBK")
# Sqlserver_PO_chcconfig = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "CHCCONFIG", "GBK")

# 数据库
conn = pymssql.connect(server='192.168.0.234', user='sa', password='Zy_123456789', database='CHC')
cursor = conn.cursor()


app = Flask(__name__)
# 设置 Flask 应用的密钥，用于对 session 数据进行加密，保护敏感信息
# app.secret_key = 'jinhao' # eyJsb2dnZWRfaW4iOnRydWV9.ZwnhEw.h7glR3jzXLKlCtXxameQVGWQxnk
app.secret_key = 'eyJsb2dnZWRfaW4iOnRydWV9.ZwnhEw.h7glR3jzXLKlCtXxameQVGWQxnk'



# todo 初始化数据
# 全局字典
global_d_ = {}
# 菜单
global_d_ = {'menu': {"searchRecord": "检索记录", "queryDesc2": "查询表结构", "importCase": "导入用例", "registerTbl": "注册规则表"}}

# 不同环境使用各自icon，mac平台显示小猪，linux平台显示龙
system = os.uname().sysname
if system == 'Linux':
    global_d_['icon'] = 'dragon.ico'
else:
    global_d_['icon'] = 'pig.ico'


# 获取规则名列表
def getRuleName():
    l_ = []
    l_d_ = Sqlserver_PO.select("select * from a_ruleList")
    # print(l_d_)  # [{'ruleName': '评估因素取值', 'ruleNameTbl': 'a_jibingquzhipanduan'},...
    for d in l_d_:
        l_.append(d['ruleName'])
    return l_  # ['评估因素取值','健康干预_已患疾病单病', '健康干预_已患疾病组合','中医体质辨识']

# 添加规则名列表
def setRuleName(ruleName):
    l_ruleName = []
    l_d_ = Sqlserver_PO.select("select * from a_ruleList")
    # print(l_d_)  # [{'ruleName': '评估因素取值', 'ruleNameTbl': 'a_jibingquzhipanduan'},...
    for d in l_d_:
        l_ruleName.append(d['ruleName'])
    if ruleName not in l_ruleName:
        dboTable = Char_PO.chinese2pinyin(ruleName)
        dboTable = "a_" + dboTable
        Sqlserver_PO.execute("insert into a_ruleList (ruleName, ruleNameTbl) values('%s', '%s')" % (ruleName, dboTable))

# 规则名对应表字典
def getRuleList():
    d_ = {}
    l_d_ = Sqlserver_PO.select("select * from a_ruleList")
    # print(l_d_)  # [{'ruleName': '评估因素取值', 'ruleNameTbl': 'a_jibingquzhipanduan'},...
    for d in l_d_:
        d_[d['ruleName']] = d['ruleNameTbl']
    # print(d_)
    return d_  # {'评估因素取值': 'a_jibingquzhipanduan', '健康干预_已患疾病单病': 'a_jiankangganyu_yihuanjibingdanbing', '健康干预_已患疾病组合': 'a_jiankangganyu_yihuanjibingzuhe'}

# 获取所有规则集
def getRuleCollection():
    l_testRule = []
    l_d_ = Sqlserver_PO.select("select distinct [rule] from a_ceshiguize")
    for d in l_d_:
        l_testRule.append(d['rule'])
    # print(l_testRule)  # ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7'...
    return l_testRule
    # global_d_['rule'] = getRuleCollection()

# global_d_['ruleName'] = getRuleName()
# global_d_['rule'] = getRuleCollection()

# ---------------------------------------------------------------------------------------------------------------------


# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/getcookie',methods=['POST','GET'])
# def getcookie():
#     if request.method=='POST':          #请求类型为POST
#         username=request.form['username']   #获取请求中的username
#         response = redirect(url_for('index'))   #重定向到index路由中，并返回响应对象
#         response.set_cookie('username',str(username),max_age=18000) #设置cookie值及属性
#         return response

# # todo 1 pin
# @app.route('/')
# def homepage():
#     return render_template('index6.html', global_d_=global_d_)
#     # return render_template('pin.html', global_d_=global_d_)

# from wtforms import Form, SelectMultipleField, SubmitField
# from wtforms.fields import core
# from wtforms.widgets import html5
#
# class MultiSelectForm(Form):
#     # 定义一个SelectMultipleField字段
#     options = [('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3')]
#     select = SelectMultipleField('Choose Options', choices=options, widget=html5.Select())
#     submit = SubmitField('Submit')



@app.route('/')
def index():
    global_d_['ruleName'] = getRuleName()
    global_d_['rule'] = getRuleCollection()

    return render_template('index.html', global_d_=global_d_)

    # username = request.cookies.get('username',None)     #获取cookie值
    # if username!=None:
    #     return render_template('index.html', global_d_=global_d_,username=username)
        # return render_template('logout.html',username=username) #渲染logout.html到网页中并传递username值
    # else:
    #     return render_template('logout.html')

# # todo 2 index
# @app.route('/')
# def index():
#     # session_value = request.cookies.get('session')
#     # print(session_value)
#     # if session_value == "jinhao":
#     # if session_value == "eyJsb2dnZWRfaW4iOnRydWV9.ZwnhEw.h7glR3jzXLKlCtXxameQVGWQxnk":
#         return render_template('index.html', global_d_=global_d_)
#         # return render_template('index.html', l_ruleName=l_ruleName, queryRuleCollection=l_testRule, queryErrorRuleId=l_ruleName, d_=global_d_)
#     # else:
#     #     return render_template('pin.html', global_d_=global_d_)


# todo index 1 查询规则集
@app.route('/get_queryRuleCollection')
def get_queryRuleCollection():
    selected_value = request.args.get('value')
    cursor.execute("select [sql] from a_ceshiguize where [rule]='%s'" % selected_value)
    rows = cursor.fetchall()
    data = ""
    # data = data + rows[0][0] + "\n\n"
    for row in rows:
        data = data + str(row[0]) + "\n"
    # print(data)
    response_data = {
        'text': data
    }
    return jsonify(response_data)


# todo index 1 及联规则集
@app.route('/get_queryRuleName')
def get_queryRuleName():
    ruleName = request.args.get('value')
    print(ruleName)
    # 获取测试规则
    cursor.execute("select distinct [rule] from a_ceshiguize where ruleName='%s'" %(ruleName))
    l_t_rows = cursor.fetchall()
    l_testRule = []
    for i in l_t_rows:
        l_testRule.append(i[0])
    print(l_testRule)
    return l_testRule

# todo index 2 更新规则集
@app.route('/updateRuleCollection', methods=['POST'])
def updateRuleCollection():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        ruleCollection = request.form['ruleCollection']
        sql = request.form['sql']
        print(ruleName,ruleCollection)

        if ruleCollection != '' and sql != '':
            l_ = sql.split("\n")
            l2 = [i.replace('\r', '') for i in l_]
            l3 = [i.strip() for i in l2 if i != '']
            # print(l3)  # ['jinhao', 'yoyo', '///', 'titi']

            cursor.execute("select count([rule]) as [rule] from a_ceshiguize where [rule]='%s'" % (ruleCollection))
            l_t_count = cursor.fetchall()
            # print(l_t_count[0][0])
            if l_t_count[0][0] != 0:
                sql = sql.replace("'", "''")

            if l_t_count[0][0] == 0:
                for index, sql in enumerate(l3, start=1):
                    sql = sql.replace("'", "''").replace("\r", "")
                    cursor.execute("insert into a_ceshiguize(ruleName,[rule],[seq],sql) values ('%s','%s',%s,'%s')" % (ruleName,ruleCollection, index, sql))
                    conn.commit()
            else:
                cursor.execute("delete from a_ceshiguize where [rule]='%s'" % (ruleCollection))
                for index, sql in enumerate(l3, start=1):
                    cursor.execute("insert into a_ceshiguize(ruleName,[rule],[seq],sql) values ('%s','%s',%s,'%s')" % (ruleName,ruleCollection, index, sql))
                    conn.commit()

            # 获取更新后的规则集
            cursor.execute("select distinct [rule] from a_ceshiguize")
            l_t_rows = cursor.fetchall()
            # print(l_t_rows)
            l_testRule1 = []
            for i in l_t_rows:
                l_testRule1.append(i[0])
            return render_template('index.html', global_d_=global_d_)
            # return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule1, queryErrorRuleId=l_ruleName, system=system)
        else:
            return render_template('index.html', global_d_=global_d_, output_testRule3='error，规则集或步骤不能为空！')


# todo index 3 测试
@app.route('/testRule', methods=['POST'])
def testRule():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        id = request.form['id']
        print(ruleName, id)
    if id != '':
        try:
            r = ChcRulePO(ruleName)
            r.runId([id])
            # subprocess.run(['python3', './cli_chcRule_flask.py', ruleName, id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            l_d_all = _getRecordById(ruleName,id)
            l_d_all[0]['ruleName'] = ruleName

            # 获取测试规则
            l_testRule = []
            cursor.execute("select distinct [rule] from a_ceshiguize where ruleName='%s'" % (ruleName))
            l_t_rows = cursor.fetchall()
            for i in l_t_rows:
                l_testRule.append(i[0])
            global_d_['rule'] = l_testRule

            # 从step步骤中获取表名
            # print(l_d_all[0]['step'])
            l_tableName = re.findall(r"from\s(\w+)\swhere", l_d_all[0]['step'], re.I)
            # print(l_tableName)  # ['TB_PREGNANT_MAIN_INFO', 'T_ASSESS_MATERNAL']
            # 获取表结构
            d_tblByStep = {}
            for i in l_tableName:
                s_desc = Sqlserver_PO.desc2(i)
                d_tblByStep[i] = s_desc
            global_d_['tblByStep'] = d_tblByStep

            return render_template('edit123.html', global_d_=global_d_, d_field=l_d_all[0], s_rule=l_d_all[0]['rule'], id=id, ruleName=ruleName)
            # return render_template('edit123.html', d_field=d_, debugRuleParam_testRule=l_testRule,queryRuleCollection=l_testRule,s_rule=d_['rule'],id=d_['id'],ruleName=d_['ruleName'],d_tbl=d_tbl, system=system)
        except:
            return render_template('index.html', global_d_=global_d_, output_testRule='error，非法id！')
    else:
        return render_template('index.html', global_d_=global_d_, output_testRule='error，id不能为空！')


def _getRecord(ruleName):

    # 获取所有记录

    d_ruleName_tbl = getRuleList()

    l_field = []
    l_d_all = []
    # 获取字段列表
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % (d_ruleName_tbl[ruleName]))
    l_t_field = cursor.fetchall()
    for i in l_t_field:
        l_field.append(i[0])
    # 获取所有值
    cursor.execute("select * from %s where [rule] != ''" % (d_ruleName_tbl[ruleName]))
    l_t_value = cursor.fetchall()
    for i, l_v in enumerate(l_t_value):
        # 将字段呢值None改为空
        l_tmp = []
        for j in l_v:
            if j == None:
                j = ''
            l_tmp.append(j)
        t_value = tuple(l_tmp)
        d_ = dict(zip(l_field, list(t_value)))
        l_d_all.append(d_)
    # print(123, l_d_all)

    # cursor.execute("select DISTINCT [rule] from %s where [rule] != ''" % (d_ruleName_tbl[ruleName]))
    # l_t_rule = cursor.fetchall()
    # print(l_t_rule)  # [('s3',), ('s4',), ('s5',)]

    return l_d_all

# todo index 4 规则名列表
@app.route('/list123/<ruleName>')
def list123(ruleName):
    # session_value = request.cookies.get('session')
    # if session_value == "jinhao":
    # if session_value == "eyJsb2dnZWRfaW4iOnRydWV9.ZwnhEw.h7glR3jzXLKlCtXxameQVGWQxnk":

    d_ruleName_tbl = getRuleList()

    # 获取规则集（去重）的步骤列表 = l_ruleSql
    s = ''
    cursor.execute("select DISTINCT [rule] from %s where [rule] != ''" % (d_ruleName_tbl[ruleName]))
    l_t_rule = cursor.fetchall()
    # print(l_t_rule)  # [('s3',), ('s4',), ('s5',)]
    c = ''
    for i in l_t_rule:
        cursor.execute("select [sql] from a_ceshiguize where [rule]='%s'" % (i[0]))
        l_t_sql = cursor.fetchall()
        # print(l_t_sql)  # [("select GUID from TB_EMPI_INDEX_ROOT where IDCARDNO = '32070719470820374X'",), ("delete from TB_DC_CHRONIC_MAIN where EMPIGUID = '{GUID}'",),
        s = ' =>'
        for index, j in enumerate(l_t_sql, start=1):
            s = s + '<br>' + str(index) + ", " + j[0]
        c = c + '<br>' + i[0] + s + '<br>'
    # print(c)

    # 重构表格标题
    # 获取字典{字段:注释}
    d_field_comment = Sqlserver_PO.getFieldComment(d_ruleName_tbl[ruleName])
    # print(d_field_comment)  # {'result': '结果', 'updateDate': '更新日期', 'step': '步骤', 'rule': '规则集', 'case': '用例', 'ruleParam': '参数', 'assessName': '评估因素名称', 'assessRule': '取值规则', 'tester': '测试者', 'id': None}
    # 重新排序排序id，将id放在第一位
    if 'id' in d_field_comment:
        del d_field_comment['id']
        del d_field_comment['step']
        d_field_comment = Dict_PO.insertFirst(d_field_comment, 'id', '编号')
        print(d_field_comment)
    # 转换为{注释:宽度}
    d_tmp2 = {}
    for k,v in d_field_comment.items():
        if k == 'id':
            d_tmp2[v] = 50
        elif k == 'result':
            d_tmp2[v] = 50
        elif k == 'rule':
            d_tmp2[v] = 50
        elif k == 'case':
            d_tmp2[v] = 50
        elif k == 'priority':
            d_tmp2[v] = 50
        elif k == 'tester':
            d_tmp2[v] = 50
        elif k == 'assessRule':
            d_tmp2[v] = 300
        else:
            d_tmp2[v] = 100

    # 重构表格数据（id移到第一）
    # print(_getRecord(ruleName))
    # s_id = ''
    l_new = []
    l_d_all = (_getRecord(ruleName))
    for d_ in l_d_all:
        s_id = d_['id']
        del d_['id']
        del d_['step']
        d_ = Dict_PO.insertFirst(d_, 'id', s_id)
        l_new.append(d_)
    l_d_all = l_new
    print(l_d_all)

    return render_template('list123.html', global_d_=global_d_, d_comment_size=d_tmp2, l_d_all=l_d_all, ruleName=ruleName, l_ruleSql=c, suspend='show')

    # if ruleName == '评估因素取值':
    #     return render_template('assessFactor.html', global_d_=global_d_, d_field_comment=d_field_comment, l_d_all=l_d_all, ruleName=ruleName, l_ruleSql=c)
    # else:
    #     return render_template('healthIntervention.html', global_d_=global_d_, d_field_comment=d_field_comment, data=_getRecord(ruleName), ruleName=ruleName, l_ruleSql=c)


def _getRecordByResult(ruleName, result):

    # 通过result筛选记录 (error,ok,all)

    l_field = []
    l_d_all = []

    d_ruleName_tbl = getRuleList()

    # 获取字段列表
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % (d_ruleName_tbl[ruleName]))
    l_t_field = cursor.fetchall()
    for i in l_t_field:
        l_field.append(i[0])

    # 获取条件result的记录
    if result != 'all' :
        cursor.execute("select * from %s where result='%s'" % (d_ruleName_tbl[ruleName], result))
        l_t_value = cursor.fetchall()
        for i, l_v in enumerate(l_t_value):
            # 将None改为空
            l_tmp = []
            for j in l_v:
                if j == None:
                    j = ''
                l_tmp.append(j)
            t_value = tuple(l_tmp)
            d_ = dict(zip(l_field, list(t_value)))
            l_d_all.append(d_)
    else:
        # 获取所有值
        cursor.execute("select * from %s where [rule] != ''" % (d_ruleName_tbl[ruleName]))
        l_t_value = cursor.fetchall()
        for i, l_v in enumerate(l_t_value):
            # 将字段呢值None改为空
            l_tmp = []
            for j in l_v:
                if j == None:
                    j = ''
                l_tmp.append(j)
            t_value = tuple(l_tmp)
            d_ = dict(zip(l_field, list(t_value)))
            l_d_all.append(d_)

    return (l_d_all)

# todo 规则名列表 - 结果
@app.route('/list4/<ruleName>/<result>')
def list4(ruleName, result):
    # session_value = request.cookies.get('session')
    # if session_value == "jinhao":
    # if session_value == "eyJsb2dnZWRfaW4iOnRydWV9.ZwnhEw.h7glR3jzXLKlCtXxameQVGWQxnk":

    d_ruleName_tbl = getRuleList()

    # 获取规则集（去重）的步骤列表 = l_ruleSql
    s = ''
    cursor.execute("select DISTINCT [rule] from %s where [rule] != ''" % (d_ruleName_tbl[ruleName]))
    l_t_rule = cursor.fetchall()
    # print(l_t_rule)  # [('s3',), ('s4',), ('s5',)]
    c = ''
    for i in l_t_rule:
        cursor.execute("select [sql] from a_ceshiguize where [rule]='%s'" % (i[0]))
        l_t_sql = cursor.fetchall()
        # print(l_t_sql)  # [("select GUID from TB_EMPI_INDEX_ROOT where IDCARDNO = '32070719470820374X'",), ("delete from TB_DC_CHRONIC_MAIN where EMPIGUID = '{GUID}'",),
        s = ' =>'
        for index, j in enumerate(l_t_sql, start=1):
            s = s + '<br>' + str(index) + ", " + j[0]
        c = c + '<br>' + i[0] + s + '<br>'
    # print(c)

    # 重构表格标题
    # 获取字典{字段:注释}
    d_field_comment = Sqlserver_PO.getFieldComment(d_ruleName_tbl[ruleName])
    # print(d_field_comment)  # {'result': '结果', 'updateDate': '更新日期', 'step': '步骤', 'rule': '规则集', 'case': '用例', 'ruleParam': '参数', 'assessName': '评估因素名称', 'assessRule': '取值规则', 'tester': '测试者', 'id': None}
    # 重新排序排序id，将id放在第一位
    if 'id' in d_field_comment:
        del d_field_comment['id']
        del d_field_comment['step']
        d_field_comment = Dict_PO.insertFirst(d_field_comment, 'id', '编号')
        print(d_field_comment)
    # 转换为{注释:宽度}
    d_tmp2 = {}
    for k,v in d_field_comment.items():
        if k == 'id':
            d_tmp2[v] = 50
        elif k == 'result':
            d_tmp2[v] = 50
        elif k == 'rule':
            d_tmp2[v] = 50
        elif k == 'case':
            d_tmp2[v] = 50
        elif k == 'tester':
            d_tmp2[v] = 50
        elif k == 'priority':
            d_tmp2[v] = 50
        elif k == 'assessRule':
            d_tmp2[v] = 300
        else:
            d_tmp2[v] = 100

    # 重构表格数据（id移到第一）
    # print(_getRecord(ruleName))
    # s_id = ''
    l_new = []
    l_d_all = (_getRecordByResult(ruleName,result))
    for d_ in l_d_all:
        s_id = d_['id']
        del d_['id']
        del d_['step']
        d_ = Dict_PO.insertFirst(d_, 'id', s_id)
        l_new.append(d_)
    l_d_all = l_new
    print(l_d_all)

    return render_template('list123.html', global_d_=global_d_, d_comment_size=d_tmp2, l_d_all=l_d_all, ruleName=ruleName, l_ruleSql=c, suspend='hidden')

    # if ruleName == '评估因素取值':
    #     return render_template('assessFactor.html', global_d_=global_d_, d_field_comment=d_field_comment, l_d_all=l_d_all, ruleName=ruleName, l_ruleSql=c)
    # else:
    #     return render_template('healthIntervention.html', global_d_=global_d_, d_field_comment=d_field_comment, data=_getRecord(ruleName), ruleName=ruleName, l_ruleSql=c)

def list411(ruleName, result):

    d_ruleName_tbl = getRuleList()

    print(ruleName, result)  # 健康干预_已患疾病组合 error
    global_d_['resultStatus'] = result

    # session_value = request.cookies.get('session')
    # if session_value == "jinhao":
    # if session_value == "eyJsb2dnZWRfaW4iOnRydWV9.ZwnhEw.h7glR3jzXLKlCtXxameQVGWQxnk":

    # 获取当前表规则集（去重）的步骤列表 = l_ruleSql
    s = ''
    cursor.execute("select DISTINCT [rule] from %s where [rule] != ''" % (d_ruleName_tbl[ruleName]))
    l_t_rule = cursor.fetchall()
    # print(l_t_rule)  # [('s3',), ('s4',), ('s5',)]
    c = ''
    for i in l_t_rule:
        cursor.execute("select [sql] from a_ceshiguize where [rule]='%s'" % (i[0]))
        l_t_sql = cursor.fetchall()
        # print(l_t_sql)  # [("select GUID from TB_EMPI_INDEX_ROOT where IDCARDNO = '32070719470820374X'",), ("delete from TB_DC_CHRONIC_MAIN where EMPIGUID = '{GUID}'",),
        s = ' =>'
        for index, j in enumerate(l_t_sql, start=1):
            s = s + '<br>' + str(index) + ", " + j[0]
        c = c + '<br>' + i[0] + s + '<br>'
    # print(c)

    if ruleName == '评估因素取值':
        return render_template('assessFactor2.html', global_d_=global_d_, data=_getRecordByResult(ruleName,result), ruleName=ruleName, l_ruleSql=c)
    else:
        return render_template('healthIntervention2.html', global_d_=global_d_, data=_getRecordByResult(ruleName, result), ruleName=ruleName, l_ruleSql=c)


# todo 规则名列表 - id提交
@app.route('/submitId', methods=['POST'])
def submitId():
    l_id = request.form.getlist("items")
    l_ruleName = request.form.getlist("ruleName")
    ruleName = l_ruleName[0]
    print(ruleName, l_id)
    if l_id != []:
        for id in l_id:
            r = ChcRulePO(ruleName)
            r.runId([id])
            # subprocess.run(['python3', './cli_chcRule_flask.py', ruleName, id], stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
            l_d_all = _getRecord(ruleName)
    return ruleName

# todo 规则名列表 - 结果 - 提交
@app.route('/submit4', methods=['POST'])
def submit4():
    l_id = request.form.getlist("id")
    l_ruleName = request.form.getlist("ruleName")
    l_result = request.form.getlist("result")
    ruleName = l_ruleName[0]
    print(ruleName, l_id, l_result[0])
    if l_id != []:
        for id in l_id:
            r = ChcRulePO(ruleName)
            r.runId([id])
            # subprocess.run(['python3', './cli_chcRule_flask.py', ruleName, id], stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
            l_d_all = _getRecord(ruleName)
    tmp = ruleName + "/" + l_result[0]
    return tmp

def _getRecordById(ruleName, id):

    # 获取一行记录数据

    d_ruleName_tbl = getRuleList()

    l_field = []
    l_d_all = []
    # 获取字段列表
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % (d_ruleName_tbl[ruleName]))
    l_t_field = cursor.fetchall()
    for i in l_t_field:
        l_field.append(i[0])
    # 获取所有值
    cursor.execute("select * from %s where id=%s" % (d_ruleName_tbl[ruleName], id))
    l_t_value = cursor.fetchall()
    for i, l_v in enumerate(l_t_value):
        # 将字段呢值None改为空
        l_tmp = []
        for j in l_v:
            if j == None:
                j = ''
            l_tmp.append(j)
        t_value = tuple(l_tmp)
        d_ = dict(zip(l_field, list(t_value)))
        l_d_all.append(d_)
    return l_d_all

# todo edit123 
@app.route('/edit123')
def edit123():
    ruleName = request.args.get('ruleName')
    id = request.args.get('id')
    print(ruleName, id)
    l_d_all = _getRecordById(ruleName,id)
    print(l_d_all)
    if l_d_all[0]['case'] != 'negative':
        l_d_all[0]['case'] = '正向用例'
    else:
        l_d_all[0]['case'] = 'negative'
    if l_d_all[0]['ruleParam'] == None:
        l_d_all[0]['ruleParam'] = ''
    l_d_all[0]['ruleName'] = ruleName

    # 获取测试规则
    l_testRule = []
    cursor.execute("select distinct [rule] from a_ceshiguize where ruleName='%s'" % (ruleName))
    l_t_rows = cursor.fetchall()
    for i in l_t_rows:
        l_testRule.append(i[0])
    global_d_['rule'] = l_testRule
    print(l_testRule)

    # 从step步骤中获取表名
    # print(l_d_all[0]['step'])
    l_tableName = re.findall(r"from\s(\w+)\swhere", l_d_all[0]['step'], re.I)
    # print(l_tableName)  # ['TB_PREGNANT_MAIN_INFO', 'T_ASSESS_MATERNAL']
    # 获取表结构
    d_tbl = {}
    for i in l_tableName:
        s_desc = Sqlserver_PO.desc2(i)
        d_tbl[i] = s_desc
    global_d_['tblByStep'] = d_tbl
    return render_template('edit123.html', global_d_=global_d_, d_field=l_d_all[0], s_rule=l_d_all[0]['rule'], id=id, ruleName=ruleName)


# todo edit123，查询sql
@app.route("/get_queryRecord", methods=["POST"])
def get_queryRecord():
    querySql = request.form.get("querySql")
    querySql = querySql.replace("SELECT ","select ").replace("WHERE ","where ")
    data = ""
    if 'select ' not in querySql :
        data = 'error，非查询语句！'
        # print('error，非查询语句！')
        # sys.exit(0)
    else:
        if 'where ' not in querySql:
            data = 'error，缺少where条件！'
            # print('error，缺少where条件！')
            # sys.exit(0)
        else:
            cursor.execute(querySql)
            rows = cursor.fetchall()
            for row in rows:
                data = data + str(row)
                # data = data + str(row) + "<br>"
            print(data)
    return data


# todo edit123，编辑规则
@app.route('/step', methods=['POST'])
def step():
    if request.method == 'POST':

        d_ruleName_tbl = getRuleList()
        d_ = {}
        d_['ruleName'] = request.form['ruleName']
        d_['id'] = request.form['id']
        d_['rule'] = request.form['rule']
        d_['case'] = request.form['case']
        d_['ruleParam'] = request.form['ruleParam']
        print(d_['ruleName'],d_['id'],d_['rule'],d_['case'],d_['ruleParam'])
        # print(ruleName, id, rule, case, ruleParam)  # 健康干预_已患疾病单病 1 s1 {'VISITTYPECODE':'31','DIAGNOSIS_CODE':'G46'}
        d_['ruleParam'] = d_['ruleParam'].replace("'","''").replace("\r","")
        # ruleParam = ruleParam.replace("\r","")
        # ruleParam = ruleParam.replace('&apos;', "'").replace("\r","")
        cursor.execute("update %s set [rule]='%s',[case]='%s',ruleParam='%s' where id = %s" % (d_ruleName_tbl[d_['ruleName']], d_['rule'], d_['case'], d_['ruleParam'], d_['id']))
        conn.commit()
        d_['ruleParam'] = d_['ruleParam'].replace("''", "'")
        r = ChcRulePO(d_['ruleName'])
        r.runId([d_['id']])
        # subprocess.run(['python3', './cli_chcRule_flask.py', d_['ruleName'], d_['id']], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        cursor.execute("select result,step from %s where id = %s" % (d_ruleName_tbl[d_['ruleName']], d_['id']))
        rows = cursor.fetchall()
        d_["result"] = rows[0][0]
        d_["step"] = rows[0][1]

        # 获取测试规则
        l_testRule = []
        cursor.execute("select distinct [rule] from a_ceshiguize where ruleName='%s'" % (d_['ruleName']))
        l_t_rows = cursor.fetchall()
        for i in l_t_rows:
            l_testRule.append(i[0])
        global_d_['rule'] = l_testRule

        # 从step步骤中获取表名
        # print(l_d_all[0]['step'])
        l_tableName = re.findall(r"from\s(\w+)\swhere", d_["step"], re.I)
        print(l_tableName)  # ['TB_PREGNANT_MAIN_INFO', 'T_ASSESS_MATERNAL']
        # 获取表结构
        d_tbl = {}
        for i in l_tableName:
            s_desc = Sqlserver_PO.desc2(i)
            d_tbl[i] = s_desc
        global_d_['tblByStep'] = d_tbl
        return render_template('edit123.html', global_d_=global_d_, d_field=d_, s_rule=d_['rule'], id=d_['id'], ruleName=d_['ruleName'])



# todo 全局检索
@app.route('/searchRecord', methods=['GET','POST'])
def searchRecord():
    if request.method == 'POST':
        db = request.form['db']
        datatype = request.form['datatype']
        text = request.form['text']
        filterTbl = request.form['filterTbl']
        l_filterTbl = filterTbl.split(",")
        print(db,datatype,text,l_filterTbl)
        Sqlserver_PO2 = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", db, "GBK")
        print(db)
        s = Sqlserver_PO2.record2('*', datatype, text, l_filterTbl)
        print(s)
        global_d_['db'] = db
        global_d_['datatype'] = datatype
        global_d_['text'] = text
        global_d_['filterTbl'] = filterTbl
        return render_template('searchRecord.html', global_d_=global_d_, result=s)
    return render_template('searchRecord.html', global_d_=global_d_)


# todo 查询表结构
@app.route('/queryDesc2')
def queryDesc2():
    return render_template('queryDesc2.html', global_d_=global_d_)
@app.route('/get_queryDesc2')
def get_queryDesc2():
    selected_value = request.args.get('value')
    print(selected_value)
    Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", selected_value, "GBK")
    l_tableName = Sqlserver_PO.getTables()
    print(l_tableName)  # ['condition_item', 'patient_demographics', 'patient_diagnosis' ...
    # 获取表结构
    d_tbl_desc2 = {}
    for i in l_tableName:
        s_desc = Sqlserver_PO.desc2(i)
        d_tbl_desc2[i] = s_desc
    print(d_tbl_desc2)
    return d_tbl_desc2


def uploadFile(html):
    # 上传文件
    if 'file' not in request.files:
        return 0
    file = request.files['file']
    # print(file.filename)
    if file.filename == '':
        return 0
    filepath = os.path.dirname(os.path.abspath(__file__))  # 获取当前项目的文件路径
    savepath = os.path.join(filepath)  # 设置保存文件路径
    file.save(os.path.join(savepath, file.filename))
    # 文件改名
    file1 = savepath + "/" + file.filename
    file2 = savepath + "/chcRuleCase1.11.xlsx"
    os.rename(file1, file2)
    global_d_['file2'] = file2
    return 1


# todo 更新用例
@app.route('/importCase',methods=['GET','POST'])
def importCase():
    message = 2
    if request.method == 'POST':
        message = uploadFile('importCase.html')
        print(message)
        if message == 0:
            return render_template('importCase.html', global_d_=global_d_, message=0)
        # 导入用例
        ruleName = request.form['ruleName']
        print(ruleName)
        if ruleName in global_d_['ruleName'] and ruleName != "none":
            ChcRule_PO = ChcRulePO()
            status = ChcRule_PO.importFull(ruleName)
            if status == 1:
                return render_template('importCase.html', global_d_=global_d_, message=1)
            else:
                return render_template('importCase.html', global_d_=global_d_, message=0)
        else:
            return render_template('importCase.html', global_d_=global_d_, message=0)

    return render_template('importCase.html', global_d_=global_d_, message=message)

def getRuleNameBySheet(file2):
    # 读取excel所有sheetName，去掉global_d_['ruleName']中的，再检查表格中应包含result updateDate step rule case ruleParam
    Openpyxl_PO = OpenpyxlPO(file2)
    l_sheet = Openpyxl_PO.getSheets()
    print(l_sheet)
    l_tmp = []
    for i in l_sheet:
        print(i, Openpyxl_PO.getOneRow(1, varSheet=i))
        l_title = (Openpyxl_PO.getOneRow(1, varSheet=i))
        if len(l_title) > 6:
            if l_title[0] == 'result' and l_title[1] == 'updateDate' and l_title[2] == 'step' and l_title[
                3] == 'rule' and l_title[4] == 'case' and l_title[5] == 'ruleParam':
                l_tmp.append(i)
    print(l_tmp)
    return l_tmp

# todo 注册规则表1
@app.route('/registerTbl',methods=['GET','POST'])
def registerTbl():
    message = 2
    if request.method == 'POST':
        message = uploadFile('registerTbl.html')
        if message != 0:
            l_tmp = getRuleNameBySheet(global_d_['file2'])
            return render_template('registerTbl2.html', global_d_=global_d_, l_canRegisterRuleName = l_tmp, message=2)
        else:
            return render_template('registerTbl.html', global_d_=global_d_, message=message)

    return render_template('registerTbl.html', global_d_=global_d_, message=message)

# todo 注册规则表2
@app.route('/registerTbl2',methods=['GET','POST'])
def registerTbl2():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        print(ruleName)
        if ruleName == 'none':
            return render_template('registerTbl.html', global_d_=global_d_, message=0)
        else:
            ChcRule_PO = ChcRulePO()
            status = ChcRule_PO.importFull(ruleName)
            setRuleName(ruleName)
            l_tmp = getRuleNameBySheet(global_d_['file2'])
            if status == 1:
                return render_template('registerTbl2.html', global_d_=global_d_, message=1, l_canRegisterRuleName = l_tmp)
            else:
                return render_template('registerTbl2.html', global_d_=global_d_, message=0, l_canRegisterRuleName = l_tmp)

    return render_template('registerTbl2.html',global_d_=global_d_, message=2)



# todo 测试多下拉框
@app.route('/testSelect',methods=['GET','POST'])
def testSelect():
    if request.method == 'POST':
        ruleName = request.form.getlist('ruleName')
        print(ruleName)
    return render_template('testSelect.html', global_d_=global_d_)


# todo 测试列表页升降序
@app.route('/testSort',methods=['GET','POST'])
def testSort():
    # 假设的数据列表
    items = ['apple', 'banana', 'cherry']
    sort_order = request.args.get('sort', 'asc')
    if sort_order == 'asc':
        items.sort()  # 升序排序
    elif sort_order == 'desc':
        items.sort(reverse=True)  # 降序排序
    return render_template('testSort.html', items=items, sort_order=sort_order, global_d_=global_d_)




from flask_wtf import FlaskForm, RecaptchaField, CSRFProtect
# todo 验证码
# https://www.jianshu.com/p/57b564efcb7b
# https://blog.csdn.net/wggglggg/article/details/116231552
class Myform2(FlaskForm):
    recaptcha = RecaptchaField()    #验证码字段
@app.route('/yanzm')
def yanzm():
    myform=Myform2()         #创建表单对象
    return render_template('yanzm.html', myform=myform)     #使用render_template()方法渲染yanzm.html文件并将myform传递到file.html中

# todo 上传文件
# https://www.jianshu.com/p/57b564efcb7b

# todo Flask框架——模型关系（1对多）
# https://www.jianshu.com/p/aa280be2991f

# todo Flask框架——数据库操作（增删改查）
# https://www.jianshu.com/p/7330eed5a865

# todo Flask框架——数据库配置及迁移同步
# https://www.jianshu.com/p/6f445603af2c

# todo Flask框架——蓝图、flask-script
# https://www.jianshu.com/p/de9d269181a2

# todo Flask框架——Session与Cookie
# https://www.jianshu.com/p/36fb6f874f0e

# todo Flask框架——flask-caching缓存
# https://www.jianshu.com/p/c220eddc0358

# todo Flask框架——消息闪现
# https://www.jianshu.com/p/aa09df69480b

# todo 发邮件
# https://www.jianshu.com/p/df0a83fc71b5

# todo SQLite
# https://www.jianshu.com/p/0db917eb8bd9

# todo Flask框架——Sijax
# https://www.jianshu.com/p/5f656555bef2

# todo Flask框架——项目可安装化
# https://www.jianshu.com/p/b608cc906f1a

# todo Flask框架——基于类视图
# https://www.jianshu.com/p/df59d86c3985

# todo Flask框架——应用错误处理
# https://www.jianshu.com/p/712cc9b9eff0

# todo Flask框架——Bootstrap-Flask使用
# https://www.jianshu.com/p/746c126eb251

# todo Flask框架——MongoEngine使用MongoDB
# https://www.jianshu.com/p/5316498393e9

# todo Flask框架——基于Celery的后台任务
# https://www.jianshu.com/p/5b4459e9f3b0


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True)  # 开发服务器，适用于开发和测试
    # os.system("/Users/linghuchong/miniconda3/envs/py308/bin/python -m flask run --host=0.0.0.0 --port=5001")
