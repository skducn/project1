# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# brew install lftp
# lftp -u ftptest,Zy123456 192.168.0.248
# 从ftp下载文件，get test.txt
# 从本地上传文件，put test.txt
# bye关闭
# ***************************************************************u**

from ftplib import FTP

# 连接到FTP服务器
ftp = FTP('192.168.0.248')

# 登录
ftp.login('ftptest', 'Zy123456')

# 查看文件列表
ftp.retrlines('LIST')

# 切换目录
ftp.cwd('10011')
ftp.retrlines('LIST')

# # 下载文件
with open('BC-5180-25-2023-05-17_123.jpg', 'wb') as f:
    ftp.retrbinary('RETR BC-5180-25-2023-05-17.jpg', f.write)
# 关闭连接
ftp.quit()