# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: FTP
# IP：192.168.0.243
# 账号：root
# 密码：Benetech79$#-
# 日志目录：EHR_2.1/logs
# ********************************************************************************************************************

from fabric import Connection

# 建议将ssh连接所需参数变量化
user = 'root'
host = '192.168.0.243'
password = 'Benetech79$#-'
c = Connection(host=f'{user}@{host}',connect_kwargs=dict(password=password))

# 上传文件
c.put('/Users/linghuchong/Downloads/51/Python/project/flask/chc/templates/index.html', '/home/flask_chc/templates/index.html')

# 利用run方法直接执行传入的命令
# c.run('echo $PATH');
# c.run('kill $(pgrep flask)');
# c.run('cd /home/flask_chc/ && FLASK_APP=app.py && flask run --host=0.0.0.0 --port=5000');

c.run('cd /home/flask_chc/ && ./sk.sh')

# a = c.run('cd /usr/local/lib/python3.9/site-packages/ && FLASK_APP=/home/flask_chc/app.py flask run --host=0.0.0.0 --port=5000');
# a = c.run('cd /usr/local/python3/bin && FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000');
# a = c.run('cd /home/flask_chc/ && FLASK_APP=app.py ./usr/local/bin/flask run --host=0.0.0.0 --port=5000');
# c.run('pwd');
# c.run('kill $(pgrep flask)');
# c.run('cd /home/flask_chc/ && flask run --host=0.0.0.0 &');

# c.run('cd /home/flask_chc/ && FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000')
# c.run('FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000')

# FLASK_APP=/home/flask_chc/app.py flask run --host=0.0.0.0 --port=5000


# print(123,a.stdout)
# # stdin, stdout, stderr = ssh.exec_command('kill $(pgrep flask)')

c.close()

# c.run('sh /home/flask_chc/k.sh');
# c.run('export FLASK_APP=app.py && cd /home/flask_chc/ && flask run --host=0.0.0.0 &');
# command = 'export FLASK_APP=app.py && cd /home/flask_chc/ && flask run --host=0.0.0.0 &'  # 根据实际情况调整命令

# import paramiko
#
# # 创建SSH对象
# ssh = paramiko.SSHClient()
#
# # 允许连接不在know_hosts文件中的主机
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# # 连接服务器
# ssh.connect(hostname='192.168.0.243', port=22, username='root', password='Benetech79$#-')
#
# # 执行命令
#
# # stdin, stdout, stderr = ssh.exec_command('sh /home/flask_chc/k.sh')
# # stdin, stdout, stderr = ssh.exec_command('kill $(pgrep flask)')
# # # 获取命令结果
# # result = stdout.read().decode()
# # error = stderr.read().decode()
# # if error:
# #     print("Error: ", error)
# # else:
# #     print("Result: ", result)
#
#
# # stdin, stdout, stderr = ssh.exec_command('home/flask_chc/flask run --host=0.0.0.0 &')
# # stdin, stdout, stderr = ssh.exec_command('cd /home/flask_chc/ && flask run --host=0.0.0.0 &')
# # stdin, stdout, stderr = ssh.exec_command('cd /home/flask_chc/ && flask run --host=0.0.0.0 &')
# stdin, stdout, stderr = ssh.exec_command('cd /home/flask_chc/ && nohup flask run --host=0.0.0.0 &')
# # stdin, stdout, stderr = ssh.exec_command('ls -l')
#
# # command = 'export FLASK_APP=app.py && cd /home/flask_chc/ && flask run --host=0.0.0.0 &'  # 根据实际情况调整命令
# # stdin, stdout, stderr = ssh.exec_command(command)
# #
# # 获取命令结果
# result = stdout.read().decode('utf-8')
# error = stderr.read().decode('utf-8')
#
# if error:
#     print("Error: ", error)
# else:
#     print("Result: ", result)

# # 关闭连接
# ssh.close()

from ftplib import FTP
import time
import tarfile
import os

# import ftplib,socket
# def ftpconnect(ftp_info):
#     ftp = ftplib.FTP(ftp_info[0])
#
#     username = ftp_info[1]
#     passwd = ftp_info[2]
#     ftp.set_pasv(True)
#     ftp.login(username,passwd)
#     return ftp
#
# ftp_info = ['192.168.0.243','root','Benetech79$#-']
# ftp = ftpconnect(ftp_info)
# print(ftp.nlst())


# from ftplib import FTP
#
# # 连接到 FTP 服务器
# ftp = FTP('192.168.0.243')  # 替换为实际的 FTP 服务器地址
# ftp.login(user='root', passwd='Benetech79$#-')  # 输入用户名和密码登录
#
# # 列出 FTP 服务器上的文件列表
# ftp.dir()
#
# # # 进入指定目录
# # ftp.cwd('path')
# #
# # # 从 FTP 服务器下载文件
# # filename = 'name.txt'
# # local_file = open(filename, 'wb')
# # ftp.retrbinary('RETR ' + filename, local_file.write, 1024)
# # local_file.close()
# #
# # # 在 FTP 服务器上上传文件
# # file_to_upload = 'file_to_upload.txt'
# # with open(file_to_upload, 'rb') as f:
# #     ftp.storbinary('STOR ' + file_to_upload, f)
# #
# # # 删除 FTP 服务器上的文件
# # file_to_delete = 'file_to_delete.txt'
# # ftp.delete(file_to_delete)
#
# # 关闭 FTP 连接
# ftp.quit()


# from ftplib import FTP            #加载ftp模块
#
# # 连接到FTP服务器
# ftp = FTP('192.168.0.243')
# # 登录到FTP服务器
# ftp.login("root","Benetech79$#-")
#
# # 执行FTP命令，例如列出当前目录下的文件
# ftp.retrlines('LIST')
#
# # 断开FTP连接
# ftp.quit()

# ftp=FTP()                         #设置变量
# ftp.set_debuglevel(2)             #打开调试级别2，显示详细信息
# ftp.connect("192.168.0.243",22)          #连接的ftp sever和端口
# ftp.login("root","Benetech79$#-")      #连接的用户名，密码
# # print(ftp.getwelcome())            #打印出欢迎信息
# ftp.retrlines('LIST')
# ftp.cwd("cd /home")
# # ftp.cmd("\home")                #进入远程目录
# print(ftp.dir())
# # bufsize=1024                      #设置的缓冲区大小
# # filename="john.txt"           #需要下载的文件
# # file_handle=open(filename,"wb").write #以写模式在本地打开文件
# # ftp.retrbinaly("RETR filename.txt",file_handle,bufsize) #接收服务器上文件并写入本地文件
# ftp.set_debuglevel(0)             #关闭调试模式
# ftp.quit()                        #退出ftp


# from ftplib import FTP
#
# def ftpconnect(host, username, password):
#     ftp = FTP()
#     # ftp.set_debuglevel(2)
#     ftp.connect(host, 21)
#     ftp.login(username, password)
#     return ftp
#
# #从ftp下载文件
# def downloadfile(ftp, remotepath, localpath):
#     bufsize = 1024
#     fp = open(localpath, 'wb')
#     ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
#     ftp.set_debuglevel(0)
#     fp.close()
#
# #从本地上传文件到ftp
# def uploadfile(ftp, remotepath, localpath):
#     bufsize = 1024
#     fp = open(localpath, 'rb')
#     ftp.storbinary('STOR ' + remotepath, fp, bufsize)
#     ftp.set_debuglevel(0)
#     fp.close()
#
# if __name__ == "__main__":
#     ftp = ftpconnect("http://10.111.3.22", "Administrator", "1q2w3e$R")
#     downloadfile(ftp, "e:\engine\john.txt", "c:\john111.txt")
#     #调用本地播放器播放下载的视频
#     # os.system('start "C:\Program Files\Windows Media Player\wmplayer.exe" "C:/Users/Administrator/Desktop/test.mp4"')
#     # uploadfile(ftp, "C:/Users/Administrator/Desktop/test.mp4", "test.mp4")
#
#     ftp.quit()
