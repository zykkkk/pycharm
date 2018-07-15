# -*- coding:utf-8 -*-

from naoqi import ALProxy
import time
import almath
import math
import logging
import cv2
import random
import numpy as np
import sys

# 原文第348行# ----------------------------Landmark相关---------------------------------
# 使用字典存储
landmark = {"size": 0.09}
ball = {'name': 'RedBall', 'diameter': 0.04}
# IP='169.254.46.69'
IP = '172.16.55.80'
Port = 9559
g_tts = g_motion = g_posture = g_memory = g_camera = g_landmarkDetection = g_tracker = g_videoDevice = None


def LoadModule():
    global g_tts, g_motion, g_posture, g_memory, g_camera, g_landmarkDetection, g_tracker,g_videoDevice
    g_tts = ALProxy("ALTextToSpeech", IP, Port)  # 说话模块
    g_motion = ALProxy("ALMotion", IP, Port)  # 移动模块
    g_posture = ALProxy("ALRobotPosture", IP, Port)  # 姿势模块
    g_memory = ALProxy("ALMemory", IP, Port)  # 内存管理模块
    g_camera = ALProxy("ALVideoDevice", IP, Port)  # 摄像头管理模块
    g_landmarkDetection = ALProxy("ALLandMarkDetection", IP, Port)  # landMark检测模块
    g_tracker = ALProxy("ALTracker", IP, Port)  # 追踪模块
    g_videoDevice = ALProxy("ALVideoDevice", IP, Port)


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
            print ("alpha: ",alpha)
            print ("beta: ", beta)
            print landmarkWidthInPic

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
        g_motion.angleInterpolationWithSpeed("HeadYaw", headYawAngle, 0.12)  # 改变头的角度
        if headYawAngle * almath.TO_DEG > 130:
            headYawAngle = -90 * almath.TO_RAD  # 摆头角度，从右往左扫
            times += 1
            continue
        # elif times == 0:
        #     headYawAngle = headYawAngle + (55 * almath.TO_RAD)
        # elif times == 1:
        headYawAngle = headYawAngle + (39 * almath.TO_RAD)
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
    '''
    搜索Landmark，返回
    :return:landmarkData(角度，距离),isFindLandMark
    '''
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
        if (markData and isinstance(markData, list) and len(markData) >= 2):
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
        headYawAngle = headYawAngle + addAngle
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


def searchLandmarkForAvoid():
    '''
    搜索Landmark，返回
    :return:landmarkData(角度，距离),isFindLandMark
    '''
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
    time.sleep(2.5)
    markData = g_memory.getData("LandmarkDetected")
    # 找到landmark
    if (markData and isinstance(markData, list) and len(markData) >= 2):
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
        # distance = math.sqrt((x+0.055)**2 + y * y) * 100  # 机器人与mark的距离distance
        # # 一些修正处理
        # x*=100
        # y*=100
        # l  = math.sqrt(x**2 + y * y)
        # modifyAngle =  math.asin((x+5.5)/distance) - math.asin(x/l)
        # logging.debug("modifyAngle:::::" + str(modifyAngle * almath.TO_DEG))
        # if markWithHeadAngle > 0:
        #     markWithHeadAngle-=modifyAngle
        # else:
        #     markWithHeadAngle+=modifyAngle
        # 修正值
        # distance = round( getRealDistanceForLandmark(distance, int(markWithHeadAngle * almath.TO_DEG) ), 2)

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

    # 提示
    if not isFindLandmark:
        print "landmark is not in sight !"
        g_tts.say("landmark is not in sight")
    # 取消事件
    g_landmarkDetection.unsubscribe("landmarkTest")
    g_camera.closeCamera(0)
    # 调整头的角度
    g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.2)
    g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.2)
    return robotToLandmarkData, isFindLandmark


LoadModule()
searchLandmarkInRight()
