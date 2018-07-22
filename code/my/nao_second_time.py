# coding:utf8
from naoqi import ALProxy
import time
import almath
import math
import logging
import cv2
import random
import numpy as np
import sys

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
    g_tts.say('init over')
    print('init over')


# ------第二场-----------  原代码中又类似函数 firstHitBallForTwo2()
def firstHitBallForTwo():
    """
    第二场第一次击球
    """
    time.sleep(1)
    g_motion.angleInterpolationWithSpeed("LWristYaw", -0.1, 0.05)
    # g_motion.setStiffnesses("LShoulderRoll", 0)
    time.sleep(1)
    # 触摸右手击球
    # 红色机器人击球---4.5米完成（场地二）
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.9, 0.12)
    g_motion.setStiffnesses("LShoulderRoll", 1)
    # time.sleep(1)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)
    g_tts.say('hit ball five meter over')
    print('击球5米完成')


def actionBeforeMoveForTwo():
    """
    走路前的拿杆动作，第二场的，减少右手与身体的间隔，避免碰到障碍物
    """
    # // moveInit动作
    g_motion.moveInit()

    # // 打完球为走路做准备的动作
    g_motion.angleInterpolationWithSpeed("LShoulderRoll", 0.25, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowRoll", 0.0, 0.2)
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", 1.5, 0.2)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.3, 0.2)

    g_motion.angleInterpolationWithSpeed("RElbowRoll", 0.0, 0.2)
    g_motion.angleInterpolationWithSpeed("RShoulderPitch", 1.5, 0.2)
    g_motion.angleInterpolationWithSpeed("RShoulderRoll", -0.1, 0.2)

    g_motion.setMoveArmsEnabled(False, False)
    g_tts.say('prepare to move')
    print('prepare to move')


# 移动函数，包装了api的移动，同时添加了一些修正
def move(x=0.0, y=0.0, theta=0.0, config=g_moveConfig):
    """
    NAO移动：以FRAME_ROBOT坐标系为参照，theta为角度
    :param x: 前进后退 单位cm
    :param y: 左右移动 cm
    :param theta: 旋转角度，往左为正，单位度数
    :param config: 行走参数配置
    :return:
    """
    g_motion.moveInit()
    try:
        # 如果传入为小数，强转
        x1 = int(x + 0.5)
        x2 = round(x)
        y1 = round(y)
        theta1 = round(theta * almath.TO_RAD, 2)
        # 行走前初始化
        g_motion.moveInit()
        # 如果是往前走，修正
        step1 = x1 / 56
        # step2 = x1 % 56 / 20
        step3 = x1 % 56
        adjustY = 3
        adjustTheta = 7
        # print ("step1: ", step1),
        # print("   step2:  ", step2),
        # print("   step3:  ", step3),
        # 走至指定位置，解决走路偏斜问题
        # 第一段，走50cm
        if x1 > 0:
            for i in range(step1):
                g_motion.moveTo(56 * 0.01, 0, 0, config)
                g_motion.moveTo(0, 0, -adjustTheta * almath.TO_RAD, config)
                # g_motion.moveTo(0, -adjustY * 0.01, 0, config)
                if i == 2:
                    adjustY += 3
                    # adjustTheta += 1
            # 第二段 走20cm
            # for i in range(step2):
            #     g_motion.moveTo(20 * 0.01, 0, 0, config)
            #     # g_motion.moveTo(0, 0, -1 * almath.TO_RAD, config)
            g_motion.moveTo(step3 * 0.01, 0, 0, config)
        else:
            g_motion.moveTo(x1 * 0.01, 0, 0, config)
        g_motion.moveTo(0, y1 * 0.01, theta1, config)
        # 记录日志
        logging.info("---------------------move------------------")
        if x != 0.0:
            logging.info("X:::: " + str(x2) + "cm")
        elif y != 0.0:
            logging.info("Y::::" + str(y1) + "cm")
        else:
            logging.info("Z:::: " + str(theta) + "度")
    except Exception, e:
        logging.error("传入参数不合法！")
        print('移动参数错误')
        g_tts.say('i can not move,go to stop')
        stop()


# 停止函数，松杆并坐下
def stop(t=2):
    global g_motion, g_tracker, g_landmarkDetection
    # 停止追踪
    g_tracker.stopTracker()
    g_tracker.unregisterAllTargets()
    landmarkInfo = g_landmarkDetection.getSubscribersInfo()
    for info in landmarkInfo:
        g_landmarkDetection.unsubscribe(info[0])
    # 松开杆
    g_motion.openHand("LHand")
    time.sleep(t)
    g_motion.closeHand("LHand")
    g_tts.say('i will be rest')
    print('stop()')
    g_motion.rest()


# ----------------------找球并击球---------------------------
def findAndHitBall(changci=1):
    distance, headYawAngle, ballCoord = trackBall()  # 找球
    g_tts.say('first find ball over')
    print('first find ball over')
    # 此处经修改后暂无意义
    for times in xrange(1):  # xrange=[0]
        # 4.1、找到球
        if distance != -1:
            # 5、调整与球之间的距离
            actionAfterFirstFindBall(distance, headYawAngle)
            print('调整与球的距离结束')
            print "action Before find mark"
            # 6、找Landmark
            if changci != 2:
                if headYawAngle < 0:
                    g_tts.say('begin search landmark in left ')
                    print('向左找landmark')
                    robotToLandmarkData, isFind = searchLandmarkInLeft()
                else:
                    g_tts.say('begin search landmark in right')
                    print('向右找landmark')
                    robotToLandmarkData, isFind = searchLandmarkInRight()
            else:
                robotToLandmarkData, isFind = searchLandmarkInRight()
                g_tts.say('the last try to find landmark')
                print('向右找landmark')
            # 没找到，继续扫
            if not isFind:
                if changci != 2:
                    if headYawAngle < 0:
                        robotToLandmarkData, isFind = searchLandmarkInRight()
                    else:
                        robotToLandmarkData, isFind = searchLandmarkInLeft()
                else:
                    robotToLandmarkData, isFind = searchLandmarkInLeft()
            # 6.1、找到landmark
            if isFind:
                # 7、调整角度
                # 7.1 重新计算与球的距离,并获取球与landmark的距离
                distance2Ball, headYawAngle, ballCoord = trackBall(18)
                # 防止数据异常
                for i in range(5):
                    if abs(ballCoord[2]) > 50:
                        distance2Ball, headYawAngle, ballCoord = trackBall(18)
                    else:
                        break
                # 一些修正：根据实际情况进行调整
                # if headYawAngle < 0:
                if robotToLandmarkData[1] > 0:
                    if distance2Ball < 13:
                        distance2Ball = 13
                    distance2Ball += 15  # 右边15
                    # distance2Ball = 26 # 右边15
                    # distance2Ball = 23 # 右边15
                    if robotToLandmarkData[0] < 35:
                        distance2Ball -= 2
                else:
                    # distance2Ball = 14.5
                    if distance2Ball < 12:
                        distance2Ball = 12
                    if robotToLandmarkData[0] < 35:
                        distance2Ball += 1
                    distance2Ball += 3.5  # 左边
                    # distance2Ball += 2.3 #左边

                distanceFromBall2Mark = calDistanceFromBall2Mark(distance2Ball, robotToLandmarkData[0],
                                                                 robotToLandmarkData[1])
                # logging.info("distanceFromBall2Mark:  " + str(distanceFromBall2Mark))
                # 7.2、计算需移动的y值
                adjustY, adjustTheta = calAdjustY(distance2Ball, robotToLandmarkData[0], robotToLandmarkData[1],
                                                  distanceFromBall2Mark)
                # 7.3 调整距离和角度
                # time.sleep(0.5)
                # 若角度过大，进行二次修正
                if 24 > adjustY > -24:
                    move(y=adjustY)
                    move(theta=adjustTheta)
                elif adjustY > 0:
                    if adjustTheta > 0:
                        move(theta=15)
                    else:
                        move(theta=-15)
                        # move(theta=adjustTheta / 1.5)
                    move(y=24)
                else:
                    if adjustTheta > 0:
                        move(theta=15)
                    else:
                        move(theta=-15)
                    move(y=-24)
                    # move(theta=adjustTheta / 1.5)
                if adjustY > 25 or adjustY < -25:
                    if changci == 2:
                        findAndHitBall()
                    else:
                        findAndHitBall2()
                else:
                    # 7.4 、调整至击球点
                    firstClosingForHitBall(robotToLandmarkData[1])
                    # 重新获取数据
                    # distance2Ball_2, headYawAngle_2, ballCoord_2 = trackBall(18)  # 我注释的
                    g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.1)
                    g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.1)
                    # 7.5 击球
                    # 根据位置的不同决定击球方式
                    if distanceFromBall2Mark is not None:
                        if robotToLandmarkData[1] > 0:
                            outShotBall(120)
                        elif robotToLandmarkData[1] < 0:
                            insideShotBall(120)
                            # 收杆
                    actionBeforeMove()
                    break
            # 判断击球次数
            # if times > 2:
            #     break

            # 没找到landmark
            else:
                print('not find landmark')
                pass
        # 没找到球
        else:
            g_tts.say('not find ball , finished')
            print('not find ball')
            return False
    return True


def trackBall(headPitch=0):
    # 需返回的参数
    headYawAngle = -1  # 头转过的角度
    distance = -1  # 球坐标
    coord = [0.0, 0.0, 0.0]
    # 一些后面需要用的参数
    times = 0  # 扭头次数
    yawDegree = 60 * almath.TO_RAD
    # 启用下摄像头
    print 'camera is open', g_camera.isCameraOpen(0)
    g_camera.setActiveCamera(1)
    # 注册追踪物
    g_tracker.registerTarget(ball['name'], ball['diameter'])
    # 设置追踪模式
    g_tracker.setMode("Head")
    # 启动追踪
    g_tracker.track(ball['name'])
    # 睡眠2秒,给机器人追踪时间
    time.sleep(1)
    # 找球
    # 将机器人头设置到指定位置
    if headPitch != 0:
        g_motion.angleInterpolationWithSpeed("HeadPitch", headPitch * almath.TO_RAD, 0.1)
    while True:
        time.sleep(1)
        # 追踪到球
        if len(g_tracker.getTargetPosition(2)) == 3:
            # time.sleep(1)
            # 以脚部坐标系获取坐标
            coord = g_tracker.getTargetPosition(2)
            for i in range(2):
                coord = g_tracker.getTargetPosition(2)
            # 将坐标转换为cm
            for i in range(len(coord)):
                coord[i] *= 100
            # 输出坐标
            # logging.debug("x = " + str(coord[0]) + "  y = " + str(coord[1]) + " z = " + str(coord[2]))
            # 获取头转的角度
            headYawAngle = g_motion.getAngles("HeadYaw", True)[0] * almath.TO_DEG
            headPitchAngle = g_motion.getAngles("HeadPitch", True)[0] * almath.TO_DEG
            # 打印
            # logging.debug("headYawAngle:" + str( headYawAngle[0] * almath.TO_DEG) + "度")
            # logging.debug("headPitchAngle:" + str(headPitchAngle[0] * almath.TO_DEG) + "度")
            logging.debug(str(coord[0]) + "    " + str(coord[1]) + "   " + str(coord[2]) + "    " + str(
                headYawAngle) + "   " + str(headPitchAngle))

            distance = getRealDisForBall(coord[0], coord[1], coord[2], headYawAngle, headPitchAngle)
            # print("distance:", distance)
            logging.info("nao与球的距离::" + str(distance) + "    角度::" + str(headYawAngle))
            # 跳出循环
            break
        # 没找到球
        else:
            # 判断扭头次数，扫描3遍
            if times < 9:
                # 先扭头往右边观察
                if times > 5:
                    # g_camera.setActiveCamera(0)
                    g_motion.setAngles("HeadPitch", 18 * almath.TO_RAD, 0.15)
                if times % 3 == 0:
                    g_motion.angleInterpolationWithSpeed("HeadYaw", -yawDegree, 0.15)
                    times += 1
                    time.sleep(0.5)
                elif times % 3 == 2:
                    g_motion.angleInterpolationWithSpeed("HeadYaw", 0, 0.15)
                    times += 1
                    time.sleep(0.5)
                else:
                    g_motion.angleInterpolationWithSpeed("HeadYaw", yawDegree, 0.15)
                    times += 1
                    time.sleep(0.5)
                    # logging.info("转头次数:" + str(times))
                    print("转头次数:" + str(times))
            else:
                g_tts.say("ball not in sight")
                break

    # 停止追踪
    g_tracker.stopTracker()
    g_tracker.unregisterTarget(ball['name'])

    # 复原头
    g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.15)
    g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.15)

    # 输出球坐标和角度
    # logging.debug("球修正后坐标cm: " + str(coord))
    # logging.debug("机器人扭头角度:" + str(headAngle[0]))
    # 返回距离和角度
    return round(distance, 2), round(headYawAngle, 4), coord


# ----------------------------Landmark相关---------------------------------
# 扫描顺序为 -110 -71 -32 7 46 85 124 163 -130 -91 -52 -13 26 65 104 143  往左为正
def searchLandmarkInRight():
    """
    搜索Landmark，返回
    :return:landmarkData(角度，距离),isFindLandMark
    """
    global g_motion, g_landmarkDetection, g_camera
    isFindLandmark = False  # landmark识别符0代表识别到，1代表未识别到。
    robotToLandmarkData = []
    headYawAngle = -110 * almath.TO_RAD  # 摆头角度，从右往左扫
    currentCamera = "CameraTop"
    # 初始化
    # # 重置头部角度
    # g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    # g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.3)
    # 设置刚度为 1 保证其头部能够运转
    g_motion.setStiffnesses("Head", 1.0)
    # 开启上摄像头
    g_camera.setActiveCamera(0)
    # 注册事件
    g_landmarkDetection.subscribe("landmarkTest")

    g_motion.angleInterpolationWithSpeed("HeadPitch", -0.1, 0.3)
    # time.sleep(2)
    # 初始为-1.5，及从由往左观察
    times = 0
    addAngle = 39 * almath.TO_RAD
    while times < 2:
        time.sleep(3)
        markData = g_memory.getData("LandmarkDetected")
        # 找到landmark
        if markData and isinstance(markData, list) and len(markData) >= 2:
            # 提示
            g_tts.say("find landmark!")
            # 置标志为rue
            isFindLandmark = True  # landmark识别符1代表识别到，0代表未识别到。
            # Retrieve landmark center position in radians.
            # 获取数据
            alpha = markData[1][0][0][1]
            beta = markData[1][0][0][2]
            # Retrieve landmark angular size in radians.
            landmarkWidthInPic = markData[1][0][0][3]
            # print ("alpha: ",alpha)
            # print ("beta: ", beta)
            # print landmarkWidthInPic

            # 获取头转动角度
            headAngle = g_motion.getAngles("HeadYaw", True)

            print ("headAngle:", headAngle)
            markWithHeadAngle = alpha + headAngle[0]  # landmark相对机器人头的角度

            # 头部正对landmark
            g_motion.angleInterpolationWithSpeed("HeadYaw", markWithHeadAngle, 0.2)

            # ----------------------------------计算距离-----------------------------------------------#
            distanceFromCameraToLandmark = landmark["size"] / (2 * math.tan(landmarkWidthInPic / 2))

            # 获取当前机器人到摄像头的距离的变换矩阵
            transform = g_motion.getTransform(currentCamera, 2, True)
            transformList = almath.vectorFloat(transform)
            robotToCamera = almath.Transform(transformList)
            # 打印
            # print("transform:", transform)
            # print("transformList :", transformList)
            # print("robotToCamera :", robotToCamera)

            # 计算指向landmark的旋转矩阵
            cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, beta, alpha)

            # 摄像头到landmark的矩阵
            cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

            # 机器人到landmark的矩阵
            robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform
            # 打印
            # print("cameraToLandmarkRotationTransform: " ,cameraToLandmarkRotationTransform)
            # print("cameraToLandmarkTranslationTransform: ",cameraToLandmarkTranslationTransform)
            # print("robotToLandmark",robotToLandmark )
            x = robotToLandmark.r1_c4
            y = robotToLandmark.r2_c4
            z = robotToLandmark.r3_c4

            distance = math.sqrt(x ** 2 + y * y) * 100

            markWithHeadAngle = round(markWithHeadAngle, 2)
            # 将数据存入列表
            robotToLandmarkData.append(distance)
            robotToLandmarkData.append(markWithHeadAngle)
            # 记录日志
            logging.info("x = " + str(x))
            logging.info("y = " + str(y))
            logging.info("z = " + str(z))
            logging.info("nao与landmark的距离 :: " + str(distance) + "   角度:: " + str(markWithHeadAngle * almath.TO_DEG))
            # 找到landmark，跳出循环
            break

        # 没找到landmark，该变角度继续扫视
        g_motion.angleInterpolationWithSpeed("HeadYaw", headYawAngle, 0.12)
        if headYawAngle * almath.TO_DEG > 130:
            headYawAngle = -130 * almath.TO_RAD  # 摆头角度，从右往左扫
            times += 1
            continue
        # elif times == 0:
        #     headYawAngle = headYawAngle + (55 * almath.TO_RAD)
        # elif times == 1:
        headYawAngle += 39 * almath.TO_RAD
        # if headYawAngle
        # else:
        #     headYawAngle = headYawAngle - (20 * almath.TO_RAD)
    # 提示
    if not isFindLandmark:
        print "landmark is not in sight !"
        g_tts.say("landmark is not in sight")
    # 取消事件
    g_landmarkDetection.unsubscribe("landmarkTest")
    g_camera.unsubscribe("AL::kTopCamera")

    # 调整头的角度
    g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.2)
    g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.2)
    return robotToLandmarkData, isFindLandmark


def searchLandmarkInLeft():
    """
    搜索Landmark，返回
    :return:landmarkData(角度，距离),isFindLandMark
    """
    global g_motion, g_landmarkDetection, g_camera
    isFindLandmark = False  # landmark识别符0代表识别到，1代表未识别到。
    robotToLandmarkData = []
    headYawAngle = 110 * almath.TO_RAD  # 摆头角度，从右往左扫
    currentCamera = "CameraTop"
    # 初始化
    # # 重置头部角度
    # g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.3)
    # g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.3)
    # 设置刚度为 1 保证其头部能够运转
    g_motion.setStiffnesses("Head", 1.0)
    # 开启上摄像头
    g_camera.setActiveCamera(0)
    # 注册事件
    g_landmarkDetection.subscribe("landmarkTest")

    g_motion.angleInterpolationWithSpeed("HeadPitch", -0.1, 0.3)
    # time.sleep(2)
    # 初始为-1.5，及从由往左观察
    times = 0
    addAngle = -39 * almath.TO_RAD
    while times < 2:
        time.sleep(3)
        markData = g_memory.getData("LandmarkDetected")
        # 找到landmark
        if markData and isinstance(markData, list) and len(markData) >= 2:
            # 提示
            g_tts.say("find landmark!")
            # 置标志为rue
            isFindLandmark = True  # landmark识别符1代表识别到，0代表未识别到。
            # Retrieve landmark center position in radians.
            # 获取数据
            alpha = markData[1][0][0][1]
            beta = markData[1][0][0][2]
            # Retrieve landmark angular size in radians.
            landmarkWidthInPic = markData[1][0][0][3]
            # print ("alpha: ",alpha)
            # print ("beta: ", beta)
            # print landmarkWidthInPic

            # 获取头转动角度
            headAngle = g_motion.getAngles("HeadYaw", True)

            print ("headAngle:", headAngle)
            markWithHeadAngle = alpha + headAngle[0]  # landmark相对机器人头的角度

            # 头部正对landmark
            g_motion.angleInterpolationWithSpeed("HeadYaw", markWithHeadAngle, 0.2)

            # ----------------------------------计算距离-----------------------------------------------#
            distanceFromCameraToLandmark = landmark["size"] / (2 * math.tan(landmarkWidthInPic / 2))

            # 获取当前机器人到摄像头的距离的变换矩阵
            transform = g_motion.getTransform(currentCamera, 2, True)
            transformList = almath.vectorFloat(transform)
            robotToCamera = almath.Transform(transformList)
            # 打印
            # print("transform:", transform)
            # print("transformList :", transformList)
            # print("robotToCamera :", robotToCamera)

            # 计算指向landmark的旋转矩阵
            cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, beta, alpha)

            # 摄像头到landmark的矩阵
            cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

            # 机器人到landmark的矩阵
            robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform
            # 打印
            # print("cameraToLandmarkRotationTransform: " ,cameraToLandmarkRotationTransform)
            # print("cameraToLandmarkTranslationTransform: ",cameraToLandmarkTranslationTransform)
            # print("robotToLandmark",robotToLandmark )
            x = robotToLandmark.r1_c4
            y = robotToLandmark.r2_c4
            z = robotToLandmark.r3_c4

            distance = math.sqrt(x ** 2 + y * y) * 100  # 机器人与mark的距离distance

            markWithHeadAngle = round(markWithHeadAngle, 2)
            # 将数据存入列表
            robotToLandmarkData.append(distance)
            robotToLandmarkData.append(markWithHeadAngle)
            # 记录日志
            logging.info("x = " + str(x))
            logging.info("y = " + str(y))
            logging.info("z = " + str(z))
            logging.info("nao与landmark的距离 :: " + str(distance) + "   角度:: " + str(markWithHeadAngle * almath.TO_DEG))
            # 找到landmark，跳出循环
            break

        # 没找到landmark，该变角度继续扫视
        g_motion.angleInterpolationWithSpeed("HeadYaw", headYawAngle, 0.12)
        if headYawAngle * almath.TO_DEG < -130:
            headYawAngle = 130 * almath.TO_RAD  # 摆头角度，从右往左扫
            times += 1
            continue
        # elif times == 0:
        #     headYawAngle = headYawAngle + (55 * almath.TO_RAD)
        # elif times == 1:
        headYawAngle += addAngle
        # if headYawAngle
        # else:
        #     headYawAngle = headYawAngle - (20 * almath.TO_RAD)
    # 提示
    if not isFindLandmark:
        print "landmark is not in sight !"
        g_tts.say("landmark is not in sight")
    # 取消事件
    g_landmarkDetection.unsubscribe("landmarkTest")
    g_camera.unsubscribe("AL::kTopCamera")
    g_camera.closeCamera(0)
    # 调整头的角度
    g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.2)
    g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.2)
    return robotToLandmarkData, isFindLandmark


# -------------找到球的一些行为--------------
def actionAfterFirstFindBall(distance, headYawAngle):
    """
    找到球后，正对球，调整距离
    :param distance: NAO与球的距离
    :param headYawAngle: NAO与球的角度
    :return:
    """
    logging.info("-----------------------actionAfterFirstFindBall----------------")
    # 正对
    move(theta=headYawAngle)
    # 计算距离
    distance, Angle, ballCoord = trackBall()
    moveDistance = distance - 15
    # 移动到指定距离
    if moveDistance > 40:
        move(30)
        distance, Angle, ballCoord = trackBall()
        actionAfterFirstFindBall(distance, Angle)
    else:
        move(x=moveDistance)
        # 再次正对
        time.sleep(0.5)
        distance, Angle, ballCoord = trackBall(18)
        times = 0
        # 防止找球不精确
        while abs(ballCoord[2]) > 50:
            distance2Ball, headYawAngle, ballCoord = trackBall(18)
            times += 1
            if times > 5:
                g_tts.say("ball data error,I can't continue")
                stop()
                exit(2)
        move(theta=Angle)
        # 一些意外情况处理
        if distance < 13 or distance > 17:
            move(distance - 15)


# -------------一---------------------些计算---------------------------------
# 利用了一些简单的三角函数
def calDistanceFromBall2Mark(distance2Ball, distance2Mark, angleForLandMark):
    # type: (float, float, float) -> float
    '''
    根据nao与球的距离，nao与landmark的距离以及角度，计算球和landmark的距离
    :param distance2Mark: ao与球的距离 cm
    :param angleForLandMark: nao与landmark的角度 弧度值表示
    :param distance2Ball: nao与landmark的距离 cm
    :return:球和landmark的距离
    '''
    logging.debug("--------------------------calDistanceFromBall2Mark---------------------")
    logging.info("distance2Ball:: " + str(distance2Ball))
    logging.info("distance2Mark:: " + str(distance2Mark))
    logging.info("angleForLandMark:: " + str(angleForLandMark))
    distanceFromBall2Mark = math.sqrt(
        distance2Ball ** 2 + distance2Mark ** 2 - 2 * distance2Mark * distance2Ball * (math.cos(abs(angleForLandMark))))
    logging.info("distanceFromBall2Mark-->" + str(distanceFromBall2Mark))
    return round(distanceFromBall2Mark, 2)


def calAdjustY(distance2Ball, distance2Mark, angleForLandMark, distanceFromBall2Mark):
    """
    根据nao与球的距离，nao与landmark的距离以及角度，计算形成直角需要修正的Y值
    :param distanceFromBall2Mark: 球和landmark的距离
    :param distance2Ball: nao与landmark的距离 cm
    :param distance2Mark: ao与球的距离 cm
    :param angleForLandMark: nao与landmark的角度 弧度值表示
    :return: 需要修正的Y值
    """
    logging.debug("--------------------------calAdjustY---------------------")
    angleForBall = math.acos((distance2Ball - distance2Mark * math.cos(abs(angleForLandMark))) / distanceFromBall2Mark)
    logging.debug("angleForBall ---> " + str(angleForBall))
    distanceY = math.tan(abs(angleForBall - math.pi / 2)) * distance2Ball
    adjustTheta = -abs(math.pi / 2 - angleForBall)
    if angleForLandMark > 0 and (angleForBall - math.pi / 2) < 0:
        distanceY = -distanceY
        adjustTheta = -adjustTheta
    elif angleForLandMark < 0 and (angleForBall - math.pi / 2) > 0:
        distanceY = -distanceY
        adjustTheta = -adjustTheta
    logging.info("distanceY-->" + str(distanceY) + "  adjustTheta-->" + str(adjustTheta * almath.TO_DEG))
    return round(distanceY, 2), round(adjustTheta * almath.TO_DEG, 1)


def findAndHitBall2(changci=1):
    distanceFromBall2Mark = None
    robotToLandmarkData = []
    distance, headYawAngle, ballCoord = trackBall()
    for times in xrange(1):
        # 4.1、找到球
        if distance != -1:
            # 5、调整与球之间的距离
            actionAfterFirstFindBall(distance, headYawAngle)
            print "Before find mark"
            # 6、找Landmark
            distanceToLandmark = 0
            if changci != 2:
                if headYawAngle < 0:
                    robotToLandmarkData, isFind = searchLandmarkInLeft()
                else:
                    robotToLandmarkData, isFind = searchLandmarkInRight()
            else:
                robotToLandmarkData, isFind = searchLandmarkInRight()
            # for i in range(2):
            #     distanceToLandmark += robotToLandmarkData[0]
            #     robotToLandmarkData, isFind = searchLandmark()
            # logging.debug("NAO与landMark的距离:  " + str(robotToLandmarkData[0]) + "  角度:  " + str(robotToLandmarkData[1]))
            # robotToLandmarkData[0] = distanceToLandmark / 3
            # 6.1、找landmark
            if isFind:
                # 7、调整角度
                # 7.1 重新计算与球的距离,并获取球与landmark的距离
                distance2Ball, headYawAngle, ballCoord = trackBall(18)
                # 防止数据异常
                for i in range(5):
                    if abs(ballCoord[2]) > 50:
                        distance2Ball, headYawAngle, ballCoord = trackBall(18)
                    else:
                        break
                # 一些修正：将NAO与的距离修正至脚后心
                # if headYawAngle < 0:
                # if robotToLandmarkData[1] < 0:
                #     print "right"
                #     distance2Ball += (15 - distance2Ball) + 15 # 右边15
                #     if robotToLandmarkData[0] < 55:
                #         distance2Ball-=5
                # else:
                #     print "left"
                #     if robotToLandmarkData[0] < 35:
                #         distance2Ball+=2
                #     distance2Ball += 3.5 #左边
                print "adjustTwice"
                distance2Ball += (15 - distance2Ball) + 13  # 右边15
                if robotToLandmarkData[0] < 45:
                    distance2Ball -= 2
                # robotToLandmarkData[0]

                distanceFromBall2Mark = calDistanceFromBall2Mark(distance2Ball, robotToLandmarkData[0],
                                                                 robotToLandmarkData[1])
                # logging.info("distanceFromBall2Mark:  " + str(distanceFromBall2Mark))
                # 7.2、计算需移动的y值
                adjustY, adjustTheta = calAdjustY(distance2Ball, robotToLandmarkData[0], robotToLandmarkData[1],
                                                  distanceFromBall2Mark)

                # 7.3 调整距离和角度
                # time.sleep(0.5)
                if 28 > adjustY > -28:
                    move(y=adjustY)
                elif adjustY > 0:
                    move(y=28)
                else:
                    move(y=-28)
                # time.sleep(0.5)
                move(theta=adjustTheta)
                if adjustY > 25 or adjustY < -25:
                    findAndHitBall()
                else:
                    # 7.4 、调整至击球点
                    firstClosingForHitBall(robotToLandmarkData[1])
                    # 重新获取数据
                    # distance2Ball_2, headYawAngle_2, ballCoord_2 = trackBall(18)
                    # if headYawAngle < 0:
                    #     robotToLandmarkData_2, isFind = searchLandmarkInLeft()
                    #     distance2Ball_2+=15
                    # else:
                    #     robotToLandmarkData_2, isFind = searchLandmarkInRight()
                    #     distance2Ball_2+=5.5
                    # if isFind:
                    #     logging.info("-----------第一种------------")
                    #     distanceFromBall2Mark_2 = calDistanceFromBall2Mark(distance2Ball_2, robotToLandmarkData_2[0],
                    #                                                      robotToLandmarkData_2[1])
                    #     adjustY_2, adjustTheta_2 = calAdjustY(distance2Ball_2, robotToLandmarkData_2[0], robotToLandmarkData_2[1],
                    #                                       distanceFromBall2Mark_2)
                    #     adjustX = distance2Ball_2 - distance2Ball_2 * math.sin(abs(adjustTheta_2))
                    #     logging.info("adjustX:::" + str(adjustX))
                    #     logging.info("-----------第二种------------")
                    #     L = math.sqrt(distance2Ball_2**2 - ballCoord_2[1]**2)
                    #     distanceFromBall2Mark_2 = calDistanceFromBall2Mark(L, robotToLandmarkData_2[0],
                    #                                                      robotToLandmarkData_2[1])
                    #     adjustY_2, adjustTheta_2 = calAdjustY(L, robotToLandmarkData_2[0], robotToLandmarkData_2[1],
                    #                                       distanceFromBall2Mark_2)
                    #     adjustX_2 = L -  L * math.sin(abs(adjustTheta_2))
                    #     logging.info("adjustX_2:::"+str(adjustX_2))

                    g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.1)
                    g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.1)
                    # times = times + 1
                    # for i in xrange(3):
                    #     robotToLandmarkData, isFind =   searchLandmark()
                    # logging.info("最后的NAO与landMark的距离:  " + str(robotToLandmarkData[0]) + "  角度:  " + str(robotToLandmarkData[1]))
                    # logging.info("球与landmark的距离: " + str(distanceFromBall2Mark))
                    # distance2Ball, headYawAngle, ballCoord = trackBall(18)
                    # distanceFromBall2Mark = calDistanceFromBall2Mark(distance2Ball, robotToLandmarkData[0],
                    #                                                  robotToLandmarkData[1])
                    #
                    # # 7.2、计算需移动的y值
                    # adjustTheta = calAdjustTheta(distance2Ball, robotToLandmarkData[0], robotToLandmarkData[1],
                    #                      distanceFromBall2Mark)* almath.TO_DEG
                    # move(theta=adjustTheta )
                    # 7.5 击球
                    # 根据位置的不同决定击球方式
                    if distanceFromBall2Mark != None:
                        if robotToLandmarkData[1] > 0:
                            outShotBall(120)
                        elif robotToLandmarkData[1] < 0:
                            insideShotBall(120)
                            # 收杆
                    actionBeforeMove()
                    break
            # 判断击球次数
            # if times > 2:
            #     break

            # 没找到landmark
            else:
                pass
        # 没找到球
        else:
            return False
    return True


# ---------------------------击球相关-----------------------------
def insideShotBall(distance):
    # // 第二次击球的准备动作（内击）
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", 0.5, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowYaw", -1.8, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowRoll", -0.83, 0.2)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.6, 0.05)
    g_motion.angleInterpolationWithSpeed("LShoulderRoll", -1.5, 0.2)
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", 0.837, 0.05)

    # time.sleep(4)

    # // 击球（内击）
    g_motion.angleInterpolationWithSpeed("LWristYaw", -0.4, 0.12)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)


def outShotBall(distance):
    # distance 球到naomark的距离,以厘米为单位

    # // 第二次击球的准备动作（外击）
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.0, 0.05)
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", 0.2, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowYaw", -1.8, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowRoll", -0.83, 0.2)
    g_motion.angleInterpolationWithSpeed("LShoulderRoll", -1.5, 0.2)
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", 0.837, 0.05)

    # time.sleep(4)

    # // 击球（外击）
    g_motion.angleInterpolationWithSpeed("LWristYaw", -0.1, 0.1)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.8, 0.085)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)


def firstClosingForHitBall(angleForLandMark):
    """
    根据与landmark的角度的正负决定击球方式，先确定击球点在进行调整
    :param angleForLandMark:
    :return:
    """
    # 1、重新获取距离
    # distance2Ball, headYawAngle, ballCoord = trackBall()
    # move(theta=headYawAngle)
    distance2Ball, headYawAngle, ballCoord = trackBall(18)
    times = 0
    while abs(ballCoord[2]) > 50:
        distance2Ball, headYawAngle, ballCoord = trackBall()
        if times > 5:
            g_tts.say("ball data error,I can't continue")
            stop()
            exit(2)
    # 2、判断机器人在球朝向Landmark的线上的哪边
    # 2.1、在左边，及angleForLandMark值为正
    # 调整距离与角度
    adjustY = ballCoord[1] - 4
    move(y=adjustY)
    distance2Ball, headYawAngle, ballCoord = trackBall(18)
    times = 0
    while abs(ballCoord[2]) > 50:
        distance2Ball, headYawAngle, ballCoord = trackBall(18)
        if times > 5:
            g_tts.say("ball data error,I can't continue")
            stop()
            exit(2)
    adjustX = distance2Ball - 9
    move(x=adjustX)
    if angleForLandMark > 0:

        # 微调
        for t in range(2):
            # 微调y
            # 重新获取与球相关的值
            distance2Ball, headYawAngle, ballCoord = trackBallNoHead(18)
            while distance2Ball > 15 or ballCoord[2] > 30:
                distance2Ball, headYawAngle, ballCoord = trackBallNoHead(18)

            if (1 < ballCoord[1] < 6) or (t % 2 == 1):
                if 7.8 < distance2Ball < 9.5:
                    break
                else:
                    # print("x")
                    move(x=distance2Ball - 9)
            elif ballCoord[1] < 1:
                #     print("y")
                move(y=-2)
            elif ballCoord[1] > 6:
                #     print("y")
                move(y=2)
        # 判断？
        # 击球
        pass
    # 2.2 右边
    else:
        # 微调
        for t in range(2):
            # 微调y
            # 重新获取与球相关的值
            distance2Ball, headYawAngle, ballCoord = trackBallNoHead(18)
            while distance2Ball > 15 or ballCoord[2] > 30:
                distance2Ball, headYawAngle, ballCoord = trackBallNoHead(18)
            if (2 < ballCoord[1] < 4) or (t % 2 == 1):
                if 7.8 < distance2Ball < 9.5:
                    break
                else:
                    print("x")
                    move(x=distance2Ball - 9)
            elif ballCoord[1] < 1:
                # print("y")
                move(y=-2)
            elif ballCoord[1] > 6:
                print("y")
                move(y=2)


# -------下摄像头找球--------------------
def trackBallNoHead(headPitch=0):
    # 全局变量
    global g_camera, g_tracker, g_motion, g_tts
    # 需返回的参数
    headYawAngle = -1  # 头转过的角度
    distance = -1  # 球坐标
    coord = [0.0, 0.0, 0.0]
    # 一些后面需要用的参数
    times = 0  # 扭头次数
    yawDegree = 60 * almath.TO_RAD
    # 启用下摄像头
    g_camera.setActiveCamera(1)
    # 注册追踪物
    g_tracker.registerTarget(ball['name'], ball['diameter'])
    # 设置追踪模式
    g_tracker.setMode("Head")
    # 启动追踪
    g_tracker.track(ball['name'])
    # 睡眠2秒,给机器人追踪时间
    time.sleep(2)
    # 找球
    # 将机器人头设置到指定位置
    if headPitch != 0:
        g_motion.angleInterpolationWithSpeed("HeadPitch", headPitch * almath.TO_RAD, 0.1)
    while True:
        time.sleep(1)
        # 追踪到球
        if len(g_tracker.getTargetPosition(2)) == 3:
            # g_tts.say("got it")
            # 以脚部坐标系获取坐标
            coord = g_tracker.getTargetPosition(2)
            for i in range(2):
                coord = g_tracker.getTargetPosition(2)
            # 将坐标转换为cm
            for i in range(len(coord)):
                coord[i] *= 100
            # 输出坐标
            # logging.debug("x = " + str(coord[0]) + "  y = " + str(coord[1]) + " z = " + str(coord[2]))
            # 获取头转的角度
            headYawAngle = g_motion.getAngles("HeadYaw", True)[0] * almath.TO_DEG
            headPitchAngle = g_motion.getAngles("HeadPitch", True)[0] * almath.TO_DEG
            # 打印
            # logging.debug("headYawAngle:" + str( headYawAngle[0] * almath.TO_DEG) + "度")
            # logging.debug("headPitchAngle:" + str(headPitchAngle[0] * almath.TO_DEG) + "度")
            logging.debug(str(coord[0]) + "    " + str(coord[1]) + "   " + str(coord[2]) + "    " + str(
                headYawAngle) + "   " + str(headPitchAngle))

            distance = getRealDisForBall(coord[0], coord[1], coord[2], headYawAngle, headPitchAngle)
            # print("distance:", distance)
            logging.info("nao与球的距离::" + str(distance) + "    角度::" + str(headYawAngle))
            # 跳出循环
            break
        # 没找到球
        else:
            # 判断扭头次数，扫描3遍
            if times < 6:
                # 先扭头往右边观察
                if times > 2:
                    # g_camera.setActiveCamera(0)
                    g_motion.setAngles("HeadPitch", 18 * almath.TO_RAD, 0.1)
                if times % 3 == 0:
                    g_motion.angleInterpolationWithSpeed("HeadYaw", -yawDegree, 0.1)
                    times += 1
                    time.sleep(0.5)
                elif times % 3 == 2:
                    g_motion.angleInterpolationWithSpeed("HeadYaw", 0, 0.1)
                    times += 1
                    time.sleep(0.5)
                else:
                    g_motion.angleInterpolationWithSpeed("HeadYaw", yawDegree, 0.1)
                    times += 1
                    time.sleep(0.5)
                    # logging.info("转头次数:" + str(times))
                    print("转头次数:" + str(times))
            else:
                g_tts.say("ball not in sight")
                break

    # 停止追踪
    g_tracker.stopTracker()
    g_tracker.unregisterTarget(ball['name'])

    # 复原头
    # g_motion.angleInterpolationWithSpeed("HeadPitch",headPitch * almath.TO_RAD, 0.1)
    g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.1)

    # 输出球坐标和角度
    # logging.debug("球修正后坐标cm: " + str(coord))
    # logging.debug("机器人扭头角度:" + str(headAngle[0]))
    # 返回距离和角度
    return distance, headYawAngle, coord


def actionBeforeMove():
    """
    走路前的拿杆动作 ,打完球后收杆
    """
    global g_motion
    # // moveInit动作
    g_motion.moveInit()

    # // 打完球为走路做准备的动作
    g_motion.angleInterpolationWithSpeed("LShoulderRoll", 0.25, 0.2)
    g_motion.angleInterpolationWithSpeed("LElbowRoll", 0.0, 0.2)
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", 1.5, 0.2)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.3, 0.2)

    g_motion.angleInterpolationWithSpeed("RElbowRoll", 0.0, 0.2)
    g_motion.angleInterpolationWithSpeed("RShoulderPitch", 1.5, 0.2)
    # g_motion.angleInterpolationWithSpeed("RShoulderRoll", -0.1, 0.2)

    g_motion.setMoveArmsEnabled(False, False)


def getRealDisForBall(x, y, z, yaw, pitch):
    '''
    根据api返回的数据，计算真正的距离
    :param x:
    :param y:
    :param z:
    :param yaw:
    :param pitch:
    :return:
    '''
    # 初始化一些数据
    z = abs(z)
    # 获取
    dis1 = math.sqrt(x ** 2 + y ** 2)
    dis_z = dis1 - z
    print("dis1:", dis1)
    print("dis_z:", dis_z)
    # 以下处理通过分析数据获得，基本依照2017-7-19的数据（注:现在需要改进）
    if dis1 < 10:
        # 未找到球
        return
    elif dis1 < 20.59 and z < 25 or (dis_z < 5 and z < 25):
        # 距离在0-5cm之间
        # if z > 20:
        #     distance = dis1 - 15
        # else:
        #     distance = dis1 - 14
        # 另一种处理方式
        distance = (dis1 - (z - 13.31) / 3.92 - 14.47) / 0.918
    elif dis1 < 27.12 or dis_z < 9.61:
        # 5 -10
        # print("5-10")
        logging.debug("5-10")
        distance = (dis1 - (z - 13.19) / 2.55 - 19.19) / 1.262 + 5
    elif dis1 < 40.47 or dis_z < 9.94:
        # 10-15
        logging.debug("10-15")
        distance = (dis1 - (z - 20.23) / 2.12 - 28.36) / 1.424 + 10
    elif dis1 < 51.43 or (dis_z < 17.69 and z < 50):
        # 15-20
        logging.debug("15-20")
        distance = (dis1 - (z - 25.17) / 1.67 - 40) / 1.582 + 15
    elif dis1 < 53.14 or dis_z < 30:
        # 20- 25
        logging.debug("20-25")
        distance = (dis1 - (z - 25) / 1.37 - 46.52) / 1.6 + 20
    elif dis1 < 58.94 or dis_z < 38.07:
        # 25- 30
        logging.debug("25-30")
        distance = (dis1 - (z - 15.80) / 1.13 - 47.55) / 1.416 + 25
    elif dis1 < 62.83 or dis_z < 46:
        # 30- 35
        logging.debug("30-35")
        distance = (dis1 - (z - 16.20) / 1.08 - 55) / 1.404 + 30
    elif dis1 < 85.20 or dis_z < 54.15:
        # 35 - 40
        logging.debug("35-40")
        distance = (dis1 - (z - 22.22) / 0.91 - 67.5) / 1.6 + 35
    elif dis_z < 67:
        # 40-45
        logging.debug("40-45")
        distance = (dis1 - (z - 18.46) / 0.86 - 71.74) / 1.358 + 40
    elif (dis1 < 120 and dis_z < 75) or (dis1 / z < 2.7 and dis_z < 85):
        # 45 - 50
        logging.debug("45-50")
        distance = (dis1 - (z - 27.21) / 0.78 - 88.73) / 1.542 + 45
    elif dis_z < 81.5 or (dis1 / z < 3.35 and dis1 < 116.5):
        # 50 - 55
        logging.debug("50-55")
        distance = (dis1 - (z - 22.91) / 0.72 - 92.17) / 1.488 + 50
    elif (dis_z < 87.5) or (dis1 > 152 and dis_z < 100.5):
        # 55-60
        logging.debug("55-60")
        distance = (dis1 - (z - 31.12) / 0.72 - 112.47) / 1.212 + 55
    elif dis_z < 96.5 or (dis1 > 150 and dis_z < 111.5 and z > 45):
        # 60-65
        logging.debug("60-65")
        distance = (dis1 - (z - 31.60) / 0.64 - 119) / 1.8 + 60
    elif dis_z < 106 or (dis1 > 158 and dis_z < 119.5 and z > 44):
        # 65 - 70
        logging.debug("65-70")
        distance = (dis1 - (z - 32.86) / 0.60 - 130.26) / 1.714 + 65
    elif dis_z < 123.5 or (dis1 > 163 and dis1 / z < 3.8):
        # 70-75
        logging.debug("70-75")
        distance = (dis1 - (z - 27.68) / 0.54 - 130.755) / 2.099 + 70
    else:
        # 75 -
        logging.debug("75-")
        distance = (dis1 - (z - 22.34) / 0.61 - 134.52) / 2.408 + 75
    return distance


# ------------上摄像头找球，使用opencv部分，此处不做注释-------------------
def searchBallUseTop():
    """
    适用上摄像头进行找球
    :return:
    """
    initAngle = -80
    endAngle = 80
    currAngle = initAngle
    distance = -1
    distance, angle = findRedBallUseTop()
    logging.info("----------------searchBallUseTop-------------------------")
    if distance > 0:
        headYawAngle = g_motion.getAngles("HeadYaw", True)
        angle = (angle + headYawAngle) * almath.TO_DEG
        return distance, angle
    while currAngle <= endAngle:
        # 找到球
        if distance > 0:
            break
        distance, angle = findRedBallUseTop()
        g_motion.angleInterpolationWithSpeed("HeadYaw", currAngle * almath.TO_RAD, 0.2)
        time.sleep(2)
        currAngle += 40
    headYawAngle = g_motion.getAngles("HeadYaw", True)[0]
    angle = (angle + headYawAngle) * almath.TO_DEG

    logging.info("distance: %f" % distance + "______________angle: %f" % (angle * almath.TO_DEG))
    # move(theta=angle * almath.TO_DEG)
    return distance, angle


def findRedBallUseTop():
    """
    使用上摄像头找球
    :return:
    """
    distance = 0
    angle = 0
    g_videoDevice = ALProxy("ALVideoDevice", IP, Port)
    # get NAOqi module proxy
    # videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)
    # motionProxy = ALProxy("ALMotion", ip_addr, port_num)
    # postureProxy = ALProxy("ALRobotPosture", ip_addr, port_num)
    # memoryProxy = ALProxy("ALMemory", ip_addr, port_num)
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

    for times in xrange(10):
        print times
        image = np.zeros((height, width, 3), np.uint8)
        # get image
        result = g_videoDevice.getImageRemote(captureDevice)

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

            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            blur1 = cv2.GaussianBlur(hsv, (0, 0), 1)
            # define range of red color in HSV
            lower_red = np.array([156, 65, 65])
            upper_red = np.array([180, 255, 255])
            # Threshlod the HSV image to get only red colors
            mask = cv2.inRange(hsv, lower_red, upper_red)

            # Bitwise-AND mask and original image
            red = cv2.bitwise_and(hsv, hsv, mask=mask)

            # 形态学处理
            img1 = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)
            img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

            _, thresh = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # 做一些形态学操作，去一些小物体的干扰
            img_morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (1, 1))
            cv2.erode(img_morph, (1, 1), img_morph, iterations=1)

            # dilate = cv2.dilate(img_morph, (1, 1), img_morph, iterations=1)

            blur = cv2.GaussianBlur(img_morph, (0, 0), 1)

            # cv.Smooth(blur, blur, cv.CV_MEDIAN)

            kernel = np.ones((0, 0), np.uint8)

            # canny = cv2.Canny(blur, 0, 250)

            # threshold image
            ret, threshed_img = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

            # ret, threshed_img = blur
            # find contours and get the external one
            image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # if not find contours, then print"Not find ball"
            if len(contours) == 0 and times > 5:
                print 'Not find ball'
                FindBall = 0
                # return FindBall
                break
            else:
                n = 0
                minContourArea = 3.0
                maxContourArea = 100.0
                contourTempArea = 0.0

                for c in contours:
                    # get the bounding rect
                    x, y, w, h = cv2.boundingRect(c)
                    print x, y, w, h

                    # 过滤太远的噪点,190cm以后的不用识别,主要过滤场外的复杂场景
                    if y <= height / 2:
                        n += 1
                        if n == len(contours) and times > 5:
                            FindBall = 0
                            print "Not find ball"
                            # return FindBall
                            break
                        continue

                    # 图片下方的发现点,75cm-190cm
                    elif y >= height / 2:
                        contoursArea = cv2.contourArea(c)
                        print "\nArea:", contoursArea
                        if minContourArea < contoursArea <= maxContourArea:
                            useSensors = False
                            headAngle = g_motion.getAngles('HeadPitch', useSensors)
                            center_x = x + w / 2
                            center_y = y + h / 2
                            distance, angle = calDistanceAndAngle(center_x, center_y, width, height, headAngle[0],
                                                                  AL_kTopCamera)
                            # cv2.imshow('blur1', blur1)
                            # 在下方发现有点之后就停止，因为在腐蚀的时候可能会将一个圆分为几块会出现这种情况
                            break
            if distance > 0:
                break
                # k = cv2.waitKey(0) & 0xFF
                #
                # if k == 27:
                #     break

                # cv2.destroyAllWindows()
                # cv2.waitKey()
    try:
        g_videoDevice.releaseImage(captureDevice)
        g_videoDevice.unsubscribe(captureDevice)
    except Exception, e:
        print "Error", e
        pass
    finally:
        return distance, angle


def calDistanceAndAngle(cxnum, rynum, colsum, rowsum, Head_angle, cameraID):
    """
    上摄像头找到球后计算距离和角度
    :param cxnum:
    :param rynum:
    :param colsum:
    :param rowsum:
    :param Head_angle:
    :param cameraID:
    :return:
    """
    distx = -(cxnum - colsum / 2)
    disty = rynum - rowsum / 2
    print "coordinate:", distx, disty
    # print disty

    Picture_angle = disty * 47.64 / 240

    if cameraID == 0:
        h = 0.463
        Camera_angle = 4.7145
        print "Head_angle:", Head_angle

    else:
        h = 0.57
        Camera_angle = 38

    print h, Picture_angle, Camera_angle

    Total_angle = math.pi * (Picture_angle + Camera_angle) / 180 + Head_angle

    print math.pi, Picture_angle, Total_angle

    d1 = h / math.tan(Total_angle)
    print "distance_y：", d1

    alpha = math.pi * (distx * 60.92 / 320) / 180
    d2 = d1 / math.cos(alpha)
    print 'angle = ', alpha, 'distance = ', d2
    return d2, alpha


# 第一个场地
def secondMain2():
    """第二场"""
    # 1、初始化日志配置、加载模块、站立，接杆
    naoInit()
    # times = 0  # 除固定击球以外击球次数
    # 第一次击球
    firstHitBallForTwo()
    # 收杆
    actionBeforeMoveForTwo()
    move(theta=77)  # 旋转
    move(y=15)  # 左右移动
    move(theta=2)
    move(x=336)  # 前后移动
    move(y=-15)
    g_tts.say('first move over')
    flag = findAndHitBall(changci=2)
    if not flag:
        g_tts.say("now I use top to find ball")
        distance, angle = searchBallUseTop()
        # 上摄像头找到球
        if distance > 0:
            move(theta=angle)
            move(distance - 60)
            findAndHitBall(changci=2)
    stop(2)


g_motion.wakeUp()
secondMain2()

# 往左边打 往左上方走（4-5米），找球，找landmark，
