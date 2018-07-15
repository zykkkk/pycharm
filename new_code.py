# coding:utf8
# 日志模块暂时取消了
from naoqi import ALProxy
import math
import almath
import time
import logging

IP = '172.16.55.80'
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


# 初始化
def naoInit():
    """开始前机器人的初始化"""
    # 1、站起来
    # g_motion.wakeUp()
    # // StandInit动作
    g_posture.goToPosture("StandInit", 0.5)
    # 第一次准备拿杆动作
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.3, 0.2)
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", 0.77, 0.2)
    g_motion.angleInterpolationWithSpeed("LShoulderRoll", -1.5, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowRoll", -0.9, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowYaw", -1.8, 0.2)

    # 拿杆
    g_motion.angleInterpolationWithSpeed("LHand", 1.0, 0.2)
    time.sleep(3)
    g_motion.angleInterpolationWithSpeed("LHand", 0.15, 0.2)
    g_motion.setStiffnesses("LHand", 1.0)
    print('init over')


# ------第一场-----------
def firstHitBallForOne():
    """
        第一场第一次击球
    """
    time.sleep(3)
    print('first hit begin')
    # 触摸右手击球
    # g_motion.angleInterpolationWithSpeed("LWristYaw", 1.5, 0.1)
    # g_motion.angleInterpolationWithSpeed("LWristYaw", -0.9, 0.5)
    # g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)
    # 第二个场地
    g_motion.angleInterpolationWithSpeed("LWristYaw", 1.2, 0.1)
    g_motion.angleInterpolationWithSpeed("LWristYaw", -0.6, 0.3)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)
    # motionProxy.angleInterpolationWithSpeed("LWristYaw", 1.2, 0.1)
    # motionProxy.angleInterpolationWithSpeed("LWristYaw", -0.6, 0.3)
    # motionProxy.angleInterpolationWithSpeed("LWristYaw", 0.3, 0.05)


def firstHitBallForOne2():
    """
        第一场第一次击球
    """
    time.sleep(3)
    print('second hit begin')
    # 触摸右手击球
    # g_motion.angleInterpolationWithSpeed("LWristYaw", 1.2, 0.1)
    # g_motion.angleInterpolationWithSpeed("LWristYaw", -0.6, 0.23)
    # g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 1.5, 0.1)
    g_motion.angleInterpolationWithSpeed("LWristYaw", -0.9, 0.5)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)


def firstHitBallForTest():
    """
        第一场第一次击球
    """
    # 触摸右手击球
    while True:
        if g_memory.getData("HandRightRightTouched"):
            # g_motion.angleInterpolationWithSpeed("LWristYaw", 1.5, 0.1)
            # g_motion.angleInterpolationWithSpeed("LWristYaw", -0.9, 0.5)
            g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)
            break

# 第二个场地
def firstMain():
    """第一场"""
    # 初始化日志配置
    # 1、初始化（站立，接杆）
    naoInit()
    # times = 0  # 除固定击球以外击球次数
    # 2、第一次击球
    firstHitBallForOne()
    # 3、第一次击球后行走
    # 3.1、行走前收杆
    actionBeforeMove()


g_motion.wakeUp()
naoInit()
firstHitBallForOne2()  # 击球有好几个函数，不知道是哪一个真正在用
g_motion.rest()
