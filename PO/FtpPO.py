# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2024-10-22
# Description: FTP远程链接
# IP：192.168.0.243
# 账号：root
# 密码：Benetech79$#-
# ********************************************************************************************************************

from fabric import Connection

class FtpPO:

    def __init__(self, varHost, varUser, varPassword):

        # 建议将ssh连接所需参数变量化
        varUser = 'root'
        varHost = '192.168.0.243'
        varPassword = 'Benetech79$#-'
        self.conn = Connection(host=f'{varUser}@{varHost}',connect_kwargs=dict(password=varPassword))

    def upload(self, varLocalPathFile, varRemotePathFile):

        # 上传文件
        # self.conn.put('/Users/linghuchong/Downloads/51/Python/project/flask/chc/templates/index.html', '/home/flask_chc/templates/index.html')
        self.conn.put(varLocalPathFile, varRemotePathFile)


    def run(self, varCommand):

        # 执行命令
        # c.run('cd /home/flask_chc/ && ./sk.sh')
        # c.run('echo $PATH');
        # c.run('kill $(pgrep flask)');
        # c.run('cd /home/flask_chc/ && FLASK_APP=app.py && flask run --host=0.0.0.0 --port=5000');
        self.conn.run(varCommand)

    def close(self):
        self.conn.close()

if __name__ == "__main__":

    Ftp_PO = FtpPO('192.168.0.243','root','Benetech79$#-')
    # Ftp_PO.upload('/Users/linghuchong/Downloads/51/Python/project/flask/chc/templates/index.html', '/home/flask_chc/templates/index.html')
    # Ftp_PO.run('cd /home/flask_chc/ && ./sk.sh')

    Ftp_PO.close()