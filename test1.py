a= list(enumerate(['Spring', 'Summer', 'Fall', 'Winter'], start=1))
print(a)


# {"Spring":0,"Summer":1}

# 导入达梦驱动
import dmPython

# ========== 1. 建立数据库连接 ==========
# 核心参数：user(用户名), password(密码), server(数据库地址), port(端口默认5236)
conn = dmPython.connect(
    user="SYSDBA",        # 你的达梦用户名，管理员是SYSDBA，自建用户写自己的
    password="dameng123", # 你的数据库密码，安装时设置的
    server="localhost",   # 本地写localhost，远程写服务器IP
    port=5236,            # 达梦默认端口，固定5236，不要改
    autoCommit=False      # 事务自动提交，默认False，建议手动控制
)

print("数据库连接成功！")
