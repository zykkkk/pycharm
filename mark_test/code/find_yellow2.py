# coding=utf-8
import cv2
import numpy as np


def find_yellow(Img, yellow):
    global times, big_area, b, jia, a, target_picture
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
    target_picture = cv2.bitwise_and(Img, Img, mask=dilation)
    # cv2.imshow('target_picture', target_picture)
    # 将滤波后的图像变成二值图像放在binary中
    ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
    # 在binary中发现轮廓，轮廓按照面积从小到大排列 findContours常用来获取轮廓
    contours_image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('t',hierarchy)
    # time.sleep(3)
    print(len(contours))
    area = contours[0]
    # print(big_area)
    for i in contours:  # 遍历所有的轮廓
        #  --------------------重点修改，根据杆子宽，高，区域面积大小，位置(下边那段)，找出杆子
        if cv2.contourArea(area) < cv2.contourArea(i) < big_area:
            area = i
    x, y, w, h = cv2.boundingRect(area)
    # print 'x,y,w,h',x,y,w,h
    cv2.rectangle(target_picture, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.imshow('target_picture', target_picture)
    print 'waitKey there'
    cv2.waitKey(0)
    for i in range(len(targetx_end)):
        if abs(x - targetx_end[i][0][0]) <= 10:
            a = a or 1  # 有一个直线就可以，不用每一个都满足
        else:
            a = a or 0
    # if w <= 5 or w >= 50 or h < 20 or h > 170 or a == 0:
    if (w <= 5 and c == 0) or w >= 50 or h < 20 or h > 170 or a == 0:  # c=0则是正常执行，c=1时解除w>5的限制
        # 宽度，高度是否合理，是否周围有直线,c 是否是寻找另一颜色区域
        print('------------------re find_yellow--------------------')
        print 'w,h', w, h
        if times == 1:
            times += 1
            print '调用　１　'
            yellow, x, y, w, h = find_yellow(Img, yellow2)  # 更换颜色区域继续寻找
        elif times == 2:
            times += 1
            print '调用　２　'
            yellow, x, y, w, h = find_yellow(Img, white)
        elif times == 3:
            times += 1
            print '调用 ６'
            yellow, x, y, w, h = find_yellow(Img, yellow3)
        else:
            print 'not find yellow find again'
            big_area = cv2.contourArea(area)  # 限定最大的 area ，重新执行
            if big_area <= 5:
                print 'big area error'
                exit(0)
            a = 0
            times = 1
            print '调用　３　'
            yellow, x, y, w, h = find_yellow(Img, yellow1)
    else:
        print('w,h', w, h)
        print('-----------------find yellow over return------------------')
        cv2.waitKey(0)
    return yellow, x, y, w, h


def select_yellow(Img,yellow):
    global w1, b, c, jia, yellow_pic_data
    yellow, x, y, w, h = find_yellow(Img, yellow)
    if yellow == yellow1 or yellow == yellow3:
        x0, y0, w0, h0 = x, y, w, h  # 记录数据，用于比较
        c = 1
        if yellow == yellow1:
            print('yellow == yellow1')
            yellow, x, y, w, h = find_yellow(Img, yellow3)
        else:
            print('yellow == yellow3')
            yellow, x, y, w, h = find_yellow(Img, yellow1)
        if x - (x0 + w0) <= 1 or (x0 + w0) - (x + w) <= 1:  # 先检测到的再左边 or 先检测到的再右边
            x = min(x, x0)
            y = min(y, y0)
            w = w0 + w
            print('x y w 修正结束', x, y, w)
        else:
            print('无需修正')
        c = 0
    else:
        print('yellow not in  yellow1&3', yellow)
    print('-------------修正over--------------')
    print('b', b)
    # if b == 0:  # 是否是在确认宽度统一，如果确认中则跳过此区域
    if w > 25 and abs(w - w1) > 5:  # 运行结果是w==20，跳过了这里 ，改为 or 试一下？
        print '----------------------test 黄杆-----------------------'
        print 'w,w1', w, w1
        w1 = w  # 重新给 w1 赋值
        yellow_pic_data.append((x, y, w, h))
        print 'yellow_pic_data', yellow_pic_data
        Img1 = Img[y + h / 7:y + 6 * h / 7, x - 10:x + w + 10]
        cv2.imshow('test Img1', Img1)
        print '调用　４　'  # 再次获取颜色范围
        b = 1
        x, y, w, h = select_yellow(Img1,yellow)
        print 'w', w
        # x1, y1, w1, h1 = cv2.boundingRect(area1)
        if abs(w1 - w) <= 3:
            print 'find yellow'
        else:
            print('not find yellow go to return')
            print '调用　５　'
            yellow_pic_data = []
            # w1 = 0  # 加上这里可能引起死循环，不加不准
            print('----------------------re select yellow-----------------------')
            select_yellow(Img,yellow)  # 重新执行,跳过了test yellow
    else:
        print('have not 修正 w,w1', w, w1)
    print('-----------------------test yellow over-----------------------')
    print 'x,y,w,h---1', x, y, w, h
    print 'yellow_pic_data end', yellow_pic_data
    if jia == 0:
        for i in range(len(yellow_pic_data)):
            # if len(yellow_pic_data) == 1:
            x = x + yellow_pic_data[i][0] - 10
            y = y + yellow_pic_data[i][1]
            jia = 1
    print('--------------------x,y增加结束--------------------')
    print 'x,y,w,h---2', x, y, w, h
    print 'there yellow pic data ', yellow_pic_data
    cv2.rectangle(target_picture, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.rectangle(Img, (x - n, y - n), (x + w + n, y + h + n), (0, 255, 0), 1)
    print 'Img there'
    cv2.imshow('test', Img)
    cv2.imshow('target', target_picture)
    print 'width', w
    print '----------------------select yellow return--------------------------'
    # else:
    #     b = 0
    #     return x, y, w, h  # 用于第二次寻找区域的宽度
    return x, y, w, h


n = 10
yellow1 = [[16, 0, 180], [50, 85, 255]]  # bright
yellow2 = [[14, 0, 0], [40, 115, 220]]  # inside bright and not bright
yellow3 = [[26, 77, 46], [35, 255, 255]]  # not bright
white = [[0, 0, 221], [180, 30, 255]]  # new white's lower and upper
# yellow = white

times = 1
targetx_end = [((152, 0), (160, 240)), ((170, 0), (161, 240)), ((178, 0), (173, 240))]
yellow_pic_data = []
big_area = 2500
a = 0  # 是否在直线周围，１为真
b = 0  # 是否宽度统一， 1为真
c = 0  # 用于分段颜色查找， 初始0
w1 = 0  # 用来判断宽度是否统一， 记录前一个宽度的值
jia = 0  # 是否已经处理了坐标， 加上宽度 10

pic_num=1
image = cv2.imread('../pic/%d.jpg' %pic_num)
select_yellow(image,yellow1)
