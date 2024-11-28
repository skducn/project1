# https://blog.csdn.net/qq_36545573/article/details/142639082 用户认证系统，实现登录
# https://www.sohu.com/a/788524743_121124359
# lsof -i :5000
# sudo ss -tulnp | grep ':5000'
# python3 app.py run -h 0.0.0.0 --debug=false


from flask import Flask, render_template, jsonify, redirect, url_for, flash, session, request, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
from flask_caching import Cache

# from flask_cors import *
# from tqdm import tqdm
# import settings
# from flask_sqlalchemy import SQLAlchemy
# import pyodbc,time, subprocess, pymssql,
# from flask_cors import CORS
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from apscheduler.schedulers.background import BackgroundScheduler
# from flask_login import LoginManager
# from flask_login import UserMixin
# from flask_login import login_user, logout_user, current_user

# from wtforms import SelectMultipleField, Form
# from wtforms.fields import core
# # from wtforms.fields import html5
# from wtforms import validators

from flask import Flask, render_template
# from flask_wtf import FlaskForm, CSRFProtect
# from flask_wtf.file import FileField, FileRequired, FileAllowed


sys.path.append(os.getcwd())

from ChcRulePO import *
from OpenpyxlPO import *

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


from PO.LogPO import *
# _path = os.path.dirname(__file__)  # 获取当前文件路径
Log_PO = LogPO('nohup.out',level="debug")

import os, datetime, sys
from datetime import date, datetime, timedelta
from fabric import Connection, task
# 建议将ssh连接所需参数变量化
user = 'root'
host = '192.168.0.243'
password = 'Benetech79$#-'
c = Connection(host=f'{user}@{host}',connect_kwargs=dict(password=password))

@task
def copy_directory(local_path, remote_path):
    with Connection(host, user=user, connect_kwargs={"password": 'Benetech79$#-'}) as conn:
        conn.put(local_path=local_path, remote_path=remote_path, recursive=True)





# 创建方法生成日志
def generation_log():
    for i in range(20):
        # Log_PO.info(i)
        Log_PO.logger.info(i)
        time.sleep(1)


# 读取日志并返回
def red_logs():
    # log_path = f'{_path}/log.log'  # 获取日志文件路径
    log_path = f'nohup.out'  # 获取日志文件路径
    with open(log_path, 'rb') as f:
        # log_size = os.path.getsize(log_path)  # 获取日志大小
        log_size = 100
        offset = -100
        # 如果文件大小为0时返回空
        if log_size == 0:
            return ''
        while True:
            # 判断offset是否大于文件字节数,是则读取所有行,并返回
            if (abs(offset) >= log_size):
                f.seek(-log_size, 2)
                data = f.readlines()
                return data
            # 游标移动倒数的字节数位置
            data = f.readlines()
            # 判断读取到的行数，如果大于1则返回最后一行，否则扩大offset
            if (len(data) > 1):
                return data
            else:
                offset *= 2


app = Flask(__name__)
# 设置 Flask 应用的密钥，用于对 session 数据进行加密，保护敏感信息
# app.secret_key = 'jinhao' # eyJsb2dnZWRfaW4iOnRydWV9.ZwnhEw.h7glR3jzXLKlCtXxameQVGWQxnk
app.secret_key = 'eyJsb2dnZWRfaW4iOnRydWV9.ZwnhEw.h7glR3jzXLKlCtXxameQVGWQxnk'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.debug =True

#
# class CDN(object):
#     def __init__(self, app=None):
#         self.app = app
#         if app is not None:
#             self.init_app(app)
#
#     def init_app(self, app):
#         # 设置静态文件的缓存控制头
#         @app.after_request
#         def add_header(response):
#             response.cache_control.max_age = 3600  # 设置缓存时间为1小时（3600秒）
#             return response
#
#
# # 初始化CDN
# cdn = CDN(app)



line_number = [0] #存放当前日志行数
# 定义接口把处理日志并返回到前端
@app.route('/get_log',methods=['GET','POST'])
def get_log():
    log_data = red_logs() # 获取日志
    # 判断如果此次获取日志行数减去上一次获取日志行数大于0，代表获取到新的日志
    if len(log_data) - line_number[0] > 0:
        log_type = 2 # 当前获取到日志
        log_difference = len(log_data) - line_number[0] # 计算获取到少行新日志
        log_list = [] # 存放获取到的新日志
        # 遍历获取到的新日志存放到log_list中
        for i in range(log_difference):
            log_i = log_data[-(i+1)].decode('utf-8') # 遍历每一条日志并解码
            log_list.insert(0,log_i) # 将获取的日志存放log_list中
    else:
        log_type = 3
        log_list = ''
    # 已字典形式返回前端
    _log = {
        'log_type' : log_type,
        'log_list' : log_list
    }
    line_number.pop() # 删除上一次获取行数
    line_number.append(len(log_data)) # 添加此次获取行数
    return _log

# 通过前端请求执行生成日志方法
@app.route('/generation_log',methods=['GET','POST'])
def generation_log_():
    if request.method == 'POST':
        generation_log()
    return ''

@app.route('/seeLog',methods=['GET','POST'])
def seeLog():
    if request.method == 'GET':
        return render_template('seeLog.html')
    if request.method == 'POST':
        return render_template('seeLog.html')

# todo 初始化数据
# 全局字典菜单
global_d_ = {'menu': {"searchRecord": "查询记录", "queryDesc2": "查询表结构", "importCase": "导入规则", "registerTbl": "创建库表", "updateFile": "更新文件","queryLog": "查询日志"}}




# 不同环境使用各自icon，mac平台显示小猪，linux平台显示龙
system = os.uname().sysname
if system == 'Linux':
    global_d_['icon'] = 'dragon.ico'
    global_d_['downloadFile'] = 'chcRuleCase.xlsx'

else:
    global_d_['downloadFile'] = '/Users/linghuchong/Downloads/51/Python/project/flask/chc/chcRuleCase.xlsx'
    global_d_['icon'] = 'pig.ico'


@app.route("/download")
def download():
    return send_file(global_d_['downloadFile'], as_attachment=True)
    # return send_file('https://192.168.0.243:5000/home/flask_chc/chcRuleCase.xlsx', as_attachment=True)
    # return send_file('/Users/linghuchong/Downloads/51/Python/project/flask/chc/chcRuleCase.xlsx', as_attachment=True)


# 获取规则名列表
def getRuleName():
    l_ = []
    l_d_ = Sqlserver_PO.select("select * from a_ruleList")
    print(l_d_)  # [{'ruleName': '评估因素取值', 'ruleNameTbl': 'a_jibingquzhipanduan'},...
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
@app.route('/pin')
def pin():
    # return render_template('index6.html', global_d_=global_d_)
    return render_template('pin.html', global_d_=global_d_)

# from wtforms import Form, SelectMultipleField, SubmitField
# from wtforms.fields import core
# from wtforms.widgets import html5
#
# class MultiSelectForm(Form):
#     # 定义一个SelectMultipleField字段
#     options = [('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3')]
#     select = SelectMultipleField('Choose Options', choices=options, widget=html5.Select())
#     submit = SubmitField('Submit')


@app.route('/index123')
def index123():
    # return redirect('123.html')
    return render_template('123.html')



@app.route('/index7')
def index7():
    global_d_['ruleName'] = getRuleName()
    print(global_d_)
    global_d_['rule'] = getRuleCollection()
    # return render_template('index7.html', global_d_=global_d_, tabName='查询规则集', subName=1)
    return render_template('index7.html', global_d_=global_d_, tabName='测试项', subName=1, message=-1)

@app.route('/')
def index():
    global_d_['ruleName'] = getRuleName()
    print("(289)global_d_['ruleName'] => ", global_d_['ruleName'])
    global_d_['rule'] = getRuleCollection()

    # return render_template('index.html', global_d_=global_d_)
    return render_template('index7.html', global_d_=global_d_, tabName='测试项', subName=1, message=-1)

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
        print("(326)规则集 - 新建/修改 =>", ruleName,ruleCollection)
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
                    cursor.execute("insert into a_ceshiguize(ruleName,[rule],seq,sql) values ('%s','%s','%s','%s')" % (ruleName,ruleCollection, str(index), sql))
                    conn.commit()
            else:
                cursor.execute("delete from a_ceshiguize where [rule]='%s'" % (ruleCollection))
                for index, sql in enumerate(l3, start=1):
                    sql = sql.replace("'", "''").replace("\r", "")
                    cursor.execute("insert into a_ceshiguize(ruleName,[rule],seq,sql) values ('%s','%s','%s','%s')" % (ruleName,ruleCollection, str(index), sql))
                    conn.commit()

            # 获取更新后的规则集
            cursor.execute("select distinct [rule] from a_ceshiguize")
            l_t_rows = cursor.fetchall()
            # print(l_t_rows)
            l_testRule1 = []
            for i in l_t_rows:
                l_testRule1.append(i[0])
            return render_template('index7.html', global_d_=global_d_, tabName='数据源', subName='查询规则集', message=1)
            # return render_template('index.html', global_d_=global_d_)
            # return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule1, queryErrorRuleId=l_ruleName, system=system)
        else:
            return render_template('index7.html', global_d_=global_d_, tabName='数据源', subName='更新规则集', message=0)
            # return render_template('index.html', global_d_=global_d_, output_testRule3='error，规则集或步骤不能为空！')


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

            # 获取表和注释字典
            # d_tbl_comment = Sqlserver_PO.getTableComment()
            # print(d_tbl_comment)  # {'SYS_ABI_CONFIG': None, 'SYS_CITY': '城市字典表',

            # 获取表结构
            d_tbl_desc2 = {}
            d_tbl_comment = {}
            for i in l_tableName:
                s_desc = Sqlserver_PO.desc2(i)
                d_tbl_desc2[i] = s_desc
                d_tbl_comment.update(Sqlserver_PO.getTableComment(i))

            d_tbl_desc2['tblComment'] = d_tbl_comment
            global_d_['tblByStep'] = d_tbl_desc2
            print("global_d_['tblByStep'] => ", global_d_['tblByStep'])

            return render_template('index7.html', global_d_=global_d_, d_field=l_d_all[0], s_rule=l_d_all[0]['rule'], tabName='测试项',subName='测试规则', testRule2=1, message=2)
            # return render_template('edit123.html', global_d_=global_d_, d_field=l_d_all[0], s_rule=l_d_all[0]['rule'], id=id, ruleName=ruleName)
            # return render_template('edit123.html', d_field=d_, debugRuleParam_testRule=l_testRule,queryRuleCollection=l_testRule,s_rule=d_['rule'],id=d_['id'],ruleName=d_['ruleName'],d_tbl=d_tbl, system=system)
        except:
            return render_template('index7.html', global_d_=global_d_, tabName='测试项',subName='测试规则', testRule2=1, message=0)
            # return render_template('index.html', global_d_=global_d_, output_testRule='error，非法id！')
    else:
        return render_template('index7.html', global_d_=global_d_, tabName='测试项',subName='测试规则', testRule2=1, message=0)
        # return render_template('index7.html', global_d_=global_d_, output_testRule='error，id不能为空！')


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
    d_field_comment = Sqlserver_PO.getFieldCommentGBK(d_ruleName_tbl[ruleName])
    print(504, d_field_comment)
    # print(d_field_comment)  # {'result': '结果', 'updateDate': '更新日期', 'step': '步骤', 'rule': '规则集', 'case': '用例', 'ruleParam': '参数', 'assessName': '评估因素名称', 'assessRule': '取值规则', 'tester': '测试者', 'id': None}
    # 重新排序排序id，将id放在第一位
    if 'id' in d_field_comment:
        del d_field_comment['id']
        del d_field_comment['step']
        d_field_comment = Dict_PO.insertFirst(d_field_comment, 'id', '编号')
        print("(527)规则名列表 - ", ruleName, " => ", d_field_comment)
    # 转换为{注释:宽度}
    d_tmp2 = {}
    for k, v in d_field_comment.items():
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
    # print(l_d_all)


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
    d_field_comment = Sqlserver_PO.getFieldCommentGBK(d_ruleName_tbl[ruleName])
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
    print("(733)",ruleName, l_id)

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
    print("l_testRule => ", l_testRule)

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
    print("global_d_['tblByStep'] => ", global_d_['tblByStep'])
    l_tbl = list(global_d_['tblByStep'].keys())

    print("d_field['step'] => ", l_d_all[0]['step'])
    l_step = l_d_all[0]['step'].split("\n")
    print("l_step => ", l_step)
    print("l_tbl => ", l_tbl)

    # 获取表和注释字典
    d_tbl_comment = Sqlserver_PO.getTableComment()
    print("d_tbl_comment => ", d_tbl_comment)

    return render_template('edit123.html', global_d_=global_d_, d_field=l_d_all[0], s_rule=l_d_all[0]['rule'], id=id, ruleName=ruleName, l_step=l_step,l_tbl=l_tbl, d_tbl_comment=d_tbl_comment)


# todo edit123，查询sql
@app.route("/get_queryRecord", methods=["POST"])
def get_queryRecord():
    querySql = request.form.get("querySql")
    querySql = querySql.replace("SELECT ", "select ").replace("WHERE ", "where ").replace("FROM ", "from ")
    if ' select ' in querySql:
        querySql = querySql.split(" select ")[1]
        querySql = "select " + querySql

        global_d_['querySQL'] = querySql.split("from ")[1].split(" where")[0]


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
            try:
                cursor.execute(querySql)
                rows = cursor.fetchall()
                for row in rows:
                    data = data + str(row)
                    # data = data + str(row) + "<br>"
                print(data)
            except:
                data = "error, 表或字段名错误！"
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
        return render_template('index7.html', global_d_=global_d_, d_field=d_, s_rule=d_['rule'], tabName='测试项', subName='测试规则',testRule2=1, message=1)
        # return render_template('edit123.html', global_d_=global_d_, d_field=d_, s_rule=d_['rule'], id=d_['id'], ruleName=d_['ruleName'])



# todo 查询记录
@app.route('/searchRecord', methods=['GET','POST'])
def searchRecord():
    if request.method == 'POST':
        db = request.form['db']
        datatype = request.form['datatype']
        text = request.form['text']
        filterTbl = request.form['filterTbl']
        l_filterTbl = filterTbl.split(",")
        print("(859)查询记录 - 参数 =>", db, datatype, text, l_filterTbl)
        Sqlserver_PO2 = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", db, "GBK")
        result = Sqlserver_PO2.record2('*', datatype, text, l_filterTbl)
        print("(862)查询记录 - 结果 =>", result)
        global_d_['db'] = db
        global_d_['datatype'] = datatype
        global_d_['text'] = text
        global_d_['filterTbl'] = filterTbl
        # return render_template('searchRecord.html', global_d_=global_d_, result=s)
        return render_template('index7.html', global_d_=global_d_, result=result, message=1, tabName='辅助工具', subName='查询记录')
    return render_template('searchRecord.html', global_d_=global_d_)


# todo 查询表结构
@app.route('/queryDesc2')
def queryDesc2():
    # return render_template('queryDesc2.html', global_d_=global_d_)
    return render_template('index7.html', global_d_=global_d_, tabName='辅助工具')
@app.route('/get_queryDesc2')
def get_queryDesc2():
    selected_value = request.args.get('value')
    print("(921)查询表结构 - 数据库 =>", selected_value)
    Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", selected_value, "GBK")

    # 获取表和注释字典
    d_tbl_comment = Sqlserver_PO.getTableComment()
    # print(d_tbl_comment)  # {'SYS_ABI_CONFIG': None, 'SYS_CITY': '城市字典表',

    # 获取表名
    l_tableName = Sqlserver_PO.getTables()
    # print(l_tableName)  # ['SYS_USER_SECURITY', 'SYS_USER_ROLE', 'SYS_CITY',  ...

    # 获取表结构
    d_tbl_desc2 = {}
    for i in l_tableName:
        s_desc = Sqlserver_PO.desc2(i)
        d_tbl_desc2[i] = s_desc
    print("d_tbl_desc2 => ", d_tbl_desc2)

    d_tbl_desc2['tblComment'] = d_tbl_comment
    return d_tbl_desc2


def uploadFile():
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
    file2 = savepath + "/chcRuleCase.xlsx"
    os.rename(file1, file2)
    global_d_['file2'] = file2
    return 1


# todo 导入用例
@app.route('/importCase',methods=['GET','POST'])
def importCase():
    message = 2
    if request.method == 'POST':
        message = uploadFile()
        print("(923)导入规则 - 上传文件 =>", message)
        if message == 0:
            return render_template('index7.html', global_d_=global_d_, message=0, tabName='数据源', subName='导入规则')
        # 导入用例
        ruleName = request.form['ruleName']
        print("(928)导入规则 - 规则名 =>", ruleName)
        if ruleName in global_d_['ruleName'] and ruleName != "none":
            ChcRule_PO = ChcRulePO()
            status = ChcRule_PO.importFull(ruleName)
            if status == 1:
                # return render_template('importCase.html', global_d_=global_d_, message=1)
                return render_template('index7.html', global_d_=global_d_, message=1, tabName='数据源', subName='导入规则')
            else:
                return render_template('index7.html', global_d_=global_d_, message=-1, tabName='数据源', subName='导入规则')
                # return render_template('importCase.html', global_d_=global_d_, message=0)
        else:
            return render_template('index7.html', global_d_=global_d_, message=0, tabName='数据源', subName='导入规则')
            # return render_template('importCase.html', global_d_=global_d_, message=0)

    # return render_template('importCase.html', global_d_=global_d_, message=message)

def getRuleNameBySheet(file2):
    # 读取excel所有sheetName，去掉global_d_['ruleName']中的，再检查表格中应包含result updateDate step rule case ruleParam
    Openpyxl_PO = OpenpyxlPO(file2)
    l_sheet = Openpyxl_PO.getSheets()
    # print(l_sheet)
    l_tmp = []
    for i in l_sheet:
        # print(i, Openpyxl_PO.getOneRow(1, varSheet=i))  # 测试规则 ['ruleName', 'rule', 'seq', 'sql']  //输出每个sheet的字段名。
        l_title = (Openpyxl_PO.getOneRow(1, varSheet=i))
        if len(l_title) > 6:
            if l_title[0] == 'result' and l_title[1] == 'updateDate' and l_title[2] == 'step' and l_title[
                3] == 'rule' and l_title[4] == 'case' and l_title[5] == 'ruleParam':
                l_tmp.append(i)
    print("(957)l_tmp(符合条件的sheet名) => ", l_tmp)
    return l_tmp

# todo 注册规则表1
@app.route('/registerTbl',methods=['GET','POST'])
def registerTbl():
    message = 2
    if request.method == 'POST':
        message = uploadFile()
        print("(966)创建库表 - 上传文件(步骤1/2)", message )
        # message = uploadFile('registerTbl.html')
        if message == 1:
            l_tmp = getRuleNameBySheet(global_d_['file2'])
            return render_template('index7.html', global_d_=global_d_, l_canRegisterRuleName=l_tmp, message=2, tabName='数据源', subName='创建库表', registerTbl2=1)
            # return render_template('registerTbl2.html', global_d_=global_d_, l_canRegisterRuleName = l_tmp, message=2)
        else:
            return render_template('index7.html', global_d_=global_d_, message=message, tabName='数据源', subName='创建库表', registerTbl2=0)
            # return render_template('registerTbl.html', global_d_=global_d_, message=message)

    # return render_template('registerTbl.html', global_d_=global_d_, message=message)

# todo 创建库表步骤2/2
@app.route('/registerTbl2',methods=['GET','POST'])
def registerTbl2():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        print("(1052)创建库表 - 规则名(步骤2/2) =>", ruleName)
        if ruleName == 'none':
            # return render_template('registerTbl.html', global_d_=global_d_, message=0)
            return render_template('index7.html', global_d_=global_d_, message=0, tabName='数据源', subName='创建库表', registerTbl2=1)
        else:
            ChcRule_PO = ChcRulePO()
            status = ChcRule_PO.importFull(ruleName)
            setRuleName(ruleName)
            l_tmp = getRuleNameBySheet(global_d_['file2'])
            print("(1061)l_tmp", l_tmp)
            if status == 1:
                return render_template('index7.html', global_d_=global_d_, l_canRegisterRuleName=l_tmp, message=1, tabName='数据源', subName='创建库表', registerTbl2=1)
                # return render_template('registerTbl2.html', global_d_=global_d_, message=1, l_canRegisterRuleName = l_tmp)
            else:
                # return render_template('registerTbl2.html', global_d_=global_d_, message=0, l_canRegisterRuleName = l_tmp)
                return render_template('index7.html', global_d_=global_d_, l_canRegisterRuleName=l_tmp, message=0, tabName='数据源', subName='创建库表', registerTbl2=1)


    # return render_template('registerTbl2.html',global_d_=global_d_, message=2)



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


# todo 自动更新文件（通过pin.html，更新当天修改过的文件）
def copyLocal2remote(s_localPath_prefix, s_remotePath_prefix, varLocalPath, varLocalFile):
    # 2,遍历本地文件，如果当天修改过则复制到服务器
    s_localPathFile = varLocalPath + "/" + varLocalFile  # '/Users/linghuchong/Downloads/51/Python/project/flask/chc/1.jpg'
    s_dateTime = datetime.fromtimestamp(os.path.getmtime(s_localPathFile))   # 获取文件日期时间
    # print(file_path, s_dateTime)  # '2023-11-15 15:56:34.431144'
    l_dateTime = str(s_dateTime).split(' ')   # ['2023-11-15', '15:56:34.431144']
    # 如果是当天日期，则复制文件到服务器
    if l_dateTime[0] == str(date.today()):
        s_del_localPathPrefix = varLocalPath.replace(s_localPath_prefix, "")
        print(s_localPathFile, " => ", s_remotePath_prefix + s_del_localPathPrefix + "/" + varLocalFile) # /Users/linghuchong/Downloads/51/Python/project/flask/chc/app.py /home/flask_chc/app.py
        c.put(s_localPathFile, s_remotePath_prefix + s_del_localPathPrefix + "/" + varLocalFile)

def getSubFolder(s_localPath, s_localPath2):
    # 获取本地指定目录下所有目录及子目录结构
    l_path_subFolder = []
    l_local_folder = []
    for entry in os.listdir(s_localPath):
        s_varPath_file = os.path.join(s_localPath, entry)
        if os.path.isdir(s_varPath_file):
            l_path_subFolder.append(s_varPath_file)
            l_path_subFolder.extend(getSubFolder(s_varPath_file, s_localPath2))  # 递归调用
    # 过滤掉前缀路径，如 /Users/linghuchong/Downloads/51/Python/project/flask/chc
    for i in l_path_subFolder:
        if ".idea" not in i:
            l_local_folder.append(i.replace(s_localPath2,""))
    return l_local_folder

def copyLocalFolder(s_local, s_remote):
    # 复制本地目录到远程目录
    a = [x for x in s_local if x in s_remote]  # 两列表交集
    return [y for y in s_local if y not in a]  # 在s_local里但不在s_remote

def delRemoteFolder(s_local, s_remote):
    # 删除远程目录及子目录文件
    a = [x for x in s_local if x in s_remote]  # 两列表交集
    return [y for y in s_remote if y not in a]  # 在s_remote里但不在s_local


@app.route('/updateSystem')
def updateSystem():
    # 遍历当前路径下所有目录和文件
    print("(1146)辅助工具 - 自动更新文件 =>")
    s_localPath_prefix = "/Users/linghuchong/Downloads/51/Python/project/flask/chc"
    s_remotePath_prefix = '/home/flask_chc'
    
    # 1,遍历本地目录与服务器目录，如果服务器上没有则复制本地目录到服务器目录（包含内部目录与文件）
    print("1, 比对/更新服务器上目录：")
    l_local_folder = getSubFolder(s_localPath_prefix, s_localPath_prefix)
    print("本地", s_localPath_prefix, "下目录结构 => ", l_local_folder)
    result = c.run(f'find {s_remotePath_prefix} \( -path "{s_remotePath_prefix}/.git" -o -path "{s_remotePath_prefix}/.idea" \) -prune -o -type d -print', hide='stdout', warn=True)
    # fabric_folder = c.run('find /home/flask_chc \( -path "/home/flask_chc/.git" -o -path "/home/flask_chc/.idea" \) -prune -o -type d -print')
    # print(type(fabric_folder))  # <class 'fabric.runners.Result'>
    # # 打印返回结果
    # print(result.stdout)  # 输出命令的标准输出
    # print(result.stderr)  # 输出命令的标准错误
    # print(result.return_code)  # 输出命令的返回码
    l_remote_folder = str(result.stdout).split("\n")
    # print("远程CHC下目录及子目录 => ", l_remote_folder)  # ['Command exited with status 0.', '=== stdout ===', '/home/flask_chc', '/home/flask_chc/__pycache__',

    l_remote_ = []
    for i in l_remote_folder:
        if f"{s_remotePath_prefix}/" in i:
            l_remote_.append(i.replace(s_remotePath_prefix, ""))
    print("远程", s_remotePath_prefix, "下目录结构2 => ", l_remote_)

    l_1 = copyLocalFolder(l_local_folder, l_remote_)
    print("复制，本地目录到远程 => ", l_1)  # ['/static/215447', '/static/708757', '/static/12', '/static/12/picture']
    for i in l_1:
        s_local_path = s_localPath_prefix + i
        s_remote_path = s_remotePath_prefix + i
        c.run(f"mkdir -p {s_remote_path}")
        for s_path, l_folder, l_file in os.walk(s_local_path):
            print(s_local_path + " => ", l_file)  # ['TableSorterV2.js', 'demo.html']
            for i in l_file:
                c.put(s_local_path + "/" + i, s_remote_path)
            break

    l_2 = delRemoteFolder(l_local_folder, l_remote_)
    print("删除，远程目录", l_2)
    for i in l_2:
        s_remote_path = s_remotePath_prefix + i
        c.run(f'rm -rf {s_remote_path}')

    # 2,遍历本地目录文件，如果当天修改过则复制到服务器
    l_local_file = []
    l_remote_file = []
    print("2，复制当天修改过的文件：")
    for s_path, l_folder, l_file in os.walk(s_localPath_prefix):
        # print(111,l_folder)
        for i in l_file:
            if i != ".DS_Store" and i != "workspace.xml":
                copyLocal2remote(s_localPath_prefix, s_remotePath_prefix, s_path, i)
                # if '/__pycache__' not in s_path and '/.idea' not in s_path and '/static' not in s_path:
                if '/__pycache__' not in s_path and '/.idea' not in s_path:
                    # print("本地文件 => ", s_path + "/" + i)
                    l_local_file.append(s_path + "/" + i)
            # l_2_fiel = delRemoteFolder(l_local_folder, l_remote_)

    print("3，遍历所有文件，更新两边的文件：")
    # r = c.run(f'find /home/flask_chc -type d \( -path "/home/flask_chc/.git" -o -path "/home/flask_chc/.idea" -o -path "/home/flask_chc/__pycache__" -o -path "/home/flask_chc/PO/__pycache__" \) -prune -o -type f -print', hide='stdout', warn=True)
    # r = c.run(f'find /home/flask_chc -type d \( -path "/home/flask_chc/.git" -o -path "/home/flask_chc/.idea" -o -path "/home/flask_chc/__pycache__" -o -path "/home/flask_chc/PO/__pycache__" -o -path "/home/flask_chc/static" \) -prune -o -type f -print', hide='stdout', warn=True)
    r = c.run(f'find /home/flask_chc -type d \( -path "/home/flask_chc/.git" -o -path "/home/flask_chc/.idea" -o -path "/home/flask_chc/__pycache__" -o -path "/home/flask_chc/PO/__pycache__" \) -prune -o -type f -print', hide='stdout', warn=True)
    # print("远程文件 => ", r.stdout)
    l_remote_file = str(r.stdout).split("\n")
    l_remote_file.pop(-1)

    print("本地文件", l_local_file)
    l_local_file2 = []
    for i in l_local_file:
        l_local_file2.append(i.replace(s_localPath_prefix, s_remotePath_prefix))
    # print("本地文件2 => ", l_local_file2)
    print("远程文件", l_remote_file)

    l_3_file = copyLocalFolder(l_local_file2, l_remote_file)
    print("复制，本地文件 => 远程文件", l_3_file)
    for i in l_3_file:
        i2 = i.replace(s_remotePath_prefix, s_localPath_prefix)
        c.put(i2, i)

    l_2_file = delRemoteFolder(l_local_file2, l_remote_file)
    print("删除，远程文件", l_2_file)
    for i in l_2_file:
        c.run(f'rm -rf {i}')


    r = c.run('cd /home/flask_chc/ && sh ./sk.sh', hide='stdout')
    # r = c.run('cd /home/flask_chc/ && nohup flask run --host=0.0.0.0 >> /home/flask_chc/log.log 0>&1 &')
    # print(r.stdout)
    # print(r.return_code)
    # return render_template('index7.html', global_d_=global_d_, message=-1, tabName='测试项', subName=1)
    sleep(5)
    return redirect("http://192.168.0.243:5000/")


# todo 查询日志
@app.route('/searchLog', methods=['POST'])
def searchLog():
    if request.method == 'POST':
        global_d_['count'] = request.form['count']
        print("(1109)辅助工具 - 查询日志 =>", global_d_['count'])
        # s = c.run('cd /home/flask_chc/ && tail -f nohup.out')
        result = c.run('cd /home/flask_chc/ && tail -n '+ global_d_['count'] +' nohup.out', hide='stdout', warn=True)
        result = str(result.stdout).replace("192.168.0.148 -", "<br>192.168.0.148 -").replace("(no stderr)", "<br>(no stderr)")

        return render_template('index7.html', global_d_=global_d_, resultSearchLog=result, message=1, tabName='系统配置', subName='查询日志')
        # return render_template('searchLog.html', global_d_=global_d_, resultSearchLog=s)
    # return render_template('index7.html', global_d_=global_d_)



# from flask_wtf import FlaskForm, RecaptchaField, CSRFProtect
# todo 验证码
# https://www.jianshu.com/p/57b564efcb7b
# https://blog.csdn.net/wggglggg/article/details/116231552
# class Myform2(FlaskForm):
#     recaptcha = RecaptchaField()    #验证码字段
# @app.route('/yanzm')
# def yanzm():
#     myform=Myform2()         #创建表单对象
#     return render_template('yanzm.html', myform=myform)     #使用render_template()方法渲染yanzm.html文件并将myform传递到file.html中

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
    # FLASK_APP=app.py && nohup flask run --host=0.0.0.0 &
