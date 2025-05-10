# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2019-1-8
# Description: ChainMap
# ********************************************************************************************************************

import re
import random


def generate_all_cases(conditions, num_samples=1):
    """
    生成所有4种可能的条件组合情况

    参数:
    conditions (list): 条件列表，例如 ['BMI>=24', '年龄>=18', '年龄<65']
    num_samples (int): 每种情况生成的样本数量

    返回:
    dict: 包含4种情况的样本字典
    """
    # 分离BMI和年龄条件
    bmi_conditions = [c for c in conditions if c.startswith('BMI')]
    age_conditions = [c for c in conditions if c.startswith('年龄')]

    # 生成每种情况的样本
    d_ = {
        "satisfied": [generate_sample(bmi_conditions, age_conditions, True, True) for _ in range(num_samples)],
        "not1": [generate_sample(bmi_conditions, age_conditions, True, False) for _ in range(num_samples)],
        "not2": [generate_sample(bmi_conditions, age_conditions, False, True) for _ in range(num_samples)],
        "not3": [generate_sample(bmi_conditions, age_conditions, False, False) for _ in range(num_samples)]
    }

    # d_ = {'satisfied': [(53.0, 25)], 'not1': [(37.4, 110)], 'not2': [(23.2, 56)], 'not3': [(60.1, 15)]}
    # 打印结果
    for case_name, samples in d_.items():
        print(f"\n情况: {case_name}")
        for i, (bmi, age) in enumerate(samples, 1):
            print(f"样本 {i}: BMI = {bmi}, 年龄 = {age}")


        # s = {"satisfied": {'BMI': '24.6', '年龄': '49'},
        #      "not": [{'BMI': '24.6', '年龄': '49'}, {'BMI': '24.6', '年龄': '49'}]}

    # "BMI和年龄都满足": [generate_sample(bmi_conditions, age_conditions, True, True) for _ in range(num_samples)],
        # "满足BMI，不满足年龄": [generate_sample(bmi_conditions, age_conditions, True, False) for _ in
        #                 range(num_samples)],
        # "不满足BMI，满足年龄，": [generate_sample(bmi_conditions, age_conditions, False, True) for _ in
        #                  range(num_samples)],
        # "BMI和年龄都不满足": [generate_sample(bmi_conditions, age_conditions, False, False) for _ in
        #                range(num_samples)]





def generate_sample(bmi_conditions, age_conditions, satisfy_bmi, satisfy_age):
    """
    生成一个符合指定条件组合的样本

    参数:
    bmi_conditions (list): BMI相关条件
    age_conditions (list): 年龄相关条件
    satisfy_bmi (bool): 是否满足BMI条件
    satisfy_age (bool): 是否满足年龄条件

    返回:
    tuple: (BMI, 年龄)
    """
    # 生成BMI值
    if satisfy_bmi:
        bmi = generate_valid_bmi(bmi_conditions)
    else:
        bmi = generate_invalid_bmi(bmi_conditions)

    # 生成年龄值
    if satisfy_age:
        age = generate_valid_age(age_conditions)
    else:
        age = generate_invalid_age(age_conditions)

    return (bmi, age)


def generate_valid_bmi(conditions):
    """生成符合所有BMI条件的值"""
    bmi_min = 10.0
    bmi_max = 60.0

    for condition in conditions:
        match = re.match(r'BMI([<>=]+)(\d+)', condition)
        if not match:
            continue

        operator, value = match.groups()
        value = float(value)

        if operator == '>':
            bmi_min = max(bmi_min, value + 0.1)
        elif operator == '>=':
            bmi_min = max(bmi_min, value)
        elif operator == '<':
            bmi_max = min(bmi_max, value - 0.1)
        elif operator == '<=':
            bmi_max = min(bmi_max, value)

    return round(random.uniform(bmi_min, bmi_max), 1)


def generate_invalid_bmi(conditions):
    """生成不符合所有BMI条件的值"""
    if not conditions:
        return round(random.uniform(10.0, 60.0), 1)

    # 计算所有BMI条件的有效范围
    bmi_min = 10.0
    bmi_max = 60.0

    for condition in conditions:
        match = re.match(r'BMI([<>=]+)(\d+)', condition)
        if not match:
            continue

        operator, value = match.groups()
        value = float(value)

        if operator == '>':
            bmi_min = max(bmi_min, value + 0.1)
        elif operator == '>=':
            bmi_min = max(bmi_min, value)
        elif operator == '<':
            bmi_max = min(bmi_max, value - 0.1)
        elif operator == '<=':
            bmi_max = min(bmi_max, value)

    # 如果有效范围存在，生成范围外的值
    if bmi_min <= bmi_max:
        # 有效范围外有两个区间：[10.0, bmi_min) 和 (bmi_max, 60.0]
        if random.random() < 0.5:
            # 选择下界区间
            return round(random.uniform(10.0, bmi_min - 0.1), 1)
        else:
            # 选择上界区间
            return round(random.uniform(bmi_max + 0.1, 60.0), 1)
    else:
        # 条件矛盾，所有值都不符合条件
        return round(random.uniform(10.0, 60.0), 1)


def generate_valid_age(conditions):
    """生成符合所有年龄条件的值"""
    age_min = 0
    age_max = 120

    for condition in conditions:
        match = re.match(r'年龄([<>=]+)(\d+)', condition)
        if not match:
            continue

        operator, value = match.groups()
        value = float(value)

        if operator == '>':
            age_min = max(age_min, value + 1)
        elif operator == '>=':
            age_min = max(age_min, value)
        elif operator == '<':
            age_max = min(age_max, value - 1)
        elif operator == '<=':
            age_max = min(age_max, value)

    return random.randint(int(age_min), int(age_max))


def generate_invalid_age(conditions):
    """生成不符合所有年龄条件的值"""
    if not conditions:
        return random.randint(0, 120)

    # 计算所有年龄条件的有效范围
    age_min = 0
    age_max = 120

    for condition in conditions:
        match = re.match(r'年龄([<>=]+)(\d+)', condition)
        if not match:
            continue

        operator, value = match.groups()
        value = float(value)

        if operator == '>':
            age_min = max(age_min, value + 1)
        elif operator == '>=':
            age_min = max(age_min, value)
        elif operator == '<':
            age_max = min(age_max, value - 1)
        elif operator == '<=':
            age_max = min(age_max, value)

    # 如果有效范围存在，生成范围外的值
    if age_min <= age_max:
        # 有效范围外有两个区间：[0, age_min) 和 (age_max, 120]
        if random.random() < 0.5:
            # 选择下界区间
            return random.randint(0, int(age_min - 1))
        else:
            # 选择上界区间
            return random.randint(int(age_max + 1), 120)
    else:
        # 条件矛盾，所有值都不符合条件
        return random.randint(0, 120)


# 使用示例
if __name__ == "__main__":
    # 条件列表
    conditions = ['BMI>=24', '年龄>=18', '年龄<65']

    try:
        # 生成每种情况的样本
        cases = generate_all_cases(conditions)
        print(cases)

        # 打印结果
        for case_name, samples in cases.items():
            print(f"\n情况: {case_name}")
            for i, (bmi, age) in enumerate(samples, 1):
                print(f"样本 {i}: BMI = {bmi}, 年龄 = {age}")

    except ValueError as e:
        print(f"错误: {e}")


s = {"satisfied": {'BMI' : '24.6', '年龄' : '49'}, "not": [{'BMI' : '24.6', '年龄' : '49'}, {'BMI' : '24.6', '年龄' : '49'}]}
   # c = Connection(host='192.168.0.243', user='root', connect_kwargs={"password": "Benetech79$#-"})
   #  local_dir = '/Users/linghuchong/Downloads/51/Python/project/flask/flask_gw_i/allureReport'
   #  remote_dir = '/home/flask_gw_i/4446'

# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import json
#
#
# def save_cookies(driver, file_path):
#     """保存当前会话的 Cookies 到文件"""
#     cookies = driver.get_cookies()
#     with open(file_path, 'w') as f:
#         json.dump(cookies, f)
#
#
# def load_cookies(driver, file_path):
#     """从文件加载 Cookies 到当前会话"""
#     try:
#         with open(file_path, 'r') as f:
#             cookies = json.load(f)
#             for cookie in cookies:
#                 driver.add_cookie(cookie)
#     except FileNotFoundError:
#         print("未找到保存的 Cookies 文件。")
#
#
# def main():
#     # 初始化浏览器驱动
#     driver = webdriver.Chrome()
#     # 目标网站的登录页面 URL
#     login_url = "http://192.168.0.203:30080/#/login"
#     # 目标网站的受保护页面 URL
#     protected_url = "https://example.com/protected"
#     # 保存 Cookies 的文件路径
#     cookies_file = "cookies.json"
#
#     # 打开登录页面
#     driver.get(login_url)
#
#     # 尝试加载保存的 Cookies
#     load_cookies(driver, cookies_file)
#
#     # 重新加载页面以应用 Cookies
#     driver.get(protected_url)
#
#     # 检查是否成功登录
#     if "login" in driver.current_url:
#         print("需要手动登录。请在浏览器中完成登录操作。")
#         # 等待用户手动登录
#         input("登录完成后按回车键继续...")
#         # 保存新的 Cookies
#         save_cookies(driver, cookies_file)
#         # 重新加载受保护页面
#         driver.get(protected_url)
#
#     # 在这里可以进行更多的自动化操作，例如查找元素并点击等
#     try:
#         # 假设页面上有一个按钮，其 ID 为 "my-button"
#         button = driver.find_element(By.ID, "my-button")
#         button.click()
#         print("按钮点击成功。")
#     except Exception as e:
#         print(f"操作失败: {e}")
#
#     # 等待一段时间，以便查看操作结果
#     time.sleep(5)
#
#     # 关闭浏览器
#     driver.quit()
#
#
# if __name__ == "__main__":
#     main()

# import subprocess
#
#
# def get_current_input_method():
#     try:
#         command = 'defaults read com.apple.HIToolbox AppleSelectedInputSources | grep -i "InputSourceKind" -A 1 | grep -i "KeyboardLayout ID" | awk -F "=" \'{print $2}\' | tr -d \'; \''
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)
#         layout_id = result.stdout.strip()
#         return layout_id
#     except Exception as e:
#         print(f"获取当前输入法时出错: {e}")
#         return None
#
#
# def switch_to_english_input():
#     try:
#         script = 'tell application "System Events" to tell process "SystemUIServer" to click menu bar item 1 of menu bar 2 whose description contains "input menu"'
#         subprocess.run(['osascript', '-e', script], check=True)
#         script = 'tell application "System Events" to tell process "SystemUIServer" to click menu item "ABC" of menu 1 of menu bar item 1 of menu bar 2 whose description contains "input menu"'
#         subprocess.run(['osascript', '-e', script], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"切换输入法时出错: {e}")
#
#
# if __name__ == "__main__":
#     current_input = get_current_input_method()
#     print(current_input)
#     if current_input and 'zh' in current_input.lower():
#         switch_to_english_input()

# from openai import OpenAI
#
# text = input("请输入: \n")
# print("正在AI思考中...")
#
# # client = OpenAI(api_key="mNF21RSnIIDP7lCzObF9w9JB", base_url="https://api.openai.com")
# client = OpenAI(api_key="sk-e2bf2354c1924fbeb55c41e4d7bd151d", base_url="https://api.deepseek.com")
#
# # 使用 stream=True 启用流式响应，默认情况下，返回的响应会被解析为一个 list，
# response = client.chat.completions.create(
#     model="ds-chat",  # 确保模型名称正确
#     messages=[
#         {"role": "system", "content": "you are a helpful assistant"},
#         {"role": "user", "content": text},
#     ],
#     stream=True  # 启用流式响应
# )
#
#
# print("AI 回答:")
# # 逐行显示响应内容
# for chunk in response:
#     if chunk.choices[0].delta.content:
#         # 检查是否有内容
#         print(chunk.choices[0].delta.content, end="", flush=True)
# print() # 换行

#
# from refact import Refact
#
# # 假设你的API密钥是'your_api_key_here'
# refact = Refact(api_key='mNF21RSnIIDP7lCzObF9w9JB')
#
# # 示例：重构代码
# result = refact.refactor(code="""def add(a, b): return a + b""")
# print(result)






# numbers = [1, 2, 3, 4, 5]
# total = sum(numbers)  # 推荐
# print(total)
#
#
# squares_gen = (x**2 for x in range(10))  # 内存占用较小
# print(squares_gen)
# print(list(squares_gen))
#
#
# # functools.lru_cache 可以缓存函数的返回值，避免重复计算，提高性能。
# import functools
# @functools.lru_cache(maxsize=None)
# def fibonacci(n):
#     if n <= 1:
#         return n
#     return fibonacci(n - 1) + fibonacci(n - 2)
# # 第一次调用会计算
# print(fibonacci(10))  # 输出: 55
#
# # 第二次调用会直接返回缓存结果
# print(fibonacci(11))  # 输出: 55，但速度更快


# import binascii
# import re
# import requests
# import logging
#
# from gmssl import sm2, func
#
# class Sm2Tools:
#     """
#     通用sm2算法类
#     """
#     class KeyStore:
#         """
#         SM2 密钥对类，包含密钥对生成、获取方法
#         """
#         _PRIVATE_KEY = ""
#         _PUBLIC_KEY = ""
#
#         def __init__(self) -> None:
#             pass
#
#         def setKey(self, priKey: str, pubKey: str) -> bool:
#             """
#             简单判断密钥对格式
#             :param priKey: 私钥
#             :param pubKey: 公钥
#             :return: bool
#             """
#             result = re.match(r"^[a-fA-F\d]{64}$", priKey)
#             if result is None:
#                 logging.error("KeyStore.setKey() -> priKey is invalid.")
#                 return False
#             result = re.match(r"^[a-fA-F\d]{128}$", pubKey)
#             if result is None:
#                 logging.error("KeyStore.setKey() -> pubKey is invalid.")
#                 return False
#             self._PRIVATE_KEY = priKey
#             self._PUBLIC_KEY = pubKey
#             return True
#
#         def createLocal(self) -> bool:
#             """
#             本地创建密钥对
#             :return: bool
#             """
#
#             class _Generate_SM2_Key(sm2.CryptSM2):
#
#                 #初始化
#                 def __init__(self, private_key=None, public_key=None, ecc_table=sm2.default_ecc_table):
#                     super().__init__(private_key, public_key, ecc_table)
#
#                 #获取私钥
#                 def get_private_key(self):
#                     if self.private_key is None:
#                         self.private_key = func.random_hex(self.para_len)  # d∈[1, n-2]
#                     private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
#                     return private_key
#                     # return self.private_key
#
#                 # private_key = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
#                 # public_key = '025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
#
#                 #获取共钥
#                 def get_public_key(self):
#                     if self.public_key is None:
#                         self.public_key = self._kg(int(self.get_private_key(), 16), self.ecc_table['g'])  # P=[d]G
#                     # return self.public_key
#                     public_key = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
#                     return public_key
#             try:
#                 # _sm2Generator = _Generate_SM2_Key()
#                 # self._PRIVATE_KEY = _sm2Generator.get_private_key()
#                 self._PRIVATE_KEY = '124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62'
#                 # self._PUBLIC_KEY = _sm2Generator.get_public_key()
#                 self._PUBLIC_KEY = '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249'
#                 return True
#             except:
#                 logging.error("KeyStore.createLocal() can't create the correct keys. ",
#                               "Please call the Lib's Designer. ")
#                 return False
#
#         def getSelf(self) -> dict:
#             """
#             获取创建的密钥对
#             :return: dict: keyStore 格式：
#             {
#                 "PRIVATE_KEY": "",
#                 "PUBLIC_KEY": ""
#             }
#             """
#             return {
#                 "PRIVATE_KEY": self._PRIVATE_KEY,
#                 "PUBLIC_KEY": self._PUBLIC_KEY
#             }
#
#         def getPrivateKey(self) -> str:
#             """
#             返回公钥
#             :return: str
#             """
#             return self._PRIVATE_KEY
#
#         def getPublicKey(self) -> str:
#             """
#             返回私钥
#             :return: str
#             """
#             return self._PUBLIC_KEY
#
#     class SM2_Util(Exception):
#         """
#         SM2 加解密类
#         """
#
#         _SM2_Util = None
#
#         def __init__(self, exception="") -> None:
#             """
#             构造函数
#             :param exception: 默认参数，用于自定义异常
#             """
#
#             self._EXCPTION = None
#             self._INIT_FLAG = False
#
#         def setKey(self, keyStore: dict) -> bool:
#             """
#             初始化密钥对
#             :param keyStore: dict: keyStore 格式：
#                 {
#                     "PRIVATE_KEY": "",
#                     "PUBLIC_KEY": ""
#                 }
#             :return: bool
#             """
#             try:
#                 # 判断是否为全为英文和数字，且是 16 个字符的字符串
#                 # 不是，则抛出异常
#                 if re.match(r"^[a-fA-F\d]{64}$", keyStore["PRIVATE_KEY"]) is None:
#                     raise Sm2Tools.SM2_Util(exception="SM2_Util.setKey() -> PRIVATE_KEY is invalid.")
#                 if re.match(r"^[a-fA-F\d]{128}$", keyStore["PUBLIC_KEY"]) is None:
#                     raise Sm2Tools.SM2_Util(exception="SM2_Util.setKey() -> PUBLIC_KEY is invalid.")
#             except Sm2Tools.SM2_Util as e:
#                 logging.error(e._EXCPTION)
#                 return False
#             self._SM2_Util = sm2.CryptSM2(public_key=keyStore["PUBLIC_KEY"], private_key=keyStore["PRIVATE_KEY"])
#             self._INIT_FLAG = True
#             return True
#
#         def getSelf(self) -> sm2.CryptSM2:
#             """
#             获取加解密类对象
#             :return: sm2.CryptSM2 类实例
#             """
#             return self._SM2_Util
#
#         def encrypt(self, data: str):
#             """
#             进行 SM2 加密操作
#             :param data: String 格式的原文 data
#             :return: String 格式的密文 enc_data
#             """
#             data_utf8 = data.encode("utf-8")
#             enc_data = self._SM2_Util.encrypt(data_utf8)
#             enc_data = binascii.b2a_hex(enc_data).decode("utf-8")
#             return enc_data
#
#         def decrypt(self, enc_data: str):
#             """
#             进行 SM2 解密操作
#             :param enc_data: String 格式的密文 enc_data
#             :return: String 格式的原文 data
#             """
#             enc_data = binascii.a2b_hex(enc_data.encode("utf-8"))
#             dec_data = self._SM2_Util.decrypt(enc_data)
#             dec_data = dec_data.decode("utf-8")
#             return dec_data
#
# def test_sm2():
#     # """
#     # SM2 test
#     # """
#     keyStore = Sm2Tools.KeyStore()
#     SM2_Util = Sm2Tools.SM2_Util()
#     if keyStore.createLocal():
#         keysDict = keyStore.getSelf()
#         SM2_Util.setKey(keysDict)
#         data = "哈哈，我的国密算法改造，已完成了！！！"
#         print("data: " + data)
#         enc_data = SM2_Util.encrypt(data)
#         print("encode_data: " + enc_data)
#         dec_data = SM2_Util.decrypt(enc_data)
#         print("decode_data: " + dec_data)
#         if data == dec_data:
#             print("data == decode_data: True")
#     else:
#         print("create fail")
#
# # main
# if __name__ == '__main__':
#     print("main begin");
#     test_sm2();
#     print("main end");
#


# numbers = [1, 2, 2, 3, 2, 3, 3]
# counts = {num: numbers.count(num) for num in set(numbers)}
# print(counts)
#
# # for num in set(numbers):
# #     print(num)
#
# print(numbers.count(2))


# # import pymysql
# # pymysql.install_as_MySQLdb()
#
# args = "FullArgSpec(args=['self', 'interName', 'param'], varargs=None, varkw=None, defaults=('',), kwonlyargs=[], kwonlydefaults=None, annotations={})"
# print(args.find('self'))
# # print(args.find(', varargs'))
# # args = args[args.find('args=') + 5:args.find(', varargs')]  # ['self', 'interName', 'param']
# # # print(args)
# # print(args[args.find('args=') + 5:args.find(', varargs')])  # ['self', 'interName', 'param']
# # print(args[17:47])
# # args = (args[17:47])
# # print(args)
# # # print(args)
#










# import collections
# from math import hypot
# from random import choice
#
# Card = collections.namedtuple('Card', ['rank', 'suit'])
#
# 类与实例 PokeDeck(object):
#     ranks = [str(n) for n in range(2, 11)] + list('JQKA')
#     suits = ['spades', 'diamonds', 'clubs', 'hearts']
#
#     def __init__(self):
#         self._card = [Card(rank, suit) for rank in self.ranks
#                                        for suit in self.suits]
#
#     def __len__(self):
#         return len(self._card)
#
#     def __getitem__(self, item):
#         return self._card[item]
#
#     def __repr__(self):
#         return "This is a deck"
#
# card = PokeDeck()
# print(card)
# print(card[0])
# print(len(card))
# print(choice(card))

# import pyttsx3
# engine = pyttsx3.init()
# engine.say('Sally sells seashells by the seashore.')
# engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()

# import pyttsx3
# # Initialize the converter
# converter = pyttsx3.init()
# # Set properties before adding
# # Things to say
# # Sets speed percent
# # Can be more than 100
# converter.setProperty('rate', 150)
# # Set volume 0-1
# converter.setProperty('volume', 0.7)
# # Queue the entered text
# # There will be a pause between
# # each one like a pause in
# # a sentence
# converter.say("Hello GeeksforGeeks")
# converter.say("I'm also a geek")
# # Empties the say() queue
# # Program will not continue
# # until all speech is done talking
# converter.runAndWait()

# # 文本转语音
# import pyttsx3
# engine = pyttsx3.init()
# rate = engine.getProperty('rate')
# # engine.setProperty('rate', rate-55)
# engine.say('The quick brown fox jumped over the lazy dog. 你是金浩吗？')
# engine.runAndWait()
#
#
# """
# 本地语音文件识别测试
# """
# import speech_recognition as sr
# import sys
#
# say = '你看看'
# r = sr.Recognizer()
#
# # 本地语音测试
# harvard = sr.AudioFile(sys.path[0]+'/youseesee.wav')
# with harvard as source:
#     # 去噪
#     r.adjust_for_ambient_noise(source, duration=0.2)
#     audio = r.record(source)
#
# # 语音识别
# test = r.recognize_google(audio, language="cmn-Hans-CN", show_all=True)
# print(test)
#
# # 分析语音
# flag = False
# for t in test['alternative']:
#     print(t)
#     if say in t['transcript']:
#         flag = True
#         break
# if flag:
#     print('Bingo')

# engine = pyttsx3.init()
# engine.say("风飘荡，雨濛茸，翠条柔弱花头重")
# engine.runAndWait()



# import imghdr

# if __name__ == '__main__':
#     # 检测一个文件
#     with open('D:/test/123.jpg', 'rb') as img_file:
#         print(imghdr.what(img_file))


#
# 类与实例 Spider:
#
#     pool_manager = urllib3.PoolManager()
#
#     @staticmethod
#     def get(url):
#         return Spider.pool_manager.urlopen('GET', url)
#
#
# 类与实例 ImageDownLoader:
#     """
#     图片下载器
#     """
#
#     @staticmethod
#     def download(url, path):
#         """
#         这个方法用来下载图片并保存
#         :param url:  图片的路径
#         :param path: 要保存到的路径
#         :return:
#         """
#         response = Spider.get(url)
#         save_name = path + uuid.uuid1().hex + "." + imghdr.what(None, response.data)
#         with open(save_name, 'wb') as img_file:
#             img_file.write(response.data)
#
#
# if __name__ == '__main__':
#     ImageDownLoader.download('http://img3.doubanio.com/view/photo/albumcover/public/p2327732376.webp', 'D:/')
#     with open('D:/e5c59ac59b4311eaa1a0505bc2b637ea.webp', 'rb') as img_file:
#         print(imghdr.what(img_file))




# import os,shutil,datetime
# # from time import sleep
# # import paramiko
# # import signal
# # import subprocess
# # import time
#
#
# import operator
# 类与实例 People :
#      age = 0
#      gender = 'male'
#
#      def __init__(self, age, gender ):
#          self.age = age
#          self.gender = gender
#      def toString ( self ):
#          return 'Age:' + str( self.age ) + ' /t Gender:' + self.gender
#
# List = [ People ( 21 , 'male' ), People ( 20 , 'famale' ), People ( 34 , 'male' ), People ( 19 , 'famale' )]
# print ('Befor sort:')
# for p in List :
#     print(p.toString())
#
# # key=lambda p1,p2: operator.eq(p1.age,p2.age)
# # List.sort(key(1,1))
#
# L = [('b',6),('a',1),('c',3),('d',4)]
# print(L.sort(key=lambda x,y:operator.eq(x[1],y[1])))

# List.sort(key=lambda p1,p2 : operator.eq(p1.age,p2.age))
# # List.sort(lambda p1,p2:operator.eq(p1.age, p2.age))
# print (' /n After ascending sort:')
# for p in List :
#     print(p.toString())
#
# # List . sort ( lambda p1 , p2 : - operator.eq ( p1 . age , p2 . age ))
# # print (' /n After descending sort:')
# # for p in List :
# #     print (p . toString () )
#
# #
#

# logFile1 = "/dkvlm/tomcat_yygdoctor/logs/catalina.out"
# logFile2 = 'test2.log'
#
#
# # 日志文件一般是按天产生，则通过在程序中判断文件的产生日期与当前时间，更换监控的日志文件
# # 程序只是简单的示例一下，监控test1.log 10秒，转向监控test2.log
# def monitorLog(logFile):
#     print '监控的日志文件 是%s' % logFile
#     # 程序运行10秒，监控另一个日志
#     stoptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 10))
#     popen = subprocess.Popen('tail -f ' + logFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     pid = popen.pid
#     print('Popen.pid:' + str(pid))
#     while True:
#         line = popen.stdout.readline().strip()
#         print line
#         # 判断内容是否为空
#         if line:
#             print(line)
#             # 当前时间
#         thistime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#         if thistime >= stoptime:
#             # 终止子进程
#             popen.kill()
#             print '杀死subprocess'
#             break
#     time.sleep(2)
#     monitorLog(logFile2)
#
#
# monitorLog(logFile1)
#
# sleep(1212)
#
# remotedir = "/root"
# remotefile = "/root/log_history.txt"
# hostname = "10.111.3.6"
# port = 22
# username = "root"
# password = "gen"
#
# paramiko.util.log_to_file('paramiko.log')
# s = paramiko.SSHClient()
# s.load_system_host_keys()
#
# s.connect(hostname,port,username,password)
# command = 'tail -f /dkvlm/tomcat_yygdoctor/logs/catalina.out'
# #command = 'df -h'
# stdin,stdout,stderr = s.exec_command(command)
# #print(2,stdout.read())
# logs = stdout.readlines()
# for i in range(len(logs)):
#     print(logs[i].rstrip())
# s.close()
#
# sleep(1212)
#
#
#
# import pexpect
#
# import paramiko
# import threading
# def ssh2(ip,username,passwd,cmd):
#   try:
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(ip,22,username,passwd,timeout=5)
#     for m in cmd:
#       stdin, stdout, stderr = ssh.exec_command(m)
# #      stdin.write("Y")  #简单交互，输入 ‘Y'
#       out = stdout.readlines()
#       #屏幕输出
#       for o in out:
#         print o,
#     print '%s\tOK\n'%(ip)
#     ssh.close()
#   except :
#     print '%s\tError\n'%(ip)
#
# ssh2("10.111.3.6", "root", "gen", ['tail -f /dkvlm/tomcat_yygdoctor/logs/catalina.out','echo hello!'])
#
# sleep(1212)
#
# def ssh_cmd(ip, user, passwd, cmd):
#     ssh = pexpect.spawn('ssh %s@%s "%s"' % (user, ip, cmd))
#     try:
#         i = ssh.expect(['password: ', 'continue connecting (yes/no)?'])
#         if i == 0:
#             ssh.sendline(passwd)
#             r = ssh.read()
#         elif i == 1:
#             ssh.sendline('yes\n')
#             ssh.expect('password: ')
#             ssh.sendline(passwd)
#             r = ssh.read()
#     except pexpect.EOF:
#         ssh.close()
#     return r
#
#
# hosts = '''
# 10.111.3.6:root:gen:tail -f,//dkvlm//tomcat_yygdoctor//logs//catalina.out
# 10.111.3.6:root:gen:ls
# '''
#
# for host in hosts.split("\n"):
#     if host:
#         ip, user, passwd, cmds = host.split(":")
#         for cmd in cmds.split(","):
#             print "-- %s run:%s --" % (ip, cmd)
#             print ssh_cmd(ip, user, passwd, cmd)
#
#
# sleep(1212)
#
#
# import ftplib
# connect = ftplib.FTP("10.111.3.6")
# connect.login("root", "gen")
# data = []
# connect.dir(data.append)
# connect.quit()
# for line in data:
#    print(line)
#
# sleep(1212)
#
# x = 88888888110
#
# for i in range(1000):
#      sum = x + i
#      tmp = u"a" + str(sum) + u"z"
#      tmp1 = tmp.replace("a",'"').replace("z",'"')
#      print tmp1
# sleep(1212)
#
#

#
#
#

#


# # json与python中dict互相转换，把dict转换成json-使用json.dumps()，将json转换为dict-使用json.loads()
# eth = {}
# eth['eth0'] = "192.168.2.12"
# eth['eth1'] = "192.168.212.12"
# print eth
# import json
# ethjson = json.dumps(eth)
# print type(ethjson)
# print ethjson
# ethdict = json.loads(ethjson)
# print ethdict
# print ethdict['eth0'], ethdict['eth1']
#
# # 结果:
# # {'eth1': '192.168.212.12', 'eth0': '192.168.2.12'}
# # <type 'str'>
# # {"eth1": "192.168.212.12", "eth0": "192.168.2.12"}
# # {u'eth1': u'192.168.212.12', u'eth0': u'192.168.2.12'}
# # 192.168.2.12 192.168.212.12
#
# a=[1,2,3]
# b=[4,5,4]
# # a.append(b)
# # print a
# a.extend(b)
# print a
# del a[3]
# print a
# a.pop()
# print a
# a.remove(3)
# print a