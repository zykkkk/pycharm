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

a = 5
mark_width = 0.09
yellow = [[16, 0, 180], [50, 85, 255]]
IP = '192.168.1.198'
Port = 9559
g_motion = ALProxy("ALMotion", IP, Port)  # 移动模块
# landmark = {"size": 0.09}
Img = cv2.imread('../../../nao_pic/test%d.png' % a)


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


# Retrieve landmark center position in radians.
# wzCamera = markData[1][0][0][1]
# wyCamera = markData[1][0][0][2]
# # Retrieve landmark angular size in radians.
# angularSize = markData[1][0][0][3]
# landmarkWidthInPic = markData[1][0][0][3]

def get_dot(area):
    x, y, w, h = area
    center_x = x + w / 2
    center_y = y + h / 2

    landmark_width_in_pic = w
    currentCamera = "CameraTop"
    # headAngle=headg_motion.getAngles("HeadYaw", True)
    head_yaw_Angle = 10
    # markWithHeadAngle = alpha + headAngle[0]  # landmark相对机器人头的角度
    markWithHeadAngle = center_x + head_yaw_Angle
    # 头部正对landmark
    g_motion.angleInterpolationWithSpeed("HeadYaw", markWithHeadAngle, 0.2)
    # ----------------------------------计算距离-----------------------------------------------#
    # distanceFromCameraToLandmark = landmark["size"] / (2 * math.tan(landmarkWidthInPic / 2))
    distanceFromCameraToLandmark = mark_width / (2 * math.tan(landmark_width_in_pic / 2))
    # 获取当前机器人到摄像头的距离的变换矩阵
    transform = g_motion.getTransform(currentCamera, 2, True)
    transformList = almath.vectorFloat(transform)
    robotToCamera = almath.Transform(transformList)
    # 打印
    # print("transform:", transform)
    # print("transformList :", transformList)
    # print("robotToCamera :", robotToCamera)

    # 计算指向landmark的旋转矩阵
    # cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, beta, alpha)
    cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, center_x, center_y)

    # 摄像头到landmark的矩阵
    cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

    # 机器人到landmark的矩阵
    robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform
    # 打印
    # print("cameraToLandmarkRotationTransform: " ,cameraToLandmarkRotationTransform)
    # print("cameraToLandmarkTranslationTransform: ",cameraToLandmarkTranslationTransform)
    # print("robotToLandmark",robotToLandmark )
    x = robotToLandmark.r1_c4
    y = robotToLandmark.r2_c4
    z = robotToLandmark.r3_c4

    distance = math.sqrt(x ** 2 + y * y) * 100

    markWithHeadAngle = round(markWithHeadAngle, 2)
    # 将数据存入列表
    return distance, markWithHeadAngle


if __name__ == '__main__':
    # print(sys.argv)
    # Img = cv2.imread('../../../nao_pic/test%d.png' % a)
    area = find_yellow(Img)  # 第一次检测，检测最大的黄色区域
    x, y, w, h = cv2.boundingRect(area)
    print cv2.contourArea(area)
    if cv2.contourArea(area) < 150:  # 判断黄色区域是否足够被认为是黄杆
        print "sorry,don't find landmark,find again"
        yellow = [[14, 0, 0], [40, 115, 220]]  # 更改黄色HSV的范围，此处是暗部的颜色取值
        area = find_yellow(Img)
        if cv2.contourArea(area) < 150:  # 暗亮都检测了，都不合适，求其次？勉强上？再测试数据是否满足其余的条件
            print "sorry,真的没找到"
            sys.exit(-1)
    print "x,y,w,h :", x, y, w, h
    print x + w / 2, y + h
    if w > 10 | h < 20:  # 超过了杆子的最大大小，或者杆子高度不够最小高度，不准
        Img2 = Img[y + h - 40:y + h, :]  # 选取底部４０px的部分来检测，去除其他的物体干扰
        print Img2.shape
        area2 = find_yellow(Img2)
        x2, y2, w2, h2 = cv2.boundingRect(area2)
        print cv2.contourArea(area2)
        print "x,y,w,h :", x2, y2, w2, h2
        if 0.2 < w2 < mark_width:
            # 更改x坐标值，其余不变？再增加一次检测，选取上边４０px来检测，是否y坐标不变(防止其他物体干扰结果造成的y值不准)
            x = x2 + w2 / 2
            print "final_button", x, y + h
        else:
            print "w,mark_width", w, mark_width  # 增加对比，比较两次的结果是否是差不多
    center_x = x
    center_y = y + h

    Img3 = Img[center_y:(y + h), :]
    area3 = find_yellow(Img3)
    x1, y1, w1, h1 = area3
    if abs(w - w1) <= 0.2:  # 选取中间部分来检测，是否黄杆的宽度几乎不变
        distance, markWithHeadAngle = get_dot(area3)
