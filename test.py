# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: # textwrap 调整换行符的位置来格式化文本
# __all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
# 官网：https://docs.python.org/zh-cn/3.8/library/textwrap.html
# 学习：https://www.cnblogs.com/wj5633/p/6931187.html
# 学习：https://blog.csdn.net/zwbzwbzwbzwbzwbzwb/article/details/52824154
# ***************************************************************u**

# a = {'tb%':['id', 'page']}
# print(list(a.keys())[0])

a = [{'COLUMN_NAME': 'id', 'DATETIME_PRECISION': "55"},{'name': 'jin', 'age': "525"}]
b = [{'test': '77', 'hello': "123"},{'yellow': '727', 'color': "4545"}]

print(len(a))

for i in range(len(a)):
    print(a[i])
    a[i].update(b[i])
print(a)



#
# from collections import Counter
# #
# # counts = Counter([1,1,1,5,6,7,8,9,9,9,9,9,9])
# # print(counts.most_common())
# # print(counts.most_common(1)[0][0])
#
#
# l_d_ = [{'a': 17, 'b': 2},{'a': 13, 'b': 5},{'a': 15, 'b': 5},{'a': 17, 'b': 5}]
# l_partFields = ['a','b']
#
# l_tmp = []
# d = {}
# for field in l_partFields:
#     for i in range(len(l_d_)):
#         l_tmp.append(l_d_[i][field])
#     d[field] = l_tmp
#     l_tmp = []
# # print(d)
# for k,v in d.items():
#     counts = Counter(v)
#     print(counts.most_common(1)[0][0])
#     d[k] = counts.most_common(1)[0][0]
# print(d)


# d = {}
# l2 = []
# for i in l1:
#     # print(i)
#     for k,v in i.items():
#         print(k,v)
#         if k in d:
#             print("```````````")
#             l2.append(v)
#         else:
#             # l2.append(v)
#             d[k] = list(str(v))
#         print(d)
#     # break
# print(d)
#
# print("``````````````````````````````")
# dd = {}
# for i in l1:
#     if dd != {}:
#         dd = {k: (dd.get(k), i.get(k)) for k in dd.keys() & i.keys()}
#         # print(dd)
#     else:
#         dd = i
# print(dd)
# print(dd['a'],type(dd['a']))
#
# print(len(dd['a']))


# dict1 = {'a': 1, 'b': 2}
# dict2 = {'a': 1, 'b': 20, 'c': 30}
#
# # 使用字典推导式
# combined_dict = {k: (dict1.get(k), dict2.get(k)) for k in dict1.keys() & dict2.keys()}
# print(combined_dict)
#
# # 或者使用循环
# combined_dict = {}
# for k in dict1.keys() & dict2.keys():
#     combined_dict[k] = (dict1.get(k), dict2.get(k))
#
# print(combined_dict)





# a = eval(assert "LMP"=='LMP')

# a= (eval('1'=='1'))
# print(a)
# import pandas as pd
#
#
# pd.read_csv("")

# l1 =  ['John', 'Doe', 'Jack', 'Bob', 'Smith']
# print("-".join(l1))
#
# d1 = {'Name': 'John', 'Age': 25}
# print(d1['Name'])
# print(d1.get('Name1', -1))
#
# int = d1.setdefault("Name1", 100)
# print(int)
# print(d1)
#
#
# for i,name in enumerate(l1, start=1):
#     print(i,name)
#
# a = 1000000000
# b = f'{a:,}'
# print(type(b),b)
#
# foods = ['Apples', 'Oranges', 'Bananas']
# # 可指定任意分隔符
# print(*foods)
# print(*foods[1][1])
# print(*foods, sep=', ', end='.\n')
# print(*foods, sep=' -- ', end='.\n')
#
#
#
# people= ['John', 'Doe', 'James', 'Bob', 'Smith', 'Stefan']
# first_person, *_, last_person = people
# print(first_person, last_person)    # Output: John Stefan
# print(_)    # ['Doe', 'James', 'Bob', 'Smith']
# print((_)[1])    # James
# print((_)[1][2])    # m
# print(*_)    # Doe James Bob Smith
# print((*_,)[1])    # James
# print((*_,)[1][2])    # m
#
# print(people[1:-1])


# age =22
# print(f'{age=}')  # age=22
# print(f'{5+10=}')  # 5+10=15
#
# n = 1314521.56789
# print(round(n,2))  # 1314521.57
# print(round(n,-1))  # 1314520.0
# print(round(n,-3))  # 1315000.0


#
# s = "abc"
# print(s.split(','))
# print(list(eval(s)))

# 123
# 13
# 13
#
# import time
# import threading
# from multiprocessing import Pool
# from tqdm import tqdm
#
# def do_work(x):
#     time.sleep(x)
#     return x
#
# def progress():
#     time.sleep(3)  # 3秒后查进度
#     print(f'任务有: {pbar.total} 已完成:{pbar.n}')
# tasks = range(10)
# pbar = tqdm(total=len(tasks))
#
# if __name__ == '__main__':
#     thread = threading.Thread(target=progress)
#     thread.start()
#     results = []
#     with Pool(processes=5) as pool:
#         for result in pool.imap_unordered(do_work, tasks):
#             results.append(result)
#             pbar.update(1)
#     print(results)





# # coding = utf-8
# import numpy as np
# from IPython import embed
# # xy 输入，可支持浮点数操作 速度很快哦
# # return xy 去重后结果
# def duplicate_removal(xy):
#   if xy.shape[0] < 2:
#     return xy
#   _tmp = (xy*4000).astype('i4')          # 转换成 i4 处理
#   _tmp = _tmp[:,0] + _tmp[:,1]*1j         # 转换成复数处理
#   keep = np.unique(_tmp, return_index=True)[1]  # 去重 得到索引
#   return xy[keep]                 # 得到数据并返回
# # _tmp[:,0] 切片操作，因为时二维数组，_tmp[a:b, c:d]为通用表达式，
# # 表示取第一维的索引 a 到索引 b，和第二维的索引 c 到索引 d
# # 当取所有时可以直接省略，但要加':'冒号 、当 a == b 时可只写 a ,同时不用':'冒号
# if __name__ == '__main__':
#   if 1: # test
#     xy = np.array([[1.0, 1.0, 1.], [2.0, 2.0, 2.0], [3.0, 0.0, 0.0], [1.0, 1.0, 1.00]])
#     print(xy)
#     new_xy = duplicate_removal(xy)
#     print(new_xy)
#   # embed()


# from flask import (
#     Flask, render_template, request, redirect, globals
# )
# import test1
#
# app = Flask(__name__)
#
#
# @app.route("/", methods=['GET', 'POST'])
# def index():
#     return '<form action = "http://localhost:5000/b" method = "post"></form><a href="/test" rel="external nofollow"  rel="external nofollow"  rel="external nofollow" ><button onclick="">进入测试</button></a><a href="/test1" rel="external nofollow" >'
#
# @app.route("/test", methods=['GET', 'POST'])
# def test():
#     test1.run()
#     return '<form action = "http://localhost:5000/b" method = "post"></form><a href="/test" rel="external nofollow"  rel="external nofollow"  rel="external nofollow" ><button onclick="">进入测试</button></a>'
#
#
# if __name__ == '__main__':
#     app.run(debug=True)






# from tqdm import tqdm
# import time
# total = 50
# for i in tqdm(range(total), desc="Processing => "):
#     time.sleep(0.1)  # 模拟耗时操作

# from tqdm import tqdm
# import time
# total = 50
# for i in tqdm(range(total), desc="Processing", bar_format="{desc}: {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"):
#     time.sleep(0.1)  # 模拟耗时操作#

# from tqdm import tqdm
# import time
# total = 50
# for i in tqdm(range(total), desc="Processing", mininterval=0.5):
#     time.sleep(0.1)  # 模拟耗时操作

# from tqdm import tqdm
# import time
# total = 50
# with tqdm(total=total, desc="Starting") as pbar:
#     for i in range(total):
#         time.sleep(0.1)  # 模拟耗时操作
#         pbar.set_description(f"Processing {i+1}")
#         pbar.update(1)


# from tqdm import tqdm
# import time
# def update_progress(progress):
#     print(f"Progress: {progress}% completed.", end="\r")
# total = 50
# for i in range(total):
#     time.sleep(0.1)  # 模拟耗时操作
#     update_progress(int((i + 1) / total * 100))
# print()  # 打印换行




# page = SessionPage()

# from DrissionPage import SessionPage



# page.get('https://gitee.com/explore/all')



# items = page.eles('t:h3')
#
# # 遍历元素
# for item in items[:-1]:
#     # 获取当前<h3>元素下的<a>元素
#     lnk = item('tag:a')
#     # 打印<a>元素文本和href属性
#     print(lnk.text, lnk.link)

#
# from DrissionPage import SessionPage
#
# page = SessionPage()
# page.get('https://gitee.com/explore')
#
# # 获取包含“全部推荐项目”文本的 ul 元素
# ul_ele = page.ele('tag:ul@text():全部推荐项目')
#
# # 获取该 ul 元素下所有 a 元素
# titles = ul_ele.eles('tag:a')
#
# # 遍历列表，打印每个 a 元素的文本
# for i in titles:
#     print(i.text)
#
# from DrissionPage import WebPage, ChromiumOptions, SessionOptions
#
# co = ChromiumOptions()
# so = SessionOptions()
#
# page = WebPage(chromium_options=co, session_or_options=so)
# # page.
# page.get('https://gitee.com/explore')
# import os
#
# varPath = '/Users/linghuchong/Downloads/video/douyin/晨辉律师直播(洪文律所)'
# os.system("cd '" + varPath + "'; open .")
# # os.system("cd " + varPath )


# l =  [{'key1': 'ID', 'value1': '499948'}, {'key1': 'QTY', 'value1': '1'}, {'key1': 'Q2', 'value1': '1'}, {'key1': 'ID', 'value1': '499'}]
#
# print(len(l))
# d = {}
# for i in range(len(l)):
#     d[l[i]['key1']] = l[i]['value1']
#
# print(d)

# # l = ['a','']
# l = ['a']
# if len(l)  ==1:
#     l.append('')
#
# a = tuple(l)
# print(a)

# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper
#
# @my_decorator
# def say_hello():
#     print("Hello!")
#
# say_hello()


# import pkg_resources
# pkg_resources.require('pandas')
#
# installed_packages = pkg_resources.working_set
# for package in installed_packages:
#     print(package.key, package.version)


# a= [{'in': 'body', 'name': 'loginFormVO', 'description': 'loginFormVO', 'required': True, 'schema': {'$ref': '#/definitions/LoginInputVO对象'}}]
#
# print(a[1]['in'])

# import os, sys
# from unrar import rarfile


# def rar_attack():
#     file_handle = rarfile.RarFile('/Users/linghuchong/Downloads/4/4.rar')
#     handle_password = open('passwords.txt')
#     for pwd in handle_password:
#         pwd = pwd.rstrip()
#         try:
#             file_handle.extractall(path='/Users/linghuchong/Downloads/4/', pwd=pwd.encode())
#             print('Found:' + pwd)
#             break
#         except:
#             pass
#     handle_password.close()
#     file_handle.close()
#
# rar_attack()

# if __name__ == '__main__':
#     file_name = sys.argv[1]
#     if os.path.isfile(file_name) and file_name.endswith('.rar'):
#         rar_attack(file_name)
#     else:
#         print('Not RAR')




# list1 = [1,2,4,6,8]
# # 反向迭代
# for i in reversed(list1):
#     print(i)




# import feapder
#
#
# class FirstSpider(feapder.AirSpider):
#     def start_requests(self):
#         yield feapder.Request("https://www.douyin.com/video/7301240807376407818", render=True)
#
#     def parse(self, request, response):
#         print(response)
#
#
# if __name__ == "__main__":
#     FirstSpider().start()

# import dmPython
# try :
#     # 输入相关配置信息
#     conn = dmPython.connect(user='SYSDBA', password='SYSDBA001', server='localhost', port=5236)
#     # 连接数据库
#     curses = conn.cursor()
#     #连接成功提示
#     print("连接成功")
# except:
#     #失败提示
#     print("失败")




# list1 = [1,2,3,4,5]
# for i in range(len(list1)):
#     list1[i] = list1[i]+4
# print(list1)
# import threading
#
# def test (x,y):
#
#  for i in range(x,y):
#
#    print(i)
#
# thread1 = threading.Thread(name='t1',target= test,args=(1,10))
#
# thread2 = threading.Thread(name='t2',target= test,args=(11,20))
#
# thread1.start()   #启动线程1
#
# thread2.start()   #启动线程2

# import pika
#
#
# def producer():
#     credentials = pika.PlainCredentials('mingchentong', 'mingchentong')
#     connection = pika.BlockingConnection(pika.ConnectionParameters('103.25.65.103', '5672', '/', credentials))
#     channel = connection.channel()
#     # channel.exchange_declare(exchange="boot_topic_exchange", durable=True)
#     channel.queue_declare(queue='boot_queue', durable=True)
#     try:
#         channel.basic_publish(exchange='', routing_key='boot_queue', body='Hello, World!123213213123123')
#
#         # channel.wait_for_confirms()
#
#         print(" [x] Sent 'Hello, World!'")
#     except Exception as e:
#         print(f"Failed to send message: {e}")
#
#     connection.close()
#
# def consumer():
#
#     credentials = pika.PlainCredentials('mingchentong', 'mingchentong')
#     connection = pika.BlockingConnection(pika.ConnectionParameters('103.25.65.103', '5672', '/', credentials))
#     channel = connection.channel()
#
#     channel.queue_declare(queue='boot_queue', durable=True)
#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(queue='boot_queue', on_message_callback=callback)
#
#     print("Waiting for messages. To exit press CTRL+C")
#
#     channel.start_consuming()
#
# def callback(ch, method, properties, body):
#     try:
#         print(f"Received message: {body}")
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#
#     except Exception as e:
#         print(f"Error processing message: {e}")
#         ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
#
# if __name__ == "__main__":
#     producer()
#     consumer()


# import trace
# from time import sleep
# def func1():
#     print("func1")
#     sleep(5)
#
# def func2():
#     print("func2")
#     func1()
#
# import trace
#
# def print_string(string):
#     tracer = trace.Trace(trace=0, count=1)
#     tracer.runfunc(func1(),string)
#     results = tracer.results()
#     results.write_results(show_missing=True, coverdir=".")
#
# print_string(12)

# import time,sys
#
# for i in range(10):
#     sys.stdout.write("\rProcessing at {}%".format((i+1)*10))
#     sys.stdout.flush()
#     time.sleep(1)

# import time
#
# # 实例：[100%]: ||||||||||||||||||||||||||||||||||||||||||||||||||||
# for i in range(0, 101, 2):
#     time.sleep(0.1)  #线程推迟指定时间运行，0.1秒代表休眠100毫秒
#     num = i // 2
#     if i == 100:
#         process = "\r[%3s%%]: |%-50s|\n" % (i, '|' * num)
#     else:
#         process = "\r[%s%%]: |%-50s|" % (i, '*' * num)
#     print(process, end='', flush=True)
#



# from time import sleep
# from tqdm import trange
# def init_progress_bar(total):
#     return trange(total)
# def get_total_iterations():
#     return 1
# def run_function():
#     progress_bar = init_progress_bar(get_total_iterations())
#     for i in range(get_total_iterations()):
#         # 执行函数的代码
#         print(111, end="")
#         sleep(5)
#
#         progress_bar.update(1)  # 更新进度条
#     progress_bar.close()  # 完成进度条
#
# run_function()


# import sys, time
# print("正在下载...")
# for i in range(11):#通过for循环输出进度条效果
#     if i != 10:
#         sys.stdout.write("==")
#     else:
#         sys.stdout.write("== " + str(i*10)+"%/100%")
#         sys.stdout.flush()
#     time.sleep(0.5)#sleep用来控制输出时间
# print(" " + "下载完成")

# list1 = ['name', 'age','sex']
# print(str(list1))

# dict1 = {'a': 1, 'b': 2, 'c': 3}
# values = dict1.keys()
# print(list(values))  # ['a', 'b', 'c']
# str2 = ','.join(list(values))
# print(str2) # a,b,c

# import exifread,os
#
# with open('DSC_0127.JPG', 'rb') as file_data:
#     tags = exifread.process_file(file_data)
#     tag_date = 'EXIF DateTimeOriginal'
#     print(tags)
#     if tag_date in tags:
#         print(tag_date)
#         file_rename =str(tags[tag_date]).replace(':','').replace(' ', '_')
#         print(file_rename)
#         # file_rename =str(tags[tag_date]).replace(':','').replace(' ', '_') + os.path.splitext(filename)[1]
#         # new_path = os.path.join(root_dir, file_rename)
#         # os.rename(file_path, new_path）


# from PO.ListPO import *
# List_PO = ListPO()

# d_data = [
#             {'idCard': '310101198004332001'},
#             {'idCard': '310101198004332002'}
#         ]
#
# for i in range(len(d_data)):
#     print(d_data[i])
#     print(d_data[i]['idCard'])

# list1 = ['GW', 'QTY0:0', 'PG_AGE003:11212', 'PG_JWS001:1']
#
# list1.pop(0)
# list1 = List_PO.list2dictByKeyValue(list1)
# print(list1)
# print(x['PG_AGE003'])

# import sys,os,datatime

# s = "['r1',123]"
# print()
#
# # var = {'母亲': ['脑卒中', '冠心病',{'其他':'123'}], '父亲': ['高血压', '糖尿病'], '其他':['12121','2020-12-12']}
# var = {'姓名': '魏梅娣', '民族': '苗族', '文化程度': '小学教育'}
# =======
#
# var = {'母亲': ['脑卒中', '冠心病',{'其他':'123'}], '父亲': ['高血压', '糖尿病'], '其他':['12121','2020-12-12']}
#
# >>>>>>> origin/master
# =======
#
# var = {'母亲': ['脑卒中', '冠心病',{'其他':'123'}], '父亲': ['高血压', '糖尿病'], '其他':['12121','2020-12-12']}
#
# >>>>>>> 135c3a46e4d45a68f5bbf120c543ea6685b3b90f
# =======
#
# var = {'母亲': ['脑卒中', '冠心病',{'其他':'123'}], '父亲': ['高血压', '糖尿病'], '其他':['12121','2020-12-12']}
#
# >>>>>>> 135c3a46e4d45a68f5bbf120c543ea6685b3b90f
# # print(len(var))
# x=1
# for k,v in var.items():
#     x = x+1
#     print(k,v,x)

#
# for i in range(len(var)):
#
#     if isinstance(v[i],dict) == True:

#
# for k,v in var.items():
# <<<<<<< HEAD
# <<<<<<< HEAD
# <<<<<<< HEAD
#     if k == '姓名':
# =======
#     if k == '其他':
# >>>>>>> origin/master
# =======
#     if k == '其他':
# >>>>>>> 135c3a46e4d45a68f5bbf120c543ea6685b3b90f
# =======
#     if k == '其他':
# >>>>>>> 135c3a46e4d45a68f5bbf120c543ea6685b3b90f
#         print(v)


    # if v.type
    # if '其他' in v:
    #     print(1121212)




# 查看9222端口情况，lsof -i tcp:9222
# 删除PID， kill -9 3333   //这里3333是9222的PID
# a = 'Ella聊美语/让我带你读你的第一本英文原著✅ \n（我的英文基础网课、自学指南电子书、一对一请看我首页） \n我初学英文的时候看的原著有\n1 Diary of a Wimpy Kid 词汇量范围 1000-3000\n它是一个青少年小说，而且有出同名电影，里面的用词和表达很日常也很俏皮，单词量范围也不会很大，highly recommend! \n2 Rich Dad Poor Dad (30'
# print(len(a))
# print(a[:5])
# from DrissionPage.easy_set import set_paths
# set_paths(browser_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
# # set_paths(browser_path='/Applications/Firefox.app/Contents/MacOS/firefox')
#
# from DrissionPage import ChromiumPage
# page = ChromiumPage()
# page2 = ChromiumPage()
# page.get('https://www.baidu.com')
# page2.get('https://www.jd.com')
#
# from decimal import Decimal

# import hashlib
# import execjs
#
#
# def getMd5(varText):
#     """2.4.1，生成MD5加密值"""
#     # 分析：加密输出是16进制的md5值，这里传入的字符串前加个b将其转为二进制，或者声明为utf-8, 否则回报错误TypeError: Unicode-objects must be encoded before hashing
#
#     m = hashlib.md5(
#         varText.encode(encoding="utf-8")
#     )  # 等同于 m = hashlib.md5(b'123456')
#     return m.hexdigest()
#
# print(getMd5("https://cn.pornhub.com/view_video.php?viewkey=640c1194860f9"))  # e10adc3949ba59abbe56e057f20f883e

# print("*" * 100)
# print("* [ignore] => " )
# print("*" * 0 )

# md = "3888ab363c8d6425133f2f83b685e39a".hashvalue
# print(md)
#
#
# def get_js():
#     # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
#     f = open("./helpers.js", 'r', encoding='UTF-8')
#     line = f.readline()
#     htmlstr = ''
#     while line:
#         htmlstr = htmlstr + line
#         line = f.readline()
#     return htmlstr
# jsstr = get_js()
# ctx = execjs.compile(jsstr)
# print(ctx.call('640c1194860f9'))

# from md5util import Md5Util
# print(Md5Util("640c1194860f9"))

# dingding机器人
# url = "https://oapi.dingtalk.com/robot/send?access_token=0708efc5088d851887a18f31a2effc31a9f1d2ba2340ab5643a5b53b3e88cb7d"
# url = "https://oapi.dingtalk.com/robot/send?access_token=528fb490067de67a0bce13c344504aeacd45d268150d86a57b949d75553a9d12"
# sign = "SEC31686f219dcb7356c3a4281f8fe4e7cc42bc40cb9f9fa63f7bca29665c06aa9e"
#
# json_text={
#     "at": {
#         "atMobiles":[
#             "180xxxxxx"
#         ],
#         "atUserIds":[
#             "user123"
#         ],
#         "isAtAll": False
#     },
#     "text": {
#         "content":"测试机器人推送服务"
#     },
#     "msgtype":"text"
# }
#
# from jsonpath import jsonpath
# print(jsonpath(json_text, '$..text'))

# import requests, json, sys
# m = requests.post(url, json.dumps(json_text), headers={"Content-Type": "application/json"}).content
# print(m)
#
# sys.exit(0)
#
#
#
# print((m.decode("utf-8", 'strict')))

# requests.post(url, json.dumps(json_text), headers={"Content-Type":"application/json;charset=utf-8"})





# x = 10.555
# print(1/8*100)
# f = 12.5
# f = 13.5
# f = (1/8*100)
#
# ff = int(f)
# if ff % 2 == 0:
#     print(round(f+1)-1)
# else:
#     print(round(f))
#
#
# print(round(12.5*100)/100)
# print(round(Decimal("12.5"),0))
# print(Decimal("12.5").quantize(Decimal("0")))
# s = '{"currPage": 0, "deptId": "", "endTime": "", "pageSize": 0, "searchId": "", "searchName": "", "starTime": ""}'
#
# print()














#
# from docx import Document
# from docx.shared import Inches
#
# def test():
#     ...
#
# def tt():
#
#
#
#
# document = Document('demo.docx')
#
# document.add_heading('Document Title', 0)
#
# p = document.add_paragraph('A plain paragraph having some ')
# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True
#
# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='Intense Quote')
#
# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )
#
# document.add_picture('test.jpg', width=Inches(1.25))
#
# records = (
#     (3, '101', 'Spam'),
#     (7, '422', 'Eggs'),
#     (4, '631', 'Spam, spam, eggs, and spam')
# )
#
# table = document.add_table(rows=1, cols=3)
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Qty'
# hdr_cells[1].text = 'Id'
# hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(qty)
#     row_cells[1].text = id
#     row_cells[2].text = desc
#
# document.add_page_break()
#
# document.save('demo.docx')



# for para in document.paragraphs:
#     print(para.text)
#     if 'first' in para.text:
#         for run in para.runs:
#             if 'first' in run.text:
#                 run.text = run.text.replace('first', '金浩')
#
# for t in document.tables:
#     for i in range(len(t.rows)):
#         for j in range(len(t.columns)):
#             print(t.cell(i, j).text)
#             if 'first' in t.cell(i, j).text:
#                 t.cell(i, j).text = t.cell(i, j).text.replace('first', '金浩')
#
#
# document.save('demo.docx')

# import PyV8
# ctxt = PyV8.JSContext()
# ctxt.enter()
# func = ctxt.eval("""
#     (function(){
#         function hello(){
#             return "Hello world.";
#         }
#         return hello();
#     })
# """)
# print(func())

# def test(*var):
#     print(len(var))
#     print(var)


# test("aaa")
# test("aaa","bbb")

# a = {5:[{"member_id":1212}], 6:[{"loan_amount":12},{"loan_":333}] }
# print(a)
# from PO.DataPO import *
# Data_PO = DataPO()
#
# d= {7:[1,2,3],8:["44",66]}
# print(d[8])

# import json
# # str1 = "{'userNo':'$.data','tt':'success','orgno':'\"wgzx\" + str(Data_PO.autoNum(3))'}"
# str1 = '{"userNo":"$.data","tt":"success","orgno":"\'wgzx\' + str(Data_PO.autoNum(3))"}'
# d = json.loads(str1)
# dd = dict(eval(str1))
# print(dd)
# # print(d)
# # print(d['orgno'])
# #
# # x = eval(d['orgno'])
# # print(x)
#
# for k, v in d.items():
#     if "str(" in v:
#         d[k] = eval(d[k])
#
# print(d)

# import json
# dict1 = {}
# # a = {"xx":"select COUNT(*) FROM ep_resident_user"}
# a = '{"xx":"select COUNT(*) FROM ep_resident_user","yy":123}'
# d_a = json.loads(a)
# print(d_a)
# for k,v in d_a.items():
#     print(k,v)
#     test=555
#     dict1[k]= test
#
# print(dict1)

# d= {"a":1, "b":2}
# print(d)
# d["b"]=3
# print(d)
#
# x = '[{"detail": "123123","endTime": "","id": 0,"isDelete": 0,"startTime": "" }]'
#
# dd = '{"a":1, "b":2}'
# import json
#
# target_list = json.loads(dd)
# print(type(target_list))
# print(target_list)

# import functools
#
# def three_way_cmp(x, y):
#     """Return -1 if x < y, 0 if x == y and 1 if x > y"""
#     # return (x > y) - (x < y)
#     return x<y
#
# case = ["1","2","3","10"]
# case.sort(key=functools.cmp_to_key(three_way_cmp))
# print(case)

# def test_1():
#     print("121212")
#
# def test_2():
#     print("99999999999")
#
#
# # for funcType in ('handler', 'request'):
#
#     # a='%s_version'%funcType
# url = eval('test_%s' % range(10))()  ###wval把string变量转换成相应函数



# x = "$.code:200"
# print(len(x.split(",")))
# print(x.split(":")[0])
# print(x.split(":")[1])
#
# a = '$.code:200,$.data.name:"政监中心4"'
# print(len(a.split(",")))
# for i in range(len(a.split(","))):
#     print(a.split(",")[i].split(":")[0])
#     print(a.split(",")[i].split(":")[1])
#

# import jsonpath
#
# dd = {'code': 200, 'msg': 'success', 'data': {'totalCount': 1, 'pageSize': 1, 'totalPage': 1, 'currPage': 1, 'list': [{'id': 16, 'name': '证监自动246更', 'code': 'ZJ0011638780963018', 'responsiblePerson': '张三丰', 'address': '北京市', 'area': '莆田区', 'contactPerson': '北京人', 'contactPhone': '13316161616', 'status': 1}]}}
# iResValue = jsonpath.jsonpath(dd, expr="$.data.list[0].name")
# print(iResValue)




# #
# import textwrap
#
# text = """abcdefg
# hijklmn
# opqrstuvwxyz
# """
#
# print(text)
# #
# # # # # todo: fill() 调整换行符,每行显示给定宽度，注意下一行前会有空格
# print("fill() 调整换行符,每行显示给定宽度".center(100, "-"))
# print(textwrap.fill(text, width=6))
# # # abcdef
# # # g hijk
# # # lmn op
# # # qrstuv
# # # wxyz
#
# # # # todo:dedent() 去除缩进
# print("dedent()去除缩进".center(100, "-"))
# sample_text = '''    aaabbb    cccddd'''
# print(textwrap.dedent(sample_text))
# # # # aaabbb    cccddd
#
# # # # todo:indent() 给定前缀
# print(":indent() 给定前缀".center(100, "-"))
# print(textwrap.indent(text, prefix='----'))
# # ----abcdefg
# # ----hijklmn
# # ----opqrstuvwxyz
#
#
# s = 'hello\n\n \nworld'
#
# # # 默认忽略空白符（包括任何行结束符）组成的行（\n）
# print(textwrap.indent(s, '+ '))
# # + hello
#
# # + world
#
#
# # # 函数对象 = lambda 参数：表达式
# print(textwrap.indent(s, '+ ', lambda line: True))
# # + hello
# # +
# # +
# # + world
#
# #
# # # todo:首行缩进，其余行添加前缀22，每行限制字符10个。
# # print("首行缩进，其余行添加前缀22，每行限制字符10个。".center(100, "-"))
# # # subsequent_indent:初始化除了第一行的所有行
# # detent_text = textwrap.dedent(text).strip()
# # print(textwrap.fill(detent_text, initial_indent='  ', subsequent_indent='22', width=10))
# # #   abcdefg
# # # 22hijklmn
# # # 22opqrstuv
# # # 22wxyz
# #
# #
# # # todo:shorten() 多余的省略号
# # print("shorten() 多余的省略号".center(100, "-"))
# # print(textwrap.shorten(text, width=20))
# # # abcdefg [...]
# # print(textwrap.shorten("Hello world", width=10, placeholder="..."))
# # # Hello...
# #
# # # todo:wrap() 将一个字符串按照width的宽度进行切割，切割后返回list
# # print("wrap() 将一个字符串按照width的宽度进行切割，切割后返回list".center(100, "-"))
# # print(textwrap.wrap(text, width=10))
# # # ['abcdefg', 'hijklmn op', 'qrstuvwxyz']
# # # 分析：结果并不是保证了每个list元素都是按照width的，因为不但要考虑到width，也要考虑到空格（换行），也就是一个单词。
# #
# # sample_text = 'aaabbbcccdddeeeedddddfffffggggghhhhhhkkkkkkk'
# # print(textwrap.wrap(sample_text, width=5))
# # # ['aaabb', 'bcccd', 'ddeee', 'edddd', 'dffff', 'fgggg', 'ghhhh', 'hhkkk', 'kkkk']
# #
# #
# # print("定义 类与实例 textwrap.TextWrapper(…)".center(100, "-"))
# # # 类与实例 textwrap.TextWrapper(…) # 这个类的构造函数接受一系列的关键字参数来初始化自己的属性信息
# # sample_text = '''aaa'''
# # textWrap = textwrap.TextWrapper()
# # textWrap.initial_indent = 'bbb'
# # print(textWrap.wrap(sample_text))
# # # ['bbbaaa']
# #
# # sample_text = '''aaa
# # kkk
# # jjj'''
# # textWrap = textwrap.TextWrapper(width = 2)
# # textWrap.initial_indent = 'bbb'
# # textWrap.subsequent_indent = 'ccc'
# # print(textWrap.wrap(sample_text))
# # # ['bbba', 'ccca', 'ccca', 'ccck', 'ccck', 'ccck', 'cccj', 'cccj', 'cccj']
# #
# #
# #


# a = ["welcome,linuxmi.com,33"]
# for i in a:
#     print(i.count(',') + 1)



# import numpy as np
# # 列表排序
# a = np.array([2,1,0,5])
# print(a)
# print(a[:3])
# print(a.min())
# a.sort()
# print(a)
# b = np.array([1,2,3])
# print(b*b)