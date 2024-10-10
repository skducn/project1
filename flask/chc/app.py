# https://blog.csdn.net/qq_36545573/article/details/142639082 用户认证系统，实现登录
# https://www.sohu.com/a/788524743_121124359
from flask import Flask, render_template, jsonify, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_cors import *
# from tqdm import tqdm
import time, subprocess, pymssql, sys, os
# import settings
from flask_sqlalchemy import SQLAlchemy
# import pyodbc
# from flask_cors import CORS
from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
# from flask_login import LoginManager
# from flask_login import UserMixin
# from flask_login import login_user, logout_user, current_user

sys.path.append(os.getcwd())
from ChcRulePO import *
from PO.TimePO import *
Time_PO = TimePO()

import socket
def get_current_ip():
    print(socket.gethostbyname(socket.getfqdn(socket.gethostname())))

    # 获取本机主机名
    hostname = socket.gethostname()
    # 根据主机名获取本机IP地址
    ip_address = socket.gethostbyname(hostname)
    return ip_address

app = Flask(__name__)
# 设置 Flask 应用的密钥，用于对 session 数据进行加密，保护敏感信息
app.secret_key = 'your_secret_key'

# CORS(app)  # 解决跨域问题
# app.config.from_object(settings)  # 加载配置文件
# print(app.config)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:Zy_123456789@192.168.0.234:1433/CHC'
# db = SQLAlchemy(app)

# 模拟的用户数据库，存储用户的用户名和经过哈希加密后的密码（防止明文存储密码）
users = {
    'jinhao': generate_password_hash('123456'),  # 'user1' 用户的密码经过哈希加密后存储
    'user2': generate_password_hash('password2')  # 'user2' 用户的密码经过哈希加密后存储
}

# 数据库
# from PO.SqlserverPO import *
# Sqlserver_PO = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database"), Configparser_PO.DB_SQL("charset"))
# Sqlserver_PO = SqlServerPO(server='192.168.0.234', user='sa', password='Zy_123456789', database='CHC',charset = 'utf-8')

conn = pymssql.connect(server='192.168.0.234', user='sa', password='Zy_123456789', database='CHC')
cursor = conn.cursor()
d_ruleName = {'健康评估': "a_jiankangpinggu", '健康干预': "a_jiankangganyu", '疾病评估': "a_jibingpinggu",'儿童健康干预': "a_ertongjiankangganyu",
              "评估因素取值": "a_pingguyinsuquzhi", "健康干预_已患疾病单病":"a_jiankangganyu_yihuanjibingdanbing", "健康干预_已患疾病组合":"a_jiankangganyu_yihuanjibingzuhe"}
l_ruleName = ['健康评估', '健康干预', '疾病评估', '儿童健康干预', '评估因素取值','健康干预_已患疾病单病', '健康干预_已患疾病组合']

# 获取测试规则
cursor.execute("select distinct [rule] from a_ceshiguize")
l_t_rows = cursor.fetchall()
# print(l_t_rows)
l_testRule = []
for i in l_t_rows:
    l_testRule.append(i[0])


# # todo [定时任务，每天凌晨2点执行]
# def my_job():
#     # print("执行定时任务...")
#     # print(Time_PO.getDateTimeByDivide())  # 2020/03/19 15:19:28
#     result = subprocess.run(['python3', './cli_chcRule_flask.py', '健康评估', 'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     # print(result.stdout)
# # # 创建调度器
# scheduler = BackgroundScheduler()
# # # 添加定时任务
# scheduler.add_job(func=my_job, trigger='cron', hour='2')
# # # 启动调度器
# scheduler.start()


@app.route('/')
def homepage():
    return render_template('pin.html')

@app.route('/index')
def index():
    print(get_current_ip)
    session_value = request.cookies.get('session')
    # print(session_value)
    # print(session['logged_in'])
    if session_value == "jinhao":
    # if session['logged_in'] == True:
        # return render_template('1.html')
        # return render_template('1.html', ruleName=l_ruleName, queryRuleCollection=l_testRule,queryErrorRuleId=l_ruleName)
        cursor.execute("select ruleName from a_memory where id = 1")
        l_t_value = cursor.fetchall()
        # print(l_t_value)
        # print(l_t_value[0][0])
        return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, queryErrorRuleId=l_ruleName,memory=l_t_value[0][0],get_current_ip=get_current_ip())
    else:
        return render_template('pin.html')





# @app.route('/pin', methods=['POST', 'GET'])
# def pin():
#     # if request.args.get('redirect') == 'true':
#     #     # return redirect('/new_url')
#     #     print("123123123")
#     #     return redirect(url_for('temp'))
#     #     # return redirect("/temp")
#     #     # return redirect("http://www.baidu.com")
#     # else:
#     #     return 'Stay on the same page'
#
#     if request.method == 'POST':
#         # 获取POST请求中的数据
#         name = request.form.get('name')
#         age = request.form.get('age')
#         print(name,age)
#         return redirect(url_for('temp'))
#         # return redirect("http://www.baidu.com",302)
#         # 处理数据...
#         # return jsonify({'message': 'Data received', 'data': {'name': name, 'age': age}})
#     elif request.method == 'GET':
#         # 获取GET请求中的数据
#         name = request.args.get('name')
#         age = request.args.get('age')
#         print(name, age)
#         # 处理数据...
#         # return jsonify({'message': 'Data received', 'data': {'name': name, 'age': age}})
#     # return redirect("http://www.baidu.com")
#     return redirect(url_for('temp'))
#     # return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, queryErrorRuleId=l_ruleName)


# 定义 '/login' 路由，并允许 GET 和 POST 两种请求方法
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 检查请求方法是否为 POST（表明用户提交了登录表单）
    if request.method == 'POST':
        # 获取用户通过表单提交的用户名
        username = request.form['username']
        # 获取用户通过表单提交的密码
        password = request.form['password']
        print(username, password)
        # 从模拟的用户数据库中获取与用户名对应的哈希密码（若用户名不存在则返回 None）
        user_hashed_password = users.get(username)
        # 检查用户是否存在并且输入的密码与数据库中的哈希密码匹配
        if user_hashed_password and check_password_hash(user_hashed_password, password):
            # 如果验证通过，设置 session，表示用户已登录
            session['logged_in'] = True
            # 重定向用户到欢迎页面
            # return redirect(url_for('welcome'))
            return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule,
                               queryErrorRuleId=l_ruleName)
        else:
            # 如果用户名或密码错误，返回错误信息
            return 'Invalid username or password'
    # 如果请求方法为 GET，返回包含用户名和密码输入框的登录表单
    return render_template('login.html')


# 定义 '/welcome' 路由，用于欢迎已登录的用户
@app.route('/welcome')
def welcome():
    # 检查 session 中是否存在 'logged_in' 并且其值为 True，表明用户已登录
    if session.get('logged_in'):
        # 如果用户已登录，返回欢迎信息
        return 'Welcome! You are logged in.'
    else:
        # 如果用户未登录，重定向到登录页面
        return redirect(url_for('login'))


# 定义 '/logout' 路由，用于处理用户登出
@app.route('/logout')
def logout():
    # 从 session 中移除 'logged_in' 键，表示用户登出
    session.pop('logged_in', None)
    # 重定向到登录页面
    return redirect(url_for('homepage'))


def getFieldValueByStep(ruleName):
    l_field = []
    l_d_all = []
    # 获取字段列表
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % (d_ruleName[ruleName]))
    l_t_field = cursor.fetchall()
    for i in l_t_field:
        l_field.append(i[0])
    # 获取所有值
    cursor.execute("select * from %s " % (d_ruleName[ruleName]))
    # cursor.execute("select * from %s where [rule] != ''" % (d_ruleName[ruleName]))
    l_t_value = cursor.fetchall()
    for i, l_v in enumerate(l_t_value):
        # 将字段呢值None改为空
        l_tmp = []
        for j in l_v:
            if j == None:
                j = ''
            j = str(j).replace("\n", "<br>")
            l_tmp.append(j)
        t_value = tuple(l_tmp)
        d_ = dict(zip(l_field, list(t_value)))
        l_d_all.append(d_)
    return l_d_all

def getFieldValue(ruleName):
    l_field = []
    l_d_all = []
    # 获取字段列表
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % (d_ruleName[ruleName]))
    l_t_field = cursor.fetchall()
    for i in l_t_field:
        l_field.append(i[0])
    # 获取所有值
    cursor.execute("select * from %s where [rule] != ''" % (d_ruleName[ruleName]))
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

    cursor.execute("select DISTINCT [rule] from %s where [rule] != ''" % (d_ruleName[ruleName]))
    l_t_rule = cursor.fetchall()
    print(l_t_rule)  # [('s3',), ('s4',), ('s5',)]

    return l_d_all

def getFieldValueById(ruleName, id):
    l_field = []
    l_d_all = []
    # 获取字段列表
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % (d_ruleName[ruleName]))
    l_t_field = cursor.fetchall()
    for i in l_t_field:
        l_field.append(i[0])
    # 获取所有值
    cursor.execute("select * from %s where id=%s" % (d_ruleName[ruleName], id))
    # cursor.execute("select * from %s where [rule] != '' and id=%s" % (d_ruleName[ruleName], id))
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


# todo 获取测试规则
@app.route('/list123/<ruleName>')
def list123(ruleName):
    session_value = request.cookies.get('session')
    if session_value == 'jinhao':
        s = ''
        cursor.execute("select DISTINCT [rule] from %s where [rule] != ''" % (d_ruleName[ruleName]))
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
            return render_template('assessFactor.html', data=getFieldValueByStep(ruleName), ruleName=ruleName, l_ruleSql=c)
        else:
            return render_template('healthIntervention.html', data=getFieldValue(ruleName), ruleName=ruleName, l_ruleSql=c)



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
            l_d_all = getFieldValue(ruleName)
    return ruleName


@app.route('/submitStep', methods=['POST'])
def submitStep():
    # "评估因素取值"
    l_id = request.form.getlist("items")
    l_ruleName = request.form.getlist("ruleName")
    ruleName = l_ruleName[0]
    print(ruleName, l_id)
    if l_id != []:
        for id in l_id:
            # print(id)
            r = ChcRulePO(ruleName)
            r.runId([id])
            # subprocess.run(['python3', './cli_chcRule_flask.py', ruleName, id], stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
            l_d_all = getFieldValue(ruleName)
        # return l_d_all
    return ruleName



@app.route('/edit123')
def edit123():
    ruleName = request.args.get('ruleName')
    id = request.args.get('id')
    print(ruleName, id)
    l_d_all = getFieldValueById(ruleName,id)
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

    # 从step步骤中获取表名
    # print(l_d_all[0]['step'])
    l_tableName = re.findall(r"from\s(\w+)\swhere", l_d_all[0]['step'], re.I)
    # print(l_tableName)  # ['TB_PREGNANT_MAIN_INFO', 'T_ASSESS_MATERNAL']
    # 获取表结构
    d_tbl = {}
    for i in l_tableName:
        s_desc = Sqlserver_PO.desc2(i)
        d_tbl[i] = s_desc

    return render_template('edit123.html', d_field=l_d_all[0], queryRuleCollection=l_testRule, s_rule=l_d_all[0]['rule'], id=id, ruleName=ruleName,l_tableName=l_tableName,d_tbl=d_tbl )
    # return render_template('edit123.html', d_field=l_d_all[0], queryRuleCollection=l_testRule, s_rule=l_d_all[0]['rule'],id=id,ruleName=ruleName,l_tableName=l_tableName,a=a )




# todo 1 测试记录
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
            l_d_all = getFieldValueById(ruleName,id)
            l_d_all[0]['ruleName'] = ruleName

            # 获取测试规则
            l_testRule = []
            cursor.execute("select distinct [rule] from a_ceshiguize where ruleName='%s'" % (ruleName))
            l_t_rows = cursor.fetchall()
            for i in l_t_rows:
                l_testRule.append(i[0])

            # 从step步骤中获取表名
            # print(l_d_all[0]['step'])
            l_tableName = re.findall(r"from\s(\w+)\swhere", l_d_all[0]['step'], re.I)
            # print(l_tableName)  # ['TB_PREGNANT_MAIN_INFO', 'T_ASSESS_MATERNAL']
            # 获取表结构
            d_tbl = {}
            for i in l_tableName:
                s_desc = Sqlserver_PO.desc2(i)
                d_tbl[i] = s_desc
            # return render_template('edit123.html', d_field=l_d_all[0])
            return render_template('edit123.html', d_field=l_d_all[0], debugRuleParam_testRule=l_testRule,queryRuleCollection=l_testRule,id=id,ruleName=ruleName,d_tbl=d_tbl)
            # return render_template('edit123.html', d_field=d_, debugRuleParam_testRule=l_testRule,queryRuleCollection=l_testRule,s_rule=d_['rule'],id=d_['id'],ruleName=d_['ruleName'],d_tbl=d_tbl)

        except:
            return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, output_testRule='error，非法id！', queryErrorRuleId=l_ruleName)


            # try:
            #     result = subprocess.run(['python3', './cli_chcRule_flask.py', ruleName, str(id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            #     print(result.stdout)
            #
            #     ruleCode = str(result.stdout).split("(r")[1].split(")")[0]
            #     ruleCode = "r" + str(ruleCode)
            #
            #     # result = result.stdout.replace("<br>", '')
            #     result = result.stdout
            #     print(result)
            #     d_result = {}
            #     if '[OK]' in result:
            #         d_result['result'] = result
            #     else:
            #         d_result = eval(result)
            #     return render_template('result.html', output_testRule={"ruleName": ruleName, "id": id, "ruleCode": ruleCode, "result": d_result}, debugRuleParam_testRule=l_testRule)
            # except:
            #     return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, output_testRule='error，非法id！', queryErrorRuleId=l_ruleName)
    else:
        return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, output_testRule='error，id不能为空！', queryErrorRuleId=l_ruleName)


# todo 2 查询错误规则的记录
@app.route('/get_queryErrorRuleId')
def get_queryErrorRuleId():
    ruleName = request.args.get('value')
    if ruleName != "none":
        print(d_ruleName[ruleName])  # a_jibingpinggu
        cursor.execute("select id,updateDate from %s where result != 'ok'" % d_ruleName[ruleName])
        rows = cursor.fetchall()
        print(rows)
        # print(rows[0][0], rows[0][1])
        data = ""
        for row in rows:
            data = data + "(" + str(row[0]) + ", " + str(row[1]) + ") "
        print(data)
        if data == '':
            response_data = {'text': 'no error'}
        else:
            response_data = {'text': data}
    else:
        response_data = {'text': ''}
    return jsonify(response_data)



# todo 3 查询step
@app.route("/get_queryRuleResult", methods=["POST"])
def get_queryRuleResult():
    ruleName = request.form.get("ruleName")
    id = request.form.get("id")
    if id != '':
        try:
            cursor.execute("select step from %s where id=%s" % (d_ruleName[ruleName], id))
            rows = cursor.fetchall()
            record = rows[0][0]
            record = record.replace("\n", '<br>')
        except:
            record = '无结果或id不存在！'
    else:
        record = 'id不能为空！'

    return record



# todo 4 查询sql
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


@app.route('/get_queryRuleName')
def get_queryRuleName():
    ruleName = request.args.get('value')
    print(ruleName)

    cursor.execute("update a_memory set ruleName='%s' where id=1" % (ruleName))
    conn.commit()

    # 获取测试规则
    cursor.execute("select distinct [rule] from a_ceshiguize where ruleName='%s'" %(ruleName))
    l_t_rows = cursor.fetchall()
    l_testRule = []
    for i in l_t_rows:
        l_testRule.append(i[0])
    print(l_testRule)
    return l_testRule


# todo 5 查询规则集
@app.route('/get_queryRuleCollection')
def get_queryRuleCollection():
    selected_value = request.args.get('value')
    # cursor.execute("select ruleName, [sql] from a_ceshiguize where [rule]='%s'" % selected_value)
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



# todo 6 更新规则集
@app.route('/updateRuleCollection', methods=['POST'])
def updateRuleCollection():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        ruleCollection = request.form['ruleCollection']
        sql = request.form['sql']
        print(ruleName,ruleCollection)
        # print(sql)

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
            return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule1, queryErrorRuleId=l_ruleName)
        else:
            return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, output_testRule3='error，rule集或sql不能为空！', queryErrorRuleId=l_ruleName)



# todo 编辑规则参数
@app.route('/debugParam', methods=['POST'])
def debugParam():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        id = request.form['id']
        ruleCode = request.form['ruleCode']
        ruleParam = request.form['ruleParam']
        print(ruleName, id, ruleCode, ruleParam)
        cursor.execute("update %s set [rule]='%s', ruleParam='%s' where id=%s" % (d_ruleName[ruleName],ruleCode,ruleParam,id))
        conn.commit()
        # r = ChcRulePO(ruleName)
        # r.runId([str(id)])
        result = subprocess.run(['python3', './cli_chcRule_flask.py', ruleName, str(id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = result.stdout.replace("<br>", '')
        print(result)
        return render_template('result.html', output_testRule={"ruleName":ruleName, "id": id, "ruleCode":ruleCode, "ruleParam": ruleParam, "result":result}, debugRuleParam_testRule=l_testRule)


# todo 编辑步骤
@app.route('/step', methods=['POST'])
def step():
    if request.method == 'POST':
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
        cursor.execute("update %s set [rule]='%s',[case]='%s',ruleParam='%s' where id = %s" % (d_ruleName[d_['ruleName']], d_['rule'], d_['case'], d_['ruleParam'], d_['id']))
        conn.commit()
        d_['ruleParam'] = d_['ruleParam'].replace("''", "'")
        r = ChcRulePO(d_['ruleName'])
        r.runId([d_['id']])
        # subprocess.run(['python3', './cli_chcRule_flask.py', d_['ruleName'], d_['id']], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        cursor.execute("select result,step from %s where id = %s" % (d_ruleName[d_['ruleName']], d_['id']))
        rows = cursor.fetchall()
        d_["result"] = rows[0][0]
        d_["step"] = rows[0][1]

        # 获取测试规则
        l_testRule = []
        cursor.execute("select distinct [rule] from a_ceshiguize where ruleName='%s'" % (d_['ruleName']))
        l_t_rows = cursor.fetchall()
        for i in l_t_rows:
            l_testRule.append(i[0])

        # 从step步骤中获取表名
        # print(l_d_all[0]['step'])
        l_tableName = re.findall(r"from\s(\w+)\swhere", d_["step"], re.I)
        # print(l_tableName)  # ['TB_PREGNANT_MAIN_INFO', 'T_ASSESS_MATERNAL']
        # 获取表结构
        d_tbl = {}
        for i in l_tableName:
            s_desc = Sqlserver_PO.desc2(i)
            d_tbl[i] = s_desc

        return render_template('edit123.html', d_field=d_, debugRuleParam_testRule=l_testRule,queryRuleCollection=l_testRule,s_rule=d_['rule'],id=d_['id'],ruleName=d_['ruleName'],d_tbl=d_tbl)





@app.route('/swagger', methods=['POST'])
def swagger():
    result = subprocess.run(['python3', './main_chcSwagger.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout
@app.route('/i', methods=['POST'])
def i():
    result = subprocess.run(['python3', './instance/zyjk/CHC/i/quanqu/main_chcIquanqu.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True)  # 开发服务器，适用于开发和测试
    # os.system("/Users/linghuchong/miniconda3/envs/py308/bin/python -m flask run --host=0.0.0.0 --port=5001")
