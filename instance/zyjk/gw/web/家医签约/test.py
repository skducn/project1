# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2025-3-25
# Description: 基本公卫 - 家医签约 - 归档记录
# *****************************************************************
from GwPO_sign import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Gw_PO_sign = GwPO_sign(logName, '归档记录')

protected_url = "http://192.168.0.203:30080/Sign/jmsign/qyfile"
# 保存 Cookies 的文件路径
cookies_file = "cookies.json"

# from PO.WebPO import *
# Web_PO = WebPO("chrome")
# print(type(Web_PO.driver))

# a = Web_PO.current_url
# print(a)
# 尝试加载保存的 Cookies
# Gw_PO_sign.load_cookies(Web_PO, cookies_file)

# 重新加载页面以应用 Cookies
# driver.get(protected_url)
# Web_PO.openURL2(protected_url, cookies_file)

# # 检查是否成功登录
# if "login" in driver.current_url:
#     print("需要手动登录。请在浏览器中完成登录操作。")
#     # 等待用户手动登录
#     input("登录完成后按回车键继续...")
#     # 保存新的 Cookies
#     save_cookies(driver, cookies_file)
#     # 重新加载受保护页面
#     driver.get(protected_url)

