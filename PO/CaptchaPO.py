# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2023-11-15
# Description   : captcha 验证码对象
# https://blog.csdn.net/Cameback_Tang/article/details/124247948 Python使用pytesseract进行验证码图像识别
# https://blog.csdn.net/u010698107/article/details/121736386 Python OCR工具pytesseract详解
# *********************************************************************
import ddddocr, random, string
from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
import pytesseract


'''
1，生成验证码图片 genCaptcha()
2，获取验证码 getCaptchaByDdddOcr()
'''

class CaptchaPO:

    def genCaptcha(self, filename):
        # 生成验证码图片
        # characters为验证码上的字符集，10个数字加26个大写英文字母
        # 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ str类型
        characters = string.digits + string.ascii_uppercase

        width, height, n_len, n_class = 170, 80, 4, len(characters)

        # 设置验证码图片的宽度widht和高度height
        # 除此之外还可以设置字体fonts和字体大小font_sizes
        generator = ImageCaptcha(width=width, height=height)

        # 生成随机的4个字符的字符串
        random_str = ''.join([random.choice(characters) for j in range(4)])

        # 生成验证码
        img = generator.generate_image(random_str)

        # 显示验证码图片、关闭坐标轴
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        # plt.title(random_str)
        # plt.show()
        plt.savefig(filename)

    def getCaptchaByDdddOcr(self, filename):
        # 获取验证码
        ocr = ddddocr.DdddOcr()
        f = open(filename, mode='rb')
        img = f.read()
        return ocr.classification(img)



if __name__ == "__main__":

    Captcha_PO = CaptchaPO()

    # 生成验证码
    # Captcha_PO.genCaptcha("./data/1.jpg")
    # Captcha_PO.genCaptcha("./data/base64.png")

    # 获取验证码
    # print(Captcha_PO.getCaptchaByDdddOcr("./data/1.jpg"))
    # print(Captcha_PO.getCaptchaByDdddOcr("./data/base64.png"))


    #上面都是导包，只需要下面这一行就能实现图片文字识别
    # text = pytesseract.image_to_string(Image.open('E:\example4.jpg',),lang='chi_sim')#设置为中文文字的识别
    # text = pytesseract.image_to_string(Image.open('/Users/linghuchong/Downloads/51/Python/project/PO/data/base64.png'),lang='eng') # 设置为英文或阿拉伯数字的识别
    text = pytesseract.image_to_string(Image.open('/Users/linghuchong/Downloads/51/Python/project/PO/data/base64.png',),lang='chi_sim') # 设置为英文或阿拉伯数字的识别
    print (text)