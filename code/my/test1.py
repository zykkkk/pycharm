# coding=utf-8
import math
import cv2
import time
import almath
from naoqi import ALProxy
import sys

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

