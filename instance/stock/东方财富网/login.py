# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2026-01-7
# Description: 每日板块涨幅 登录
# https://quote.eastmoney.com/zixuan/lite.html
# 获取每个组列表页数据，保存到文件
# *****************************************************************

from PO.WebPO import *


def login_eastmoney(web_po_instance):
    """
    东方财富网登录流程封装
    :param web_po_instance: WebPO实例
    """
    web_po_instance.openURL("https://quote.eastmoney.com/zixuan/lite.html")
    web_po_instance.clkByX("/html/body/div[7]/img[1]", 1)  # 广告
    web_po_instance.clkByX("/html/body/div[1]/div/div[2]/div[2]/div/a[1]", 3)  # 登陆
    web_po_instance.swhIframeById("frame_login")
    web_po_instance.moveLabel('//*[contains(text(), "账号登录") and not(contains(text(), "扫码"))]')   # 移动到登陆标签
    web_po_instance.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[1]/input", "13816109050")
    web_po_instance.setTextEnterByX("/html/body/div/div[2]/div/form[1]/div/div[2]/input", "Jinhao123")
    web_po_instance.clkByX("/html/body/div/div[2]/div/form[1]/div/div[4]/div/img[1]", 2)  # 勾选
    web_po_instance.clkByX("/html/body/div/div[2]/div/form[1]/div/div[3]/div[1]/div/div[4]/div/div", 2)  # 验证点击
    web_po_instance.quitIframe(2)

def create_logged_web_instance(browser_type="chrome"):
    """
    创建并返回已登录的WebPO实例
    :param browser_type: 浏览器类型
    :return: 已登录的WebPO实例
    """
    web_po = WebPO(browser_type)
    login_eastmoney(web_po)
    return web_po

