# coding:utf-8
import cv2
import numpy as np
import time
import sys
import almath
import math
from naoqi import ALProxy

# don't find 1 2 9 10 20
# with 2*2 kernel can find 3 4 5 6 7 12 13 14 15 16 17
# with 4*4 kernel can find 8 11
# with no kernel just test8.png cant find

# bright 3 4 5 12 13 14 15 16 17 21 22  use 2*2 kernel
# not bright 8 11 12 18 19   use 4*4 kernel

# 单个区域，但是有其他物体扩大了杆子的宽，选取有颜色区域最下方的40px
# 根据杆子的宽宽来过滤，

a = 1
n=0
yellow = [[16, 0, 180], [50, 85, 255]]
yellow = [[14, 0, 0], [40, 255, 250]]
Img = cv2.imread('../pic/%d.jpg' % a)


if Img is not None:  # 判断图片是否读入
    HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
    '''
HSV模型中颜色的参数分别是：色调（H），饱和度（S），明度（V）  H(0-180) S(0-255) V(0-255)
H(26-35) S(77-255) V(46-255)
下面两个值是要识别的颜色范围
'''
    # yellow = [[16, 0, 180], [50, 85, 255]]  # bright 3 4 5 12 13 14 15 16 17 21 22  use 2*2 kernel
    # yellow = [[14, 0, 0], [28, 115, 220]]  # not bright 6 7  use 4*4 kernel
    # yellow = [[14, 0, 0], [40, 115, 220]]  # not bright 8 11 12 18 19   use 4*4 kernel
    # 9 and 10 and 20 dont should find

    Lower, Upper = np.array(yellow)
    # mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
    mask = cv2.inRange(HSV, Lower, Upper)
    dilation = mask
    # target是把原图中的非目标颜色区域去掉剩下的图像
    target = cv2.bitwise_and(Img, Img, mask=dilation)
    # target=cv2.blur(target, (2,20))
    # cv2.imshow('target', target)
    # 将滤波后的图像变成二值图像放在binary中
    ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
    # 在binary中发现轮廓，轮廓按照面积从小到大排列 findContours常用来获取轮廓
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('t',hierarchy)
    # time.sleep(3)
    area = contours[0]
    for i in contours:  # 遍历所有的轮廓
        #  --------------------重点修改，根据杆子宽，高，区域面积大小，位置(下边那段)，找出杆子
        if cv2.contourArea(i) > cv2.contourArea(area):
            area = i
            # print 'area',area
else:
    print('there is no picture')
    sys.exit(0)
# def my_event(event, x, y, flags, param):
#     if event == cv2.EVENT_FLAG_LBUTTON:
#         print targetx
#         print targetx_end
#         print x
x,y,w,h=cv2.boundingRect(area)
print 'x,y,w,h',x,y,w,h
cv2.rectangle(target, (x, y), (x + w, y + h), (0, 255, 0), 1)
cv2.rectangle(Img, (x-n, y-n), (x + w+n, y + h+n), (0, 255, 0), 1)
cv2.imshow('test', Img)
cv2.imshow('target', target)
print w
cv2.waitKey(0)


