# coding:utf8
from naoqi import ALProxy
import math
import almath
import time
import logging
import sys

IP = '192.168.1.102'
# IP = '172.16.55.80'
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


def naoInit():  #
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


def firstHitBallForOne():
    """
        第一场第一次击球
    """
    g_motion.angleInterpolationWithSpeed("LWristYaw", 1.2, 0.1)
    g_motion.angleInterpolationWithSpeed("LWristYaw", -0.6, 0.3)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)
    print('hit over')


def actionBeforeMove():
    """
    走路前的拿杆动作 ,打完球后收杆
    """
    # global g_motion
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
    print('action before move over')


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
        g_motion.rest()
        sys.exit()
        # stop()


def find_ball():
    g_motion.setStiffnesses("Head", 1.0)
    g_camera.setActiveCamera(1)
    # 注册追踪物
    g_tracker.registerTarget(ball['name'], ball['diameter'])
    # 设置追踪模式
    g_tracker.setMode("Head")
    # 启动追踪
    g_tracker.track(ball['name'])
    g_tts.say('begin to find ball')
    for i in range(14):
        j = i / 7
        k = i % 7
        if j > 0:
            anger = almath.TO_RAD * (-k * 30 + 90)
        else:
            anger = almath.TO_RAD * (k * 30 - 90)
        g_motion.angleInterpolationWithSpeed("HeadYaw", anger, 0.15)  # set head anger
        # 睡眠2秒,给机器人追踪时间
        time.sleep(1)
        if len(g_tracker.getTargetPosition(2)) == 3:
            g_tts.say('find ball')
            # time.sleep(1)
            # 以脚部坐标系获取坐标
            coord = g_tracker.getTargetPosition(2)  # coord is 坐标系 2 is 脚部
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
            distance = getRealDisForBall(coord[0], coord[1], coord[2], headYawAngle, headPitchAngle)
            g_tracker.stopTracker()
            g_tracker.unregisterTarget(ball['name'])
            return round(distance, 2), round(headYawAngle, 4), coord
        else:
            g_tts.say('can not find ball %d time' % i)
    time.sleep(1)
    g_tts.say('have not found ball , over')
    return -1, -1, -1


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


def searchLandmark(turn='left'):
    """
    搜索Landmark，返回
    :return:landmarkData(角度，距离),isFindLandMark
    """
    isFindLandmark = False  # landmark识别符0代表识别到，1代表未识别到。
    robotToLandmarkData = []

    # 设置刚度为 1 保证其头部能够运转
    g_motion.setStiffnesses("Head", 1.0)
    # 开启上摄像头
    g_camera.setActiveCamera(0)
    # 注册事件
    g_landmarkDetection.subscribe("landmarkTest")

    if turn == 'left':
        a = 1
    elif turn == 'right':
        a = -1
    else:
        a = 0

    # g_tts.say('begin to find landmark in %s' %turn)
    print ('begin to find landmark in %s' %turn)

    for i in range(8):
        j = i / 4
        k = i % 4
        if j == 0:
            anger = almath.TO_RAD * (k * 30) * a
        else:
            anger = almath.TO_RAD * (90 - k * 30) * a

        # g_motion.angleInterpolationWithSpeed("HeadPitch", anger, 0.1)   #
        g_motion.angleInterpolationWithSpeed("HeadYaw", anger, 0.1)   #
        time.sleep(3)
        markData = g_memory.getData("LandmarkDetected")

        if markData and isinstance(markData, list) and len(markData) >= 2:
            # 提示
            # g_tts.say("find landmark!")
            print ("find landmark!")
            # 置标志为rue
            isFindLandmark = True  # landmark识别符1代表识别到，0代表未识别到。
            # Retrieve landmark center position in radians.
            # 获取数据
            alpha = markData[1][0][0][1]
            beta = markData[1][0][0][2]
            landmarkWidthInPic = markData[1][0][0][3]   # Retrieve landmark angular size in radians.
            print ('there',alpha,beta,landmarkWidthInPic)

            # 获取头转动角度
            headAngle = g_motion.getAngles("HeadYaw", True)  # 视觉中心
            markWithHeadAngle = alpha + headAngle[0]  # landmark相对机器人头的角度  ,视觉中心 + 视觉中的角度  ,为毛不需要上下的角度
            print('markWithHeadAngle:  ',markWithHeadAngle)
            # 头部正对landmark
            g_motion.angleInterpolationWithSpeed("HeadYaw", markWithHeadAngle, 0.2)

            # ----------------------------------计算距离-----------------------------------------------#
            distanceFromCameraToLandmark = landmark["size"] / (2 * math.tan(landmarkWidthInPic / 2))

            # 获取当前机器人到摄像头的距离的变换矩阵
            transform = g_motion.getTransform("CameraTop", 2, True)
            transformList = almath.vectorFloat(transform)
            robotToCamera = almath.Transform(transformList)

            # 计算指向landmark的旋转矩阵
            cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, beta, alpha)
            print('cameraToLandmarkRotationTransform:  ',cameraToLandmarkRotationTransform)

            # 摄像头到landmark的矩阵
            cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)
            print('cameraToLandmarkTranslationTransform: ',cameraToLandmarkTranslationTransform)

            # 机器人到landmark的矩阵
            robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform
            print('robotToLandmark:  ',robotToLandmark)

            x = robotToLandmark.r1_c4  # 1row  4cloumn
            y = robotToLandmark.r2_c4
            z = robotToLandmark.r3_c4
            distance = math.sqrt(x ** 2 + y * y) * 100
            print ('distance  ',distance)

            markWithHeadAngle = round(markWithHeadAngle, 2)
            # 将数据存入列表
            robotToLandmarkData.append(distance)
            robotToLandmarkData.append(markWithHeadAngle)
            # 取消事件
            g_landmarkDetection.unsubscribe("landmarkTest")
            g_camera.unsubscribe("AL::kTopCamera")
            # 调整头的角度
            g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.2)
            g_motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.2)
            return robotToLandmarkData, isFindLandmark
        else:
            # g_tts.say('not find landmark %d time' % i)
            print ('not find landmark %d time' %i)

    g_tts.say("landmark is not in sight,over")
    return -1, -1


if __name__ == '__main__':
    # naoInit()
    # firstHitBallForOne()
    # move(theta=-90)  # zuo +
    # move(x=200)  # qianhou
    g_motion.wakeUp()
    # find_ball()
    searchLandmark(turn='left')
    # searchLandmark(turn='right')
    # g_tts.say('i am going to rest')
    g_motion.rest()
    # g_posture.goToPosture("StandInit", 0.5)
    # g_motion.setStiffnesses("Head", 1.0)
    # g_motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.2)
    # g_motion.angleInterpolationWithSpeed("HeadYaw", 1.5, 0.2)
    # g_motion.angleInterpolationWithSpeed("HeadYaw", -1.5, 0.2)
    # g_motion.angleInterpolationWithSpeed("HeadYaw", 0, 0.2)