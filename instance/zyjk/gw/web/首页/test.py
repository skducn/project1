# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-12-19
# Description: 公卫 - 首页
# *****************************************************************
import pytesseract
from PIL import Image

# 替换为图片实际路径
# image_path = "高血压.png"
# image_path = "糖尿病.png"
# image_path = "高血脂.png"
# image_path = "肺结核.png"
# image_path = "精神障碍.png"
# image_path = "老年人.png"
# image_path = "孕产妇.png"
# image_path = "0～6岁儿童.png"
# image_path = "脑卒中.png"
# image_path = "冠心病.png"
image_path = "残疾人.png"
img = Image.open(image_path)

# 执行 OCR 识别
# recognized_text = pytesseract.image_to_string(img)
recognized_text = pytesseract.image_to_string(img, lang='chi_sim+eng')

# 处理识别结果，提取数字
extracted_numbers = recognized_text.strip().split()
print("识别结果：", extracted_numbers)
