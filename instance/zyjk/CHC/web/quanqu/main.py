# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************

import sys,os
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取 上层 目录的绝对路径
project_dir = os.path.abspath(os.path.join(current_dir, '..'))
# 将 上层 目录添加到 sys.path
sys.path.insert(0, project_dir)
from ChcPO_quanqu import *
logName = "./" + os.path.basename(__file__).split('.')[0] + ".log"
Chc_PO_quanqu = ChcPO_quanqu(logName)
from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')
# 登录
Chc_PO_quanqu.login(Configparser_PO.HTTP("url"), Configparser_PO.ACCOUNT("user"), Configparser_PO.ACCOUNT("password"))
d_menu = Chc_PO_quanqu.getMenu2Url()
print('d_menu =', d_menu)
# d_menu = {'首页': 'http://192.168.0.243:8010/#/index', '健康服务': 'http://192.168.0.243:8010/#/SignManage/service', '健康评估及干预': 'http://192.168.0.243:8010/#/SignManage/signAssess', '慢病管理': 'http://192.168.0.243:8010/#/SignManage/chronic', '老年人体检': 'http://192.168.0.243:8010/#/SignManage/snrExam', '重点人群': 'http://192.168.0.243:8010/#/SignManage/keyPopulation', '居民登记': 'http://192.168.0.243:8010/#/OpManage/register', '健康评估': 'http://192.168.0.243:8010/#/OpManage/assess', '机构维护': 'http://192.168.0.243:8010/#/UserManage/org', '用户维护': 'http://192.168.0.243:8010/#/UserManage/user', '角色维护': 'http://192.168.0.243:8010/#/UserManage/role', '接口管理': 'http://192.168.0.243:8010/#/UserManage/interface', '批量评估': 'http://192.168.0.243:8010/#/UserManage/MassAppraisal', '错误日志': 'http://192.168.0.243:8010/#/UserManage/errorLog', '报告模板引用': 'http://192.168.0.243:8010/#/UserManage/templateReference', '报告模板管理': 'http://192.168.0.243:8010/#/UserManage/templateManage', '常住人口': 'http://192.168.0.243:8010/#/Community/permanent', '家医团队维护': 'http://192.168.0.243:8010/#/Community/team', '家医助手': 'http://192.168.0.243:8010/#/Community/assistant', '干预规则配置': 'http://192.168.0.243:8010/#/Community/interveneRule', '打印': 'http://192.168.0.243:8010/#/Community/print', '停止评估名单': 'http://192.168.0.243:8010/#/Community/stopList', '社区用户维护': 'http://192.168.0.243:8010/#/Community/communityUser', '评估建议': 'http://192.168.0.243:8010/#/Community/SuggestionTemplate', '定时任务': 'http://192.168.0.243:8010/#/monitor/index', '社区健康评估': 'http://192.168.0.243:8010/#/dataStatistics/communityHealth', '全区健康评估': 'http://192.168.0.243:8010/#/dataStatistics/allHealth', '全区评估率': 'http://192.168.0.243:8010/#/dataStatistics/allAssessRate', '社区评估率': 'http://192.168.0.243:8010/#/dataStatistics/communityAssessRate', '档案首页': 'http://192.168.0.243:8010/#/HealthRecord/archiveIndex', '居民评估报告': 'http://192.168.0.243:8010/#/HealthManage/AssessReport'}



# import pyautogui
# from bs4 import BeautifulSoup
# from PIL import Image
#
# # 转换图片尺寸，
# def resize_image(input_image_path, output_image_path, size):
#     with Image.open(input_image_path) as image:
#         resized_image = image.resize(size)
#         resized_image.save(output_image_path)

# 如将图片尺寸转换成 1440*900
# resize_image('/Users/linghuchong/Downloads/111.jpg', '/Users/linghuchong/Downloads/222.jpg', (1440, 900))

# 获取屏幕尺寸
# from screeninfo import get_monitors
#
# for monitor in get_monitors():
#     print(f"Width: {monitor.width}, Height: {monitor.height}")
#


# 获取图片的高度和宽度
import cv2, pyautogui
# image = cv2.imread('/Users/linghuchong/Downloads/111.jpg')
# height, width = image.shape[:2]
# print(height, width)







# print(a)

# # 2, 获取首页源码，点击菜单
# html_source = Web_PO.getSource()
# # print(html_source)
#
# # 获取首页上指标名称与值
# print("1，获取首页信息")
# chcWebPO_quan.getTechnicalTarget()
#
# # 首页
# # chcWebPO_quan.clkMenu(html_source, '首页')
#
# # # 居民健康服务
# print("2,点击健康服务")
# chcWebPO_quan.clkMenu(html_source, '健康服务')
# chcWebPO_quan.clkMenu(html_source, '健康评估及干预')
# # 健康评估及干预 - 查询
# # chcWebPO_quan.healthEvaluateIntervene_search({'姓名': '儿童', '身份证': '310101', '人群分类': '老年人', '家庭医生': '测试', '签约日期范围start': '2024-05-01', '签约日期范围end': '2024-05-02', '年度评估状态': '未评估', '管理人群': '高血压', '最近一次评估日期start': '2024-05-03', '最近一次评估日期end': '2024-05-05', '最近一次确认日期start': '2024-05-06', '最近一次确认日期end': '2024-05-07'})
# # chcWebPO_quan.healthEvaluateIntervene_search({'姓名': '儿童', '家庭医生': '测试', '年度评估状态': '预评估'})



# chcWebPO_quan.clkMenu(html_source, '慢病管理')
# chcWebPO_quan.clkMenu(html_source, '老年人体检')
# chcWebPO_quan.clkMenu(html_source, '重点人群')

# 健康管理门诊
# chcWebPO_quan.clkMenu(html_source, '居民登记')
# chcWebPO_quan.clkMenu(html_source, '健康评估')

# 用户中心
# chcWebPO_quan.clkMenu(html_source, '机构维护')
# chcWebPO_quan.clkMenu(html_source, '用户维护')
# chcWebPO_quan.clkMenu(html_source, '角色维护')
# chcWebPO_quan.clkMenu(html_source, '接口管理')
# chcWebPO_quan.clkMenu(html_source, '批量评估')
# chcWebPO_quan.clkMenu(html_source, '错误日志')

# 社区配置
# chcWebPO_quan.clkMenu(html_source, '常住人口')
# chcWebPO_quan.clkMenu(html_source, '家医团队维护')
# chcWebPO_quan.clkMenu(html_source, '家医助手')
# chcWebPO_quan.clkMenu(html_source, '干预规则配置')
# chcWebPO_quan.clkMenu(html_source, '停止评估名单')
# chcWebPO_quan.clkMenu(html_source, '社区用户维护')
# chcWebPO_quan.clkMenu(html_source, '评估建议')

# 系统监控
# chcWebPO_quan.clkMenu(html_source, '定时任务')

# # 统计分析
# chcWebPO_quan.clkMenu(html_source, '社区健康评估')
# # 点击 导出Excel
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div/div[2]/div[1]/div/div[1]/div[2]/button", 2)
# # 模拟按下 command + S 完成保存
# pyautogui.keyDown('command')
# pyautogui.press('s')
# pyautogui.keyUp('s')
# pyautogui.keyUp('command')

# pyautogui.moveTo(x=1033, y=627, duration=1)  # 将鼠标移动到确定按钮的位置
# pyautogui.click()
# 如果需要输入文件名，可以使用pyautogui的类型函数
# pyautogui.typewrite('my_filename')
# 然后点击保存




# chcWebPO_quan.clkMenu(html_source, '全区健康评估')

# 大屏可视化 - 社区中心 (必须放在最后)
# Web_PO.opn(varUrl + "largeScreen/community")
