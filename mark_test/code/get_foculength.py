# coding=utf-8
import cv2
import numpy as np
import sys

# 0.jpg 120  # 原始
# 1.jpg 100
# 2.jpg 110
# 3.jpg 70
# 4.jpg 40
# 5.jpg 30


# 1英尺(ft)=30.48厘米(cm)
# focalLength = 264.0
yellow = [[16, 0, 180], [50, 85, 255]]
# yellow = [[14, 0, 0], [40, 115, 220]]  # not bright

white = [[0, 0, 221], [180, 30, 255]]  # new white's lower and upper
# yellow = white

a=2
n = 0
KNOWN_DISTANCE=110
KNOWN_WIDTH=5

def find_marker(Img):
    if Img is not None:  # 判断图片是否读入
        # cv2.imshow('test', Img)
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
        cv2.imshow('target', target)
        # 将滤波后的图像变成二值图像放在binary中
        ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
        # 在binary中发现轮廓，轮廓按照面积从小到大排列 findContours常用来获取轮廓
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow('t',hierarchy)
        # time.sleep(3)
        area = contours[0]
        for i in contours:  # 遍历所有的轮廓
            print('area', cv2.contourArea(i))  # print the size of area
            #  --------------------重点修改，根据杆子宽，高，区域面积大小，位置(下边那段)，找出杆子
            if cv2.contourArea(i) > cv2.contourArea(area):
                area = i
    else:
        print('there is no picture')
        sys.exit(0)
    print 'area_final',cv2.contourArea(area)
    return area

image=cv2.imread('../mypic/%d.jpg' %a)
area=find_marker(image)
x,y,w,h=cv2.boundingRect(area)
# w += 1
cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
focalLength = (w * KNOWN_DISTANCE) / KNOWN_WIDTH
print 'focalLength',focalLength
cv2.imshow('image',image)
cv2.waitKey(0)

