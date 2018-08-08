# coding=utf-8
import random
import cv2
from naoqi import ALProxy
import almath
import numpy as np
import math
import time

IP = "172.16.55.80"
Port = 9559
g_motion = g_videoDevice = g_posture = None


def init():
    global g_motion, g_videoDevice, g_posture
    try:
        g_motion = ALProxy("ALMotion", IP, Port)  # 移动模块
        g_videoDevice = ALProxy("ALVideoDevice", IP, Port)
        g_motion.setStiffnesses("Head", 1.0)
        g_posture = ALProxy("ALRobotPosture", IP, Port)  # 姿势模块
        g_posture.goToPosture("StandInit", 0.5)
    except Exception, e:
        print e


def get_pic():
    # subscribe top camera
    AL_kTopCamera = 0
    AL_kQVGA = 1  # 320*240
    AL_kBGRColorSpace = 13
    # create image
    width = 320
    height = 240
    name = str(random.random())
    g_motion.angleInterpolationWithSpeed("HeadPitch", 5 * almath.TO_RAD, 0.3)
    # g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.3)
    captureDevice = g_videoDevice.subscribeCamera(
        name, AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)
    # np.zeros返回一个给定形状和类型的用0填充的数组；
    image = np.zeros((height, width, 3), np.uint8)  # ,unit8（无符号的整数，unit8是0～255）
    # get image
    result = g_videoDevice.getImageRemote(captureDevice)

    if result == None:
        print 'cannot capture.'

    elif result[6] == None:
        print 'no image data string.'
        print result[6]

    else:
        # translate value to mat
        # imgHeader our image binary to the openCV image
        # map第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。
        # ord函数返回字符串对应的 ASCII 数值
        values = map(ord, list(result[6]))
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image.itemset((y, x, 0), values[i + 0])
                image.itemset((y, x, 1), values[i + 1])
                image.itemset((y, x, 2), values[i + 2])
                i += 3
        cv2.imshow('image', image)
    # cv2.imwrite('../%d.jpg' %a,image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image


def my_event(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        try:
            print x, y
        except Exception, e:
            print(e)


def find_mark(img):
    n1 = n2 = 1
    y = [-20, -40]
    x = [0, 0]
    lines = []
    lines_num = 0
    lines_error = 0
    length_of_line = 40
    maxLineGap = 40
    # img0=img
    cv2.imshow('img0', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    cv2.imshow('edges', edges)
    while lines_num != 2 or 5 <= abs(y[0] - y[1]):
        lines_end = []
        print('lines num,y', lines_num, y)
        nums = lines_num = 0
        print('there')
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, length_of_line, maxLineGap=maxLineGap)

        if lines is None:
            print('None length of line', length_of_line)
            print('lines is none')
            if length_of_line >= 120:
                print('length of line error')
                cv2.waitKey(0)
                exit(-1)
            continue
        print('len lines', len(lines))
        # if len(lines)>=2:
        #     cv2.waitKey(0)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            theta = abs((y2 - y1) / (x2 - x1))
            if theta > 2 or x2 == x1:
                if nums == 2:  # 防止越界
                    continue
                if y2 > y1:
                    x[nums] = x2
                    y[nums] = y2
                    print('nums,y2,y', nums,y2,y)
                else:
                    x[nums] = x1
                    y[nums] = y1
                nums += 1
                print('x1,y1,x2,y2', x1, y1, x2, y2)
                cv2.imshow('img', img)
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                lines_end.append(line[0])
                lines_num += 1
                cv2.imshow('img', img)
                # cv2.waitKey(0)
        print('y[0],y[1]', y[0], y[1])
        # if length_of_line == 41 and maxLineGap == 40:
        #     print('right', lines_num, abs(y[0] - y[1]))
        #     cv2.waitKey(0)
        if lines_error == 0:
            length_of_line += 1
        else:
            if maxLineGap == 70:
                length_of_line += 1
                maxLineGap = 20
            else:
                maxLineGap += 5
        if length_of_line >= 120:
            if lines_error == 0:
                print('length_of_line error, continue')
                lines_error = 1
                length_of_line = 40
                maxLineGap = 20
            else:
                print('length of line error ,maxLineGap error too')
                exit(-1)
        else:
            print('length of line', length_of_line)
    print('len lines', len(lines))
    print('n1,n2', n1, n2)
    print('x', x)
    width = abs(x[1] - x[0])
    distx = -((x[1] + x[0]) / 2 - 320 / 2)
    # alpha = math.pi * (distx * 60.92 / 320) / 180
    alpha = distx * 60.92 / 320
    print('width', width)
    cv2.imshow('img', img)
    cv2.setMouseCallback('img0', my_event)
    cv2.setMouseCallback('img', my_event)
    cv2.setMouseCallback('edges', my_event)
    # cv2.waitKey(0)
    return width, alpha


def get_distance(w, focalLength=264.0):
    KNOWN_WIDTH = 5  # 黄杆的宽
    # focalLength = 264.0
    distance = (KNOWN_WIDTH * focalLength) / w
    return distance


# def get_angle(lines,):


a0 = 9
# init();image = get_pic()
image = cv2.imread('../pic/%d.jpg' % a0)
width, alpha = find_mark(image)
print('alpha', alpha)
distance = get_distance(width, 264.0)
print('distance', distance)
cv2.waitKey(0)
