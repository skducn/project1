# https://blog.jetbrains.com/zh-hans/pycharm/2022/08/flask-tutorial/
# https://blog.csdn.net/weixin_44072077/article/details/102531756

# https://blog.51cto.com/u_16175517/7231181 Flask-python-前端实时显示后端处理进度
# https://www.cnblogs.com/mqxs/p/7930064.html 【Flask】前端调用后端方法返回页面
# https://blog.csdn.net/gui818/article/details/135848698

# 安装 Microsoft ODBC Driver for SQL Server (macOS)
# https://learn.microsoft.com/zh-cn/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16
# Microsoft ODBC 18
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
# brew update
# HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18

# 杀5000端口进程
# sudo kill -9 `lsof -t -i:5000`
# sudo kill -9 `netstat -nlp | grep :5000 | awk '{print $7}' | cut -d '/' -f 1`

# # 局域网ip`
# /Users/linghuchong/miniconda3/envs/py308/bin/python -m flask run --host=0.0.0.0 --port=5001

# https://max.book118.com/html/2024/0712/7005163005006133.shtm  flask用户认证与权限管理
#***************************************************************



from flask import Flask, render_template, request, jsonify, Response, json, redirect, url_for
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
from flask import request

sys.path.append(os.getcwd())
from PO.TimePO import *
Time_PO = TimePO()


app = Flask(__name__)
# CORS(app)  # 解决跨域问题
# app.config.from_object(settings)  # 加载配置文件
# print(app.config)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:Zy_123456789@192.168.0.234:1433/CHC'
# db = SQLAlchemy(app)

# 数据库
conn = pymssql.connect(server='192.168.0.234', user='sa', password='Zy_123456789', database='CHC')
cursor = conn.cursor()
d_ruleName = {'健康评估': "a_jiankangpinggu", '健康干预': "a_jiankangganyu", '疾病评估': "a_jibingpinggu", '儿童健康干预': "a_ertongjiankangganyu", "评估因素取值": "a_pingguyinsuquzhi"}
l_ruleName = ['健康评估', '健康干预', '疾病评估', '儿童健康干预', '评估因素取值']
# 获取测试规则
cursor.execute("select distinct [rule] from a_ceshiguize")
l_t_rows = cursor.fetchall()
# print(l_t_rows)
l_testRule = []
for i in l_t_rows:
    l_testRule.append(i[0])


# 登录
# login_manager = LoginManager()
# login_manager.init_app(app)
# app.secret_key = '12345678900'
# users = {"jinhao":{'password': 'jinhao123'},"chenxiaodong":{'password': '123456'}, "shuyangyang":{'password': '666666'}}

# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id
#
# @login_manager.user_loader
# def load_user(user_id):
#     if user_id in users:
#         return User(user_id)
#     return None

@app.route('/')
def index():
    # todo 获取访问者ip
    # ip_address = request.remote_addr
    # print(ip_address)
    # ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    # print(ip_address)
    # if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    #     print(request.environ['REMOTE_ADDR'])
    # else:
    #     print(request.environ['HTTP_X_FORWARDED_FOR'])  # if behind a proxy
    # client_ip = request.headers.get('X-Forwarded-For', None)
    # print(client_ip)
    # return render_template('login.html')
    return render_template('index.html', ruleName=l_ruleName, queryTestRule=l_testRule, queryErrorRuleId=l_ruleName)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         print(username,password)
#         if username in users and users[username]['password'] == password:
#             user = User(username)
#             login_user(user)
#             # return redirect(url_for('protected'))
#             return render_template('index.html', ruleName=l_ruleName, queryTestRule=l_testRule, queryErrorRuleId=l_ruleName)
#         else:
#             return render_template('login.html', output_login='error，账号或密码有误！')
#
#             # return "Invalid username or password"
#     return render_template('login.html')

# @app.route('/protected')
# # @login_required
# def protected():
#     return f"Hello, {current_user.id}! This is a protected page."
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# # todo [定时任务，每天凌晨2点执行]
# def my_job():
#     # print("执行定时任务...")
#     # print(Time_PO.getDateTimeByDivide())  # 2020/03/19 15:19:28
#     result = subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', '健康评估', 'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#     # print(result.stdout)
# # # 创建调度器
# scheduler = BackgroundScheduler()
# # # 添加定时任务
# scheduler.add_job(func=my_job, trigger='cron', hour='2')
# # # 启动调度器
# scheduler.start()






# todo 测试记录
@app.route('/testRule', methods=['POST'])
def testRule():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        id = request.form['id']
        print(ruleName, id)
    if id != '':
        if ruleName == "评估因素取值":
            try:
                result = subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', ruleName, str(id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(result.stdout)
                # result = result.stdout
                # print(type(result))
                # result = result.replace("\n", '\n\r')

                d_result = {}
                d_result = eval(result.stdout)
                # d_result['result'] = result
                # if '[OK]' in result:
                #     d_result['result'] = result
                # else:

                return render_template('result2.html', output_testRule={"ruleName": ruleName, "id": id, "result": d_result}, debugRuleParam_testRule=l_testRule)
            except:
                return render_template('index.html', ruleName=l_ruleName, queryTestRule=l_testRule, output_testRule='error，非法id！', queryErrorRuleId=l_ruleName)
        else:
            try:
                result = subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', ruleName, str(id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(result.stdout)

                ruleCode = str(result.stdout).split("(r")[1].split(")")[0]
                ruleCode = "r" + str(ruleCode)

                # result = result.stdout.replace("<br>", '')
                result = result.stdout
                print(result)
                d_result = {}
                if '[OK]' in result:
                    d_result['result'] = result
                else:
                    d_result = eval(result)
                return render_template('result.html', output_testRule={"ruleName": ruleName, "id": id, "ruleCode": ruleCode, "result": d_result}, debugRuleParam_testRule=l_testRule)
            except:
                return render_template('index.html', ruleName=l_ruleName, queryTestRule=l_testRule, output_testRule='error，非法id！', queryErrorRuleId=l_ruleName)
    else:
        return render_template('index.html', ruleName=l_ruleName, queryTestRule=l_testRule, output_testRule='error，id不能为空！', queryErrorRuleId=l_ruleName)


# todo 查询错误结果id
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
            response_data = {'text': '未找到error'}
        else:
            response_data = {'text': data}
    else:
        response_data = {'text': ''}
    return jsonify(response_data)


# todo 查询错误结果结果
# @app.route('/get_queryRuleResult', methods=['POST'])
# def get_queryRuleResult():
#     if request.method == 'POST':
#         ruleName = request.form['ruleName']
#         id = request.form['id']
#         print(ruleName, id)
#         if id !='':
#             try:
#                 cursor.execute("select result from %s where id=%s" %(d_ruleName[ruleName], id))
#                 rows = cursor.fetchall()
#                 record = rows[0][0]
#                 # return redirect('/', code=302, ruleName=l_ruleName, mySelect=l_testRule, output_queryStatus=record, output_queryStatus_sql=[d_ruleName[ruleName],id])
#                 return render_template('index.html', ruleName=l_ruleName, mySelect=l_testRule, output_queryStatus=record, output_queryStatus_sql=[d_ruleName[ruleName],id])
#             except:
#                 return render_template('index.html', ruleName=l_ruleName, mySelect=l_testRule, output_queryStatus='error，非法id！')
#         else:
#             return render_template('index.html', ruleName=l_ruleName, mySelect=l_testRule, output_queryStatus='error，id不能为空！')
@app.route("/get_queryRuleResult", methods=["POST"])
def get_queryRuleResult():
    ruleName = request.form.get("ruleName")
    id = request.form.get("id")
    if id != '':
        try:
            cursor.execute("select result from %s where id=%s" % (d_ruleName[ruleName], id))
            rows = cursor.fetchall()
            record = rows[0][0]
            record = record.replace("\n", '<br>')
        except:
            record = 'error，id不存在或无result！'
    else:
        record = 'error，id不能为空！'

    return record


# todo 查询完整记录
# @app.route('/get_queryRecord', methods=['POST'])
# def get_queryRecord():
#     if request.method == 'POST':
#         sql = request.form['sql']
#         print(sql)
#         if 'update ' in sql or 'delete from' in sql:
#             return render_template('index.html', ruleName=l_ruleName, mySelect=l_testRule, output_querySQL='error，非查询语句！')
#         else:
#             try:
#                 cursor.execute(sql)
#                 rows = cursor.fetchall()
#                 record = rows
#                 return render_template('index.html', ruleName=l_ruleName, mySelect=l_testRule, output_querySQL=record)
#             except:
#                 return render_template('index.html', ruleName=l_ruleName, mySelect=l_testRule, output_querySQL='error，非法语句！')
#     # if request.method == 'GET':
#     #     sql = request.args.get('id')
#     #     print(sql)
@app.route("/get_queryRecord", methods=["POST"])
def get_queryRecord():
    sql = request.form.get("sql")
    if 'select ' not in sql :
        rows='error，非查询语句！'
    else:
        if 'where' not in sql:
            rows = 'error，缺少where条件！'
        else:
            cursor.execute(sql)
            rows = cursor.fetchall()
            data = ""
            for row in rows:
                data = data + str(row) + "<br>"
            print(data)
    return data


# todo 查询规则语句
@app.route('/get_queryTestRule')
def get_queryTestRule():
    selected_value = request.args.get('value')
    # print(selected_value)
    cursor.execute("select * from a_ceshiguize where [rule]='%s'" % selected_value)
    rows = cursor.fetchall()
    data = ""
    for row in rows:
        data = data + str(row) + "\n\n"
    print(data)
    response_data = {
        'text': data
    }
    return jsonify(response_data)


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
        result = subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', ruleName, str(id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = result.stdout.replace("<br>", '')
        print(result)
        return render_template('result.html', output_testRule={"ruleName":ruleName, "id": id, "ruleCode":ruleCode, "ruleParam": ruleParam, "result":result}, debugRuleParam_testRule=l_testRule)


# todo 编辑步骤
@app.route('/step', methods=['POST'])
def step():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        id = request.form['id']
        step = request.form['step']
        print(1,step)
        if step != "":
            step = step.replace("'","''").replace("\r","")
        # print(step)
        # sys.exit(0)
        # cursor.execute('update %s set step="%s" where id=%s' % (d_ruleName[ruleName], step, id))
            cursor.execute("update %s set step='%s' where id=%s" % (d_ruleName[ruleName], step, id))
            conn.commit()
            result = subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', ruleName, str(id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # result = result.stdout.replace("<br>", '')
            result = result.stdout
            d_result = eval(result)
            # return render_template('result2.html', output_testRule={"ruleName":ruleName, "id": id, "step": step, "result":result}, debugRuleParam_testRule=l_testRule)
            return render_template('result2.html', output_testRule={"ruleName": ruleName, "id": id, "result": d_result}, debugRuleParam_testRule=l_testRule)
        else:
            return render_template('index.html', ruleName=l_ruleName, queryTestRule=l_testRule, queryErrorRuleId=l_ruleName)


@app.route('/swagger', methods=['POST'])
def swagger():
    result = subprocess.run(['python3', './instance/zyjk/CHC/swagger/main_chcSwagger.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout
@app.route('/i', methods=['POST'])
def i():
    result = subprocess.run(['python3', './instance/zyjk/CHC/i/quanqu/main_chcIquanqu.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True)  # 开发服务器，适用于开发和测试
    # os.system("/Users/linghuchong/miniconda3/envs/py308/bin/python -m flask run --host=0.0.0.0 --port=5001")
