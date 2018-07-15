# coding:utf8
from naoqi import ALProxy
import math
import almath
import time
import logging

# IP = '172.16.55.80'
IP = '172.16.55.81'
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
    print('init over')


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


def firstHitBallForOne():
    """
        第一场第一次击球
    """
    g_motion.angleInterpolationWithSpeed("LWristYaw", 1.2, 0.1)
    g_motion.angleInterpolationWithSpeed("LWristYaw", -0.6, 0.3)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.4, 0.05)
    print('hit over')


def trackBall(headPitch=0):
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
    print g_camera.isCameraOpen(0)
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
            # g_tts.say("got it")
            # time.sleep(1)
            # 以脚部坐标系获取坐标
            coord = g_tracker.getTargetPosition(2)
            for i in range(2):
                coord = g_tracker.getTargetPosition(2)
            # 将坐标转换为cm
            for i in range(len(coord)):
                coord[i] = coord[i] * 100
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


def test():
    g_posture.goToPosture("StandInit", 0.5)  # 一个固定的姿势
    # time.sleep(2)
    g_motion.angleInterpolationWithSpeed("LWristYaw", 0.3, 0.2)  # 手腕旋转
    g_motion.angleInterpolationWithSpeed("LShoulderPitch", 0.77, 0.2)  # 手臂，胳膊抬起，放下
    g_motion.angleInterpolationWithSpeed("LShoulderRoll", -1.5, 0.2)  # 手臂，胳膊左右伸开，靠拢
    g_motion.angleInterpolationWithSpeed("LElbowRoll", -0.9, 0.2)  # 手肘旋转
    g_motion.angleInterpolationWithSpeed("LElbowYaw", -1.8, 0.2)  # 手肘左右

    g_motion.angleInterpolationWithSpeed("LHand", 1.0, 0.2)  # 伸开手指
    #
    time.sleep(2)
    g_motion.angleInterpolationWithSpeed("LHand", 0.5, 0.2)  # 合拢手指   yuan 0.15,0.2
    # g_motion.setStiffnesses("LHand", 1.0)


# g_motion.wakeUp()
# time.sleep(3)

# test()
# time.sleep(3)
# g_motion.rest()
# 第二个场地
# g_motion.wakeUp()
# naoInit()  # 站立，接杆wlp3s0
# time.sleep(1)
# firstHitBallForOne()  # 击球
# time.sleep(1)
# actionBeforeMove()  # 走路前的拿杆动作（也可以说收杆）
# time.sleep(1)
# g_motion.rest()
