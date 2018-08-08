# coding=utf-8
import random
import cv2
from naoqi import ALProxy
import almath
import numpy as np
import math
import time

a = 5
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
            print ptt
            print targetx_end
        except Exception, e:
            print(e)


def paixu(target):
    for i in range(len(target)):
        for j in range(len(target)):
            if max(target[i][1][0], target[i][0][0]) < (max(target[j][1][0], target[j][0][0])):
                new = target[i]
                target[i] = target[j]
                target[j] = new
    return target


def calc(targetx):
    # targetx.sort()  # 排序
    print 'targetx', targetx
    print 'len', targetx[0][0][0]
    paixu(targetx)
    print '排序 targetx', targetx
    # b = []
    targetx_end_ready = []
    t = targetx[0]
    print t
    for i in targetx:
        # print 'i',i
        if 0 <= abs(max(i[1][0], i[0][0]) - max(t[1][0], t[0][0])) <= 3:
            t = i
        else:
            targetx_end_ready.append(t)
            t = i
    targetx_end_ready.append(t)
    t = targetx_end_ready[0]
    for i in targetx_end_ready:
        # print 'i',i
        if abs(max(i[1][0], i[0][0]) - max(t[1][0], t[0][0])) <= 30:
            t = i
            targetx_end.append(t)
        else:
            t = i
    # targetx_end.append(t)
    print('target_end_ready', targetx_end_ready)
    print('target_end', targetx_end)
    # exit()


def find_yellow(Img, yellow):
    global times, a, area0, big_area, b, w, x, y, h, jia, w1
    cv2.imshow('Img', Img)
    # cv2.waitKey(0)
    print yellow
    # time.sleep(3)
    print 'times', times
    if Img is None:  # 判断图片是否读入
        print 'there is no picture'
        exit(0)
    HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
    # yellow = [[16, 0, 180], [50, 85, 255]]  # bright 3 4 5 12 13 14 15 16 17 21 22  use 2*2 kernel
    # yellow = [[14, 0, 0], [28, 115, 220]]  # not bright 6 7  use 4*4 kernel
    # yellow = [[14, 0, 0], [40, 115, 220]]  # not bright 8 11 12 18 19   use 4*4 kernel

    Lower, Upper = np.array(yellow)
    # mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
    mask = cv2.inRange(HSV, Lower, Upper)
    # mask = cv2.blur(mask, (3, 3))
    dilation = mask
    # target是把原图中的非目标颜色区域去掉剩下的图像
    target = cv2.bitwise_and(Img, Img, mask=dilation)
    # cv2.imshow('target', target)
    # 将滤波后的图像变成二值图像放在binary中
    ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
    # 在binary中发现轮廓，轮廓按照面积从小到大排列 findContours常用来获取轮廓
    image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('t',hierarchy)
    # time.sleep(3)
    area = contours[0]
    for i in contours:  # 遍历所有的轮廓
        #  --------------------重点修改，根据杆子宽，高，区域面积大小，位置(下边那段)，找出杆子
        if cv2.contourArea(area) < cv2.contourArea(i) < big_area:
            area = i

    x, y, w, h = cv2.boundingRect(area)
    # print 'x,y,w,h',x,y,w,h
    cv2.rectangle(target, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.imshow('target', target)
    print 'waitKey there'
    cv2.waitKey(0)
    for i in range(len(targetx_end)):
        if abs(x - targetx_end[i][0][0]) <= 10:
            a = a or 1
        else:
            a = a or 0
    if w <= 5 or w >= 50 or h < 20 or h > 170 or a == 0:
        print 'w,h', w, h
        if times == 1:
            times += 1
            print '调用　１　'
            area, x, y, w, h = find_yellow(Img, yellow2)  # 更换颜色区域继续寻找
        elif times == 2:
            times += 1
            print '调用　２　'
            area, x, y, w, h = find_yellow(Img, white)
        elif times == 3:
            times += 1
            print '调用 ６'
            area, x, y, w, h = find_yellow(Img, yellow3)
        else:
            print 'not find yellow find again'
            big_area = cv2.contourArea(area)
            if big_area <= 5:
                print 'big area error'
                exit(0)
            a = 0
            times = 1
            print '调用　３　'
            area, x, y, w, h = find_yellow(Img, yellow1)
    # if yellow == yellow1 or yellow == yellow3:
    #     x0,y0, w0,h0= x,y, w,h
    #     if yellow == yellow1:
    #         area, x, y, w, h = find_yellow(Img, yellow3)
    #     else:
    #         area, x, y, w, h = find_yellow(Img, yellow1)
    #     if abs(x - (x0 + w0)) <= 1 or abs((x0 + w0) - (x + w)) <= 1:  # 先检测到的再左边 or 先检测到的再右边
    #         x = min(x, x0)
    #         y=min(y,y0)
    #         w = w0 + w
    if w > 20 and abs(w - w1) > 5:
        print 'w', w
        w1 = w
        if b == 0:
            yellow_pic_data.append((x, y, w, h))
            print 'yellow_pic_data', yellow_pic_data
            print 'test 黄杆'
            Img1 = Img[y + h / 7:y + 5 * h / 7, x - 10:x + w + 10]
            # cv2.rectangle(target, (x, y), (x + w, y + h), (0, 255, 0), 1)
            # Img1=Img[x:x+w,y+h/7:y+5*h/7]
            cv2.imshow('test Img1', Img1)
            # cv2.waitKey(0)
            print '调用　４　'
            area1, x1, y1, w1, h1 = find_yellow(Img1, yellow)
            print 'w1', w1
            # x1, y1, w1, h1 = cv2.boundingRect(area1)
            if abs(w1 - w) <= 3:
                b = 1
                print 'finded'
            else:
                print '调用　５　'
                area, x, y, w, h = find_yellow(Img1, yellow1)
    # x, y, w, h = cv2.boundingRect(area)
    print 'x,y,w,h---1', x, y, w, h
    print 'yellow_pic_data end', yellow_pic_data
    if jia == 0:
        for i in range(len(yellow_pic_data)):
            # if len(yellow_pic_data) == 1:
            x = x + yellow_pic_data[i][0] - 10
            y = y + yellow_pic_data[i][1]
            jia = 1
    print 'x,y,w,h---2', x, y, w, h
    print 'there yellow pic data ', yellow_pic_data
    cv2.rectangle(target, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.rectangle(Img, (x - n, y - n), (x + w + n, y + h + n), (0, 255, 0), 1)
    print 'Img there'
    # cv2.imshow('Img_there',Img)
    # cv2.waitKey(0)
    cv2.imshow('test', Img)
    cv2.imshow('target', target)
    print w
    print 'find yellow ready return'
    return area, x, y, w, h


def cal_num(targetx_end):
    global dis
    print 'dis', dis
    print 'length targetx_end', len(targetx_end)
    alpha = None
    w = None
    if len(targetx_end) < 2:
        print 'cal_num targetx_end error <2'
        cv2.waitKey(0)
        exit(1)
    if len(targetx_end) == 2:
        print 'targetx_end', targetx_end
        w = targetx_end[1][1][0] - targetx_end[0][1][0]
        print 'w= ', w
        x = ((targetx_end[0][1][0] + targetx_end[0][0][0]) + (targetx_end[1][1][0] + targetx_end[1][0][0])) / 4
        print 'x,y', x, 240 / 2
        distx = -(x - 320 / 2)
        alpha = math.pi * (distx * 60.92 / 320) / 180
        print 'alpha', alpha
        print 'cal_num return'
        print w, alpha
        return w, alpha
    else:
        area, x, y, w, h = find_yellow(img0, yellow1)
        # x, y, w, h = cv2.boundingRect(area)  # 最后的area 起作用了,修改的x,y,w,h 无效额
        print 'x,y,w,h', x, y, w, h
        final_x = []
        for i in targetx_end:
            if abs(i[0][0] - x) <= 30 or abs(i[0][0] - x - w) <= dis:
                final_x.append(i)
            else:
                print 'no thing'  # 如果黄色区域错误,造成距离检测不准,不计入最终数据
        if dis >= 60:
            print 'yellow dis error ,not find '
            exit(0)
        dis += 2
        w, alpha = cal_num(final_x)
        print w, alpha
        return w, alpha


if __name__ == '__main__':
    yellow1 = [[16, 0, 180], [50, 85, 255]]  # bright
    yellow2 = [[14, 0, 0], [40, 115, 220]]  # inside bright and not bright
    yellow3 = [[26, 77, 46], [35, 255, 255]]  # not bright
    white = [[0, 0, 221], [180, 30, 255]]  # new white's lower and upper
    # yellow = white
    times = 1
    n = 0
    image_num = 2
    img0 = cv2.imread("../pic/%d.jpg" % image_num)  # 使用本地图片
    # init();img0=get_pic()  # 使用机器人
    cv2.imshow('img0', img0)
    # cv2.imwrite('../pic/8.jpg',img0)
    # find_yellow(img0)
    # exit(0)
    b = 70  # 可以看到全部的黄杆
    # b = 40  # 看到部分的黄杆
    # img0 = cv2.imread("../pic/%d.jpg" % a)
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)  # 貌似可加可不加
    # img = cv2.GaussianBlur(img, (3, 3), 0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, math.pi / 180, b)  # 这里对最后一个参数(最小的像素点数)使用了经验型的值
    print('length lines', len(lines))
    result = img.copy()
    cv2.imshow('Canny', edges)
    cv2.setMouseCallback('Canny', my_event)
    ptt = []
    print result.shape  # 返回宽,长,3
    for line in lines:
        line = line[0]
        rho = line[0]  # 第一个元素是距离rho
        theta = line[1]  # 第二个元素是角度theta 极角,弧度
        jiao = abs(theta / math.pi * 180)
        # if (theta < (math.pi / 4.)) or (theta > (3. * math.pi / 4.0)):  # 垂直直线 　
        if (theta < 0.80) or (theta > 2.50):  # 垂直直线　　在45度到135度之间的直线
            # if (theta < 0.01) or (theta > 3.11):  # 垂直直线  theta 的线条与目标直线垂直,此处的0.01和3.11请查看test1.py
            print 'jiao', round(jiao, 5), theta, math.pi / 4, 3 * math.pi / 4.0
            # if jiao <=2:  # 垂直直线
            # 该直线与第一行的交点
            pt1 = (int(rho / math.cos(theta)), 0)
            print pt1
            # time.sleep(2)
            # cv2.waitKey(2000)
            # 该直线与最后一行的焦点
            pt2 = (int((rho - result.shape[0] * math.sin(theta)) / math.cos(theta)), result.shape[0])
            print pt2
            # 绘制一条白线
            cv2.line(result, pt1, pt2, (255))
            ptt.append((pt1, pt2))
        else:  # 水平直线
            # 该直线与第一列的交点
            pt1 = (0, int(rho / math.sin(theta)))
            # 该直线与最后一列的交点
            pt2 = (result.shape[1], int((rho - result.shape[1] * math.cos(theta)) / math.sin(theta)))
            # 绘制一条直线
            # cv2.line(result, pt1, pt2, (255), 1)
            # print 'else', pt1, pt2
            # time.sleep(2)
            # cv2.waitKey(4000)
    cv2.imshow('Result', result)
    cv2.setMouseCallback('Result', my_event)
    # cv2.waitKey(0)
    print 'len ptt', len(ptt), ptt
    targetx_end = []
    calc(ptt)
    print 'targetx_end', targetx_end
    # cv2.waitKey(0)
    dis = 2
    a = 0  # 是否在直线周围，１为真
    big_area = 1000  # 第二次检测使用的参数
    b = 0  # 是否宽度统一
    yellow_pic_data = []
    jia = 0  # 是否已经处理了坐标
    w1 = 0  # 判断宽度是否统一
    # x, y, w, h = None
    w, alpha = cal_num(targetx_end)  # 返回黄杆宽度和水平偏角
    print 'w,alpha', w, alpha
    KNOWN_WIDTH = 5  # 黄杆的宽
    focalLength = 264.0
    distance = (KNOWN_WIDTH * focalLength) / w
    print 'distance', distance
    # cv2.setMouseCallback('Canny', my_event)
    # cv2.setMouseCallback('Result', my_event)
    cv2.waitKey(0)
