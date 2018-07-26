# coding:utf-8
import cv2
import numpy as np
import time
import sys

# don't find 1 2 9 10 20
# with 2*2 kernel can find 3 4 5 6 7 12 13 14 15 16 17
# with 4*4 kernel can find 8 11
# with no kernel just test8.png cant find

# bright 3 4 5 12 13 14 15 16 17 21 22  use 2*2 kernel
# not bright 8 11 12 18 19   use 4*4 kernel

# 单个区域，但是有其他物体扩大了杆子的宽，选取有颜色区域最下方的40px
# 根据杆子的宽宽来过滤，

a = 5
area = 0
mark_width = 20
yellow = [[16, 0, 180], [50, 85, 255]]

def find_yellow(Img):
    if Img is not None:  # 判断图片是否读入
        cv2.imshow('test', Img)
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
            print(cv2.contourArea(i))  # print the size of area
            #  --------------------重点修改，根据杆子宽，高，区域面积大小，位置(下边那段)，找出杆子
            if cv2.contourArea(i) > cv2.contourArea(area):
                area = i
    else:
        print('there is no picture')
        sys.exit(0)
    while True:
        Key = chr(cv2.waitKey(15) & 255)
        if Key == 'q':
            cv2.destroyAllWindows()
            return area


if __name__ == '__main__':
    # print(sys.argv)
    Img = cv2.imread('../../../nao_pic/test%d.png' % a)
    area = find_yellow(Img)
    x, y, w, h = cv2.boundingRect(area)
    print cv2.contourArea(area)
    if cv2.contourArea(area)<150:
        print "sorry,don't find landmark"
        yellow = [[14, 0, 0], [40, 115, 220]]
        area=find_yellow(Img)
    print "x,y,w,h :", x, y, w, h
    print x + w / 2, y + h
    if w > 10:  # 超过了杆子的大小，不准
        Img2 = Img[y + h - 40:y + h, :]  # 选取底部４０px的部分来检测
        print Img2.shape
        area2 = find_yellow(Img2)
        x2, y2, w2, h2 = cv2.boundingRect(area2)
        print cv2.contourArea(area2)
        print "x,y,w,h :", x2, y2, w2, h2
        if w2 < mark_width:
            x = x2 + w2 / 2
            print "final", x, y + h
        else:
            print "w,mark_width", w, mark_width
    center_x = x
    center_y = y + h
