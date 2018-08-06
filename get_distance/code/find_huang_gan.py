#!usr/bin/python
# -*- coding: utf-8 -*-
# 定义编码，中文注释

# import the necessary packages
import numpy as np
import cv2
import sys


# 找到目标函数,---------------------修改这里
def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    # cv2.imshow('image', image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray', gray)  # 灰度图
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # 高斯滤波
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # 高斯滤波
    # cv2.imshow('gauss', gray)  # 模糊后的灰度图
    edged = cv2.Canny(gray, 35, 125)  # 边缘检测
    cv2.imshow('edged', edged)  # 边缘检测图

    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image

    # (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # def findContours(image, mode, method, contours=None, hierarchy=None, offset=None):
    # real signature unknown; restored from __doc__
    # """ findContours(image, mode, method[, contours[, hierarchy[, offset]]]) -> contours, hierarchy """

    # 取值一：CV_RETR_EXTERNAL 只检测最外围轮廓，包含在外围轮廓内的内围轮廓被忽略
    # 取值二：CV_RETR_LIST     检测所有的轮廓，包括内围、外围轮廓，但是检测到的轮廓不建立等级关

    # 取值一：CV_CHAIN_APPROX_NONE 保存物体边界上所有连续的轮廓点到contours向量内
    # 取值二：CV_CHAIN_APPROX_SIMPLE 仅保存轮廓的拐点信息，把所有轮廓拐点处的点保存入contours
    # 向量内，拐点与拐点之间直线段上的信息点不予保留
    # 取值三和四：CV_CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近
    # 似算法

    # 求最大面积
    c = max(cnts, key=cv2.contourArea)  # 返回由cv2.contourArea 计算的最大面积的轮廓

    # compute the bounding box of the of the paper region and return it
    # cv2.minAreaRect() c代表点集，返回rect[0]是最小外接矩形中心点坐标，
    # rect[1][0]是width，rect[1][1]是height，rect[2]是角度
    # return c  # 返回包含所有坐标点的不知道啥 [[[x y]];[[x y]]...]
    return cv2.minAreaRect(c)


# 距离计算函数
def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth


# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0  # 测量的距离

# initialize the known object width, which in this case, the piece of
# paper is 11 inches wide
# A4纸的长和宽(单位:inches)
KNOWN_WIDTH = 11.69  # 黄杆的宽
# KNOWN_HEIGHT = 8.27  # 黄杆的高

# initialize the list of images that we'll be using
IMAGE_PATHS = ["../picture/1.png", "../picture/2.png", "../picture/3.png"]

# load the furst image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
# 读入第一张图，通过已知距离计算相机焦距
# image = cv2.imread(IMAGE_PATHS[0])
image = cv2.imread('/home/sl/my/pycharm_workspaces/code/naoproj/nao_test/get_distance/picture/1.png')
# cv2.imshow('test', image)
# cv2.waitKey(500)
# cv2.destroyAllWindows()
marker = find_marker(image)
print "marker", marker
box = np.int0(cv2.cv.BoxPoints(marker))
print "box",box
cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
cv2.imshow('image', image)
cv2.waitKey(3000)
cv2.destroyAllWindows()
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

# 通过摄像头标定获取的像素焦距
# focalLength = 811.82
print('focalLength = ', focalLength)

# 打开摄像头
camera = cv2.VideoCapture(0)

while camera.isOpened():
    # get a frame
    (grabbed, frame) = camera.read()
    marker = find_marker(frame)
    if marker == 0:
        print(marker)
        continue
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

    # draw a bounding box around the image and display it
    box = np.int0(cv2.cv.BoxPoints(marker))
    cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

    # inches 转换为 cm
    cv2.putText(frame, "%.2fcm" % (inches * 30.48 / 12),
                (frame.shape[1] - 200, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)

    # show a frame
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
