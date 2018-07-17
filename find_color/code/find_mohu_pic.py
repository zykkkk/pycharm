# coding:utf-8

import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

# set blue thresh
# lower_blue=np.array([78,43,46])
# upper_blue=np.array([110,255,255])
blue = [[75, 50, 46], [124, 255, 255]]
yellow = [[26, 77, 46], [35, 255, 255]]
yellow = blue
lower_blue, upper_blue = np.array(yellow)
kernel_4 = np.ones((4, 4), np.uint8)


def mohu(res, x,y):
    res = cv2.blur(res, (x,y))  # 均值滤波
    res2 = cv2.medianBlur(res, 3)  # 中值滤波
    res3 = cv2.GaussianBlur(res, (x,y), 0)  # 高斯滤波  x and y 都必须为正数和奇数
    res4=cv2.bilateralFilter(res,15,150,3)  # 双边滤波
    # res = res2
    res = cv2.erode(res, kernel_4/2, iterations=1)  # erode 侵蝕 being small
    res = cv2.erode(res, kernel_4/2, iterations=1)  # erode 侵蝕 being small
    res = cv2.dilate(res, kernel_4/2, iterations=1)
    res = cv2.dilate(res, kernel_4/2, iterations=1)
    return res, res2, res3,res4


while (1):
    # get a frame and show
    ret, frame = cap.read()
    cv2.imshow('Capture', frame)

    # change to hsv model
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # cv2.imshow('test',hsv)

    # get mask
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow('Mask', mask)

    # detect blue
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('Result', res)
    # mohu
    res = cv2.blur(res, (1, 1))  # blur(src,(x,y)) , x and y is fangxiang
    a=0
    for i in mohu(res,3,3):
        a+=1
        cv2.imshow('res%d' %a,i)

    # time.sleep(20)  # cant use with time.sleep
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
