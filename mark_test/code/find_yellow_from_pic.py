# coding:utf-8
import cv2
import numpy as np
import time
from PIL import Image
import sys

# dont find 1 2 9 10 20
# with 2*2 kernel can fand 3 4 5 6 7 12 13 14 15 16 17
# with 4*4 kernel can find 8 11
# with no kernel just test8.png cant find

a=5
def mohu(res,x):
    res2 = cv2.blur(res, x)
    # res2 = cv2.dilate(res2, kernel_4, iterations=1)
    res2 = cv2.erode(res2, kernel_4, iterations=1)  # erode 侵蝕 being small
    res2 = cv2.erode(res2, kernel_4, iterations=1)  # erode 侵蝕 being small
    res2 = cv2.dilate(res2, kernel_4, iterations=1)
    res2 = cv2.dilate(res2, kernel_4, iterations=1)

    return res2
if __name__ == '__main__':
    # print(sys.argv)
    # Img = cv2.imread('/home/sl/my/pycharm_workspaces/naoproj/find_color/test_picture/color.jpg')  # 读入一幅图像
    # Img = cv2.imread('../../nao_pic/test3.png')
    # Img = cv2.imread('../../nao_pic/test4.png')
    # Img = cv2.imread('../../nao_pic/test6.png')
    Img = cv2.imread('../pic/%d.jpg' %a)
    # Img = cv2.imread('../../nao_pic/test8.png')
    # Img = cv2.imread('../../nao_pic/test22.png')
    # Img = cv2.imread('/home/sl/my/pycharm_workspaces/naoproj/find_color/test_picture/yellow.png')  # 读入一幅图像
    # Img = cv2.imread('/home/sl/my/pycharm_workspaces/naoproj/find_color/code/test.png')  # 读入一幅图像
    # Image.open('/home/sl/my/pycharm_workspaces/naoproj/find_color/code/test.png').show()
    # Image.open('test.png').show()   # 不知道什么毛病,pycharm 软件读取不到相对路径,重启有效没有不知道,应该有效的
    # sys.exit(0)
    # Img = cv2.imread('../test_picture/color.jpg')  # 读入一幅图像
    # kernel_4 = np.ones((2, 2), np.uint8)  # 2x2的卷积核
    # kernel_4 = np.ones((3, 3), np.uint8)  # 3x3的卷积核
    kernel_4 = np.ones((4, 4), np.uint8)  # 4x4的卷积核
    if Img is not None:  # 判断图片是否读入
        cv2.imshow('test', Img)
        HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)  # 把BGR图像转换为HSV格式
        '''
  HSV模型中颜色的参数分别是：色调（H），饱和度（S），明度（V）  H(0-180) S(0-255) V(0-255)
    H(26-35) S(77-255) V(46-255)
  下面两个值是要识别的颜色范围
  '''
        # Lower = np.array([20, 20, 20])  # 要识别颜色的下限
        # Upper = np.array([30, 255, 255])  # 要识别的颜色的上限
        # yellow=[[26, 77, 46],[35, 255, 255]] #row yellow's lower and upper
        # white=[[0,0,221],[180,30,255]] #row white's lower and upper

        # yellow = [[0, 0, 170], [180, 30, 255]]  # test3.png
        # yellow = [[0, 0, 0], [28, 70, 255]]  # test4.png test5.png test6.png
        # yellow = [[16, 0, 0], [50, 160, 150]]  # test7.png test8.png test11.png
        # yellow = [[14, 0, 0], [40, 120, 235]]  # test12.png
        # yellow = [[16, 0, 150], [50, 255, 255]]  # test13.png
        # yellow = [[14, 0, 200], [40, 85, 255]]  #  with 2*2 kernel_4  2*2 kernel 13 14 15 16 17
        # yellow = [[20, 25, 46], [40, 85, 255]]  #18 19
        yellow = [[0, 0, 180], [50, 85, 255]]  # bright 3 4 5 12 13 14 15 16 17 21 22  use 2*2 kernel
        # yellow = [[14, 0, 0], [28, 115, 220]]  # not bright 6 7  use 4*4 kernel
        # yellow = [[14, 0, 0], [40, 115, 220]]  # not bright 8 11 12 18 19   use 4*4 kernel   9 and 10 and 20 dont should find
        # yellow = [[14, 0, 160], [40, 115, 220]]  # for 11
        # not bright LH=14 HH=28 or 50
        # need to better 11
        # amazing 19 should be find
        white=[[0,0,221],[180,30,255]] #new white's lower and upper
        # yellow=white
        Lower, Upper = np.array(yellow)
        # Lower,Upper=np.array(white)
        # Lower = np.array(yellow[0])  # 要识别颜色的下限
        # Upper = np.array(yellow[1])  # 要识别的颜色的上限
        # mask是把HSV图片中在颜色范围内的区域变成白色，其他区域变成黑色
        mask = cv2.inRange(HSV, Lower, Upper)
        cv2.imshow('mask', mask)
        mask = cv2.blur(mask, (3,3))
        cv2.imshow('blur_mask', mask)
        # 下面四行是用卷积进行滤波
        # cv2.imshow('dilation', dilation)
        # target是把原图中的非目标颜色区域去掉剩下的图像
        target = cv2.bitwise_and(Img, Img, mask=mask)
        cv2.imshow('target', target)
        # 将滤波后的图像变成二值图像放在binary中
        ret, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        # 在binary中发现轮廓，轮廓按照面积从小到大排列 findContours常用来获取轮廓
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow('t',hierarchy)
        # time.sleep(3)
        p = 0
        for i in contours:  # 遍历所有的轮廓
            print(cv2.contourArea(i))  #print the size of area
            # time.sleep(1)
            print "I",i
            # time.sleep(3)
            x, y, w, h = cv2.boundingRect(i)  # 将轮廓分解为识别对象的左上角坐标和宽、高
            # 在图像上画上矩形（图片、左上角坐标、右下角坐标、颜色、线条宽度）
            cv2.rectangle(Img, (x, y), (x + w, y + h), (0, 255,), 3)
            # 给识别对象写上标号
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(Img, str(p), (x - 10, y + 10), font, 1, (0, 0, 255), 2)  # 加减10是调整字符位置
            p += 1
        # print('there')
        # time.sleep(5)

        print('黄色方块的数量是', p, '个')  # 终端输出目标数量
        # time.sleep(1.5)
        # cv2.imshow('target', target)
        # cv2.imshow('Mask', mask)
        # cv2.imshow("prod", dilation)
        # cv2.imshow('Img', Img)
        # cv2.imwrite('Img.png', Img)  # 将画上矩形的图形保存到当前目录
        # cv2.imshow('test',image)
    else:
        print('there is no picture')
        sys.exit(0)
    cv2.waitKey(0)
