from flask import Flask  # 导入Flask库
from flask import Flask, render_template, jsonify, redirect, url_for, flash, session, request, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
# from flask_caching import Cache
app = Flask(__name__)  # 创建一个Flask应用实例，__name__代表当前模块的名称


@app.route("/")  # 装饰器，告诉Flask当用户访问根路径时应该执行下面定义的index函数
def index():  # 定义index函数，处理来自根路径的请求
    # return "Hello World"  # 返回字符串 "Hello World" 给用户
    return render_template('index.html')

@app.route("/test")  # 装饰器，告诉Flask当用户访问根路径时应该执行下面定义的index函数
def test():  # 定义index函数，处理来自根路径的请求
    # return "Hello World"  # 返回字符串 "Hello World" 给用户
    # return render_template('index7.html')
    return render_template('hospital.html')


# # todo 登录
# @app.route('/login2', methods=['POST'])
# def login2():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == 'test' and password == '123456':
#             return render_template('index7.html', global_d_=global_d_, tabName='测试项', subName='测试规则', message=-1)
#         else:
#             return render_template('login2.html')


if __name__ == '__main__':  # 检查当前模块是否作为主程序运行
    # app.run()  # 启动Flask的开发服务器，监听请求并响应，默认运行在http://127.0.0.1:5000/
    app.run(debug=True, port=5002)