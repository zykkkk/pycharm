# coding=utf-8
import cv2
import math
import time
import numpy as np


# 0 40 10
# 1 40 7
# 3 40 9
# 4 40 6
# 5 40 6


def my_event(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        print ptt
        print targetx_end
        print x


def paixu(target):
    for i in range(len(target)):
        for j in range(len(target)):
            if target[i][1][0] < target[j][1][0]:
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
    t = targetx[0]
    print t
    for i in targetx:
        # print 'i',i
        if 0 <= i[1][0] - t[1][0] <= 3:
            t = i
        else:
            targetx_end.append(t)
            t = i
    targetx_end.append(t)


def find_yellow(Img, yellow):
    global times, a, area0, big_area, b, w, x, y, h,jia
    cv2.imshow('Img',Img)
    # cv2.waitKey(0)
    print yellow
    # time.sleep(3)
    print 'times', times
    if Img is  None:  # 判断图片是否读入
        print 'there is no picture'
        exit(0)
    HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
    # yellow = [[16, 0, 180], [50, 85, 255]]  # bright 3 4 5 12 13 14 15 16 17 21 22  use 2*2 kernel
    # yellow = [[14, 0, 0], [28, 115, 220]]  # not bright 6 7  use 4*4 kernel
    # yellow = [[14, 0, 0], [40, 115, 220]]  # not bright 8 11 12 18 19   use 4*4 kernel

    Lower, Upper = np.array(yellow)
    # mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
    mask = cv2.inRange(HSV, Lower, Upper)
    dilation = mask
    # target是把原图中的非目标颜色区域去掉剩下的图像
    target = cv2.bitwise_and(Img, Img, mask=dilation)
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
        if cv2.contourArea(i) > cv2.contourArea(area) and cv2.contourArea(i) != big_area:
            area = i

    x, y, w, h = cv2.boundingRect(area)
    # print 'x,y,w,h',x,y,w,h
    cv2.rectangle(target, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.imshow('target', target)
    # cv2.waitKey(0)
    for i in range(len(targetx_end)):
        if abs(x - targetx_end[i][0][0]) <= 10:
            a = a or 1
        else:
            a = a or 0
    if w <= 10 or w >= 50 or h < 20 or h > 150 or a == 0:
        print 'w,h', w, h
        if times == 1:
            times += 1
            print '调用　１　'
            area, x, y, w, h= find_yellow(Img, yellow2)  # 更换颜色区域继续寻找
        elif times == 2:
            times += 1
            print '调用　２　'
            area, x, y, w, h = find_yellow(Img, white)
        else:
            print 'not find yellow find again'
            big_area = cv2.contourArea(area)
            a = 0
            times = 1
            print '调用　３　'
            area, x, y, w, h = find_yellow(Img, yellow1)
    if w > 20:
        if b == 0:
            yellow_pic_data.append((x, y, w, h))
            print 'yellow_pic_data', yellow_pic_data
            print 'test 黄杆'
            Img1 = Img[y + h / 7:y + 5 * h / 7, x:x + w]
            # cv2.rectangle(target, (x, y), (x + w, y + h), (0, 255, 0), 1)
            # Img1=Img[x:x+w,y+h/7:y+5*h/7]
            cv2.imshow('test Img1', Img1)
            cv2.waitKey(0)
            print '调用　４　'
            area1, x1, y1, w1, h1 = find_yellow(Img1, yellow)
            # x1, y1, w1, h1 = cv2.boundingRect(area1)
            if abs(w1 - w) <= 3:
                b = 1
                print 'finded'
            else:
                print '调用　５　'
                area, x, y, w, h = find_yellow(Img1, yellow1)
    # x, y, w, h = cv2.boundingRect(area)
    print 'x,y,w,h---1', x, y, w, h
    print 'yellow_pic_data end',yellow_pic_data
    if jia==0:
        for i in range(len(yellow_pic_data)):
        # if len(yellow_pic_data) == 1:
            x = x + yellow_pic_data[i][0]
            y = y + yellow_pic_data[i][1]
            jia=1
    print 'x,y,w,h---2', x, y, w, h
    print 'there yellow pic data ',yellow_pic_data
    cv2.rectangle(target, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.rectangle(Img, (x - n, y - n), (x + w + n, y + h + n), (0, 255, 0), 1)
    print 'Img there'
    # cv2.imshow('Img_there',Img)
    # cv2.waitKey(0)
    cv2.imshow('test', Img)
    cv2.imshow('target', target)
    print w
    print 'find yellow ready return'
    return area,x,y,w,h


def cal_num(targetx_end):
    global dis
    print 'dis', dis
    print 'length targetx_end', len(targetx_end)
    alpha = None
    w = None
    if len(targetx_end) < 2:
        print 'cal_num targetx_end error <2'
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
        area,x, y, w, h = find_yellow(img0, yellow1)
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
    yellow1 = [[16, 0, 180], [50, 85, 255]]
    yellow2 = [[14, 0, 0], [40, 115, 220]]  # not bright
    white = [[0, 0, 221], [180, 30, 255]]  # new white's lower and upper
    # yellow = white
    times = 1
    n = 0
    image_num = 8
    img0 = cv2.imread("../pic/%d.jpg" % image_num)
    cv2.imshow('img0', img0)
    # find_yellow(img0)
    # exit(0)
    b = 70  # 能看到杆子的全部
    # b=40  # 看不到杆子的全部
    # img0 = cv2.imread("../pic/%d.jpg" % a)
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)  # 貌似可加可不加
    img = cv2.GaussianBlur(img, (3, 3), 0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, math.pi / 180, b)  # 这里对最后一个参数(最小的像素点数)使用了经验型的值
    result = img.copy()
    cv2.imshow('Canny', edges)
    ptt = []
    print result.shape  # 返回宽,长,3
    for line in lines[0]:
        rho = line[0]  # 第一个元素是距离rho
        theta = line[1]  # 第二个元素是角度theta 极角,弧度
        jiao = abs(theta / math.pi * 180)
        # if (theta < (math.pi / 4.)) or (theta > (3. * math.pi / 4.0)):  # 垂直直线
        if (theta < 0.78) or (theta > 2.35):  # 45度到135度
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
    print 'len ptt', len(ptt), ptt
    targetx_end = []
    calc(ptt)
    print 'targetx_end', targetx_end
    cv2.setMouseCallback('Canny', my_event)
    cv2.setMouseCallback('Result', my_event)
    # cv2.waitKey(0)
    dis = 2
    a = 0  # 是否在直线周围，１为真
    big_area = None  # 第二次检测使用的参数
    b = 0  # 是否宽度统一
    yellow_pic_data = []
    jia=0
    # x, y, w, h = None
    w, alpha = cal_num(targetx_end)  # 返回黄杆宽度和水平偏角
    print 'w,alpha', w, alpha
    KNOWN_WIDTH = 5  # 黄杆的宽
    focalLength = 264.0
    distance = (KNOWN_WIDTH * focalLength) / w
    print 'distance', distance
    cv2.waitKey(0)
