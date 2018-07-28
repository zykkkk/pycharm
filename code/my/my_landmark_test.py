# coding:utf8
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
g_camera = ALProxy("ALVideoDevice", IP, Port)  # 摄像头管理模块
g_tracker = ALProxy("ALTracker", IP, Port)  # 追踪模块


def findAndHitBall(changci=1):
    # isFind=0
    distanceFromBall2Mark = None
    robotToLandmarkData = []
    # 此处经修改后暂无意义
    headYawAngle = g_motion.getAngles("HeadYaw", True)
    for times in xrange(1):
        # 4.1、找到球
            # 5、调整与球之间的距离
            # 6、找Landmark
            # distanceToLandmark = 0
        if changci != 2:
            if headYawAngle < 0:
                # g_tts.say('not find landmark')
                # g_motion.rest()
                robotToLandmarkData, isFind = searchLandmarkInLeft()
            else:
                robotToLandmarkData, isFind = searchLandmarkInRight()
        else:
            robotToLandmarkData, isFind = searchLandmarkInRight()
        # 没找到，继续扫
        if not isFind:
            if changci != 2:
                if headYawAngle < 0:
                    searchLandmarkInRight()
                else:
                    # g_tts.say('not find landmark')
                    robotToLandmarkData, isFind = searchLandmarkInLeft()
            else:
                # g_tts.say('not find landmark')
                robotToLandmarkData, isFind = searchLandmarkInLeft()
    print changci
    changci+=1



# ----------------------------Landmark相关---------------------------------
def searchLandmarkInRight():
    '''
    搜索Landmark，返回
    :return:landmarkData(角度，距离),isFindLandMark
    '''
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

            distance = math.sqrt(x ** 2 + y * y) * 100
            print distance
            markWithHeadAngle = round(markWithHeadAngle, 2)
            print markWithHeadAngle
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
            print distance

            markWithHeadAngle = round(markWithHeadAngle, 2)
            print markWithHeadAngle
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


g_motion.wakeUp()
findAndHitBall()
# g_tts.say('hit over')
# searchLandmarkInRight()
# g_motion.rest()
