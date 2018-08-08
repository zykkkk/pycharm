# coding=utf-8
import math
import cv2
import time
import almath
from naoqi import ALProxy
import sys
import logging

# for i in xrange(7):
#     print i,
# print
# print xrange(7)
# for i in range(7):
#     print i,
# print
# print range(7)

# for i in range(14):
#     j = i / 7
#     k = i % 7
#     if j > 0:
#         anger = almath.TO_RAD * (-k * 30 + 90)
#         print anger
#     else:
#         anger = almath.TO_RAD * (k * 30 - 90)
#         print anger

# a='test'
# b='test'
# if a==b:
#     print 'haha'

# a=-1
# for i in range(8):
#     j = i / 4
#     k = i % 4
#     if j == 0:
#         anger = almath.TO_RAD * (k * 30) * a
#         print anger
#     else:
#         anger = almath.TO_RAD * (90-k * 30) * a
#         print anger

# a=1,2,3
# print(len(a))
# for i in a:
#     print(i)

# a=range(2,7)
# for i in a:
#     print(i,end=',')

# a=math.pi
# print (round(a,3))

# a=(1,2,3)
# print a[1]

# headYawAngle = -110 * almath.TO_RAD  # 摆头角度，从右往左扫
# # headYawAngle=-110
# times = 0
# while times < 2:
#     anger=headYawAngle
#     print anger,
#     if headYawAngle * almath.TO_DEG > 130:
#         headYawAngle = -130 * almath.TO_RAD  # 摆头角度，从右往左扫
#         times += 1
#         continue
#     headYawAngle += 39 * almath.TO_RAD
#
# print
#
# headYawAngle=-110
# times = 0
# while times < 2:
#     anger=headYawAngle
#     print anger,
#     if headYawAngle > 130:
#         headYawAngle = -130 # 摆头角度，从右往左扫
#         times += 1
#         continue
#     headYawAngle += 39


# a=1
# cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     ok, frame = cap.read()  # 读取一帧数据
#     cv2.resizeWindow('frame',320,240)
#     cv2.imshow('frame',frame)
#     c = cv2.waitKey(1)
#     if c & 0xFF ==ord('c'):
#         cv2.imwrite('/home/sl/my/pycharm_workspaces/__pictures__/landmark/%d.jpg' %a,frame)
#         print 'have write %d picture' %a
#         a+=1
#     if c & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

# a=[-11,2,3,4,5]
# print max(a,key=lambda x: abs(x))


# func = lambda x: x + 1
# print(func(1))
# print(func(2))
#
#
# # 以上lambda等同于以下函数
# def func(x):
#     return (x + 1)

# a=[[[259,232]], [[259,247]], [[265, 247]], [[265, 232]]]
# print a[0][0][0]
# for i in a:
#     for j in i:
#         print j


# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='/tmp/test.log',
#                     filemode='w')
# logging.debug('debug message')
# logging.info('info message')
# logging.warning('warning message')
# logging.error('error message')
# logging.critical('critical message')

# print 4 == 4.
# if not type(4) == type(4.):
#     print type(4)
#     print (type(4.))

# print math.pi / 4.
# print 3. * math.pi / 4.0
# print 0.785398163397*180/math.pi  # 45度
# print 2.35619449019*180/math.pi  # 135度
# i=88.9
# # while i <91.1:
# #     print i*math.pi/180
# #     i+=0.1
# print 89*math.pi/180
# print 91*math.pi/180
# print '1.56',int(math.tan(1.56))  # 结果是斜率,数字是弧度 1.56
# print '1.57',int(math.tan(1.57))
# print '1.58',int(math.tan(1.58))
# print math.tan(91)


# print 5 and 1
# print 5 or 0
# print 1 or 0


# def a():
#     return 3
# def b():
#     return a()
# print(b())


x=1
if 1:
    for i in range(2):
        x=0
        x+=2
print(x)  # 改变了x