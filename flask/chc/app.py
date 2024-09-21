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
d_ruleName = {'健康评估': "a_jiankangpinggu", '健康干预': "a_jiankangganyu", '疾病评估': "a_jibingpinggu",'儿童健康干预': "a_ertongjiankangganyu",
              "评估因素取值": "a_pingguyinsuquzhi", "健康干预_已患疾病单病":"a_jiankangganyu_yihuanjibingdanbing"}
l_ruleName = ['健康评估', '健康干预', '疾病评估', '儿童健康干预', '评估因素取值','健康干预_已患疾病单病']
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
    return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, queryErrorRuleId=l_ruleName)


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



# 获取测试规则
@app.route('/excel/<ruleName>')
def excel(ruleName):
    # print(ruleName)  # '健康干预_已患疾病单病'
    cursor.execute(
        "select result,updateDate,step,[rule],ruleParam,ruleCode,diseaseRuleCode,diseaseCodeDesc,tester,id from %s where [rule] != ''" % (d_ruleName[ruleName]))
    l_t_rows = cursor.fetchall()
    # print(l_t_rows)  # [('ok', datetime.date(2024, 9, 14),
    l_key = ['result', 'updateDate', 'step', 'rule', 'ruleParam', 'ruleCode', 'diseaseRuleCode', 'diseaseCodeDesc', 'tester', 'id']
    l_tmp = []
    for i, l_v in enumerate(l_t_rows):
        # print(i,l_v)
        # print(dict(zip(l_key,list(l_v))))
        d_ = dict(zip(l_key, list(l_v)))
        d_['ruleName'] = ruleName
        l_tmp.append(d_)
    return render_template('about.html', data=l_tmp, ruleName=ruleName)


@app.route('/submit', methods=['POST'])
def submit():
    # ruleName = '健康干预_已患疾病单病'
    l_id = request.form.getlist("items")
    l_ruleName = request.form.getlist("ruleName")
    ruleName = l_ruleName[0]
    print(l_id)  # ['1', '4', '5']
    # print(ruleName)  # 健康干预_已患疾病单病
    if l_id != []:
        for id in l_id:
            print(id)
            subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', ruleName, id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            cursor.execute(
                "select result,updateDate,step,[rule],ruleParam,ruleCode,diseaseRuleCode,diseaseCodeDesc,tester,id from %s where [rule] != '' and id=%s" % (
                d_ruleName[ruleName], id))
            l_t_rows = cursor.fetchall()
            print(l_t_rows)  # [('ok', datetime.date(2024, 9, 14),
            l_key = ['result', 'updateDate', 'step', 'rule', 'ruleParam', 'ruleCode', 'diseaseRuleCode', 'diseaseCodeDesc', 'tester','id']
            l_tmp = []
            for i, l_v in enumerate(l_t_rows):
                # print(i,l_v)
                # print(dict(zip(l_key,list(l_v))))
                d_ = dict(zip(l_key, list(l_v)))
                d_['ruleName'] = ruleName
                l_tmp.append(d_)
            print(l_tmp)

        # refreshed = False
        # if request.headers.get('X-Reload'):
        #     # 如果是页面刷新，设置refreshed为True
        #     refreshed = True
            # 你可以在这里添加更多的刷新逻辑
        # return render_template('index.html', refreshed=refreshed)
        # return render_template('about.html', data=l_tmp, ruleName=ruleName, refreshed=refreshed)

        # return redirect('/excel')
        # return redirect('http://www.baidu.com',code=301)

        return redirect(url_for('excel',ruleName=ruleName))
    else:
        return redirect(url_for('excel',ruleName=ruleName))







# todo 1 测试记录
@app.route('/testRule', methods=['POST'])
def testRule():
    if request.method == 'POST':
        ruleName = request.form['ruleName']
        id = request.form['id']
        print(ruleName, id)
    if id != '':
        if ruleName == "评估因素取值":
            # try:
            result = subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', ruleName, id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            d_result = {}
            d_result = eval(result.stdout)

            cursor.execute("select step from %s where id = %s" % (d_ruleName[ruleName], id))
            rows = cursor.fetchall()
            print(rows[0][0])
            return render_template('result2.html', output_testRule={"ruleName": ruleName, "id": id, "step": rows[0][0], "result":d_result})
            # except:
            #     return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, output_testRule='error，非法id！', queryErrorRuleId=l_ruleName)

        elif ruleName == "健康干预_已患疾病单病":
            try:
                subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', ruleName, id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                cursor.execute("select result,step,[rule],ruleParam from %s where id = %s" % (d_ruleName[ruleName], id))
                rows = cursor.fetchall()
                return render_template('result2.html', output_testRule={"result": rows[0][0], "step": rows[0][1], "ruleName": ruleName, "id": id, "rule": rows[0][2], "ruleParam": rows[0][3]})
            except:
                return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, output_testRule='error，非法id！', queryErrorRuleId=l_ruleName)

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
                return render_template('index.html', ruleName=l_ruleName, queryRuleCollection=l_testRule, output_testRule='error，非法id！', queryErrorRuleId=l_ruleName)
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
    if 'select ' not in querySql :
        rows='error，非查询语句！'
    else:
        if 'where' not in querySql:
            rows = 'error，缺少where条件！'
        else:
            data = ""
            cursor.execute(querySql)
            rows = cursor.fetchall()
            for row in rows:
                data = data + str(row) + "<br>"
            print(data)
    return data



# todo 5 查询规则集
@app.route('/get_queryRuleCollection')
def get_queryRuleCollection():
    selected_value = request.args.get('value')
    cursor.execute("select [sql] from a_ceshiguize where [rule]='%s'" % selected_value)
    rows = cursor.fetchall()
    print(rows)
    data = ""
    for row in rows:
        data = data + str(row[0]) + "\n"
    print(data)
    response_data = {
        'text': data
    }
    return jsonify(response_data)



# todo 6 更新规则集
@app.route('/updateRuleCollection', methods=['POST'])
def updateRuleCollection():
    if request.method == 'POST':
        ruleCollection = request.form['ruleCollection']
        sql = request.form['sql']

        print(ruleCollection, sql)

        if ruleCollection != '' and sql != '':
            l_ = sql.split("\n")
            l2 = [i.replace('\r', '') for i in l_]
            l3 = [i.strip() for i in l2 if i != '']
            # print(l3)  # ['jinhao', 'yoyo', '///', 'titi']

            cursor.execute("select count([rule]) as [rule] from a_ceshiguize where [rule]='%s'" % (ruleCollection))
            l_t_count = cursor.fetchall()
            # print(l_t_count[0][0])

            if l_t_count[0][0] == 0:
                for index, sql in enumerate(l3, start=1):
                    sql = sql.replace("'", "''").replace("\r", "")
                    cursor.execute("insert into a_ceshiguize([rule],[seq],sql) values ('%s',%s,'%s')" % (ruleCollection, index, sql))
                    conn.commit()
            else:
                cursor.execute("delete from a_ceshiguize where [rule]='%s'" % (ruleCollection))
                for index, sql in enumerate(l3, start=1):
                    cursor.execute("insert into a_ceshiguize([rule],[seq],sql) values ('%s',%s,'%s')" % (ruleCollection, index, sql))
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
        rule = request.form['rule']
        ruleParam = request.form['ruleParam']
        print(ruleName, id, rule, ruleParam)  # 健康干预_已患疾病单病 1 s1 {'VISITTYPECODE':'31','DIAGNOSIS_CODE':'G46'}
        print("12121212")
        ruleParam = ruleParam.replace("'","''").replace("\r","")
        # ruleParam = ruleParam.replace("\r","")
        # ruleParam = ruleParam.replace('&apos;', "'").replace("\r","")
        cursor.execute("update %s set ruleParam='%s' where id=%s" % (d_ruleName[ruleName], ruleParam, id))
        conn.commit()
        ruleParam = ruleParam.replace("''", "'")
        subprocess.run(['python3', './instance/zyjk/CHC/rule/cli_chcRule_flask.py', ruleName, str(id)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        cursor.execute("select result,step,eachStep from %s where id = %s" % (d_ruleName[ruleName], id))
        rows = cursor.fetchall()
        # print(rows)
        return render_template('result2.html', output_testRule={"result": rows[0][0], "step": rows[0][1], "eachStep": rows[0][2], "ruleName": ruleName, "id": id, "rule": rule, "ruleParam": ruleParam}, debugRuleParam_testRule=l_testRule)


@app.route('/about4')
def about4():
    ruleName = request.args.get('ruleName')
    id = request.args.get('id')
    print(ruleName, id)  # 健康干预_已患疾病单病 2
    cursor.execute("select result,step,[rule],ruleParam,diseaseCodeDesc,eachStep from %s where id=%s " % (d_ruleName[ruleName], id))
    l_t_rows = cursor.fetchall()
    result = l_t_rows[0][0]
    step = l_t_rows[0][1]
    rule = l_t_rows[0][2]
    ruleParam = l_t_rows[0][3]
    diseaseCodeDesc = l_t_rows[0][4]
    eachStep = l_t_rows[0][5]
    return render_template('result2.html', output_testRule={"ruleName":ruleName, "id": id, "result": result, "step":step, "rule": rule, "ruleParam": ruleParam, 'diseaseCodeDesc':diseaseCodeDesc, 'eachStep':eachStep})




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
