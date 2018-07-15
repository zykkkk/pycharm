

from naoqi import ALProxy
import logging
import Dialog
import almath
import sys


robotIP = '172.16.40.43'
PORT = 9559

landmark = {"size": 0.09}
ball = {'name': 'RedBall', 'diameter': 0.04}


print(landmark["size"])

# sys.exit(0)

try:
    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
except Exception,e:
    logging.error('haha')
    print('therer is at least one error')

