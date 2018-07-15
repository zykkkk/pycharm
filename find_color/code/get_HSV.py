# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np

a=3
# in PIL Image.getpixel((x, y))
# mouse callback function
# 获取HSV值
def my_event(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        print('RGB2:', img[x, y], '   ', 'GSV:', HSV[x, y])


# 创建图像与窗口并将窗口与回调函数绑定
# img=cv2.imread('../test_picture/color.jpg')
img = cv2.imread('../../nao_pic/test%d.png' %a)
x, y, i = img.shape
print(img.shape)

x1 = x / 100
y1 = y / 100
x2 = round(x1) * 100
y2 = round(y1) * 100
img = cv2.resize(img, (y2, x2))
print(img.shape)  # 图片大小
time.sleep(3)
# time.sleep(4)
HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
cv2.namedWindow('image')  # 此处已经有界面 #
cv2.resizeWindow('image', x, y)
cv2.imshow('image', img)
cv2.imshow('test', HSV)
cv2.resizeWindow('test', x, y)
cv2.setMouseCallback('image', my_event)
while (1):
    # press 'esc' to exit
    if cv2.waitKey(20) & 0xFF == 27:
        break
        # else:
        #     print(cv2.waitKey(20)&0xFF)
cv2.destroyAllWindows()
