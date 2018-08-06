# coding=utf-8
import random
import cv2
from naoqi import ALProxy
import almath
import numpy as np
import math
import time

a = 5
IP = "172.16.55.80"
Port = 9559

g_motion = ALProxy("ALMotion", IP, Port)  # 移动模块
g_videoDevice = ALProxy("ALVideoDevice", IP, Port)
g_motion.setStiffnesses("Head", 1.0)
g_posture = ALProxy("ALRobotPosture", IP, Port)  # 姿势模块
g_posture.goToPosture("StandInit", 0.5)
g_motion.rest()

