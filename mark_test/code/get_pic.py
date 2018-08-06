# coding=utf-8
import random
import cv2
from naoqi import ALProxy
import almath
import numpy as np

a=5
IP = "172.16.55.80"
Port = 9559

g_motion = ALProxy("ALMotion", IP, Port)  # 移动模块

g_videoDevice = ALProxy("ALVideoDevice", IP, Port)
g_motion.setStiffnesses("Head", 1.0)

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
#np.zeros返回一个给定形状和类型的用0填充的数组；
image = np.zeros((height, width, 3), np.uint8)#,unit8（无符号的整数，unit8是0～255）
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
#map第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。
#ord函数返回字符串对应的 ASCII 数值
    values = map(ord, list(result[6]))
    i = 0
    for y in range(0, height):
        for x in range(0, width):
            image.itemset((y, x, 0), values[i + 0])
            image.itemset((y, x, 1), values[i + 1])
            image.itemset((y, x, 2), values[i + 2])
            i += 3
    cv2.imshow('image',image)
cv2.imwrite('../%d.jpg' %a,image)
cv2.waitKey(0)
cv2.destroyAllWindows()
