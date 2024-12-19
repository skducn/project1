# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2024-12-19
# Description   : tesseract
# https://blog.csdn.net/Cameback_Tang/article/details/124247948 Python使用pytesseract进行验证码图像识别
# https://blog.csdn.net/u010698107/article/details/121736386 Python OCR工具pytesseract详解
# https://www.cnblogs.com/BlueSkyyj/p/9481178.html

# todo 问题：pytesseract.pytesseract.TesseractNotFoundError: tesseract is not installed or it's not in your path
# 解决方法：配置pytesseract模块路径
# 1，pytesseract安装包路径：/Users/linghuchong/miniconda3/envs/py308/lib/python3.8/site-packages/pytesseract
# 2, 配置 pytesseract.py ，将 tesseract_cmd = 'tesseract' 改为： tesseract_cmd = '/usr/local/Cellar/tesseract/5.4.1/bin/tesseract'

# todo 问题：pytesseract.pytesseract.TesseractError: (1, 'Error opening data file /usr/local/share/tessdata/chi_sim.traineddata Please make sure the TESSDATA_PREFIX environment variable is set to your "tessdata" directory. Failed loading language \'chi_sim\' Tesseract couldn\'t load any languages! Could not initialize tesseract.')
# 下载中文语言包
# 1，官网下载：https://github.com/tesseract-ocr/tessdata
# chi_sim.traineddata(42.3M) https://github.com/tesseract-ocr/tessdata/blob/main/chi_sim.traineddata
# 百度网盘获取：https://pan.baidu.com/s/1uuSTBNo3byJib4f8eRSIFw，提取码：8v8u
# 2,将文件复制到 /usr/local/share/tessdata
# 3，配置tessdata环境变量
# sudo vi ~/.bash_profile
# export TESSDATA_PREFIX=/usr/local/share/tessdata  或 export TESSDATA_PREFIX=/usr/local/Cellar/tesseract/5.4.1/share/tessdata
# 4，重启电脑才会生效。
# *********************************************************************

from PIL import Image
import pytesseract



'''
1，生成验证码图片 genCaptcha()
2，获取验证码 getCaptchaByDdddOcr()
'''

class TesseractPO:

    def image2string(self, varImg, varLang):

        # lang = 'chi_sim')  # 设置为中文文字的识别
        # lang = 'eng')  # 设置为英文或阿拉伯数字的识别
        # text = pytesseract.image_to_string(Image.open('E:\example4.jpg'),lang='chi_sim')#设置为中文文字的识别
        text = pytesseract.image_to_string(Image.open(varImg), lang=varLang)
        return text



if __name__ == "__main__":

    Tesseract_PO = TesseractPO()
    #
    print(Tesseract_PO.image2string("/Users/linghuchong/Downloads/51/Python/project/PO/data/base64.png",'eng'))
    print(Tesseract_PO.image2string("/Users/linghuchong/Downloads/51/Python/project/PO/data/base64.png", 'chi_sim'))

