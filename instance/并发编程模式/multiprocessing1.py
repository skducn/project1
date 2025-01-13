# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-12-30
# Description: 使用 multiprocessing 模块并行处理
# multiprocessing 模块允许你并行执行多个进程，充分利用多核 CPU 的计算能力。
# http://www.51testing.com/html/80/15326880-7803860.html
# https://blog.csdn.net/u013421629/article/details/100284962
# 实例 - CHC - web - changning - main.py 新泾镇社区卫生服务中心 - 执行自动上报 - 多进程
# *****************************************************************

from multiprocessing import Pool
import cv2, time
import numpy as np

def convert_to_grayscale(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def square(x, y):
    return x * y

def p_square(param):
    return square(param[0], param[1])


if __name__ == "__main__":

    # image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
    # with Pool(4) as pool:  # 假设有 4 个 CPU 核心
    #     gray_images = pool.map(convert_to_grayscale, image_paths)
    # # 可以进一步处理 gray_images，例如保存到磁盘或进行其他分析
    # for i, gray_image in enumerate(gray_images):
    #     cv2.imwrite(f"gray_{image_paths[i]}", gray_image)


    time1 = time.time()
    # 假设有 4 个 CPU 核心
    with Pool(4) as pool:
        squared_numbers = pool.map(p_square, [(2,3), (4,5), (6,7), (8,9)])
    print(squared_numbers)
    time2 = time.time()
    pool.close()
    pool.join()
    print('总共耗时：' + str(time2 - time1) + 's')

