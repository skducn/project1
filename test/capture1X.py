# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2019-10-16
# Description: 截屏操作 ???
#***************************************************************

# 截屏指定图片中某一区域，并另存为。
import cv2
img = cv2.imread('123.png')
# h、w为想要截取的图片大小
h = 40
w = 130
cropImg = img[(452):(452 + h), (1480):(1480 + w)]
cv2.imwrite('333.png', cropImg)



