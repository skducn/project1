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
# pip3 install --upgrade --force-reinstall pyobjc


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


class ZhihuAutoAuth:
    def __init__(self, cookie_path="zhihu_cookies.json"):
        self.driver = webdriver.Chrome()
        self.cookie_path = cookie_path
        self.base_url = "https://www.zhihu.com"
        self.login_url = f"{self.base_url}/signin"
        self.user_home_xpath = '//div[@class="UserProfileHeader"]//a[contains(@href, "/people/")]'

    def _save_cookies(self):
        """保存当前会话的Cookie到文件"""
        with open(self.cookie_path, "w") as f:
            json.dump(self.driver.get_cookies(), f)
        print(f"✅ Cookie已保存到 {self.cookie_path}")

    def _load_cookies(self):
        """从文件加载Cookie并注入浏览器"""
        try:
            with open(self.cookie_path, "r") as f:
                cookies = json.load(f)
                # 过滤无效Cookie（如过期或非当前域）
                valid_cookies = [c for c in cookies if c.get('domain') in self.base_url]
                for cookie in valid_cookies:
                    # 处理Expiry时间（Selenium要求int类型）
                    if 'expiry' in cookie and isinstance(cookie['expiry'], float):
                        cookie['expiry'] = int(cookie['expiry'])
                    self.driver.add_cookie(cookie)
                print(f"✅ 加载{len(valid_cookies)}个有效Cookie")
                return True
        except FileNotFoundError:
            print("❌ 未找到Cookie文件，需手动登录")
            return False

    def _is_logged_in(self):
        """验证是否已登录（通过用户头像元素存在性）"""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, self.user_home_xpath))
            )
            return True
        except:
            return False

    def auth(self, force_login=False):
        """自动鉴权主流程"""
        self.driver.get(self.base_url)

        # 尝试加载本地Cookie（非强制登录时）
        if not force_login and self._load_cookies():
            self.driver.refresh()  # 刷新页面使Cookie生效
            if self._is_logged_in():
                print("🎉 已通过Cookie自动登录")
                return

        # 触发手动登录流程
        print("🔑 开始手动登录（请在30秒内完成）")
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 30).until(
            EC.url_changes(self.login_url)  # 等待登录成功跳转
        )

        # 保存新Cookie
        if self._is_logged_in():
            self._save_cookies()
        else:
            raise Exception("❌ 登录失败，请检查账号密码")

    def close(self):
        self.driver.quit()


# 使用示例
if __name__ == "__main__":
    auth = ZhihuAutoAuth()
    try:
        auth.auth()  # 首次运行需手动登录，后续自动复用Cookie
        # 执行需要登录的操作（例如访问个人主页）
        auth.driver.get(f"{auth.base_url}/people/your-username")
        time.sleep(3)  # 演示停留
    finally:
        auth.close()








# import markdown
#
# # 定义Markdown文本
# markdown_text = "# 标题\n这是一段Markdown文本。"
#
# # 将Markdown文本转换为HTML
# html = markdown.markdown(markdown_text)
#
# print(html)
#
# def text_to_markdown_with_headers(text, header_level=1):
#     lines = text.splitlines()
#     markdown_lines = []
#     for line in lines:
#         if line.strip():
#             header = '#' * header_level + ' ' + line
#             markdown_lines.append(header)
#         else:
#             markdown_lines.append(line)
#     return '\n'.join(markdown_lines)
#
# text = "这是一个标题\n这是正文内容"
# markdown_text = text_to_markdown_with_headers(text)
# print(markdown_text)

#
# import re
#
# def text_to_markdown(text):
#     lines = text.splitlines()
#     markdown_lines = []
#     for line in lines:
#         if re.match(r'^\s*$', line):
#             markdown_lines.append(line)
#         elif re.match(r'^\s*\d+\.\s', line):
#             markdown_lines.append(line)
#         elif re.match(r'^\s*[-+*]\s', line):
#             markdown_lines.append(line)
#         elif len(line) > 0 and line[0].isupper():
#             markdown_lines.append('# ' + line)
#         else:
#             markdown_lines.append(line)
#     return '\n'.join(markdown_lines)
#
# text = "这是一个标题\n这是第一点\n这是第二点"
# markdown_text = text_to_markdown(text)
# print(markdown_text)



# def outer_function(x):
#     def inner_function(y):
#         return x + y
#     return inner_function
#
# closure = outer_function(10)  # 外部函数执行完毕，x 被设置为 10
# closure(5)
# print(closure(5))  # 内部函数仍然可以访问 x，输出 15
# print(closure(5))  # 内部函数仍然可以访问 x，输出 15

# def replace_second(list1, list2):
#     for i in range(len(list2)):
#         if i < len(list1):
#             list2[i][1] = list1[i]
#     return list2
#
#
# list1 = ['a', 'b', 'c']
# list2 = [[1, '', 3], [1, '', 3], [1, '', 3]]
# result = replace_second(list1, list2)
# print(result)

# from AppKit import NSWorkspace, NSRunningApplication, NSTextInputContext
# from Foundation import NSBundle
#
# print("导入成功")
# import objc
# from AppKit import NSWorkspace, NSRunningApplication, NSTextInputContext
# from Foundation import NSBundle
#
# def get_current_input_method():
#     """
#     获取当前输入法
#     :return: 当前输入法的 ID
#     """
#     text_input_context = NSTextInputContext.sharedInputContext()
#     input_method = text_input_context.inputMethod()
#     if input_method:
#         bundle = NSBundle.bundleForClass_(input_method)
#         if bundle:
#             return bundle.bundleIdentifier()
#     return None
#
# def switch_to_english_abc():
#     """
#     切换到英文 ABC 输入法
#     """
#     # 英文 ABC 输入法的 ID
#     english_abc_id = 'com.apple.keylayout.ABC'
#     text_input_context = NSTextInputContext.sharedInputContext()
#     input_methods = text_input_context.availableInputMethods()
#     for method in input_methods:
#         bundle = NSBundle.bundleForClass_(method)
#         if bundle and bundle.bundleIdentifier() == english_abc_id:
#             text_input_context.setInputMethod_(method)
#             break
#
# if __name__ == "__main__":
#     current_id = get_current_input_method()
#     if current_id and 'com.apple.inputmethod.SCIM.ITABC' in current_id:
#         switch_to_english_abc()

# # a = '残\n高\n脂'
# # print(len(a.split("\n")))
# my_dict = {'a': 1, 'b': 2, 'c': 3}
# print(len(my_dict))
# # 使用enumerate遍历字典项
# for index, (key, value) in enumerate(my_dict.items()):
#     print(f"Index: {index}, Key: {key}, Value: {value}")

# from collections import ChainMap
#
# d_global = {
#
#         }
#
# d_1 = {'身份证号': 'shuzi', "33":'44'}
#
# d6 = dict(ChainMap(d_global, d_1))
# print(d6)
#
# dd = {'无':"",'肺炎': '12', '外伤': '44', '其他': "3333"}
# # print(list(my_dict.keys()))  # 将字典的键转换为列表
# # print(list(my_dict.keys())[0])  # 将字典的键转换为列表
#
# if "外3伤" in dd:
#     print(dd['外伤'])

# import qwen
#
# # 初始化 Qwen 实例
# qwen_instance = qwen.Qwen()
#
# # 调用方法
# result = qwen_instance.some_method()
# print(result)

# visitDate = '2025-02-17'
# l_1 = visitDate.split("-")
# l_ = []
# for i in l_1:
#     l_.append(int(i))
# print(l_)

# import os
# from openai import OpenAI
#
# client = OpenAI(
#     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
#     api_key="sk-f3e3d8f64cab416fb028d582533c1e01",
#     # api_key=os.getenv("DASHSCOPE_API_KEY"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
# completion = client.chat.completions.create(
#     model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#     messages=[
#         {'role': 'system', 'content': 'You are a helpful assistant.'},
#         {'role': 'user', 'content': '你是谁？'}],
# )
#
# print(completion.model_dump_json())




# # x = 'multiply'
# # code = "def " + x + "(x, y): return x * y"
# # exec(code)
# # print(multiply(5, 3))  # 输出: 15
#
# func_name = "abc"
# # func_code = f"def {func_name}:\n print('Hello, World!') \n print(x * y) \n"
# func_code = f"def {func_name}(x,y):" \
#             f"print('Hello, World!') " \
#             f"print(x * y) \n"
# exec(func_code)

# 现在可以调用x函数
# abc(2,4)  # 输出: Hello, World!


# import pyautogui
#
#
# # 获取屏幕尺寸
# width, height = pyautogui.size()
# print(width, height)  # 1440 900
#
# # 获取鼠标位置
# x, y = pyautogui.position()
# print(x,y)  # 2512 767
# import ctypes
# from ctypes.util import find_library
# import objc
# from AppKit import NSBundle
# # from Foundation import NSBundleResourceRequest
# from Foundation import NSBundle
#
# # 获取主 bundle
# main_bundle = NSBundle.mainBundle()
# print(main_bundle.bundlePath())  # /Users/linghuchong/miniconda3/envs/py310/bin
#
#
# # 加载CoreServices框架
# CoreServices = NSBundle.bundleWithIdentifier_("com.apple.CoreServices")
# CoreServices.load()
#
# # 找到TISSelectInputMethod的地址
# TISSelectInputMethod = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(CoreServices.functionForName_("TISSelectInputMethod"))
# TISSelectInputMethod.restype = None
# TISSelectInputMethod.argtypes = [ctypes.c_void_p]
#
# # 获取输入法的标识符，例如："com.apple.inputmethod.Pinyin" 是中文拼音输入法
# input_method_identifier = "com.apple.inputmethod.Pinyin"  # 例如切换到中文拼音输入法
# input_method = ctypes.c_void_p(CoreServices.functionForName_("TISCopyCurrentKeyboardInputSource").__call__())
# TISSelectInputMethod(input_method)  # 切换到指定的输入法
#
#



# # from AppKit import NSWorkspace, NSWorkspaceInputMethodIdentifierKey, NSWorkspaceInputMethodDisplayNameKey
# from AppKit import NSWorkspace, NSWorkspaceInputMethodIdentifierKey
#
#
# def get_current_input_method():
#     workspace = NSWorkspace.sharedWorkspace()
#     input_methods = workspace.localizedInputMethods()
#     for method in input_methods:
#         if method[NSWorkspaceInputMethodIdentifierKey] == workspace.activeInputMethodIdentifier():
#             return method[NSWorkspaceInputMethodDisplayNameKey]
#     return None
#
#
# print(get_current_input_method())

import objc
#!/usr/bin/python

# 查找当前活动窗口的应用程序名称?
# from AppKit import NSWorkspace
# activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
# print(activeAppName)

# from AppKit import NSWorkspace, NSLocaleIdentifier, NSLocaleLanguageCode, NSLocaleLanguageName, NSLocaleCountryCode, NSLocaleCountryName
#
# def get_current_input_method_details():
#     workspace = NSWorkspace.sharedWorkspace()
#     input_method_identifier = workspace.activeInputMethodIdentifier()
#     input_method = workspace.inputMethodWithIdentifier_(input_method_identifier)
#     locale = input_method.locale()
#     language_code = locale.objectForKey_(NSLocaleLanguageCode)
#     country_code = locale.objectForKey_(NSLocaleCountryCode)
#     # language_name = locale.displayNameForKey_(NSLocaleLanguageName, value: language_code)
#     # country_name = locale.displayNameForKey_(NSLocaleCountryName, value: country_code)
#     return {
#         "identifier": input_method_identifier,
#         # "language": language_name,
#         # "country": country_name,
#         "locale": locale.localeIdentifier()
#     }
#
# details = get_current_input_method_details()
# print("Current Input Method Details:", details)


# from AppKit import NSWorkspaceInputMethodIdentifierKey
# # NSWorkspaceInputMethodIdentifierKey
#
# workspace = NSWorkspace.sharedWorkspace()
# input_methods = workspace.preferredInputMethods()
#
# for method in input_methods:
#     if NSWorkspaceInputMethodIdentifierKey in method:
#         print(method[NSWorkspaceInputMethodIdentifierKey])


# import subprocess
#
# # 切换到拼音输入法（以拼音输入法标识为例）
# subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke "1" using {command down}'])



# l_date = ['2024-09-30', '2024-10-08', '2024-10-09']
# l_1_date = l_date[0].split("-")
# print(l_1_date)
#
#
# l_date = []
# print(len(l_date))


# import pandas as pd
# import seaborn as sns
# # import jqdata as jq
# import jqdatasdk as jq
# # pip install jqdatasdk
# import numpy as np
# # from jqdata import *
# from jqlib.technical_analysis import *
#
# # 找出涨停板股票并去除ST,停牌股
# security = list(get_all_securities(['stock']).index)
# for stock in security:
#     st=get_extras('is_st', stock, start_date='2024-09-30', end_date='2024-09-30')
#     price = get_price(stock, start_date='2022-12-07', end_date='2022-12-07', fields=['high_limit','high'],skip_paused=False, fill_paused=False)
#     if price.iloc[0,0] == price.iloc[0,1] and st.iloc[0,0] == False:
#         print(stock)

# a = ['高血压', '2025-01-07', '糖尿病', '2025-01-01', 'shou1', '2025-01-13', 'shou55', '2025-01-07', 'wai2', '2025-01-08', 'shu3', '2025-01-30']
# lst = ['', '有\n无','','']
# lst_filtered = [i for i in lst if i][0]
# print(lst_filtered)
#
# a = ['25', '26', '27', '28', '29', '30', '1']
# a = [int(i) for i in a]
# a = [0 if i > 10 else i for i in a]
# print(a)
#
# import os
#
# # 获取CPU核数
# cpu_count = os.cpu_count()
# print(f"CPU cores: {cpu_count}")
# import psutil
#
#
#
# def get_cpu_cores_psutil():
#     return psutil.cpu_count()
#
# if __name__ == "__main__":
#     print(f"Number of CPU cores: {get_cpu_cores_psutil()}")
#
#
# import multiprocessing
#
# def get_cpu_cores_multiprocessing():
#     return multiprocessing.cpu_count()
#
# if __name__ == "__main__":
#     print(f"Number of CPU cores: {get_cpu_cores_multiprocessing()}")


# import sys
# print(sys.version_info)
#
# if sys.version_info < (3,8,16,"final",1):
#     print("121212")
# else:
#     print(0000)


# # psutil 是一个跨平台库，用于轻松获取系统运行的进程和系统利用率（CPU、内存、磁盘、网络等）信息。
# import psutil
# # 获取CPU使用率
# cpu_usage = psutil.cpu_percent(interval=1)
# print(f'CPU Usage: {cpu_usage}%')
# # 获取内存使用率
# memory_info = psutil.virtual_memory()
# print(f'Total Memory: {memory_info.total / (1024 ** 3):.2f} GB')
# print(f'Available Memory: {memory_info.available / (1024 ** 3):.2f} GB')
#
#
# import platform
# # 获取操作系统信息
# system = platform.system()
# version = platform.version()
# architecture = platform.architecture()
# print(f'System: {system}')
# print(f'Version: {version}')
# print(f'Architecture: {architecture}')

# import itchat
# itchat.auto_login(hotReload=True)
#
# # 获取好友列表
# friends = itchat.get_friends(update=True)
#
# for friend in friends:
#     print(friend['NickName'])


# def deduplication(varList):
#     # 5.5 列表元素去重
#
#     return sorted(set(varList), key=varList.index)
#
# d = ['30%', '35%', '40%', '30%', '35%', '40%', '30%', '35%', '40%', '30%', '35%', '40%', '45%', '35%', '40%', '45%', '50%', '55%', '45%', '50%', '55%', '60%', '45%', '50%', '55%', '60%', '65%', '50%', '55%', '60%', '65%', '55%', '60%', '65%', '70%']
#
# print(deduplication(d))


# print(list(d.keys()))
# # a = list(d.keys())
# a.remove('主席')
# print(a)
#
# # print(d['222'])
# print(d.get('主席'))
# a = ['医院\n金泽社区\n科室\n检验科\n会议类型\n会议计划时间\n实际会议时间\n请注意实际会议时间提交后不可调整\n实际劳务费用\n元\n实际餐费\n元\n场地费\n元\n会中执行清单\n已勾选0项目\n实际参会者\n实际参会者共0人\n计划参会者\n新增参会者']
# a = a[0].split("\n")
# print(a)
# for i in a:
#     if "实际参会者共" in i:
#         print(i)
#         a = i.split("实际参会者共")[1].split("人")[0]
#         print(a)
#         if a == 0

#
# print([i.split("\n")[0] for i in a])
#
# varList = [1,2,3,4,3,2,3]
# print(sorted(set(varList), key=varList.index))
#
# print([item for item in varList if varList.count(item) == 1])


# from collections import Counter
#
# a = [1,2,"你好",3]
# b = [2,1,3,"你好"]
#
# # a = Counter(a)
# # b = Counter(b)
# print (dict(Counter(a))==dict(Counter(b)))
# if dict(Counter(a)) != dict(Counter(b)):
#     print(123)
#
# a = "你"
# print(a[0])
# print(a[1:])
#
# print(len(a))
# a = '临床主任确认即可过会, 需投票，过三分之二票数'
#
# print(a.split(", "))


# a = {'科室主任': {'李标': '支持'}}
#
# print(list(a['科室主任'].values())[0])
# l_post = ["rr","gg","Vv"]
# for index, k in enumerate(l_post, start=1):
#     print(index, k)
#
# for index, i in enumerate({'郭震': '支持', '杨忠英': '反对', '陈健': '中立'}, start=2):
#     print

# a = ['HCO00000122-崇中心', '氨叶-CP102', '薛伟、彭琦', '韦彩雯', '支持', '杨忠英', '支持']
#
# a.pop(0)
# a.pop(0)
# a.pop(0)
# print(a)

# l_field = ['医院信息', '产品信息', '负责人', '开发次数', '提单科室', '提单规则', '提单状态', '药剂科会前确认信息', '药事会计划开始日期', '药事会计划结束日期', '药事会实际召开时间',
#            '会前评估能否过会', '经改进后能否过会', '过会日期']
#
# l_ = ['HCO00000001-曹路社区', '恒康正清-CP107', '薛伟、', '二次开发', '神外', '可随时提单', '可随时提单，已承诺', '已收到报告，确认上会', '2025-07-10 ', '2025-11-10 ', '2024-12-12 12:12:00', '否', '是', '2025-07-10', '']
# l_value = l_[:-1]
# print(l_value)
#
# d_dev = dict(zip(l_field, l_value))
# print(d_dev)

#
# def fibonacci(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fibonacci(n - 1) + fibonacci(n - 2)
# print(fibonacci(10))  # 输出: 55
#
# a= 10
# b =3
#
# def hello(a,b):
#
#     if a != b:
#         b = b + 1
#         print(b)
#         return hello(a,b)
#     else:
#         return 1
#
# print(hello(10, 3))


# {'医院信息': 'HCO00000001-曹路社区', '产品信息': '恒康正清-CP107', '负责人': '薛伟、', '开发次数': '二次开发', '提单科室': '神外', '提单规则': '可随时提单',
# '提单状态': '可随时提单，已承诺', '药剂科会前确认信息': '已收到报告，确认上会', '药事会计划开始日期': '2025-07-10 ', '药事会计划结束日期': '2025-11-10 ',
# '药事会实际召开时间': '2024-12-12 12:12:00', '会前评估能否过会': '否', '经改进后能否过会': '是', '过会日期': '2025-07-10'}

import sys

# for i in range(8):
#     print(i)
# d= {}
# a = [2014, 1, 1]
# b = ["".join(str(x)) for x in a]
# c = ("-".join(["".join(str(x)) for x in a]))
# print(c)
# 1.7 元素转字符串 print(",".join(['John', 'Doe', 'Jack', 'Bob', 'Smith']))  # John,Doe,Jack,Bob,Smith


# a = '拜访达成统计排名\n2024-12-06 至 2024-12-06\n团队排名\n个人排名\n薛伟团队\n浦东/闵行/徐汇\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%\n陈东升团队\n奉贤/金山\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%\n【空岗】团队\n静安/闵行/徐汇\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%\n钮学彬团队\n静安/普陀/闸北/长宁\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%\n张慧涛团队\n闵行/松江\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%\n陈似锦团队\n青浦\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%\n刘挺团队\n宝山/黄埔/崇明\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%\n饶顺荣团队\n虹口/杨浦\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%\n王桂花团队\n耗材经理岗\n指标达成分数：0.00\n实地工作拜访完成率\n0.00%\n定位匹配率\n0.00%\n双A客户达成率\n0.00%\n高潜客户达成率\n0.00%'
#
# a = '1指标达成分数2指标达成分数3指标达成分数4'
#
# print(len(a.split("指标达成分数")))

# print([int(x) for x in str(12345)])  # [1, 2, 3, 4, 5]
#
# a = 'abcddfdrer'
# print([str(x) for x in str('abcddfdrer')])  # ['a', 'b', 'c', 'd', 'd', 'f', 'd', 'r', 'e', 'r']
# print({int(x) for x in str(a)})
# print('（{}）'.format(sys._getframe().f_lineno))

# d = {"唐晓晶": "支持", "刘月月": "反对"}
#
# for i,k in enumerate(d):
#     print(i,k)


# del d['其他药事会成员']['唐晓晶']
# print(d)
# print(len(d['其他药事会成员']))
#
# print(d['其他药事会成员'][list(d['其他药事会成员'].keys())[0]])


# def PRINT(string):
#     print('func:{}(),line:{},'.format(sys._getframe().f_code.co_name, sys._getframe().f_lineno), end="")
#     # /print('调用该函数的上级为{}'.format(sys._getframe(1).f_code.co_name))
#     print(string)
#
# PRINT("help :%d" % 123654)



# d_ = {'HDL':{'TB_DC_DM_VISIT':{'今天往前一年内的日期':'2024-10-01','今天往前一年内的日期1':'2024-10-02','result':2,'result1':'2','maxvisitdate':'2024-10-02'},
# 'TB_DC_HTN_VISIT':{'今天往前一年内的日期':'2024-10-03','今天往前一年内的日期1':'2024-10-04','result':4,'result1':'4','maxvisitdate':'2024-10-04'},
# 'TB_DC_EXAMINATION_INFO':{'今天往前一年内的日期':'2024-10-05','今天往前一年内的日期1':'2024-10-06','result':6,'result1':'6','maxvisitdate':'2024-10-06'}
# }}
#
# print(list(d_.get('HDL')))

# import datetime
# d_ = {datetime.datetime(2024, 10, 2, 0, 0): '2', datetime.datetime(2024, 10, 4, 0, 0): '4', datetime.datetime(2024, 10, 6, 0, 0): '6', datetime.datetime(2024, 10, 8, 0, 0): '8', datetime.datetime(2024, 10, 10, 0, 0): '10'}
# 
# l_ = list(d_.keys())
# dt_tmpDate = datetime.datetime(2024, 1, 1, 0, 0)
# for dt_date in l_:
#     if dt_tmpDate < dt_date:
#         dt_tmpDate = dt_date
# print(dt_tmpDate)
# print(d_[dt_tmpDate])

# -*- coding: utf-8 -*-
# @Time    : 2020/3/17 17:29
# @Author  : felix
# @File    : idNumber.py
# @Software: PyCharm

# import random
#
#
# def getIdcard(birthyear, birthmonth, birthday):
#     # 预设地区:
#     codelist = ["110101", "110102", "110105", "110106", "110107", "420117", "420200", "420202", "420203", "420204",
#                 "420205", "420222"]  # 随便设置了几个地区，基本都是湖北和北京的；
#     weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
#     checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
#                  '10': '2'}  # 校验码映射
#
#     #身份证前6位
#     try:
#         id = codelist[random.randint(0,len(codelist))] #地区项
#     except:
#         id = "110101"
#
#     #7-10位，出生年份
#     try:
#         birthdayStr = str(birthyear).zfill(4)+str(birthmonth).zfill(2)+str(birthday).zfill(2)
#         id = id + birthdayStr
#     except:
#         id = id + "19900101"
#
#     #最后4位的随机前3位
#     sex = ""
#     try:
#         sign = random.randint(1,999)
#         if sign%2 == 0:
#             sex = "女"
#         else:
#             sex = "男"
#         id = id + str(sign).zfill(3) #顺序号简单处理
#     except:
#         id = id + "999"
#     #判断性别
#
#     sum_1 = 0
#     for a in range(17):
#         sum_1 = sum_1+int(id[a])*weight[a]
#     index_id = sum_1%11
#     result_id = id + str(checkcode[str(index_id)])  #最终号码
#     return (result_id,sex)
#
# if __name__ == '__main__':
#     # birthyear = input("请输入出生年（例如：1990）： ")
#     # birthmonth = input("请输入出生月（例如：10）： ")
#     # birthday = input("请输入出生日（例如：2）： ")
#     (id,sex) = newIdNum('1950','12','12')
#     print("身份证号码为：%s，性别：%s" %(id,sex))

# l = []
# l.append("BV1HV41197iW")
# l.append("BV1qK4y1i7JL")
# print(l)


# d = {"a":1 , "b":3}
# for i in d:
#     print(i)

# import os, datetime, sys
# from datetime import date, datetime, timedelta
# from fabric import Connection
# # 建议将ssh连接所需参数变量化
# user = 'root'
# host = '192.168.0.243'
# password = 'Benetech79$#-'
# c = Connection(host=f'{user}@{host}',connect_kwargs=dict(password=password))
# r = c.run('cd /home/flask_chc/ && sh ./sk.sh')

# s = "12 delete test "
# s = s.split(" select ")[1]
# s = "select " + s
# print(s)


# from fabric.api import run, env
#
# env.hosts = ['example1.com', 'example2.com']
# env.user = 'bjhee'
# env.password = '111111'
#
# def hello():
#     run('ls -l /home/bjhee/')


# import datetime
# import os
# import time,datetime
#
# # 获取日期的时间戳
# date_obj = datetime.datetime.strptime("2024-10-28", "%Y-%m-%d")
# timestamp = date_obj.timestamp()
# print(timestamp)  # 1730044800.0
#
# # 获取当前目录下的所有子目录
#
# def getSubFolder(s_localPath, s_localPath2):
#     # 获取本地指定目录下所有目录及子目录
#     l_path_subFolder = []
#     l_local_folder = []
#     for entry in os.listdir(s_localPath):
#         s_varPath_file = os.path.join(s_localPath, entry)
#         if os.path.isdir(s_varPath_file):
#             l_path_subFolder.append(s_varPath_file)
#             l_path_subFolder.extend(getSubFolder(s_varPath_file, s_localPath2))  # 递归调用
#     # 过滤掉前缀路径，如 /Users/linghuchong/Downloads/51/Python/project/flask/chc
#     for i in l_path_subFolder:
#         if ".idea" not in i:
#             l_local_folder.append(i.replace(s_localPath2,""))
#     return l_local_folder
#
#
#
# l_sub = getSubFolder('/Users/linghuchong/Downloads/51/Python/project/flask/chc','/Users/linghuchong/Downloads/51/Python/project/flask/chc')
# print(l_sub)  # ['/Users/linghuchong/Downloads/51/Python/project/flask/chc/__pycache__',。。。。
#
# for s_path, l_folder, l_file in os.walk("/Users/linghuchong/Downloads/51/Python/project/flask/chc/static/215447"):
#     print(s_path, l_file)
#
#
# # print(111,l_folder)
#
#
# def get_newest_directory(path):
#     newest = (0, None)
#     for dirname in os.listdir(path):
#         full_path = os.path.join(path, dirname)
#         if os.path.isdir(full_path) and os.path.getctime(full_path) > newest[0]:
#             # print(os.path.getctime(full_path))
#             newest = (os.path.getctime(full_path), full_path)
#             print(newest)
#     return newest[1]


# for i in l_subdirectories:
#     newest_directory = get_newest_directory(i)
#     print(f"最新创建的目录是: {newest_directory}")


# date = os.path.getatime('/Users/linghuchong/Downloads/51/Python/project/flask/chc/static/12')
# print(date)
#
# aa = time.ctime(date)
# print(aa)


# 遍历本地目录与服务器目录，如果服务器上没有则复制本地目录到服务器目录（包含内部目录与文件）
# 遍历本地文件，如果当天修改过则复制到服务器


# # 使用示例
# for s_path, l_folder, l_file in os.walk("/Users/linghuchong/Downloads/51/Python/project/flask/chc"):
#     print(l_folder)
#     # directory_path = '/Users/linghuchong/Downloads/51/Python/project/flask/chc/static'  # 替换为你的目录路径
#     newest_directory = get_newest_directory(l_folder)
#     print(f"最新创建的目录是: {newest_directory}")





# from collections import Counter
#
#

# l_subdirectories = get_subdirectories('/Users/linghuchong/Downloads/51/Python/project/flask/chc')
# print(l_subdirectories)  # ['/Users/linghuchong/Downloads/51/Python/project/flask/chc/__pycache__',。。。。


# # print(datetime.now())
# def getDateByFile(varPath, varFile):
#     # 获取文件的最后修改日期和时间
#
#     file_path = varPath + "/" + varFile
#     # print(file_path)
#     # file_path = '/Users/linghuchong/Downloads/51/Python/project/PO/data/1.jpg'  # 文件路径
#     dateTime = datetime.fromtimestamp(os.path.getmtime(file_path))  # 将修改时间转换为日期格式
#     l_ = str(dateTime).split(' ')
#     # print(l_)  # ['2023-11-15', '15:56:34.431144']
#     if l_[0] == str(date.today()):
#         # print(varPath, varFile, "更新文件")  # /Users/linghuchong/Downloads/51/Python/project/flask/chc/templates index.html 更新文件
#         # 上传文件
#         varPath1 = varPath.replace("/Users/linghuchong/Downloads/51/Python/project/flask/chc","")
#         print(varPath + "/" + varFile, '/home/flask_chc' + varPath1 + "/" + varFile) # /Users/linghuchong/Downloads/51/Python/project/flask/chc/app.py /home/flask_chc/app.py
#         # c.put(varPath + "/" + varFile, '/home/flask_chc' + varPath1 + "/" + varFile)
#
#
# # 遍历所有的文件
# for s_path, l_folder, l_file in os.walk("/Users/linghuchong/Downloads/51/Python/project/flask/chc"):
#     for i in l_file:
#         if i != ".DS_Store" and i != "workspace.xml":
#             getDateByFile(s_path, i)
#
# # c.run('cd /home/flask_chc/ && ./sk.sh')




# # 将key插入第一个前面
# def insertFirst(varDict,key,value):
#     lis = list(varDict.items())
#     lis.insert(0, (key,value))
#     return dict(lis)
#
# dict1 = {'a':1, 'b':2, 'd':4, 'e':5}
# dict1 = insertFirst(dict1,'c',3)
# print(dict1)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
#
# # 将key插入某个key后
# def insertPosition(varDict,pre_key,key,value):
#     # 插入到 pre_key 关键字 的后面
#     lis = list(varDict.items())
#     lis.insert([*varDict].index(pre_key)+1,(key,value))
#     return dict(lis)
#
# dict1 = {'a':1, 'b':2, 'd':4, 'e':5}
# dict1 = insertPosition(dict1,'e','c',3)
# print(dict1)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}



# from collections import OrderedDict
#
# # 创建一个空的有序字典
# ordered_dict = OrderedDict()
# ordered_dict = {'result': '结果', 'updateDate': '更新日期'}
#
# ordered_dict['id']=123
# print(ordered_dict)

# from PO.CharPO import *
# Char_PO = CharPO()
#
# d_ruleName_tbl = {}
# l_ruleName = ['评估因素取值','健康干预_已患疾病单病', '健康干预_已患疾病组合']
# for i in l_ruleName:
#     d_ruleName_tbl[i] = 'a_' + Char_PO.chinese2pinyin(i)
#
# print(d_ruleName_tbl)

# l_ruleName = ['评估因素取值','健康干预_已患疾病单病', '健康干预_已患疾病组合']
#
# if "健康干预_已患疾病" in l_ruleName:
#     print(123)
# else:
#     print("rwerwer")


# a = "1 select GUID from TB_EMPI_INDEX_ROOT where IDCARDNO = '520300198802242314'2 DELETE FROM TB_DC_EXAMINATION_INFO WHERE GUID = '16644766'"
# 3 DELETE FROM TB_DC_DM_VISIT  WHERE CARDID = '520300198802242314'
# 4 DELETE FROM TB_PREGNANT_MAIN_INFO WHERE ZJHM ='520300198802242314'
# 5 DELETE FROM TB_DC_HTN_VISIT WHERE CARDID ="
# a = "INSERT INTO [dbo].[TB_PREGNANT_MAIN_INFO] ([YCFID], [JCH], [XM], [ZJHM], [CSRQ], [MCYJ], [SG], [YQTZ], [SSY], [SZY], [LRRQ], [JCRQ], [GLSQ], [CJSJ]) VALUES ('{随机11}', '13', '张美丽','520300198802242314', '2016-12-02', '2024-08-08', 168.00, 67.00, '123', '67', '2024-09-12', '2024-09-14', '2024-01-12','{昨天日期}')"
#
# import re
# # b = a.lower()
# # b.split()
#
# # print(b)
#
# # text = "This is a test sentence with words in between"
# pattern = r"from\s(\w+)\swhere"
# matches = re.findall(pattern, a, re.I)
# print(matches)
#
# import socket
#
# print(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
#
#
# def get_current_ip():
#
#     # 获取本机主机名
#     hostname = socket.gethostname()
#     # 根据主机名获取本机IP地址
#     ip_address = socket.gethostbyname(hostname)
#     return ip_address
#
# print(get_current_ip())

# a = {'MCYJ': '123'}
# b = {'hello': '456'}
#
# a.update(b)
# print(a)

# a = ('', None, '', 's1', 'negative', None, 'GY_YH002001', 'YH_JB002', '糖尿病', '舒阳阳', 4)
# l = []
# for i in a:
#     if i == None:
#         i = ''
#     l.append(i)
# b = tuple(l)
# print(b)


# l_1 =['脑卒中', '慢性肾脏病']
# l_2 =['高血压', '糖尿病', '脑卒中', '慢性肾脏病', '慢性阻塞性肺疾病', '肺癌', '结直肠癌', '乳腺癌']
#
#
# l_1 = [x for x in l_2 if x not in l_1]  # 两个列表中都存在
# print(l_1)

# import random
# s_prefixICD = random.sample(l_1, 2)
# print(s_prefixICD)


# a = [x for x in l_1 if x in l_2]  # 两个列表中都存在
# return [y for y in (varList1) if y not in a], [y for y in (varList2) if y not in a]

#
# d = {'prefixICD': {'高血压': 'I12'}}
# d['prefixICD']['高血压'] = '33'
# print(d)

# varSign = 0
# d_total = {'GUID': '65209815', 'YH_JB001': 1, 'YH_JB002': 1, 'GY_YHZH078001': 1}
# l_diseaseRuleCode = ['YH_JB001','YH_JB002','GY_YHZH078001']
# for i in l_diseaseRuleCode:
#     if i in d_total.keys():
#         if d_total[i] == 1:
#             varSign = varSign + 0
#         else:
#             varSign = varSign + 1
# print(varSign)

# d = {'N03': 'ok', 'N11': 'ok'}
# print(list(d.values()))
#
# if "error" in list(d.values()):
#     print(111)
# else:
#     print(999)

# a = None
#
# print(type(a))
# print(type(''))
#
# if isinstance(a, str):


# l = ['     jinhao\r', '\r', 'yoyo\r', '\r', '\r', '\r', '\r', '\r', '     ///     \r', '\r', '\r', '\r', '\r', 'titi\r', '\r', '']
# print([i.replace('\r', '') for i in l])
#
# l2 = [i.replace('\r', '') for i in l]
# l3 = [i.strip() for i in l2 if i != '']
# print(l3)

# print( [l2.remove(i) for i in l2 if i == ''])



# d_param = {'CZRYBM': '1100', 'CZRYXM': '自动化', 'JMXM': '杨莹'}
# for i, v in enumerate(list(d_param.keys())):
#     if 'CZRYXM' == v:
#         print(list(d_param.values())[i])

#         break
# a = {"CZRYBM":123, "CZRYXM":456}
# for i,v in enumerate(list(a.keys())):
#     if 'CZRYXM' == v :
#         print(list(a.values())[i])

# a = {'tb%':['id', 'page']}
# print(list(a.keys())[0])
#
# a = [{'COLUMN_NAME': 'id', 'DATETIME_PRECISION': "55"},{'name': 'jin', 'age': "525"}]
# b = [{'test': '77', 'hello': "123"},{'yellow': '727', 'color': "4545"}]
#
# print(len(a))
#
# for i in range(len(a)):
#     print(a[i])
#     a[i].update(b[i])
# print(a)



#
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