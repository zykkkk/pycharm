# -*- coding:utf-8 -*-

from naoqi import ALProxy

IP='169.254.46.69'
Port=9559
g_tts = g_motion = g_posture = g_memory = g_camera = g_landmarkDetection = g_tracker = g_videoDevice= None
# 加载所需模块
def loadModule(IP="127.0.0.1", Port=9559):
    global g_tts, g_motion, g_posture, g_memory, g_camera, g_landmarkDetection, g_tracker
    g_tts = ALProxy("ALTextToSpeech", IP, Port)  # 说话模块
    g_motion = ALProxy("ALMotion", IP, Port)  # 移动模块
    g_posture = ALProxy("ALRobotPosture", IP, Port)  # 姿势模块
    g_memory = ALProxy("ALMemory", IP, Port)  # 内存管理模块
    g_camera = ALProxy("ALVideoDevice", IP, Port)  # 摄像头管理模块
    g_landmarkDetection = ALProxy("ALLandMarkDetection", IP, Port)  # landMark检测模块
    g_tracker = ALProxy("ALTracker", IP, Port)  # 追踪模块
    g_videoDevice=ALProxy("ALVideoDevice", IP, Port)

# loadModule()
g_tts=ALProxy('ALTexTtoSpeech',IP,Port)
# g_motion.wakeup()
g_tts.say('Im  nao')
