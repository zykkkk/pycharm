# coding:utf8
from naoqi import ALProxy
import math
import almath
import time
import numpy as np
import logging
import random
import cv2

# IP = '172.16.55.80'
IP = '192.168.1.192'
Port = 9559

# 步伐参数配置
g_moveConfig1 = [["MaxStepX", 0.04], ["MaxStepY", 0.13], ["MaxStepTheta", 0.4], ["MaxStepFrequency", 0.5],
                 ["StepHeight", 0.0155], ["TorsoWx", 0.0], ["TorsoWy", 0.0]]

g_moveConfig2 = [["MaxStepX", 0.04], ["MaxStepY", 0.13], ["MaxStepTheta", 0.4], ["MaxStepFrequency", 0.65],
                 ["StepHeight", 0.023], ["TorsoWx", 0.0], ["TorsoWy", 0.0]]

g_moveConfig = [["MaxStepX", 0.04], ["MaxStepY", 0.13], ["MaxStepTheta", 0.4], ["MaxStepFrequency", 0.6],
                ["StepHeight", 0.02], ["TorsoWx", 0.0], ["TorsoWy", 0.0]]
# LandMark及ball参数
landmark = {"size": 0.09}
ball = {'name': 'RedBall', 'diameter': 0.04}

g_landmarkDetection = ALProxy("ALLandMarkDetection", IP, Port)  # landMark检测模块
g_memory = ALProxy("ALMemory", IP, Port)  # 内存管理模块
g_tts = ALProxy("ALTextToSpeech", IP, Port)  # 说话模块
g_motion = ALProxy("ALMotion", IP, Port)  # 移动模块
g_posture = ALProxy("ALRobotPosture", IP, Port)  # 姿势模块
g_camera = ALProxy("ALVideoDevice", IP, Port)  # 摄像头管理模块
g_tracker = ALProxy("ALTracker", IP, Port)  # 追踪模块

g_motion.angleInterpolationWithSpeed("HeadPitch", 5 * almath.TO_RAD, 0.3)
# g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.3)
distance = 0
angle = 0
# get NAOqi module proxy
# videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)
# motionProxy = ALProxy("ALMotion", ip_addr, port_num)
# postureProxy = ALProxy("ALRobotPosture", ip_addr, port_num)
# memoryProxy = ALProxy("ALMemory", ip_addr, port_num)
g_motion.setStiffnesses("Head", 1.0)


def test1():
    # subscribe top camera
    AL_kTopCamera = 0
    AL_kQVGA = 1  # 320*240
    AL_kBGRColorSpace = 13
    # create image
    name = str(random.random())
    g_motion.angleInterpolationWithSpeed("HeadPitch", 5 * almath.TO_RAD, 0.3)
    # g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.3)
    captureDevice = g_camera.subscribeCamera(
        name, AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)

    result = g_camera.getImageRemote(captureDevice)


def findRedBallUseTop():
    """
    使用上摄像头找球
    :return:
    """
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
    captureDevice = g_camera.subscribeCamera(
        name, AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)

    for times in xrange(10):
        print times
        image = np.zeros((height, width, 3), np.uint8)
        # get image
        result = g_camera.getImageRemote(captureDevice)

        if result is None:
            print 'cannot capture.'

        elif result[6] is None:
            print 'no image data string.'
            print result[6]

        else:
            # translate value to mat
            # imgHeader our image binary to the openCV image

            values = map(ord, list(result[6]))
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    image.itemset((y, x, 0), values[i + 0])
                    image.itemset((y, x, 1), values[i + 1])
                    image.itemset((y, x, 2), values[i + 2])
                    i += 3
        cv2.imshow('test',image)